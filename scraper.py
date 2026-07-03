#!/usr/bin/env python3
"""
Rockabilly Radar Event Scraper - DIAGNOSTIC VERSION
Mit vollständiger Fehlerdiagnose und Fallback-Daten
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
ALL_EVENTS = []

def log(msg):
    """Logging mit Flush für GitHub Actions"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def geocode(city):
    """Konvertiert Stadtnamen zu Koordinaten"""
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
        log(f"  ⚠ Geocode error for {city}: {e}")
    return None

def parse_date(text):
    """Extrahiert Datum aus Text"""
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

def scrape_we_love_country():
    """Scrapt WeLoveCountry mit robuster Fehlerbehandlung"""
    events = []
    url = "https://www.we-love-country.de/1_term.php"
    
    log("\n" + "="*70)
    log("[1/4] SCRAPING: WeLoveCountry")
    log("="*70)
    log(f"URL: {url}")
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        r = requests.get(url, headers=headers, timeout=30)
        log(f"Status Code: {r.status_code}")
        log(f"Content Length: {len(r.text)} bytes")
        
        if r.status_code != 200:
            log("❌ ERROR: Non-200 status code")
            return events
        
        soup = BeautifulSoup(r.text, "lxml")
        
        # Diagnostik: Was finden wir?
        tables = soup.find_all("table")
        log(f"Tabellen gefunden: {len(tables)}")
        
        trs = soup.find_all("tr")
        log(f"Tabellen-Reihen (tr): {len(trs)}")
        
        # Suche nach Datums-Patterns
        date_matches = re.findall(r'\d{2}\.\d{2}\.\d{4}', r.text)
        log(f"Daten (DD.MM.YYYY) im HTML: {len(date_matches)}")
        if date_matches:
            log(f"Beispiel-Daten: {date_matches[:5]}")
        
        # Versuche verschiedene Extraktions-Methoden
        current_date = None
        events_found = 0
        
        for table in tables:
            table_text = table.get_text(" ", strip=True)
            
            # Methode 1: Datums-Header
            date_match = re.search(r'(Mo|Di|Mi|Do|Fr|Sa|So)\.?\s+(\d{2}\.\d{2}\.\d{4})', table_text)
            if date_match and len(table.find_all("tr")) <= 3:
                current_date = date_match.group(2)
                log(f"  → Datums-Header: {current_date}")
                continue
            
            if not current_date:
                continue
            
            # Methode 2: Durchsuche alle Zeilen
            for row in table.find_all("tr"):
                cells = row.find_all("td")
                if not cells or len(cells) == 0:
                    continue
                
                row_text = row.get_text(" ", strip=True)
                
                # Versuche PLZ + Stadt + Titel Pattern
                plz_match = re.search(r'(\d{5})\s+([^,]+),\s*(.+)', row_text)
                if plz_match:
                    plz, city, title = plz_match.groups()
                    
                    events_found += 1
                    if events_found <= 3:
                        log(f"  ✓ Event gefunden: {title[:50]}... in {city}")
                    
                    genres = ["Country"]
                    if "line dance" in row_text.lower():
                        genres.append("Line Dance")
                    if "rockabilly" in row_text.lower():
                        genres.append("Rockabilly")
                    
                    ev = {
                        "title": title.strip(),
                        "date": current_date,
                        "city": city.strip(),
                        "desc": row_text[:300],
                        "url": url,
                        "genres": list(set(genres))
                    }
                    
                    coords = geocode(city.strip())
                    if coords:
                        ev["lat"], ev["lon"] = coords
                    
                    events.append(ev)
        
        log(f"✅ WeLoveCountry: {len(events)} Events extrahiert")
        
        if len(events) == 0:
            log("⚠ WARNING: Keine Events gefunden! HTML-Struktur könnte sich geändert haben.")
            # Zeige Beispiel-HTML für Debugging
            sample = soup.get_text(" ", strip=True)[:500]
            log(f"HTML-Beispiel: {sample}")
        
    except Exception as e:
        log(f"❌ EXCEPTION: {type(e).__name__}: {str(e)}")
        import traceback
        log(traceback.format_exc())
    
    return events

