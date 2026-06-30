import json
import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime, timedelta

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
    "Boogie Banausen", "Toto & Raw Deals", "Si Cranstoun", "Elbonautics",
    "Suffy Sand Rocats", "Suffy Sand Combo", "Yellow Boogie Dancers"
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
    },
    {
        "title": "Firebirds Festival 2026", 
        "date": "03.07. - 05.07.2026",
        "location": "Kloster Nimbschen, Grimma",
        "city": "Grimma", 
        "lat": 51.2294, 
        "lon": 12.7561,
        "desc": "Rock'n'Roll im historischen Kloster. Live-Bands, Rockabilly-Markt und Party.",
        "url": "https://www.firebirds-festival.de"
    },
    {
        "title": "Rhythm Riot 2026", 
        "date": "15.11. - 19.11.2026",
        "location": "Camber Sands, Rye, England",
        "city": "Rye", 
        "lat": 50.9324, 
        "lon": 0.7941,
        "desc": "UKs legendärer Rock'n'Roll Weekender. Weltspitze des Rhythm & Blues.",
        "url": "https://www.rhythmriot.com"
    }
]

TARGETS = [
    {"name": "Noels Ballroom", "url": "https://noels-ballroom.de/", "city": "Leipzig"},
    {"name": "Tonelli's Leipzig", "url": "http://www.tonellis.de/programm.html", "city": "Leipzig"},
    {"name": "Tanzcafé Waldenburg", "url": "https://www.tanzcafe-waldenburg.de/", "city": "Waldenburg"},
    {"name": "Kulturfabrik Leipzig", "url": "https://www.kufa.info/programm/", "city": "Leipzig"},
    {"name": "Conne Island", "url": "https://www.conne-island.de/programm", "city": "Leipzig"},
    {"name": "Naumanns", "url": "https://www.naumanns-leipzig.de/programm", "city": "Leipzig"},
    {"name": "Tante Ella", "url": "https://www.tante-ella.de/programm/", "city": "Leipzig"},
    {"name": "Musikclub Zwickau", "url": "https://www.musikclub-zwickau.de/programm/", "city": "Zwickau"},
    {"name": "Alter Schlachthof Dresden", "url": "https://www.alter-schlachthof-dresden.de/programm/", "city": "Dresden"},
    {"name": "Club Passage Erfurt", "url": "https://www.club-passage.de/programm/", "city": "Erfurt"}
]

# KORRIGIERTES DATUMS-PATTERN (Backslashes sind jetzt korrekt!)
DATE_PATTERN = re.compile(r'\b\d{1,2}\.\d{1,2}\.?\s*(?:\d{2,4})?\b')

MONTHS_DE = {
    'januar': 1, 'jan': 1,
    'februar': 2, 'feb': 2,
    'märz': 3, 'maerz': 3, 'mar': 3,
    'april': 4, 'apr': 4,
    'mai': 5,
    'juni': 6, 'jun': 6,
    'juli': 7, 'jul': 7,
    'august': 8, 'aug': 8,
    'september': 9, 'sep': 9, 'sept': 9,
    'oktober': 10, 'okt': 10,
    'november': 11, 'nov': 11,
    'dezember': 12, 'dez': 12
}

def parse_german_date(date_str):
    """Parst verschiedene deutsche Datumsformate."""
    if not date_str:
        return None
    
    date_str = date_str.strip().lower()
    
    # Entferne Wochentage am Anfang
    weekdays = ['montag', 'dienstag', 'mittwoch', 'donnerstag', 'freitag', 'samstag', 'sonntag', 
                'mo.', 'di.', 'mi.', 'do.', 'fr.', 'sa.', 'so.']
    for day in weekdays:
        if date_str.startswith(day):
            date_str = date_str[len(day):].strip()
            if date_str.startswith(','):
                date_str = date_str[1:].strip()
            break
    
    # Muster 1: 12.05.2024
    match = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{2,4})?', date_str)
    if match:
        day = int(match.group(1))
        month = int(match.group(2))
        year = match.group(3)
        
        if year:
            year = int(year)
            if year < 100:
                year = 2000 + year if year < 50 else 1900 + year
        else:
            year = datetime.now().year
        
        try:
            return datetime(year, month, day)
        except ValueError:
            return None
    
    # Muster 2: 12. Mai 2024
    match = re.search(r'(\d{1,2})[\.\s]+([a-zA-ZäöüÄÖÜß]+)\s*(\d{4})?', date_str)
    if match:
        day = int(match.group(1))
        month_str = match.group(2).lower()
        year = int(match.group(3)) if match.group(3) else datetime.now().year
        
        month = MONTHS_DE.get(month_str)
        if month:
            try:
                return datetime(year, month, day)
            except ValueError:
                return None
    
    return None

