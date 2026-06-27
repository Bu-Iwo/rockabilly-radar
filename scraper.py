import json
import requests
from bs4 import BeautifulSoup
import time
import urllib.parse

def get_coordinates(city_name):
    """Holt die exakten Koordinaten für den Umkreis-Filter"""
    if not city_name:
        return 51.3396, 12.3731
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
    # Regionale Fallbacks, falls die API hakt
    if "zwönitz" in city_clean.lower(): return 50.6294, 12.8128
    if "zwickau" in city_clean.lower(): return 50.7189, 12.4961
    if "chemnitz" in city_clean.lower(): return 50.8333, 12.9167
    if "leipzig" in city_clean.lower(): return 51.3396, 12.3731
    return 51.3396, 12.3731

def run_radar_scraper():
    print("🤖 Multi-Quellen Rockabilly-Radar Roboter startet...")
    
    alle_events = [
        # Premium-Datenbank (Feste Events)
        {"title": "Summer Jamboree #27", "date": "01.08. - 09.08.2026", "location": "Senigallia Promenade", "city": "Senigallia", "lat": 43.7147, "lon": 13.2183, "desc": "Das größte Rockabilly-Festival Europas an der Adria (Italien).", "url": "https://www.summerjamboree.com", "type": "festival"},
        {"title": "Rhythm Riot 2026", "date": "15.11. - 19.11.2026", "location": "Pontins Camber Sands", "city": "Rye", "lat": 50.9324, "lon": 0.7941, "desc": "UKs legendärer Weekender. Weltspitze des Rhythm & Blues.", "url": "https://www.rhythmriot.com", "type": "festival"},
        {"title": "Firebirds Festival 2026", "date": "03.07. - 05.07.2026", "location": "Schloss Trebsen", "city": "Trebsen", "lat": 51.2892, "lon": 12.7558, "desc": "Das ultimative Rock'n'Roll-Wochenende in Sachsen!", "url": "https://www.firebirds-festival.de", "type": "festival"},
        {"title": "Walldorf Rock'n'Roll Weekender 2027", "date": "Mai 2027 (Pfingsten)", "location": "Waldintercamp Walldorf", "city": "Walldorf/Meiningen", "lat": 50.6122, "lon": 10.3789, "desc": "Kult-Weekender in Thüringen.", "url": "https://www.walldorf-weekender.net", "type": "festival"}
    ]

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    # -------------------------------------------------------------------------
    # LIVE-SCRAPING: YELLOW BOOGIE DANCERS ZWÖNITZ
    # -------------------------------------------------------------------------
    print("💃 Scrape Termine von Yellow Boogie Dancers Zwönitz...")
    try:
        boogie_url = "https://www.yellow-boogie-zwoenitz.de/"
        response = requests.get(boogie_url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            potenzielle_termine = soup.find_all(['p', 'div', 'tr', 'li'])
            found_boogie = 0
            for item in potenzielle_termine:
                text = item.text.strip()
                if ("2026" in text or "2027" in text) and any(x in text.lower() for x in ["party", "event", "auftritt", "turnier", "boogie"]):
                    lines = [l.strip() for l in text.split('\n') if l.strip()]
                    if len(lines) >= 1 and len(lines[0]) < 100:
                        lat, lon = get_coordinates("Zwönitz")
                        alle_events.append({
                            "title": f"Yellow Boogie Zwönitz: {lines[0][:40]}...",
                            "date": "Siehe Homepage",
                            "location": "Sachsen / Zwönitz",
                            "city": "Zwönitz",
                            "lat": lat,
                            "lon": lon,
                            "desc": "Veranstaltung der Yellow Boogie Dancers Zwönitz e.V.",
                            "url": boogie_url,
                            "type": "party"
                        })
                        found_boogie += 1
                        if found_boogie >= 5: break
            print("✅ Yellow Boogie Dancers integriert.")
    except Exception as e:
        print(f"⚠️ Fehler bei Yellow Boogie Dancers: {e}")

    # -------------------------------------------------------------------------
    # LIVE-SCRAPING: JUKEBOX STOMPERS LEIPZIG
    # -------------------------------------------------------------------------
    print("🕺 Scrape Termine von den Jukebox Stompers...")
    try:
        jukebox_url = "https://www.jukeboxstompers.de/"
        response = requests.get(jukebox_url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            potenzielle_termine = soup.find_all(['p', 'div', 'tr', 'li'])
            found_juke = 0
            for item in potenzielle_termine:
                text = item.text.strip()
                if ("2026" in text or "2027" in text) and any(x in text.lower() for x in ["party", "event", "auftritt", "meisterschaft", "rock", "boogie"]):
                    lines = [l.strip() for l in text.split('\n') if l.strip()]
                    if len(lines) >= 1 and len(lines[0]) < 100:
                        lat, lon = get_coordinates("Leipzig")
                        alle_events.append({
                            "title": f"Jukebox Stompers: {lines[0][:40]}...",
                            "date": "Siehe Homepage",
                            "location": "Raum Leipzig",
                            "city": "Leipzig",
                            "lat": lat,
                            "lon": lon,
                            "desc": "Event oder Auftritt der Jukebox Stompers.",
                            "url": jukebox_url,
                            "type": "party"
                        })
                        found_juke += 1
                        if found_juke >= 5: break
            print("✅ Jukebox Stompers integriert.")
    except Exception as e:
        print(f"⚠️ Fehler bei Jukebox Stompers: {e}")

    # -------------------------------------------------------------------------
    # LIVE-SCRAPING: GLOBALER ROCKABILLY-KALENDER
    # -------------------------------------------------------------------------
    print("🎸 Versuche globalen Rockabilly-Kalender anzuzapfen...")
    try:
        kalender_url = "https://www.rockabilly-kalender.de/"
        response = requests.get(kalender_url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            rows = soup.find_all(['tr', 'article', 'div'], class_=['event', 'entry', 'vcalendar'])
            for row in rows[:8]:
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
                        "desc": "Gig aus dem bundesweiten Kalender.",
                        "url": kalender_url,
                        "type": "gig"
                    })
            print("✅ Bundesweiter Kalender erfolgreich integriert.")
    except Exception as e:
        print(f"⚠️ Kalender-Scrape übersprungen.")

    # -------------------------------------------------------------------------
    # SPEICHERN
    # -------------------------------------------------------------------------
    gesehene_titel = set()
    einzigartige_events = []
    for ev in alle_events:
        if ev["title"] not in gesehene_titel:
            gesehene_titel.add(ev["title"])
            einzigartige_events.append(ev)

    with open('events.json', 'w', encoding='utf-8') as f:
        json.dump(einzigartige_events, f, ensure_ascii=False, indent=4)
    
    print(f"💾 Fertig! {len(einzigartige_events)} Events gesichert.")

if __name__ == "__main__":
    run_radar_scraper()
    
