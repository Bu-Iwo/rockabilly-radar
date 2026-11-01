/*
  ROCKABILLY RADAR – Event-Liste (Festivals, Weekender, Tanzabende)
  Stand der Recherche: 01.11.2026

  Diese Datei und die Dateien events-country-1.js bis events-country-3.js
  enthalten die Termine. Jeder Eintrag in RR_EVENTS ist ein Event.

  kind   "festival" = Festival, Weekender, Großevent
         "local"    = lokaler Abend (Konzert, Tanzabend, Party)
         "course"   = Kurs oder Workshop (Extra)
         "tribute"  = Tribute-Show (Extra)

  status "ok"      = Datum und Ort wurden auf mindestens einer Veranstalter-/Hotelseite gefunden
         "kalender" = Termin stammt aus einem Szene-Kalender (Quelle steht bei src)
         "check"   = Datum oder Ort ist nicht sicher, die App zeigt einen Hinweis
*/

window.RR_EVENTS = [
  /* ---------- Festivals und Weekender (Veranstalter-Seiten geprüft) ---------- */
  {
    id: "rockin-race-2027", kind: "festival",
    title: "Rockin' Race Jamboree",
    start: "2027-02-03", end: "2027-02-07",
    city: "Torremolinos", countryName: "Spanien",
    venue: "Auditorio Príncipe de Asturias und weitere Orte in Torremolinos",
    lat: 36.6217, lng: -4.4999,
    styles: ["Rock'n'Roll", "Rockabilly"],
    features: ["33. Ausgabe", "Classics on Wheels"],
    info: "https://rockinrace.com/",
    tickets: "https://rockinrace.com/entradas/",
    status: "ok", note: ""
  },
  {
    id: "berlin-shake-5-2027", kind: "festival",
    title: "Berlin Shake R'n'R Weekender #5",
    start: "2027-03-26", end: "2027-03-28",
    city: "Berlin", countryName: "Deutschland",
    venue: "Festsaal Kreuzberg, Am Flutgraben 2",
    lat: 52.4944, lng: 13.4507,
    styles: ["Rock'n'Roll"], features: [],
    info: "https://www.berlinshake.com/",
    status: "check",
    note: "Der 26.03.2027 steht bei einem Ticketportal und im Kalender der Jukebox Stompers. Das Enddatum 28.03. nennt nur der Kalender."
  },
  {
    id: "rocking-riot-2027", kind: "festival",
    title: "Rocking Riot",
    start: "2027-04-02", end: "2027-04-04",
    city: "Eindhoven", countryName: "Niederlande",
    venue: "Klokgebouw",
    lat: 51.4476, lng: 5.4547,
    styles: ["Rockabilly", "Rock'n'Roll"],
    features: ["Rocking Rebels Eindhoven"],
    info: "https://www.rebelshop.nl/details-en-registratie/rocking-riot-2027",
    tickets: "https://www.rebelshop.nl/details-en-registratie/rocking-riot-2027",
    status: "check",
    note: "Die Seite nennt 2.–4. April, im Text aber nur zwei Tage (2. und 3.). Bitte beim Veranstalter prüfen."
  },
  {
    id: "wiesloch-weekender-2027", kind: "festival",
    title: "Rock'n'Roll Weekender Wiesloch",
    start: "2027-05-27", end: "2027-05-30",
    city: "Wiesloch", countryName: "Deutschland",
    venue: "Palatin Kongresshotel und Kulturzentrum",
    lat: 49.2944, lng: 8.6988,
    styles: ["Rock'n'Roll", "Rockabilly"],
    features: ["Tanzkurse", "Record Hop", "50s-Markt", "Oldtimer-Treffen"],
    acts: "Jack Baymoore, Spunyboys, Black Raven, Revolutionaires, Jake Calypso Trio u. a.",
    info: "https://www.palatin.de/kultur/rocknroll-weekender/",
    hotel: { label: "Hotelpaket mit Ticket", url: "https://www.palatin.de/hotel/rocknroll-weekender-2027/" },
    status: "ok",
    note: "Das Ticket gibt es im Hotelpaket (ab 79,50 € pro Person und Nacht im Doppelzimmer). Weitere Bands folgen."
  },

  /* ---------- Aus dem Kalender der Jukebox Stompers (jukeboxstompers.de) ---------- */
  { id: "js-wellness-2026", kind: "festival", title: "Swingin' Wellness Weekend", start: "2026-11-06", end: "2026-11-08", city: "Bad Blumau", countryName: "Österreich", venue: "Rogner Bad Blumau", lat: 47.1161, lng: 16.0516, styles: ["Boogie", "Swing"], features: ["Lindy Hop", "West Coast Swing", "Balboa"], info: "https://www.facebook.com/events/1167433208928157", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-ossig-2026", kind: "local", title: "Rock'n'Roll Hotel Dance", start: "2026-11-07", end: "2026-11-07", city: "Roßwein (Ossig)", countryName: "Deutschland", venue: "Landhotel Sonnenhof, Ossig 9e", lat: 51.065, lng: 13.185, styles: ["Rock'n'Roll"], features: [], info: "https://www.facebook.com/LandhotelOssig", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-jukebox-1114", kind: "local", title: "50s Boogie & Swing Jukebox", start: "2026-11-14", end: "2026-11-14", city: "Leipzig", countryName: "Deutschland", venue: "Tanzsaal Frische Prieße, Prießnitzstr. 1", lat: 51.3406, lng: 12.3747, styles: ["Boogie", "Swing", "Rock'n'Roll"], features: ["Jive", "R&B", "Doo Wop"], info: "https://www.jukeboxstompers.de/index.php/veranstaltungen/veranstaltungskalender", status: "kalender", src: "jukeboxstompers.de", note: "Kartenvorbestellung per E-Mail, einen Link gibt es nicht." },
  { id: "js-sdn-1114", kind: "local", title: "Swing Dance Night", start: "2026-11-14", end: "2026-11-14", city: "Leipzig", countryName: "Deutschland", venue: "Swing Dance Leipzig, Holbeinstr. 29", lat: 51.3406, lng: 12.3747, styles: ["Swing"], features: ["Balboa", "Lindy Hop"], info: "https://www.swingdanceleipzig.com/index.php/tanzen-leipzig/", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-sdn-burg-1121", kind: "local", title: "Swing Dance Night", start: "2026-11-21", end: "2026-11-21", city: "Burgstädt", countryName: "Deutschland", venue: "Hotel Goldener Löwe, Burkersdorfer Str. 122", lat: 50.9159, lng: 12.8008, styles: ["Swing", "Boogie"], features: ["Lindy Hop", "Balboa"], info: "https://www.loewe-burgstaedt.de/VORSCHAU-TERMINE-TANZ-2026/", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-dm-boogie-2026", kind: "festival", title: "Deutsche Meisterschaft Boogie Woogie", start: "2026-11-21", end: "2026-11-21", city: "Rain", countryName: "Deutschland", venue: "Mehrzweckhalle, Attinger Stare 10", lat: 48.8957, lng: 12.4476, styles: ["Boogie"], features: ["Turnier"], info: "https://www.boogie-mäuse.de/", status: "check", src: "jukeboxstompers.de", note: "Der Kalender nennt nur 'Rain'. Die Lage des Ortes habe ich geschätzt (Rain bei Straubing). Bitte prüfen." },
  { id: "js-teadance-1129", kind: "local", title: "Sunday Teadance", start: "2026-11-29", end: "2026-11-29", city: "Leipzig", countryName: "Deutschland", venue: "Noels Ballroom, Kurt-Eisner-Str. 43", lat: 51.3406, lng: 12.3747, styles: ["Boogie", "Swing"], features: ["Lindy Hop", "Jive", "nur Vinyl"], info: "https://www.lindyhopleipzig.de/Veranstaltungen/", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-sdn-1212", kind: "local", title: "Swing Dance Night", start: "2026-12-12", end: "2026-12-12", city: "Leipzig", countryName: "Deutschland", venue: "Swing Dance Leipzig, Holbeinstr. 29", lat: 51.3406, lng: 12.3747, styles: ["Swing"], features: ["Balboa", "Lindy Hop"], info: "https://www.swingdanceleipzig.com/index.php/tanzen-leipzig/", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-belly-1212", kind: "local", title: "Belly Dance meet Pink Pettycoats", start: "2026-12-12", end: "2026-12-12", city: "Freiberg", countryName: "Deutschland", venue: "Tivoli Freiberg, Dr.-Külz-Str. 3", lat: 50.9169, lng: 13.3429, styles: ["Rock'n'Roll", "Swing"], features: ["Orientalischer Tanz"], info: "https://www.facebook.com/events/973470839015601", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-teadance-1213", kind: "local", title: "Weihnachts-Sunday-Teadance", start: "2026-12-13", end: "2026-12-13", city: "Leipzig", countryName: "Deutschland", venue: "Noels Ballroom, Kurt-Eisner-Str. 43", lat: 51.3406, lng: 12.3747, styles: ["Boogie", "Swing"], features: ["Lindy Hop", "Jive"], info: "https://www.lindyhopleipzig.de/Veranstaltungen/", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-xmas-dortmund-2026", kind: "festival", title: "Rockin' Around the Christmas Tree", start: "2026-12-18", end: "2026-12-20", city: "Dortmund", countryName: "Deutschland", venue: "Musiktheater Piano, Lütgendortmunder Str. 43", lat: 51.5142, lng: 7.4653, styles: ["Rock'n'Roll"], features: ["R&B", "Jive"], info: "https://www.musiktheater-piano.de/events/rockin-around-the-christmas-tree-20261218/", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-sdn-burg-1229", kind: "local", title: "Swing Dance Night", start: "2026-12-29", end: "2026-12-29", city: "Burgstädt", countryName: "Deutschland", venue: "Hotel Goldener Löwe, Burkersdorfer Str. 122", lat: 50.9159, lng: 12.8008, styles: ["Swing", "Boogie"], features: ["Lindy Hop", "Balboa"], info: "https://www.loewe-burgstaedt.de/VORSCHAU-TERMINE-TANZ-2026/", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-lgw-2026", kind: "festival", title: "Let's Get Wild", start: "2026-12-30", end: "2027-01-02", city: "Stuttgart", countryName: "Deutschland", venue: "Sängerhalle, Lindenstr. 29", lat: 48.7784, lng: 9.18, styles: ["Rock'n'Roll", "Rockabilly", "Country"], features: ["R&B", "Blues", "Soul"], info: "https://www.facebook.com/groups/745452892556376", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-silvester-boheme-2026", kind: "local", title: "Ballroom Boheme Silvester Party", start: "2026-12-31", end: "2026-12-31", city: "Leipzig", countryName: "Deutschland", venue: "Felsenkeller, Karl-Heine-Str. 32", lat: 51.3406, lng: 12.3747, styles: ["Swing"], features: ["1920er"], info: "https://www.felsenkeller-leipzig.com/silvester/", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-golden-swing-2026", kind: "local", title: "Golden Swing Night", start: "2026-12-31", end: "2026-12-31", city: "Leipzig", countryName: "Deutschland", venue: "Parkschloss, Im Dölitzer Holz 20", lat: 51.3406, lng: 12.3747, styles: ["Swing"], features: [], info: "https://parkschlossleipzig.de/silvester/", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-boogie-bash-2027", kind: "local", title: "Rockin' All Night Boogie Bash", start: "2027-01-16", end: "2027-01-16", city: "Freiberg (Kleinwaltersdorf)", countryName: "Deutschland", venue: "Bürgerhaus Kleinwaltersdorf, Walterstal 76", lat: 50.9328, lng: 13.2909, styles: ["Boogie", "Rock'n'Roll", "Rockabilly"], features: ["Jive"], info: "https://www.facebook.com/events/2255353928590915", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-winter-rockin-jive-2027", kind: "festival", title: "Winter Rockin' Jive", start: "2027-01-22", end: "2027-01-24", city: "Hohenkirchen", countryName: "Deutschland", venue: "Wangerland Resort, Jeversche Str. 100", lat: 53.6639, lng: 7.9157, styles: ["Rockabilly", "Rock'n'Roll"], features: ["Jive"], info: "https://www.wangerland-resort.de/winter-rock-jive-weekender/", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-triple-step-2027", kind: "festival", title: "Triple Step Madness", start: "2027-01-22", end: "2027-01-24", city: "De Rijp", countryName: "Niederlande", venue: "Hotel De Rijp, Zuiddijk 2A", lat: 52.5549, lng: 4.8442, styles: ["Swing", "Boogie"], features: ["Lindy Hop"], info: "https://triplestepmadness.nl/de/", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-rts-20-2027", kind: "festival", title: "Rock That Swing #20", start: "2027-02-04", end: "2027-02-08", city: "München", countryName: "Deutschland", venue: "Vintage Club & Deutsches Theater, Sonnenstr. 12", lat: 48.1371, lng: 11.5754, styles: ["Swing", "Boogie"], features: ["Lindy Hop", "Shag", "Balboa"], info: "http://www.rockthatswing.com/", status: "kalender", src: "jukeboxstompers.de", note: "Das Festival war bisher in der Liste 'Termin offen'. Der Kalender nennt jetzt den 4.–8. Februar 2027." },
  { id: "js-rac-2027", kind: "festival", title: "Rock Around The Clock", start: "2027-04-02", end: "2027-04-04", city: "Wels", countryName: "Österreich", venue: "Tanzschule Hippmann, Pollheimerstr. 7", lat: 48.1565, lng: 14.0244, styles: ["Boogie"], features: [], info: "https://rockaclock.com/", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-bb-camp-2027", kind: "festival", title: "BB Dance Camp #40", start: "2027-05-14", end: "2027-05-17", city: "Landsberg am Lech", countryName: "Deutschland", venue: "Sportzentrum, Katharinenstr. 1", lat: 48.0497, lng: 10.8769, styles: ["Boogie", "Swing"], features: ["Lindy Hop", "Dance Camp"], info: "https://www.bb-dancecamp.com/de/home.html", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-skyrocket-2027", kind: "festival", title: "Sky Rocket Festival", start: "2027-06-11", end: "2027-06-13", city: "Neuruppin", countryName: "Deutschland", venue: "Hangar-312, Hugo-Eckener-Ring 40", lat: 52.9244, lng: 12.8093, styles: ["Rockabilly", "Rock'n'Roll", "Swing"], features: ["Blues"], info: "https://hangar-312.de/veranstaltungen/skyrocket-festival", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-boogie-schmiede-2027", kind: "festival", title: "10 Jahre Boogie Schmiede", start: "2027-06-12", end: "2027-06-13", city: "Bad Füssing", countryName: "Deutschland", venue: "Kulturhaus Bad Füssing", lat: 48.3404, lng: 13.3184, styles: ["Boogie"], features: [], info: "https://boogieschmiede.de/", status: "check", src: "jukeboxstompers.de", note: "Der Kalender nennt '12.–13.06.2026 (?)' mitten unter den Terminen für 2027. Ich gehe von 2027 aus. Bitte prüfen." },
  { id: "js-firebirds-2027", kind: "festival", title: "Firebirds Festival #15", start: "2027-07-02", end: "2027-07-04", city: "Leisnig", countryName: "Deutschland", venue: "Kloster Buch, Klosterbuch 1", lat: 51.16, lng: 12.9266, styles: ["Rock'n'Roll", "Boogie"], features: ["Dance Camp"], info: "https://www.firebirds-festival.de/", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-oldietown-2027", kind: "festival", title: "Oldietown Festival", start: "2027-07-09", end: "2027-07-11", city: "Wolframs-Eschenbach", countryName: "Deutschland", venue: "Altstadt (7 Bühnen)", lat: 49.2265, lng: 10.7259, styles: ["Rock'n'Roll", "Rockabilly"], features: ["R&B", "50er bis 70er"], info: "https://oldietown.de/", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-boogie-feets-2027", kind: "festival", title: "Boogie Feets #10", start: "2027-07-22", end: "2027-07-26", city: "Oslo", countryName: "Norwegen", venue: "Boogie Feet Festival, Rosenkrantz' gate 7", lat: 59.9133, lng: 10.739, styles: ["Boogie"], features: [], info: "https://boogiefeetfestival.com/", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-sommer-oldies-2027", kind: "festival", title: "Sommer Oldies 2027", start: "2027-08-06", end: "2027-08-08", city: "Zwönitz", countryName: "Deutschland", venue: "Marktplatz / Stadtmitte", lat: 50.6301, lng: 12.8132, styles: ["Rock'n'Roll"], features: ["50er-Jahre-Musik"], info: "https://sommeroldies.zwoenitz.de/", status: "check", src: "jukeboxstompers.de", note: "Der Kalender nennt '06.–08.08.2026 (?)' unter den Terminen für 2027. Ich gehe von 2027 aus. Bitte prüfen." },
  { id: "js-summershelter-2027", kind: "festival", title: "Summershelter Festival 2027", start: "2027-08-13", end: "2027-08-15", city: "Biederitz", countryName: "Deutschland", venue: "Heyrothsberger Park, Parkweg 1b", lat: 52.1567, lng: 11.7198, styles: ["Rock'n'Roll"], features: ["Open Air"], info: "https://www.facebook.com/events/1586728179663156", status: "kalender", src: "jukeboxstompers.de", note: "" },
  { id: "js-cruise-2027", kind: "festival", title: "Rock'n'Roll Cruise #4", start: "2027-10-09", end: "2027-10-16", city: "Triest", countryName: "Italien", venue: "Kreuzfahrtschiff ab/bis Triest (Mittelmeer)", lat: 45.6496, lng: 13.7773, styles: ["Rock'n'Roll", "Boogie", "Swing"], features: ["Kreuzfahrt"], info: "https://www.rocknrollcruise.de/de/index.html", status: "kalender", src: "jukeboxstompers.de", note: "" }
];

/* Events, deren Termin 2027 noch nicht veröffentlicht oder noch nicht sicher ist */
window.RR_PENDING = [
  {
    title: "Summer Jamboree",
    place: "Senigallia, Italien",
    last: "31. Juli bis 9. August 2026",
    info: "https://www.summerjamboree.com/en/festival/"
  },
  {
    title: "Rockabilly Days",
    place: "Region Stuttgart, Deutschland",
    last: "31. Juli 2026 (drei Tage)",
    info: "https://rockabillydays.de/"
  },
  {
    title: "Rhythm Riot",
    place: "Great Yarmouth, Großbritannien",
    last: "8. bis 12. Oktober 2026",
    info: "https://rhythmriot.com/"
  },
  {
    title: "26. Boogie Attack",
    place: "Markkleeberg bei Leipzig, Deutschland",
    last: "Termin noch nicht bestätigt (Anfang oder Mitte September)",
    info: "https://www.boogie-attack.de/"
  }
];
