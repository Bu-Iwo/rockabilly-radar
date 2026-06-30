import json
import requests
from bs4 import BeautifulSoup
import re
import time

# --- KONFIGURATION ---
OUTPUT_FILE = 'events.json'

# Bekannte VIP-Bands und Festivals (Manuelle Pflege ist bei Scraping oft nötig)
VIP_BANDS = [
    "Ray Collins Hot Club", "Ray Allen", "Class of 58", "The Firebirds",
    "Jumpin'Up", "The Nymonics", "The Trainyard Kings", "Shotgun Jones", 
    "Jukebox Stompers", "Boppin'B", "Cherry Casino", "The Baseballs",
    "Restless", "Matchbox", "Darrel Higham", "Mad Sin"
]

# Feste Top-Events (Diese werden immer hinzugefügt)
HARDCODED_EVENTS = [
    {
        "title": "Summer Jamboree 2026", 
        "date": "01.08. - 09.08.2026",
        "location": "Senigallia, Italien",
        "city": "Senigallia", 
        "lat": 43.7147, 
        "lon": 13.2183,
        "desc": "Das größte Rockabilly-Festival Europas.",
        "url": "https://www.summerjamboree.com"
    },
    {
        "title": "Firebirds Festival 2026", 
        "date": "03.07. - 05.07.2026",
        "location": "Kloster Nimbschen, Grimma",
        "city": "Grimma", 
        "lat": 51.2294, 
        "lon": 12.7561,
        "desc": "Rock'n'Roll im Kloster.",
        "url": "https://www.firebirds-festival.de"
    }
]

# Ziel-Webseiten zum Scannen
TARGETS = [
    {"name": "Noels Ballroom", "url": "https://noels-ballroom.de/", "city": "Leipzig"},
    {"name": "Tonelli's Leipzig", "url": "http://www.tonellis.de/programm.html", "city": "Leipzig"},
    {"name": "Tanzcafé Waldenburg", "url": "https://www.tanzcafe-waldenburg.de/", "city": "Waldenburg"}
]

def get_coords(city_name):
    """Holt GPS-Koordinaten für eine Stadt über OpenStreetMap."""
    try:
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={city_name}&limit=1"
        headers = {'User-Agent': 'RockabillyRadarBot/1.0'}
        resp = requests.get(url, headers=headers, timeout=5)
        data = resp.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except:
        pass
    return None, None

def clean_text(text):
    """Bereinigt Text von HTML-Resten und Menü-Einträgen."""
    if not text: return ""
    # Entferne sehr kurze Wörter und typischen Webseiten-Müll
    junk_words = ["home", "impressum", "datenschutz", "kontakt", "menu", "suche", "zum inhalt"]
    lower_text = text.lower()
    for word in junk_words:
        if word in lower_text and len(text) < 100: # Nur bei kurzen Texten streng sein
            return None
    return text.strip()

def run_scraper():
    print("🚀 Rockabilly Radar Scraper startet...")
    
    # Lade bestehende Events, um Duplikate zu vermeiden
    existing_events = []
    try:
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            existing_events = json.load(f)
    except:
        existing_events = []

    # Starte mit den Hardcoded Events
    new_events_list = list(HARDCODED_EVENTS)

    # Helper für Duplikat-Check
    def is_duplicate(title, date, url):
        for ev in existing_events:
            if ev.get('title') == title and ev.get('date') == date:
                return True
        for ev in new_events_list:
            if ev.get('title') == title and ev.get('date') == date:
                return True
        return False

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    for target in TARGETS:
        print(f"🔍 Prüfe: {target['name']}")
        try:
            resp = requests.get(target['url'], headers=headers, timeout=10)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                # Suche nach Datumsmustern (z.B. 12.05. oder 12. Mai)
                date_pattern = re.compile(r'\d{1,2}\.\d{1,2}\.?\s*(\d{2,4})?')
                
                # Wir suchen nach Absätzen oder Listenelementen
                elements = soup.find_all(['p', 'li', 'div'], class_=re.compile(r'event|termin|date|program'))
                if not elements:
                    elements = soup.find_all(['p', 'li']) # Fallback: Alle Absätze

                for el in elements:
                    text = el.get_text(separator=" ", strip=True)
                    clean_desc = clean_text(text)
                    
                    if not clean_desc or len(clean_desc) < 20:
                        continue
                    
                    # Prüfe ob Datum vorhanden
                    dates_found = date_pattern.findall(text)
                    if not dates_found:
                        # Wenn kein Datum, prüfe ob VIP-Band genannt wird
                        band_found = next((b for b in VIP_BANDS if b.lower() in text.lower()), None)
                        if not band_found:
                            continue
                        date_str = "Termin folgt"
                    else:
                        date_str = text[date_pattern.search(text).start():date_pattern.search(text).end()]

                    # Titel generieren
                    band_found = next((b for b in VIP_BANDS if b.lower() in text.lower()), None)
                    title = f"{band_found} @ {target['name']}" if band_found else f"Event @ {target['name']}"
                    
                    # Duplikat-Check
                    if not is_duplicate(title, date_str, target['url']):
                        lat, lon = get_coords(target['city'])
                        
                        new_event = {
                            "title": title,
                            "date": date_str,
                            "location": f"{target['name']}, {target['city']}",
                            "city": target['city'],
                            "lat": lat,
                            "lon": lon,
                            "desc": clean_desc[:150] + "...",
                            "url": target['url']
                        }
                        new_events_list.append(new_event)
                        print(f"   ✅ Neu gefunden: {title}")
            
            time.sleep(2) # Pause, um nicht geblockt zu werden

        except Exception as e:
            print(f"   ❌ Fehler bei {target['name']}: {e}")

    # Speichern
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_events_list, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Fertig! {len(new_events_list)} Events gespeichert.")

if __name__ == "__main__":
    run_scraper()