def is_past_event(date_str, days_buffer=1):
    """Prüft ob ein Event in der Vergangenheit liegt."""
    event_date = parse_german_date(date_str)
    if not event_date:
        return False
    
    cutoff_date = datetime.now() - timedelta(days=days_buffer)
    return event_date < cutoff_date

def get_coords(city_name):
    """Holt GPS-Koordinaten für eine Stadt."""
    try:
        city_clean = city_name.replace("Deutschland", "").replace("Italien", "").replace("Schweiz", "").replace("England", "").replace("Österreich", "").replace("Niederlande", "").strip()
        
        if not city_clean or len(city_clean) < 3:
            return None, None
        
        countries_to_try = [city_clean, f"{city_clean}, Germany", f"{city_clean}, Deutschland"]
        headers = {'User-Agent': 'RockabillyRadarBot/1.0'}
        
        for query in countries_to_try:
            try:
                url = f"https://nominatim.openstreetmap.org/search?format=json&q={query}&limit=1"
                resp = requests.get(url, headers=headers, timeout=5)
                data = resp.json()
                if data and len(data) > 0:
                    return float(data[0]['lat']), float(data[0]['lon'])
            except:
                continue
    except Exception as e:
        print(f"   ⚠️ GPS-Fehler für {city_name}: {e}")
    
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
                        
                        city = extract_city(location_text)
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
    """Prüft ob Text ein relevantes Event ist."""
    if not text or len(text) < 15:
        return False
    
    event_keywords = ['konzert', 'gig', 'show', 'festival', 'live', 'bühne', 'concert', 
                      'event', 'party', 'dance', 'ball', 'abend', 'night', 'live-musik',
                      'livemusik', 'kneipe', 'bar', 'club', 'gaststätte', 'pub', 'lounge']
    
    rock_keywords = ['rockabilly', 'rock\'n\'roll', 'rock and roll', 'rock n roll', 
                     '50er', '60er', 'vintage', 'pinup', 'teddy', 'greaser',
                     'boogie', 'swing', 'lindy hop']
    
    text_lower = text.lower()
    
    # VIP Band gefunden?
    band_found = any(band.lower() in text_lower for band in VIP_BANDS)
    if band_found:
        return True
    
    # Datum + Event/rock Keyword?
    has_date = DATE_PATTERN.search(text)
    has_event = any(keyword in text_lower for keyword in event_keywords)
    has_rock = any(keyword in text_lower for keyword in rock_keywords)
    
    if has_date and (has_event or has_rock):
        return True
    
    return False

def run_scraper():
    print("🚀 Rockabilly Radar Scraper startet...")
    print(f"📅 Heute ist: {datetime.now().strftime('%d.%m.%Y')}")
    
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

    # 2. Normale Webseiten durchsuchen
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
                    
                    date_match = DATE_PATTERN.search(text)
                    date_str = date_match.group(0) if date_match else "Termin folgt"
                    
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
                    print(f"   ⚠️ Keine neuen Events gefunden")
            
            time.sleep(2)

        except Exception as e:
            print(f"   ❌ Fehler bei {target['name']}: {e}")

    # 3. Vergangene Events löschen
    print("\n🧹 Entferne vergangene Events...")
    events_before = len(new_events_list)
    
    cleaned_events = []
    removed_count = 0
    
    for event in new_events_list:
        date_str = event.get('date', '')
        
        if not date_str or date_str == "Termin folgt":
            cleaned_events.append(event)
            continue
        
        if not is_past_event(date_str, days_buffer=1):
            cleaned_events.append(event)
        else:
            removed_count += 1
            print(f"   🗑️ Entfernt: {event['title']} ({date_str})")
    
    events_after = len(cleaned_events)
    print(f"   ✅ {removed_count} alte Events entfernt ({events_before} → {events_after})")

    # 4. Speichern
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(cleaned_events, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Fertig! {len(cleaned_events)} Events gespeichert.")
    print(f"📊 Statistik: {events_after} zukünftige Events, {removed_count} vergangene gelöscht")

if __name__ == "__main__":
    run_scraper()
