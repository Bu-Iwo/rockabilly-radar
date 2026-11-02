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

  Die Monatsaufgabe pflegt diese Datei. Datumsangaben immer im Format JJJJ-MM-TT.
*/

window.RR_PRUEFUNG = {
  stand: "2026-11-03",
  quellen: {
  },
  termine: {
  }
};
