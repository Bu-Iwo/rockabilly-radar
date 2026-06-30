import json
import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime, timedelta

OUTPUT_FILE = 'events.json'

# Erweiterte Liste bekannter Bands (nur echte Rockabilly/R'n'R/Lindy Hop/Jazz Bands)
VIP_BANDS = [
    # Rockabilly
    "Ray Collins Hot Club", "Ray Collins' Hot Club", "Ray Allen", "Class of 58", "The Firebirds",
    "Jumpin'Up", "Jumpin' Up", "The Nymonics", "The Trainyard Kings", "Shotgun Jones", 
    "Jukebox Stompers", "Boppin'B", "Cherry Casino", "The Baseballs",
    "Restless", "Matchbox", "Darrel Higham", "Mad Sin", "The Rattles",
    "Big Town Playboys", "Shakin' Stevens", "Stray Cats", "Rocky Sharpe",
    "The Jets", "The Cats", "Dave Phillips", "Kim Lenz", "The Hot Rods",
    "George And His New Heartaches", "Marty's Henpecked Club", "Chris Aron",
    "Cat Lee King", "Foggy Mountain Rockers", "Howlin'Ric", "Cody Lee",
    "Boogie Banausen", "Toto & Raw Deals", "Si Cranstoun", "Elbonautics",
    "Suffy Sand Rocats", "Suffy Sand Combo", "Yellow Boogie Dancers",
    "Imelda May", "The Polecats", "The Sharks",
    "Guana Batz", "Frantic Flintstones", "Batmobile",
    "Nekromantix", "Horrorpops", "Tiger Army", "Reverend Horton Heat",
    "Long Tall Texans", "The Barnshakers",
    
    # Rock'n'Roll / 50er / 60er
    "Bill Haley", "Chuck Berry", "Elvis Presley", "Buddy Holly", "Jerry Lee Lewis",
    "Little Richard", "Carl Perkins", "Gene Vincent", "Eddie Cochran",
    "The Beatles", "The Rolling Stones", "The Who", "The Kinks",
    
    # Lindy Hop / Swing
    "Lindy Hop", "Swing Dance", "Jitterbug", "Boogie Woogie",
    "Count Basie", "Duke Ellington", "Benny Goodman", "Glenn Miller",
    
    # Jazz (im Vintage-Kontext)
    "Django Reinhardt", "Stéphane Grappelli", "Hot Club", "Gypsy Jazz"
]

