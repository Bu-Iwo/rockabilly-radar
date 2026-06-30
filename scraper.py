import json
import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime, timedelta
import os

OUTPUT_FILE = 'events.json'
BACKUP_FILE = 'events_backup.json'

VIP_BANDS = [
    "Ray Collins Hot Club", "Ray Collins' Hot Club", "Ray Allen", "Class of 58", "The Firebirds",
    "Jumpin'Up", "Jumpin' Up", "The Nymonics", "The Trainyard Kings", "Shotgun Jones", 
    "Jukebox Stompers", "Boppin'B", "Cherry Casino", "The Baseballs",
    "Restless", "Matchbox", "Darrel Higham", "Mad Sin", "The Rattles",
    "Big Town Playboys", "Shakin' Stevens", "Stray Cats", "Rocky Sharpe",
    "The Jets", "The Cats", "Dave Phillips", "Kim Lenz", "The Hot Rods"
]

# NUR HARDCODED EVENTS - diese sind garantiert korrekt
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
        "desc": "Rock'n'Roll im Kloster. Live-Bands, Rockabilly-Markt und Party.",
        "url": "https://www.firebirds-festival.de"
    },
    {
        "title": "Hemsby Rock'n'Roll Weekender 2026", 
        "date": "15.05. - 18.05.2026",
        "location": "Hemsby, England",
        "city": "Hemsby", 
        "lat": 52.6750, 
        "lon": 1.6850,
        "desc": "Kult-Festival in England mit internationalen Bands.",
        "url": "https://www.hemsbyrockweekender.co.uk"
    }
]

# NUR VERIFIZIERTE URLs - alle anderen wurden entfernt
VERIFIED_TARGETS = [
    # Diese URLs wurden geprüft und funktionieren
    {"name": "Jukebox Stompers", "url": "https://www.jukeboxstompers.de/index.php/veranstaltungen/veranstaltungskalender", "city": "Diverse", "type": "special"},
    {"name": "Noels Ballroom", "url": "https://noels-ballroom.de/termine/", "city": "Leipzig", "type": "normal"},
]

MONTHS_DE = {
    'januar': 1, 'jan': 1, 'februar': 2, 'feb': 2,
    'märz': 3, 'maerz': 3, 'mar': 3, 'april': 4, 'apr': 4,
    'mai': 5, 'juni': 6, 'jun': 6, 'juli': 7, 'jul': 7,
    'august': 8, 'aug': 8, 'september': 9, 'sep': 9, 'sept': 9,
    'oktober': 10, 'okt': 10, 'november': 11, 'nov': 11,
    'dezember': 12, 'dez': 12
}

def parse_german_date(date_str):
    """Parst deutsche Datumsformate"""
    if not date_str:
        return None
    
    try:
        date_str = date_str.strip().lower()
        
        weekdays = ['montag', 'dienstag', 'mittwoch', 'donnerstag', 'freitag', 'samstag', 'sonntag', 
                    'mo.', 'di.', 'mi.', 'do.', 'fr.', 'sa.', 'so.']
        for day in weekdays:
            if date_str.startswith(day):
                date_str = date_str[len(day):].strip()
                if date_str.startswith(','):
                    date_str = date_str[1:].strip()
                break
        
        # 12.05.2024
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
            
            if 1 <= day <= 31 and 1 <= month <= 12:
                return datetime(year, month, day)
        
        # 12. Mai 2024
        match = re.search(r'(\d{1,2})[\.\s]+([a-zA-ZäöüÄÖÜß]+)\s*(\d{4})?', date_str)
        if match:
            day = int(match.group(1))
            month_str = match.group(2).lower()
            year = int(match.group(3)) if match.group(3) else datetime.now().year
            
            month = MONTHS_DE.get(month_str)
            if month and 1 <= day <= 31:
                try:
                    return datetime(year, month, day)
                except:
                    pass
        
        return None
    except:
        return None

def is_past_event(date_str, days_buffer=1):
    event_date = parse_german_date(date_str)
    if not event_date:
        return False
    cutoff_date = datetime.now() - timedelta(days=days_buffer)
    return event_date < cutoff_date

