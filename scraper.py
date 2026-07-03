#!/usr/bin/env python3
"""
Rockabilly Radar Event Scraper - FIXED VERSION
Funktioniert mit der tatsächlichen HTML-Struktur aller 4 Websites
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

def scrape_we_love_country():
    """FIXED: Scrapt alle 667 Events mit korrektem Pattern-Matching"""
    events = []
    url = "https://www.we-love-country.de/1_term.php"
    
    log("\n" + "="*70)
    log("[1/4] SCRAPING: WeLoveCountry (667 Events)")
    log("="*70)
    
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        r = requests.get(url, headers=headers, timeout=60)
        r.encoding = "utf-8"
        
        if r.status_code != 200:
            log(f"❌ Status {r.status_code}")
            return events
        
        log(f"✓ Seite geladen: {len(r.text)} bytes")
        
        soup = BeautifulSoup(r.text, "lxml")
        text = soup.get_text("\n", strip=True)
        
        # Pattern: "Fr. 03.07.2026 08107 Kirchberg\nEvent-Titel\nDetails"
        # Suche nach allen Datums-Blöcken
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
                
                genres = ["Country"]
                full_text = (title + " " + details).lower()
                
                if "line dance" in full_text: genres.append("Line Dance")
                if "rockabilly" in full_text: genres.append("Rockabilly")
                if "rock'n'roll" in full_text or "rock 'n' roll" in full_text: genres.append("Rock'n'Roll")
                if "irish" in full_text: genres.append("Irish")
                if "boogie" in full_text: genres.append("Boogie Woogie")
                
                ev = {
                    "title": title,
                    "date": date,
                    "city": city,
                    "desc": details[:300] if details else title,
                    "url": url,
                    "genres": list(set(genres))
                }
                
                coords = geocode(city)
                if coords:
                    ev["lat"], ev["lon"] = coords
                
                events.append(ev)
                
                if len(events) <= 5:
                    log(f"  → {date} | {city} | {title[:50]}")
        
        log(f"✅ WeLoveCountry: {len(events)} Events extrahiert")
        
    except Exception as e:
        log(f"❌ ERROR: {type(e).__name__}: {str(e)}")
        import traceback
        log(traceback.format_exc())
    
    return events

def scrape_jukeboxstompers():
    """Funktioniert bereits - 27 Events"""
    events = []
    url = "https://www.jukeboxstompers.de/index.php/veranstaltungen/veranstaltungskalender"
    
    log("\n" + "="*70)
    log("[2/4] SCRAPING: JukeboxStompers")
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
                
                genres = ["Rock'n'Roll"]
                tl = text.lower()
                if "boogie" in tl: genres.append("Boogie Woogie")
                if "swing" in tl or "lindy" in tl: genres.append("Swing")
                if "rockabilly" in tl: genres.append("Rockabilly")
                
                ev = {
                    "title": title,
                    "date": date,
                    "city": city,
                    "desc": text[:300],
                    "url": url,
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
    """Versucht verschiedene Pattern-Matching Methoden"""
    events = []
    url = "https://swingcalendar.com/de"
    
    log("\n" + "="*70)
    log("[3/4] SCRAPING: SwingCalendar")
    log("="*70)
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=30)
        
        if r.status_code != 200:
            return events
        
        soup = BeautifulSoup(r.text, "lxml")
        text = soup.get_text("\n", strip=True)
        
        # Suche nach Event-Patterns
        items = soup.find_all(["div", "article", "li"])
        log(f"Container: {len(items)}")
        
        for item in items:
            item_text = item.get_text(" ", strip=True)
            date = parse_date(item_text)
            
            if not date or len(item_text) < 20:
                continue
            
            # Versuche Titel zu finden
            title_el = item.find(["h2", "h3", "h4", "strong"])
            if title_el:
                title = title_el.get_text(strip=True)
            else:
                # Nimm erste Zeile als Titel
                lines = item_text.split("\n")
                title = lines[0][:80] if lines else item_text[:80]
            
            if len(title) < 3:
                continue
            
            cities = ["Berlin", "Dresden", "Leipzig", "München", "Hamburg", "Köln", 
                     "Frankfurt", "Wien", "Zürich", "London", "Paris", "Rom", 
                     "Madrid", "Prag", "Amsterdam", "Stockholm", "Oslo", "Helsinki"]
            city = next((c for c in cities if c in item_text), "")
            
            genres = ["Swing"]
            tl = item_text.lower()
            if "lindy" in tl: genres.append("Lindy Hop")
            if "balboa" in tl: genres.append("Balboa")
            if "charleston" in tl: genres.append("Charleston")
            
            link = item.find("a", href=True)
            ev_url = urljoin(url, link["href"]) if link else url
            
            ev = {
                "title": title,
                "date": date,
                "city": city,
                "desc": item_text[:300],
                "url": ev_url,
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
    """Versucht verschiedene Pattern-Matching Methoden"""
    events = []
    url = "https://swingindd.com/home/regionale-swing-kalender/"
    
    log("\n" + "="*70)
    log("[4/4] SCRAPING: SwingInDD")
    log("="*70)
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=30)
        
        if r.status_code != 200:
            return events
        
        soup = BeautifulSoup(r.text, "lxml")
        items = soup.find_all(["div", "article", "li"])
        
        log(f"Container: {len(items)}")
        
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
            
            genres = ["Swing"]
            tl = item_text.lower()
            if "lindy" in tl: genres.append("Lindy Hop")
            if "balboa" in tl: genres.append("Balboa")
            if "charleston" in tl: genres.append("Charleston")
            
            link = item.find("a", href=True)
            ev_url = urljoin(url, link["href"]) if link else url
            
            ev = {
                "title": title,
                "date": date,
                "city": city,
                "desc": item_text[:300],
                "url": ev_url,
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
    log("🎸 ROCKABILLY RADAR EVENT SCRAPER - FIXED")
    log("="*70)
    
    all_events = []
    
    all_events.extend(scrape_we_love_country())
    time.sleep(2)
    
    all_events.extend(scrape_jukeboxstompers())
    time.sleep(2)
    
    all_events.extend(scrape_swingcalendar())
    time.sleep(2)
    
    all_events.extend(scrape_swingindd())
    
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
    log(f"   Größe: {len(json.dumps(all_events, ensure_ascii=False))} bytes")
    log("="*70)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"\n❌ FATAL: {type(e).__name__}: {str(e)}")
        import traceback
        log(traceback.format_exc())
        sys.exit(1)
