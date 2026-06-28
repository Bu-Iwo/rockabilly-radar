import json
import requests
from bs4 import BeautifulSoup
import re

def run_free_smart_scraper():
    print("🤖 Zero-Cost 'Sniper' Scraper startet...")
    alle_events = []
    
    # Tarnung, damit wir nicht blockiert werden
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    targets = [
        {"name": "Tonelli's Leipzig", "url": "http://www.tonellis.de/programm.html", "city": "Leipzig"},
        {"name": "Noels Ballroom", "url": "https://noels-ballroom.de/", "city": "Leipzig"},
        {"name": "Tanzcafé Waldenburg", "url": "https://www.tanzcafe-waldenburg.de/", "city": "Waldenburg"},
        {"name": "Lady Yule", "url": "https://www.ladyyule.de/", "city": "Dresden"}
    ]

    # Der "Detektiv": Sucht nach Datumsformaten wie 12.08. oder 12.08.2026
    date_pattern = re.compile(r'\b\d{1,2}\.\d{1,2}\.?(?:\d{2,4})?\b')
    
    # Signalwörter, die auf eine Party hindeuten
    keywords = ['live', 'band', 'konzert', 'rockabilly', 'boogie', 'rock', 'party', 'auftritt', 'veranstaltung']

    for target in targets:
        try:
            print(f"🔍 Scanne {target['name']}...")
            response = requests.get(target['url'], headers=headers, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Wir durchsuchen alle Absätze, Listen und Tabellen
                elements = soup.find_all(['p', 'li', 'div', 'td'])
                gefunden = 0
                
                for el in elements:
                    text = el.get_text(separator=' ', strip=True)
                    text_lower = text.lower()
                    
                    # Wenn ein Datum UND ein Signalwort im selben Satz stehen
                    if date_pattern.search(text) and any(kw in text_lower for kw in keywords):
                        # Text darf nicht extrem lang sein (sonst ist es ein ganzer Artikel)
                        if 15 < len(text) < 300: 
                            # Datum extrahieren
                            found_dates = date_pattern.findall(text)
                            event_date = found_dates[0] if found_dates else "Demnächst"
                            
                            # Text bereinigen für die App
                            clean_text = text.replace('\n', ' ').strip()
                            
                            alle_events.append({
                                "title": f"{target['name']} Event",
                                "date": event_date,
                                "location": target['name'],
                                "city": target['city'],
                                "desc": clean_text,
                                "url": target['url']
                            })
                            gefunden += 1
                            
                            # Max 4 Termine pro Location, damit die App nicht überflutet wird
                            if gefunden >= 4: 
                                break
                
                # Falls er keine genauen Daten findet, packen wir den direkten Link rein
                if gefunden == 0:
                    alle_events.append({
                        "title": f"Radar: {target['name']}",
                        "date": "Regelmäßig",
                        "location": target['name'],
                        "city": target['city'],
                        "desc": "Checke die Website für aktuelle Gigs.",
                        "url": target['url']
                    })

        except Exception as e:
            print(f"⚠️ Fehler bei {target['name']}: {e}")

    # Zum Schluss die Facebook-Bands und den Google-Kalender als Dauer-Links hinzufügen
    dauer_links = [
        {"name": "Jukebox Stompers (Events)", "url": "https://share.google/a892eE4QQbXLEXA4q", "city": "Leipzig"},
        {"name": "Elbonautics (Band)", "url": "https://www.facebook.com/elbonautics/", "city": "Leipzig"},
        {"name": "Shotgun Jones (Band)", "url": "https://www.facebook.com/ShotgunJonesBand/", "city": "Leipzig"}
    ]
    for dl in dauer_links:
        alle_events.append({
            "title": f"Band/Kalender: {dl['name']}",
            "date": "Immer aktuell",
            "location": dl['name'],
            "city": dl['city'],
            "desc": "Direktlink zur Seite.",
            "url": dl['url']
        })

    with open('events.json', 'w', encoding='utf-8') as f:
        json.dump(alle_events, f, ensure_ascii=False, indent=4)
    print(f"💾 Fertig! {len(alle_events)} Einträge völlig kostenlos gesichert.")

if __name__ == "__main__":
    run_free_smart_scraper()
                            