# GROSSE FESTIVALS - Nur verifizierte Szene-Festivals
HARDCODED_EVENTS = [
    # Italien
    {
        "title": "Summer Jamboree 2026", 
        "date": "01.08. - 09.08.2026",
        "location": "Senigallia, Italien",
        "city": "Senigallia", 
        "lat": 43.7147, 
        "lon": 13.2183,
        "desc": "Das größte Rockabilly & Rock'n'Roll Festival Europas. 10 Tage Live-Musik, Lindy Hop, Vintage-Flair und 50er Jahre Atmosphäre am Strand.",
        "url": "https://www.summerjamboree.com",
        "genres": ["Rockabilly", "Rock'n'Roll", "Lindy Hop", "50er"]
    },
    
    # Deutschland
    {
        "title": "Firebirds Festival 2026", 
        "date": "03.07. - 05.07.2026",
        "location": "Kloster Nimbschen, Grimma",
        "city": "Grimma", 
        "lat": 51.2294, 
        "lon": 12.7561,
        "desc": "Rock'n'Roll im historischen Kloster. The Firebirds & Friends, Rockabilly-Markt, Custom Cars und Lindy Hop Tanzfläche.",
        "url": "https://www.firebirds-festival.de",
        "genres": ["Rock'n'Roll", "Rockabilly", "60er"]
    },
    {
        "title": "High Rockabilly 2026",
        "date": "15.05. - 17.05.2026",
        "location": "Irun, Spanien",
        "city": "Irun",
        "lat": 43.3396,
        "lon": -1.7894,
        "desc": "Eines der besten Rockabilly-Festivals Europas mit internationalen Top-Bands der Szene.",
        "url": "https://www.highrockabilly.com",
        "genres": ["Rockabilly", "Rock'n'Roll"]
    },
    {
        "title": "Let's Get Wild Festival 2026",
        "date": "12.06. - 14.06.2026",
        "location": "Berlin",
        "city": "Berlin",
        "lat": 52.5200,
        "lon": 13.4050,
        "desc": "Deutschlands größtes Rock'n'Roll & Rockabilly Festival mit Live-Musik, Vintage-Markt, Pin-Up Contest und Lindy Hop Workshops.",
        "url": "https://www.letsgetwild.de",
        "genres": ["Rock'n'Roll", "Rockabilly", "Lindy Hop", "50er"]
    },
    {
        "title": "Rockabilly Rave 2026",
        "date": "18.09. - 20.09.2026",
        "location": "Berlin",
        "city": "Berlin",
        "lat": 52.5200,
        "lon": 13.4050,
        "desc": "Die legendäre Rockabilly-Party mit internationalen DJs und Live-Bands der Szene.",
        "url": "https://www.rockabillyrave.de",
        "genres": ["Rockabilly", "Psychobilly"]
    },
    {
        "title": "Psychobilly Meeting 2026",
        "date": "23.10. - 25.10.2026",
        "location": "Pineda de Mar, Spanien",
        "city": "Pineda de Mar",
        "lat": 41.6200,
        "lon": 2.6847,
        "desc": "Das größte Psychobilly-Festival der Welt am Mittelmeer.",
        "url": "https://www.psychobillymeeting.com",
        "genres": ["Psychobilly", "Rockabilly"]
    },
    
    # England
    {
        "title": "Hemsby Rock'n'Roll Weekender 2026", 
        "date": "15.05. - 18.05.2026",
        "location": "Hemsby, England",
        "city": "Hemsby", 
        "lat": 52.6750, 
        "lon": 1.6850,
        "desc": "Kult-Festival in England mit internationalen Rock'n'Roll Bands, DJs, Lindy Hop und Vintage-Markt.",
        "url": "https://www.hemsbyrockweekender.co.uk",
        "genres": ["Rock'n'Roll", "Lindy Hop", "50er", "60er"]
    },
    {
        "title": "Rhythm Riot 2026", 
        "date": "13.11. - 15.11.2026",
        "location": "Camber Sands, Rye, England",
        "city": "Rye", 
        "lat": 50.9324, 
        "lon": 0.7941,
        "desc": "UKs legendärer Rock'n'Roll Weekender. Weltspitze des Rhythm & Blues, Rockabilly und Lindy Hop.",
        "url": "https://www.rhythmriot.com",
        "genres": ["Rock'n'Roll", "Rhythm & Blues", "Lindy Hop"]
    },
    
    # USA
    {
        "title": "Viva Las Vegas 2026",
        "date": "16.04. - 19.04.2026",
        "location": "Las Vegas, USA",
        "city": "Las Vegas",
        "lat": 36.1699,
        "lon": -115.1398,
        "desc": "Das legendärste Rockabilly-Festival der Welt im Orleans Hotel, Las Vegas.",
        "url": "https://www.vivalasvegas.net",
        "genres": ["Rockabilly", "Rock'n'Roll", "50er"]
    },
    
    # Skandinavien
    {
        "title": "Let's Get Wild Stockholm 2026",
        "date": "28.08. - 30.08.2026",
        "location": "Stockholm, Schweden",
        "city": "Stockholm",
        "lat": 59.3293,
        "lon": 18.0686,
        "desc": "Schwedens größtes Rock'n'Roll Festival mit internationalen Rockabilly Acts und Lindy Hop.",
        "url": "https://www.letsgetwild.se",
        "genres": ["Rock'n'Roll", "Rockabilly", "Lindy Hop"]
    },
    
    # Österreich
    {
        "title": "Rock'n'Roll Weekend Saalbach 2026",
        "date": "21.08. - 23.08.2026",
        "location": "Saalbach-Hinterglemm, Österreich",
        "city": "Saalbach",
        "lat": 47.3883,
        "lon": 12.6372,
        "desc": "Rock'n'Roll in den Alpen mit Live-Musik, Custom Car Show, 50er Jahre Flair und Lindy Hop.",
        "url": "https://www.rockweekend.at",
        "genres": ["Rock'n'Roll", "50er", "Lindy Hop"]
    },
    
    # Niederlande
    {
        "title": "Psychobilly Meeting Netherlands 2026",
        "date": "05.06. - 07.06.2026",
        "location": "Eindhoven, Niederlande",
        "city": "Eindhoven",
        "lat": 51.4416,
        "lon": 5.4697,
        "desc": "Das niederländische Psychobilly-Treffen mit den härtesten Bands der Szene.",
        "url": "https://www.psychobillymeeting.nl",
        "genres": ["Psychobilly", "Rockabilly"]
    },
    
    # Weitere deutsche Festivals
    {
        "title": "Hot Rockin' Summer 2026",
        "date": "10.07. - 12.07.2026",
        "location": "Hamburg",
        "city": "Hamburg",
        "lat": 53.5511,
        "lon": 9.9937,
        "desc": "Hamburgs heißestes Rockabilly-Festival mit Open-Air-Bühne, Lindy Hop und Strand-Feeling.",
        "url": "https://www.hotrockin.de",
        "genres": ["Rockabilly", "Rock'n'Roll", "Lindy Hop"]
    },
    {
        "title": "Rock'n'Roll Meeting Kiel 2026",
        "date": "24.07. - 26.07.2026",
        "location": "Kiel",
        "city": "Kiel",
        "lat": 54.3233,
        "lon": 10.1228,
        "desc": "Norddeutschlands größtes Rock'n'Roll Treffen an der Ostsee mit 50er Jahre Atmosphäre.",
        "url": "https://www.rockmeeting.de",
        "genres": ["Rock'n'Roll", "50er"]
    },
    {
        "title": "Teddy Boy Weekender 2026",
        "date": "04.09. - 06.09.2026",
        "location": "Köln",
        "city": "Köln",
        "lat": 50.9375,
        "lon": 6.9603,
        "desc": "Das authentische Teddy Boy Festival mit original 50er Jahre Rock'n'Roll Atmosphäre.",
        "url": "https://www.teddyboyweekender.de",
        "genres": ["Rock'n'Roll", "50er", "Teddy Boy"]
    },
    
    # Lindy Hop / Swing Festivals
    {
        "title": "Lindy Hop Festival Berlin 2026",
        "date": "08.05. - 10.05.2026",
        "location": "Berlin",
        "city": "Berlin",
        "lat": 52.5200,
        "lon": 13.4050,
        "desc": "Internationales Lindy Hop & Swing Festival mit Workshops, Live-Bands und Social Dancing.",
        "url": "https://www.lindyhopfestival.de",
        "genres": ["Lindy Hop", "Swing", "Jazz"]
    },
    {
        "title": "Swing Camp Catalina 2026",
        "date": "19.06. - 22.06.2026",
        "location": "Catalina Island, USA",
        "city": "Catalina",
        "lat": 33.3961,
        "lon": -118.4167,
        "desc": "Das legendäre Swing & Lindy Hop Camp mit den besten Tänzern und Bands der Welt.",
        "url": "https://www.swingcamp.com",
        "genres": ["Lindy Hop", "Swing", "Jazz"]
    }
]

