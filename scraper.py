import json
import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime, timedelta

OUTPUT_FILE = 'events.json'
LOG_FILE = 'scraper_log.json'

# ============================================================
# VIP BANDS – Nur echte Rockabilly / R'n'R / Lindy Hop / Jazz
# ============================================================
VIP_BANDS = [
    # Rockabilly
    "Ray Collins Hot Club", "Ray Collins' Hot Club", "Ray Allen", "Class of 58",
    "The Firebirds", "Jumpin'Up", "Jumpin' Up", "The Nymonics",
    "The Trainyard Kings", "Shotgun Jones", "Jukebox Stompers", "Boppin'B",
    "Cherry Casino", "The Baseballs", "Restless", "Matchbox", "Darrel Higham",
    "Mad Sin", "The Rattles", "Big Town Playboys", "Shakin' Stevens",
    "Stray Cats", "Rocky Sharpe", "The Jets", "The Cats", "Dave Phillips",
    "Kim Lenz", "The Hot Rods", "George And His New Heartaches",
    "Marty's Henpecked Club", "Chris Aron", "Cat Lee King",
    "Foggy Mountain Rockers", "Howlin'Ric", "Cody Lee", "Boogie Banausen",
    "Toto & Raw Deals", "Si Cranstoun", "Elbonautics",
    "Suffy Sand Rocats", "Yellow Boogie Dancers", "Imelda May",
    "The Polecats", "The Sharks", "Guana Batz", "Frantic Flintstones",
    "Batmobile", "Nekromantix", "Horrorpops", "Tiger Army",
    "Reverend Horton Heat", "Long Tall Texans", "The Barnshakers",
    # Lindy Hop / Swing / Jazz
    "Count Basie", "Duke Ellington", "Benny Goodman", "Glenn Miller",
    "Django Reinhardt", "Stéphane Grappelli"
]

# ============================================================
# VERIFIZIERTE FESTIVALS (Stand: 02.07.2026 – alle URLs geprüft)
# ============================================================
HARDCODED_EVENTS = [
    {
        "title": "Summer Jamboree 2026",
        "date": "01.08. - 09.08.2026",
        "location": "Senigallia, Italien",
        "city": "Senigallia",
        "lat": 43.7147, "lon": 13.2183,
        "desc": "Größtes Rockabilly-Festival Europas. 10 Tage Live-Musik, Lindy Hop, Vintage-Flair am Strand.",
        "url": "https://www.summerjamboree.com",
        "genres": ["Rockabilly", "Rock'n'Roll", "Lindy Hop"]
    },
    {
        "title": "Firebirds Festival 2026",
        "date": "03.07. - 05.07.2026",
        "location": "Kloster Nimbschen, Grimma",
        "city": "Grimma",
        "lat": 51.2294, "lon": 12.7561,
        "desc": "Rock'n'Roll im historischen Kloster. The Firebirds & Friends, Markt, Custom Cars.",
        "url": "https://www.firebirds-festival.de",
        "genres": ["Rock'n'Roll", "Rockabilly"]
    },
    {
        "title": "High Rockabilly 2026",
        "date": "15.05. - 17.05.2026",
        "location": "Irun, Spanien",
        "city": "Irun",
        "lat": 43.3396, "lon": -1.7894,
        "desc": "Top internationales Rockabilly-Festival mit Weltklasse-Bands.",
        "url": "https://www.highrockabilly.com",
        "genres": ["Rockabilly", "Rock'n'Roll"]
    },
    {
        "title": "Hemsby Rock'n'Roll Weekender 2026",
        "date": "15.05. - 18.05.2026",
        "location": "Hemsby, England",
        "city": "Hemsby",
        "lat": 52.6750, "lon": 1.6850,
        "desc": "Kult-Weekender in England. Internationale Bands, DJs, Lindy Hop, Vintage-Markt.",
        "url": "https://www.hemsbyrockweekender.co.uk",
        "genres": ["Rock'n'Roll", "Lindy Hop", "50er"]
    },
    {
        "title": "Rhythm Riot 2026",
        "date": "13.11. - 15.11.2026",
        "location": "Camber Sands, Rye, England",
        "city": "Rye",
        "lat": 50.9324, "lon": 0.7941,
        "desc": "UKs legendärer Rhythm & Blues und Rock'n'Roll Weekender.",
        "url": "https://www.rhythmriot.com",
        "genres": ["Rock'n'Roll", "Rhythm & Blues", "Lindy Hop"]
    },
    {
        "title": "Viva Las Vegas 2026",
        "date": "16.04. - 19.04.2026",
        "location": "Las Vegas, USA",
        "city": "Las Vegas",
        "lat": 36.1699, "lon": -115.1398,
        "desc": "Das legendärste Rockabilly-Festival der Welt im Orleans Hotel.",
        "url": "https://www.vivalasvegas.net",
        "genres": ["Rockabilly", "Rock'n'Roll", "50er"]
    },
    {
        "title": "Psychobilly Meeting 2026",
        "date": "23.10. - 25.10.2026",
        "location": "Pineda de Mar, Spanien",
        "city": "Pineda de Mar",
        "lat": 41.6200, "lon": 2.6847,
        "desc": "Größtes Psychobilly-Festival der Welt am Mittelmeer.",
        "url": "https://www.psychobillymeeting.com",
        "genres": ["Psychobilly", "Rockabilly"]
    }
]

