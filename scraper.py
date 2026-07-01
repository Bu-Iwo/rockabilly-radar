import json, requests, re, time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

OUTPUT_FILE = 'events.json'
VIP_BANDS = ["Ray Collins Hot Club", "The Firebirds", "Jukebox Stompers", "Boppin'B", "Restless", "Mad Sin", "Stray Cats", "Si Cranstoun"]

HARDCODED_EVENTS = [
    {"title": "Summer Jamboree 2026", "date": "01.08. - 09.08.2026", "location": "Senigallia, Italien", "city": "Senigallia", "lat": 43.7147, "lon": 13.2183, "desc": "Europas größtes Rockabilly-Festival.", "url": "https://www.summerjamboree.com", "genres": ["Rockabilly"]},
    {"title": "Firebirds Festival 2026", "date": "03.07. - 05.07.2026", "location": "Grimma, Deutschland", "city": "Grimma", "lat": 51.2294, "lon": 12.7561, "desc": "Rock'n'Roll im Kloster.", "url": "https://www.firebirds-festival.de", "genres": ["Rock'n'Roll"]},
    {"title": "Viva Las Vegas 2026", "date": "16.04. - 19.04.2026", "location": "Las Vegas, USA", "city": "Las Vegas", "lat": 36.1699, "lon": -115.1398, "desc": "Das weltgrößte Rockabilly-Event.", "url": "https://www.vivalasvegas.net", "genres": ["Rockabilly"]}
]

TARGETS = [
    {"name": "Noels Ballroom", "url": "https://noels-ballroom.de/", "city": "Leipzig"},
    {"name": "Tonelli's Leipzig", "url": "http://www.tonellis.de/programm.html", "city": "Leipzig"},
    {"name": "Tanzcafé Waldenburg", "url": "https://www.tanzcafe-waldenburg.de/", "city": "Waldenburg"},
    {"name": "Rockabilly Radio", "url": "https://www.rockabillyradio.net/events/", "city": "Diverse"},
    {"name": "Rock'n'Roll Calendar NL", "url": "https://www.rockabilly.nl/calendar.php", "city": "Diverse"}
]

def verify_genre(text):
    t = text.lower()
    positive = ['rockabilly', 'rock\'n\'roll', '50er', '60er', 'lindy hop', 'swing', 'boogie', 'vintage', 'psychobilly']
    negative = ['techno', 'house', 'metal', 'punk', 'hip hop', 'schlager', 'indie']
    if any(n in t for n in negative): return False
    if any(b.lower() in t for b in VIP_BANDS): return True
    has_date = bool(re.search(r'\d{1,2}\.\d{1,2}', text))
    return has_date and any(p in t for p in positive)

def get_coords(city):
    try:
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={city}, Germany&limit=1"
        resp = requests.get(url, headers={'User-Agent': 'RockabillyBot/1.0'}, timeout=5).json()
        if resp: return float(resp[0]['lat']), float(resp[0]['lon'])
    except: pass
    return None, None

def run_scraper():
    print(f"🚀 Scraper Start: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    events = list(HARDCODED_EVENTS)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    # Jukebox Stompers Spezial-Parser
    try:
        resp = requests.get("https://www.jukeboxstompers.de/index.php/veranstaltungen/veranstaltungskalender", headers=headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            for row in soup.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) >= 3:
                    date_t = cols[0].get_text(strip=True)
                    desc_t = cols[2].get_text(separator=" ", strip=True)
                    if date_t and verify_genre(desc_t):
                        city = cols[1].get_text(strip=True).split('\n')[0]
                        lat, lon = get_coords(city)
                        events.append({"title": f"Live @ Jukebox Stompers", "date": date_t, "location": city, "city": city, "lat": lat, "lon": lon, "desc": desc_t[:200], "url": "https://www.jukeboxstompers.de", "genres": ["Rockabilly"]})
                        print(f"   ✅ Jukebox: {date_t}")
    except Exception as e: print(f"   ❌ Jukebox Error: {e}")

    # Standard Webseiten
    for target in TARGETS:
        try:
            resp = requests.get(target['url'], headers=headers, timeout=10)
            if resp.status_code != 200: continue
            soup = BeautifulSoup(resp.text, 'html.parser')
            for el in soup.find_all(['p', 'li', 'div', 'h3']):
                text = el.get_text(separator=" ", strip=True)
                if len(text) > 15 and verify_genre(text):
                    date_m = re.search(r'\d{1,2}\.\d{1,2}\.?\s*(?:\d{4})?', text)
                    if date_m:
                        band = next((b for b in VIP_BANDS if b.lower() in text.lower()), None)
                        title = f"{band} @ {target['name']}" if band else f"Live @ {target['name']}"
                        lat, lon = get_coords(target['city'])
                        events.append({"title": title, "date": date_m.group(0), "location": f"{target['name']}, {target['city']}", "city": target['city'], "lat": lat, "lon": lon, "desc": text[:200], "url": target['url'], "genres": ["Rockabilly"]})
                        print(f"   ✅ {target['name']}: {title}")
            time.sleep(2)
        except Exception as e: print(f"   ❌ {target['name']}: {e}")

    # Vergangene Events filtern
    now = datetime.now()
    clean_events = []
    for ev in events:
        d = ev.get('date', '')
        if not d or d == "Termin folgt": 
            clean_events.append(ev)
            continue
        try:
            match = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})?', d)
            if match:
                day, month = int(match.group(1)), int(match.group(2))
                year = int(match.group(3)) if match.group(3) else now.year
                if datetime(year, month, day) >= (now - timedelta(days=1)):
                    clean_events.append(ev)
        except: clean_events.append(ev)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(clean_events, f, ensure_ascii=False, indent=2)
    print(f"💾 Fertig! {len(clean_events)} Events gespeichert.")

if __name__ == "__main__":
    run_scraper()
