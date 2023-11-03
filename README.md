# Anleitung für Fabi

#### 1. Checken ob **git** auf dem PC installiert ist

`git --version`

#### 2. Repository in Ordner der Wahl clonen

`cd <gewünschter_ordner>`

`git clone https://github.com/jasperschalla/birdnet.git`

#### 3. Checken ob **Anaconda** installiert ist

`conda --version`

Im ordner der Wahl, in den man das repository geclont hat, requirements.txt nutzen um environment zu erstellen:

`conda create --name <environment_name> --file requirements.txt`

<span style="color:red">Falls das Programm auf Windows ausgeführt gibt es Probleme mit dem tensorflow-macos Paket! Tensorflow-Pakete aus <i>requirements.txt</i> löschen und selber installieren.</span> 

#### 4. Audiodateien kopieren

In den Ordner `/sounds` die .wav-Dateien kopieren

#### 5. Script ausführen

Conda-Environment aktivieren:

`conda activate <environment_name>`

Und schließlich das Script ausführen:

`python analyze.py`

.csv-Datei mit Ergebnissen wird erstellt.

#### 6. UI nutzen

UI-App starten:

`streamlit run app.py`

Angezeigte URL öffnen, z.B. http://localhost:8501