# ============================================================
# VERIFIZIERTE WEBSEITEN (Stand: 02.07.2026 – alle erreichbar)
# ============================================================
TARGETS = [
    {"name": "Noels Ballroom",           "url": "https://noels-ballroom.de/",                        "city": "Leipzig"},
    {"name": "Tonelli's Leipzig",        "url": "http://www.tonellis.de/programm.html",              "city": "Leipzig"},
    {"name": "Tanzcafé Waldenburg",      "url": "https://www.tanzcafe-waldenburg.de/",               "city": "Waldenburg"},
    {"name": "Kulturfabrik Leipzig",     "url": "https://www.kufa.info/programm/",                   "city": "Leipzig"},
    {"name": "Conne Island Leipzig",     "url": "https://www.conne-island.de/programm",              "city": "Leipzig"},
    {"name": "Naumanns Leipzig",         "url": "https://www.naumanns-leipzig.de/programm",          "city": "Leipzig"},
    {"name": "Tante Ella Leipzig",       "url": "https://www.tante-ella.de/programm/",               "city": "Leipzig"},
    {"name": "Musikclub Zwickau",        "url": "https://www.musikclub-zwickau.de/programm/",        "city": "Zwickau"},
    {"name": "Alter Schlachthof Dresden","url": "https://www.alter-schlachthof-dresden.de/programm/","city": "Dresden"},
    {"name": "Club Passage Erfurt",      "url": "https://www.club-passage.de/programm/",             "city": "Erfurt"},
    {"name": "Rockabilly Radio Events",  "url": "https://www.rockabillyradio.net/events/",           "city": "Diverse"},
    {"name": "Rock'n'Roll Calendar NL",  "url": "https://www.rockabilly.nl/calendar.php",            "city": "Diverse"}
]

# ============================================================
# DATUMS-PARSING
# ============================================================
DATE_PATTERN = re.compile(r'\b\d{1,2}\.\d{1,2}\.?\s*(?:\d{4})?\b')

MONTHS_DE = {
    'januar': 1, 'jan': 1, 'februar': 2, 'feb': 2,
    'märz': 3, 'maerz': 3, 'mar': 3, 'april': 4, 'apr': 4,
    'mai': 5, 'juni': 6, 'jun': 6, 'juli': 7, 'jul': 7,
    'august': 8, 'aug': 8, 'september': 9, 'sep': 9, 'sept': 9,
    'oktober': 10, 'okt': 10, 'november': 11, 'nov': 11,
    'dezember': 12, 'dez': 12
}


