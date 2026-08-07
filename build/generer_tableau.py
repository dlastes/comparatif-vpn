#!/usr/bin/env python3
"""Genere le contenu HTML statique du tableau comparatif (lignes de
<tbody>) et des fiches courtes par fournisseur, a partir de
site/data/vpns.json, et les injecte dans index.html et comparatif.html
entre des marqueurs de commentaire.

Pourquoi un rendu statique plutot que le fetch()+render JS existant
(site/js/app.js) : un moteur de recherche qui ne rend pas le JS (ou avec
delai) voyait "Chargement..." a la place du contenu qui justifie la page —
mauvais pour un site pense pour le SEO. Le HTML genere ici est maintenant
la source de verite affichee au chargement ; app.js s'appuie dessus pour
le tri interactif (il regenere le meme balisage cote client au clic sur
une colonne, voir la fonction rendreLigne() commune aux deux).

Usage: python build/generer_tableau.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

RACINE = Path(__file__).parent.parent
DATA = RACINE / "site" / "data" / "vpns.json"

DEBUT_TABLEAU = "<!-- TABLEAU:DEBUT -->"
FIN_TABLEAU = "<!-- TABLEAU:FIN -->"
DEBUT_FICHES = "<!-- FICHES:DEBUT -->"
FIN_FICHES = "<!-- FICHES:FIN -->"


def non_renseigne():
    return '<span class="non-renseigne">non communique</span>'


def fmt_prix(vpn):
    val = vpn.get("prix_mensuel_engagement_usd") or vpn.get("prix_mensuel_engagement_eur")
    if val is None:
        return non_renseigne()
    symbole = "$" if vpn.get("devise_source") == "USD" else "€"
    return f"{val:.2f} {symbole}/mois"


def fmt_audit(vpn):
    audit = vpn.get("audit_no_logs")
    if not audit:
        return non_renseigne()
    non_audite = "aucun audit" in audit.lower()
    classe = "badge-non-audite" if non_audite else "badge-audite"
    libelle = "Non audite" if non_audite else "Audite"
    return f'<span class="badge {classe}">{libelle}</span> <span class="audit-detail">{audit}</span>'


def fmt_serveurs(vpn):
    parts = []
    if vpn.get("nb_serveurs"):
        parts.append(f"{vpn['nb_serveurs']:,}".replace(",", " ") + " serveurs")
    if vpn.get("nb_pays"):
        parts.append(f"{vpn['nb_pays']} pays")
    elif vpn.get("nb_emplacements"):
        parts.append(f"{vpn['nb_emplacements']} emplacements")
    return ", ".join(parts) if parts else non_renseigne()


def fmt_paiement(vpn):
    return vpn["paiement_anonyme"] if vpn.get("paiement_anonyme") else non_renseigne()


def ligne_tableau(vpn):
    return f'''    <tr>
      <td class="nom-vpn">
        <a href="/avis/{vpn['id']}.html" class="lien-fournisseur">
          <img src="{vpn['logo']}" alt="" width="28" height="28" class="logo-vpn" loading="lazy">
          {vpn['nom']}
        </a>
      </td>
      <td class="prix">{fmt_prix(vpn)}</td>
      <td>{vpn['juridiction']}</td>
      <td>{fmt_audit(vpn)}</td>
      <td>{fmt_serveurs(vpn)}</td>
      <td>{fmt_paiement(vpn)}</td>
      <td><a href="{vpn['site_officiel']}" rel="nofollow noopener sponsored" target="_blank" class="lien-officiel">Site officiel &#8599;</a></td>
    </tr>'''


def carte_fiche(vpn):
    audit = vpn.get("audit_no_logs") or ""
    non_audite = "aucun audit" in audit.lower()
    badge = (
        '<span class="badge badge-non-audite">Non audite</span>'
        if non_audite
        else '<span class="badge badge-audite">Audite</span>'
    )
    description = vpn.get("juridiction_note") or non_renseigne()
    return f'''      <div class="carte carte-vpn">
        <div class="carte-vpn-entete">
          <img src="{vpn['logo']}" alt="Logo {vpn['nom']}" width="36" height="36" class="logo-vpn">
          <h3>{vpn['nom']}</h3>
          {badge}
        </div>
        <p>{description}</p>
        <div class="carte-vpn-liens">
          <a href="/avis/{vpn['id']}.html">Voir la fiche complete &#8594;</a>
          <a href="{vpn['site_officiel']}" rel="nofollow noopener sponsored" target="_blank">Site officiel &#8599;</a>
        </div>
      </div>'''


def injecter(chemin: Path, debut: str, fin: str, contenu: str):
    texte = chemin.read_text(encoding="utf-8")
    motif = re.compile(re.escape(debut) + r".*?" + re.escape(fin), re.DOTALL)
    remplacement = f"{debut}\n{contenu}\n    {fin}"
    if not motif.search(texte):
        raise SystemExit(f"Marqueurs {debut}/{fin} introuvables dans {chemin}")
    chemin.write_text(motif.sub(remplacement, texte), encoding="utf-8")
    print(f"[ok] {chemin.relative_to(RACINE)}")


def main():
    donnees = json.loads(DATA.read_text(encoding="utf-8"))
    vpns = donnees["vpns"]

    lignes = "\n".join(ligne_tableau(v) for v in vpns)
    fiches = "\n".join(carte_fiche(v) for v in vpns)

    for nom_fichier in ("index.html", "comparatif.html"):
        chemin = RACINE / "site" / nom_fichier
        injecter(chemin, DEBUT_TABLEAU, FIN_TABLEAU, lignes)

    injecter(RACINE / "site" / "index.html", DEBUT_FICHES, FIN_FICHES, fiches)

    print(f"{len(vpns)} fournisseurs rendus dans le tableau et les fiches courtes.")


if __name__ == "__main__":
    main()
