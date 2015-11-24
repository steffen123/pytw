[b]Pytw, das Angriffstool[/b]

[b]Funktionen[/b]
- Liest Spionage- und Kampfreporte und speichert sie in eine Datenbank
- Filtern zwischen Spielern und Barbaren
- Filtern nach Wall-Stufe, Einheitenanzahl, Entfernung, letztem Loot, min. Loot bei erreichen des Zieles und/oder erspähten Rohstoffen
- Zeigt die möglichen Ziele tabelarisch an
- Berechnet anhand der Gebäude, der Entfernung, Geschwindigkeit der einzusetzenden Einheit und des Berichtsalters wieviel man bei dem jeweiligen Ziel mitnehmen kann und wieviele Einheiten man dafür schicken muss. Speicher&Versteck werden dabei berücksichtigt.
- Kann nur Spieler anzeigen (default), nur Barbaren, oder beides
- Erkennt automatisch aus welchen Dörfern man angreift (Dörfer, aus denen mindestens zwei Trupps geschickt wurden, bzw. wo Berichte dafür vorliegen) und berechnet die Werte anhand des aktiven Dorfes
- Bisher unterstützt es nur die Einstellungen der Welt 122/deutsch, kann ich aber leicht erweitern
- Programm arbeitet komplett lokal auf eurem Rechner und ist nicht von Webdiensten oder irgendwas abhängig (und es nutzt solche auch nicht)
- Freie Software, d.h. kann gemäß der AGPL-Lizenz von jedem verändert oder weitergegeben werden.

[b]Bugreports, Vorschläge, Kommentare[/b]
Per Die-Stämme-PM, hier im Stammesforum, oder per Mail an steffen@schaumburger.info
Viele Funktionen ließen sich ganz leicht einbauen also ruhig sagen was ihr braucht. Ansonsten baue ich weitere Funktionen nach eigenem Bedarf ein.

[spoiler=Anforderungen]Python 3.4 oder höher und PyQt 5 (verfügbar für alle Betriebssysteme)
Links zum Download sind in den Installationsabschnitten[/spoiler]

[spoiler=Android/iOS]Habe ich momentan keine Pläne für, aber für einen Programmierer sollte die Anpassung für Android nicht allzu schwer sein[/spoiler]

[spoiler=Installation - Windows (64 bit)]Python downloaden und installieren: https://www.python.org/ftp/python/3.4.3/python-3.4.3.amd64.msi
Die Stämme erlaubt offenbar keine Links zu exe-Dateien. Daher müsst ihr das Leerzeichen im folgenden Link in "x64 exe" durch einen Punkt ersetzen.
PyQt downloaden und installieren: http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.5.1/PyQt5-5.5.1-gpl-Py3.4-Qt5.5.1-x64 exe/download
Jetzt weitermachen bei "Installation - allgemeiner Teil"[/spoiler]

[spoiler=Installation - Windows (32 bit)]Python downloaden und installieren: https://www.python.org/ftp/python/3.4.3/python-3.4.3.msi
Die Stämme erlaubt offenbar keine Links zu exe-Dateien. Daher müsst ihr das Leerzeichen im folgenden Link in "x32 exe" durch einen Punkt ersetzen.
PyQt downloaden und installieren: http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.5.1/PyQt5-5.5.1-gpl-Py3.4-Qt5.5.1-x32 exe/download
Jetzt weitermachen bei "Installation - allgemeiner Teil"[/spoiler]

[spoiler=Installation - allgemeiner Teil]Das Programm selbst runterladen, entweder den alpha-Release oder die aktuelle Entwicklerversion:
aktuelle alpha7: https://github.com/steffen123/pytw/archive/alpha7.zip
aktuelle Entwicklerversion: https://github.com/steffen123/pytw/archive/master.zip
Das Archiv irgendwohin entpacken. Eine "richtige Installation" ist für das eigentliche Tool nicht notwendig.[/spoiler]

[spoiler=Installation (sonstige)]Hängt vom Betriebssystem ab. Bitte Info und ich schreib die Anleitung für das jeweilige Betriebssystem. Brauche diese Details:
- Betriebssystem (z.B. Gentoo Linux oder Windows)
- Version des Betriebssystems[/spoiler]

[spoiler=Updaten]Einfach die neue Programm-Version (nur das Programm selber) runterladen und entpacken. Dann die bisher gespeicherten Reporte aus dem import-Verzeichnis der alten Version in das Import-Verzeichnis der neuen Version kopieren und fertig.
Die alte Version kann unabhängig von der neuen weiter verwendet werden. Alternativ kann man sie natürlich auch löschen.[/spoiler]

[b]Starten[/b]
Windows: Im Verzeichnis wo es entpackt ist pytw.bat doppelklicken.
Linux/Mac: Im Verzeichnis wo es entpackt ist pytw.sh doppelklicken.

