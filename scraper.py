import json
import requests
from bs4 import BeautifulSoup
import urllib.parse

def run_radar_scraper():
    print("🤖 Rockabilly-Radar: Dresden & Stompers Update...")
    alle_events = []
    
    # Deine Wunsch-Locations & Bands
    targets = [
        {"name": "Tonelli's Leipzig", "url": "http://www.tonellis.de/programm.html", "city": "Leipzig", "lat": 51.3396, "lon": 12.3731},
        {"name": "Gaststätte zur Seilbahn", "url": "https://www.zur-seilbahn.de/", "city": "Leipzig", "lat": 51.3396, "lon": 12.3731},
        {"name": "Tanzcafé Waldenburg", "url": "https://www.tanzcafe-waldenburg.de/", "city": "Waldenburg", "lat": 50.8787, "lon": 12.6033},
        {"name": "Lady Yule (Dresden)", "url": "https://www.ladyyule.de/", "city": "Dresden", "lat": 51.0504, "lon": 13.7373},
        {"name": "Jukebox Stompers (Events)", "url": "https://share.google/a892eE4QQbXLEXA4q", "city": "Leipzig", "lat": 51.3396, "lon": 12.3731},
        {"name": "Elbonautics (Band)", "url": "https://www.facebook.com/elbonautics/", "city": "Leipzig", "lat": 51.3396, "lon": 12.3731},
        {"name": "Shotgun Jones (Band)", "url": "https://www.facebook.com/ShotgunJonesBand/", "city": "Leipzig", "lat": 51.3396, "lon": 12.3731},
        {"name": "Noels Ballroom", "url": "https://noels-ballroom.de/", "city": "Leipzig", "lat": 51.3396, "lon": 12.3731}
    ]

    for target in targets:
        alle_events.append({
            "title": f"Radar: {target['name']}",
            "date": "Check Kalender",
            "location": target['name'],
            "city": target['city'],
            "lat": target['lat'],
            "lon": target['lon'],
            "desc": f"Direktlink zum Programm oder Social Media von {target['name']}.",
            "url": target['url'],
            "type": "venue"
        })

    # Speichern
    with open('events.json', 'w', encoding='utf-8') as f:
        json.dump(alle_events, f, ensure_ascii=False, indent=4)
    print("💾 Alle Favoriten (inkl. Jukebox Stompers) gesichert.")

if __name__ == "__main__":
    run_radar_scraper()
    
