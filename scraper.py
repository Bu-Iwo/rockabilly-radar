import json
import requests
from bs4 import BeautifulSoup
import re
import time

OUTPUT_FILE = 'events.json'

VIP_BANDS = [
    "Ray Collins Hot Club", "Ray Collins' Hot Club", "Ray Allen", "Class of 58", "The Firebirds",
    "Jumpin'Up", "Jumpin' Up", "The Nymonics", "The Trainyard Kings", "Shotgun Jones", 
    "Jukebox Stompers", "Boppin'B", "Cherry Casino", "The Baseballs",
    "Restless", "Matchbox", "Darrel Higham", "Mad Sin", "The Rattles",
    "Big Town Playboys", "Shakin' Stevens", "Stray Cats", "Rocky Sharpe",
    "The Jets", "The Cats", "Dave Phillips", "Kim Lenz", "The Hot Rods",
    "George And His New Heartaches", "Marty's Henpecked Club", "Chris Aron",
    "Cat Lee King", "Foggy Mountain Rockers", "Howlin'Ric", "Cody Lee",
    "Boogie Banausen", "Toto & Raw Deals", "Si Cranstoun"
]

HARDCODED_EVENTS = [
    {
        "title": "Summer Jamboree 2026", 
        "date": "01.08. - 09.08.2026",
        "location": "Senigallia, Italien",
        "city": "Senigallia", 
        "lat": 43.7147, 
        "lon": 13.2183,
        "desc": "Das größte Rockabilly-Festival Europas. 10 Tage Rock'n'Roll, Live-Musik, Tanzen und Vintage-Flair.",
        "url": "https://www.summerjamboree.com"
    }
]

TARGETS = [
    {"name": "Noels Ballroom", "url": "https://noels-ballroom.de/", "city": "Leipzig"},
    {"name": "Tonelli's Leipzig", "url": "http://www.tonellis.de/programm.html", "city": "Leipzig"},
    {"name": "Tanzcafé Waldenburg", "url": "https://www.tanzcafe-waldenburg.de/", "city": "Waldenburg"},
    {"name": "Rockabilly Radio Events", "url": "https://www.rockabillyradio.net/events/", "city": "Diverse"},
    {"name": "Go-Hamburg", "url": "https://www.go-hamburg.de/rockabilly-termine", "city": "Hamburg"},
    {"name": "Rock'n'Roll Calendar", "url": "https://www.rockabilly.nl/calendar.php", "city": "Diverse"},
    {"name": "Kulturfabrik Leipzig", "url": "https://www.kufa.info/programm/", "city": "Leipzig"},
    {"name": "Conne Island", "url": "https://www.conne-island.de/programm", "city": "Leipzig"},
    {"name": "Naumanns", "url": "https://www.naumanns-leipzig.de/programm", "city": "Leipzig"},
    {"name": "Tante Ella", "url": "https://www.tante-ella.de/programm/", "city": "Leipzig"},
    {"name": "Musikclub Zwickau", "url": "https://www.musikclub-zwickau.de/programm/", "city": "Zwickau"},
    {"name": "Alter Schlachthof Dresden", "url": "https://www.alter-schlachthof-dresden.de/programm/", "city": "Dresden"},
    {"name": "Club Passage Erfurt", "url": "https://www.club-passage.de/programm/", "city": "Erfurt"}
]

def get_coords(city_name):
    try:
        city_clean = city_name.replace("Deutschland", "").replace("Italien", "").replace("Schweiz", "").replace("England", "").replace("Österreich", "").strip()
        if not city_clean or len(city_clean) < 3:
            return None, None
            
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={city_clean}&limit=1"
        headers = {'User-Agent': 'RockabillyRadarBot/1.0'}
        resp = requests.get(url, headers=headers, timeout=5)
        data = resp.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except:
        pass
    return None, None

