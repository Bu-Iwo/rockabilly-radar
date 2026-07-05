#!/usr/bin/env python3
"""
Rockabilly Radar Scraper - FUNKTIONIERENDE VERSION
- Korrekter WeLoveCountry Parser (Markdown-Tabellen)
- Playwright für JavaScript-Seiten
- Robuste Fehlerbehandlung
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime
from urllib.parse import urljoin, quote
import sys

# Playwright Import
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️ Playwright nicht installiert!")

GEOCODE_CACHE = {}
TODAY = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

SOCIAL_MEDIA_DOMAINS = [
    "facebook.com", "instagram.com", "tiktok.com", 
    "twitter.com", "x.com", "youtube.com", "fb.com", "youtu.be"
]

PLZ_CORRECTIONS = {
    "52224": ("09366", "Stollberg"),
    "09366": ("09366", "Stollberg"),
}

KNOWN_CITIES = [
    "Berlin", "Hamburg", "München", "Köln", "Frankfurt", "Stuttgart", "Düsseldorf",
    "Leipzig", "Dresden", "Hannover", "Nürnberg", "Bremen", "Chemnitz", "Zwickau",
    "Grimma", "Stollberg", "Ganderkesee", "Biederitz", "Markkleeberg", "Bad Pyrmont",
    "Eging am See", "Neumarkt", "Schipkau", "Forchheim", "Rain",
    "Wolfenbüttel", "Haimhausen", "Landsberg", "Hohenkirchen", "Bad Lauterberg",
    "Lathen-Hilter", "Maintal", "Rodalben", "Limburg", "Mücke", "Ranstadt",
    "Bassum", "Bebra", "Birstein", "Burgstädt", "Celle", "Dreieichenhain",
    "Einbeck", "Eching", "Edewecht", "Elsteraue", "Finsterwalde", "Freising",
    "Gera", "Görlitz", "Hasselfelde", "Hattersheim", "Herzberg", "Hofheim",
    "Krölpa", "Lauf", "Lahnstein", "Leinefelde", "Neuwied", "Niederstriegis",
    "Osterholz", "Pfedelbach", "Perwenitz", "Pretzfeld", "Ramstein",
    "Rossleben", "Saulheim", "Schleusingen", "Schellerten", "Schönwölkau",
    "Solnhofen", "Strausberg", "Tanna", "Teuchern", "Untermeitingen", "Vechta",
    "Waldenburg", "Weichering", "Weiterstadt", "Wernigerode", "Wuppertal",
    "Bissingen", "Buchholz", "Düren", "Asendorf", "Beverstedt", "Au",
    "Wangerland", "Hooksiel", "Senigallia", "Irun", "Las Vegas", "Oslo",
    "Herräng", "Wien", "Zürich", "London", "Paris", "Madrid", "Prag",
    "Amsterdam", "Stockholm", "Helsinki", "Bochum", "Dortmund", "Essen",
    "Triest", "De Rijp", "Valencia", "Blackpool", "Chicago", "Vinuesa",
    "Mühlacker", "Ebenhausen", "Wolframs-Eschenbach", "Magdeburg", "Neuenhagen",
    "Haan", "Hitzacker", "Hamburg-Harburg", "Berlin-Kreuzberg", "Hamburg-Altona",
    "Köln-Ehrenfeld", "Teuchern-Plotha", "Bad Blumau", "Königsleitn", 
    "Great Yarmouth", "Krakau", "Santa Susanna", "Rosolina Mare", "Sos",
    "Meßstetten", "Schwebheim", "Hammelburg", "Nürburg", "Wldfischbach-Burgalben",
    "Aalen-Fachsenfeld", "Hofheim-Eichelsdorf", "Creglingen", "Nohfelden",
    "Dossenheim", "Schwäbisch Gmünd", "Schwäbisch Hall-Sulzdorf", "Essenbach-Ohu",
    "Affing", "Neu-Ulm", "Merkendorf", "Berching-Pollanten", "Kasendorf",
    "Geldersheim", "Homburg", "Wasserburg am Inn", "Elsendorf", "Treuchtlingen",
    "Bad Vilbel", "Kaiserslautern", "Hechingen", "Burghausen", "Sand am Main"
]

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def get_playwright_content(url, scroll=True):
    """Holt HTML-Content einer Seite mit Playwright (Headless Chrome)"""
    if not PLAYWRIGHT_AVAILABLE: return None
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            log(f"  🌐 Playwright: Lade {url}...")
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(5000)
            
            if scroll:
                for _ in range(20):
                    page.evaluate("window.scrollBy(0, 1000)")
                    page.wait_for_timeout(500)
            
            content = page.content()
            browser.close()
            return content
    except Exception as e:
        log(f"  ❌ Playwright Fehler: {e}")
        return None

def geocode_by_plz(plz):
    if not plz: return None
    cache_key = f"plz_{plz}"
    if cache_key in GEOCODE_CACHE: return GEOCODE_CACHE[cache_key]
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": plz, "format": "json", "limit": 1, "countrycodes": "de"},
            headers={"User-Agent": "RockabillyRadar/1.0"},
            timeout=10
        )
        data = r.json()
        if data:
            coords = (float(data[0]["lat"]), float(data[0]["lon"]))
            GEOCODE_CACHE[cache_key] = coords
            time.sleep(1.1)
            return coords
    except: pass
    return None

def geocode(city):
    if not city: return None
    if city in GEOCODE_CACHE: return GEOCODE_CACHE[city]
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": city + ", Deutschland", "format": "json", "limit": 1},
            headers={"User-Agent": "RockabillyRadar/1.0"},
            timeout=10
        )
        data = r.json()
        if data:
            coords = (float(data[0]["lat"]), float(data[0]["lon"]))
            GEOCODE_CACHE[city] = coords
            time.sleep(1.1)
            return coords
    except: pass
    return None

def is_social_media_url(url):
    if not url: return False
    return any(domain in url.lower() for domain in SOCIAL_MEDIA_DOMAINS)

def clean_city(raw_city):
    if not raw_city: return ""
    raw_city = raw_city.replace("'", "").replace('"', '').replace('|', '').strip()
    if ',' in raw_city:
        raw_city = raw_city.split(',')[0].strip()
    for known in KNOWN_CITIES:
        if known.lower() in raw_city.lower():
            return known
    first_word = raw_city.split()[0] if raw_city else ""
    return first_word if 2 < len(first_word) < 30 else raw_city

def correct_plz(plz, city):
    if plz in PLZ_CORRECTIONS:
        correct_plz_val, correct_city = PLZ_CORRECTIONS[plz]
        return correct_plz_val, correct_city
    return plz, city

def parse_date_flexible(text):
    if not text: return None
    m = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', text)
    if m:
        d, mo, y = m.groups()
        return f"{int(d):02d}.{int(mo):02d}.{y}"
    m = re.search(r'(\d{1,2})\.(\d{1,2})\.\s*(?:bis|-|–)\s*(\d{1,2})\.(\d{1,2})\.(\d{4})', text)
    if m:
        d1, m1, d2, m2, y = m.groups()
        return f"{int(d1):02d}.{int(m1):02d}.{y}"
    months_de = {"januar":"01","februar":"02","märz":"03","april":"04","mai":"05","juni":"06",
                 "juli":"07","august":"08","september":"09","oktober":"10","november":"11","dezember":"12"}
    m = re.search(r'(\d{1,2})\.\s*(?:bis|-|–)\s*(\d{1,2})\.\s*(\w+)\s+(\d{4})', text, re.IGNORECASE)
    if m:
        d1, d2, month_name, y = m.groups()
        mo = months_de.get(month_name.lower(), "01")
        return f"{int(d1):02d}.{mo}.{y}"
    months_en = {"jan":"01","feb":"02","mar":"03","apr":"04","may":"05","jun":"06",
                 "jul":"07","aug":"08","sep":"09","oct":"10","nov":"11","dec":"12"}
    m = re.search(r'(?:\w+),\s*(\d{1,2})\s*(?:-|–|bis)\s*(?:\w+),\s*(\d{1,2})\s+(\w+)\s+(\d{4})', text)
    if m:
        d1, d2, month_name, y = m.groups()
        mo = months_en.get(month_name[:3].lower(), "01")
        return f"{int(d1):02d}.{mo}.{y}"
    m = re.search(r'(\w+)\s+(\d{1,2})(?:\s*-\s*(\w+)\s+(\d{1,2}))?,\s*(\d{4})', text, re.IGNORECASE)
    if m:
        mo1_name, d1, mo2_name, d2, y = m.groups()
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
    m = re.search(r'(?:Bands?|Live|Musik|Line Up|Interpreten?)[:\s]*([^\n.]+)', text, re.IGNORECASE)
    if m:
        for part in re.split(r'[,;&]| und ', m.group(1)):
            p = part.strip()
            if 3 < len(p) < 60 and not any(x in p.lower() for x in ["workshops", "shows", "tanzen", "folgt noch"]):
                bands.append(p)
    return bands[:5] if bands else None

def detect_genres(text):
    genres = []
    tl = text.lower()
    if "rockabilly" in tl: genres.append("Rockabilly")
    if "rock'n'roll" in tl or "rock 'n' roll" in tl or "rock and roll" in tl:
        genres.append("Rock'n'Roll")
    if "lindy hop" in tl or "lindy" in tl: genres.append("Lindy Hop")
    if "balboa" in tl: genres.append("Balboa")
    if "charleston" in tl: genres.append("Charleston")
    if "west coast swing" in tl or "west coast" in tl: genres.append("West Coast Swing")
    if "shag" in tl or "collegiate shag" in tl: genres.append("Shag")
    if "solo jazz" in tl or "jazz roots" in tl: genres.append("Solo Jazz")
    if "swing" in tl and not any(g in genres for g in ["Lindy Hop", "Balboa", "Charleston", "West Coast Swing", "Shag", "Solo Jazz"]):
        genres.append("Swing")
    if "boogie" in tl: genres.append("Boogie Woogie")
    if "country" in tl: genres.append("Country")
    if "line dance" in tl: genres.append("Line Dance")
    if "irish" in tl and "Country" not in genres: genres.append("Country")
    if "psychobilly" in tl: genres.append("Rockabilly")
    return list(set(genres)) if genres else []

def build_direct_url(base_url, container, title):
    if container:
        link = container.find("a", href=True)
        if link:
            href = link["href"]
            if href.startswith("http"):
                if is_social_media_url(href): return base_url
                return href
            full_url = urljoin(base_url, href)
            if is_social_media_url(full_url): return base_url
            return full_url
    safe_title = quote(title.strip()[:50])
    return f"{base_url}#:~:text={safe_title}"

def add_coords(ev):
    city = ev.get("city", "")
    plz = ev.get("plz", "")
    if plz:
        corrected_plz, corrected_city = correct_plz(plz, city)
        if corrected_city != city:
            ev["city"] = corrected_city
            city = corrected_city
        ev["address"] = f"{corrected_plz} {corrected_city}"
        plz = corrected_plz
    if city and "lat" not in ev:
        coords = geocode(city)
        if coords:
            ev["lat"], ev["lon"] = coords
            return ev
    if plz and "lat" not in ev:
        coords = geocode_by_plz(plz)
        if coords:
            ev["lat"], ev["lon"] = coords
            return ev
    return ev

# ==================== QUELLE 1: WeLoveCountry (KORRIGIERT) ====================
def scrape_we_love_country():
    """Parst das Markdown-Tabellen-Format von WeLoveCountry"""
    events = []
    url = "https://www.we-love-country.de/1_term.php"
    log("\n[1/10] WeLoveCountry...")
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
        r.encoding = "utf-8"
        if r.status_code != 200:
            log(f"  ❌ HTTP {r.status_code}")
            return events
        
        soup = BeautifulSoup(r.text, "lxml")
        text = soup.get_text("\n", strip=True)
        
        # Splitte in Zeilen
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        
        current_date = None
        count = 0
        
        for i, line in enumerate(lines):
            # Suche nach Datums-Überschriften: "## So. 05.07.2026"
            date_match = re.match(r'^##\s*(?:Mo|Di|Mi|Do|Fr|Sa|So)\.?\s+(\d{2}\.\d{2}\.\d{4})', line)
            if date_match:
                current_date = date_match.group(1)
                continue
            
            # Wenn wir ein Datum haben und die Zeile eine Tabellenzeile ist
            if current_date and '|' in line:
                # Entferne die Pipe-Zeichen
                clean_line = line.replace('|', '').strip()
                
                # Suche nach PLZ (5-stellig)
                plz_match = re.search(r'\b(\d{5})\b', clean_line)
                if not plz_match:
                    continue
                
                plz = plz_match.group(1)
                
                # Extrahiere Stadt (nach PLZ, vor Komma)
                city_match = re.search(r'\d{5}\s+([^,]+)', clean_line)
                if not city_match:
                    continue
                
                city_raw = city_match.group(1).strip()
                city = clean_city(city_raw)
                
                # Extrahiere Event-Titel (nach Komma)
                title_match = re.search(r',\s*[\'"]?([^\'"]+?)[\'"]?\s*(?:im|am|auf|der|des|in|an|bei)', clean_line)
                if not title_match:
                    # Alternativ: Alles nach dem Komma bis zum nächsten Komma oder Ende
                    title_match = re.search(r'\d{5}\s+[^,]+,\s*(.+?)(?:\s*$|\s*Interpret)', clean_line)
                
                if not title_match:
                    continue
                
                title = title_match.group(1).strip()[:100]
                if len(title) < 3:
                    continue
                
                # Hole Details aus den nächsten Zeilen
                details = ""
                for j in range(i+1, min(i+3, len(lines))):
                    if 'Interpret' in lines[j] or 'Beginn' in lines[j]:
                        details = lines[j].replace('|', '').strip()
                        break
                
                if not is_future_event(current_date):
                    continue
                
                full = f"{title} {details}"
                genres = detect_genres(full)
                if not genres:
                    genres = ["Country"]
                
                ev = {
                    "title": title,
                    "date": current_date,
                    "city": city,
                    "plz": plz,
                    "address": f"{plz} {city}",
                    "desc": details[:500] if details else title,
                    "time": extract_time(full),
                    "price": extract_price(full),
                    "bands": extract_bands(full),
                    "url": url,
                    "event_url": url,
                    "genres": genres
                }
                ev = add_coords(ev)
                events.append(ev)
                count += 1
        
        log(f"  ✅ {count} Events")
    except Exception as e:
        log(f"  ❌ Fehler: {e}")
        import traceback
        log(traceback.format_exc())
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
        tables = soup.find_all("table")
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all(["td", "th"])
                if len(cells) < 3: continue
                date_text = cells[0].get_text(" ", strip=True)
                date = parse_date_flexible(date_text)
                if not date or not is_future_event(date): continue
                loc_text = cells[1].get_text(" ", strip=True)
                city = ""
                for c in KNOWN_CITIES:
                    if c.lower() in loc_text.lower(): city = c; break
                desc_text = cells[2].get_text(" ", strip=True)
                if "geschlossene veranstaltung" in desc_text.lower(): continue
                if "abgesagt" in desc_text.lower() or "verschoben" in desc_text.lower(): continue
                title_el = cells[2].find(["strong", "b", "h3", "h4"])
                title = title_el.get_text(strip=True) if title_el else desc_text.split(".")[0][:80]
                if len(title) < 3: continue
                genres = detect_genres(desc_text)
                if not genres: genres = ["Rock'n'Roll"]
                ev = {
                    "title": title.strip(), "date": date, "city": city,
                    "plz": "", "address": loc_text, "desc": desc_text[:500],
                    "time": extract_time(desc_text), "price": extract_price(desc_text),
                    "bands": extract_bands(desc_text),
                    "url": url, "event_url": build_direct_url(url, cells[2], title),
                    "genres": genres
                }
                ev = add_coords(ev)
                events.append(ev)
        log(f"  ✅ {len(events)} Events")
    except Exception as e:
        log(f"  ❌ Fehler: {e}")
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
        pattern = r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)?),\s*([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)\n([^\n]+)\n##\s*([^\n]+)'
        matches = re.findall(pattern, text)
        for match in matches:
            city, country, date_text, title = match
            date = parse_date_flexible(date_text)
            if not date or not is_future_event(date): continue
            if title.lower() in ["load more", "see more", "weiter"]: continue
            if len(title) < 3: continue
            genres = detect_genres(f"{title} {city} {country}")
            if not genres: genres = ["Rockabilly", "Rock'n'Roll"]
            ev = {
                "title": title.strip(), "date": date, "city": city,
                "plz": "", "address": f"{city}, {country}", "desc": f"{title} in {city}, {country}",
                "url": url, "event_url": url, "genres": genres
            }
            ev = add_coords(ev)
            events.append(ev)
        log(f"  ✅ {len(events)} Events")
    except Exception as e:
        log(f"  ❌ Fehler: {e}")
    return events

# ==================== QUELLE 4: SwingCalendar (PLAYWRIGHT) ====================
def scrape_swingcalendar():
    events = []
    url = "https://swingcalendar.com/de"
    log("\n[4/10] SwingCalendar (Playwright)...")
    html = get_playwright_content(url)
    if not html:
        log("  ⚠️ Playwright fehlgeschlagen")
        return events
    
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text("\n", strip=True)
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    count = 0
    for i, line in enumerate(lines):
        date = parse_date_flexible(line)
        if date and is_future_event(date):
            context = " ".join(lines[i:min(i+6, len(lines))])
            city = ""
            for c in KNOWN_CITIES:
                if c.lower() in context.lower():
                    city = c
                    break
            if not city: continue
            title = ""
            for j in range(i+1, min(i+4, len(lines))):
                if len(lines[j]) > 5 and not parse_date_flexible(lines[j]):
                    title = lines[j][:100]
                    break
            if not title or len(title) < 3: continue
            genres = detect_genres(context)
            if not genres: genres = ["Swing", "Lindy Hop"]
            ev = {
                "title": title, "date": date, "city": city,
                "plz": "", "address": city, "desc": context[:500],
                "url": url, "event_url": url, "genres": genres
            }
            ev = add_coords(ev)
            events.append(ev)
            count += 1
    log(f"  ✅ {count} Events via Playwright")
    return events

# ==================== QUELLE 5: SwingInDD (PLAYWRIGHT) ====================
def scrape_swingindd():
    events = []
    url = "https://swingindd.com/home/regionale-swing-kalender/"
    log("\n[5/10] SwingInDD (Playwright)...")
    
    if not PLAYWRIGHT_AVAILABLE:
        log("  ⚠️ Playwright nicht verfügbar")
        return events
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(3000)
            
            buttons = page.query_selector_all('button, .dropdown-toggle, [role="tab"], a')
            for btn in buttons[:20]:
                try:
                    if any(city in (btn.inner_text() or "").lower() for city in ["dresden", "leipzig", "berlin", "hamburg", "prag", "krakau"]):
                        btn.click()
                        page.wait_for_timeout(1500)
                except: pass
            
            for _ in range(15):
                page.evaluate("window.scrollBy(0, 800)")
                page.wait_for_timeout(500)
            
            content = page.content()
            browser.close()
        
        soup = BeautifulSoup(content, "lxml")
        text = soup.get_text("\n", strip=True)
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        
        count = 0
        for i, line in enumerate(lines):
            date = parse_date_flexible(line)
            if date and is_future_event(date):
                context = " ".join(lines[i:min(i+6, len(lines))])
                tl = context.lower()
                if not any(kw in tl for kw in ["swing", "lindy", "balboa", "shag", "tanz", "dance", "social", "party"]):
                    continue
                city = "Dresden"
                for c in KNOWN_CITIES:
                    if c.lower() in context.lower():
                        city = c
                        break
                title = ""
                for j in range(i+1, min(i+4, len(lines))):
                    if len(lines[j]) > 5 and not parse_date_flexible(lines[j]):
                        title = lines[j][:100]
                        break
                if not title or len(title) < 3: continue
                genres = detect_genres(context)
                if not genres: genres = ["Swing", "Lindy Hop"]
                ev = {
                    "title": title, "date": date, "city": city,
                    "plz": "", "address": city, "desc": context[:500],
                    "url": url, "event_url": url, "genres": genres
                }
                ev = add_coords(ev)
                events.append(ev)
                count += 1
        log(f"  ✅ {count} Events via Playwright")
    except Exception as e:
        log(f"  ❌ Playwright Fehler: {e}")
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
        items = soup.find_all(["div", "article", "li", "tr"])
        for item in items:
            text = item.get_text(" ", strip=True)
            date = parse_date_flexible(text)
            if not date or len(text) < 20 or not is_future_event(date): continue
            t_el = item.find(["h2", "h3", "h4", "strong"])
            title = t_el.get_text(strip=True) if t_el else text[:80]
            if len(title) < 3: continue
            cm = {"BO": "Bochum", "DO": "Dortmund", "E": "Essen"}
            city = next((v for k, v in cm.items() if v.lower() in text.lower()), "")
            genres = detect_genres(text)
            if "Lindy Hop" not in genres and "Shag" not in genres:
                genres.insert(0, "Lindy Hop")
            if not genres: genres = ["Lindy Hop", "Swing"]
            ev = {
                "title": title, "date": date, "city": city,
                "plz": "", "address": city, "desc": text[:500],
                "url": url, "event_url": build_direct_url(url, item, title),
                "genres": genres
            }
            ev = add_coords(ev)
            events.append(ev)
        log(f"  ✅ {len(events)} Events")
    except Exception as e:
        log(f"  ❌ Fehler: {e}")
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
        plz_match = re.search(r'\b(\d{5})\b', address)
        plz = plz_match.group(1) if plz_match else ""
        ev = {
            "title": default_title, "date": date, "city": city,
            "plz": plz, "address": address, "desc": text[:500],
            "time": extract_time(text), "price": extract_price(text),
            "bands": extract_bands(text),
            "url": url, "event_url": url, "genres": genres
        }
        ev = add_coords(ev)
        events.append(ev)
        log(f"  ✅ 1 Event")
    except Exception as e:
        log(f"  ❌ Fehler: {e}")
    return events

# ==================== QUELLE 10: Dresden-Hepcats ====================
def scrape_dresden_hepcats():
    events = []
    url = "https://www.dresden-hepcats.de/socials-de"
    log("\n[10/10] Dresden-Hepcats...")
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if r.status_code != 200: return events
        soup = BeautifulSoup(r.text, "lxml")
        items = soup.find_all(["div", "article", "section"])
        for item in items:
            text = item.get_text(" ", strip=True)
            date = parse_date_flexible(text)
            if not date or not is_future_event(date): continue
            if "live" not in text.lower() or "tanz" not in text.lower(): continue
            genres = detect_genres(text)
            if not genres: genres = ["Swing", "Lindy Hop"]
            ev = {
                "title": "Live Tanz Bar", "date": date, "city": "Dresden",
                "plz": "01324", "address": "Parkhotel, Bautzner Landstraße 32, 01324 Dresden",
                "desc": "Social mit Live-Band im Parkhotel auf dem Weißen Hirsch.",
                "time": "20:00 Uhr", "url": url,
                "event_url": build_direct_url(url, item, "Live Tanz Bar"),
                "genres": genres
            }
            ev = add_coords(ev)
            events.append(ev)
        log(f"  ✅ {len(events)} Events")
    except Exception as e:
        log(f"  ❌ Fehler: {e}")
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
    log("🎸 ROCKABILLY RADAR SCRAPER - FUNKTIONIERENDE VERSION")
    log(f"Heute: {TODAY.strftime('%d.%m.%Y')}")
    log(f"Playwright verfügbar: {PLAYWRIGHT_AVAILABLE}")
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
    all_events.extend(scrape_single_festival("https://www.firebirds-festival.de/", "Grimma", "Kloster Nimbschen, Nimbschener Landstraße 1, 04668 Grimma", "Firebirds Festival", ["Rock'n'Roll", "Boogie Woogie", "Lindy Hop"]))
    time.sleep(2)
    all_events.extend(scrape_single_festival("https://rocknroll-festival.de/", "Ganderkesee", "Flugplatz Ganderkesee, Otto-Lilienthal-Str. 23", "Rock'n'Roll Festival Ganderkesee", ["Rock'n'Roll", "Rockabilly"]))
    time.sleep(2)
    all_events.extend(scrape_dresden_hepcats())

    log(f"\n{'=' * 70}")
    log(f"📈 Total vor Deduplikation: {len(all_events)}")
    all_events = deduplicate(all_events)
    log(f"📈 Total nach Deduplikation: {len(all_events)}")

    all_events = sorted(all_events, key=lambda e: parse_date_for_sort(e['date']))
    log("✓ Chronologisch sortiert")

    with open("events.json", "w", encoding="utf-8") as f:
        json.dump(all_events, f, ensure_ascii=False, indent=2)

    log(f"\n✅ GESPEICHERT: {len(all_events)} Events in events.json")
    log("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"\n❌ FATAL: {e}")
        import traceback
        log(traceback.format_exc())
        sys.exit(1)