def get_coords(city_name):
    try:
        city_clean = str(city_name).strip()
        if not city_clean or len(city_clean) < 2:
            return None, None
        
        for country in ['Deutschland', 'Germany', 'Italien', 'Italy', 'Schweiz', 'Switzerland', 'England', 'UK']:
            city_clean = city_clean.replace(country, '').strip()
        
        if not city_clean:
            return None, None
        
        queries = [city_clean]
        if len(city_clean) < 15:
            queries.append(f"{city_clean}, Germany")
        
        headers = {'User-Agent': 'RockabillyRadarBot/1.0'}
        
        for query in queries:
            try:
                url = f"https://nominatim.openstreetmap.org/search?format=json&q={query}&limit=1"
                resp = requests.get(url, headers=headers, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    if data and len(data) > 0:
                        return float(data[0]['lat']), float(data[0]['lon'])
            except:
                continue
        
        return None, None
    except:
        return None, None

def parse_jukebox_stompers():
    """Parser für Jukebox Stompers"""
    print("🔍 Parse Jukebox Stompers Kalender...")
    events = []
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        url = "https://www.jukeboxstompers.de/index.php/veranstaltungen/veranstaltungskalender"
        resp = requests.get(url, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            tables = soup.find_all('table')
            
            for table in tables:
                rows = table.find_all('tr')
                
                for row in rows:
                    try:
                        cols = row.find_all('td')
                        
                        if len(cols) >= 3:
                            date_text = cols[0].get_text(strip=True)
                            location_text = cols[1].get_text(separator=" ", strip=True)
                            desc_text = cols[2].get_text(separator=" ", strip=True)
                            
                            if not date_text or len(date_text) < 5:
                                continue
                            
                            city = location_text.split('\n')[0].strip() if '\n' in location_text else location_text[:50]
                            
                            title = "Jukebox Stompers Live"
                            if desc_text:
                                first_line = desc_text.strip().split('\n')[0].strip()
                                if len(first_line) > 5 and len(first_line) < 100:
                                    title = first_line
                            
                            lat, lon = get_coords(city)
                            
                            event = {
                                "title": title,
                                "date": date_text,
                                "location": location_text.replace("\n", ", ")[:100],
                                "city": city[:50],
                                "lat": lat,
                                "lon": lon,
                                "desc": desc_text[:250],
                                "url": url
                            }
                            events.append(event)
                            print(f"   ✅ {title} - {date_text}")
                    except:
                        continue
        
        time.sleep(2)
        
    except Exception as e:
        print(f"   ❌ Fehler bei Jukebox Stompers: {e}")
    
    return events

def parse_normal_site(target):
    """Parser für normale Webseiten"""
    print(f"🔍 Prüfe: {target['name']}")
    events = []
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        resp = requests.get(target['url'], headers=headers, timeout=10)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            elements = soup.find_all(['p', 'li', 'div', 'h3', 'h4', 'article'])
            
            for el in elements:
                try:
                    text = el.get_text(separator=" ", strip=True)
                    
                    if len(text) < 20:
                        continue
                    
                    # Suche nach Datum
                    date_match = re.search(r'(\d{1,2}\.\d{1,2}\.?\s*\d{2,4}?)', text)
                    date_str = date_match.group(1) if date_match else "Termin folgt"
                    
                    # Prüfe auf Band
                    band_found = next((b for b in VIP_BANDS if b.lower() in text.lower()), None)
                    title = f"{band_found} @ {target['name']}" if band_found else f"Live @ {target['name']}"
                    
                    lat, lon = get_coords(target['city'])
                    
                    event = {
                        "title": title,
                        "date": date_str,
                        "location": f"{target['name']}, {target['city']}",
                        "city": target['city'],
                        "lat": lat,
                        "lon": lon,
                        "desc": text[:250],
                        "url": target['url']
                    }
                    events.append(event)
                except:
                    continue
            
            print(f"   ✅ {len(events)} Events gefunden")
        else:
            print(f"   ❌ HTTP {resp.status_code}")
        
        time.sleep(2)
        
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
    
    return events

def run_scraper():
    print("🚀 Rockabilly Radar Scraper startet...")
    print(f"📅 Heute: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    
    # Lade bestehende Events
    existing_events = []
    try:
        if os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                existing_events = json.load(f)
            print(f"📚 {len(existing_events)} bestehende Events geladen")
            
            # Backup
            with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
                json.dump(existing_events, f, ensure_ascii=False, indent=2)
    except:
        existing_events = []

    new_events_list = list(HARDCODED_EVENTS)
    print(f" {len(HARDCODED_EVENTS)} Hardcoded Events")

    def is_duplicate(title, date):
        for ev in new_events_list:
            if ev.get('title') == title and ev.get('date') == date:
                return True
        return False

    # 1. Jukebox Stompers (Special Parser)
    jukebox_events = parse_jukebox_stompers()
    for event in jukebox_events:
        if not is_duplicate(event['title'], event['date']):
            new_events_list.append(event)

    # 2. Andere verifizierte URLs
    for target in VERIFIED_TARGETS:
        if target['type'] == 'special':
            continue  # Jukebox schon geparst
        
        site_events = parse_normal_site(target)
        for event in site_events:
            if not is_duplicate(event['title'], event['date']):
                new_events_list.append(event)

    # 3. Alte Events entfernen
    print("\n🧹 Entferne vergangene Events...")
    cleaned_events = []
    
    for event in new_events_list:
        date_str = event.get('date', '')
        
        if not date_str or date_str == "Termin folgt":
            cleaned_events.append(event)
            continue
        
        if not is_past_event(date_str, days_buffer=1):
            cleaned_events.append(event)
    
    print(f"   ✅ {len(new_events_list) - len(cleaned_events)} alte Events entfernt")

    # 4. Speichern
    if len(cleaned_events) == 0:
        print("❌ Keine Events! Backup wird wiederhergestellt...")
        if os.path.exists(BACKUP_FILE):
            with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
                cleaned_events = json.load(f)
        else:
            cleaned_events = HARDCODED_EVENTS

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(cleaned_events, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Fertig! {len(cleaned_events)} Events gespeichert.")

if __name__ == "__main__":
    run_scraper()