def parse_jukebox_stompers():
    """Spezial-Parser für Jukebox Stompers Veranstaltungskalender."""
    print("🔍 Parse Jukebox Stompers Kalender...")
    events = []
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        url = "https://www.jukeboxstompers.de/index.php/veranstaltungen/veranstaltungskalender"
        resp = requests.get(url, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Suche nach der Tabelle mit Klasse "veranstaltungen" oder ähnlichem
            tables = soup.find_all('table')
            
            for table in tables:
                rows = table.find_all('tr')
                
                for row in rows:
                    cols = row.find_all('td')
                    
                    if len(cols) >= 3:
                        date_text = cols[0].get_text(strip=True)
                        location_text = cols[1].get_text(separator=" ", strip=True)
                        desc_text = cols[2].get_text(separator=" ", strip=True)
                        
                        if not date_text or len(date_text) < 5:
                            continue
                        
                        # Extrahiere Stadt
                        city = extract_city(location_text)
                        
                        # Extrahiere Titel
                        title = extract_title(desc_text)
                        
                        if not title:
                            title = "Jukebox Stompers Live"
                        
                        desc = clean_description(desc_text)
                        lat, lon = get_coords(city)
                        
                        event = {
                            "title": title,
                            "date": date_text,
                            "location": location_text.replace("\n", ", "),
                            "city": city,
                            "lat": lat,
                            "lon": lon,
                            "desc": desc,
                            "url": url
                        }
                        events.append(event)
                        print(f"   ✅ {title} - {date_text} - {city}")
        
        time.sleep(2)
        
    except Exception as e:
        print(f"   ❌ Fehler bei Jukebox Stompers: {e}")
    
    return events

def extract_city(location_text):
    lines = location_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if line and len(line) > 2:
            line = line.replace('**', '').strip()
            if len(line) > 2 and line[0].isupper():
                # Entferne Ländernamen
                for country in ['Deutschland', 'Italien', 'Schweiz', 'England', 'Österreich', 'Niederlande']:
                    line = line.replace(country, '').strip()
                if len(line) > 2:
                    return line
    
    return "Unbekannt"

def extract_title(desc_text):
    lines = desc_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if line and len(line) > 5 and len(line) < 100:
            title = line.replace('**', '').strip()
            return title
    
    return None

def clean_description(text):
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    if len(text) > 300:
        text = text[:300] + "..."
    return text

def is_relevant_event(text):
    if not text or len(text) < 15:
        return False
    
    event_keywords = ['konzert', 'gig', 'show', 'festival', 'live', 'bühne', 'concert', 
                      'event', 'party', 'dance', 'ball', 'abend', 'night', 'live-musik',
                      'livemusik', 'kneipe', 'bar', 'club', 'gaststätte', 'pub', 'lounge']
    
    rock_keywords = ['rockabilly', 'rock\'n\'roll', 'rock and roll', 'rock n roll', 
                     '50er', '60er', 'vintage', 'pinup', 'teddy', 'greaser',
                     'boogie', 'swing', 'lindy hop']
    
    text_lower = text.lower()
    
    band_found = any(band.lower() in text_lower for band in VIP_BANDS)
    if band_found:
        return True
    
    has_date = re.search(r'\d{1,2}\.\d{1,2}\.?\s*(\d{2,4})?', text)
    has_event = any(keyword in text_lower for keyword in event_keywords)
    has_rock = any(keyword in text_lower for keyword in rock_keywords)
    
    if has_date and (has_event or has_rock):
        return True
    
    return False

def run_scraper():
    print("🚀 Rockabilly Radar Scraper startet...")
    
    existing_events = []
    try:
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            existing_events = json.load(f)
    except:
        existing_events = []

    new_events_list = list(HARDCODED_EVENTS)

    def is_duplicate(title, date):
        for ev in existing_events:
            if ev.get('title') == title and ev.get('date') == date:
                return True
        for ev in new_events_list:
            if ev.get('title') == title and ev.get('date') == date:
                return True
        return False

    # 1. Jukebox Stompers
    jukebox_events = parse_jukebox_stompers()
    for event in jukebox_events:
        if not is_duplicate(event['title'], event['date']):
            new_events_list.append(event)
            print(f"   ✅ Hinzugefügt: {event['title']}")

    # 2. Normale Webseiten
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for target in TARGETS:
        print(f"🔍 Prüfe: {target['name']}")
        try:
            resp = requests.get(target['url'], headers=headers, timeout=10)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                
                elements = soup.find_all(['p', 'li', 'div', 'article', 'h3', 'h4'])
                
                found_count = 0
                for el in elements:
                    text = el.get_text(separator=" ", strip=True)
                    
                    if not is_relevant_event(text):
                        continue
                    
                    date_match = re.search(r'(\d{1,2}\.\d{1,2}\.?\s*(\d{2,4})?)', text)
                    date_str = date_match.group(1) if date_match else "Termin folgt"
                    
                    band_found = next((b for b in VIP_BANDS if b.lower() in text.lower()), None)
                    title = f"{band_found} @ {target['name']}" if band_found else f"Live-Musik @ {target['name']}"
                    
                    if not is_duplicate(title, date_str):
                        lat, lon = get_coords(target['city'])
                        
                        new_event = {
                            "title": title,
                            "date": date_str,
                            "location": f"{target['name']}, {target['city']}",
                            "city": target['city'],
                            "lat": lat,
                            "lon": lon,
                            "desc": text[:250] + "..." if len(text) > 250 else text,
                            "url": target['url']
                        }
                        new_events_list.append(new_event)
                        found_count += 1
                        print(f"   ✅ Neu: {title}")
                
                if found_count == 0:
                    print(f"   ️ Keine neuen Events gefunden")
            
            time.sleep(2)

        except Exception as e:
            print(f"   ❌ Fehler bei {target['name']}: {e}")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_events_list, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Fertig! {len(new_events_list)} Events gespeichert.")

if __name__ == "__main__":
    run_scraper()
