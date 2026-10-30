# Übungen: Git & Docker

Übungsprojekt: ein Mini-Webserver (`app.py`), der Besuche zählt, plus Tests (`test_app.py`).
Hier darf alles kaputtgehen – im Zweifel Ordner löschen und neu anfangen.

Alle Befehle im Terminal in diesem Ordner ausführen:

```bash
cd ~/Code/uebung-git-docker
```

---

## Teil A – Git

### Lektion 0: Einmalig einrichten

```bash
git config --global user.name "Martin Wielander"
git config --global user.email "martin.wielander@konverto.eu"
git config --global init.defaultBranch main
```

Das steht später in jedem Commit als Autor.

### Lektion 1: Das erste Repository

1. App ausprobieren: `python3 app.py`, dann http://localhost:8000 öffnen, ein paar Mal neu laden.
   Mit `Ctrl+C` beenden. Es gibt jetzt einen Ordner `data/` mit `zaehler.txt`.
2. Tests laufen lassen: `python3 -m unittest -v`
3. Repository anlegen: `git init` – es entsteht ein versteckter Ordner `.git` (das ist die ganze Historie).
4. `git status` – alles ist „untracked“ (Git kennt die Dateien noch nicht).
5. **`.gitignore` anlegen** – Dinge, die *nicht* versioniert werden sollen:
   ```
   __pycache__/
   data/
   .DS_Store
   ```
   Wieder `git status`: `data/` und `__pycache__/` sind verschwunden.
6. Dateien vormerken („stagen“): `git add .`  → `git status` zeigt sie grün.
7. Commit: `git commit -m "Erste Version der Zähler-App"`
8. Historie ansehen: `git log` (beenden mit `q`), kompakter: `git log --oneline`

> **Merksatz:** Arbeitsordner → `git add` → Staging → `git commit` → Historie.

### Lektion 2: Änderungen verfolgen und rückgängig machen

1. Ändere in `app.py` den Text in `begruessung()`, z. B. „Servus! …“.
2. `git diff` – zeigt genau, was sich geändert hat (rot = alt, grün = neu).
3. Tests laufen lassen. Schlägt einer fehl? Warum (nicht)?
4. `git add app.py` und `git commit -m "Begrüßung geändert"`
5. **Rückgängig machen üben:** Lösche irgendeine Zeile in `app.py` und speichere.
   Dann: `git restore app.py` – die Datei ist wieder wie beim letzten Commit.
6. Einen alten Stand anschauen: `git log --oneline`, dann `git show <commit-id>`.

### Lektion 3: Branches

1. Neuen Branch anlegen und wechseln: `git switch -c farbe`
2. Ändere in `app.py` das `<h1>` zu `<h1 style='color: green'>`, committen.
3. Zurück zu main: `git switch main` – die Farbe ist weg! (Sie lebt nur im Branch.)
4. `git log --oneline --graph --all` – zeigt beide Branches.
5. Zusammenführen: `git merge farbe`  →  die Änderung ist jetzt auch in main.
6. Branch aufräumen: `git branch -d farbe`

**Bonus – Merge-Konflikt provozieren:**
Lege Branch `a` an und ändere die Begrüßung, committen. Zurück auf `main`, ändere *dieselbe Zeile* anders, committen.
`git merge a` → Konflikt! Öffne `app.py`, du siehst `<<<<<<<`, `=======`, `>>>>>>>`.
Entscheide dich, Markierungen löschen, dann `git add app.py` und `git commit`.
Keine Panik: mit `git merge --abort` kommst du jederzeit zurück.

### Lektion 4 (optional): GitHub

1. Auf github.com ein neues **privates**, **leeres** Repository `uebung-git-docker` anlegen.
2. Verbinden und hochladen (GitHub zeigt dir die exakten Befehle an):
   ```bash
   git remote add origin https://github.com/<dein-name>/uebung-git-docker.git
   git push -u origin main
   ```
3. Ab jetzt: nach Commits einfach `git push`. Von einem anderen Rechner: `git clone …`, dann `git pull`.

---

## Teil B – Docker

Zuerst Docker Desktop starten (Wal-Symbol in der Menüleiste muss ruhig sein).

### Lektion 5: Das erste Image

