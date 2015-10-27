[b]Pytw, das Angriffstool[/b]

[b]Funktionen[/b]
- Liest Spionage- und Kampfreporte und speichert sie in eine Datenbank
- Filtern zwischen Spielern und Barbaren
- Filtern nach Wall-Stufe und Einheitenanzahl (min, max, oder genaue Zahl)
- Zeigt die möglichen Ziele tabelarisch an
- Berechnet anhand der Gebäude, der Entfernung, Geschwindigkeit der einzusetzenden Einheit und des Berichtsalters wieviel man bei dem jeweiligen Ziel mitnehmen kann
- Kann nur Spieler anzeigen (default), nur Barbaren, oder beides
- Programm arbeitet komplett auf eurem Rechner und ist nicht von Webdiensten oder irgendwas abhängig (und es nutzt solche auch nicht)
- Freie Software, d.h. kann gemäß der AGPL-Lizenz von jedem verändert oder geteilt (wiederveröffentlicht) werden.

[b]Bugreports, Vorschläge, Kommentare[/b]
Per Die-Stämme-PM, hier im Stammesforum, oder per Mail an steffen@schaumburger.info
Viele Funktionen ließen sich ganz leicht einbauen also ruhig sagen was ihr braucht.

[spoiler=Anforderungen]Python 3.4 oder höher und PyQt 5 (verfügbar für alle Betriebssysteme)
Links zum Download sind in den Installationsabschnitten[/spoiler]

[spoiler=Installation - Windows (64 bit)]Python downloaden und installieren: https://www.python.org/ftp/python/3.4.3/python-3.4.3.amd64.msi
Die Stämme erlaubt offenbar keine Links zu exe-Dateien. Daher müsst ihr das Leerzeichen im folgenden Link in "x64 exe" durch einen Punkt ersetzen.
PyQt downloaden und installieren: http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.5.1/PyQt5-5.5.1-gpl-Py3.4-Qt5.5.1-x64 exe/download
Jetzt weitermachen bei "Installation - allgemeiner Teil"[/spoiler]

[spoiler=Installation - Windows (32 bit)]Python downloaden und installieren: https://www.python.org/ftp/python/3.4.3/python-3.4.3.msi
Die Stämme erlaubt offenbar keine Links zu exe-Dateien. Daher müsst ihr das Leerzeichen im folgenden Link in "x32 exe" durch einen Punkt ersetzen.
PyQt downloaden und installieren: http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.5.1/PyQt5-5.5.1-gpl-Py3.4-Qt5.5.1-x32 exe/download
Jetzt weitermachen bei "Installation - allgemeiner Teil"[/spoiler]

[spoiler=Installation - andere Betriebssysteme]Bitte anfragen.[/spoiler]

[spoiler=Installation - allgemeiner Teil]Das Programm selbst runterladen, entweder den alpha-Release oder die aktuelle Entwicklerversion:
aktuelle alpha3: https://github.com/steffen123/pytw/archive/alpha3.zip
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
Ganz normal im Browser einen Spionage- oder Angriffsbericht aufrufen. Diesen in das "import/reports/" Verzeichnis im Installationsverzeichnis abspeichern. Dies muss für jeden Bericht gemacht werden. Bitte nur die HTML-Datei abspeichern, nicht die komplette Seite (Firefox zumindest erlaubt das, falls andere Browser das nicht können halt die komplette Seite abspeichern). Der Dateiname ist völlig egal. Ich numeriere sie einfach durch. Es ist egal ob Bericht mehrfach gespeichert sind oder ob mehrere Berichte zu einem Ziel vorhanden sind - das Programm ignoriert ältere Berichte falls nötig.

Nun im Programm "Import Reports" anklicken. Das Programm verarbeitet nun alle Berichte und zeigt dann die in Frage kommenden Ziele an.

Bisher lädt das Programm jedes mal wenn man importiert sämtliche Berichte neu. Auf meinem über 5 Jahre alten PC dauert das für 300 Berichte knapp 5 Sekunden, aber eine Beschleunigung davon werde ich bald implementieren.
Für optimale Nutzung des Programms (und sowieso) sollte man bei jedem Angriff einen Späher dabei haben.

[b]Angreifen[/b]
Dies ist optional, aber für die Übersichtlichkeit gut wenn man viele Angriffe macht.
Für jedes Ziel sind rechts eine Reihe von Buttons. Wenn du einen Angriff losschickst klicke den entsprechenden Button für die langsamste Einheit (Bögen und Äxte sind so schnell wie Speere) am. Dann versteckt das Programm das Ziel für die Zeitdauer bis die Truppe beim Ziel eintrifft.

[b]Entwicklungsstand[/b]
Alpha. Das Programm ist noch sehr ungeschliffen und hat nur grundlegende Funktionen. Eventuelle Probleme kann ich aber i.d.R. schnell beheben. Ich benutze es jetzt seit einigen Tagen für dutzende Angriffe pro Tag und hatte bisher keine Probleme. Es ist auch nur Englisch, aber es kommen insgesamt nur 20 Wörter oder so vor, ich hoffe das geht.

[b]Bekannte auffällige Probleme[/b]
1. Nicht direkt ein Bug, aber nervt etwas: Man muss jeden Bericht mit seinem Browser abspeichern.

[spoiler=Changelog]
[b]alpha1 26.10.2015[/b]
- erste veröffentlichte Version
[b]alpha2 26.10.2015[/b]
- batch-Datei für Windows
[b]alpha3 27.10.2015[/b]
- diverse kleine Komfort-Verbesserungen
- Zeigt nun auch Wall-Stufe und Einheitenanzahl am Ziel an
- Kann nach Wall-Stufe und Einheitenanzahl filtern[/spoiler]

[b]Beziehung zu InnoGames/Die Stämme; Spielregeln[/b]
Dieses Programm ist nicht von InnoGames geprüft, authorisiert, empfohlen oder sonst irgendwas. Da es aber keinerlei Handlungen in DS auslöst ist es erlaubt.
