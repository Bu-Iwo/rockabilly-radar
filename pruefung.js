/*
  ROCKABILLY RADAR – Prüfdaten
  Diese Datei sagt der App, wann ein Termin zuletzt geprüft wurde und wie.
  Die Termine selbst stehen weiter in events.js und events-country-1.js bis -3.js.

  stand     Tag der letzten Gesamt-Recherche. Gilt für alle Termine, die unten keine eigene Angabe haben.
            Diese Termine erscheinen als "Szene-Kalender".
  quellen   Wann eine Quelle zuletzt gelesen wurde (überschreibt "stand" für Termine dieser Quelle).
            Beispiel: "jukeboxstompers.de": "2026-11-29"
  termine   Termine, die beim Veranstalter geprüft wurden. Der Schlüssel ist die id des Termins.
            art "veranstalter" = erscheint als "Termin bestätigt" und "beim Veranstalter geprüft".
            Beispiel: "rockin-race-2027": { datum: "2026-11-29", art: "veranstalter" }

  fehlt     Termine, die bei der letzten Prüfung in ihrer Quelle nicht mehr gefunden wurden. Die App zeigt sie weiter an, aber mit der
            Warnung "Bitte beim Veranstalter prüfen". Wird der Termin bei der nächsten Prüfung wieder gefunden, fliegt der Eintrag raus.
            Fehlt er erneut, wird der Termin aus den Daten entfernt.
            Beispiel: "x-rr-20261106-karlsruhe-swingin-charlie-20": { seit: "2026-11-29", anzahl: 1 }

  Die Monatsaufgabe pflegt diese Datei. Datumsangaben immer im Format JJJJ-MM-TT.
*/

window.RR_PRUEFUNG = {
  stand: "2026-11-03",
  quellen: {
    "the-hot-club.com": "2026-11-05",
    "wyattchristmasfive.de": "2026-11-05",
    "shotgunjones.de": "2026-11-05",
    "rocats.de": "2026-11-05",
    "b-shakers.ch": "2026-11-05",
    "kajuete-ratzdorf.com": "2026-11-05",
    "dochornberlin.de": "2026-11-05",
    "Eventim": "2026-11-05",
    "Jambase": "2026-11-05",
    "Songkick": "2026-11-05",
    "mvp.de": "2026-11-05",
    "alanpowerandtheaftershocks.com": "2026-11-05"
  },
  termine: {
  },
  fehlt: {
  }
};
