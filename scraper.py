import json
import requests
from bs4 import BeautifulSoup
import re
import time

OUTPUT_FILE = 'events.json'

# Erweiterte Liste bekannter Bands
VIP_BANDS = [
    "Ray Collins Hot Club", "Ray Allen", "Class of 58", "The Firebirds",
    "Jumpin'Up", "The Nymonics", "The Trainyard Kings", "Shotgun Jones", 
    "Jukebox Stompers", "Boppin'B", "Cherry Casino", "The Baseballs",
    "Restless", "Matchbox", "Darrel Higham", "Mad Sin", "The Rattles",
    "Big Town Playboys", "Shakin' Stevens", "Stray Cats", "Rocky Sharpe"
]

# Feste Top-Events
HARDCODED_EVENTS = [
    {
        "title": "Summer Jamboree 2026", 
        "date": "01.08. - 09.08.2026",
        "location": "Senigallia, Italien",
        "city": "Senigallia", 
        "lat": 43.7147, 
        "lon": 13.2183,
        "desc": "Das größte Rockabilly-Festival Europas.",
        "url": "https://www.summerjamboree.com"
    },
    {
        "title": "Firebirds Festival 2026", 
        "date": "03.07. - 05.07.2026",
        "location": "Kloster Nimbschen, Grimma",
        "city": "Grimma", 
        "lat": 51.2294, 
        "lon": 12.7561,
        "desc": "Rock'n'Roll im Kloster.",
        "url": "https://www.firebirds-festival.de"
    },
    {
        "title": "Hemsby Rock'n'Roll Weekender", 
        "date": "15.05. - 18.05.2026",
        "location": "Hemsby, England",
        "city": "Hemsby", 
        "lat": 52.6750, 
        "lon": 1.6850,
        "desc": "Kult-Festival in England.",
        "url": "https://www.hemsbyrockweekender.co.uk"
    }
]

# Erweiterte Liste von Webseiten
TARGETS = [
    {"name": "Noels Ballroom", "url": "https://noels-ballroom.de/", "city": "Leipzig"},
    {"name": "Tonelli's Leipzig", "url": "http://www.tonellis.de/programm.html", "city": "Leipzig"},
    {"name": "Tanzcafé Waldenburg", "url": "https://www.tanzcafe-waldenburg.de/", "city": "Waldenburg"},
    {"name": "Rockabilly Radio Events", "url": "https://www.rockabillyradio.net/events/", "city": "Diverse"},
    {"name": "Go-Hamburg", "url": "https://www.go-hamburg.de/rockabilly-termine", "city": "Hamburg"},
    {"name": "Rock'n'Roll Calendar", "url": "https://www.rockabilly.nl/calendar.php", "city": "Diverse"}
]

def get_coords(city_name):
    try:
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={city_name}&limit=1"
        headers = {'User-Agent': 'RockabillyRadarBot/1.0'}
        resp = requests.get(url, headers=headers, timeout=5)
        data = resp.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except:
        pass
    return None, None

def is_relevant_event(text):
    """Prüft ob Text ein relevantes Event ist."""
    if not text or len(text) < 15:
        return False
    
    # Typische Event-Begriffe
    event_keywords = ['konzert', 'gig', 'show', 'festival', 'live', 'bühne', 'concert', 
                      'event', 'party', 'dance', 'ball', 'abend', 'night']
    
    # Rockabilly-Begriffe
    rock_keywords = ['rockabilly', 'rock\'n\'roll', 'rock and roll', 'rock n roll', 
                     '50er', '60er', 'vintage', 'pinup', 'teddy', 'greaser']
    
    text_lower = text.lower()
    
    # Prüfe ob Band genannt wird
    band_found = any(band.lower() in text_lower for band in VIP_BANDS)
    if band_found:
        return True
    
    # Prüfe ob Datum + Event-Begriff
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

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for target in TARGETS:
        print(f"🔍 Prüfe: {target['name']}")
        try:
            resp = requests.get(target['url'], headers=headers, timeout=10)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                
                # Suche nach verschiedenen Elementen
                elements = soup.find_all(['p', 'li', 'div', 'article', 'h3', 'h4'])
                
                found_count = 0
                for el in elements:
                    text = el.get_text(separator=" ", strip=True)
                    
                    if not is_relevant_event(text):
                        continue
                    
                    # Datum extrahieren
                    date_match = re.search(r'(\d{1,2}\.\d{1,2}\.?\s*(\d{2,4})?)', text)
                    date_str = date_match.group(1) if date_match else "Termin folgt"
                    
                    # Band finden
                    band_found = next((b for b in VIP_BANDS if b.lower() in text.lower()), None)
                    title = f"{band_found} @ {target['name']}" if band_found else f"Event @ {target['name']}"
                    
                    if not is_duplicate(title, date_str):
                        lat, lon = get_coords(target['city'])
                        
                        new_event = {
                            "title": title,
                            "date": date_str,
                            "location": f"{target['name']}, {target['city']}",
                            "city": target['city'],
                            "lat": lat,
                            "lon": lon,
                            "desc": text[:200] + "..." if len(text) > 200 else text,
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

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_events_list, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Fertig! {len(new_events_list)} Events gespeichert.")

if __name__ == "__main__":
    run_scraper()