# Erweiterte Liste von Webseiten
TARGETS = [
    # Große Venues
    {"name": "Noels Ballroom", "url": "https://noels-ballroom.de/", "city": "Leipzig"},
    {"name": "Tonelli's Leipzig", "url": "http://www.tonellis.de/programm.html", "city": "Leipzig"},
    {"name": "Tanzcafé Waldenburg", "url": "https://www.tanzcafe-waldenburg.de/", "city": "Waldenburg"},
    
    # Festival-Portale & Event-Kalender (nur Szene-relevante)
    {"name": "Rockabilly Radio Events", "url": "https://www.rockabillyradio.net/events/", "city": "Diverse"},
    {"name": "Rock'n'Roll Calendar", "url": "https://www.rockabilly.nl/calendar.php", "city": "Diverse"},
    
    # Clubs & Kulturhäuser
    {"name": "Kulturfabrik Leipzig", "url": "https://www.kufa.info/programm/", "city": "Leipzig"},
    {"name": "Conne Island", "url": "https://www.conne-island.de/programm", "city": "Leipzig"},
    {"name": "Naumanns", "url": "https://www.naumanns-leipzig.de/programm", "city": "Leipzig"},
    {"name": "Tante Ella", "url": "https://www.tante-ella.de/programm/", "city": "Leipzig"},
    {"name": "Musikclub Zwickau", "url": "https://www.musikclub-zwickau.de/programm/", "city": "Zwickau"},
    {"name": "Alter Schlachthof Dresden", "url": "https://www.alter-schlachthof-dresden.de/programm/", "city": "Dresden"},
    {"name": "Club Passage Erfurt", "url": "https://www.club-passage.de/programm/", "city": "Erfurt"},
    
    # Bars & kleine Locations
    {"name": "Rock'n'Roll Bar Berlin", "url": "https://www.rockbar-berlin.de/events/", "city": "Berlin"},
    {"name": "Café Burger Berlin", "url": "https://www.cafe-burger.de/programm/", "city": "Berlin"},
    {"name": "Badehaus Berlin", "url": "https://www.badehaus-berlin.com/programm/", "city": "Berlin"},
    
    # Lindy Hop / Swing spezifische Quellen
    {"name": "Lindy Hop Events Deutschland", "url": "https://www.lindyhop.de/events", "city": "Diverse"},
    {"name": "Swing Dance Calendar", "url": "https://www.swingdancecalendar.com", "city": "Diverse"}
]