def parse_german_date(date_str):
    """Parst deutsche Datumsformate inkl. ausgeschriebene Monate."""
    if not date_str:
        return None
    date_str = date_str.strip().lower()

    # Wochentage entfernen
    for day in ['montag', 'dienstag', 'mittwoch', 'donnerstag', 'freitag',
                'samstag', 'sonntag', 'mo.', 'di.', 'mi.', 'do.', 'fr.', 'sa.', 'so.']:
        if date_str.startswith(day):
            date_str = date_str[len(day):].strip().lstrip(',')

    # Muster: 12.05.2026
    m = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', date_str)
    if m:
        try:
            return datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except ValueError:
            pass

    # Muster: 12.05. (ohne Jahr)
    m = re.search(r'(\d{1,2})\.(\d{1,2})\.?$', date_str)
    if m:
        year = datetime.now().year
        try:
            d = datetime(year, int(m.group(2)), int(m.group(1)))
            if d < datetime.now():
                d = d.replace(year=year + 1)
            return d
        except ValueError:
            pass

    # Muster: 12. Mai 2026
    m = re.search(r'(\d{1,2})[\.\s]+([a-zA-ZäöüÄÖÜß]+)\s*(\d{4})?', date_str)
    if m:
        month = MONTHS_DE.get(m.group(2).lower())
        if month:
            year = int(m.group(3)) if m.group(3) else datetime.now().year
            try:
                d = datetime(year, month, int(m.group(1)))
                if not m.group(3) and d < datetime.now():
                    d = d.replace(year=year + 1)
                return d
            except ValueError:
                pass
    return None


def is_past_event(date_str, days_buffer=1):
    """Prüft ob Event vergangen ist."""
    d = parse_german_date(date_str)
    if not d:
        return False
    return d < (datetime.now() - timedelta(days=days_buffer))


# ============================================================
# GPS-KOORDINATEN
# ============================================================
def get_coords(city_name):
    """Holt Koordinaten via Nominatim mit Länder-Fallback."""
    city_clean = re.sub(
        r'(Deutschland|Italien|Schweiz|England|Österreich|Niederlande|Spanien|Schweden|USA)',
        '', city_name
    ).strip()
    if len(city_clean) < 3:
        return None, None

    headers = {'User-Agent': 'RockabillyRadarBot/1.0'}
    for query in [city_clean, f"{city_clean}, Germany"]:
        try:
            resp = requests.get(
                f"https://nominatim.openstreetmap.org/search?format=json&q={query}&limit=1",
                headers=headers, timeout=5
            )
            data = resp.json()
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
        except Exception:
            continue
    return None, None


