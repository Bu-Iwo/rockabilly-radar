import json
import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse

OUTPUT_FILE = 'events.json'
LOG_FILE = 'scraper_log.txt'

# Konfiguration
MIN_DATE = datetime(2026, 7, 1)   # Heute: 01.07.2026
MAX_DATE = datetime(2027, 12, 31) # Max. 1.5 Jahre voraus
REQUEST_TIMEOUT = 10
USER_AGENT = 'RockabillyRadarBot/1.0 (Event-Scraper)'

# Stabile, verifizierte Quellen (Stand 01.07.2026)
VERIFIED_SOURCES = [
    {
        "name": "Jukebox Stompers Kalender",
        "url": "https://www.jukeboxstompers.de/index.php/veranstaltungen/veranstaltungskalender",
        "type": "table"
    },
    {
        "name": "Rockabilly Radio Events",
        "url": "https://www.rockabillyradio.net/events/",
        "type": "general"
    }
]

# VIP Bands (nur echte, bekannte Szene-Bands)
VIP_BANDS = [
    "Ray Collins Hot Club", "The Firebirds", "Jumpin'Up", "Shotgun Jones",
    "Jukebox Stompers", "Boppin'B", "Restless", "Stray Cats", "Mad Sin",
    "Darrel Higham", "Si Cranstoun", "Kim Lenz", "Imelda May",
    "Rocky Sharpe", "The Baseballs", "Shakin' Stevens", "Matchbox"
]

# Strenge Genre-Keywords
GENRE_KEYWORDS = {
    'positive': [
        'rockabilly', 'rock\'n\'roll', 'rock and roll', 'rock n roll',
        '50er', '60er', 'fifties', 'sixties', 'teddy boy', 'greaser',
        'vintage', 'pin-up', 'pinup', 'psychobilly',
        'lindy hop', 'lindyhop', 'swing dance', 'jitterbug',
        'boogie woogie', 'boogie-woogie',
        'country', 'western swing', 'line dance', 'honky tonk',
        'rock\'n\'roll tanz', 'jive'
    ],
    'negative': [
        'techno', 'house', 'trance', 'edm', 'electronic', 'dubstep',
        'metal', 'death metal', 'punk', 'hardcore', 'grunge',
        'hip hop', 'hip-hop', 'rap', 'trap',
        'schlager', 'volksmusik', 'klassik', 'opera',
        'reggae', 'dub', 'ska', 'indie rock'
    ]
}

DATE_PATTERN = re.compile(r'\b(\d{1,2})\.(\d{1,2})\.(\d{4})\b')