# DATUMS-PATTERN
DATE_PATTERN = re.compile(r'\b\d{1,2}\.\d{1,2}\.?\s*(?:\d{4})?\b')

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
    
    weekdays = ['montag', 'dienstag', 'mittwoch', 'donnerstag', 'freitag', 'samstag', 'sonntag', 
                'mo.', 'di.', 'mi.', 'do.', 'fr.', 'sa.', 'so.']
    for day in weekdays:
        if date_str.startswith(day):
            date_str = date_str[len(day):].strip()
            if date_str.startswith(','):
                date_str = date_str[1:].strip()
            break
    
    match = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', date_str)
    if match:
        day = int(match.group(1))
        month = int(match.group(2))
        year = int(match.group(3))
        try:
            return datetime(year, month, day)
        except ValueError:
            return None
    
    match = re.search(r'(\d{1,2})\.(\d{1,2})\.?$', date_str)
    if match:
        day = int(match.group(1))
        month = int(match.group(2))
        year = datetime.now().year
        if datetime(year, month, day) < datetime.now():
            year += 1
        try:
            return datetime(year, month, day)
        except ValueError:
            return None
    
    match = re.search(r'(\d{1,2})[\.\s]+([a-zA-ZäöüÄÖÜß]+)\s*(\d{4})?', date_str)
    if match:
        day = int(match.group(1))
        month_str = match.group(2).lower()
        year = int(match.group(3)) if match.group(3) else datetime.now().year
        month = MONTHS_DE.get(month_str)
        if month:
            if not match.group(3) and datetime(year, month, day) < datetime.now():
                year += 1
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
        city_clean = city_name.replace("Deutschland", "").replace("Italien", "").replace("Schweiz", "").replace("England", "").replace("Österreich", "").replace("Niederlande", "").replace("Spanien", "").replace("Schweden", "").replace("USA", "").strip()
        
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

