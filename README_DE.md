Mit diesem Tool erzeugt ihr eine distortion.json um die Verzerrung eurer Webcams in Autodarts zu entfernen. Leider benötigt ihr hierfür eine Computer mit installiertem Linux und einer Desktop Umgebung.

Ich werde später prüfen, ob ich es auch unter Windows laufen lassen kann und versuchen, eine Raspberry Pi Version zu bauen. Wir werden an einer Lösung arbeiten, mit der man das Tool auch auf einem Desktop-losen Gerät wie dem Pi nutzen kann.

### Anferderungen and Installation

Als erstes wird ein Schbrettmuster benötigt (ihr könnt euch eins ausdrucken), welches ihr so flach wie möglich auf eine passende Unterlage klebt.
Die Oberfläche muss absolut flach sein, da sonst die Kalibrierung nicht korrekt funktioniert.

Ihr könnt folgendes Muster benutzen https://docs.opencv.org/4.5.2/pattern.png

Das Tool wurde in Python geschrieben, welches ihr zuvor installiern müsst, falls ihr das noch nicht bereits getan habt. Da das Programm Fenster öffnet in dem ihr sehen könnt, was die Kmaera aktuell aufnimmt, benötigt ihr ein Dekstop Umgebung wie zBsp. Ubuntu Desktop oder Raspberry Pi mit installiertem Desktop


Viele System kommen bereits mit einem vorinstallieren Python

Mit folgendem Befehl könnt ihr prüfen ob python korrekt installiert ist

    python3 -V

Sieht die Ausgabe so, oder so ähnlich aus, ist alles in Ordnung

    Python 3.8.10

Bitte beachtet, das mindestens Python Version 3.5.x benötigt wird.

Hier sind zwei gute Anleitungen für Ubuntu und Raspberry Pi falls ihr Python installieren müsst 

Ubuntu: https://docs.python-guide.org/starting/install3/linux/

Raspberry: https://projects.raspberrypi.org/en/projects/generic-python-install-python3#linux

Zusätzlich wird git benötigit. Dies könnt ihr mit folgendem Befehl prüfen.

    git --version

Sieht die Asugabe so, oder so ähnlich aus, ist alles in Ordnung

    git version 2.25.1

Falls nicht könnt ihr git über den Paketmanager von Ubuntu oder Raspberry nachinstallieren. 
Benutzt für Ubuntu und Raspberry dazu einfach folgenden Befehlen

    sudo apt-get update
    sudo apt-get install git-all
    
Danach könnt ihr mit dem voherigen Befehl erneut prüfen ob git nun korrekt installiert wurde.

Wir benötigen den Paketmanager für Python

    sudo apt-get install python3-pip

Danach installieren wir openCV und die tqdm Bibliothek die ebenfalls benötigt weredn

    pip3 install tqdm opencv-python

Nun klonen wir uns da Projekt von GitHUB...

    git clone https://github.com/autodarts/cam-calibration.git

...und  wechseln in das Verzeichnis

    cd cam-calibration

## Kalibrierung

Bitte versichert euch, das die Kamera(s) die ihr kalibrieren wollt, korrekt mit dem PC verbunden sind. Es können bis zu drei Kameras gleichzeitig auf eurem Dartboard kalibriert werden.
Als nächstes benötigt ihr das zuvor vorbereitete Schachbrettmuster. Ihr müsst in der Lage sein, dieses vor die Kameras auf dem Dartbrett zu heben. (s.h. Bilder weiter untern)

Sobald ihr das Tool startet, öffnet sich für jede angegeben Kamera ein eigenes Fenster.
Danach wird damit begonnen, jede Sekunde ein Bild mit jeder Kamera zu schießen. Diese werden dann im Ordner calibrationImages mit entsprechenden Unterordnern für jede KameraID abgespeichert
Je mehr Bilder ihr aufnehmt, umso genauer wird die distortion.json
(Mit 30-50 Bilder bekommt ihr bereits ein sehr gutes Ergebnis.)

Hebt das Muster immer so, dass es vollständig auf den Kameras zu sehen ist. Ihr könnt das in den Fenstern kontrollieren. versucht nun so viele Bilder aus möglichst vielen unterschiedlichen Richtungen und Winkeln aufzunehmen.
Hebt es zBsp. Flach auf das Brett, dreht es, neigt es zu den Kameras usw.

Hier seht ihr ein paar Beispiele, we es aussehen sollte:

<img src="https://learnopencv.com/wp-content/uploads/2020/02/calibration-patterns.gif" width="40%" height="40%">

<img src="examplePictures/img_1920x1080_38_cam1.jpg" width="40%" height="40%">
<img src="examplePictures/img_1920x1080_38_cam2.jpg" width="40%" height="40%">
<img src="examplePictures/img_1920x1080_38_cam3.jpg" width="40%" height="40%">

Habt ihr alles vorbereitet, könnt ihr das Tool mit folgendem Befehl starten
Das Tool bietet mehrer Einstellmöglichkeiten

    python3 main.py generate -camIds 0 2 3 -fps 30 -w 800 -h 600

Dieser Befehl nimmt alle 5 Sekunden Bilder mit 30 fps und einer Auflösung von 800x600 auf. Ihr könnt die Auflösung ändern, indem ihr die Werte -w und -h ändert.
Um herauszufinden welche Kamera angeschlossen und erkannt wurden, und welche KameraIDs diese haben, benutzt folgenden Befehl

    v4l2-ctl --list-devices

Falls ihr v4l2-ctl nicht installiert habt, könnt ihr dieses für Ubuntu und Raspberry mit folgenden Befehl tun.

    sudo apt-get install v4l-utils

Ersetzt die Nummer hinter -camIds mit euren IDs. Ihr könnt eine, zwei oder drei IDs angeben, je nachdem welche oder wieviele Kameras ihr kalibrieren wollt.

Nach dem Start sollte für jede angegeben ID ein seperates Fenster erscheinen und es wir begonnen regelmäßig Bilder aufzunehmen. Da erkennt ihr daran, das die Fenster kurz mit einem grünen Rahmen aufblitzen.

Habt ihr alle Bilder aufgenommen, beendet das Programm indem ihr ESC oder Strg+C auf der KOmmandozeile eintippt.

### Erstellung der  n

Mit folgendem Befehl beginnt ihr mit der Erstellung der distortion.json

    python3 main.py distortion -w 800 -h 600

Hier müsst ihr wieder die gleiche Auflösung wie bei der Kalibrierung oben benutzen. Falls nicht, wird die Erstellung nicht funktionieren.

Nach Abschluss findet ihr eine distortion.json im Ordner, Kopiert diese in euren .autodarts Ordner und startet die Autodarts neu.
    
    mv distortion.json ~/.autodarts

Nun könnt ihr in Autodarts unter Calibration prüfen ob die Kalibrierung erfolgreich war.