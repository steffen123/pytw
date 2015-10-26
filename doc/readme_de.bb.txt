Pytw, das Angriffstool

[b]Funktionen[/b]
- Liest Spionage- und Kampfreporte und speichert sie in eine Datenbank
- Erkennt sichere Ziele (d.h. ohne Truppen oder Wall)
- Berechnet anhand der Gebäude, der Entfernung und des Berichtsalters wieviel man bei dem jeweiligen Ziel raubbar ist
- Kann nur Spieler anzeigen (default), nur Barbaren, oder beides
- Programm arbeitet komplett auf eurem Rechner und ist nicht von Webdiensten oder irgendwas abhängig (und es nutzt solche auch nicht)
- Freie Software, d.h. kann gemäß der AGPL-Lizenz von jedem verändert oder geteilt (wiederveröffentlicht) werden.

[b]Bugreports, Wünsche, Kontakt[/b]
Per Die-Stämme-PM, hier im Stammesforum, oder per Mail an [mail]steffen@schaumburger.info[/mail].
Viele Funktionen ließen sich ganz leicht einbauen also ruhig sagen was ihr braucht.

[b]Anforderungen[/b]
Software: Python 3.4 oder höher und PyQt 5 (verfügbar für alle Betriebssysteme)

[b]Installation - Windows (64 bit)[/b]
Python downloaden und installieren: https://www.python.org/ftp/python/3.4.3/python-3.4.3.amd64.msi
PyQt downloaden und installieren: http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.5.1/PyQt5-5.5.1-gpl-Py3.4-Qt5.5.1-x64.exe/download
Jetzt weitermachen bei "Installation - allgemeiner Teil"

[b]Installation - Windows (32 bit)[/b]
Python downloaden und installieren: https://www.python.org/ftp/python/3.4.3/python-3.4.3.msi
PyQt downloaden und installieren: http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.5.1/PyQt5-5.5.1-gpl-Py3.4-Qt5.5.1-x32.exe/download
Jetzt weitermachen bei "Installation - allgemeiner Teil"

[b]Installation - andere Betriebssysteme[/b]
Bitte anfragen.

[b]Installation - allgemeiner Teil"[/b]
Das Programm selbst runterladen, entweder den alpha-Release oder die aktuelle Entwicklerversion:
alpha1: TODO
aktuelle Entwicklerversion: https://github.com/steffen123/pytw/archive/master.zip

[b]Installation (sonstige)[/b]
Hängt vom Betriebssystem ab. Bitte Info und ich schreib die Anleitung für das jeweilige Betriebssystem. Brauche diese Details:
- Betriebssystem (z.B. Gentoo Linux oder Windows)
- Version des Betriebssystems
- Falls bekannt: die Bitness (32bit oder 64bit)

[b]Starten[/b]
Im Installationsverzeichnis pytw.pyw doppelklicken.

[b]Bedienung[/b]
Ganz normal im Browser einen Spionage- oder Angriffsbericht aufrufen. Diesen in das "import/reports/" Verzeichnis im Installationsverzeichnis abspeichern. Dies muss für jeden Bericht gemacht werden. Bitte nur die HTML-Datei abspeichern, nicht die komplette Seite (Firefox zumindest erlaubt das, falls andere Browser das nicht können halt die komplette Seite abspeichern). Der Dateiname ist völlig egal. Ich numeriere sie einfach durch. Es ist egal ob Bericht mehrfach gespeichert sind oder ob mehrere Berichte zu einem Ziel vorhanden sind - das Programm ignoriert ältere Berichte falls nötig.

Nun im Programm "Import Reports" anklicken. Das Programm verarbeitet nun alle Berichte und zeigt dann die in Frage kommenden Ziele an. Die Drop-Down-Boxen oben sind zur Filterung.

Bisher lädt das Programm jedes mal wenn man importiert sämtliche Berichte neu. Auf meinem über 5 Jahre alten PC dauert das für 300 Berichte knapp 5 Sekunden, aber eine Beschleunigung davon werde ich bald implementieren.

[b]Entwicklungsstand[/b]
Alpha. Das Programm ist noch sehr ungeschliffen und hat nur grundlegende Funktionen. Eventuelle Probleme kann ich aber i.d.R. schnell beheben. Ich benutze es jetzt seit einigen Tagen für dutzende Angriffe pro Tag und hatte bisher keine Probleme.

[b]Bekannte auffällige Probleme[/b]
1. Nicht direkt ein Bug, aber nervt etwas: Man muss jeden Bericht mit seinem Browser abspeichern.

[b]Changelog[/b]
alpha1: erste veröffentlichte Version

[b]Beziehung zu InnoGames/Die Stämme; Spielregeln[/b]
Dieses Programm ist nicht von InnoGames geprüft, authorisiert, empfohlen oder sonst irgendwas. So wie ich die Regeln verstehe kann ich mir aber nicht vorstellen, dass irgendwer auch nur auf Idee kommen könnte, dass dieses Tool etwas unerlaubtes macht.
