"""Mini-Webserver zum Üben: zählt Besuche und speichert den Zähler in einer Datei.

Nur Python-Standardbibliothek, also keine Installation nötig.
Starten:  python3 app.py   →  http://localhost:8000
"""
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# Über Umgebungsvariablen einstellbar – wichtig später für Docker.
DATA_DIR = Path(os.environ.get("DATA_DIR", "data"))
PORT = int(os.environ.get("PORT", "8000"))
ZAEHLER_DATEI = DATA_DIR / "zaehler.txt"


def lade_zaehler(datei: Path) -> int:
    if not datei.exists():
        return 0
    return int(datei.read_text().strip() or 0)


def erhoehe_zaehler(datei: Path) -> int:
    anzahl = lade_zaehler(datei) + 1
    datei.parent.mkdir(parents=True, exist_ok=True)
    datei.write_text(str(anzahl))
    return anzahl


def begruessung(anzahl: int) -> str:
    return f"ServusMain! Du bist Besucher Nr. {anzahl}."


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        text = begruessung(erhoehe_zaehler(ZAEHLER_DATEI))
        body = f"<html><body><h1>{text}</h1></body></html>".encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    print(f"Server läuft auf http://localhost:{PORT}  (Daten in {DATA_DIR.resolve()})")
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
