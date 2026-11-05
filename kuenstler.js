/*
  ROCKABILLY RADAR – Künstlerliste (Stand 2026-11-05)

  Wofür diese Datei da ist:
  - Sie sammelt die Bands und Acts, die in unseren Terminen vorkommen, mit ihrer eigenen Homepage.
  - Die Pflege-Aufgabe soll später reihum die Terminseiten dieser Bands lesen: Termine bestätigen und neue Termine als Kandidaten melden.
  - Die App (index.html) lädt diese Datei NICHT. Sie wird nur von der Pflege-Aufgabe gelesen.
  - Es stehen nur öffentliche Angaben von Bands und Acts darin (Name und offizielle Seite).

  Felder je Eintrag:
  - name / alias: Name der Band und andere Schreibweisen
  - homepage: eigene Homepage, leer wenn noch nicht gefunden
  - lesbar: "offen" (noch nicht geprüft), "ja", "nein", "nur-facebook" (Facebook/Instagram sind nicht lesbar)
  - geprueft: Datum der letzten Prüfung (JJJJ-MM-TT), leer wenn noch nie
  - naechste: Datum, ab dem die Band wieder geprüft werden soll
  - termine: Anzahl Termine in unseren Daten (je höher, desto wichtiger)
  - terminseite: Adresse der Terminseite, falls getrennt von der Homepage
  - von: "nutzer" = Adresse stammt vom Nutzer (sicher), sonst aus Termin-Links (ungeprüft)
  - hinweis: Bemerkung zum Stand
  - ignorieren: Liste von Terminen (JJJJ-MM-TT), die der Nutzer abgelehnt hat. Die Pflege-Aufgabe meldet sie nicht wieder als Kandidaten.
*/
window.RR_KUENSTLER = {
 "stand": "2026-11-05",
 "eintraege": [
  {
   "name": "The Cashbags",
   "alias": [],
   "homepage": "https://atributetojohnnycash.com",
   "lesbar": "ja",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 18,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland",
    "Österreich"
   ],
   "hinweis": "Terminseite lesbar, alle Termine schon bei uns.",
   "terminseite": "https://www.atributetojohnnycash.com/termine",
   "von": "nutzer"
  },
  {
   "name": "Boppin' B",
   "alias": [],
   "homepage": "https://www.boppinb.de",
   "lesbar": "ja",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 3,
   "stil": [
    "Rockabilly",
    "Rock'n'Roll"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Live-Seite nennt nur Ticketportale (Eventim, Reservix, ADticket). Termine über Portale (Songkick, Eventim) suchen. Offen: Münster 30.04.2027 nicht bestätigt.",
   "terminseite": "https://www.boppinb.de/live",
   "von": "nutzer"
  },
  {
   "name": "Spunyboys",
   "alias": [],
   "homepage": "https://www.bandsintown.com/a/6046190-spunyboys",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Rock'n'Roll",
    "Rockabilly"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Bandsintown bekannt, noch nicht getestet (Nutzungsbedingungen prüfen).",
   "von": "nutzer"
  },
  {
   "name": "The Firebirds",
   "alias": [],
   "homepage": "https://www.the-firebirds.de",
   "lesbar": "nein",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Rock'n'Roll",
    "Rockabilly"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Seite sperrt automatisches Lesen (robots.txt). thefirebirds.com ist die ENGLISCHE Band, nicht verwechseln.",
   "von": "nutzer"
  },
  {
   "name": "Alan Power & the Aftershocks",
   "alias": [],
   "homepage": "https://alanpowerandtheaftershocks.com",
   "lesbar": "ja",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 0,
   "stil": [],
   "land": [],
   "hinweis": "Termine im Bereich TOUR der Startseite (Irland).",
   "terminseite": "https://alanpowerandtheaftershocks.com/home#tour",
   "von": "nutzer"
  },
  {
   "name": "Booze Bombs",
   "alias": [],
   "homepage": "http://www.boozebombs.de",
   "lesbar": "nein",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 0,
   "stil": [],
   "land": [],
   "hinweis": "Seite sperrt automatisches Lesen (robots.txt).",
   "von": "nutzer"
  },
  {
   "name": "Cat Lee King & His Cocks",
   "alias": [],
   "homepage": "https://www.facebook.com/catleekingandhiscocks/",
   "lesbar": "nur-facebook",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 0,
   "stil": [],
   "land": [],
   "hinweis": "Nur Facebook (nicht lesbar).",
   "von": "nutzer"
  },
  {
   "name": "Die Boogie Banausen",
   "alias": [],
   "homepage": "https://www.boogiebanausen.de",
   "lesbar": "ja",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 0,
   "stil": [],
   "land": [],
   "hinweis": "Seite zuletzt Januar 2026 aktualisiert, letzter Termin 26.09.2026.",
   "von": "nutzer"
  },
  {
   "name": "Doc Horn & the Hornbabes",
   "alias": [],
   "homepage": "https://dochornberlin.de",
   "lesbar": "ja",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 0,
   "stil": [],
   "land": [],
   "hinweis": "Termine stehen auf der Startseite.",
   "von": "nutzer"
  },
  {
   "name": "Dusty Dave & The Heart Attacks",
   "alias": [],
   "homepage": "https://dustydave.mystrikingly.com",
   "lesbar": "nein",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 0,
   "stil": [],
   "land": [],
   "hinweis": "Auf der Seite stehen keine Termine.",
   "von": "nutzer"
  },
  {
   "name": "Georgina Peach & The Savoys",
   "alias": [],
   "homepage": "https://www.facebook.com/georginapeachandthesavoys/",
   "lesbar": "nur-facebook",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 0,
   "stil": [],
   "land": [],
   "hinweis": "Nur Facebook (nicht lesbar).",
   "von": "nutzer"
  },
  {
   "name": "Imelda May",
   "alias": [],
   "homepage": "https://www.imeldamay.co.uk",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 0,
   "stil": [],
   "land": [],
   "hinweis": "Seitenabruf lieferte einen Fehler. Große Tour, meist UK/Irland.",
   "von": "nutzer"
  },
  {
   "name": "Jason Starday",
   "alias": [],
   "homepage": "https://www.facebook.com/jasonstarday/",
   "lesbar": "nur-facebook",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 0,
   "stil": [],
   "land": [],
   "hinweis": "Nur Facebook (nicht lesbar).",
   "von": "nutzer"
  },
  {
   "name": "Jumpin'up",
   "alias": [],
   "homepage": "https://www.jumpinup.it",
   "lesbar": "nein",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 0,
   "stil": [],
   "land": [],
   "hinweis": "Verweist nur auf Bandsintown, keine Termine auf der Seite.",
   "von": "nutzer"
  },
  {
   "name": "Ray Allen and Band",
   "alias": [],
   "homepage": "https://c-a-t-enterprises.de",
   "lesbar": "nein",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 0,
   "stil": [],
   "land": [],
   "hinweis": "Seite sperrt automatisches Lesen (robots.txt).",
   "von": "nutzer"
  },
  {
   "name": "Ray Black & The Flying Carpets",
   "alias": [],
   "homepage": "https://www.facebook.com/RayBlackAndTheFlyingCarpets/",
   "lesbar": "nur-facebook",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 0,
   "stil": [],
   "land": [],
   "hinweis": "Nur Facebook (nicht lesbar).",
   "von": "nutzer"
  },
  {
   "name": "Ray Collins' Hot Club",
   "alias": [],
   "homepage": "https://www.the-hot-club.com",
   "lesbar": "ja",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 0,
   "stil": [],
   "land": [],
   "hinweis": "Terminseite lesbar, 6 Termine bis Mai 2027.",
   "terminseite": "https://www.the-hot-club.com/tour_dates/",
   "von": "nutzer"
  },
  {
   "name": "Shotgun Jones",
   "alias": [],
   "homepage": "https://www.shotgunjones.de",
   "lesbar": "ja",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 0,
   "stil": [],
   "land": [],
   "hinweis": "Termine auf den Seiten konzerte-2026 und konzerte-2027. Abgelehnt: 05.12.2026 Thalheim, 05.06.2027 Marienberg (Bergmannstag).",
   "terminseite": "https://www.shotgunjones.de/konzerte-2027",
   "von": "nutzer",
   "ignorieren": [
    "2026-12-05",
    "2027-06-05"
   ]
  },
  {
   "name": "Si Cranstoun",
   "alias": [],
   "homepage": "https://www.sicranstoun.com",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 0,
   "stil": [],
   "land": [],
   "hinweis": "Terminliste liegt extern (Kurzlink bnds.us), noch nicht gelesen. Britischer Künstler.",
   "von": "nutzer"
  },
  {
   "name": "Suffy Sand RoCats",
   "alias": [],
   "homepage": "https://rocats.de",
   "lesbar": "ja",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 0,
   "stil": [],
   "land": [],
   "hinweis": "Terminseite lesbar, teils ohne Stadt oder Jahr.",
   "terminseite": "https://rocats.de/events/",
   "von": "nutzer"
  },
  {
   "name": "The B-Shakers",
   "alias": [],
   "homepage": "https://www.b-shakers.ch",
   "lesbar": "ja",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 0,
   "stil": [],
   "land": [],
   "hinweis": "Terminseite lesbar (Schweizer Band, viele Termine im Ausland).",
   "terminseite": "https://www.b-shakers.ch/index.php/gigs",
   "von": "nutzer"
  },
  {
   "name": "The Backyard Casanovas",
   "alias": [],
   "homepage": "https://www.facebook.com/thebackyardcasanovas/",
   "lesbar": "nur-facebook",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 0,
   "stil": [],
   "land": [],
   "hinweis": "Nur Facebook (nicht lesbar).",
   "von": "nutzer"
  },
  {
   "name": "The Rhythm Torpedoes",
   "alias": [],
   "homepage": "https://www.rhythm-torpedoes.com",
   "lesbar": "nein",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 0,
   "stil": [],
   "land": [],
   "hinweis": "Auf der Shows-Seite keine lesbaren Termine.",
   "von": "nutzer"
  },
  {
   "name": "The Tin Cans",
   "alias": [],
   "homepage": "https://www.facebook.com/p/The-Tin-Cans-100032892716623/",
   "lesbar": "nur-facebook",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 0,
   "stil": [],
   "land": [],
   "hinweis": "Nur Facebook (nicht lesbar).",
   "von": "nutzer"
  },
  {
   "name": "The Wyattchristmasfive",
   "alias": [],
   "homepage": "https://wyattchristmasfive.de",
   "lesbar": "ja",
   "geprueft": "2026-11-05",
   "naechste": "",
   "termine": 0,
   "stil": [],
   "land": [],
   "hinweis": "Terminseite lesbar, Termine bis Dezember 2027.",
   "terminseite": "https://wyattchristmasfive.de/termine/",
   "von": "nutzer"
  },
  {
   "name": "Die Cowboys",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 16,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "Rick Allen",
   "alias": [
    "Texas Roots",
    "Rick Allen & Chris S.",
    "Rick & Chris S.",
    "Rick Allen & DJ Olli",
    "Rick Allen Band"
   ],
   "homepage": "https://www.rick-allen-country.com",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 16,
   "stil": [
    "Country",
    "Rockabilly"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Purling Brooks",
   "alias": [],
   "homepage": "https://purlingbrooks.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 12,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Why Not Band",
   "alias": [],
   "homepage": "https://simon-saz.de/wnb/v3/?page_id=2",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 12,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Catch Trio",
   "alias": [
    "Catch XL",
    "Catch Trio feat. Beth",
    "Catch Trio feat. Kim Bennet"
   ],
   "homepage": "https://www.catch-country.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 11,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse gehört evtl. einem Lokal oder Veranstalter, nicht der Band. Bitte prüfen."
  },
  {
   "name": "Reach",
   "alias": [],
   "homepage": "http://www.reach-country.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 8,
   "stil": [
    "Country",
    "Rock'n'Roll"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "High Risk",
   "alias": [],
   "homepage": "https://high-risk-web.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 7,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Tom Rascal & The Lakeland Cowboys",
   "alias": [],
   "homepage": "https://lakelandcowboys.com",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 7,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Heartland Harmony",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 6,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "Yvonne",
   "alias": [
    "Jost & Doris Anklamm",
    "Thomas",
    "The Mountaineers",
    "Mike Strauss & Nashville Friends"
   ],
   "homepage": "http://www.western-saloon.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 6,
   "stil": [
    "Country",
    "Swing"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse gehört evtl. einem Lokal oder Veranstalter, nicht der Band. Bitte prüfen."
  },
  {
   "name": "Chris Angels & Miriam",
   "alias": [],
   "homepage": "https://chrisangelscountry.wixsite.com/my-site-1",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 5,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Country Friends",
   "alias": [],
   "homepage": "https://countryfriends-zirndorf.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 5,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "CountryBell",
   "alias": [],
   "homepage": "https://www.countrybell.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 5,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Four Roses",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 5,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "Lennebrothers Band",
   "alias": [
    "LenneBrothers Band"
   ],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 5,
   "stil": [
    "Country",
    "Rockabilly",
    "Rock'n'Roll",
    "Boogie"
   ],
   "land": [
    "Deutschland",
    "Großbritannien"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Nashville",
   "alias": [],
   "homepage": "https://www.nashville-band.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 5,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Rock'n Rodeo",
   "alias": [],
   "homepage": "https://www.rocknrodeo.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 5,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "The Forgotten Sons Of Ben Cartwright",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 5,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "Frank Martini & The Roaring Twenties",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 4,
   "stil": [
    "Swing",
    "Lindy Hop",
    "Charleston"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Paul & Eric Stowe",
   "alias": [],
   "homepage": "https://paulstowe.com",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 4,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Rattlesnake Torpedos",
   "alias": [],
   "homepage": "https://rattlesnake-saloon.com/rattlesnake-torpedos",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 4,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "B-Country-Boy",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 3,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "Copperhead Jack & Co",
   "alias": [],
   "homepage": "https://copperheadjack.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 3,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Country Company",
   "alias": [],
   "homepage": "https://www.country-company.eu",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 3,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Hee Haw Pickin' Band",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 3,
   "stil": [
    "Country",
    "Rockabilly"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "Huckleberry Five",
   "alias": [],
   "homepage": "https://www.ruediger-helbig.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 3,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Mountain Four",
   "alias": [],
   "homepage": "https://www.mountain-four.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 3,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Shakin' Cats",
   "alias": [],
   "homepage": "http://www.shakin-cats.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 3,
   "stil": [
    "Rock'n'Roll"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Silver Highway",
   "alias": [],
   "homepage": "https://silver-highway.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 3,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "The Jitterbug Bites",
   "alias": [],
   "homepage": "http://www.jitterbug-bites.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 3,
   "stil": [
    "Swing",
    "Lindy Hop",
    "Boogie"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "The Scotty Bullock Trio",
   "alias": [],
   "homepage": "https://scottybullocktrio.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 3,
   "stil": [
    "Country",
    "Rock'n'Roll",
    "Boogie",
    "Rockabilly"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Waylon Wyatt",
   "alias": [],
   "homepage": "https://www.waylonwyatt.com",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 3,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "BANDANA",
   "alias": [],
   "homepage": "https://www.bandana-music.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Becky Jay & Band",
   "alias": [],
   "homepage": "https://becky-jay.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Big S. Fullband",
   "alias": [],
   "homepage": "https://www.bigsmusic.com",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Bloodsucking Zombies from Outer Space",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Rockabilly"
   ],
   "land": [
    "Deutschland",
    "Österreich"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Bonny Tones",
   "alias": [],
   "homepage": "https://bonnytones.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country",
    "Rock'n'Roll"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Bud'n'Cellar",
   "alias": [],
   "homepage": "https://budncellar.live",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Cagey Strings",
   "alias": [],
   "homepage": "https://cageystrings.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country",
    "Rock'n'Roll"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Daniel T. Coates Trio & Saints & Sinners",
   "alias": [
    "Daniel T. Coates Band"
   ],
   "homepage": "https://danieltcoates.jimdofree.com",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Dasha",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "De Waltons",
   "alias": [],
   "homepage": "https://dewaltons.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Emily Ann Roberts",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Honky Tonk Five",
   "alias": [],
   "homepage": "https://honkytonkfive.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country",
    "Rockabilly",
    "Swing"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Jelly Roll",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Juke West & The Band",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Little Roadhouse",
   "alias": [],
   "homepage": "https://littleroadhouse.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Loose Moose Band",
   "alias": [],
   "homepage": "https://loose-moose-band.online",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Matt Lang",
   "alias": [],
   "homepage": "https://mattlangmusic.com",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Nicolle Rochelle",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Swing",
    "Lindy Hop",
    "Charleston"
   ],
   "land": [
    "Schweiz"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Pick Up Ramblers",
   "alias": [],
   "homepage": "http://pick-up-ramblers.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Reindeers",
   "alias": [],
   "homepage": "http://www.reindeers.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Rock'n'Roll",
    "Boogie"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Rita Wilson",
   "alias": [],
   "homepage": "https://www.eventim.de/artist/rita-wilson",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Simone & Ihr Flotter Dreier",
   "alias": [
    "Real Treat & Simone & Ihr Flotter Dreier"
   ],
   "homepage": "https://www.der-flotte-dreier.com",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Solitary Man",
   "alias": [],
   "homepage": "https://westernsaloon-okee-dokee.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Southern Hills",
   "alias": [],
   "homepage": "https://www.southernhillsband.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "The Big Five",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Swing",
    "Lindy Hop",
    "Charleston"
   ],
   "land": [
    "Schweiz"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "The Ridin' Dudes",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "The Washboard Union",
   "alias": [],
   "homepage": "https://www.thewashboardunion.com",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Truck Stop",
   "alias": [],
   "homepage": "https://www.truck-stop.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Two Faces",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Wild Country & Udo G.",
   "alias": [],
   "homepage": "https://wild-country-band.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 2,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "'Hofgenuss' Country Music",
   "alias": [],
   "homepage": "https://weingut-hillabrand.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "2U & Mi",
   "alias": [],
   "homepage": "https://www.2u-and-mi.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "4 Cash",
   "alias": [],
   "homepage": "https://www.4cash-band.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Alex Klein Band",
   "alias": [],
   "homepage": "https://www.alexklein.ch",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Schweiz"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "All in Tune",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "Andy Lee & His Rockin' Country Men",
   "alias": [],
   "homepage": "https://www.andylee.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country",
    "Rock'n'Roll"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Andy Nickel & Tom Rascal",
   "alias": [],
   "homepage": "https://linedancebang.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Angie & Hillbilly Deluxe",
   "alias": [],
   "homepage": "https://www.hillbillydeluxe.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country",
    "Rockabilly"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Aron King & His Ferriday Rockers",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country",
    "Rockabilly"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "Arron Walker & Chris Aron And The Croakers",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country",
    "Rock'n'Roll"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "Ashley McBride",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "B-Country-Boy & DJ André",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "Belmondos Tanzkappelle",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing",
    "Balboa"
   ],
   "land": [
    "Schweiz"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Big S",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Big S. Trio",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Big T. & Friends",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Bill Conlon & Juke West & The Band",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Österreich"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "Black Raven",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Rock'n'Roll",
    "Rockabilly"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Bourbon Street Stompers",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing",
    "Lindy Hop",
    "Charleston"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Brand New Dusty Boots",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "Buddy Dee & The Ghostriders",
   "alias": [],
   "homepage": "https://www.buddydee.ch",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Schweiz"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Buffalo Drive",
   "alias": [],
   "homepage": "https://www.buffalodrive.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Carter Faith",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Catch",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "CCR Tribute Band",
   "alias": [],
   "homepage": "https://www.ccr-tribute.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Chicago Swing Collective",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing",
    "Lindy Hop",
    "Balboa",
    "Charleston",
    "Shag"
   ],
   "land": [
    "Schweiz"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Christoph Wiatre & Ralph Schlunk",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing",
    "Lindy Hop"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Coniglio Connection",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing",
    "Lindy Hop",
    "Charleston"
   ],
   "land": [
    "Schweiz"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Cooper Alan",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Country Friends Duo",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Country Music Award",
   "alias": [],
   "homepage": "https://www.pullmancity.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Country Wochenende der NZ Bäbenger Wildsaue",
   "alias": [],
   "homepage": "https://www.mountainmusicband.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Countryholics",
   "alias": [],
   "homepage": "https://countryholics.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Dakota Train (Daisy Town)",
   "alias": [],
   "homepage": "https://www.daisytown-band.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Daniel Duspiwa Quartet",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing",
    "Lindy Hop",
    "Balboa",
    "Shag"
   ],
   "land": [
    "Schweiz"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Daniel T. Coates Band",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Daniel T. Coates Duo",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Dee Dee & The Bel Airs",
   "alias": [],
   "homepage": "https://www.deedeeandthebelairs.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country",
    "Rockabilly"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Doc Adams",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "Dr. Wisebrod's Swingboppers",
   "alias": [],
   "homepage": "https://shop.kinoweinheim.de/products/8-november-2026-11-uhr-matinee-mit-dr-wisebrod-s-swingboppers",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Drew Baldridge",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Dynamite Dudes",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country",
    "Rockabilly",
    "Rock'n'Roll",
    "Boogie"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Fairschärft",
   "alias": [],
   "homepage": "https://www.fairschaerft.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Federolfs Syncopators",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing",
    "Lindy Hop",
    "Charleston"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Flaggstaff",
   "alias": [],
   "homepage": "https://flaggstaff.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "George Hug Band & Martina Meier",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Schweiz"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Gudrun Lange & Kactus",
   "alias": [],
   "homepage": "https://www.gudrunlange-kactus.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Hagen Horn and his Little Big Band",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing",
    "Lindy Hop",
    "Balboa",
    "Blues"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Hard Travelin'",
   "alias": [],
   "homepage": "https://www.hardtravelin.com",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Head Over Heels",
   "alias": [],
   "homepage": "https://head-over-heels.ch",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Schweiz"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Hee Haw Pickin' Band mit Bill Conlon",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "Heiligensetzer Boogie Trio",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Boogie"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "IKS Bigband",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing",
    "Lindy Hop",
    "Balboa",
    "Blues"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Jack Baymoore",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Rock'n'Roll",
    "Rockabilly"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Jake Calypso Trio",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Rock'n'Roll",
    "Rockabilly"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Jeepers Creepers",
   "alias": [],
   "homepage": "https://www.jeeperscreepers.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Johnny Bee & Casey",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Johnny Ray",
   "alias": [],
   "homepage": "https://johnnyray-country.wixsite.com/countrymusic",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Jolina Carl & Der Wuppertiger",
   "alias": [],
   "homepage": "https://jolinacarl.com",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "JugendJazzOrchester Saar",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing",
    "Lindy Hop"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Kämmerling Jazz Quartett",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing",
    "Lindy Hop",
    "Balboa",
    "Charleston",
    "Blues",
    "Shag",
    "Boogie"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Kapelle Federolf",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing",
    "Charleston"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Keep Calm",
   "alias": [],
   "homepage": "https://keepcalm-band.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Kraichgau Buffalos",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "La Nuit Boheme",
   "alias": [],
   "homepage": "https://www.mein-event.shop/produkt/la-nuit-boheme-lavant-garde-19122026",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "LenneRockets",
   "alias": [],
   "homepage": "https://www.lennerockets.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country",
    "Rockabilly"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Let's Misbehave",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing",
    "Lindy Hop",
    "Charleston"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Limelight",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Rock'n'Roll"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Lonnie Dale",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "Lottmann & Masters",
   "alias": [],
   "homepage": "https://www.robertlottmann.com",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Louisiana & Kings Cotton",
   "alias": [],
   "homepage": "https://www.louisiana-ontour.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Ludwig Seuss & Band mit Henry Heggen",
   "alias": [],
   "homepage": "http://www.ludwig-seuss.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Maverick",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "Mountain Music Band",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "New Hot Club of Zurich",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing",
    "Balboa"
   ],
   "land": [
    "Schweiz"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Pepi's Crew",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Schweiz"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Ramblin' Boots",
   "alias": [],
   "homepage": "https://www.ramblinboots.nl",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Raphael Jost Quintet",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing",
    "Balboa"
   ],
   "land": [
    "Schweiz"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Rascal & Dodger",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "Ray Allen",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Rock'n'Roll",
    "Rockabilly"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Red River Band",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Reverent Juke",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing",
    "Lindy Hop",
    "Charleston"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Revolutionaires",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Rock'n'Roll",
    "Rockabilly"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Riffmen'n'Groove",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Ronny Nash",
   "alias": [],
   "homepage": "https://www.ronnynash.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "ROY",
   "alias": [],
   "homepage": "http://www.band-roy.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Ryan Eden",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Saddle n' Boots",
   "alias": [],
   "homepage": "https://www.saddleandboots.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Sixpack Corner",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "Skyline Riders",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Solitary Man & Pascal Goldt",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "Steve Morgen Band",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Swingin' Charlie 2026",
   "alias": [],
   "homepage": "https://www.swingincharlie.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Syncopation Society Orchestra",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing",
    "Lindy Hop",
    "Charleston"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "T-Bone-Country",
   "alias": [],
   "homepage": "https://www.t-bone-country.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Texas 45",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "The Alligators",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Rock'n'Roll"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "The Big Five feat. Nicolle Rochelle",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing",
    "Lindy Hop",
    "Balboa",
    "Shag"
   ],
   "land": [
    "Schweiz"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "The Blazing Cowboys",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "The Boosters",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Rock'n'Roll"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "The County Boys",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "The Crown Jewels",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "The Groovy Four",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing",
    "Lindy Hop",
    "Balboa",
    "Blues"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "The Highwayman",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "The Moonshiners",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "The Open Range",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "The Rockin' Rudolphs",
   "alias": [],
   "homepage": "https://rogerleuenberger.ch/rudolphs.html",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Schweiz"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "The Satelliters",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Rockabilly",
    "Rock'n'Roll"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "The Spikes",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country",
    "Rockabilly",
    "Rock'n'Roll",
    "Boogie"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "The Spirit of the Twenties",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing",
    "Lindy Hop",
    "Balboa",
    "Charleston",
    "Blues",
    "Boogie"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "The Stardust Sycopators",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Swing",
    "Balboa"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  },
  {
   "name": "Three Chords & The Truth",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "Tom Mac",
   "alias": [],
   "homepage": "https://www.kaisers-mackenbach.com",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Tommy Romero",
   "alias": [],
   "homepage": "https://www.tommyromero.com",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country",
    "Rock'n'Roll"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Western Helden",
   "alias": [],
   "homepage": "https://www.western-helden.de",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Adresse stammt aus dem Termin-Link, noch nicht geprüft."
  },
  {
   "name": "Western Trail",
   "alias": [],
   "homepage": "",
   "lesbar": "nur-facebook",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Nur Facebook bekannt (nicht lesbar). Eigene Homepage suchen."
  },
  {
   "name": "Woodstones",
   "alias": [],
   "homepage": "",
   "lesbar": "offen",
   "geprueft": "",
   "naechste": "",
   "termine": 1,
   "stil": [
    "Country"
   ],
   "land": [
    "Deutschland"
   ],
   "hinweis": "Noch keine Adresse. Homepage suchen."
  }
 ]
};
