/*
  ROCKABILLY RADAR – Englische Übersetzung der Event-Texte

  Wofür diese Datei da ist:
  - Die Oberfläche der App (Knöpfe, Überschriften) ist direkt in index.html übersetzt.
  - Diese Datei enthält die Übersetzungen der Texte aus den Terminen: Länder, Städte-Namen, Schlagworte, Hinweise.
  - Fehlt zu einem Text hier die Übersetzung, zeigt die App in der englischen Ansicht einfach den deutschen Text. Es geht nichts kaputt.
  - Namen von Events, Bands, Orten und Straßen werden nicht übersetzt.

  Neue Termine: Taucht bei einem neuen Termin ein neuer deutscher Hinweis auf, wird er unter "notes" ergänzt:
  "Deutscher Text": "English text",
*/
window.RR_EN = {
  countries: {
    'Deutschland': 'Germany',
    'Österreich': 'Austria',
    'Schweiz': 'Switzerland',
    'Niederlande': 'Netherlands',
    'Italien': 'Italy',
    'Spanien': 'Spain',
    'Norwegen': 'Norway',
    'Großbritannien': 'United Kingdom',
    'Frankreich': 'France',
    'Belgien': 'Belgium',
    'Dänemark': 'Denmark',
    'Schweden': 'Sweden',
    'Polen': 'Poland',
    'Tschechien': 'Czechia',
    'Portugal': 'Portugal',
    'Irland': 'Ireland'
  },

  /* Nur Städte mit gebräuchlichem englischem Namen. Zusammengesetzte Namen wie "München-Allach" werden automatisch mit übersetzt. */
  cities: {
    'München': 'Munich',
    'Köln': 'Cologne',
    'Nürnberg': 'Nuremberg',
    'Wien': 'Vienna',
    'Triest': 'Trieste',
    'Zürich': 'Zurich',
    'Rom': 'Rome',
    'Mailand': 'Milan',
    'Prag': 'Prague',
    'Kopenhagen': 'Copenhagen',
    'Lissabon': 'Lisbon'
  },

  features: {
    '33. Ausgabe': '33rd edition',
    'Tanzkurse': 'Dance classes',
    '50s-Markt': '50s market',
    'Oldtimer-Treffen': 'Classic car meet',
    'Turnier': 'Competition',
    'nur Vinyl': 'Vinyl only',
    'Orientalischer Tanz': 'Oriental dance',
    '1920er': '1920s',
    '50er bis 70er': '50s to 70s',
    '50er-Jahre-Musik': '1950s music',
    'Kreuzfahrt': 'Cruise',
    'Poolpartys': 'Pool parties',
    'Live-Musik täglich': 'Live music daily',
    'Steptanz': 'Tap dance',
    'Live-Musik': 'Live music',
    'Tanzen': 'Dancing',
    'Vintage-Markt': 'Vintage market'
  },

  /* Orte, die eine Beschreibung statt eines Namens enthalten */
  venues: {
    'Swingkurse und -parties (Orte beim Veranstalter)': 'Swing classes and parties (venues via the organiser)',
    'Auditorio Príncipe de Asturias und weitere Orte in Torremolinos': 'Auditorio Príncipe de Asturias and other venues in Torremolinos',
    'Davos (Ort nicht genannt)': 'Davos (venue not named)',
    '10 Years Luckymonkey (Ort nicht genannt)': '10 Years Luckymonkey (venue not named)'
  },

  hotel: {
    'Hotelpaket mit Ticket': 'Hotel package with ticket'
  },

  pending: {
    'Summer Jamboree': { place: 'Senigallia, Italy', last: '31 July to 9 August 2026' },
    'Rockabilly Days': { place: 'Stuttgart area, Germany', last: '31 July 2026 (three days)' },
    'Rhythm Riot': { place: 'Great Yarmouth, United Kingdom', last: '8 to 12 October 2026' },
    '26. Boogie Attack': { place: 'Markkleeberg near Leipzig, Germany', last: 'date not yet confirmed (early or mid-September)' }
  },

  /* Hinweise zu Terminen (Feld "note"). Einfache Hinweise wie "Beginn 20:00 Uhr" übersetzt die App selbst. */
  notes: {
    'Der 26.03.2027 steht bei einem Ticketportal und im Kalender der Jukebox Stompers. Das Enddatum 28.03. nennt nur der Kalender.':
      'The date 26 March 2027 is listed on a ticket portal and in the Jukebox Stompers calendar. Only the calendar gives the end date, 28 March.',
    'Die Seite nennt 2.–4. April, im Text aber nur zwei Tage (2. und 3.). Bitte beim Veranstalter prüfen.':
      'The page says 2–4 April, but the text only mentions two days (2 and 3 April). Please check with the organiser.',
    'Das Ticket gibt es im Hotelpaket (ab 79,50 € pro Person und Nacht im Doppelzimmer). Weitere Bands folgen.':
      'The ticket comes as part of a hotel package (from €79.50 per person and night in a double room). More bands to follow.',
    'Kartenvorbestellung per E-Mail, einen Link gibt es nicht.':
      'Tickets can be reserved by e-mail; there is no link.',
    'Der Kalender nennt nur \'Rain\'. Die Lage des Ortes habe ich geschätzt (Rain bei Straubing). Bitte prüfen.':
      'The calendar only says "Rain". The location is estimated (Rain near Straubing). Please check.',
    'Das Festival war bisher in der Liste \'Termin offen\'. Der Kalender nennt jetzt den 4.–8. Februar 2027.':
      'The festival used to be on the "date open" list. The calendar now gives 4–8 February 2027.',
    'Der Kalender nennt \'12.–13.06.2026 (?)\' mitten unter den Terminen für 2027. Ich gehe von 2027 aus. Bitte prüfen.':
      'The calendar lists "12–13.06.2026 (?)" among the 2027 dates. I assume 2027. Please check.',
    'Der Kalender nennt \'06.–08.08.2026 (?)\' unter den Terminen für 2027. Ich gehe von 2027 aus. Bitte prüfen.':
      'The calendar lists "06–08.08.2026 (?)" among the 2027 dates. I assume 2027. Please check.',
    'Beginn 20:00 Uhr (Stadtkoordinate). Der Kalender nennt Straubing, die Adresse liegt in Leiblfing.':
      'Starts 20:00 (pin at city centre). The calendar says Straubing; the address is in Leiblfing.',
    'Beginn 19:30 Uhr. Abfahrt in Prien am Chiemsee.':
      'Starts 19:30. Departure in Prien am Chiemsee.',
    'Live: The Shirt Tail Stompers (Fr/Sa). Sonntag: Fächerswing. (Stadtkoordinate)':
      'Live: The Shirt Tail Stompers (Fri/Sat). Sunday: Fächerswing (fan swing). (pin at city centre)',
    'Einlass 19 Uhr (Uhrzeit laut Quelle mit Fragezeichen). (Stadtkoordinate)':
      'Doors 19:00 (time given with a question mark in the source). (pin at city centre)',
    'Rock\'n\'Roll-Tanzfahrt auf dem Rhein. Beginn 19:30 Uhr. (Stadtkoordinate)':
      'Rock\'n\'roll dance cruise on the Rhine. Starts 19:30. (pin at city centre)',
    'Brunch und Matinee, Beginn 11:00 Uhr. (Stadtkoordinate)':
      'Brunch and matinee, starts 11:00. (pin at city centre)',
    'Beginn 20:30 Uhr. Die Quelle nennt keinen Stil, die Eintragung stammt aus einem Rock\'n\'Roll-Kalender. (Stadtkoordinate)':
      'Starts 20:30. The source names no style; the entry comes from a rock\'n\'roll calendar. (pin at city centre)',
    'Beginn 20:00 Uhr, Kartenbestellung beim Veranstalter. (Stadtkoordinate)':
      'Starts 20:00, tickets via the organiser. (pin at city centre)',
    'Einlass 19 Uhr, Beginn 20:30 Uhr, Abendkasse 15 €. (Stadtkoordinate)':
      'Doors 19:00, starts 20:30, box office €15. (pin at city centre)',
    'Beginn 19:00 Uhr, Eintritt 64,50 € inkl. Getränke und Häppchen. (Stadtkoordinate)':
      'Starts 19:00, admission €64.50 incl. drinks and canapés. (pin at city centre)',
    'Beginn 20:00 Uhr. Mit Christoph Steinbach, Albert Koch, Richie Loidl, Daniel Balázs, Lluís Coloma, Robert Shumy, Ben Holder, Walt Bender und Wolfgang Janischowski. (Stadtkoordinate)':
      'Starts 20:00. With Christoph Steinbach, Albert Koch, Richie Loidl, Daniel Balázs, Lluís Coloma, Robert Shumy, Ben Holder, Walt Bender and Wolfgang Janischowski. (pin at city centre)',
    'Weitere Termine dort: 11.12. und 12.12.2026. Konzerttermin laut Broken Silence. (Stadtkoordinate)':
      'More dates there: 11 and 12 December 2026. Concert date per Broken Silence. (pin at city centre)',
    'Mehrere Abende: 20., 21., 27., 28.11., 3., 4., 5., 10., 11., 12., 17., 18., 19., 20., 28. und 31.12.2026. Konzerttermin laut Broken Silence. (Stadtkoordinate)':
      'Several evenings: 20, 21, 27, 28 Nov and 3, 4, 5, 10, 11, 12, 17, 18, 19, 20, 28 and 31 Dec 2026. Concert date per Broken Silence. (pin at city centre)',
    'Der Ort ist nur als „Leubnitz“ angegeben, die Lage ist geschätzt. Konzerttermin laut Broken Silence. (Stadtkoordinate)':
      'The place is only given as “Leubnitz”, so the location is estimated. Concert date per Broken Silence. (pin at city centre)',
    'Programm laut Veranstalter u. a. Tribut „Streets of Bakersfield“, 70 Jahre Carl Perkins Dance Album und eine Show zum 50. Todestag von Elvis Presley. Einzelne Künstler stehen noch nicht auf der Seite.':
      'Programme per organiser includes the tribute “Streets of Bakersfield”, 70 years of the Carl Perkins Dance Album and a show for the 50th anniversary of Elvis Presley\'s death. Some artists are not yet on the website.',
    'Konzerttermin laut Homepage der Band.':
      'Concert date per the band\'s website.',
    'Konzerttermin laut Homepage der Band. (Stadtkoordinate)':
      'Concert date per the band\'s website. (pin at city centre)',
    'Konzerte am 28. und 29.05.2027 laut Homepage der Band. Den Veranstaltungsort nennt die Seite nicht. (Stadtkoordinate)':
      'Concerts on 28 and 29 May 2027 per the band\'s website. The page does not name the venue. (pin at city centre)',
    'Kartenreservierung: 0178 9332241. Konzerttermin laut Homepage der Band. (Stadtkoordinate)':
      'Ticket reservation: 0178 9332241. Concert date per the band\'s website. (pin at city centre)',
    'Kartenreservierung: 03774 505851. Konzerttermin laut Homepage der Band. (Stadtkoordinate)':
      'Ticket reservation: 03774 505851. Concert date per the band\'s website. (pin at city centre)',
    'Shotgun Jones spielt laut Homepage der Band. Die Seite nennt „US Car & Bike Evolution, F60“. Bitte den Ort beim Veranstalter prüfen. (Stadtkoordinate)':
      'Shotgun Jones play, per the band\'s website. The page says “US Car & Bike Evolution, F60”. Please check the venue with the organiser. (pin at city centre)',
    'Shotgun Jones spielt laut Homepage der Band am 16.07. (Main Street) und am 17.07. (Hudson Bay Bühne). Das Festival-Programm steht noch nicht beim Veranstalter. Bitte dort prüfen.':
      'Shotgun Jones play, per the band\'s website, on 16 July (Main Street) and 17 July (Hudson Bay stage). The festival programme is not yet on the organiser\'s site. Please check there.',
    'Beginn 20:30 Uhr. Konzerttermin laut Homepage der Band.':
      'Starts 20:30. Concert date per the band\'s website.',
    'Beginn 20:30 Uhr. Konzerttermin laut Homepage der Band. (Stadtkoordinate)':
      'Starts 20:30. Concert date per the band\'s website. (pin at city centre)',
    'Beginn 21:00 Uhr. Konzerttermin laut Homepage der Band. (Stadtkoordinate)':
      'Starts 21:00. Concert date per the band\'s website. (pin at city centre)',
    'Die Seite der Band nennt nur „10 Years Luckymonkey“. Den genauen Ort bitte prüfen. (Stadtkoordinate)':
      'The band\'s page only says “10 Years Luckymonkey”. Please check the exact venue. (pin at city centre)',
    'Beginn 20:00 Uhr, Bar ab 18:00 Uhr. Eintritt 15 € an der Abendkasse, Reservierung per E-Mail an kontakt@kajuete-ratzdorf.com. (Stadtkoordinate)':
      'Starts 20:00, bar open from 18:00. Admission €15 at the box office, reservations by e-mail to kontakt@kajuete-ratzdorf.com. (pin at city centre)',
    'Bei Eventim steht „Silvestersause mit Boppin\'B und Celebration X“ am 31.12.2026, ohne Ortsangabe. Dreieich und Bürgerhaus stammen aus der Bandsuche. Bitte prüfen. (Stadtkoordinate)':
      'Eventim lists “Silvestersause mit Boppin\'B und Celebration X” on 31 Dec 2026 without a location. Dreieich and Bürgerhaus come from the band search. Please check. (pin at city centre)',
    'Beginn 20:00 Uhr. Karten ab 27 €.':
      'Starts 20:00. Tickets from €27.',
    'Karten ab 23,85 €. Uhrzeit nicht angegeben.':
      'Tickets from €23.85. Start time not given.',
    'Einlass 19:00 Uhr, Beginn 20:00 Uhr, Karten ab 25 €. Mit dem Heidelberger Boogie-Woogie-Pianisten Harald „Lee“ Krüger.':
      'Doors 19:00, starts 20:00, tickets from €25. With Heidelberg boogie-woogie pianist Harald “Lee” Krüger.',
    'Zwei Abende: 30. und 31.05.2027. Karten ab 46 €.':
      'Two evenings: 30 and 31 May 2027. Tickets from €46.',
    'Beginn 18:00 Uhr. Konzerttermin laut Homepage der Band. (Stadtkoordinate)':
      'Starts 18:00. Concert date per the band\'s website. (pin at city centre)',
    'Beginn 19:00 Uhr. Konzerttermin laut Homepage der Band.':
      'Starts 19:00. Concert date per the band\'s website.',
    '11. Ausgabe, 20. bis 23.05.2027. Das Programm mit den Bands steht noch nicht auf der Seite.':
      '11th edition, 20 to 23 May 2027. The band line-up is not yet on the website.'
  }
};