def verify_event_genre(text, title):
    """
    STRENGE VERIFIZIERUNG: Prüft ob ein Event wirklich zur Szene gehört.
    Gibt True zurück wenn das Event Rockabilly/Rock'n'Roll/50er/60er/Lindy Hop/Jazz ist.
    """
    text_lower = (text + " " + title).lower()
    
    # STARKE POSITIVE INDIKATOREN (mindestens einer muss vorkommen)
    strong_indicators = [
        'rockabilly', 'rock \'n\' roll', 'rock\'n\'roll', 'rock and roll', 'rock n roll', 'r\'n\'r',
        '50er jahre', '50er party', '50s', 'fifties', 'fünfziger',
        '60er jahre', '60er party', '60s', 'sixties', 'sechziger',
        'teddy boy', 'teddyboy', 'teddy girl',
        'lindy hop', 'lindyhop', 'swing dance', 'swing tanzen', 'jitterbug',
        'boogie woogie', 'boogie-woogie',
        'rock \'n\' roll tanz', 'rock\'n\'roll tanz', 'rock n roll tanz',
        'vintage', 'retro', 'pin-up', 'pinup', 'rockabella',
        'psychobilly', 'neo-rockabilly',
        'swing jazz', 'gypsy jazz', 'hot club', 'djang',
        'jukebox', 'oldtimer', 'custom car', 'hot rod', 'hotrod',
        'greaser', 'rockers', 'rock\'n\'roll party', 'rock n roll party'
    ]
    
    # MITTELMÄSSIGE INDIKATOREN (müssen mit VIP-Band oder starkem Indikator kombiniert sein)
    medium_indicators = [
        'rock', 'roll', 'live musik', 'livemusik', 'konzert', 'gig', 'show',
        'festival', 'party', 'tanzen', 'dance', 'ball', 'abend',
        'band', 'musiker', 'sänger', 'dj',
        'oldies', 'classics', 'evergreens'
    ]
    
    # NEGATIVE INDIKATOREN (wenn diese vorkommen, ist es KEIN Szene-Event)
    negative_indicators = [
        'techno', 'house', 'trance', 'edm', 'electronic', 'elektronisch',
        'metal', 'heavy metal', 'death metal', 'black metal',
        'punk', 'hardcore', 'grunge', 'alternative',
        'hip hop', 'hip-hop', 'rap', 'trap', 'drill',
        'schlager', 'volksmusik', 'volkstümlich',
        'klassik', 'opera', 'oper',
        'jazz fusion', 'smooth jazz', 'free jazz',
        'reggae', 'dubstep', 'dub',
        'indie', 'indie rock', 'indie pop'
    ]
    
    # Prüfe negative Indikatoren zuerst
    for negative in negative_indicators:
        if negative in text_lower:
            return False
    
    # Prüfe starke Indikatoren
    strong_match = any(indicator in text_lower for indicator in strong_indicators)
    if strong_match:
        return True
    
    # Prüfe VIP-Band
    band_match = any(band.lower() in text_lower for band in VIP_BANDS)
    
    # Prüfe mittelmäßige Indikatoren
    medium_match = any(indicator in text_lower for indicator in medium_indicators)
    
    # Nur akzeptieren wenn VIP-BAND + mittelmäßiger Indikator ODER starker Indikator
    if band_match and medium_match:
        return True
    
    return False

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
                        
                        # VERIFIZIERUNG: Nur hinzufügen wenn es wirklich zur Szene gehört
                        if not verify_event_genre(desc_text + " " + title, title):
                            print(f"   ❌ Nicht verifiziert: {title} - {date_text}")
                            continue
                        
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
                            "url": url,
                            "genres": ["Rockabilly", "Rock'n'Roll"]
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
                for country in ['Deutschland', 'Italien', 'Schweiz', 'England', 'Österreich', 'Niederlande', 'Spanien', 'Schweden', 'USA']:
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

