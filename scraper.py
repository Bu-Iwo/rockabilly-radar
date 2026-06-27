import json
import requests
from bs4 import BeautifulSoup
import time
import urllib.parse

# [DEINE get_coordinates Funktion bleibt genau so wie sie ist - einfach hier oben lassen]
def get_coordinates(city_name):
    if not city_name: return 51.3396, 12.3731
    try:
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={urllib.parse.quote(city_name)}&limit=1"
        headers = {'User-Agent': 'RockabillyRadar-Bot-EuroEdition'}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        if data and len(data) > 0:
            return float(data[0]['lat']), float(data[0]['lon'])
    except: pass
    return 51.3396, 12.3731

def run_radar_scraper():
    print("🤖 Autarker Rockabilly-Radar Roboter startet...")
    alle_events = [
        {"title": "Summer Jamboree #27", "date": "August 2026", "gCalDates": "20260801T100000Z/20260809T220000Z", "location": "Senigallia Promenade", "city": "Senigallia", "lat": 43.7147, "lon": 13.2183, "desc": "Das größte Rockabilly-Festival Europas.", "url": "https://www.summerjamboree.com", "type": "festival"},
        {"title": "Rhythm Riot 2026", "date": "November 2026", "gCalDates": "20261115T120000Z/20261119T230000Z", "location": "Pontins Camber Sands", "city": "Rye", "lat": 50.9324, "lon": 0.7941, "desc": "UKs legendäres Weekender-Event.", "url": "https://www.rhythmriot.com", "type": "festival"},
        {"title": "Rock'n'Roll Cruise 2027", "date": "Oktober 2027", "gCalDates": "20271001T100000Z/20271008T220000Z", "location": "Mittelmeer-Kreuzfahrt", "city": "Genua", "lat": 44.4056, "lon": 8.9463, "desc": "Die legendäre Rock'n'Roll Kreuzfahrt.", "url": "https://www.rocknroll-cruise.de", "type": "festival"}
    ]

    print("🎸 Scrape Termine von den Jukebox Stompers Leipzig...")
    try:
        target_url = "https://www.jukeboxstompers.de/termine/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(target_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # NEU: Wir suchen nach allen Tabellenzeilen ODER Listenpunkten
            # Und wir lassen uns in den Logs ausgeben, wie viele wir finden
            eintraege = soup.find_all('tr') + soup.find_all('li')
            print(f"DEBUG: Habe insgesamt {len(eintraege)} potenzielle Elemente auf der Seite gefunden.")
            
            for item in eintraege:
                text = item.text.strip()
                # Check, ob der Text nach einem Termin aussieht (Datum-Muster prüfen)
                if len(text) > 10 and any(char.isdigit() for char in text[:5]):
                    # Einfache Extraktion: Alles in eine Liste
                    lines = [l.strip() for l in text.split('\n') if l.strip()]
                    
                    # Hier kannst du anpassen, wie er die Daten liest
                    if len(lines) >= 2:
                        datum = lines[0]
                        titel = lines[1]
                        ort = lines[2] if len(lines) > 2 else "Leipzig"
                        
                        lat, lon = get_coordinates(ort)
                        time.sleep(0.5)
                        
                        alle_events.append({
                            "title": f"Jukebox Stompers: {titel}",
                            "date": datum,
                            "location": ort,
                            "city": ort,
                            "lat": lat,
                            "lon": lon,
                            "url": target_url,
                            "type": "gig"
                        })
            print(f"✅ Verarbeitung beendet. Neue Events gefunden.")
    except Exception as e:
        print(f"⚠️ Fehler: {e}")

    with open('events.json', 'w', encoding='utf-8') as f:
        json.dump(alle_events, f, ensure_ascii=False, indent=4)
    print(f"💾 Fertig! Gesamtzahl: {len(alle_events)}")

if __name__ == "__main__":
    run_radar_scraper()
    
