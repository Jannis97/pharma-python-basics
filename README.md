# Python Grundlagen für Pharma-Anwendungen

Dieses Repository enthält Lernmaterialien und Übungen für Python-Programmierung im pharmazeutischen Kontext. Es richtet sich an Einsteiger und fortgeschrittene Anfänger, die Python für Datenanalyse, Berechnungen und Automatisierungen im pharmazeutischen Bereich nutzen möchten.

## Struktur des Repositories

```
pharma-python-basics/
├── 0_Syntax_basics/           # Grundlegende Python-Syntax
│   ├── 0_grundlagen.py        # Einführung in Python
│   ├── 1_datentypen.py        # Basisdatentypen in Python
│   ├── 2_collection.py        # Collection-Datentypen (Listen, Tupel, Dictionaries)
│   ├── 3_kontrollstrukturen.py # Bedingte Anweisungen und Schleifen
│   ├── 4_funktionen.py        # Funktionsdefinition und -verwendung
│   ├── 5_einfache_gehaltsbestimmung.py # Anwendungsbeispiel: Kalibrationsreihe
│   ├── 6_load_csv.py          # Daten aus CSV-Dateien laden
│   ├── exercises_syntax.py    # Übungen zur Syntax
│   ├── exercises_data_processing.py # Übungen zur Datenverarbeitung
│   ├── solutions_syntax.py    # Lösungen zu Syntax-Übungen
│   └── solutions_data_processing.py # Lösungen zu Datenverarbeitungs-Übungen
│
├── simulated_data/            # Simulierte Datensätze für Übungen
│   └── data/                  # CSV-Dateien
│       ├── chromatogram-01.csv
│       ├── chromatogram-02.csv
│       └── ...
│
├── data_generation.py         # Skript zur Generierung von Beispieldaten
├── hello.py                   # Einfaches Beispielskript
└── Synthax_basics.pdf         # Begleitende Dokumentation
```

## Voraussetzungen

Um mit diesem Repository zu arbeiten, benötigen Sie:

1. Python 3.7 oder höher
2. Folgende Python-Bibliotheken:
   - numpy
   - pandas
   - matplotlib
   - scipy

Installation der benötigten Pakete:

```bash
pip install numpy pandas matplotlib scipy tqdm
```

## Einrichtung einer virtuellen Umgebung in PyCharm

Eine virtuelle Umgebung (venv) ist eine isolierte Python-Umgebung, die unabhängig von der systemweiten Python-Installation ist. Wir empfehlen die Verwendung einer virtuellen Umgebung für dieses Projekt.

### Erstellen und Aktivieren einer virtuellen Umgebung in PyCharm:

1. **Öffnen Sie das Projekt in PyCharm**

2. **Virtuelle Umgebung erstellen:**
   - Gehen Sie zu `File` > `Settings` (Windows/Linux) oder `PyCharm` > `Preferences` (macOS)
   - Navigieren Sie zu `Project: [Projektname]` > `Python Interpreter`
   - Klicken Sie auf das Zahnrad-Symbol und wählen Sie `Add...`
   - Wählen Sie `Virtualenv Environment` und dann `New environment`
   - Wählen Sie einen Speicherort für die virtuelle Umgebung (standardmäßig `.venv` im Projektverzeichnis)
   - Wählen Sie die gewünschte Python-Version
   - Klicken Sie auf `OK`

3. **Pakete in der virtuellen Umgebung installieren:**
   - Nach der Erstellung der virtuellen Umgebung können Sie entweder:
     - Die automatische Paketinstallation über PyCharm verwenden: 
       - Gehen Sie zu `File` > `Settings` > `Project: [Projektname]` > `Python Interpreter`
       - Klicken Sie auf `+` und suchen Sie nach den benötigten Paketen
     - Oder das Terminal in PyCharm öffnen (`View` > `Tool Windows` > `Terminal`) und die Pakete manuell installieren:
       ```bash
       pip install numpy pandas matplotlib scipy tqdm
       ```

4. **Virtuelle Umgebung aktivieren (wenn Sie das Terminal außerhalb von PyCharm verwenden):**
   - In Windows:
     ```
     .venv\Scripts\activate
     ```
   - In macOS/Linux:
     ```
     source .venv/bin/activate
     ```

5. **Virtuelle Umgebung deaktivieren:**
   ```
   deactivate
   ```

Wenn Sie PyCharm verwenden, wird die virtuelle Umgebung automatisch für Ihr Projekt aktiviert, sodass Sie keine manuellen Aktivierungsbefehle verwenden müssen.

## Einführung in die Syntax-Grundlagen

Der Ordner `0_Syntax_basics` enthält die grundlegenden Python-Konzepte:

1. **Python-Grundlagen** (0_grundlagen.py):
   - Was ist Python?
   - "Hello World"-Beispiel
   - Grundlegende Syntax-Regeln
   - Entwicklungsumgebungen
   - Installation und Paketverwaltung

2. **Basisdatentypen** (1_datentypen.py):
   - Int, Float, Boolean, String
   - Typumwandlung (Casting)

3. **Collection-Datentypen** (2_collection.py):
   - Listen, Tupel, Dictionaries
   - Operationen mit Collections

4. **Kontrollstrukturen** (3_kontrollstrukturen.py):
   - Bedingte Anweisungen (if, elif, else)
   - Schleifen (for, while)

5. **Funktionen** (4_funktionen.py):
   - Funktionsdefinition und -aufruf
   - Parameter und Rückgabewerte

6. **Anwendungsbeispiel**: Gehaltsbestimmung mit Kalibrationsgerade (5_einfache_gehaltsbestimmung.py)

7. **CSV-Daten laden** (6_load_csv.py):
   - Einlesen von CSV-Dateien mit pandas
   - Grundlegende Datenvisualisierung

## Übungen

Das Repository enthält Übungen für:

1. **Syntax-Grundlagen** (exercises_syntax.py):
   - Variablen und Operationen
   - Bedingungen und Schleifen
   - Datenstrukturen

2. **Datenverarbeitung** (exercises_data_processing.py):
   - Dateien und Verzeichnisse
   - Daten laden und verarbeiten
   - Visualisierung von Daten

Die Lösungen zu diesen Übungen finden Sie in den jeweiligen Solutions-Dateien.

## Simulierte Daten

Im Ordner `simulated_data/data/` finden Sie simulierte Chromatogramm-Daten, die für die praktischen Übungen verwendet werden können.

## Verwendung

1. Beginnen Sie mit den Grundlagenfiles (0_grundlagen.py bis 4_funktionen.py).
2. Studieren Sie die Anwendungsbeispiele (5_einfache_gehaltsbestimmung.py, 6_load_csv.py).
3. Bearbeiten Sie die Übungen in exercises_syntax.py und exercises_data_processing.py.
4. Vergleichen Sie Ihre Lösungen mit den Lösungsdateien.

## Weiterführende Ressourcen

Neben den Materialien in diesem Repository können folgende Ressourcen hilfreich sein:

- [pandas-Dokumentation](https://pandas.pydata.org/docs/)
- [matplotlib-Dokumentation](https://matplotlib.org/stable/contents.html)
- [NumPy-Dokumentation](https://numpy.org/doc/stable/)
