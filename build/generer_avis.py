#!/usr/bin/env python3
"""Genere site/avis/<id>.html a partir de site/data/vpns.json.

Une fiche par fournisseur, avec chaque donnee affichee telle quelle (jamais
de valeur devinee pour combler un champ absent — voir site/methodologie.html
et le champ note_methodologie du JSON source).

Usage: python build/generer_avis.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import SITE_URL, ASSET_VERSION

RACINE = Path(__file__).parent.parent
DATA = RACINE / "site" / "data" / "vpns.json"
SORTIE = RACINE / "site" / "avis"


def non_renseigne(html=True):
    if html:
        return '<span class="non-renseigne">non communique</span>'
    return "non communique"


def fmt_prix(vpn):
    val = vpn.get("prix_mensuel_engagement_usd") or vpn.get("prix_mensuel_engagement_eur")
    if val is None:
        return non_renseigne()
    symbole = "$" if vpn.get("devise_source") == "USD" else "€"
    return f"{val:.2f} {symbole}/mois <span>avec engagement</span>"


def fmt_prix_sans_engagement(vpn):
    val = vpn.get("prix_mensuel_sans_engagement_usd") or vpn.get("prix_mensuel_sans_engagement_eur")
    if val is None:
        return non_renseigne()
    symbole = "$" if vpn.get("devise_source") == "USD" else "€"
    return f"{val:.2f} {symbole}/mois"


def fmt_serveurs(vpn):
    parts = []
    if vpn.get("nb_serveurs"):
        parts.append(f"{vpn['nb_serveurs']:,}".replace(",", " ") + " serveurs")
    if vpn.get("nb_pays"):
        parts.append(f"{vpn['nb_pays']} pays")
    elif vpn.get("nb_emplacements"):
        parts.append(f"{vpn['nb_emplacements']} emplacements")
    return ", ".join(parts) if parts else non_renseigne()


def fmt_audit(vpn):
    audit = vpn.get("audit_no_logs")
    if not audit:
        return non_renseigne()
    return audit


def sources_html(vpn):
    items = "".join(
        f'<li><a href="{s["url"]}" rel="nofollow noopener" target="_blank">{s["label"]}</a></li>'
        for s in vpn.get("sources", [])
    )
    return items or "<li>Aucune source complementaire citee.</li>"


def rendre_fiche(vpn):
    nom = vpn["nom"]
    audit = vpn.get("audit_no_logs") or ""
    non_audite = "aucun audit" in audit.lower()

    encart_audit = ""
    if non_audite:
        encart_audit = f'''
    <div class="encart alerte">
      <strong>Pas d'audit no-logs independant publie.</strong> {audit}. Les engagements de confidentialite de {nom} reposent, a ce jour, sur ses seules declarations.
    </div>'''

    note_supp = vpn.get("note_supplementaire", "")
    encart_note = f'<div class="encart">{note_supp}</div>' if note_supp else ""

    paiement = vpn.get("paiement_anonyme")
    paiement_html = paiement if paiement else non_renseigne()

    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{nom} — Avis, prix et audit no-logs 2026 | ComparatifVPN</title>
<meta name="description" content="{nom} : prix reel, juridiction ({vpn['juridiction']}), audit no-logs et methodes de paiement. Fiche sourcee, mise a jour le 7 aout 2026.">
<link rel="canonical" href="{SITE_URL}/avis/{vpn['id']}.html">
<link rel="stylesheet" href="/css/style.css?v={ASSET_VERSION}">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4671241466590955" crossorigin="anonymous"></script>
</head>
<body>

<header class="entete">
  <div class="conteneur entete-barre">
    <a href="/" class="logo"><img src="/img/logo.svg" alt="" width="26" height="26" class="logo-mark">comparatif<span class="point">.</span>vpn</a>
    <nav class="nav-principale">
      <a href="/comparatif.html">Comparatif</a>
      <a href="/guides/">Guides</a>
      <a href="/methodologie.html">Methodologie</a>
    </nav>
  </div>
</header>

<main class="conteneur-etroit">
  <p class="fil-ariane"><a href="/">Accueil</a> / <a href="/comparatif.html">Comparatif</a> / {nom}</p>

  <div class="fiche-entete">
    <div class="fiche-titre">
      <img src="{vpn['logo']}" alt="Logo {nom}" width="40" height="40" class="logo-vpn">
      <h1>{nom}</h1>
    </div>
    <div class="fiche-prix-badge">{fmt_prix(vpn)}</div>
  </div>
  <p><a href="{vpn['site_officiel']}" rel="nofollow noopener sponsored" target="_blank" class="lien-officiel">Site officiel de {nom} &#8599;</a></p>

  <div class="fiche-grille">
    <div class="fiche-stat">
      <div class="libelle">Juridiction</div>
      <div class="valeur">{vpn['juridiction']}</div>
    </div>
    <div class="fiche-stat">
      <div class="libelle">Prix sans engagement</div>
      <div class="valeur mono">{fmt_prix_sans_engagement(vpn)}</div>
    </div>
    <div class="fiche-stat">
      <div class="libelle">Serveurs / couverture</div>
      <div class="valeur">{fmt_serveurs(vpn)}</div>
    </div>
    <div class="fiche-stat">
      <div class="libelle">Paiement anonyme</div>
      <div class="valeur">{paiement_html}</div>
    </div>
  </div>

  <section>
    <h2>Notre avis sur {nom}</h2>
    <p>{vpn.get('notre_avis', "Avis editorial non redige pour ce fournisseur.")}</p>
  </section>

  <section>
    <h2>Juridiction</h2>
    <p>{vpn.get('juridiction_note', non_renseigne(False))}</p>
  </section>

  <section>
    <h2>Audit no-logs</h2>
    <p>{fmt_audit(vpn)}</p>
    {encart_audit}
  </section>

  {encart_note}

  <section>
    <h2>Sources</h2>
    <ul class="liste-sources">
      {sources_html(vpn)}
    </ul>
  </section>

</main>

<footer class="pied">
  <div class="conteneur">
    <p>ComparatifVPN — comparateur independant. Les prix et conditions changent frequemment : verifiez toujours sur le site officiel avant de payer.</p>
    <div class="pied-liens">
      <a href="/methodologie.html">Methodologie</a>
      <a href="/comparatif.html">Comparatif</a>
      <a href="/guides/">Guides</a>
      <a href="/confidentialite.html">Confidentialite</a>
    </div>
  </div>
</footer>

</body>
</html>
'''


def main():
    donnees = json.loads(DATA.read_text(encoding="utf-8"))
    SORTIE.mkdir(parents=True, exist_ok=True)
    for vpn in donnees["vpns"]:
        chemin = SORTIE / f"{vpn['id']}.html"
        chemin.write_text(rendre_fiche(vpn), encoding="utf-8")
        print(f"[ok] {chemin.relative_to(RACINE)}")
    print(f"{len(donnees['vpns'])} fiches generees.")


if __name__ == "__main__":
    main()