1. Lege die Datei `Dockerfile` (ohne Endung) an:
   ```dockerfile
   # Basis: ein schlankes Linux mit Python 3.12
   FROM python:3.12-slim

   # Arbeitsordner im Container
   WORKDIR /app

   # Unseren Code in das Image kopieren
   COPY app.py test_app.py ./

   # Wo die App ihre Daten ablegt und auf welchem Port sie lauscht
   ENV DATA_DIR=/data PORT=8000
   EXPOSE 8000

   # Was beim Start des Containers ausgeführt wird
   CMD ["python", "app.py"]
   ```
2. Image bauen: `docker build -t zaehler .`  (der Punkt = „dieser Ordner“)
3. `docker images` – dein Image `zaehler` ist da.
4. Container starten: `docker run --rm -p 8000:8000 zaehler`
   - `-p 8000:8000` = Port deines Macs → Port im Container
   - `--rm` = Container nach dem Beenden wegwerfen
5. Im Browser http://localhost:8000 öffnen. Läuft – aber diesmal in Linux, nicht auf macOS!
6. In einem zweiten Terminal: `docker ps` zeigt laufende Container. Beenden mit `Ctrl+C`.
7. Commit nicht vergessen: `git add Dockerfile && git commit -m "Dockerfile hinzugefügt"`

### Lektion 6: Volumes – Daten überleben den Container

1. Container starten, ein paar Mal neu laden, beenden, neu starten:
   **Der Zähler fängt wieder bei 1 an.** Container sind Wegwerf-Ware.
2. Mit Volume starten:
   ```bash
   docker run --rm -p 8000:8000 -v zaehler-daten:/data zaehler
   ```
   Jetzt bleibt der Zähler erhalten, auch nach Neustart.
3. `docker volume ls` zeigt das Volume `zaehler-daten`.

> **Merksatz:** Code gehört ins Image, Daten gehören in ein Volume.

### Lektion 7: Docker Compose – alles in einer Datei

Statt langer `docker run`-Befehle beschreibst du alles in `compose.yaml`:

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - zaehler-daten:/data
    restart: unless-stopped

volumes:
  zaehler-daten:
```

- Starten: `docker compose up --build`  (im Hintergrund: zusätzlich `-d`)
- Logs ansehen: `docker compose logs -f`
- Stoppen: `docker compose down`
- **Tests im Container:** `docker compose run --rm app python -m unittest -v`
  → getestet wird in genau der Umgebung, die später auch auf dem Server läuft.

Committen!

### Lektion 8: Entwickeln mit Docker

Nervig: nach jeder Code-Änderung neu bauen. Lösung für die Entwicklung – den Code als Volume einbinden.
Lege `compose.dev.yaml` an:

```yaml
services:
  app:
    volumes:
      - .:/app
```

Starten mit: `docker compose -f compose.yaml -f compose.dev.yaml up --build`
Ändere die Begrüßung, Container neu starten (`docker compose restart`) – ohne Neubau aktiv.

### Lektion 9: Deployen (Gedankenexperiment / echter Server)

Auf einem Linux-Server mit Docker reicht dann:

```bash
git clone https://github.com/<dein-name>/uebung-git-docker.git
cd uebung-git-docker
docker compose up -d --build
```

Update später: `git pull && docker compose up -d --build`
Das ist der ganze Ablauf: **Code ändern → testen → commit → push → auf dem Server pull + up.**

---

## Spickzettel

| Git | |
|---|---|
| `git status` | Was ist geändert? |
| `git add <datei>` / `git add .` | Für Commit vormerken |
| `git commit -m "…"` | Stand speichern |
| `git log --oneline --graph --all` | Historie |
| `git diff` | Ungespeicherte Änderungen |
| `git restore <datei>` | Änderung verwerfen |
| `git switch -c <name>` / `git switch <name>` | Branch anlegen / wechseln |
| `git merge <name>` | Branch übernehmen |
| `git push` / `git pull` | Mit GitHub abgleichen |

| Docker | |
|---|---|
| `docker build -t <name> .` | Image bauen |
| `docker run --rm -p 8000:8000 <name>` | Container starten |
| `docker ps` / `docker images` | Container / Images anzeigen |
| `docker compose up --build -d` | Alles bauen + starten |
| `docker compose logs -f` | Logs |
| `docker compose down` | Stoppen |
| `docker compose run --rm app <befehl>` | Einmal-Befehl im Container |
| `docker system prune` | Aufräumen (ungenutzte Images/Container) |