def log(message):
    """Schreibt Log-Nachrichten in Datei und Console."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry + '\n')

def check_url_alive(url):
    """Prüft ob URL erreichbar ist (HTTP 200)."""
    try:
        headers = {'User-Agent': USER_AGENT}
        resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        if resp.status_code == 200:
            log(f"✅ URL erreichbar: {url}")
            return True, resp
        else:
            log(f"❌ URL nicht erreichbar (HTTP {resp.status_code}): {url}")
            return False, None
    except requests.exceptions.Timeout:
        log(f"⏱️ Timeout bei: {url}")
        return False, None
    except Exception as e:
        log(f"❌ Fehler bei URL-Check: {url} - {str(e)}")
        return False, None

def verify_genre(text):
    """Strenge Genre-Prüfung. Gibt True zurück nur wenn Event zur Szene gehört."""
    if not text:
        return False
    
    text_lower = text.lower()
    
    # 1. Negative Keywords prüfen (sofort ablehnen)
    for negative in GENRE_KEYWORDS['negative']:
        if negative in text_lower:
            return False
    
    # 2. VIP Band gefunden? (sofort akzeptieren)
    for band in VIP_BANDS:
        if band.lower() in text_lower:
            return True
    
    # 3. Positive Keywords suchen
    for positive in GENRE_KEYWORDS['positive']:
        if positive in text_lower:
            return True
    
    return False

def parse_and_validate_date(date_str):
    """
    Parst Datum und prüft ob es im gültigen Bereich liegt.
    Gibt datetime-Objekt zurück oder None wenn ungültig.
    """
    if not date_str:
        return None
    
    match = DATE_PATTERN.search(date_str)
    if not match:
        return None
    
    try:
        day = int(match.group(1))
        month = int(match.group(2))
        year = int(match.group(3))
        event_date = datetime(year, month, day)
        
        # Prüfe ob Datum im gültigen Bereich
        if event_date < MIN_DATE:
            return None  # Zu alt
        if event_date > MAX_DATE:
            return None  # Zu weit in Zukunft
        
        return event_date
    except ValueError:
        return None

def get_coords(city_name):
    """Holt GPS-Koordinaten für eine Stadt."""
    try:
        city_clean = re.sub(
            r'(Deutschland|Italien|Schweiz|England|Österreich|Niederlande|Spanien|Schweden|USA|Frankreich)',
            '',
            city_name
        ).strip()
        
        if len(city_clean) < 3:
            return None, None
        
        headers = {'User-Agent': USER_AGENT}
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={city_clean}&limit=1"
        resp = requests.get(url, headers=headers, timeout=5)
        data = resp.json()
        
        if data and len(data) > 0:
            return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        log(f"⚠️ GPS-Fehler für {city_name}: {str(e)}")
    
    return None, None

def extract_city_from_text(text):
    """Versucht Stadtname aus Text zu extrahieren."""
    # Häufige deutsche/europäische Städte
    cities = [
        'Berlin', 'Hamburg', 'München', 'Köln', 'Frankfurt', 'Stuttgart', 'Düsseldorf',
        'Leipzig', 'Dresden', 'Hannover', 'Nürnberg', 'Bremen',
        'Senigallia', 'Las Vegas', 'Irun', 'Grimma', 'Hemsby', 'Rye', 'Pineda de Mar',
        'Stockholm', 'Saalbach', 'Barcelona', 'London', 'Paris', 'Amsterdam'
    ]
    
    text_lower = text.lower()
    for city in cities:
        if city.lower() in text_lower:
            return city
    
    return "Unbekannt"

def parse_jukebox_stompers(response):
    """Spezial-Parser für Jukebox Stompers Veranstaltungskalender."""
    events = []
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for table in soup.find_all('table'):
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) >= 3:
                date_text = cols[0].get_text(strip=True)
                location_text = cols[1].get_text(separator=" ", strip=True)
                desc_text = cols[2].get_text(separator=" ", strip=True)
                
                # 1. Datum validieren
                event_date = parse_and_validate_date(date_text)
                if not event_date:
                    log(f"   ⚠️ Ungültiges Datum ignoriert: {date_text}")
                    continue
                
                # 2. Genre prüfen
                full_text = f"{desc_text} Jukebox Stompers"
                if not verify_genre(full_text):
                    log(f"   ❌ Genre-Filter: {date_text}")
                    continue
                
                # 3. Stadt extrahieren
                city = extract_city_from_text(location_text)
                
                # 4. Koordinaten holen
                lat, lon = get_coords(city)
                
                event = {
                    "title": f"Jukebox Stompers Live - {event_date.strftime('%d.%m.%Y')}",
                    "date": event_date.strftime('%d.%m.%Y'),
                    "location": location_text.replace("\n", ", "),
                    "city": city,
                    "lat": lat,
                    "lon": lon,
                    "desc": desc_text[:300] if desc_text else "Jukebox Stompers Live-Konzert",
                    "url": "https://www.jukeboxstompers.de/index.php/veranstaltungen/veranstaltungskalender",
                    "genres": ["Rockabilly", "Rock'n'Roll"],
                    "verified": True,
                    "source": "Jukebox Stompers Kalender"
                }
                events.append(event)
                log(f"   ✅ Verifiziert: {event['title']} am {event['date']}")
    
    return events

def parse_general_events(response, source_url):
    """Allgemeiner Parser für Event-Listen."""
    events = []
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Suche nach typischen Event-Elementen
    for element in soup.find_all(['div', 'article', 'li', 'p']):
        text = element.get_text(separator=" ", strip=True)
        
        if len(text) < 20:
            continue
        
        # 1. Datum finden und validieren
        event_date = parse_and_validate_date(text)
        if not event_date:
            continue
        
        # 2. Genre prüfen
        if not verify_genre(text):
            continue
        
        # 3. Titel extrahieren (erste Zeile oder Überschrift)
        title_element = element.find(['h1', 'h2', 'h3', 'h4', 'strong', 'b'])
        title = title_element.get_text(strip=True) if title_element else f"Event am {event_date.strftime('%d.%m.%Y')}"
        
        # 4. Stadt extrahieren
        city = extract_city_from_text(text)
        
        # 5. Koordinaten holen
        lat, lon = get_coords(city)
        
        # 6. Genres bestimmen
        genres = []
        text_lower = text.lower()
        if 'rockabilly' in text_lower:
            genres.append('Rockabilly')
        if 'rock\'n\'roll' in text_lower or 'rock and roll' in text_lower:
            genres.append("Rock'n'Roll")
        if 'lindy hop' in text_lower:
            genres.append('Lindy Hop')
        if 'swing' in text_lower:
            genres.append('Swing')
        if not genres:
            genres = ['Rockabilly']
        
        event = {
            "title": title,
            "date": event_date.strftime('%d.%m.%Y'),
            "location": text[:100],
            "city": city,
            "lat": lat,
            "lon": lon,
            "desc": text[:300],
            "url": source_url,
            "genres": genres,
            "verified": True,
            "source": urlparse(source_url).netloc
        }
        events.append(event)
        log(f"   ✅ Verifiziert: {event['title']} am {event['date']}")
    
    return events

def run_scraper():
    """Haupt-Scraper mit vollständiger Verifizierung."""
    log("=" * 60)
    log("🚀 ROCKABILLY RADAR SCRAPER STARTET")
    log(f"📅 Heute: {datetime.now().strftime('%d.%m.%Y')}")
    log(f"🔍 Suche Events von {MIN_DATE.strftime('%d.%m.%Y')} bis {MAX_DATE.strftime('%d.%m.%Y')}")
    log("=" * 60)
    
    # Bestehende Events laden
    existing_events = []
    try:
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            existing_events = json.load(f)
            log(f"📊 Bestehende Events geladen: {len(existing_events)}")
    except FileNotFoundError:
        log("📊 Keine bestehende events.json gefunden")
    except Exception as e:
        log(f"⚠️ Fehler beim Laden: {str(e)}")
    
    new_events = []
    verified_count = 0
    rejected_count = 0
    
    # Jede Quelle durchgehen
    for source in VERIFIED_SOURCES:
        log(f"\n🔍 Prüfe Quelle: {source['name']}")
        
        # URL auf Erreichbarkeit prüfen
        alive, response = check_url_alive(source['url'])
        if not alive:
            log(f"⛔ Quelle übersprungen (nicht erreichbar)")
            continue
        
        # Events parsen
        if source['type'] == 'table':
            events = parse_jukebox_stompers(response)
        else:
            events = parse_general_events(response, source['url'])
        
        # Duplikate filtern
        for event in events:
            # Prüfe ob Event schon existiert
            is_duplicate = any(
                e.get('title') == event['title'] and e.get('date') == event['date']
                for e in existing_events + new_events
            )
            
            if is_duplicate:
                log(f"   ⚠️ Duplikat ignoriert: {event['title']}")
                rejected_count += 1
            else:
                new_events.append(event)
                verified_count += 1
        
        time.sleep(2)  # Höfliche Pause zwischen Requests
    
    # Alle Events zusammenführen
    all_events = existing_events + new_events
    
    # Vergangene Events entfernen (nochmal prüfen)
    cleaned_events = []
    removed_old = 0
    
    for event in all_events:
        event_date = parse_and_validate_date(event.get('date', ''))
        if event_date and event_date >= MIN_DATE:
            cleaned_events.append(event)
        else:
            removed_old += 1
            log(f"🗑️ Altes Event entfernt: {event.get('title', 'Unbekannt')}")
    
    # Speichern
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(cleaned_events, f, ensure_ascii=False, indent=2)
        
        log("\n" + "=" * 60)
        log("📊 ERGEBNIS:")
        log(f"   ✅ Neu verifizierte Events: {verified_count}")
        log(f"   ❌ Abgelehnt (Duplikat/Genre): {rejected_count}")
        log(f"   🗑️ Alte Events entfernt: {removed_old}")
        log(f"   💾 Gesamt gespeichert: {len(cleaned_events)}")
        log("=" * 60)
        
    except Exception as e:
        log(f"❌ Kritischer Fehler beim Speichern: {str(e)}")

if __name__ == "__main__":
    run_scraper()
