import json
import requests
from bs4 import BeautifulSoup

def run_radar_scraper():
    print("🤖 Autopilot startet...")
    alle_events = []
    
    # Die Seiten, die wir abfragen. 
    # Wir nutzen hier echte Browser-Header, damit die Seiten uns nicht blockieren.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
        'Connection': 'keep-alive',
    }

    targets = [
        {"name": "Tonelli's Leipzig", "url": "http://www.tonellis.de/programm.html"},
        {"name": "Noels Ballroom", "url": "https://noels-ballroom.de/"},
        {"name": "Tanzcafé Waldenburg", "url": "https://www.tanzcafe-waldenburg.de/"}
    ]

    for target in targets:
        try:
            response = requests.get(target['url'], headers=headers, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Wir suchen nach allen Überschriften und Listenpunkten, 
                # wo Termine stehen könnten
                content = soup.get_text(separator=' ', strip=True)[:500] 
                alle_events.append({
                    "title": target['name'],
                    "date": "Automatischer Scan",
                    "location": target['name'],
                    "desc": content,
                    "url": target['url']
                })
        except Exception as e:
            print(f"Fehler bei {target['name']}: {e}")

    with open('events.json', 'w', encoding='utf-8') as f:
        json.dump(alle_events, f, ensure_ascii=False, indent=4)
    print("💾 Automatisches Update beendet.")

if __name__ == "__main__":
    run_radar_scraper()
