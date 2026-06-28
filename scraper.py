import json
import requests
from bs4 import BeautifulSoup
import re

def run_free_smart_scraper():
    print("🤖 Radar-Autopilot: VIP-Bands & Wildcard-Detektiv aktiviert...")
    alle_events = []
    
    # Deine VIP-Bands (und ein paar Szene-Klassiker als Bonus)
    vip_bands = [
        "Ray Collins Hot Club", "Ray Allen", "Class of 58", "The Firebirds", 
        "Jumpin'Up", "Suffy Sand Rocats", "Suffy Sand Combo", "The Nymonics", 
        "The Trainyard Kings", "Elbonautics", "Shotgun Jones", "Jukebox Stompers", 
        "Yellow Boogie Dancers", "Boppin'B", "Cherry Casino", "The Baseballs", 
        "Restless", "Matchbox", "Darrel Higham"
    ]
    
    # 1. FESTE GROSSE EVENTS (Mit präzisen Adressen)
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
            "location": "Schloss Trebsen, Zum Schloss 1, 04687 Trebsen/Mulde", 
            "city": "Trebsen", "lat": 51.2892, "lon": 12.7558, 
            "desc": "Das ultimative Rock'n'Roll-Wochenende in Sachsen!", 
            "url": "https://www.firebirds-festival.de"
        },
        {
            "title": "Rhythm Riot 2026", "date": "15.11. - 19.11.2026", 
            "location": "Pontins Camber Sands Holiday Park, New Lydd Rd, Camber, Rye TN31 7RL, UK", 
            "city": "Rye", "lat": 50.9324, "lon": 0.7941, 
            "desc": "UKs legendärer Weekender. Weltspitze des Rhythm & Blues.", 
            "url": "https://www.rhythmriot.com"
        },
        {
            "title": "Walldorf Rock'n'Roll Weekender 2027", "date": "Mai 2027 (Pfingsten)", 
            "location": "Waldintercamp Walldorf, Melkerser Str. 1, 98617 Meiningen", 
            "city": "Walldorf", "lat": 50.6122, "lon": 10.3789, 
            "desc": "Kult-Weekender in Thüringen.", 
            "url": "https://www.walldorf-weekender.net"
        }
    ]
    alle_events.extend(feste_events)

    # 2. LOCATIONS MIT FESTEN ADRESSEN
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    targets = [
        {"name": "Tonelli's Leipzig", "url": "http://www.tonellis.de/programm.html", "city": "Leipzig", "address": "Neumarkt 9, 04109 Leipzig", "lat": 51.3396, "lon": 12.3731},
        {"name": "Gaststätte zur Seilbahn", "url": "https://www.zur-seilbahn.de/", "city": "Leipzig", "address": "Max-Liebermann-Straße 103, 04157 Leipzig", "lat": 51.3731, "lon": 12.3711},
        {"name": "Noels Ballroom", "url": "https://noels-ballroom.de/", "city": "Leipzig", "address": "Karl-Liebknecht-Straße 48, 04275 Leipzig", "lat": 51.3255, "lon": 12.3739},
        {"name": "Tanzcafé Waldenburg", "url": "https://www.tanzcafe-waldenburg.de/", "city": "Waldenburg", "address": "Altenburger Str. 44, 09399 Waldenburg", "lat": 50.8787, "lon": 12.6033},
        {"name": "Lady Yule", "url": "https://www.ladyyule.de/", "city": "Dresden", "address": "Münzgasse 2, 01067 Dresden", "lat": 51.0514, "lon": 13.7415},
        {"name": "Jukebox Stompers (Home)", "url": "https://www.jukeboxstompers.de/", "city": "Leipzig", "address": "Veranstaltungsort siehe Beschreibung", "lat": 51.3396, "lon": 12.3731}
    ]

    date_pattern = re.compile(r'\b\d{1,2}\.\d{1,2}\.?(?:\d{2,4})?\b')
    keywords = ['live', 'band', 'konzert', 'rockabilly', 'boogie', 'rock', 'party', 'auftritt', 'veranstaltung', 'gig']
    
    # Muster für unbekannte Bands (Sucht nach "Live:" oder "Band:")
    wildcard_pattern = re.compile(r'(?:live|band)[\s:]+([A-Z][a-zA-Z0-9\'\s]{3,25})', re.IGNORECASE)

    for target in targets:
        try:
            print(f"🔍 Scanne {target['name']}...")
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
                            clean_text = text.replace('\n', ' ').strip()
                            
                            # KREUZSUCHE 1: Ist es eine VIP Band?
                            match_band = None
                            for band in vip_bands:
                                if band.lower() in text_lower:
                                    match_band = band
                                    break
                            
                            # KREUZSUCHE 2: Wenn keine VIP Band, schnappt der Wildcard-Detektiv eine unbekannte Band?
                            if not match_band:
                                wildcard_match = wildcard_pattern.search(clean_text)
                                if wildcard_match:
                                    match_band = wildcard_match.group(1).strip()
                            
                            # Titel dynamisch anpassen
                            if match_band:
                                event_title = f"🎸 {match_band} @ {target['name']}"
                            else:
                                event_title = f"{target['name']} Event"
                            
                            alle_events.append({
                                "title": event_title,
                                "date": event_date,
                                "location": f"{target['name']}, {target['address']}",
                                "city": target['city'],
                                "lat": target.get("lat"),
                                "lon": target.get("lon"),
                                "desc": clean_text,
                                "url": target['url']
                            })
                            gefunden += 1
                            if gefunden >= 6:
                                break
                                
                if gefunden == 0 and "Home" not in target['name']:
                    alle_events.append({
                        "title": f"Radar: {target['name']}",
                        "date": "Programm prüfen",
                        "location": f"{target['name']}, {target['address']}",
                        "city": target['city'],
                        "lat": target.get("lat"),
                        "lon": target.get("lon"),
                        "desc": "Checke die Website direkt für kurzfristige Gigs.",
                        "url": target['url']
                    })
        except Exception as e:
            print(f"⚠️ Fehler bei {target['name']}: {e}")

    # Speichern
    with open('events.json', 'w', encoding='utf-8') as f:
        json.dump(alle_events, f, ensure_ascii=False, indent=4)
    print(f"💾 Fertig! {len(alle_events)} Einträge inkl. Bands gesichert.")

if __name__ == "__main__":
    run_free_smart_scraper()
    
