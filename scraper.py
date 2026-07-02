#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime
from urllib.parse import urljoin

GEOCODE_CACHE = {}

def geocode(city):
    if not city or city in GEOCODE_CACHE:
        return GEOCODE_CACHE.get(city)
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
        print(f"Geocode error for {city}: {e}")
    return None

def parse_date(text):
    patterns = [
        r'(\d{2})\.(\d{2})\.(\d{4})',
        r'(\d{1,2})\.(\d{1,2})\.(\d{4})',
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            d, mo, y = m.groups()
            return f"{int(d):02d}.{int(mo):02d}.{y}"
    # Partial date DD.MM.
    m = re.search(r'(\d{1,2})\.(\d{1,2})\.', text)
    if m:
        d, mo = m.groups()
        return f"{int(d):02d}.{int(mo):02d}.{datetime.now().year}"
    return None

def scrape_jukeboxstompers():
    events = []
    url = "https://www.jukeboxstompers.de/index.php/veranstaltungen/veranstaltungskalender"
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        soup = BeautifulSoup(r.content, "lxml")
        items = soup.select("div.event, article.event, li.event, tr[class*='event'], div[class*='calendar'] div")
        if not items:
            items = soup.find_all(["div", "article", "li"])
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
            city_match = re.search(r'(?:in|@)\s+([A-ZÄÖÜ][a-zäöüß\-]+(?:\s[a-zäöüß\-]+)?)', text)
            city = city_match.group(1) if city_match else ""
            link = item.find("a", href=True)
            ev_url = urljoin(url, link["href"]) if link else url
            genres = ["Rock'n'Roll"]
            tl = (title + " " + text).lower()
            if "boogie" in tl: genres.append("Boogie Woogie")
            if "swing" in tl or "lindy" in tl: genres.append("Swing")
            if "rockabilly" in tl: genres.append("Rockabilly")
            ev = {"title": title, "date": date, "city": city, "desc": text[:300], "url": ev_url, "genres": list(set(genres))}
            if city:
                coords = geocode(city)
                if coords:
                    ev["lat"], ev["lon"] = coords
            events.append(ev)
    except Exception as e:
        print(f"JukeboxStompers error: {e}")
    print(f"JukeboxStompers: {len(events)} events")
    return events

def scrape_we_love_country():
    events = []
    url = "https://www.we-love-country.de/1_term.php"
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.content, "lxml")
        rows = soup.find_all("tr")
        for row in rows:
            cells = row.find_all(["td", "th"])
            if len(cells) < 2:
                continue
            text = row.get_text(" ", strip=True)
            date = parse_date(text)
            if not date:
                continue
            title_el = row.find(["strong", "b", "a"])
            title = title_el.get_text(strip=True) if title_el else text[:80]
            if len(title) < 3:
                continue
            city_match = re.search(r'(?:in|@)\s+([A-ZÄÖÜ][a-zäöüß\-]+(?:\s[a-zäöüß\-]+)?)', text)
            city = city_match.group(1) if city_match else ""
            link = row.find("a", href=True)
            ev_url = urljoin(url, link["href"]) if link else url
            genres = ["Country"]
            tl = text.lower()
            if "line dance" in tl: genres.append("Line Dance")
            if "rockabilly" in tl: genres.append("Rockabilly")
            if "irish" in tl: genres.append("Irish")
            ev = {"title": title, "date": date, "city": city, "desc": text[:300], "url": ev_url, "genres": list(set(genres))}
            if city:
                coords = geocode(city)
                if coords:
                    ev["lat"], ev["lon"] = coords
            events.append(ev)
    except Exception as e:
        print(f"WeLoveCountry error: {e}")
    print(f"WeLoveCountry: {len(events)} events")
    return events

def scrape_swingcalendar():
    events = []
    url = "https://swingcalendar.com/de"
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        soup = BeautifulSoup(r.content, "lxml")
        items = soup.select("article, div.event, div.item, li.event")
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
            cities = ["Berlin","Dresden","Leipzig","München","Hamburg","Köln","Frankfurt","Wien","Zürich","London","Paris","Rom","Madrid","Prag","Amsterdam","Stockholm","Oslo","Helsinki","Kopenhagen","Trient","Fenestrelle","Perugia"]
            city = next((c for c in cities if c in text), "")
            link = item.find("a", href=True)
            ev_url = urljoin(url, link["href"]) if link else url
            genres = ["Swing"]
            tl = (title + " " + text).lower()
            if "lindy" in tl: genres.append("Lindy Hop")
            if "balboa" in tl: genres.append("Balboa")
            if "charleston" in tl: genres.append("Charleston")
            if "blues" in tl: genres.append("Blues")
            ev = {"title": title, "date": date, "city": city, "desc": text[:300], "url": ev_url, "genres": list(set(genres))}
            if city:
                coords = geocode(city)
                if coords:
                    ev["lat"], ev["lon"] = coords
            events.append(ev)
    except Exception as e:
        print(f"SwingCalendar error: {e}")
    print(f"SwingCalendar: {len(events)} events")
    return events

def scrape_swingindd():
    events = []
    url = "https://swingindd.com/home/regionale-swing-kalender/"
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        soup = BeautifulSoup(r.content, "lxml")
        items = soup.select("article, div.event, li.event, div.entry-content")
        if not items:
            items = soup.find_all(["div", "article", "li"])
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
            city = "Dresden" if "dresden" in text.lower() else ""
            link = item.find("a", href=True)
            ev_url = urljoin(url, link["href"]) if link else url
            genres = ["Swing"]
            tl = (title + " " + text).lower()
            if "lindy" in tl: genres.append("Lindy Hop")
            if "balboa" in tl: genres.append("Balboa")
            if "charleston" in tl: genres.append("Charleston")
            if "shag" in tl: genres.append("Shag")
            ev = {"title": title, "date": date, "city": city, "desc": text[:300], "url": ev_url, "genres": list(set(genres))}
            if city:
                coords = geocode(city)
                if coords:
                    ev["lat"], ev["lon"] = coords
            events.append(ev)
    except Exception as e:
        print(f"SwingInDD error: {e}")
    print(f"SwingInDD: {len(events)} events")
    return events

def deduplicate(events):
    seen = set()
    unique = []
    for ev in events:
        key = f"{ev['title']}_{ev['date']}_{ev.get('city','')}"
        if key not in seen:
            seen.add(key)
            unique.append(ev)
    return unique

def main():
    print("=" * 60)
    print("Rockabilly Radar Event Scraper")
    print("=" * 60)
    all_events = []
    all_events.extend(scrape_jukeboxstompers())
    time.sleep(2)
    all_events.extend(scrape_we_love_country())
    time.sleep(2)
    all_events.extend(scrape_swingcalendar())
    time.sleep(2)
    all_events.extend(scrape_swingindd())
    all_events = deduplicate(all_events)
    print(f"\nTotal unique events: {len(all_events)}")
    with open("events.json", "w", encoding="utf-8") as f:
        json.dump(all_events, f, ensure_ascii=False, indent=2)
    print("Saved to events.json")
    print("=" * 60)

if __name__ == "__main__":
    main()
