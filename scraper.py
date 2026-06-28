import json
import requests
from bs4 import BeautifulSoup
import re

def run_free_smart_scraper():
    print("🤖 Radar-Autopilot: Update läuft...")
    alle_events = []
    
    vip_bands = [
        "Ray Collins Hot Club", "Ray Allen", "Class of 58", "The Firebirds", 
        "Jumpin'Up", "Suffy Sand Rocats", "Suffy Sand Combo", "The Nymonics", 
        "The Trainyard Kings", "Elbonautics", "Shotgun Jones", "Jukebox Stompers", 
        "Yellow Boogie Dancers", "Boppin'B", "Cherry Casino", "The Baseballs", 
        "Restless", "Matchbox", "Darrel Higham"
    ]
    
    # 1. FESTE GROSSE EVENTS (Firebirds korrigiert)
    feste_events = [
        {
            "title": "Summer Jamboree #27", "date": "01.08. - 09.08.2026", 
            "location": "Foro Annonario & Promenade, 60019 Senigallia (AN), Italien", 
            "city": "Senigallia", "lat": 43.7147, "lon": 13.2183, 
            "desc": "Das größte Rockabilly-Festival Europas an der Adria.", 
            "url": "https://www.summerjamboree.com"
        },
        {
            "title": "Firebirds Festival 2026", "date": "03.07. - 05.07.2026", 
            "location": "Kloster Nimbschen, Nimbschener Landstraße 1, 04668 Grimma", 
            "city": "Grimma", "lat": 51.2294, "lon": 12.7561, 
            "desc": "Das ultimative Rock'n'Roll-Wochenende im Kloster Nimbschen!", 
            "url": "https://www.firebirds-festival.de"
        },
        {
            "title": "Rhythm Riot 2026", "date": "15.11. - 19.11.2026", 
            "location": "Pontins Camber Sands Holiday Park, New Lydd Rd, Camber, Rye TN31 7RL, UK", 
            "city": "Rye", "lat": 50.9324, "lon": 0.7941, 
            "desc": "UKs legendärer Weekender. Weltspitze des Rhythm & Blues.", 
            "url": "https://www.rhythmriot.com"
        }
    ]
    alle_events.extend(feste_events)

    # 2. TARGETS (Lady Yule entfernt)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    targets = [
        {"name": "Tonelli's Leipzig", "url": "http://www.tonellis.de/programm.html", "city": "Leipzig", "address": "Neumarkt 9, 04109 Leipzig", "lat": 51.3396, "lon": 12.3731},
        {"name": "Gaststätte zur Seilbahn", "url": "https://www.zur-seilbahn.de/", "city": "Leipzig", "address": "Max-Liebermann-Straße 103, 04157 Leipzig", "lat": 51.3731, "lon": 12.3711},
        {"name": "Noels Ballroom", "url": "https://noels-ballroom.de/", "city": "Leipzig", "address": "Karl-Liebknecht-Straße 48, 04275 Leipzig", "lat": 51.3255, "lon": 12.3739},
        {"name": "Tanzcafé Waldenburg", "url": "https://www.tanzcafe-waldenburg.de/", "city": "Waldenburg", "address": "Altenburger Str. 44, 09399 Waldenburg", "lat": 50.8787, "lon": 12.6033},
        {"name": "Jukebox Stompers (Home)", "url": "https://www.jukeboxstompers.de/", "city": "Leipzig", "address": "Veranstaltungsort siehe Beschreibung", "lat": 51.3396, "lon": 12.3731}
    ]

    date_pattern = re.compile(r'\b\d{1,2}\.\d{1,2}\.?(?:\d{2,4})?\b')
    keywords = ['live', 'band', 'konzert', 'rockabilly', 'boogie', 'rock', 'party', 'auftritt', 'veranstaltung', 'gig']
    wildcard_pattern = re.compile(r'(?:live|band)[\s:]+([A-Z][a-zA-Z0-9\'\s]{3,25})', re.IGNORECASE)

    for target in targets:
        try:
            response = requests.get(target['url'], headers=headers, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                elements = soup.find_all(['p', 'li', 'div', 'td', 'tr', 'h3', 'h4'])
                gefunden = 0
                for el in elements:
                    text = el.get_text(separator=' ', strip=True)
                    text_lower = text.lower()
                    if date_pattern.search(text) and any(kw in text_lower for kw in keywords):
                        if 10 < len(text) < 300:
                            found_dates = date_pattern.findall(text)
                            event_date = found_dates[0] if found_dates else "Demnächst"
                            match_band = next((b for b in vip_bands if b.lower() in text_lower), None)
                            if not match_band:
                                wc = wildcard_pattern.search(text)
                                if wc: match_band = wc.group(1).strip()
                            
                            alle_events.append({
                                "title": f"🎸 {match_band} @ {target['name']}" if match_band else f"{target['name']} Event",
                                "date": event_date,
                                "location": f"{target['name']}, {target['address']}",
                                "city": target['city'],
                                "desc": text.replace('\n', ' ').strip(),
                                "url": target['url']
                            })
                            gefunden += 1
                            if gefunden >= 6: break
        except Exception as e:
            print(f"Fehler bei {target['name']}: {e}")

    with open('events.json', 'w', encoding='utf-8') as f:
        json.dump(alle_events, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run_free_smart_scraper()
    
