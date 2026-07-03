#!/usr/bin/env python3
"""DIAGNOSE: Zeigt was die Websites tatsächlich zurückgeben"""
import requests
from bs4 import BeautifulSoup

urls = {
    "WeLoveCountry": "https://www.we-love-country.de/1_term.php",
    "JukeboxStompers": "https://www.jukeboxstompers.de/index.php/veranstaltungen/veranstaltungskalender",
    "SwingCalendar": "https://swingcalendar.com/de",
    "SwingInDD": "https://swingindd.com/home/regionale-swing-kalender/"
}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

for name, url in urls.items():
    print(f"\n{'='*70}")
    print(f"{name}: {url}")
    print('='*70)
    try:
        r = requests.get(url, headers=headers, timeout=30)
        print(f"Status: {r.status_code}")
        print(f"Content-Length: {len(r.text)} Zeichen")
        
        soup = BeautifulSoup(r.text, "lxml")
        
        # Zähle alle relevanten Elemente
        tables = soup.find_all("table")
        divs_event = soup.find_all(["div","article","li"], class_=lambda c: c and any(x in str(c).lower() for x in ["event","calendar","item","post"]))
        all_divs = soup.find_all("div")
        trs = soup.find_all("tr")
        
        print(f"Tabellen: {len(tables)}")
        print(f"Event-Divs: {len(divs_event)}")
        print(f"Alle Divs: {len(all_divs)}")
        print(f"Tabellen-Reihen (tr): {len(trs)}")
        
        # Zeige erste 500 Zeichen des Textes
        text = soup.get_text(" ", strip=True)[:500]
        print(f"\nErster Text-Auszug:\n{text}")
        
        # Suche nach Datums-Mustern
        import re
        dates = re.findall(r'\d{2}\.\d{2}\.\d{4}', r.text)
        print(f"\nGefundene Daten (DD.MM.YYYY): {len(dates)}")
        if dates:
            print(f"Beispiele: {dates[:5]}")
            
    except Exception as e:
        print(f"FEHLER: {e}")

print("\n" + "="*70)
print("DIAGNOSE FERTIG - Bitte Ergebnisse prüfen!")
print("="*70)
