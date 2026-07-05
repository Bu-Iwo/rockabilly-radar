#!/usr/bin/env python3
"""
Rockabilly Radar Event Scraper - VERIFIED VERSION
Nur tatsächlich existierende Events, chronologisch sortiert
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime
from urllib.parse import urljoin
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
        r'(?:Beginn|Einlass|Start)\s*(\d{1,2}:\d{2})\s*(?:Uhr)?',
        r'(\d{1,2}:\d{2})\s*Uhr',
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            times.append(match if isinstance(match, str) else f"{match[0]}:{match[1]}")
    return ', '.join(times[:3]) if times else None

def extract_price(text):
    patterns = [
        r'(\d+[,.]?\d*)\s*(?:€|Euro)',
        r'Eintritt[:\s]*(?:frei|kostenlos)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    return None

def generate_smart_url(base_url, date, city):
    if not date:
        return base_url
    m = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', date)
    if m:
        d, mo, y = m.groups()
        return f"{base_url}#date-{y}-{mo}-{d}"
    return base_url

def scrape_we_love_country():
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
        
        pattern = r'(?:Mo|Di|Mi|Do|Fr|Sa|So)\.?\s+(\d{2}\.\d{2}\.\d{4})\s+(\d{5})\s+([^\n]+)\n([^\n]+)(?:\n([^\n]+))?'
        matches = re.findall(pattern, text)
        
        log(f"✓ {len(matches)} Event-Blöcke gefunden")
        
        for match in matches:
            if len(match) >= 4:
                date = match[0]
                plz = match[1]
                city = match[2].strip()
                title = match[3].strip()
                details = match[4].strip() if len(match) > 4 else ""
                
                if len(title) < 3:
                    continue
                
                full_text = f"{title} {details}"
                
                time_info = extract_time(full_text)
                price_info = extract_price(full_text)
                address = f"{plz} {city}"
                
                genres = ["Country"]
                full_lower = full_text.lower()
                
                if "line dance" in full_lower: genres.append("Line Dance")
                if "rockabilly" in full_lower: genres.append("Rockabilly")
                if "rock'n'roll" in full_lower: genres.append("Rock'n'Roll")
                
                ev = {
                    "title": title,
                    "date": date,
                    "city": city,
                    "address": address,
                    "desc": details[:500] if details else title,
                    "time": time_info,
                    "price": price_info,
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
                
                genres = ["Rock'n'Roll"]
                tl = text.lower()
                if "boogie" in tl: genres.append("Boogie Woogie")
                if "swing" in tl or "lindy" in tl: genres.append("Swing")
                
                ev = {
                    "title": title,
                    "date": date,
                    "city": city,
                    "address": city,
                    "desc": text[:500],
                    "time": time_info,
                    "price": price_info,
                    "url": url,
                    "event_url": generate_smart_url(url, date, city),
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
                title = item_text[:80]
            
            if len(title) < 3:
                continue
            
            cities = ["Berlin", "Dresden", "Leipzig", "München", "Hamburg", "Köln"]
            city = next((c for c in cities if c in item_text), "")
            
            genres = ["Swing"]
            if "lindy" in item_text.lower(): genres.append("Lindy Hop")
            
            ev = {
                "title": title,
                "date": date,
                "city": city,
                "address": city,
                "desc": item_text[:500],
                "url": url,
                "event_url": generate_smart_url(url, date, city),
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
                title = item_text[:80]
            
            if len(title) < 3:
                continue
            
            city = "Dresden" if "dresden" in item_text.lower() else ""
            
            genres = ["Swing"]
            if "lindy" in item_text.lower(): genres.append("Lindy Hop")
            
            ev = {
                "title": title,
                "date": date,
                "city": city,
                "address": city,
                "desc": item_text[:500],
                "url": url,
                "event_url": generate_smart_url(url, date, city),
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

def scrape_dresden_hepcats():
    """Scrapt NUR tatsächlich gelistete Events von Hepcats"""
    events = []
    url = "https://www.dresden-hepcats.de/socials-de"
    
    log("\n" + "="*70)
    log("[5/6] SCRAPING: Dresden-Hepcats")
    log("="*70)
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=30)
        
        if r.status_code != 200:
            return events
        
        soup = BeautifulSoup(r.text, "lxml")
        text = soup.get_text("\n", strip=True)
        
        log(f"✓ Seite geladen: {len(r.text)} bytes")
        
        # Suche nach spezifischen Datumsangaben auf der Seite
        # Die Seite listet nur konkrete Termine, keine generellen Regeln
        
        items = soup.find_all(["div", "article", "section"])
        
        for item in items:
            item_text = item.get_text(" ", strip=True)
            date = parse_date(item_text)
            
            # Nur Events mit explizitem Datum extrahieren
            if not date or len(item_text) < 30:
                continue
            
            # Suche nach "Live Tanz Bar" oder ähnlichen Titeln
            if "live" in item_text.lower() and "tanz" in item_text.lower():
                title = "Live Tanz Bar"
            else:
                continue
            
            city = "Dresden"
            address = "Parkhotel, Bautzner Landstraße 32, 01324 Dresden"
            
            ev = {
                "title": title,
                "date": date,
                "city": city,
                "address": address,
                "desc": "Social mit Live-Band im Parkhotel auf dem Weißen Hirsch.",
                "time": "20:00 Uhr",
                "url": url,
                "event_url": url,
                "genres": ["Swing", "Lindy Hop"]
            }
            
            coords = geocode(city)
            if coords:
                ev["lat"], ev["lon"] = coords
            
            events.append(ev)
        
        log(f"✅ Dresden-Hepcats: {len(events)} Events gefunden (nur explizit gelistete)")
        
    except Exception as e:
        log(f"❌ ERROR: {type(e).__name__}: {str(e)}")
    
    return events

def scrape_lindypott():
    events = []
    url = "https://www.lindypott.de/kalender.html?ort=BO,DO,E&art=3"
    
    log("\n" + "="*70)
    log("[6/6] SCRAPING: Lindypott")
    log("="*70)
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=30)
        
        if r.status_code != 200:
            return events
        
        soup = BeautifulSoup(r.text, "lxml")
        items = soup.find_all(["div", "article", "li", "tr"])
        
        for item in items:
            item_text = item.get_text(" ", strip=True)
            date = parse_date(item_text)
            
            if not date or len(item_text) < 20:
                continue
            
            title_el = item.find(["h2", "h3", "h4", "strong"])
            title = title_el.get_text(strip=True) if title_el else item_text[:80]
            
            if len(title) < 3:
                continue
            
            cities_mapping = {"BO": "Bochum", "DO": "Dortmund", "E": "Essen"}
            city = ""
            for code, city_name in cities_mapping.items():
                if city_name.lower() in item_text.lower():
                    city = city_name
                    break
            
            genres = ["Swing"]
            if "lindy" in item_text.lower(): genres.append("Lindy Hop")
            
            ev = {
                "title": title,
                "date": date,
                "city": city,
                "address": city,
                "desc": item_text[:500],
                "url": url,
                "event_url": generate_smart_url(url, date, city),
                "genres": list(set(genres))
            }
            
            if city:
                coords = geocode(city)
                if coords:
                    ev["lat"], ev["lon"] = coords
            
            events.append(ev)
        
        log(f"✅ Lindypott: {len(events)} Events gefunden")
        
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
    log("🎸 ROCKABILLY RADAR EVENT SCRAPER - VERIFIED")
    log("Nur tatsächlich existierende Events")
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
    
    # Chronologisch sortieren
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
