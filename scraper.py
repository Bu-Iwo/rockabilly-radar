#!/usr/bin/env python3
"""
Rockabilly Radar Event Scraper - EXPANDED (10 Quellen)
Nur zukünftige Events, chronologisch sortiert, mit allen Details
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
TODAY = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

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
        m = re.search(r'(\d{2})\.(\d{2})\.\s*-\s*(\d{2})\.(\d{2})\.(\d{4})', date_str)
        if m:
            d1, m1, d2, m2, y = m.groups()
            return datetime(int(y), int(m2), int(d2))
    except:
        pass
    return None

def is_future_event(date_str):
    end_date = get_event_end_date(date_str)
    if not end_date:
        return True
    return end_date >= TODAY

def parse_date_for_sort(date_str):
    try:
        m = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', date_str)
        if m:
            d, mo, y = m.groups()
            return datetime(int(y), int(mo), int(d))
    except:
        pass
    return datetime.max

def extract_time(text):
    times = []
    for pattern in [r'(?:Beginn|Einlass|Start)\s*(\d{1,2}:\d{2})\s*(?:Uhr)?', r'(\d{1,2}:\d{2})\s*Uhr']:
        for match in re.findall(pattern, text, re.IGNORECASE):
            times.append(match if isinstance(match, str) else f"{match[0]}:{match[1]}")
    return ', '.join(times[:3]) if times else None

def extract_price(text):
    for pattern in [r'(\d+[,.]?\d*)\s*(?:€|Euro)', r'Eintritt[:\s]*(?:frei|kostenlos)']:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    return None

def extract_bands(text):
    bands = []
    for pattern in [r'(?:Bands?|Live|Musik)[:\s]*([^\n]+)', r'([A-Z][a-z]+\s+(?:&|and)\s+[A-Z][a-z]+(?:\s+Band)?)']:
        for match in re.findall(pattern, text, re.IGNORECASE):
            if 3 < len(match) < 100:
                bands.append(match.strip())
    return bands[:5] if bands else None

def generate_smart_url(base_url, date, city):
    if not date:
        return base_url
    m = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', date)
    if m:
        d, mo, y = m.groups()
        return f"{base_url}#date-{y}-{mo}-{d}"
    return base_url

def add_coords(ev):
    city = ev.get("city", "")
    if city:
        coords = geocode(city)
        if coords:
            ev["lat"], ev["lon"] = coords
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
        pattern = r'(?:Mo|Di|Mi|Do|Fr|Sa|So)\.?\s+(\d{2}\.\d{2}\.\d{4})\s+(\d{5})\s+([^\n]+)\n([^\n]+)(?:\n([^\n]+))?'
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
            if "rock'n'roll" in fl: genres.append("Rock'n'Roll")
            if "boogie" in fl: genres.append("Boogie Woogie")
            ev = add_coords({"title": title, "date": date, "city": city, "address": f"{plz} {city}",
                "desc": details[:500] if details else title, "time": extract_time(full),
                "price": extract_price(full), "bands": extract_bands(full),
                "url": url, "event_url": generate_smart_url(url, date, city), "genres": list(set(genres))})
            events.append(ev)
        log(f"  ✅ {len(events)} Events")
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
        for table in soup.find_all("table"):
            for row in table.find_all("tr"):
                cells = row.find_all(["td", "th"])
                if len(cells) < 2: continue
                text = row.get_text(" ", strip=True)
                date = parse_date(text)
                if not date or not is_future_event(date): continue
                title_el = cells[0].find(["strong", "b", "a"])
                title = title_el.get_text(strip=True) if title_el else text[:80]
                if len(title) < 3: continue
                city_m = re.search(r'(?:in|@|,)\s*([A-ZÄÖÜ][a-zäöüß\-]+)', text)
                city = city_m.group(1) if city_m else ""
                addr = cells[1].get_text(strip=True) if len(cells) >= 2 and len(cells[1].get_text(strip=True)) > 10 else city
                genres = ["Rock'n'Roll"]
                tl = text.lower()
                if "boogie" in tl: genres.append("Boogie Woogie")
                if "swing" in tl or "lindy" in tl: genres.append("Swing")
                if "rockabilly" in tl: genres.append("Rockabilly")
                link = cells[0].find("a", href=True)
                ev_url = urljoin(url, link["href"]) if link else generate_smart_url(url, date, city)
                ev = add_coords({"title": title, "date": date, "city": city, "address": addr,
                    "desc": text[:500], "time": extract_time(text), "price": extract_price(text),
                    "bands": extract_bands(text), "url": url, "event_url": ev_url, "genres": list(set(genres))})
                events.append(ev)
        log(f"  ✅ {len(events)} Events")
    except Exception as e: log(f"  ❌ {e}")
    return events

# ==================== QUELLE 3: SwingCalendar ====================
def scrape_swingcalendar():
    events = []
    url = "https://swingcalendar.com/de"
    log("\n[3/10] SwingCalendar...")
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if r.status_code != 200: return events
        soup = BeautifulSoup(r.text, "lxml")
        for item in soup.find_all(["div", "article", "li"]):
            text = item.get_text(" ", strip=True)
            date = parse_date(text)
            if not date or len(text) < 20 or not is_future_event(date): continue
            t_el = item.find(["h2", "h3", "h4", "strong"])
            title = t_el.get_text(strip=True) if t_el else text[:80]
            if len(title) < 3: continue
            cities = ["Berlin","Dresden","Leipzig","München","Hamburg","Köln","Frankfurt","Wien","Zürich","London","Paris","Rom","Madrid","Prag","Amsterdam","Stockholm","Oslo","Helsinki"]
            city = next((c for c in cities if c in text), "")
            genres = ["Swing"]
            if "lindy" in text.lower(): genres.append("Lindy Hop")
            if "balboa" in text.lower(): genres.append("Balboa")
            link = item.find("a", href=True)
            ev_url = urljoin(url, link["href"]) if link else generate_smart_url(url, date, city)
            ev = add_coords({"title": title, "date": date, "city": city, "address": city,
                "desc": text[:500], "url": url, "event_url": ev_url, "genres": list(set(genres))})
            events.append(ev)
        log(f"  ✅ {len(events)} Events")
    except Exception as e: log(f"  ❌ {e}")
    return events

# ==================== QUELLE 4: SwingInDD ====================
def scrape_swingindd():
    events = []
    url = "https://swingindd.com/home/regionale-swing-kalender/"
    log("\n[4/10] SwingInDD...")
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if r.status_code != 200: return events
        soup = BeautifulSoup(r.text, "lxml")
        for item in soup.find_all(["div", "article", "li"]):
            text = item.get_text(" ", strip=True)
            date = parse_date(text)
            if not date or len(text) < 20 or not is_future_event(date): continue
            t_el = item.find(["h2", "h3", "h4", "strong"])
            title = t_el.get_text(strip=True) if t_el else text[:80]
            if len(title) < 3: continue
            city = "Dresden" if "dresden" in text.lower() else ""
            genres = ["Swing"]
            if "lindy" in text.lower(): genres.append("Lindy Hop")
            if "balboa" in text.lower(): genres.append("Balboa")
            link = item.find("a", href=True)
            ev_url = urljoin(url, link["href"]) if link else generate_smart_url(url, date, city)
            ev = add_coords({"title": title, "date": date, "city": city, "address": city,
                "desc": text[:500], "url": url, "event_url": ev_url, "genres": list(set(genres))})
            events.append(ev)
        log(f"  ✅ {len(events)} Events")
    except Exception as e: log(f"  ❌ {e}")
    return events

# ==================== QUELLE 5: Dresden-Hepcats ====================
def scrape_dresden_hepcats():
    events = []
    url = "https://www.dresden-hepcats.de/socials-de"
    log("\n[5/10] Dresden-Hepcats...")
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if r.status_code != 200: return events
        soup = BeautifulSoup(r.text, "lxml")
        for item in soup.find_all(["div", "article", "section"]):
            text = item.get_text(" ", strip=True)
            date = parse_date(text)
            if not date or len(text) < 30 or not is_future_event(date): continue
            if "live" not in text.lower() or "tanz" not in text.lower(): continue
            ev = add_coords({"title": "Live Tanz Bar", "date": date, "city": "Dresden",
                "address": "Parkhotel, Bautzner Landstraße 32, 01324 Dresden",
                "desc": "Social mit Live-Band im Parkhotel auf dem Weißen Hirsch.",
                "time": "20:00 Uhr", "url": url, "event_url": url, "genres": ["Swing", "Lindy Hop"]})
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
            date = parse_date(text)
            if not date or len(text) < 20 or not is_future_event(date): continue
            t_el = item.find(["h2", "h3", "h4", "strong"])
            title = t_el.get_text(strip=True) if t_el else text[:80]
            if len(title) < 3: continue
            cm = {"BO": "Bochum", "DO": "Dortmund", "E": "Essen"}
            city = next((v for k, v in cm.items() if v.lower() in text.lower()), "")
            genres = ["Swing"]
            if "lindy" in text.lower(): genres.append("Lindy Hop")
            link = item.find("a", href=True)
            ev_url = urljoin(url, link["href"]) if link else generate_smart_url(url, date, city)
            ev = add_coords({"title": title, "date": date, "city": city, "address": city,
                "desc": text[:500], "url": url, "event_url": ev_url, "genres": list(set(genres))})
            events.append(ev)
        log(f"  ✅ {len(events)} Events")
    except Exception as e: log(f"  ❌ {e}")
    return events

# ==================== QUELLE 7: Summer Shelter ====================
def scrape_summer_shelter():
    events = []
    url = "https://summershelter.de/"
    log("\n[7/10] Summer Shelter...")
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if r.status_code != 200: return events
        soup = BeautifulSoup(r.text, "lxml")
        text = soup.get_text(" ", strip=True)
        # Suche nach Datum und Event-Infos
        date = parse_date(text)
        if date and is_future_event(date):
            # Extrahiere Bands aus dem Text
            bands = extract_bands(text)
            price = extract_price(text)
            time_info = extract_time(text)
            ev = add_coords({"title": "Summer Shelter - Rock'n'Roll Open Air",
                "date": date, "city": "Biederitz", "address": "Parkweg 1A, 39175 Biederitz",
                "desc": "Rock'n'Roll Open Air Festival bei Magdeburg mit Live Bands, Shows, Marketplace und Cars.",
                "time": time_info, "price": price, "bands": bands,
                "url": url, "event_url": url, "genres": ["Rock'n'Roll", "Rockabilly"]})
            events.append(ev)
        log(f"  ✅ {len(events)} Events")
    except Exception as e: log(f"  ❌ {e}")
    return events

# ==================== QUELLE 8: Firebirds Festival ====================
def scrape_firebirds():
    events = []
    url = "https://www.firebirds-festival.de/"
    log("\n[8/10] Firebirds Festival...")
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if r.status_code != 200: return events
        soup = BeautifulSoup(r.text, "lxml")
        text = soup.get_text(" ", strip=True)
        date = parse_date(text)
        if date and is_future_event(date):
            bands = extract_bands(text)
            price = extract_price(text)
            ev = add_coords({"title": "Firebirds Festival",
                "date": date, "city": "Grimma", "address": "Kloster Nimbschen, Nimbschener Landstraße 1, 04668 Grimma",
                "desc": "Deutschlands schönster Rock'n'Roll Weekender mit 30 internationalen Bands & DJs, Dancecamp, Oldtimer.",
                "price": price, "bands": bands,
                "url": url, "event_url": url, "genres": ["Rock'n'Roll", "Rockabilly", "Swing"]})
            events.append(ev)
        log(f"  ✅ {len(events)} Events")
    except Exception as e: log(f"  ❌ {e}")
    return events

# ==================== QUELLE 9: Rock'n'Roll Festival Ganderkesee ====================
def scrape_rocknroll_festival():
    events = []
    url = "https://rocknroll-festival.de/"
    log("\n[9/10] Rock'n'Roll Festival Ganderkesee...")
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if r.status_code != 200: return events
        soup = BeautifulSoup(r.text, "lxml")
        text = soup.get_text(" ", strip=True)
        date = parse_date(text)
        if date and is_future_event(date):
            bands = extract_bands(text)
            price = extract_price(text)
            ev = add_coords({"title": "Rock'n'Roll Festival Ganderkesee",
                "date": date, "city": "Ganderkesee", "address": "Flugplatz Ganderkesee, Otto-Lilienthal-Str. 23, 27777 Ganderkesee",
                "desc": "3 Tage Rock'n'Roll Festival am Flugplatz mit historischen Flugzeugen, Oldtimern, Vintage-Market.",
                "price": price, "bands": bands,
                "url": url, "event_url": url, "genres": ["Rock'n'Roll", "Rockabilly"]})
            events.append(ev)
        log(f"  ✅ {len(events)} Events")
    except Exception as e: log(f"  ❌ {e}")
    return events

# ==================== QUELLE 10: RockabillyRules ====================
def scrape_rockabillyrules():
    events = []
    url = "https://rockabillyrules.com/all-events/"
    log("\n[10/10] RockabillyRules...")
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if r.status_code != 200: return events
        soup = BeautifulSoup(r.text, "lxml")
        # RockabillyRules listet Events als Karten/Listeneinträge
        for item in soup.find_all(["div", "article", "li"]):
            text = item.get_text(" ", strip=True)
            date = parse_date(text)
            if not date or len(text) < 20 or not is_future_event(date): continue
            t_el = item.find(["h2", "h3", "h4", "strong"])
            title = t_el.get_text(strip=True) if t_el else text[:80]
            if len(title) < 3: continue
            # Stadt aus Text extrahieren
            city_m = re.search(r'(?:in|@|,)\s*([A-Z][a-z]+(?:\s[a-z]+)?)', text)
            city = city_m.group(1) if city_m else ""
            genres = ["Rockabilly", "Rock'n'Roll"]
            if "psychobilly" in text.lower(): genres.append("Psychobilly")
            link = item.find("a", href=True)
            ev_url = urljoin(url, link["href"]) if link else url
            ev = add_coords({"title": title, "date": date, "city": city, "address": city,
                "desc": text[:500], "url": url, "event_url": ev_url, "genres": list(set(genres))})
            events.append(ev)
        log(f"  ✅ {len(events)} Events")
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
    log("🎸 ROCKABILLY RADAR SCRAPER - 10 QUELLEN")
    log(f"Heute: {TODAY.strftime('%d.%m.%Y')} - nur zukünftige Events")
    log("=" * 70)

    all_events = []
    scrapers = [
        scrape_we_love_country, scrape_jukeboxstompers, scrape_swingcalendar,
        scrape_swingindd, scrape_dresden_hepcats, scrape_lindypott,
        scrape_summer_shelter, scrape_firebirds, scrape_rocknroll_festival,
        scrape_rockabillyrules
    ]
    for scraper in scrapers:
        all_events.extend(scraper())
        time.sleep(2)

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
