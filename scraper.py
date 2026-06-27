import json
import requests
from bs4 import BeautifulSoup
import time
import urllib.parse

def get_coordinates(city_name):
    """Holt die exakten Koordinaten für den Umkreis-Filter auf dem Handy"""
    if not city_name:
        return 51.3396, 12.3731
    # Bereinigung für bekannte regionale Orte
    city_clean = city_name.split(',')[-1].strip().split(' ')[-1]
    try:
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={urllib.parse.quote(city_clean)}&limit=1"
        headers = {'User-Agent': 'RockabillyRadar-Bot-MultiEdition'}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        if data and len(data) > 0:
            return float(data[0]['lat']), float(data[0]['lon'])
    except:
        pass
    # Regionale Fallbacks, falls OSM mal dichtmacht
    if "zwönitz" in city_clean.lower(): return 50.6294, 12.8128
    if "zwickau" in city_clean.lower(): return 50.7189, 12.4961
    if "chemnitz" in city_clean.lower(): return 50.8333, 12.9167
    if "leipzig" in city_clean.lower(): return 51.3396, 12.3731
    return 51.3396, 12.3731

def run_radar_scraper():
    print("🤖 Multi-Quellen Rockabilly-Radar Roboter startet...")
    
    # -------------------------------------------------------------------------
    # SEKTION 1: DIE FESTE PREMIUM-DATENBANK (Festivals & Regionale Highlights 2026/2027)
    # -------------------------------------------------------------------------
    alle_events = [
        # Internationale Riesen
        {"title": "Summer Jamboree #27", "date": "01.08. - 09.08.2026", "location": "Senigallia Promenade", "city": "Senigallia", "lat": 43.7147, "lon": 13.2183, "desc": "Das größte Rockabilly-Festival Europas an der Adria (Italien).", "url": "https://www.summerjamboree.com", "type": "festival"},
        {"title": "Rhythm Riot 2026", "date": "15.11. - 19.11.2026", "location": "Pontins Camber Sands", "city": "Rye", "lat": 50.9324, "lon": 0.7941, "desc": "UKs legendärer Weekender. Weltspitze des Rhythm & Blues.", "url": "https://www.rhythmriot.com", "type": "festival"},
        {"title": "Rock'n'Roll Cruise 2027", "date": "01.10. - 08.10.2027", "location": "Mittelmeer-Kreuzfahrt mit den Firebirds", "city": "Genua", "lat": 44.4056, "lon": 8.9463, "desc": "Die legendäre Kreuzfahrt mit hochkarätigen Live-Bands an Bord.", "url": "https://www.rocknroll-cruise.de", "type": "festival"},
        
        # Mitteldeutsche Top-Events (Sachsen / Thüringen / Umland)
        {"title": "Firebirds Festival 2026", "date": "03.07. - 05.07.2026", "location": "Schloss Trebsen", "city": "Trebsen", "lat": 51.2892, "lon": 12.7558, "desc": "Das ultimative Rock'n'Roll-Wochenende in Sachsen! Live-Bands, Tanz-Workshops, US-Cars.", "url": "https://www.firebirds-festival.de", "type": "festival"},
        {"title": "Walldorf Rock'n'Roll Weekender 2027", "date": "Mai 2027 (Pfingsten)", "location": "Waldintercamp Walldorf", "city": "Walldorf/Meiningen", "lat": 50.6122, "lon": 10.3789, "desc": "Kult-Weekender in Thüringen. Hot Rods, Tätowierer und bester 50s Sound.", "url": "https://www.walldorf-weekender.net", "type": "festival"},
        {"title": "Rockabilly Convention 2026", "date": "August 2026", "location": "Event-Areal", "city": "Moosburg", "lat": 48.4669, "lon": 11.9383, "desc": "Großes Treffen der Szene mit Live-Musik, Markt und US-Cars.", "url": "https://www.rockabilly-convention.de", "type": "festival"},
        {"title": "Boogie Woogie & Rock'n'Roll Tanzabend", "date": "Regelmäßig Herbst 2026", "location": "Tanzzentrum Sachsen", "city": "Chemnitz", "lat": 50.8333, "lon": 12.9167, "desc": "Regionaler Social Dance für Rock'n'Roll und Boogie-Woogie Fans.", "url": "https://www.yellow-boogie-dancers.de", "type": "party"}
    ]

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    # -------------------------------------------------------------------------
    # SEKTION 2: LIVE-SCRAPING - YELLOW BOOGIE DANCERS
    # -------------------------------------------------------------------------
    print("💃 Scrape Termine von den Yellow Boogie Dancers Zwönitz...")
    try:
        boogie_url = "https://www.yellow-boogie-dancers.de/"
        # Wir versuchen die Hauptseite oder typische Unterseiten zu laden
        response = requests.get(boogie_url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extrem breiter Suchfilter, der nach Texten sucht, die "2026" oder "2027" enthalten
            potenzielle_termine = soup.find_all(['p', 'div', 'tr', 'li'])
            found_boogie = 0
            
            for item in potenzielle_termine:
                text = item.text.strip()
                if ("2026" in text or "2027" in text) and any(x in text.lower() for x in ["party", "event", "auftritt", "turnier", "boogie"]):
                    lines = [l.strip() for l in text.split('\n') if l.strip()]
                    if len(lines) >= 1 and len(lines[0]) < 100:
                        lat, lon = get_coordinates("Zwönitz")
                        alle_events.append({
                            "title": f"Yellow Boogie Event: {lines[0][:50]}",
                            "date": "Siehe Homepage",
                            "location": "Sachsen / Vereinsgelände",
                            "city": "Zwönitz",
                            "lat": lat,
                            "lon": lon,
                            "desc": f"Veranstaltung oder Kurs der Yellow Boogie Dancers e.V. Details direkt auf der Website.",
                            "url": boogie_url,
                            "type": "party"
                        })
                        found_boogie += 1
                        if found_boogie >= 5: break # Begrenzen, um Dubletten zu vermeiden
            print(f"✅ Yellow Boogie Dancers Routine beendet.")
    except Exception as e:
        print(f"⚠️ Fehler bei Yellow Boogie Dancers: {e}")

    # -------------------------------------------------------------------------
    # SEKTION 3: LIVE-SCRAPING - ALLGEMEINER ROCKABILLY-KALENDER DE
    # -------------------------------------------------------------------------
    print("🎸 Versuche globalen Rockabilly-Kalender anzuzapfen...")
    try:
        # Ein sehr stabiler, großer deutscher Fankalender
        kalender_url = "https://www.rockabilly-kalender.de/"
        response = requests.get(kalender_url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Sucht nach Tabellenzeilen oder Event-Containern
            rows = soup.find_all(['tr', 'article', 'div'], class_=['event', 'entry', 'vcalendar'])
            
            for row in rows[:8]: # Die nächsten 8 Top-Gigs abgreifen
                text = row.text.strip()
                lines = [l.strip() for l in text.split('\n') if l.strip()]
                if len(lines) >= 2:
                    datum = lines[0]
                    titel = lines[1]
                    ort = lines[2] if len(lines) > 2 else "Deutschland"
                    
                    lat, lon = get_coordinates(ort)
                    alle_events.append({
                        "title": titel,
                        "date": datum,
                        "location": ort,
                        "city": ort,
                        "lat": lat,
                        "lon": lon,
                        "desc": "Automatisch importierter Gig aus dem bundesweiten Rockabilly-Kalender.",
                        "url": kalender_url,
                        "type": "gig"
                    })
            print("✅ Bundesweiter Kalender erfolgreich integriert.")
    except Exception as e:
        print(f"⚠️ Kalender-Scrape übersprungen (Fallback aktiv): {e}")

    # -------------------------------------------------------------------------
    # SEKTION 4: SPEICHERN DER DATEN
    # -------------------------------------------------------------------------
    # Dubletten herausfiltern anhand des Titels
    gesehene_titel = set()
    einzigartige_events = []
    for ev in alle_events:
        if ev["title"] not in gesehene_titel:
            gesehene_titel.add(ev["title"])
            einzigartige_events.append(ev)

    with open('events.json', 'w', encoding='utf-8') as f:
        json.dump(einzigartige_events, f, ensure_ascii=False, indent=4)
    
    print(f"💾 Fertig! Insgesamt {len(einzigartige_events)} Events autonom gesichert und bereitgestellt.")

if __name__ == "__main__":
    run_radar_scraper()
                        
