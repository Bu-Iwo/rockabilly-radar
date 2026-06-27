import json
import requests
from bs4 import BeautifulSoup
import time
import urllib.parse

def get_coordinates(city_name):
    """Holt die exakten Koordinaten für jeden Veranstaltungsort über OpenStreetMap"""
    if not city_name:
        return 51.3396, 12.3731 # Standard-Fallback: Leipzig
    try:
        # Nominatim API verlangt einen eindeutigen User-Agent
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={urllib.parse.quote(city_name)}&limit=1"
        headers = {'User-Agent': 'RockabillyRadar-Bot-EuroEdition'}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        if data and len(data) > 0:
            return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print(f"🌍 Ortung fehlgeschlagen für {city_name}: {e}")
    return 51.3396, 12.3731 # Fallback Leipzig

def run_radar_scraper():
    print("🤖 Autarker Rockabilly-Radar Roboter startet...")
    
    # Hier sammeln wir alle Gigs
    alle_events = []
    
    # -------------------------------------------------------------------------
    # SEKTION 1: DIE EUROPA-HIGHLIGHTS (Feste Basis-Einträge)
    # -------------------------------------------------------------------------
    euro_highlights = [
        {
            "title": "Summer Jamboree #27",
            "date": "August 2026",
            "gCalDates": "20260801T100000Z/20260809T220000Z",
            "location": "Senigallia Promenade",
            "city": "Senigallia",
            "lat": 43.7147,
            "lon": 13.2183,
            "desc": "Das größte Rockabilly-Festival Europas an der adriatischen Küste Italiens. 50s Musik, US-Cars und Tiki-Bars!",
            "url": "https://www.summerjamboree.com",
            "type": "festival"
        },
        {
            "title": "Rhythm Riot 2026",
            "date": "November 2026",
            "gCalDates": "20261115T120000Z/20261119T230000Z",
            "location": "Pontins Camber Sands",
            "city": "Rye",
            "lat": 50.9324,
            "lon": 0.7941,
            "desc": "UKs legendäres Weekender-Event. Die absolute Weltspitze des Rhythm & Blues und Rock'n'Roll unter einem Dach.",
            "url": "https://www.rhythmriot.com",
            "type": "festival"
        },
        {
            "title": "Rock'n'Roll Cruise 2027 (mit den Firebirds)",
            "date": "Oktober 2027",
            "gCalDates": "20271001T100000Z/20271008T220000Z",
            "location": "Mittelmeer-Kreuzfahrt",
            "city": "Genua",
            "lat": 44.4056,
            "lon": 8.9463,
            "desc": "Die legendäre Rock'n'Roll Kreuzfahrt im Herbst 2027. Mit den Firebirds und hochkarätigen internationalen Szene-Bands live an Bord!",
            "url": "https://www.rocknroll-cruise.de",
            "type": "festival"
        }
    ]
    alle_events.extend(euro_highlights)

    # -------------------------------------------------------------------------
    # SEKTION 2: LIVE-SCRAPING JUKEBOX STOMPERS LEIPZIG
    # -------------------------------------------------------------------------
    print("🎸 Scrape Termine von den Jukebox Stompers Leipzig...")
    try:
        # Die offizielle Termin-Sektion der Jukebox Stompers
        target_url = "https://www.jukeboxstompers.de/termine/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(target_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Der Roboter durchsucht die typischen Tabellen/Einträge auf der WordPress-Seite
            # Er findet jeden Termin-Block einzeln
            termin_eintraege = soup.find_all('tr', class_='vcalendar') or soup.find_all('div', class_='event-item') or soup.find_all('tr')
            
            for item in termin_eintraege:
                try:
                    # Textbausteine säubern
                    text = item.text.strip()
                    if not text or "keine termine" in text.lower():
                        continue
                        
                    # Filter: Nur Zeilen nehmen, die nach einem echten Event aussehen
                    lines = [l.strip() for l in text.split('\n') if l.strip()]
                    if len(lines) >= 2:
                        datum = lines[0] # Meistens steht das Datum vorn oder oben
                        titel = lines[1] # Der Name des Events/Auftritts
                        ort = lines[2] if len(lines) > 2 else "Leipzig"
                        
                        # "Abgesagt"-Schutzschalter
                        if "abgesagt" in titel.lower() or "ausfall" in titel.lower():
                            continue
                        
                        # Stadt für das GPS isolieren (nimmt das letzte Wort aus der Ortsangabe)
                        stadt = ort.split(',')[-1].strip().split(' ')[-1]
                        
                        # Roboter holt sich die genauen Koordinaten für den Umkreis-Filter auf dem Handy
                        lat, lon = get_coordinates(stadt)
                        
                        # Kurze Pause, um die OpenStreetMap-Server nicht zu überlasten
                        time.sleep(1)
                        
                        alle_events.append({
                            "title": f"Jukebox Stompers: {titel}",
                            "date": datum,
                            "gCalDates": "20260701T180000Z/20260701T220000Z", # Standard-Dummy für Google Kalender
                            "location": ort,
                            "city": stadt,
                            "lat": lat,
                            "lon": lon,
                            "desc": f"Live-Auftritt / Event mit den Jukebox Stompers aus Leipzig. Aktuelle Infos direkt auf deren Homepage.",
                            "url": "https://www.jukeboxstompers.de/termine/",
                            "type": "gig"
                        })
                except Exception as inner_e:
                    continue
            print(f"✅ Jukebox Stompers erfolgreich verarbeitet ({len(alle_events) - len(euro_highlights)} Termine gefunden).")
    except Exception as e:
        print(f"⚠️ Fehler beim Auslesen der Jukebox Stompers: {e}")

    # -------------------------------------------------------------------------
    # SEKTION 3: SPEICHERN DER DATEN
    # -------------------------------------------------------------------------
    with open('events.json', 'w', encoding='utf-8') as f:
        json.dump(alle_events, f, ensure_ascii=False, indent=4)
    
    print(f"💾 Fertig! Insgesamt {len(alle_events)} Euro- & Regional-Events autonom gesichert.")

if __name__ == "__main__":
    run_radar_scraper()
