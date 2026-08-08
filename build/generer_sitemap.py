#!/usr/bin/env python3
"""Genere site/sitemap.xml a partir des pages statiques + des fiches VPN."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import SITE_URL

RACINE = Path(__file__).parent.parent
DATA = RACINE / "site" / "data" / "vpns.json"
SORTIE = RACINE / "site" / "sitemap.xml"

PAGES_FIXES = [
    "/",
    "/comparatif.html",
    "/methodologie.html",
    "/confidentialite.html",
    "/guides/",
    "/guides/quest-ce-qu-un-vpn.html",
    "/guides/juridiction-vpn.html",
    "/guides/comprendre-audit-no-logs.html",
    "/guides/paiement-anonyme-vpn.html",
    "/guides/vpn-gratuit.html",
]


def main():
    donnees = json.loads(DATA.read_text(encoding="utf-8"))
    urls = list(PAGES_FIXES) + [f"/avis/{v['id']}.html" for v in donnees["vpns"]]

    items = "\n".join(
        f"  <url><loc>{SITE_URL}{u}</loc></url>" for u in urls
    )
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{items}
</urlset>
'''
    SORTIE.write_text(xml, encoding="utf-8")
    print(f"[ok] {SORTIE.relative_to(RACINE)} ({len(urls)} URLs)")


if __name__ == "__main__":
    main()
