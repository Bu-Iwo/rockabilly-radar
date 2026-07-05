#!/usr/bin/env python3
"""
Rockabilly Radar Scraper - FINAL PRODUCTION VERSION
- 10 Quellen, strikte Validierung, keine Generierung
- Direkte Event-Links oder CSS Text Fragments für Auto-Scroll
- Optimiert für 1000+ Events
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime
from urllib.parse import urljoin, quote
import sys

GEOCODE_CACHE = {}
TODAY = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def geocode(city):
    if not city: return None
    if city in GEOCODE_CACHE: return GEOCODE_CACHE[city]
    try:
        r = requests.get("https://nominatim.openstreetmap.org/search",
            params={"q": city, "format": "json", "limit": 1},
            headers={"User-Agent": "RockabillyRadar/1.0"}, timeout=10)
        data = r.json()
        if data:
            coords = (float(data[0]["lat"]), float(data[0]["lon"]))
            GEOCODE_CACHE[city] = coords
            time.sleep(1.1)
            return coords
    except: pass
    return None

def parse_date_flexible(text):
    """Parst alle bekannten Datumsformate aus den Quellen"""
    # DD.MM.YYYY
    m = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', text)
    if m:
        d, mo, y = m.groups()
        return f"{int(d):02d}.{int(mo):02d}.{y}"
    
    # DD.MM. bis DD.MM.YYYY
    m = re.search(r'(\d{1,2})\.(\d{1,2})\.\s*(?:bis|-|–)\s*(\d{1,2})\.(\d{1,2})\.(\d{4})', text)
    if m:
        d1, m1, d2, m2, y = m.groups()
        return f"{int(d1):02d}.{int(m1):02d}.{y}"
    
    # "21. - 23. August 2026"
    months_de = {"januar":"01","februar":"02","märz":"03","april":"04","mai":"05","juni":"06",
                 "juli":"07","august":"08","september":"09","oktober":"10","november":"11","dezember":"12"}
    m = re.search(r'(\d{1,2})\.\s*(?:bis|-|–)\s*(\d{1,2})\.\s*(\w+)\s+(\d{4})', text, re.IGNORECASE)
    if m:
        d1, d2, month_name, y = m.groups()
        mo = months_de.get(month_name.lower(), "01")
        return f"{int(d1):02d}.{mo}.{y}"
    
    # "Fri, 03 - Sun, 05 Jul 2026" (RockabillyRules)
    months_en = {"jan":"01","feb":"02","mar":"03","apr":"04","may":"05","jun":"06",
                 "jul":"07","aug":"08","sep":"09","oct":"10","nov":"11","dec":"12"}
    m = re.search(r'(?:\w+),\s*(\d{1,2})\s*(?:-|–|bis)\s*(?:\w+),\s*(\d{1,2})\s+(\w+)\s+(\d{4})', text)
    if m:
        d1, d2, month_name, y = m.groups()
        mo = months_en.get(month_name[:3].lower(), "01")
        return f"{int(d1):02d}.{mo}.{y}"
    
    # "Tue, 30 Jun - Tue, 07 Jul 2026"
    m = re.search(r'(?:\w+),\s*(\d{1,2})\s+(\w+)\s*(?:-|–)\s*(?:\w+),\s*(\d{1,2})\s+(\w+)\s+(\d{4})', text)
    if m:
        d1, mo1_name, d2, mo2_name, y = m.groups()
        mo = months_en.get(mo1_name[:3].lower(), "01")
        return f"{int(d1):02d}.{mo}.{y}"
    
    return None

def get_event_end_date(date_str):
    try:
        matches = list(re.finditer(r'(\d{2})\.(\d{2})\.(\d{4})', date_str))
        if len(matches) >= 2:
            last = matches[-1]
            d, mo, y = last.groups()
            return datetime(int(y), int(mo), int(d))
        elif len(matches) == 1:
            d, mo, y = matches[0].groups()
            return datetime(int(y), int(mo), int(d))
    except: pass
    return None

def is_future_event(date_str):
    end_date = get_event_end_date(date_str)
    if not end_date: return True
    return end_date >= TODAY

def parse_date_for_sort(date_str):
    try:
        m = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', date_str)
        if m:
            d, mo, y = m.groups()
            return datetime(int(y), int(mo), int(d))
    except: pass
    return datetime.max

def extract_time(text):
    for p in [r'(?:Beginn|Einlass|Start)\s*[:\s]*(\d{1,2}:\d{2})', r'(\d{1,2}:\d{2})\s*Uhr']:
        m = re.search(p, text, re.IGNORECASE)
        if m: return m.group(1)
    return None

def extract_price(text):
    m = re.search(r'(\d+[,.]?\d*)\s*(?:€|Euro)', text, re.IGNORECASE)
    if m: return m.group(0)
    if re.search(r'(?:frei|kostenlos)', text, re.IGNORECASE): return "Eintritt frei"
    return None

def extract_bands(text):
    bands = []
    m = re.search(r'(?:Bands?|Live|Musik|Line Up)[:\s]*([^\n.]+)', text, re.IGNORECASE)
    if m:
        for part in re.split(r'[,;&]| und ', m.group(1)):
            p = part.strip()
            if 3 < len(p) < 60: bands.append(p)
    return bands[:5] if bands else None

def build_direct_url(base_url, container, title):
    """Findet echten Link im Container oder nutzt CSS Text Fragment für Auto-Scroll.
       WICHTIG: Filtert Facebook, Instagram, TikTok etc. heraus!"""
    link = container.find("a", href=True)
    if link:
        href = link["href"]
        if href.startswith("http"):
            # KEINE Social Media Links als Event-URL akzeptieren
            social_media_domains = ["facebook.com", "instagram.com", "tiktok.com", 
                                    "twitter.com", "x.com", "youtube.com", "fb.com", "youtu.be"]
            if any(sm in href.lower() for sm in social_media_domains):
                return base_url # Fallback auf die Hauptseite der Quelle
            return href
        return urljoin(base_url, href)
    
    # Fallback: CSS Text Fragment (scrollt & highlightet automatisch im Browser)
    safe_title = quote(title.strip()[:50])
    return f"{base_url}#:~:text={safe_title}"

def add_coords(ev):
    city = ev.get("city", "")
    if city and "lat" not in ev:
        coords = geocode(city)
        if coords: ev["lat"], ev["lon"] = coords
    return ev

# ==================== QUELLE 1: WeLoveCountry ====================
def scrape_we_love_country():
    events = []
    url = "https://www.we-love-country.de/1_term.php"
    log("\n[1/10] WeLoveCountry...")
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
        r.encoding = "utf-8"
        if r.status_code != 200: return events
        soup = BeautifulSoup(r.text, "lxml")
        text = soup.get_text("\n", strip=True)
        
        pattern = r'(?:Mo|Di|Mi|Do|Fr|Sa|So)\.?\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{5})\s+([^\n]+)\n([^\n]+)(?:\n([^\n]+))?'
        count = 0
        for match in re.findall(pattern, text):
            if len(match) < 4: continue
            date, plz, city, title = match[0], match[1], match[2].strip(), match[3].strip()
            details = match[4].strip() if len(match) > 4 else ""
            if len(title) < 3 or not is_future_event(date): continue
            
            full = f"{title} {details}"
            genres = ["Country"]
            fl = full.lower()
            if "line dance" in fl: genres.append("Line Dance")
            if "rockabilly" in fl: genres.append("Rockabilly")
            if "rock'n'roll" in fl or "rock 'n' roll" in fl: genres.append("Rock'n'Roll")
            if "boogie" in fl: genres.append("Boogie Woogie")
            if "irish" in fl: genres.append("Irish")
            
            ev = add_coords({
                "title": title, "date": date, "city": city,
                "address": f"{plz} {city}",
                "desc": details[:500] if details else title,
                "time": extract_time(full), "price": extract_price(full),
                "bands": extract_bands(full),
                "url": url, "event_url": build_direct_url(url, soup, title),
                "genres": list(set(genres))
            })
            events.append(ev)
            count += 1
        log(f"  ✅ {count} Events")
    except Exception as e: log(f"  ❌ {e}")
    return events

# ==================== QUELLE 2: JukeboxStompers ====================
def scrape_jukeboxstompers():
    events = []
    url = "https://www.jukeboxstompers.de/index.php/veranstaltungen/veranstaltungskalender"
    log("\n[2/10] JukeboxStompers...")
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if r.status_code != 200: return events
        soup = BeautifulSoup(r.text, "lxml")
        
        for row in soup.select("table tr"):
            cells = row.find_all(["td", "th"])
            if len(cells) < 3: continue
            
            date_text = cells[0].get_text(" ", strip=True)
            date = parse_date_flexible(date_text)
            if not date or not is_future_event(date): continue
            
            loc_text = cells[1].get_text(" ", strip=True)
            city = ""
            for c in ["Leipzig","Grimma","Bad Pyrmont","Oslo","Biederitz","Ganderkesee","Markkleeberg","Zürich","Wolfenbüttel","Haimhausen","Rain","Hohenkirchen","München","Landsberg","Triest","De Rijp"]:
                if c.lower() in loc_text.lower(): city = c; break
            
            desc_text = cells[2].get_text(" ", strip=True)
            title_el = cells[2].find(["strong", "b"])
            title = title_el.get_text(strip=True) if title_el else desc_text.split(".")[0][:80]
            if len(title) < 3: continue
            
            genres = ["Rock'n'Roll"]
            tl = desc_text.lower()
            if "boogie" in tl: genres.append("Boogie Woogie")
            if "swing" in tl or "lindy" in tl: genres.append("Swing")
            if "rockabilly" in tl: genres.append("Rockabilly")
            
            ev = add_coords({
                "title": title.strip(), "date": date, "city": city,
                "address": loc_text, "desc": desc_text[:500],
                "time": extract_time(desc_text), "price": extract_price(desc_text),
                "bands": extract_bands(desc_text),
                "url": url, "event_url": build_direct_url(url, cells[2], title),
                "genres": list(set(genres))
            })
            events.append(ev)
        log(f"  ✅ {len(events)} Events")
    except Exception as e: log(f"  ❌ {e}")
    return events

# ==================== QUELLE 3: RockabillyRules ====================
def scrape_rockabillyrules():
    events = []
    url = "https://rockabillyrules.com/all-events/"
    log("\n[3/10] RockabillyRules...")
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if r.status_code != 200: return events
        soup = BeautifulSoup(r.text, "lxml")
        text = soup.get_text("\n", strip=True)
        
        # Format: City, Country\nDay, DD - Day, DD Mon YYYY\n## Title
        blocks = re.split(r'\n(?=[A-Z][a-z]+,\s*[A-Z])', text)
        for block in blocks:
            lines = [l.strip() for l in block.split("\n") if l.strip()]
            if len(lines) < 3: continue
            
            city_raw = lines[0]
            city = city_raw.split(",")[0].strip()
            date = parse_date_flexible(lines[1])
            if not date or not is_future_event(date): continue
            
            title = lines[2].replace("##", "").strip()
            if len(title) < 3: continue
            
            genres = ["Rockabilly", "Rock'n'Roll"]
            if "psychobilly" in title.lower(): genres.append("Psychobilly")
            
            ev = add_coords({
                "title": title, "date": date, "city": city,
                "address": city_raw, "desc": f"{title} in {city_raw}",
                "url": url, "event_url": build_direct_url(url, soup, title),
                "genres": list(set(genres))
            })
            events.append(ev)
        log(f"  ✅ {len(events)} Events")
    except Exception as e: log(f"  ❌ {e}")
    return events

# ==================== QUELLE 4: SwingCalendar ====================
def scrape_swingcalendar():
    events = []
    url = "https://swingcalendar.com/de"
    log("\n[4/10] SwingCalendar...")
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if r.status_code != 200: return events
        soup = BeautifulSoup(r.text, "lxml")
        
        for item in soup.find_all(["div", "article", "li"]):
            text = item.get_text(" ", strip=True)
            date = parse_date_flexible(text)
            if not date or len(text) < 30 or not is_future_event(date): continue
            
            t_el = item.find(["h2", "h3", "h4", "strong"])
            title = t_el.get_text(strip=True) if t_el else text[:80]
            if len(title) < 3: continue
            
            cities = ["Berlin","Dresden","Leipzig","München","Hamburg","Köln","Frankfurt","Wien","Zürich","London","Paris","Rom","Madrid","Prag","Amsterdam","Stockholm","Oslo","Helsinki"]
            city = next((c for c in cities if c in text), "")
            
            genres = ["Swing"]
            if "lindy" in text.lower(): genres.append("Lindy Hop")
            if "balboa" in text.lower(): genres.append("Balboa")
            
            ev = add_coords({
                "title": title, "date": date, "city": city, "address": city,
                "desc": text[:500], "url": url, "event_url": build_direct_url(url, item, title),
                "genres": list(set(genres))
            })
            events.append(ev)
        log(f"  ✅ {len(events)} Events")
    except Exception as e: log(f"  ❌ {e}")
    return events

# ==================== QUELLE 5: SwingInDD ====================
def scrape_swingindd():
    events = []
    url = "https://swingindd.com/home/regionale-swing-kalender/"
    log("\n[5/10] SwingInDD...")
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if r.status_code != 200: return events
        soup = BeautifulSoup(r.text, "lxml")
        
        for item in soup.find_all(["div", "article", "li"]):
            text = item.get_text(" ", strip=True)
            date = parse_date_flexible(text)
            if not date or len(text) < 20 or not is_future_event(date): continue
            
            t_el = item.find(["h2", "h3", "h4", "strong"])
            title = t_el.get_text(strip=True) if t_el else text[:80]
            if len(title) < 3: continue
            
            city = "Dresden" if "dresden" in text.lower() else ""
            genres = ["Swing"]
            if "lindy" in text.lower(): genres.append("Lindy Hop")
            if "balboa" in text.lower(): genres.append("Balboa")
            
            ev = add_coords({
                "title": title, "date": date, "city": city, "address": city,
                "desc": text[:500], "url": url, "event_url": build_direct_url(url, item, title),
                "genres": list(set(genres))
            })
            events.append(ev)
        log(f"  ✅ {len(events)} Events")
    except Exception as e: log(f"  ❌ {e}")
    return events

# ==================== QUELLE 6: Lindypott ====================
def scrape_lindypott():
    events = []
    url = "https://www.lindypott.de/kalender.html?ort=BO,DO,E&art=3"
    log("\n[6/10] Lindypott...")
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if r.status_code != 200: return events
        soup = BeautifulSoup(r.text, "lxml")
        
        for item in soup.find_all(["div", "article", "li", "tr"]):
            text = item.get_text(" ", strip=True)
            date = parse_date_flexible(text)
            if not date or len(text) < 20 or not is_future_event(date): continue
            
            t_el = item.find(["h2", "h3", "h4", "strong"])
            title = t_el.get_text(strip=True) if t_el else text[:80]
            if len(title) < 3: continue
            
            cm = {"BO": "Bochum", "DO": "Dortmund", "E": "Essen"}
            city = next((v for k, v in cm.items() if v.lower() in text.lower()), "")
            genres = ["Swing"]
            if "lindy" in text.lower(): genres.append("Lindy Hop")
            
            ev = add_coords({
                "title": title, "date": date, "city": city, "address": city,
                "desc": text[:500], "url": url, "event_url": build_direct_url(url, item, title),
                "genres": list(set(genres))
            })
            events.append(ev)
        log(f"  ✅ {len(events)} Events")
    except Exception as e: log(f"  ❌ {e}")
    return events

# ==================== QUELLE 7-9: Einzel-Festivals ====================
def scrape_single_festival(url, city, address, default_title, genres):
    events = []
    log(f"\n  🔍 {url}...")
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if r.status_code != 200: return events
        soup = BeautifulSoup(r.text, "lxml")
        text = soup.get_text(" ", strip=True)
        date = parse_date_flexible(text)
        if not date or not is_future_event(date): return events
        
        ev = add_coords({
            "title": default_title, "date": date, "city": city, "address": address,
            "desc": text[:500], "time": extract_time(text), "price": extract_price(text),
            "bands": extract_bands(text), "url": url, "event_url": url,
            "genres": genres
        })
        events.append(ev)
        log(f"  ✅ 1 Event")
    except Exception as e: log(f"  ❌ {e}")
    return events

# ==================== QUELLE 10: Dresden-Hepcats ====================
def scrape_dresden_hepcats():
    # Strikt: Nur explizit gelistete Daten. Keine Generierung!
    events = []
    url = "https://www.dresden-hepcats.de/socials-de"
    log("\n[10/10] Dresden-Hepcats...")
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if r.status_code != 200: return events
        soup = BeautifulSoup(r.text, "lxml")
        for item in soup.find_all(["div", "article", "section"]):
            text = item.get_text(" ", strip=True)
            date = parse_date_flexible(text)
            if not date or not is_future_event(date): continue
            if "live" not in text.lower() or "tanz" not in text.lower(): continue
            
            ev = add_coords({
                "title": "Live Tanz Bar", "date": date, "city": "Dresden",
                "address": "Parkhotel, Bautzner Landstraße 32, 01324 Dresden",
                "desc": "Social mit Live-Band im Parkhotel auf dem Weißen Hirsch.",
                "time": "20:00 Uhr", "url": url, "event_url": build_direct_url(url, item, "Live Tanz Bar"),
                "genres": ["Swing", "Lindy Hop"]
            })
            events.append(ev)
        log(f"  ✅ {len(events)} Events (nur explizit gelistet)")
    except Exception as e: log(f"  ❌ {e}")
    return events

# ==================== MAIN ====================
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
    log("=" * 70)
    log("🎸 ROCKABILLY RADAR SCRAPER - STRICT & COMPLETE")
    log(f"Heute: {TODAY.strftime('%d.%m.%Y')} - nur explizit gelistete, zukünftige Events")
    log("=" * 70)

    all_events = []
    all_events.extend(scrape_we_love_country())
    time.sleep(2)
    all_events.extend(scrape_jukeboxstompers())
    time.sleep(2)
    all_events.extend(scrape_rockabillyrules())
    time.sleep(2)
    all_events.extend(scrape_swingcalendar())
    time.sleep(2)
    all_events.extend(scrape_swingindd())
    time.sleep(2)
    all_events.extend(scrape_lindypott())
    time.sleep(2)
    all_events.extend(scrape_single_festival("https://summershelter.de/", "Biederitz", "Parkweg 1A, 39175 Biederitz", "Summer Shelter Open Air", ["Rock'n'Roll", "Rockabilly"]))
    time.sleep(2)
    all_events.extend(scrape_single_festival("https://www.firebirds-festival.de/", "Grimma", "Kloster Nimbschen, Nimbschener Landstraße 1", "Firebirds Festival", ["Rock'n'Roll", "Boogie Woogie", "Lindy Hop"]))
    time.sleep(2)
    all_events.extend(scrape_single_festival("https://rocknroll-festival.de/", "Ganderkesee", "Flugplatz Ganderkesee, Otto-Lilienthal-Str. 23", "Rock'n'Roll Festival Ganderkesee", ["Rock'n'Roll", "Rockabilly"]))
    time.sleep(2)
    all_events.extend(scrape_dresden_hepcats())

    log(f"\nTotal vor Deduplikation: {len(all_events)}")
    all_events = deduplicate(all_events)
    log(f"Total nach Deduplikation: {len(all_events)}")

    future = [e for e in all_events if is_future_event(e['date'])]
    log(f"Zukünftige Events: {len(future)}")

    future = sorted(future, key=lambda e: parse_date_for_sort(e['date']))
    log("✓ Chronologisch sortiert")

    with open("events.json", "w", encoding="utf-8") as f:
        json.dump(future, f, ensure_ascii=False, indent=2)

    log(f"\n✅ GESPEICHERT: {len(future)} Events")
    log("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"\n❌ FATAL: {e}")
        import traceback
        log(traceback.format_exc())
        sys.exit(1)
