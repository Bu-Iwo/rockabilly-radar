#!/usr/bin/env python3
"""
Rockabilly Radar Event Scraper - FINAL VERSION
Scrapt ALLE Events von 4 Quellen mit vollständiger Pagination
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse, parse_qs

GEOCODE_CACHE = {}

def geocode(city):
    """Konvertiert Stadtnamen zu Koordinaten"""
    if not city or city in GEOCODE_CACHE:
        return GEOCODE_CACHE.get(city)
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": city, "format": "json", "limit": 1},
            headers={"User-Agent": "RockabillyRadar/1.0 (Event Scraper)"},
            timeout=10
        )
        data = r.json()
        if data:
            coords = (float(data[0]["lat"]), float(data[0]["lon"]))
            GEOCODE_CACHE[city] = coords
            time.sleep(1.1)  # Nominatim Rate Limit
            return coords
    except Exception as e:
        print(f"  ⚠ Geocode error for {city}: {e}")
    return None

def parse_date(text):
    """Extrahiert Datum aus Text"""
    # DD.MM.YYYY
    m = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', text)
    if m:
        d, mo, y = m.groups()
        return f"{int(d):02d}.{int(mo):02d}.{y}"
    # D.M.YYYY
    m = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', text)
    if m:
        d, mo, y = m.groups()
        return f"{int(d):02d}.{int(mo):02d}.{y}"
    # DD.MM. (aktuelles Jahr)
    m = re.search(r'(\d{1,2})\.(\d{1,2})\.', text)
    if m:
        d, mo = m.groups()
        return f"{int(d):02d}.{int(mo):02d}.{datetime.now().year}"
    return None

def parse_date_for_sort(date_str):
    """Parst Datum für Sortierung"""
    try:
        # Extrahiere erstes Datum aus "DD.MM. - DD.MM.YYYY"
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
    """Scrapt ALLE 670+ Events von we-love-country.de mit Pagination"""
    events = []
    base_url = "https://www.we-love-country.de"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    print("\n[WeLoveCountry] Starte Scraping...")
    
    # Versuche verschiedene Pagination-Formate
    page_urls = []
    
    # Methode 1: Prüfe ob es page-Parameter gibt
    test_url = f"{base_url}/1_term.php?page=2"
    try:
        r = requests.get(test_url, headers=headers, timeout=30)
        if r.status_code == 200 and len(r.text) > 1000:
            # Pagination existiert! Finde alle Seiten
            print("  ✓ Pagination gefunden")
            page_num = 1
            while page_num <= 100:  # Max 100 Seiten
                url = f"{base_url}/1_term.php?page={page_num}" if page_num > 1 else f"{base_url}/1_term.php"
                page_urls.append(url)
                
                # Prüfe ob nächste Seite existiert
                r = requests.get(url, headers=headers, timeout=30)
                soup = BeautifulSoup(r.content, "lxml")
                
                # Suche nach "Weiter" oder nächster Seite
                next_link = soup.find("a", href=re.compile(rf"page={page_num+1}"))
                if not next_link:
                    # Alternative: Prüfe ob Seite noch Events hat
                    if len(soup.find_all("tr")) < 5:
                        break
                
                page_num += 1
                time.sleep(1)
        else:
            # Keine Pagination, nur eine Seite
            page_urls = [f"{base_url}/1_term.php"]
    except:
        page_urls = [f"{base_url}/1_term.php"]
    
    print(f"  → {len(page_urls)} Seiten zu scrapen")
    
    # Jetzt alle Seiten scrapen
    for page_url in page_urls:
        try:
            r = requests.get(page_url, headers=headers, timeout=30)
            r.encoding = "utf-8"
            soup = BeautifulSoup(r.content, "lxml")
            
            current_date = None
            all_tables = soup.find_all("table")
            
            for table in all_tables:
                text = table.get_text(" ", strip=True)
                
                # Datums-Header erkennen
                date_match = re.search(r'(Mo|Di|Mi|Do|Fr|Sa|So)\.\s+(\d{2}\.\d{2}\.\d{4})', text)
                if date_match and len(table.find_all("tr")) <= 3:
                    current_date = date_match.group(2)
                    continue
                
                if not current_date:
                    continue
                
                # Events aus Tabelle extrahieren
                rows = table.find_all("tr")
                for row in rows:
                    cells = row.find_all("td")
                    if not cells:
                        continue
                    
                    row_text = row.get_text(" ", strip=True)
                    
                    # Verschiedene Formate erkennen
                    # Format 1: "80995 München, Event-Titel"
                    plz_match = re.search(r'(\d{5})\s+([^,]+),\s*(.+)', row_text)
                    if plz_match:
                        plz, city, title = plz_match.groups()
                        
                        # Details aus nächster Zeile holen
                        details = ""
                        next_row = row.find_next_sibling("tr")
                        if next_row:
                            details = next_row.get_text(" ", strip=True)
                        
                        genres = ["Country"]
                        full_text = (title + " " + details).lower()
                        
                        if "line dance" in full_text: genres.append("Line Dance")
                        if "rockabilly" in full_text: genres.append("Rockabilly")
                        if "rock'n'roll" in full_text: genres.append("Rock'n'Roll")
                        if "irish" in full_text: genres.append("Irish")
                        if "boogie" in full_text: genres.append("Boogie Woogie")
                        
                        ev = {
                            "title": title.strip(),
                            "date": current_date,
                            "city": city.strip(),
                            "desc": details[:300] if details else title,
                            "url": page_url,
                            "genres": list(set(genres))
                        }
                        
                        coords = geocode(city.strip())
                        if coords:
                            ev["lat"], ev["lon"] = coords
                        
                        events.append(ev)
                    
                    # Format 2: Einfache Zeile mit Titel und Ort
                    elif len(cells) >= 2:
                        title = cells[0].get_text(strip=True)
                        if len(title) < 3:
                            continue
                        
                        city_match = re.search(r'(?:in|@|,)\s*([A-ZÄÖÜ][a-zäöüß\-]+)', row_text)
                        city = city_match.group(1) if city_match else ""
                        
                        genres = ["Country"]
                        if "line dance" in row_text.lower(): genres.append("Line Dance")
                        
                        ev = {
                            "title": title,
                            "date": current_date,
                            "city": city,
                            "desc": row_text[:300],
                            "url": page_url,
                            "genres": list(set(genres))
                        }
                        
                        if city:
                            coords = geocode(city)
                            if coords:
                                ev["lat"], ev["lon"] = coords
                        
                        events.append(ev)
            
            print(f"  ✓ Seite {page_urls.index(page_url)+1}/{len(page_urls)}: {len(events)} Events total")
            time.sleep(1)
            
        except Exception as e:
            print(f"  ✗ Fehler bei {page_url}: {e}")
    
    print(f"\n✓ WeLoveCountry: {len(events)} Events gefunden")
    return events

def scrape_jukeboxstompers():
    """Scrapt Events von jukeboxstompers.de"""
    events = []
    url = "https://www.jukeboxstompers.de/index.php/veranstaltungen/veranstaltungskalender"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    print("\n[JukeboxStompers] Starte Scraping...")
    
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.content, "lxml")
        
        # Alle Tabellen durchsuchen
        tables = soup.find_all("table")
        
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
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
        
        print(f"✓ JukeboxStompers: {len(events)} Events gefunden")
        
    except Exception as e:
        print(f"✗ JukeboxStompers error: {e}")
    
    return events

def scrape_swingcalendar():
    """Scrapt Events von swingcalendar.com"""
    events = []
    url = "https://swingcalendar.com/de"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    print("\n[SwingCalendar] Starte Scraping...")
    
    try:
        r = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(r.content, "lxml")
        
        items = soup.find_all(["article", "div"], class_=re.compile(r'event|calendar|item'))
        if not items:
            items = soup.find_all(["div", "article"])
        
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
        
        print(f"✓ SwingCalendar: {len(events)} Events gefunden")
        
    except Exception as e:
        print(f"✗ SwingCalendar error: {e}")
    
    return events

def scrape_swingindd():
    """Scrapt Events von swingindd.com"""
    events = []
    url = "https://swingindd.com/home/regionale-swing-kalender/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    print("\n[SwingInDD] Starte Scraping...")
    
    try:
        r = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(r.content, "lxml")
        
        items = soup.find_all(["div", "article", "li"])
        
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
        
        print(f"✓ SwingInDD: {len(events)} Events gefunden")
        
    except Exception as e:
        print(f"✗ SwingInDD error: {e}")
    
    return events

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

def sort_by_date(events):
    """Sortiert Events chronologisch nach Datum"""
    return sorted(events, key=lambda e: parse_date_for_sort(e['date']))

def main():
    print("=" * 70)
    print("Rockabilly Radar Event Scraper - FINAL VERSION")
    print("Scrapt ALLE Events mit vollständiger Pagination")
    print("=" * 70)
    
    all_events = []
    
    # Alle Quellen scrapen
    all_events.extend(scrape_we_love_country())
    time.sleep(2)
    
    all_events.extend(scrape_jukeboxstompers())
    time.sleep(2)
    
    all_events.extend(scrape_swingcalendar())
    time.sleep(2)
    
    all_events.extend(scrape_swingindd())
    
    # Duplikate entfernen
    print(f"\n{'=' * 70}")
    print(f"Total Events vor Deduplikation: {len(all_events)}")
    all_events = deduplicate(all_events)
    print(f"Total Events nach Deduplikation: {len(all_events)}")
    
    # Nach Datum sortieren
    all_events = sort_by_date(all_events)
    print(f"✓ Events chronologisch sortiert")
    
    # Speichern
    with open("events.json", "w", encoding="utf-8") as f:
        json.dump(all_events, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Gespeichert in events.json ({len(all_events)} Events)")
    print("=" * 70)

if __name__ == "__main__":
    main()
