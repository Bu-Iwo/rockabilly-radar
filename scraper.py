import json
import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse

OUTPUT_FILE = 'events.json'
LOG_FILE = 'scraper_log.txt'

# Konfiguration
MIN_DATE = datetime(2026, 7, 1)   # Heute: 01.07.2026
MAX_DATE = datetime(2027, 12, 31) # Max. 1.5 Jahre voraus
REQUEST_TIMEOUT = 10
USER_AGENT = 'RockabillyRadarBot/1.0 (Event-Scraper)'

# Stabile, verifizierte Quellen (Stand 01.07.2026)
VERIFIED_SOURCES = [
    {
        "name": "Jukebox Stompers Kalender",
        "url": "https://www.jukeboxstompers.de/index.php/veranstaltungen/veranstaltungskalender",
        "type": "table"
    },
    {
        "name": "Rockabilly Radio Events",
        "url": "https://www.rockabillyradio.net/events/",
        "type": "general"
    }
]

# VIP Bands (nur echte, bekannte Szene-Bands)
VIP_BANDS = [
    "Ray Collins Hot Club", "The Firebirds", "Jumpin'Up", "Shotgun Jones",
    "Jukebox Stompers", "Boppin'B", "Restless", "Stray Cats", "Mad Sin",
    "Darrel Higham", "Si Cranstoun", "Kim Lenz", "Imelda May",
    "Rocky Sharpe", "The Baseballs", "Shakin' Stevens", "Matchbox"
]

# Strenge Genre-Keywords
GENRE_KEYWORDS = {
    'positive': [
        'rockabilly', 'rock\'n\'roll', 'rock and roll', 'rock n roll',
        '50er', '60er', 'fifties', 'sixties', 'teddy boy', 'greaser',
        'vintage', 'pin-up', 'pinup', 'psychobilly',
        'lindy hop', 'lindyhop', 'swing dance', 'jitterbug',
        'boogie woogie', 'boogie-woogie',
        'country', 'western swing', 'line dance', 'honky tonk',
        'rock\'n\'roll tanz', 'jive'
    ],
    'negative': [
        'techno', 'house', 'trance', 'edm', 'electronic', 'dubstep',
        'metal', 'death metal', 'punk', 'hardcore', 'grunge',
        'hip hop', 'hip-hop', 'rap', 'trap',
        'schlager', 'volksmusik', 'klassik', 'opera',
        'reggae', 'dub', 'ska', 'indie rock'
    ]
}

DATE_PATTERN = re.compile(r'\b(\d{1,2})\.(\d{1,2})\.(\d{4})\b')

def log(message):
    """Schreibt Log-Nachrichten in Datei und Console."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
