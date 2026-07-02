#!/usr/bin/env python3
"""
Rockabilly Radar Event Scraper v2.0
Scrapt ALLE Events von 4 Quellen mit Pagination:
- we-love-country.de (670+ Events)
- swingcalendar.com/de (234+ Events)
- swingindd.com (140+ Events)
- jukeboxstompers.de (25+ Events)
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
    """Geocoding mit Cache und Rate-Limiting"""
    if not city or city in GEOCODE_CACHE:
        return GEOCODE_CACHE.get(city)
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": city, "format": "json", "limit": 1},
            headers={"User-Agent": "RockabillyRadar/1.0 (Event Aggregator)"},
            timeout=10
        )
        data = r.json()
        if data:
            coords = (float(data[0]["lat"]), float(data[0]["lon"]))
            GEOCODE_CACHE[city] = coords
            time.sleep(1.1)  # Nominatim Rate Limit: 1 req/sec
            return coords
    except Exception as e:
        print(f"[GEO] Error for '{city}': {e}")
    return None

def parse_date(text):
    """Extrahiert Datum aus beliebigem Text"""
    patterns = [
        r'(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})',  # DD. MM. YYYY
        r'(\d{2})\.(\d{2})\.(\d{4})',             # DD.MM.YYYY
        r'(\d{1,2})\.(\d{1,2})\.(\d{2})',         # DD.MM.YY
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            groups = m.groups()
            if len(groups) == 3:
                d, mo, y = groups
                y = y if len(y) == 4 else f"20{y}"
                return f"{int(d):02d}.{int(mo):02d}.{y}"
    # Fallback: DD.MM. (aktuelles Jahr)
    m = re.search(r'(\d{1,2})\.(\d{1,2})\.', text)
    if m:
        d, mo = m.groups()
        return f"{int(d):02d}.{int(mo):02d}.{datetime.now().year}"
    return None

def extract_city(text):
    """Versucht, einen Stadtnamen aus dem Text zu extrahieren"""
    # Bekannte Städte priorisieren
    known_cities = [
        "Berlin","Dresden","Leipzig","München","Hamburg","Köln","Frankfurt","Stuttgart",
        "Wien","Zürich","London","Paris","Rom","Madrid","Prag","Amsterdam","Brüssel",
        "Stockholm","Oslo","Helsinki","Kopenhagen","Warschau","Budapest","Lissabon",
        "Senigallia","Grimma","Irun","Las Vegas","Oslo","Leipzig","Magdeburg",
        "Burgstädt","Ganderkesee","Königsleitn","Markkleeberg","Zürich","Great Yarmouth",
        "Wolfenbüttel","Haimhausen","Bad Blumau","Rain","Hohenkirchen","De Rijp",
        "Landsberg am Lech","Wolframs-Eschenbach","Zwönitz","Triest","Trient",
        "Fenestrelle","Perugia","Kåstrup","Herräng","Wuppertal","Sapporo","Eging am See",
        "Mannheim","Vohburg","Pullman City","Mühlhausen","St. Florian","Bad Lauterberg",
        "Melle","Oberursel","Erbach","Lemberg","Hüttlingen","Olching","Böhmenkirch",
        "Schönsee","Riedenburg","Hofheim","Geldersheim","Sand am Main","Schönwölkau",
        "Neuendorf","Düren","Limburg","Krölpa","Chemnitz","Hasselfelde","Rödermark",
        "Winkelhaid","Neustadt","Sondershausen","Ranstatt","Buchholz","Pohlheim",
        "Erftstadt","Bissingen","Mücke","Lauf","Apolda","Pretzfeld","Wernigerode",
        "Untermeitingen","Kirchberg","Am Mellensee","Künzell","Friedrichsdorf","Herrenberg",
        "Volkertshausen","Nürnberg","Pegnitz","Schmalkalden","Zwickau","Affing","Burgau"
    ]
    for city in known_cities:
        if city.lower() in text.lower():
            # Finde die korrekte Schreibweise
            m = re.search(rf'({re.escape(city)})', text, re.I)
            if m:
                return m.group(1)
    # Fallback: Regex für deutsche Städtenamen
    m = re.search(r'(?:in|@|bei|nahe)\s+([A-ZÄÖÜ][a-zäöüß\-]+(?:\s+[A-ZÄÖÜ][a-zäöüß\-]+)*)', text)
    if m:
        return m.group(1)
    return ""

# ============================================================================
# SCRAPER: we-love-country.de (mit Pagination!)
# ============================================================================
def scrape_we_love_country():
    """Scrapt ALLE Seiten von we-love-country.de"""
    events = []
    base_url = "https://www.we-love-country.de"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    page = 1
    max_pages = 100  # Sicherheitslimit
    
    while page <= max_pages:
        url = f"{base_url}/1_term.php" if page == 1 else f"{base_url}/1_term.php?page={page}"
        print(f"[WLC] Scraping page {page}: {url}")
        
        try:
            r = requests.get(url, headers=headers, timeout=30)
            r.encoding = "utf-8"
            
            if r.status_code != 200 or len(r.text.strip()) < 1000:
                print(f"[WLC] No more content at page {page}")
                break
                
            soup = BeautifulSoup(r.content, "lxml")
            rows = soup.find_all("tr")
            
            page_count = 0
            for row in rows:
                text = row.get_text(" ", strip=True)
                if not text or len(text) < 10:
                    continue
                    
                date = parse_date(text)
                if not date:
                    continue
                    
                # Titel extrahieren
                title_el = row.find(["strong", "b", "a"])
                title = title_el.get_text(strip=True) if title_el else text[:100]
                if len(title.strip()) < 3:
                    continue
                    
                city = extract_city(text)
                
                # URL extrahieren
                link = row.find("a", href=True)
                ev_url = urljoin(base_url, link["href"]) if link else f"{base_url}/1_term.php"
                
                # Genres bestimmen
                genres = ["Country"]
                tl = text.lower()
                if "line dance" in tl: genres.append("Line Dance")
                if "rockabilly" in tl: genres.append("Rockabilly")
                if "rock'n'roll" in tl or "rock 'n' roll" in tl: genres.append("Rock'n'Roll")
                if "irish" in tl or "scottish" in tl: genres.append("Irish")
                
                ev = {
                    "title": title.strip(),
                    "date": date,
                    "city": city,
                    "desc": text[:300].strip(),
                    "url": ev_url,
                    "genres": list(set(genres))
                }
                
                # Geocoding
                if city:
                    coords = geocode(city)
                    if coords:
                        ev["lat"], ev["lon"] = coords
                
                events.append(ev)
                page_count += 1
            
            print(f"[WLC] Page {page}: {page_count} new events (total: {len(events)})")
            
            if page_count == 0:
                print("[WLC] No events found, stopping")
                break
            
            # Nächste Seite finden
            next_found = False
            for link in soup.find_all("a", href=True):
                href = link["href"]
                if f"page={page+1}" in href or (page == 1 and "page=2" in href):
                    next_found = True
                    break
            
            if not next_found:
                # Alternative: prüfe Text-Links wie "Weiter", ">>", "Next"
                if not soup.find(string=re.compile(r"Weiter|Nächste|Next|>>|›", re.I)):
                    print("[WLC] No next page link found")
                    break
            
            page += 1
            time.sleep(2)  # Höflichkeit
            
        except requests.exceptions.RequestException as e:
            print(f"[WLC] Request error page {page}: {e}")
            break
        except Exception as e:
            print(f"[WLC] Parse error page {page}: {e}")
            break
    
    print(f"[WLC] DONE: {len(events)} events from {page} pages")
    return events

# ============================================================================
# SCRAPER: swingcalendar.com/de (mit Pagination!)
# ============================================================================
def scrape_swingcalendar():
    """Scrapt ALLE Seiten von swingcalendar.com/de"""
    events = []
    base_url = "https://swingcalendar.com"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    page = 1
    max_pages = 50
    
    while page <= max_pages:
        url = f"{base_url}/de" if page == 1 else f"{base_url}/de?page={page}"
        print(f"[SC] Scraping page {page}: {url}")
        
        try:
            r = requests.get(url, headers=headers, timeout=30)
            if r.status_code != 200:
                break
                
            soup = BeautifulSoup(r.content, "lxml")
            items = soup.select("article, div.event, div.item, li.event, .calendar-item")
            if not items:
                items = soup.find_all(["div", "article"], class_=re.compile(r"event|item|calendar", re.I))
            
            page_count = 0
            for item in items:
                title_el = item.find(["h2", "h3", "h4", "h5"])
                if not title_el:
                    continue
                title = title_el.get_text(strip=True)
                if len(title) < 3:
                    continue
                    
                text = item.get_text(" ", strip=True)
                date = parse_date(text)
                if not date:
                    continue
                    
                city = extract_city(text)
                
                link = item.find("a", href=True)
                ev_url = urljoin(base_url, link["href"]) if link else f"{base_url}/de"
                
                genres = ["Swing"]
                tl = (title + " " + text).lower()
                if "lindy" in tl: genres.append("Lindy Hop")
                if "balboa" in tl: genres.append("Balboa")
                if "charleston" in tl: genres.append("Charleston")
                if "blues" in tl: genres.append("Blues")
                if "shag" in tl: genres.append("Shag")
                if "west coast" in tl: genres.append("West Coast Swing")
                
                ev = {
                    "title": title.strip(),
                    "date": date,
                    "city": city,
                    "desc": text[:300].strip(),
                    "url": ev_url,
                    "genres": list(set(genres))
                }
                
                if city:
                    coords = geocode(city)
                    if coords:
                        ev["lat"], ev["lon"] = coords
                
                events.append(ev)
                page_count += 1
            
            print(f"[SC] Page {page}: {page_count} events (total: {len(events)})")
            
            if page_count == 0 and page > 1:
                break
            
            # Nächste Seite finden
            next_found = False
            for link in soup.find_all("a", href=True):
                if f"page={page+1}" in link["href"] or (page==1 and "page=2" in link["href"]):
                    next_found = True
                    break
            if not next_found:
                if not soup.find(string=re.compile(r"Weiter|Next|›|>>", re.I)):
                    break
            
            page += 1
            time.sleep(2)
            
        except Exception as e:
            print(f"[SC] Error page {page}: {e}")
            break
    
    print(f"[SC] DONE: {len(events)} events from {page} pages")
    return events

# ============================================================================
# SCRAPER: swingindd.com (mit Pagination!)
# ============================================================================
def scrape_swingindd():
    """Scrapt ALLE Seiten von swingindd.com"""
    events = []
    base_url = "https://swingindd.com"
    url = f"{base_url}/home/regionale-swing-kalender/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    page = 1
    max_pages = 30
    
    while page <= max_pages:
        page_url = url if page == 1 else f"{url}?page={page}"
        print(f"[SID] Scraping page {page}: {page_url}")
        
        try:
            r = requests.get(page_url, headers=headers, timeout=30)
            if r.status_code != 200:
                break
                
            soup = BeautifulSoup(r.content, "lxml")
            items = soup.select("article, div.event, li.event, div.entry-content, .post")
            if not items:
                items = soup.find_all(["div", "article", "li"])
            
            page_count = 0
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
                    
                # Dresden ist der Hauptort
                city = "Dresden" if "dresden" in text.lower() else extract_city(text)
                
                link = item.find("a", href=True)
                ev_url = urljoin(base_url, link["href"]) if link else url
                
                genres = ["Swing"]
                tl = (title + " " + text).lower()
                if "lindy" in tl: genres.append("Lindy Hop")
                if "balboa" in tl: genres.append("Balboa")
                if "charleston" in tl: genres.append("Charleston")
                if "shag" in tl: genres.append("Shag")
                
                ev = {
                    "title": title.strip(),
                    "date": date,
                    "city": city,
                    "desc": text[:300].strip(),
                    "url": ev_url,
                    "genres": list(set(genres))
                }
                
                if city:
                    coords = geocode(city)
                    if coords:
                        ev["lat"], ev["lon"] = coords
                
                events.append(ev)
                page_count += 1
            
            print(f"[SID] Page {page}: {page_count} events (total: {len(events)})")
            
            if page_count == 0 and page > 1:
                break
            
            # Nächste Seite
            next_found = False
            for link in soup.find_all("a", href=True):
                if f"page={page+1}" in link["href"] or (page==1 and "page=2" in link["href"]):
                    next_found = True
                    break
            if not next_found:
                if not soup.find(string=re.compile(r"Weiter|Next|›|>>", re.I)):
                    break
            
            page += 1
            time.sleep(2)
            
        except Exception as e:
            print(f"[SID] Error page {page}: {e}")
            break
    
    print(f"[SID] DONE: {len(events)} events from {page} pages")
    return events

# ============================================================================
# SCRAPER: jukeboxstompers.de (mit Pagination!)
# ============================================================================
def scrape_jukeboxstompers():
    """Scrapt ALLE Seiten von jukeboxstompers.de"""
    events = []
    base_url = "https://www.jukeboxstompers.de"
    url = f"{base_url}/index.php/veranstaltungen/veranstaltungskalender"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    page = 1
    max_pages = 20
    
    while page <= max_pages:
        page_url = url if page == 1 else f"{url}&page={page}"
        print(f"[JBS] Scraping page {page}: {page_url}")
        
        try:
            r = requests.get(page_url, headers=headers, timeout=30)
            if r.status_code != 200:
                break
                
            soup = BeautifulSoup(r.content, "lxml")
            items = soup.select("div.event, article.event, li.event, tr.event, .calendar-event")
            if not items:
                items = soup.find_all(["div", "article", "li", "tr"], class_=re.compile(r"event", re.I))
            
            page_count = 0
            for item in items:
                title_el = item.find(["h2", "h3", "h4", "strong", "b"])
                if not title_el:
                    continue
                title = title_el.get_text(strip=True)
                if len(title) < 3:
                    continue
                    
                text = item.get_text(" ", strip=True)
                date = parse_date(text)
                if not date:
                    continue
                    
                city = extract_city(text)
                
                link = item.find("a", href=True)
                ev_url = urljoin(base_url, link["href"]) if link else url
                
                genres = ["Rock'n'Roll"]
                tl = (title + " " + text).lower()
                if "boogie" in tl: genres.append("Boogie Woogie")
                if "swing" in tl or "lindy" in tl: genres.append("Swing")
                if "rockabilly" in tl: genres.append("Rockabilly")
                if "balboa" in tl: genres.append("Balboa")
                if "shag" in tl: genres.append("Shag")
                if "west coast" in tl: genres.append("West Coast Swing")
                
                ev = {
                    "title": title.strip(),
                    "date": date,
                    "city": city,
                    "desc": text[:300].strip(),
                    "url": ev_url,
                    "genres": list(set(genres))
                }
                
                if city:
                    coords = geocode(city)
                    if coords:
                        ev["lat"], ev["lon"] = coords
                
                events.append(ev)
                page_count += 1
            
            print(f"[JBS] Page {page}: {page_count} events (total: {len(events)})")
            
            if page_count == 0 and page > 1:
                break
            
            # Nächste Seite
            next_found = False
            for link in soup.find_all("a", href=True):
                if f"page={page+1}" in link["href"] or "&page=" in link["href"]:
                    next_found = True
                    break
            if not next_found:
                if not soup.find(string=re.compile(r"Weiter|Next|›|>>", re.I)):
                    break
            
            page += 1
            time.sleep(2)
            
        except Exception as e:
            print(f"[JBS] Error page {page}: {e}")
            break
    
    print(f"[JBS] DONE: {len(events)} events from {page} pages")
    return events

# ============================================================================
# MAIN
# ============================================================================
def deduplicate(events):
    """Entfernt Duplikate basierend auf Titel+Datum+Stadt"""
    seen = set()
    unique = []
    for ev in events:
        key = f"{ev['title'].lower()}|{ev['date']}|{ev.get('city','').lower()}"
        if key not in seen:
            seen.add(key)
            unique.append(ev)
    return unique

def sort_events(events):
    """Sortiert nach Datum"""
    def parse_sort_date(d):
        try:
            parts = d.split(".")
            if len(parts) >= 3:
                return datetime(int(parts[2]), int(parts[1]), int(parts[0]))
            return datetime.max
        except:
            return datetime.max
    return sorted(events, key=lambda e: parse_sort_date(e["date"]))

def main():
    print("=" * 70)
    print("🎸 Rockabilly Radar Event Scraper v2.0")
    print("   Scraping ALL pages from 4 sources...")
    print("=" * 70)
    
    all_events = []
    
    # Alle Quellen scrapen (mit Pagination)
    all_events.extend(scrape_we_love_country())
    time.sleep(3)
    
    all_events.extend(scrape_swingcalendar())
    time.sleep(3)
    
    all_events.extend(scrape_swingindd())
    time.sleep(3)
    
    all_events.extend(scrape_jukeboxstompers())
    
    # Deduplizieren und sortieren
    print(f"\n[MAIN] Before dedup: {len(all_events)} events")
    all_events = deduplicate(all_events)
    print(f"[MAIN] After dedup: {len(all_events)} events")
    all_events = sort_events(all_events)
    
    # Speichern
    output_file = "events.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_events, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Saved {len(all_events)} events to {output_file}")
    print("=" * 70)
    
    # Statistik
    genres = {}
    for ev in all_events:
        for g in ev.get("genres", []):
            genres[g] = genres.get(g, 0) + 1
    print("Genre distribution:")
    for g, c in sorted(genres.items(), key=lambda x: -x[1]):
        print(f"  {g}: {c}")

if __name__ == "__main__":
    main()