def scrape_jukeboxstompers():
    """Scrapt JukeboxStompers"""
    events = []
    url = "https://www.jukeboxstompers.de/index.php/veranstaltungen/veranstaltungskalender"
    
    log("\n" + "="*70)
    log("[2/4] SCRAPING: JukeboxStompers")
    log("="*70)
    log(f"URL: {url}")
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=30)
        log(f"Status Code: {r.status_code}")
        
        if r.status_code != 200:
            log("❌ ERROR: Non-200 status code")
            return events
        
        soup = BeautifulSoup(r.text, "lxml")
        
        tables = soup.find_all("table")
        log(f"Tabellen gefunden: {len(tables)}")
        
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
        log(f"❌ EXCEPTION: {type(e).__name__}: {str(e)}")
    
    return events

def scrape_swingcalendar():
    """Scrapt SwingCalendar"""
    events = []
    url = "https://swingcalendar.com/de"
    
    log("\n" + "="*70)
    log("[3/4] SCRAPING: SwingCalendar")
    log("="*70)
    log(f"URL: {url}")
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=30)
        log(f"Status Code: {r.status_code}")
        
        if r.status_code != 200:
            log("❌ ERROR: Non-200 status code")
            return events
        
        soup = BeautifulSoup(r.text, "lxml")
        
        items = soup.find_all(["article", "div"], class_=re.compile(r'event|calendar|item'))
        if not items:
            items = soup.find_all(["div", "article"])
        
        log(f"Container gefunden: {len(items)}")
        
        for item in items:
            title_el = item.find(["h2", "h3", "h4"])
            if not title_el:
                continue
            
            title = title_el.get_text(strip=True)
            if len(title) < 3:
                continue
            
            text = item.get_text(" ", strip=True)
            date = parse_date(text)
            if not date:
                continue
            
            cities = ["Berlin", "Dresden", "Leipzig", "München", "Hamburg", "Köln", 
                     "Frankfurt", "Wien", "Zürich", "London", "Paris", "Rom", 
                     "Madrid", "Prag", "Amsterdam", "Stockholm", "Oslo", "Helsinki"]
            city = next((c for c in cities if c in text), "")
            
            genres = ["Swing"]
            tl = (title + " " + text).lower()
            if "lindy" in tl: genres.append("Lindy Hop")
            if "balboa" in tl: genres.append("Balboa")
            if "charleston" in tl: genres.append("Charleston")
            
            link = item.find("a", href=True)
            ev_url = urljoin(url, link["href"]) if link else url
            
            ev = {
                "title": title,
                "date": date,
                "city": city,
                "desc": text[:300],
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
        log(f"❌ EXCEPTION: {type(e).__name__}: {str(e)}")
    
    return events

def scrape_swingindd():
    """Scrapt SwingInDD"""
    events = []
    url = "https://swingindd.com/home/regionale-swing-kalender/"
    
    log("\n" + "="*70)
    log("[4/4] SCRAPING: SwingInDD")
    log("="*70)
    log(f"URL: {url}")
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=30)
        log(f"Status Code: {r.status_code}")
        
        if r.status_code != 200:
            log("❌ ERROR: Non-200 status code")
            return events
        
        soup = BeautifulSoup(r.text, "lxml")
        
        items = soup.find_all(["div", "article", "li"])
        log(f"Container gefunden: {len(items)}")
        
        for item in items:
            text = item.get_text(" ", strip=True)
            date = parse_date(text)
            if not date:
                continue
            
            title_el = item.find(["h2", "h3", "h4", "strong"])
            title = title_el.get_text(strip=True) if title_el else text[:80]
            
            if len(title) < 3:
                continue
            
            city = "Dresden" if "dresden" in text.lower() else ""
            
            genres = ["Swing"]
            tl = text.lower()
            if "lindy" in tl: genres.append("Lindy Hop")
            if "balboa" in tl: genres.append("Balboa")
            if "charleston" in tl: genres.append("Charleston")
            
            link = item.find("a", href=True)
            ev_url = urljoin(url, link["href"]) if link else url
            
            ev = {
                "title": title,
                "date": date,
                "city": city,
                "desc": text[:300],
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
        log(f"❌ EXCEPTION: {type(e).__name__}: {str(e)}")
    
    return events

def get_fallback_events():
    """Fallback Events falls Scraping fehlschlägt"""
    log("\n⚠ Verwende Fallback-Events (manuell gepflegt)")
    return [
        {"title":"Summer Jamboree 2026","date":"01.08. - 09.08.2026","city":"Senigallia","lat":43.7147,"lon":13.2183,"desc":"Europas größtes Rockabilly-Festival","url":"https://www.summerjamboree.com","genres":["Rockabilly"]},
        {"title":"Firebirds Festival #14","date":"03.07. - 05.07.2026","city":"Grimma","lat":51.2294,"lon":12.7561,"desc":"Rock'n'Roll im Kloster Nimbschen","url":"https://www.jukeboxstompers.de/","genres":["Rock'n'Roll","Boogie Woogie","Lindy Hop"]},
        {"title":"High Rockabilly 2026","date":"15.05. - 17.05.2026","city":"Irun","lat":43.3396,"lon":-1.7894,"desc":"Top Rockabilly Festival Spanien","url":"https://www.highrockabilly.com","genres":["Rockabilly"]},
        {"title":"Viva Las Vegas 2026","date":"16.04. - 19.04.2026","city":"Las Vegas","lat":36.1699,"lon":-115.1398,"desc":"Weltgrößtes Rockabilly Festival","url":"https://www.vivalasvegas.net","genres":["Rockabilly","50er"]},
        {"title":"Rock That Swing #20","date":"04.02. - 08.02.2027","city":"München","lat":48.1351,"lon":11.5820,"desc":"20. Rock That Swing Festival","url":"https://www.jukeboxstompers.de/","genres":["Lindy Hop","Boogie Woogie","Balboa","Shag"]},
        {"title":"Boogie Feets Festival 2026","date":"23.07. - 27.07.2026","city":"Oslo","lat":59.9139,"lon":10.7522,"desc":"Internationales Boogie Woogie Weekend","url":"https://www.jukeboxstompers.de/","genres":["Boogie Woogie"]},
        {"title":"Herräng Dance Camp","date":"04.07. - 11.07.2026","city":"Herräng","lat":59.8500,"lon":16.9000,"desc":"Legendäres Swing Dance Camp Schweden","url":"https://swingcalendar.com/de","genres":["Lindy Hop","Swing","Balboa"]}
    ]

def deduplicate(events):
    """Entfernt Duplikate"""
    seen = set()
    unique = []
    for ev in events:
        key = f"{ev['title']}_{ev['date']}_{ev.get('city', '')}"
        if key not in seen:
            seen.add(key)
            unique.append(ev)
    return unique

def parse_date_for_sort(date_str):
    """Parst Datum für Sortierung"""
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

def main():
    log("="*70)
    log("🎸 ROCKABILLY RADAR EVENT SCRAPER")
    log("="*70)
    
    all_events = []
    
    # Scrape alle Quellen
    all_events.extend(scrape_we_love_country())
    time.sleep(2)
    
    all_events.extend(scrape_jukeboxstompers())
    time.sleep(2)
    
    all_events.extend(scrape_swingcalendar())
    time.sleep(2)
    
    all_events.extend(scrape_swingindd())
    
    # Zusammenfassung
    log("\n" + "="*70)
    log("ZUSAMMENFASSUNG")
    log("="*70)
    log(f"Total Events vor Deduplikation: {len(all_events)}")
    
    all_events = deduplicate(all_events)
    log(f"Total Events nach Deduplikation: {len(all_events)}")
    
    # Fallback wenn zu wenige Events
    if len(all_events) < 10:
        log("⚠ WARNING: Nur wenige Events gefunden! Verwende Fallback-Daten...")
        fallback = get_fallback_events()
        all_events = deduplicate(all_events + fallback)
        log(f"Total Events mit Fallback: {len(all_events)}")
    
    # Sortieren
    all_events = sorted(all_events, key=lambda e: parse_date_for_sort(e['date']))
    log("✓ Events chronologisch sortiert")
    
    # Speichern
    output_file = "events.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_events, f, ensure_ascii=False, indent=2)
    
    log(f"\n✅ GESPEICHERT: {output_file}")
    log(f"   Anzahl Events: {len(all_events)}")
    log(f"   Dateigröße: {len(json.dumps(all_events, ensure_ascii=False))} bytes")
    log("="*70)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"\n❌ FATAL ERROR: {type(e).__name__}: {str(e)}")
        import traceback
        log(traceback.format_exc())
        sys.exit(1)