[b]Berichte importieren[/b]
Ganz normal im Browser einen Spionage- oder Angriffsbericht aufrufen. Diesen in das "import/reports/" Verzeichnis im Installationsverzeichnis abspeichern. Dies muss für jeden Bericht gemacht werden. Bitte nur die HTML-Datei abspeichern, nicht die komplette Seite (Firefox zumindest erlaubt das, falls andere Browser das nicht können halt die komplette Seite abspeichern). Der Dateiname ist völlig egal. Ich numeriere sie einfach durch.
Es stört nicht wenn man einen Bericht doppelt abspeichert oder mehrere Berichte zu einem Ziel hat, das Programm berücksichtigt momentan nur den jeweils aktuellsten Bericht.

Nun im Programm "Import Reports" anklicken. Das Programm verarbeitet nun alle Berichte und zeigt dann die in Frage kommenden Ziele an.

Wenn man sehr viele neue Berichte (hunderte) hat kann das importieren ein paar Sekunden dauern, währenddessen wirkt das Programm so als ob es eingefroren ist.

Für optimale Nutzung des Programms (und sowieso) sollte man bei jedem Angriff einen Späher dabei haben.

[b]Filtern[/b]
In dem Filter-Tab kann man diverse Filter einstellen und wählt aus aus welchem Dorf Angriffe geschickt werden und stellt die langsamste Einheit ein.

Ich denke die anderen Filter sind selbsterklärend, auf jeder Zeile kann man einen Wert eintragen und den Vergleichsvorgang auswählen.

Default ist mein Lieblingsfilter: Spieler, die irgendetwas haben (durch einen Bug werden Dörfer wo garnichts war sowieso nicht angezeigt, falls jemand die sehen will bitte bescheid geben).
Zusätzlich hat sich für mich auch dieser bewährt: Default bis auf: Spieler+Barbaren und Mindest-Loot *oder* Mindest-Erspähte über 300.

[b]Angreifen[/b]
Dies ist streng genommen optional, aber für die Übersichtlichkeit gut wenn man viele Angriffe macht.
Wenn du einen Angriff losschickst wähle in den Filtern den Einheitentyp der langsamsten Einheit, wechsel in das andere Tab und klicke dann bei dem angegriffenen Ziel auf den Button. Dann versteckt das Programm das Ziel für die Zeitdauer bis die Truppe beim Ziel eintrifft.

[b]Entwicklungsstand[/b]
Alpha. Das Programm ist noch sehr ungeschliffen und hat nur grundlegende Funktionen. Eventuelle Probleme kann ich aber i.d.R. schnell beheben. Ich benutze es jetzt seit einigen Wochen für dutzende Angriffe pro Tag und hatte bisher keine Probleme. Es ist auch nur Englisch, aber es kommen insgesamt nur 20 Wörter oder so vor, ich hoffe das geht. Der Code hat die Qualität, die Code hat, wenn man im 3/4-Schlaf Code schreibt, ist also extrem peinlich. Funktionieren tut er aber trotzdem ;)

[b]Bekannte auffällige Probleme[/b]
1. Nicht direkt ein Bug, aber nervt: Man muss jeden Bericht mit seinem Browser abspeichern.
2. Ziele wo nichts geholt wurde und nichts zu sehen war werden unterschlagen. Da dies ein nützlicher Bug ist habe ich ihn bisher nicht gesucht, aber falls das jemanden stört einfach bescheid geben. 
3. Das vertikale Arrangement hat einen Bug

[spoiler=Changelog]
[b]alpha1 26.10.2015[/b]
- erste veröffentlichte Version
[b]alpha2 26.10.2015[/b]
- batch-Datei für Windows
[b]alpha3 27.10.2015[/b]
- diverse kleine Komfort-Verbesserungen
- Zeigt nun auch Wall-Stufe und Einheitenanzahl am Ziel an
- Kann nach Wall-Stufe und Einheitenanzahl filtern
[b]alpha4 29.10.2015[/b]
- diverse kleine Komfort-Verbesserungen
- Bugfixe für Loot und erspähte Res
- Filtern nach Entfernung und min. Loot (Einheit wählbar)
- erspähte Res anzeigen
[b]alpha5 10.11.2015[/b]
- Berücksichtigt jetzt Speicher und Versteck
- Verbesserte Anzeige von Ziel-Koordinaten und erwartetem Loot
- Zeigt Loot vom letzten mal an
- Neues DB-Schema
[b]alpha6 17.11.2015[/b]
- Neues Tab um mehr Filter flexibler und schöner einstellen zu können
- Kleinigkeiten
[b]alpha7 21.11.2015[/b]
- Unterstützt jetzt mehrere Dörfer
- Bessere Ansicht der Filter
- Koordinaten der Ziele sind jetzt für Copy&Paste geeignet
- Tabs werden jetzt falls nötig automatisch neu gezeichnet
- Importierte Dateien werden jetzt verschoben - dies verhindert automatisch, dass die gleichen Reporte jedes mal neu importiert werden
[/spoiler]

[b]Beziehung zu InnoGames/Die Stämme; Spielregeln[/b]
Dieses Programm ist nicht von InnoGames geprüft, authorisiert, empfohlen oder sonst irgendwas. Da es aber keinerlei Handlungen in DS auslöst ist es nicht Gegenstand der DS-Spielregeln.
