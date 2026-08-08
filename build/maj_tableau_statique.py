#!/usr/bin/env python3
"""Script ponctuel (2026-08-08) : met a jour les cellules Serveurs/Paiement
anonyme du tableau comparatif hardcode dans index.html et comparatif.html,
pour qu'elles restent coherentes avec site/data/vpns.json apres l'ajout de
donnees precedemment 'non communique'. index.html/comparatif.html restent
ecrits a la main (voir CLAUDE.md) -- ce script est un patch chirurgical sur
2 cellules par fournisseur, pas un generateur complet, pour ne pas toucher
au reste du HTML redige a la main.
"""
import json
import re
from pathlib import Path

RACINE = Path(__file__).parent.parent
DATA = RACINE / "site" / "data" / "vpns.json"


def fmt_serveurs(vpn):
    parts = []
    if vpn.get("nb_serveurs"):
        parts.append(f"{vpn['nb_serveurs']:,}".replace(",", " ") + " serveurs")
    if vpn.get("nb_pays"):
        parts.append(f"{vpn['nb_pays']} pays")
    elif vpn.get("nb_emplacements"):
        parts.append(f"{vpn['nb_emplacements']} emplacements")
    return ", ".join(parts) if parts else '<span class="non-renseigne">non communique</span>'


def fmt_paiement(vpn):
    p = vpn.get("paiement_anonyme")
    return p if p else '<span class="non-renseigne">non communique</span>'


def main():
    donnees = json.loads(DATA.read_text(encoding="utf-8"))
    for fichier in ["index.html", "comparatif.html"]:
        chemin = RACINE / "site" / fichier
        html = chemin.read_text(encoding="utf-8")
        for vpn in donnees["vpns"]:
            vid = vpn["id"]
            serveurs = fmt_serveurs(vpn)
            paiement = fmt_paiement(vpn)
            # Isole le <tr> de ce fournisseur (ancre : le lien vers sa fiche).
            motif = re.compile(
                r'(<td class="nom-vpn">\s*<a href="/avis/' + re.escape(vid) + r'\.html".*?</tr>)',
                re.DOTALL,
            )
            m = motif.search(html)
            if not m:
                print(f"[!!] {fichier} : ligne introuvable pour {vid}")
                continue
            bloc = m.group(1)
            cellules = re.findall(r"<td[^>]*>.*?</td>", bloc, re.DOTALL)
            if len(cellules) != 7:
                print(f"[!!] {fichier}/{vid} : {len(cellules)} cellules trouvees, 7 attendues, ignore")
                continue
            nouvelle_serveurs = f"<td>{serveurs}</td>"
            nouvelle_paiement = f"<td>{paiement}</td>"
            nouveau_bloc = bloc.replace(cellules[4], nouvelle_serveurs, 1).replace(
                cellules[5], nouvelle_paiement, 1
            )
            html = html.replace(bloc, nouveau_bloc, 1)
        chemin.write_text(html, encoding="utf-8")
        print(f"[ok] {fichier} mis a jour")


if __name__ == "__main__":
    main()
