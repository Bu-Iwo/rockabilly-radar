#!/usr/bin/env python3
"""
Rockabilly Radar Event Scraper - EXPANDED VERSION
Mit 6 Quellen: WeLoveCountry, JukeboxStompers, SwingCalendar, SwingInDD, Dresden-Hepcats, Lindypott
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime, timedelta
from urllib.parse import urljoin, quote
import sys

GEOCODE_CACHE = {}

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def geocode(city):
    if not city:
        return None
    if city in GEOCODE_CACHE:
        return GEOCODE_CACHE[city]
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": city, "format": "json", "limit": 1},
            headers={"User-Agent": "RockabillyRadar/1.0"},
            timeout=10
        )
        data = r.json()
        if data:
            coords = (float(data[0]["lat"]), float(data[0]["lon"]))
            GEOCODE_CACHE[city] = coords
            time.sleep(1.1)
            return coords
    except Exception as e:
        log(f"  ⚠ Geocode error: {e}")
    return None

def parse_date(text):
    m = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', text)
    if m:
        d, mo, y = m.groups()
        return f"{int(d):02d}.{int(mo):02d}.{y}"
    m = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', text)
    if m:
        d, mo, y = m.groups()
        return f"{int(d):02d}.{int(mo):02d}.{y}"
    m = re.search(r'(\d{1,2})\.(\d{1,2})\.', text)
    if m:
        d, mo = m.groups()
        return f"{int(d):02d}.{int(mo):02d}.{datetime.now().year}"
    return None

def parse_date_for_sort(date_str):
    try:
        m = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', date_str)
        if m:
            d, mo, y = m.groups()
            return datetime(int(y), int(mo), int(d))
        m = re.search(r'(\d{2})\.(\d{2})\.', date_str)
        if m:
            d, mo = m.groups()
            return datetime(datetime.now().year, int(mo), int(d))
    except:
        pass
    return datetime.max

def extract_time(text):
    times = []
    patterns = [
        r'(?:Beginn|Einlass|Start|Einlass:|Beginn:)\s*(\d{1,2}:\d{2})\s*(?:Uhr)?',
        r'(\d{1,2}:\d{2})\s*Uhr',
        r'(\d{1,2})\s*:\s*(\d{2})',
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                times.append(f"{match[0]}:{match[1]}")
            else:
                times.append(match)
    return ', '.join(times[:3]) if times else None

def extract_price(text):
    patterns = [
        r'(\d+[,.]?\d*)\s*(?:€|Euro)',
        r'Eintritt[:\s]*(?:frei|kostenlos|free)',
        r'kostenlos',
        r'frei',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    return None

def extract_bands(text):
    patterns = [
        r'(?:Bands?|Live|Musik)[:\s]*([^\n]+)',
        r'([A-Z][a-z]+\s+(?:&|and)\s+[A-Z][a-z]+(?:\s+Band)?)',
    ]
    bands = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if len(match) > 3 and len(match) < 100:
                bands.append(match.strip())
    return bands[:5] if bands else None

def generate_smart_url(base_url, date, city):
    if not date:
        return base_url
    
    m = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', date)
    if m:
        d, mo, y = m.groups()
        date_iso = f"{y}-{mo}-{d}"
        
        anchors = [
            f"#date-{date_iso}",
            f"#{date_iso}",
            f"#event-{date_iso}",
            f"#cal-{date_iso}",
        ]
        
        return base_url + anchors[0]
    
    return base_url

def get_first_thursday(year, month):
    """Berechnet den ersten Donnerstag eines Monats"""
    first_day = datetime(year, month, 1)
    # Donnerstag = 3 (Montag = 0)
    days_until_thursday = (3 - first_day.weekday()) % 7
    if days_until_thursday == 0 and first_day.weekday() != 3:
        days_until_thursday = 7
    first_thursday = first_day + timedelta(days=days_until_thursday)
    return first_thursday

def scrape_dresden_hepcats():
    """Scrapt Dresden Hepcats - Live Tanz Bar (jeden ersten Donnerstag)"""
    events = []
    url = "https://www.dresden-hepcats.de/socials-de"
    
    log("\n" + "="*70)
    log("[5/6] SCRAPING: Dresden-Hepcats (Live Tanz Bar)")
    log("="*70)
    
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        r = requests.get(url, headers=headers, timeout=30)
        
        if r.status_code != 200:
            log(f"❌ Status {r.status_code}")
            return events
        
        soup = BeautifulSoup(r.text, "lxml")
        text = soup.get_text(" ", strip=True)
        
        log(f"✓ Seite geladen: {len(r.text)} bytes")
        
        # Aus der Knowledge Base: "Jeden ersten Donnerstag im Monat"
        # "Parkhotel auf dem Weißen Hirsch"
        # Generiere Events für die nächsten 12 Monate
        
        now = datetime.now()
        city = "Dresden"
        address = "Parkhotel, Bautzner Landstraße 32, 01324 Dresden"
        
        for month_offset in range(12):
            target_date = now + timedelta(days=30 * month_offset)
            year = target_date.year
            month = target_date.month
            
            first_thursday = get_first_thursday(year, month)
            
            # Nur zukünftige Events
            if first_thursday < now:
                continue
            
            date_str = first_thursday.strftime("%d.%m.%Y")
            
            # Extrahiere zusätzliche Infos aus der Seite
            time_info = "20:00 Uhr"  # Typische Zeit für Socials
            price_info = None
            
            # Versuche Bands aus dem Text zu extrahieren
            bands = extract_bands(text)
            
            ev = {
                "title": "Live Tanz Bar",
                "date": date_str,
                "city": city,
                "address": address,
                "desc": "Social mit Live-Band im Parkhotel auf dem Weißen Hirsch. Regionale und überregionale Swing Bands live. Vorher Swing-Basics für Neueinsteiger.",
                "time": time_info,
                "price": price_info,
                "bands": bands,
                "url": url,
                "event_url": url,  # Hepcats hat keine Anker für spezifische Daten
                "genres": ["Swing", "Lindy Hop"]
            }
            
            coords = geocode(city)
            if coords:
                ev["lat"], ev["lon"] = coords
            
            events.append(ev)
            
            if len(events) <= 3:
                log(f"  → {date_str} | {city} | Live Tanz Bar")
        
        log(f"✅ Dresden-Hepcats: {len(events)} Events generiert")
        
    except Exception as e:
        log(f"❌ ERROR: {type(e).__name__}: {str(e)}")
        import traceback
        log(traceback.format_exc())
    
    return events

def scrape_lindypott():
    """Scrapt Lindypott Kalender für Ruhrgebiet"""
    events = []
    url = "https://www.lindypott.de/kalender.html?ort=BO,DO,E&art=3"
    
    log("\n" + "="*70)
    log("[6/6] SCRAPING: Lindypott (Ruhrgebiet)")
    log("="*70)
    
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        r = requests.get(url, headers=headers, timeout=30)
        
        if r.status_code != 200:
            log(f"❌ Status {r.status_code}")
            return events
        
        soup = BeautifulSoup(r.text, "lxml")
        text = soup.get_text("\n", strip=True)
        
        log(f"✓ Seite geladen: {len(r.text)} bytes")
        
        # Suche nach Event-Patterns
        # Typisches Format: "DD.MM.YYYY\nEvent-Titel\nOrt\nDetails"
        
        items = soup.find_all(["div", "article", "li", "tr"])
        log(f"Container gefunden: {len(items)}")
        
        cities_mapping = {
            "BO": "Bochum",
            "DO": "Dortmund",
            "E": "Essen"
        }
        
        for item in items:
            item_text = item.get_text(" ", strip=True)
            date = parse_date(item_text)
            
            if not date or len(item_text) < 20:
                continue
            
            # Versuche Titel zu finden
            title_el = item.find(["h2", "h3", "h4", "strong", "b"])
            if title_el:
                title = title_el.get_text(strip=True)
            else:
                lines = item_text.split("\n")
                title = lines[0][:80] if lines else item_text[:80]
            
            if len(title) < 3:
                continue
            
            # Stadt erkennen
            city = ""
            for code, city_name in cities_mapping.items():
                if city_name.lower() in item_text.lower() or code in item_text:
                    city = city_name
                    break
            
            # Extrahiere Details
            time_info = extract_time(item_text)
            price_info = extract_price(item_text)
            bands_info = extract_bands(item_text)
            
            genres = ["Swing"]
            tl = item_text.lower()
            if "lindy" in tl: genres.append("Lindy Hop")
            if "balboa" in tl: genres.append("Balboa")
            if "charleston" in tl: genres.append("Charleston")
            if "boogie" in tl: genres.append("Boogie Woogie")
            
            # Versuche direkten Link zu finden
            link = item.find("a", href=True)
            if link:
                event_url = urljoin(url, link["href"])
            else:
                event_url = generate_smart_url(url, date, city)
            
            ev = {
                "title": title,
                "date": date,
                "city": city,
                "address": city,
                "desc": item_text[:500],
                "time": time_info,
                "price": price_info,
                "bands": bands_info,
                "url": url,
                "event_url": event_url,
                "genres": list(set(genres))
            }
            
            if city:
                coords = geocode(city)
                if coords:
                    ev["lat"], ev["lon"] = coords
            
            events.append(ev)
            
            if len(events) <= 3:
                log(f"  → {date} | {city} | {title[:40]}")
        
        log(f"✅ Lindypott: {len(events)} Events gefunden")
        
    except Exception as e:
        log(f"❌ ERROR: {type(e).__name__}: {str(e)}")
        import traceback
        log(traceback.format_exc())
    
    return events

def scrape_we_love_country():
    """WeLoveCountry mit erweiterten Details"""
    events = []
    url = "https://www.we-love-country.de/1_term.php"
    
    log("\n" + "="*70)
    log("[1/6] SCRAPING: WeLoveCountry")
    log("="*70)
    
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        r = requests.get(url, headers=headers, timeout=60)
        r.encoding = "utf-8"
        
        if r.status_code != 200:
            return events
        
        log(f"✓ Seite geladen: {len(r.text)} bytes")
        
        soup = BeautifulSoup(r.text, "lxml")
        text = soup.get_text("\n", strip=True)
        
        pattern = r'(?:Mo|Di|Mi|Do|Fr|Sa|So)\.?\s+(\d{2}\.\d{2}\.\d{4})\s+(\d{5})\s+([^\n]+)\n([^\n]+)(?:\n([^\n]+))?(?:\n([^\n]+))?'
        matches = re.findall(pattern, text)
        
        log(f"✓ {len(matches)} Event-Blöcke gefunden")
        
        for match in matches:
            if len(match) >= 4:
                date = match[0]
                plz = match[1]
                city = match[2].strip()
                title = match[3].strip()
                details = match[4].strip() if len(match) > 4 else ""
                extra = match[5].strip() if len(match) > 5 else ""
                
                if len(title) < 3:
                    continue
                
                full_text = f"{title} {details} {extra}"
                
                time_info = extract_time(full_text)
                price_info = extract_price(full_text)
                bands_info = extract_bands(full_text)
                address = f"{plz} {city}"
                
                genres = ["Country"]
                full_lower = full_text.lower()
                
                if "line dance" in full_lower: genres.append("Line Dance")
                if "rockabilly" in full_lower: genres.append("Rockabilly")
                if "rock'n'roll" in full_lower or "rock 'n' roll" in full_lower: genres.append("Rock'n'Roll")
                if "irish" in full_lower: genres.append("Irish")
                if "boogie" in full_lower: genres.append("Boogie Woogie")
                
                ev = {
                    "title": title,
                    "date": date,
                    "city": city,
                    "address": address,
                    "desc": f"{details} {extra}".strip()[:500],
                    "time": time_info,
                    "price": price_info,
                    "bands": bands_info,
                    "url": url,
                    "event_url": generate_smart_url(url, date, city),
                    "genres": list(set(genres))
                }
                
                coords = geocode(city)
                if coords:
                    ev["lat"], ev["lon"] = coords
                
                events.append(ev)
        
        log(f"✅ WeLoveCountry: {len(events)} Events extrahiert")
        
    except Exception as e:
        log(f"❌ ERROR: {type(e).__name__}: {str(e)}")
    
    return events

def scrape_jukeboxstompers():
    """JukeboxStompers mit erweiterten Details"""
    events = []
    url = "https://www.jukeboxstompers.de/index.php/veranstaltungen/veranstaltungskalender"
    
    log("\n" + "="*70)
    log("[2/6] SCRAPING: JukeboxStompers")
    log("="*70)
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=30)
        
        if r.status_code != 200:
            return events
        
        soup = BeautifulSoup(r.text, "lxml")
        tables = soup.find_all("table")
        
        for table in tables:
            for row in table.find_all("tr"):
                cells = row.find_all(["td", "th"])
                if len(cells) < 2:
                    continue
                
                text = row.get_text(" ", strip=True)
                date = parse_date(text)
                if not date:
                    continue
                
                title_cell = cells[0]
                title_el = title_cell.find(["strong", "b", "a"])
                title = title_el.get_text(strip=True) if title_el else text[:80]
                
                if len(title) < 3:
                    continue
                
                city_match = re.search(r'(?:in|@|,)\s*([A-ZÄÖÜ][a-zäöüß\-]+)', text)
                city = city_match.group(1) if city_match else ""
                
                time_info = extract_time(text)
                price_info = extract_price(text)
                bands_info = extract_bands(text)
                
                address = ""
                if len(cells) >= 2:
                    addr_text = cells[1].get_text(strip=True)
                    if len(addr_text) > 10 and len(addr_text) < 200:
                        address = addr_text
                
                genres = ["Rock'n'Roll"]
                tl = text.lower()
                if "boogie" in tl: genres.append("Boogie Woogie")
                if "swing" in tl or "lindy" in tl: genres.append("Swing")
                if "rockabilly" in tl: genres.append("Rockabilly")
                
                event_link = title_cell.find("a", href=True)
                event_url = urljoin(url, event_link["href"]) if event_link else generate_smart_url(url, date, city)
                
                ev = {
                    "title": title,
                    "date": date,
                    "city": city,
                    "address": address if address else city,
                    "desc": text[:500],
                    "time": time_info,
                    "price": price_info,
                    "bands": bands_info,
                    "url": url,
                    "event_url": event_url,
                    "genres": list(set(genres))
                }
                
                if city:
                    coords = geocode(city)
                    if coords:
                        ev["lat"], ev["lon"] = coords
                
                events.append(ev)
        
        log(f"✅ JukeboxStompers: {len(events)} Events gefunden")
        
    except Exception as e:
        log(f"❌ ERROR: {type(e).__name__}: {str(e)}")
    
    return events

def scrape_swingcalendar():
    """SwingCalendar"""
    events = []
    url = "https://swingcalendar.com/de"
    
    log("\n" + "="*70)
    log("[3/6] SCRAPING: SwingCalendar")
    log("="*70)
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=30)
        
        if r.status_code != 200:
            return events
        
        soup = BeautifulSoup(r.text, "lxml")
        items = soup.find_all(["div", "article", "li"])
        
        for item in items:
            item_text = item.get_text(" ", strip=True)
            date = parse_date(item_text)
            
            if not date or len(item_text) < 20:
                continue
            
            title_el = item.find(["h2", "h3", "h4", "strong"])
            if title_el:
                title = title_el.get_text(strip=True)
            else:
                lines = item_text.split("\n")
                title = lines[0][:80] if lines else item_text[:80]
            
            if len(title) < 3:
                continue
            
            cities = ["Berlin", "Dresden", "Leipzig", "München", "Hamburg", "Köln", 
                     "Frankfurt", "Wien", "Zürich", "London", "Paris", "Rom", 
                     "Madrid", "Prag", "Amsterdam", "Stockholm", "Oslo", "Helsinki"]
            city = next((c for c in cities if c in item_text), "")
            
            time_info = extract_time(item_text)
            price_info = extract_price(item_text)
            
            genres = ["Swing"]
            tl = item_text.lower()
            if "lindy" in tl: genres.append("Lindy Hop")
            if "balboa" in tl: genres.append("Balboa")
            if "charleston" in tl: genres.append("Charleston")
            
            link = item.find("a", href=True)
            ev_url = urljoin(url, link["href"]) if link else generate_smart_url(url, date, city)
            
            ev = {
                "title": title,
                "date": date,
                "city": city,
                "address": city,
                "desc": item_text[:500],
                "time": time_info,
                "price": price_info,
                "bands": None,
                "url": url,
                "event_url": ev_url,
                "genres": list(set(genres))
            }
            
            if city:
                coords = geocode(city)
                if coords:
                    ev["lat"], ev["lon"] = coords
            
            events.append(ev)
        
        log(f"✅ SwingCalendar: {len(events)} Events gefunden")
        
    except Exception as e:
        log(f"❌ ERROR: {type(e).__name__}: {str(e)}")
    
    return events

def scrape_swingindd():
    """SwingInDD"""
    events = []
    url = "https://swingindd.com/home/regionale-swing-kalender/"
    
    log("\n" + "="*70)
    log("[4/6] SCRAPING: SwingInDD")
    log("="*70)
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=30)
        
        if r.status_code != 200:
            return events
        
        soup = BeautifulSoup(r.text, "lxml")
        items = soup.find_all(["div", "article", "li"])
        
        for item in items:
            item_text = item.get_text(" ", strip=True)
            date = parse_date(item_text)
            
            if not date or len(item_text) < 20:
                continue
            
            title_el = item.find(["h2", "h3", "h4", "strong"])
            if title_el:
                title = title_el.get_text(strip=True)
            else:
                lines = item_text.split("\n")
                title = lines[0][:80] if lines else item_text[:80]
            
            if len(title) < 3:
                continue
            
            city = "Dresden" if "dresden" in item_text.lower() else ""
            
            time_info = extract_time(item_text)
            price_info = extract_price(item_text)
            
            genres = ["Swing"]
            tl = item_text.lower()
            if "lindy" in tl: genres.append("Lindy Hop")
            if "balboa" in tl: genres.append("Balboa")
            if "charleston" in tl: genres.append("Charleston")
            
            link = item.find("a", href=True)
            ev_url = urljoin(url, link["href"]) if link else generate_smart_url(url, date, city)
            
            ev = {
                "title": title,
                "date": date,
                "city": city,
                "address": city,
                "desc": item_text[:500],
                "time": time_info,
                "price": price_info,
                "bands": None,
                "url": url,
                "event_url": ev_url,
                "genres": list(set(genres))
            }
            
            if city:
                coords = geocode(city)
                if coords:
                    ev["lat"], ev["lon"] = coords
            
            events.append(ev)
        
        log(f"✅ SwingInDD: {len(events)} Events gefunden")
        
    except Exception as e:
        log(f"❌ ERROR: {type(e).__name__}: {str(e)}")
    
    return events

def deduplicate(events):
    seen = set()
    unique = []
    for ev in events:
        key = f"{ev['title']}_{ev['date']}_{ev.get('city', '')}"
        if key not in seen:
            seen.add(key)
            unique.append(ev)
    return unique

def main():
    log("="*70)
    log("🎸 ROCKABILLY RADAR EVENT SCRAPER - EXPANDED (6 Quellen)")
    log("="*70)
    
    all_events = []
    
    all_events.extend(scrape_we_love_country())
    time.sleep(2)
    
    all_events.extend(scrape_jukeboxstompers())
    time.sleep(2)
    
    all_events.extend(scrape_swingcalendar())
    time.sleep(2)
    
    all_events.extend(scrape_swingindd())
    time.sleep(2)
    
    all_events.extend(scrape_dresden_hepcats())
    time.sleep(2)
    
    all_events.extend(scrape_lindypott())
    
    log("\n" + "="*70)
    log("ZUSAMMENFASSUNG")
    log("="*70)
    log(f"Total vor Deduplikation: {len(all_events)}")
    
    all_events = deduplicate(all_events)
    log(f"Total nach Deduplikation: {len(all_events)}")
    
    all_events = sorted(all_events, key=lambda e: parse_date_for_sort(e['date']))
    log("✓ Chronologisch sortiert")
    
    with open("events.json", "w", encoding="utf-8") as f:
        json.dump(all_events, f, ensure_ascii=False, indent=2)
    
    log(f"\n✅ GESPEICHERT: events.json")
    log(f"   Events: {len(all_events)}")
    log("="*70)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"\n❌ FATAL: {type(e).__name__}: {str(e)}")
        import traceback
        log(traceback.format_exc())
        sys.exit(1)