# ============================================================
# URL-ERREICHBARKEITSPRÜFUNG
# ============================================================
def check_url_alive(url, timeout=8):
    """Prüft ob URL erreichbar ist. Gibt True/False zurück."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        resp = requests.head(url, timeout=timeout, allow_redirects=True, headers=headers)
        if resp.status_code == 200:
            return True
    except Exception:
        pass
    # Fallback: GET-Request
    try:
        resp = requests.get(url, timeout=timeout, headers=headers)
        return resp.status_code == 200
    except Exception:
        return False


# ============================================================
# GENRE-VERIFIZIERUNG
# ============================================================
STRONG_INDICATORS = [
    'rockabilly', 'rock \'n\' roll', 'rock\'n\'roll', 'rock and roll',
    'rock n roll', 'r\'n\'r', '50er jahre', '50er party', '50s', 'fifties',
    '60er jahre', '60er party', '60s', 'sixties', 'teddy boy', 'teddyboy',
    'lindy hop', 'lindyhop', 'swing dance', 'swing tanzen', 'jitterbug',
    'boogie woogie', 'psychobilly', 'neo-rockabilly', 'swing jazz',
    'gypsy jazz', 'hot club', 'jukebox', 'greaser', 'pin-up', 'pinup'
]

NEGATIVE_INDICATORS = [
    'techno', 'house', 'trance', 'edm', 'electronic', 'metal', 'heavy metal',
    'death metal', 'punk', 'hardcore', 'grunge', 'hip hop', 'rap', 'trap',
    'schlager', 'volksmusik', 'klassik', 'opera', 'reggae', 'dubstep', 'indie'
]


def verify_genre(text, title=''):
    """Streng: Nur Rockabilly/R'n'R/Lindy Hop/Jazz/50er/60er."""
    combined = (text + ' ' + title).lower()
    if any(neg in combined for neg in NEGATIVE_INDICATORS):
        return False
    if any(pos in combined for pos in STRONG_INDICATORS):
        return True
    if any(band.lower() in combined for band in VIP_BANDS):
        return True
    return False


# ============================================================
# JUKEBOX STOMPERS SPEZIAL-PARSER
# ============================================================
def parse_jukebox_stompers():
    """Parst den Jukebox Stompers Veranstaltungskalender."""
    print("🔍 Parse Jukebox Stompers Kalender...")
    events = []
    url = "https://www.jukeboxstompers.de/index.php/veranstaltungen/veranstaltungskalender"

    if not check_url_alive(url):
        print("   ⛔ Jukebox Stompers URL nicht erreichbar")
        return events

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            print(f"   ❌ HTTP {resp.status_code}")
            return events

        soup = BeautifulSoup(resp.text, 'html.parser')
        for table in soup.find_all('table'):
            for row in table.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) < 3:
                    continue

                date_text = cols[0].get_text(strip=True)
                location_text = cols[1].get_text(separator=" ", strip=True)
                desc_text = cols[2].get_text(separator=" ", strip=True)

                if not date_text or len(date_text) < 5:
                    continue

                title = None
                for line in desc_text.split('\n'):
                    line = line.strip().replace('**', '')
                    if 5 < len(line) < 100:
                        title = line
                        break
                if not title:
                    title = "Jukebox Stompers Live"

                if not verify_genre(desc_text + ' ' + title, title):
                    print(f"   ❌ Nicht verifiziert: {title[:50]}")
                    continue

                # Stadt extrahieren
                city = "Unbekannt"
                for line in location_text.split('\n'):
                    line = line.strip().replace('**', '')
                    if len(line) > 2 and line[0].isupper():
                        for country in ['Deutschland', 'Italien', 'Schweiz', 'England', 'Österreich']:
                            line = line.replace(country, '').strip()
                        if len(line) > 2:
                            city = line
                            break

                lat, lon = get_coords(city)
                desc = re.sub(r'\s+', ' ', desc_text).strip()
                if len(desc) > 300:
                    desc = desc[:300] + "..."

                events.append({
                    "title": title,
                    "date": date_text,
                    "location": location_text.replace("\n", ", "),
                    "city": city,
                    "lat": lat, "lon": lon,
                    "desc": desc,
                    "url": url,
                    "genres": ["Rockabilly", "Rock'n'Roll"]
                })
                print(f"   ✅ {title} – {date_text} – {city}")

        time.sleep(2)
    except Exception as e:
        print(f"   ❌ Fehler: {e}")

    return events


# ============================================================
# HAUPTPROZESS
# ============================================================
def run_scraper():
    start_time = datetime.now()
    print("=" * 60)
    print("🚀 Rockabilly Radar Scraper startet")
    print(f"📅 {start_time.strftime('%d.%m.%Y %H:%M')}")
    print(f"🔮 Suche bis {(start_time + timedelta(days=365)).strftime('%d.%m.%Y')}")
    print(f"🎯 Nur: Rockabilly, R'n'R, 50er, 60er, Lindy Hop, Jazz")
    print("=" * 60)

    # Bestehende Events laden
    existing_events = []
    try:
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            existing_events = json.load(f)
    except Exception:
        pass

    new_events = list(HARDCODED_EVENTS)
    log_entries = []

    def is_duplicate(title, date):
        for ev in existing_events + new_events:
            if ev.get('title') == title and ev.get('date') == date:
                return True
        return False

    # --- 1. Jukebox Stompers ---
    jukebox_events = parse_jukebox_stompers()
    for ev in jukebox_events:
        if not is_duplicate(ev['title'], ev['date']):
            new_events.append(ev)
            print(f"   ✅ Hinzugefügt: {ev['title']}")

    # --- 2. Verifizierte Webseiten ---
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    stats = {'verified': 0, 'rejected': 0, 'dead_urls': 0, 'errors': 0}

    for target in TARGETS:
        print(f"\n🔍 {target['name']} ({target['url']})")

        # URL vorab prüfen
        if not check_url_alive(target['url']):
            print(f"   ⛔ NICHT ERREICHBAR – übersprungen")
            stats['dead_urls'] += 1
            log_entries.append({
                "source": target['name'],
                "url": target['url'],
                "status": "dead",
                "time": datetime.now().isoformat()
            })
            continue

        try:
            resp = requests.get(target['url'], headers=headers, timeout=10)
            if resp.status_code != 200:
                print(f"   ❌ HTTP {resp.status_code}")
                stats['errors'] += 1
                continue

            soup = BeautifulSoup(resp.text, 'html.parser')
            elements = soup.find_all(['p', 'li', 'div', 'article', 'h3', 'h4'])
            found = 0

            for el in elements:
                text = el.get_text(separator=" ", strip=True)
                if len(text) < 15:
                    continue

                date_match = DATE_PATTERN.search(text)
                date_str = date_match.group(0) if date_match else "Termin folgt"

                band_found = next((b for b in VIP_BANDS if b.lower() in text.lower()), None)

                if band_found:
                    title = f"{band_found} @ {target['name']}"
                elif 'lindy hop' in text.lower() or 'swing' in text.lower():
                    title = f"Lindy Hop / Swing @ {target['name']}"
                elif 'open air' in text.lower() or 'freilicht' in text.lower():
                    title = f"Open Air Rock'n'Roll @ {target['name']}"
                elif 'festival' in text.lower():
                    title = f"Festival @ {target['name']}"
                else:
                    title = f"Rock'n'Roll Live @ {target['name']}"

                if not verify_genre(text, title):
                    stats['rejected'] += 1
                    continue

                if not is_duplicate(title, date_str):
                    lat, lon = get_coords(target['city'])

                    genres = []
                    tl = text.lower()
                    if 'rockabilly' in tl: genres.append('Rockabilly')
                    if any(x in tl for x in ["rock 'n' roll", "rock'n'roll"]): genres.append("Rock'n'Roll")
                    if 'lindy hop' in tl: genres.append('Lindy Hop')
                    if 'swing' in tl: genres.append('Swing')
                    if any(x in tl for x in ['50er', '50s']): genres.append('50er')
                    if any(x in tl for x in ['60er', '60s']): genres.append('60er')
                    if 'psychobilly' in tl: genres.append('Psychobilly')
                    if not genres: genres = ['Rockabilly']

                    new_events.append({
                        "title": title,
                        "date": date_str,
                        "location": f"{target['name']}, {target['city']}",
                        "city": target['city'],
                        "lat": lat, "lon": lon,
                        "desc": (text[:250] + "...") if len(text) > 250 else text,
                        "url": target['url'],
                        "genres": genres
                    })
                    found += 1
                    stats['verified'] += 1
                    print(f"   ✅ {title}")

            if found == 0:
                print(f"   ⚠️ Keine verifizierten Events")

        except Exception as e:
            print(f"   ❌ Fehler: {e}")
            stats['errors'] += 1
            log_entries.append({
                "source": target['name'],
                "url": target['url'],
                "status": f"error: {str(e)[:100]}",
                "time": datetime.now().isoformat()
            })

        time.sleep(2)

    # --- 3. Vergangene Events löschen ---
    print(f"\n{'=' * 60}")
    print("🧹 Entferne vergangene Events...")
    before = len(new_events)
    cleaned = []
    removed = 0
    for ev in new_events:
        ds = ev.get('date', '')
        if not ds or ds == "Termin folgt" or not is_past_event(ds):
            cleaned.append(ev)
        else:
            removed += 1
            print(f"   🗑️ {ev['title']} ({ds})")
    print(f"   ✅ {removed} alte Events entfernt ({before} → {len(cleaned)})")

    # --- 4. Speichern ---
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    # --- 5. Log speichern ---
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log_entries, f, ensure_ascii=False, indent=2)

    # --- 6. Zusammenfassung ---
    runtime = (datetime.now() - start_time).total_seconds()
    print(f"\n{'=' * 60}")
    print(f"💾 Fertig! {len(cleaned)} Events gespeichert")
    print(f"⏱️ Laufzeit: {runtime:.1f} Sekunden")
    print(f"📊 Statistik:")
    print(f"   ✅ {stats['verified']} neue Events verifiziert")
    print(f"   ❌ {stats['rejected']} abgelehnt (kein Szene-Genre)")
    print(f"   ⛔ {stats['dead_urls']} tote URLs übersprungen")
    print(f"   ⚠️ {stats['errors']} Fehler")
    print(f"   🗑️ {removed} vergangene Events gelöscht")
    print(f"   🎪 {len(HARDCODED_EVENTS)} Festivals (manuell verifiziert)")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    run_scraper()
