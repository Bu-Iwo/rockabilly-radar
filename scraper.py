import json
import requests
from bs4 import BeautifulSoup
import re

def run_free_smart_scraper():
    print("🤖 Zero-Cost 'Sniper' Scraper startet (Komplett-Edition)...")
    alle_events = []
    
    # 1. FESTE GROSSE EVENTS (Die dürfen bei Updates nie verschwinden!)
    feste_events = [
        {"title": "Summer Jamboree #27", "date": "01.08. - 09.08.2026", "location": "Senigallia Promenade", "city": "Senigallia", "lat": 43.7147, "lon": 13.2183, "desc": "Das größte Rockabilly-Festival Europas an der Adria (Italien).", "url": "https://www.summerjamboree.com"},
        {"title": "Rhythm Riot 2026", "date": "15.11. - 19.11.2026", "location": "Pontins Camber Sands", "city": "Rye", "lat": 50.9324, "lon": 0.7941, "desc": "UKs legendärer Weekender. Weltspitze des Rhythm & Blues.", "url": "https://www.rhythmriot.com"},
        {"title": "Firebirds Festival 2026", "date": "03.07. - 05.07.2026", "location": "Schloss Trebsen", "city": "Trebsen", "lat": 51.2892, "lon": 12.7558, "desc": "Das ultimative Rock'n'Roll-Wochenende in Sachsen!", "url": "https://www.firebirds-festival.de"},
        {"title": "Walldorf Rock'n'Roll Weekender 2027", "date": "Mai 2027 (Pfingsten)", "location": "Waldintercamp Walldorf", "city": "Walldorf/Meiningen", "lat": 50.6122, "lon": 10.3789, "desc": "Kult-Weekender in Thüringen.", "url": "https://www.walldorf-weekender.net"},
        {"title": "Rock'n'Roll Cruise", "date": "Check Website", "location": "Schiff/Hafen", "city": "Kiel", "lat": 54.3233, "lon": 10.1394, "desc": "Die offizielle R'n'R Cruise auf hoher See.", "url": "https://www.rocknrollcruise.de/de/index.html"}
    ]
    # Wir fügen die festen Events sofort der Liste hinzu
    alle_events.extend(feste_events)

    # 2. DYNAMISCHES SCRAPING (Sucht nach einzelnen Terminen auf den Webseiten)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    # Die Seiten, die der Bot nach Datumsangaben durchschnüffelt
    targets = [
        {"name": "Tonelli's Leipzig", "url": "http://www.tonellis.de/programm.html", "city": "Leipzig", "lat": 51.3396, "lon": 12.3731},
        {"name": "Gaststätte zur Seilbahn", "url": "https://www.zur-seilbahn.de/", "city": "Leipzig", "lat": 51.3396, "lon": 12.3731},
        {"name": "Noels Ballroom", "url": "https://noels-ballroom.de/", "city": "Leipzig", "lat": 51.3396, "lon": 12.3731},
        {"name": "Tanzcafé Waldenburg", "url": "https://www.tanzcafe-waldenburg.de/", "city": "Waldenburg", "lat": 50.8787, "lon": 12.6033},
        {"name": "Lady Yule", "url": "https://www.ladyyule.de/", "city": "Dresden", "lat": 51.0504, "lon": 13.7373},
        # Hier holen wir jetzt die echten Termine von den Vereins-Webseiten:
        {"name": "Jukebox Stompers", "url": "https://www.jukeboxstompers.de/", "city": "Leipzig", "lat": 51.3396, "lon": 12.3731},
        {"name": "Yellow Boogie Dancers", "url": "https://www.yellow-boogie-zwoenitz.de/", "city": "Zwönitz", "lat": 50.6294, "lon": 12.8128}
    ]

    # Der Such-Filter für das Datum
    date_pattern = re.compile(r'\b\d{1,2}\.\d{1,2}\.?(?:\d{2,4})?\b')
    keywords = ['live', 'band', 'konzert', 'rockabilly', 'boogie', 'rock', 'party', 'auftritt', 'veranstaltung', 'meisterschaft', 'gig', 'stompers', 'termin']

    for target in targets:
        try:
            print(f"🔍 Scanne {target['name']}...")
            response = requests.get(target['url'], headers=headers, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                elements = soup.find_all(['p', 'li', 'div', 'td', 'tr', 'h3'])
                gefunden = 0
                
                for el in elements:
                    text = el.get_text(separator=' ', strip=True)
                    text_lower = text.lower()
                    
                    if date_pattern.search(text) and any(kw in text_lower for kw in keywords):
                        if 10 < len(text) < 300: 
                            found_dates = date_pattern.findall(text)
                            event_date = found_dates[0] if found_dates else "Demnächst"
                            clean_text = text.replace('\n', ' ').strip()
                            
                            alle_events.append({
                                "title": f"{target['name']} Event",
                                "date": event_date,
                                "location": target['name'],
                                "city": target['city'],
                                "lat": target.get("lat"),
                                "lon": target.get("lon"),
                                "desc": clean_text,
                                "url": target['url']
                            })
                            gefunden += 1
                            if gefunden >= 5: # Max 5 Termine pro Verein/Bar auslesen
                                break
                
                # Fallback
                if gefunden == 0:
                    alle_events.append({
                        "title": f"Radar: {target['name']}",
                        "date": "Siehe Homepage",
                        "location": target['name'],
                        "city": target['city'],
                        "lat": target.get("lat"),
                        "lon": target.get("lon"),
                        "desc": f"Hier aktuell nach Infos oder Terminen schauen.",
                        "url": target['url']
                    })
        except Exception as e:
            print(f"⚠️ Fehler bei {target['name']}: {e}")

    # 3. DAUER-LINKS (Bands, die primär auf Facebook sind)
    dauer_links = [
        {"name": "Elbonautics (Band)", "url": "https://www.facebook.com/elbonautics/", "city": "Leipzig", "lat": 51.3396, "lon": 12.3731},
        {"name": "Shotgun Jones (Band)", "url": "https://www.facebook.com/ShotgunJonesBand/", "city": "Leipzig", "lat": 51.3396, "lon": 12.3731}
    ]
    for dl in dauer_links:
        alle_events.append({
            "title": f"Band: {dl['name']}",
            "date": "Check Facebook",
            "location": dl['name'],
            "city": dl['city'],
            "lat": dl.get("lat"),
            "lon": dl.get("lon"),
            "desc": "Checke die Social Media Seite für die nächsten Gigs.",
            "url": dl['url']
        })

    with open('events.json', 'w', encoding='utf-8') as f:
        json.dump(alle_events, f, ensure_ascii=False, indent=4)
    print(f"💾 Fertig! {len(alle_events)} Einträge gesichert.")

if __name__ == "__main__":
    run_free_smart_scraper()
                    
