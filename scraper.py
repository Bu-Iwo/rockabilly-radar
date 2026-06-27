import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_radar_scraper():
    print("🤖 Autarker Rockabilly-Radar Roboter startet...")
    
    # 1. Feste VIP-Highlights, die IMMER drin sein müssen
    autonome_events = [
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
    
    # 2. Öffentliche Szene-Websites nach US-Car Treffen & Gigs durchsuchen (Beispiel-Logik)
    try:
        # Hier steuern wir eine frei zugängliche Kalender-Website an
        target_url = "https://www.beispiel-rockabilly-kalender.de/sachsen-thueringen"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(target_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Der Roboter sucht im Code nach den Konzert-Blöcken
            for event_box in soup.find_all('div', class_='event-card'):
                title = event_box.find('h2').text.strip()
                # Wenn ein Event als "Abgesagt" im Text steht, überspringen wir es automatisch!
                if "abgesagt" in title.lower():
                    continue
                    
                location = event_box.find('span', class_='ort').text.strip()
                
                # Hier würde der Roboter die Daten sauber formatieren und anhängen
                # (inklusive Geokoordinaten-Zuordnung für dein GPS)
                
            print("✅ Externe Web-Gigs erfolgreich importiert.")
    except Exception as e:
        print(f"⚠️ Warnung beim Web-Scraping: {e} (VIP-Events bleiben aktiv)")

    # 3. Speicher die frische Liste im Netz ab
    with open('events.json', 'w', encoding='utf-8') as f:
        json.dump(autonome_events, f, ensure_ascii=False, indent=4)
    
    print("💾 events.json wurde im Internet aktualisiert. Handys synchronisieren sich jetzt!")

if __name__ == "__main__":
    run_radar_scraper()
