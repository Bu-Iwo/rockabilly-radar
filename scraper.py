#!/usr/bin/env python3
"""
Rockabilly Radar Event Scraper
Scrapt Events von:
- we-love-country.de
- swingcalendar.com
- swingindd.com
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from datetime import datetime
import re
from urllib.parse import urljoin
import os

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Cache für Geocoding
geocode_cache = {}

def geocode_city(city_name):
    """Konvertiert Stadtnamen zu Koordinaten via Nominatim"""
    if city_name in geocode_cache:
        return geocode_cache[city_name]
    
    try:
        url = f"https://nominatim.openstreetmap.org/search"
        params = {
            'q': city_name,
            'format': 'json',
            'limit': 1,
            'countrycodes': 'de,at,ch,fr,it,es,uk,us,nl,dk,se,no,fi,be,lu,pl,cz'
        }
        headers = {'User-Agent': 'RockabillyRadar/1.0 (Event Scraper)'}
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            geocode_cache[city_name] = (lat, lon)
            time.sleep(1)  # Rate limiting für Nominatim
            return (lat, lon)
    except Exception as e:
        logger.error(f"Geocoding Fehler für {city_name}: {e}")
    
    return None

def extract_date_from_text(text):
    """Extrahiert Datum aus Text"""
    # Verschiedene Datumsformate
    patterns = [
        r'(\d{2})\.(\d{2})\.(\d{4})',  # DD.MM.YYYY
        r'(\d{2})\.(\d{2})\.',          # DD.MM. (Jahr wird ergänzt)
        r'(\d{1,2})\.(\d{1,2})\.(\d{4})',  # D.M.YYYY
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            if len(match.groups()) == 3:
                day, month, year = match.groups()
                return f"{day.zfill(2)}.{month.zfill(2)}.{year}"
            elif len(match.groups()) == 2:
                day, month = match.groups()
                year = datetime.now().year
                return f"{day.zfill(2)}.{month.zfill(2)}.{year}"
    
    return None

def scrape_we_love_country():
    """Scrapt alle Events von we-love-country.de"""
    logger.info("Starte Scraping: we-love-country.de")
    events = []
    
    base_url = "https://www.we-love-country.de"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        # Hauptseite laden
        response = requests.get(f"{base_url}/1_term.php", headers=headers, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Alle Event-Container finden
        event_containers = soup.find_all('div', class_='event')
        
        if not event_containers:
            # Alternative Struktur versuchen
            event_containers = soup.find_all('tr')
        
        logger.info(f"Gefunden: {len(event_containers)} Event-Container")
        
        for container in event_containers:
            try:
                # Titel extrahieren
                title_elem = container.find(['h2', 'h3', 'strong', 'b'])
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                if not title or len(title) < 3:
                    continue
                
                # Datum extrahieren
                date_text = container.get_text()
                date = extract_date_from_text(date_text)
                
                if not date:
                    continue
                
                # Stadt extrahieren
                city = ""
                city_elem = container.find(string=re.compile(r'in\s+([A-ZÄÖÜ][a-zäöü]+)'))
                if city_elem:
                    match = re.search(r'in\s+([A-ZÄÖÜ][a-zäöü]+)', city_elem)
                    if match:
                        city = match.group(1)
                
                # Beschreibung extrahieren
                desc = container.get_text(strip=True)
                if len(desc) > 300:
                    desc = desc[:300] + "..."
                
                # URL extrahieren
                url = base_url + "/1_term.php"
                link_elem = container.find('a', href=True)
                if link_elem:
                    url = urljoin(base_url, link_elem['href'])
                
                # Genres bestimmen
                genres = ["Country"]
                title_lower = title.lower()
                desc_lower = desc.lower()
                
                if "line dance" in title_lower or "line dance" in desc_lower:
                    genres.append("Line Dance")
                if "rockabilly" in title_lower or "rockabilly" in desc_lower:
                    genres.append("Rockabilly")
                if "rock'n'roll" in title_lower or "rock 'n' roll" in desc_lower:
                    genres.append("Rock'n'Roll")
                if "irish" in title_lower or "irish" in desc_lower:
                    genres.append("Irish")
                
                event = {
                    "title": title,
                    "date": date,
                    "city": city,
                    "desc": desc,
                    "url": url,
                    "genres": genres
                }
                
                # Geocoding
                if city:
                    coords = geocode_city(city)
                    if coords:
                        event["lat"] = coords[0]
                        event["lon"] = coords[1]
                
                events.append(event)
                
            except Exception as e:
                logger.error(f"Fehler beim Verarbeiten eines Events: {e}")
                continue
        
        logger.info(f"we-love-country.de: {len(events)} Events extrahiert")
        
    except Exception as e:
        logger.error(f"Fehler beim Scraping von we-love-country.de: {e}")
    
    return events

def scrape_swing_calendar():
    """Scrapt Events von swingcalendar.com"""
    logger.info("Starte Scraping: swingcalendar.com")
    events = []
    
    base_url = "https://swingcalendar.com"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        # Deutsche Version
        response = requests.get(f"{base_url}/de", headers=headers, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Event-Container finden
        event_containers = soup.find_all(['article', 'div'], class_=re.compile(r'event|calendar'))
        
        if not event_containers:
            event_containers = soup.find_all('div', class_='item')
        
        logger.info(f"Gefunden: {len(event_containers)} Event-Container")
        
        for container in event_containers:
            try:
                # Titel
                title_elem = container.find(['h2', 'h3', 'h4'])
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                if not title or len(title) < 3:
                    continue
                
                # Datum
                date_text = container.get_text()
                date = extract_date_from_text(date_text)
                
                if not date:
                    continue
                
                # Stadt
                city = ""
                location_elem = container.find(string=re.compile(r'(Berlin|Dresden|Leipzig|München|Hamburg|Köln|Frankfurt|Wien|Zürich|London|Paris|Rom|Madrid|Prag|Amsterdam|Brüssel|Stockholm|Oslo|Helsinki|Kopenhagen)'))
                if location_elem:
                    for city_name in ['Berlin', 'Dresden', 'Leipzig', 'München', 'Hamburg', 'Köln', 'Frankfurt', 'Wien', 'Zürich', 'London', 'Paris', 'Rom', 'Madrid', 'Prag', 'Amsterdam', 'Brüssel', 'Stockholm', 'Oslo', 'Helsinki', 'Kopenhagen']:
                        if city_name in location_elem:
                            city = city_name
                            break
                
                # Beschreibung
                desc = container.get_text(strip=True)
                if len(desc) > 300:
                    desc = desc[:300] + "..."
                
                # URL
                url = base_url + "/de"
                link_elem = container.find('a', href=True)
                if link_elem:
                    url = urljoin(base_url, link_elem['href'])
                
                # Genres
                genres = ["Swing"]
                title_lower = title.lower()
                desc_lower = desc.lower()
                
                if "lindy hop" in title_lower or "lindy hop" in desc_lower:
                    genres.append("Lindy Hop")
                if "balboa" in title_lower or "balboa" in desc_lower:
                    genres.append("Balboa")
                if "charleston" in title_lower or "charleston" in desc_lower:
                    genres.append("Charleston")
                if "blues" in title_lower or "blues" in desc_lower:
                    genres.append("Blues")
                if "shag" in title_lower or "shag" in desc_lower:
                    genres.append("Shag")
                
                event = {
                    "title": title,
                    "date": date,
                    "city": city,
                    "desc": desc,
                    "url": url,
                    "genres": list(set(genres))
                }
                
                # Geocoding
                if city:
                    coords = geocode_city(city)
                    if coords:
                        event["lat"] = coords[0]
                        event["lon"] = coords[1]
                
                events.append(event)
                
            except Exception as e:
                logger.error(f"Fehler beim Verarbeiten eines Events: {e}")
                continue
        
        logger.info(f"swingcalendar.com: {len(events)} Events extrahiert")
        
    except Exception as e:
        logger.error(f"Fehler beim Scraping von swingcalendar.com: {e}")
    
    return events

def scrape_swing_in_dresden():
    """Scrapt Events von swingindd.com"""
    logger.info("Starte Scraping: swingindd.com")
    events = []
    
    base_url = "https://swingindd.com"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        # Regionale Swing Kalender
        response = requests.get(f"{base_url}/home/regionale-swing-kalender/", headers=headers, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Event-Container
        event_containers = soup.find_all(['article', 'div', 'li'], class_=re.compile(r'event|post|item'))
        
        if not event_containers:
            event_containers = soup.find_all('div', class_='entry-content')
        
        logger.info(f"Gefunden: {len(event_containers)} Event-Container")
        
        for container in event_containers:
            try:
                # Titel
                title_elem = container.find(['h2', 'h3', 'h4'])
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                if not title or len(title) < 3:
                    continue
                
                # Datum
                date_text = container.get_text()
                date = extract_date_from_text(date_text)
                
                if not date:
                    continue
                
                # Stadt (meist Dresden)
                city = "Dresden"
                
                # Beschreibung
                desc = container.get_text(strip=True)
                if len(desc) > 300:
                    desc = desc[:300] + "..."
                
                # URL
                url = base_url + "/home/regionale-swing-kalender/"
                link_elem = container.find('a', href=True)
                if link_elem:
                    url = urljoin(base_url, link_elem['href'])
                
                # Genres
                genres = ["Swing"]
                title_lower = title.lower()
                desc_lower = desc.lower()
                
                if "lindy hop" in title_lower or "lindy hop" in desc_lower:
                    genres.append("Lindy Hop")
                if "balboa" in title_lower or "balboa" in desc_lower:
                    genres.append("Balboa")
                if "charleston" in title_lower or "charleston" in desc_lower:
                    genres.append("Charleston")
                if "shag" in title_lower or "shag" in desc_lower:
                    genres.append("Shag")
                
                event = {
                    "title": title,
                    "date": date,
                    "city": city,
                    "desc": desc,
                    "url": url,
                    "genres": list(set(genres))
                }
                
                # Geocoding
                coords = geocode_city(city)
                if coords:
                    event["lat"] = coords[0]
                    event["lon"] = coords[1]
                
                events.append(event)
                
            except Exception as e:
                logger.error(f"Fehler beim Verarbeiten eines Events: {e}")
                continue
        
        logger.info(f"swingindd.com: {len(events)} Events extrahiert")
        
    except Exception as e:
        logger.error(f"Fehler beim Scraping von swingindd.com: {e}")
    
    return events

def remove_duplicates(events):
    """Entfernt Duplikate basierend auf Titel und Datum"""
    seen = set()
    unique_events = []
    
    for event in events:
        key = f"{event['title']}_{event['date']}_{event.get('city', '')}"
        if key not in seen:
            seen.add(key)
            unique_events.append(event)
    
    return unique_events

def sort_events_by_date(events):
    """Sortiert Events nach Datum"""
    def parse_date(date_str):
        try:
            # Versuche verschiedene Formate
            for fmt in ['%d.%m.%Y', '%d.%m.%y']:
                try:
                    return datetime.strptime(date_str, fmt)
                except:
                    continue
            return datetime.max
        except:
            return datetime.max
    
    return sorted(events, key=lambda e: parse_date(e['date']))

def main():
    """Hauptfunktion"""
    logger.info("=" * 60)
    logger.info("Starte Rockabilly Radar Event Scraper")
    logger.info("=" * 60)
    
    all_events = []
    
    # Alle Quellen scrapen
    all_events.extend(scrape_we_love_country())
    time.sleep(2)  # Pause zwischen Requests
    
    all_events.extend(scrape_swing_calendar())
    time.sleep(2)
    
    all_events.extend(scrape_swing_in_dresden())
    
    # Duplikate entfernen
    logger.info(f"Total Events vor Deduplikation: {len(all_events)}")
    all_events = remove_duplicates(all_events)
    logger.info(f"Total Events nach Deduplikation: {len(all_events)}")
    
    # Nach Datum sortieren
    all_events = sort_events_by_date(all_events)
    
    # Als JSON speichern
    output_file = 'events.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_events, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Events gespeichert in: {output_file}")
    logger.info("=" * 60)
    logger.info("Scraping abgeschlossen!")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()