def run_scraper():
    print("🚀 Rockabilly Radar Scraper startet...")
    print(f"📅 Heute ist: {datetime.now().strftime('%d.%m.%Y')}")
    print(f"🔮 Suche Events bis: {(datetime.now() + timedelta(days=365)).strftime('%d.%m.%Y')}")
    print(f"🎯 Filter: Nur Rockabilly, Rock'n'Roll, 50er, 60er, Lindy Hop, Jazz")
    
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
    
    verified_count = 0
    rejected_count = 0
    
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
                    
                    if len(text) < 15:
                        continue
                    
                    date_match = DATE_PATTERN.search(text)
                    date_str = date_match.group(0) if date_match else "Termin folgt"
                    
                    band_found = next((b for b in VIP_BANDS if b.lower() in text.lower()), None)
                    
                    # Titel generieren
                    if band_found:
                        title = f"{band_found} @ {target['name']}"
                    elif 'lindy hop' in text.lower() or 'swing' in text.lower():
                        title = f"Lindy Hop / Swing Event @ {target['name']}"
                    elif 'open air' in text.lower() or 'freilicht' in text.lower():
                        title = f"Open Air Rock'n'Roll @ {target['name']}"
                    elif 'festival' in text.lower():
                        title = f"Rockabilly Festival @ {target['name']}"
                    else:
                        title = f"Rock'n'Roll Live @ {target['name']}"
                    
                    # VERIFIZIERUNG: Nur hinzufügen wenn es wirklich zur Szene gehört
                    if not verify_event_genre(text, title):
                        rejected_count += 1
                        print(f"   ❌ Abgelehnt (keine Szene): {title[:50]}...")
                        continue
                    
                    if not is_duplicate(title, date_str):
                        lat, lon = get_coords(target['city'])
                        
                        # Genres extrahieren
                        genres = []
                        text_lower = text.lower()
                        if 'rockabilly' in text_lower:
                            genres.append('Rockabilly')
                        if 'rock \'n\' roll' in text_lower or 'rock\'n\'roll' in text_lower:
                            genres.append("Rock'n'Roll")
                        if 'lindy hop' in text_lower:
                            genres.append('Lindy Hop')
                        if 'swing' in text_lower:
                            genres.append('Swing')
                        if '50er' in text_lower or '50s' in text_lower:
                            genres.append('50er')
                        if '60er' in text_lower or '60s' in text_lower:
                            genres.append('60er')
                        if 'psychobilly' in text_lower:
                            genres.append('Psychobilly')
                        
                        if not genres:
                            genres = ['Rockabilly']  # Fallback
                        
                        new_event = {
                            "title": title,
                            "date": date_str,
                            "location": f"{target['name']}, {target['city']}",
                            "city": target['city'],
                            "lat": lat,
                            "lon": lon,
                            "desc": text[:250] + "..." if len(text) > 250 else text,
                            "url": target['url'],
                            "genres": genres
                        }
                        new_events_list.append(new_event)
                        found_count += 1
                        verified_count += 1
                        print(f"   ✅ Verifiziert & hinzugefügt: {title}")
                
                if found_count == 0:
                    print(f"   ⚠️ Keine verifizierten Events gefunden")
            
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
    
    print(f"\n💾 Fertig! {len(cleaned_events)} verifizierte Events gespeichert.")
    print(f"📊 Statistik:")
    print(f"   ✅ {verified_count} neue Events verifiziert & hinzugefügt")
    print(f"   ❌ {rejected_count} Events abgelehnt (keine Szene)")
    print(f"   🗑️ {removed_count} vergangene Events gelöscht")
    print(f"   🎪 {len(HARDCODED_EVENTS)} große Festivals (manuell verifiziert)")

if __name__ == "__main__":
    run_scraper()
