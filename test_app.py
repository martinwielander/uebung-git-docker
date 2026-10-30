"""Tests für app.py.  Ausführen:  python3 -m unittest -v"""
import tempfile
import unittest
from pathlib import Path

from app import begruessung, erhoehe_zaehler, lade_zaehler


class ZaehlerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.datei = Path(self.tmp.name) / "zaehler.txt"

    def tearDown(self):
        self.tmp.cleanup()

    def test_startet_bei_null(self):
        self.assertEqual(lade_zaehler(self.datei), 0)

    def test_zaehlt_hoch_und_speichert(self):
        erhoehe_zaehler(self.datei)
        self.assertEqual(erhoehe_zaehler(self.datei), 2)
        self.assertEqual(lade_zaehler(self.datei), 2)


class BegruessungTest(unittest.TestCase):
    def test_enthaelt_nummer(self):
        self.assertIn("Nr. 7", begruessung(7))


if __name__ == "__main__":
    unittest.main()
