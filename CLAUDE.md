# ComparatifVPN

Site statique (vanilla HTML/CSS/JS, aucun framework, aucun build step JS) comparant des
fournisseurs VPN grand public — prix, juridiction, audits no-logs independants, methodes de
paiement. Fait partie de la famille de sites `dlastes` (PrixDuMètre, ValeurÉcole, PleinMalin,
RisqueCommune web, InfraRoute web, ConvCollectives web), meme stack et meme discipline
"jamais de donnee inventee", mais **premier site de la famille pense des le depart pour
l'affiliation** (pas encore active — voir "Affiliation" ci-dessous).

## Pourquoi ce projet existe

Decision prise avec le mainteneur (2026-08-07) : lancer un nouveau site orientable vers
l'affiliation VPN, un marche a forte valeur par clic mais tres concurrentiel en SEO. Pas de
compte d'affiliation cree pour l'instant ("pas la peine d'avoir ces comptes tant qu'on a pas
de trafic") — les liens vers chaque fournisseur pointent vers leur site officiel, sans code de
suivi, en attendant un volume de trafic qui justifie une inscription aupres des reseaux
d'affiliation (Impact, PartnerStack, ou directement aupres de chaque fournisseur selon leurs
propres programmes).

## Stack

- Frontend : HTML/CSS/JS vanilla, aucun framework, aucune dependance npm.
- Donnees : `site/data/vpns.json`, un objet unique agregeant 10 fournisseurs — pas de base
  SQLite ni de sql.js (volume trop faible pour le justifier, a la difference des autres sites
  de la famille qui gerent des dizaines de milliers de lignes).
- Generation de contenu statique : `build/generer_avis.py` (une fiche HTML par fournisseur,
  a partir de `vpns.json`) et `build/generer_sitemap.py` (sitemap.xml). Aucun autre build
  step — `index.html`, `comparatif.html`, `methodologie.html`, `confidentialite.html` et les
  3 guides sont ecrits a la main, pas generes.
- Deploiement : Cloudflare Pages, dossier de build = `site/`, deploiement automatique via
  GitHub Actions (`.github/workflows/deploy.yml`, `on: push: branches: [main]`) — meme
  pattern que PleinMalin (site pur des le depart, pas de branche `web-redesign` puisqu'il n'y
  a pas d'ancien export Expo a menager).

## Regenerer le site apres une modification de `site/data/vpns.json`

```
python build/generer_avis.py       # data/vpns.json -> site/avis/<id>.html (10 fiches)
python build/generer_sitemap.py    # -> site/sitemap.xml
```

`build/config.py` centralise `SITE_URL` (`https://comparatif-vpn.pages.dev` — domaine `.fr`/
`.com` non achete a ce jour, meme situation que les autres sites de la famille) et
`ASSET_VERSION` (cache-busting `?v=N` sur `style.css`/`app.js`, a incrementer a chaque
modification de l'un des deux — meme mecanisme et meme raison que celui documente dans le
CLAUDE.md de ValeurEcole, apres qu'un bug de cache navigateur y ait ete trouve et corrige).

## Discipline "jamais de donnee inventee"

Meme regle absolue que le reste de la famille de projets, avec un enjeu de credibilite plus
direct ici (un comparatif VPN qui invente un chiffre de confidentialite serait le contraire du
service qu'il pretend rendre) :

- Chaque fiche fournisseur (`site/data/vpns.json`) cite ses sources individuellement
  (`sources: [{label, url}]`), affichees en bas de chaque page `/avis/<id>.html`.
- Un champ absent (nombre de serveurs, prix sans engagement, methode de paiement anonyme...)
  est stocke `null` et rendu `"non communique"` cote HTML — jamais une estimation, jamais une
  moyenne du secteur.
- **Aucun test de vitesse, de fuite DNS/WebRTC ou de contournement de geoblocage n'est
  realise par ce site** (pas de materiel de test dedie) — `site/methodologie.html` le dit
  explicitement, pour ne pas laisser croire a une mesure independante inexistante.
- Les "3 selections" de la page d'accueil (`index.html`) sont des choix editoriaux justifies
  chacun par un fait source verifiable et cite, **pas un score calcule automatiquement** —
  volontaire, pour eviter une fausse impression de precision qu'une formule ponderee
  (audits × prix × serveurs...) donnerait sans justification solide.

## Donnees au 2026-08-07 — 10 fournisseurs, recherche sourcee

NordVPN, ExpressVPN, Surfshark, Proton VPN, Mullvad, CyberGhost, Private Internet Access
(PIA), IVPN, Windscribe, PrivadoVPN. Chaque fiche a ete recherchee individuellement
(WebSearch) contre des sources tierces (Security.org, Tom's Guide, TechRadar, vpnMentor,
VPN.com, Gizmodo, European Purpose, FindCheapVPNs) et les communiques d'audit des cabinets
eux-memes. Points notables verifies pendant cette recherche, a ne pas re-deviner :

- **Juridiction hors 5/9/14 Eyes** : ExpressVPN (Iles Vierges britanniques), NordVPN (Panama),
  CyberGhost (Roumanie), Proton VPN (Suisse), IVPN (Gibraltar/Suisse), PrivadoVPN (Islande,
  a quitte la Suisse en 2025 suite aux reformes de surveillance suisses).
- **Dans le perimetre Nine/Fourteen Eyes** : Surfshark (Pays-Bas), Mullvad (Suede).
- **Dans le perimetre Five Eyes** : PIA (Etats-Unis), Windscribe (Canada).
- **Paiement anonyme documente** : seuls Mullvad (especes par courrier, Monero, pas d'email
  requis) et IVPN (especes, cryptomonnaies, inscription sans email) — les 8 autres n'ont
  aucune methode anonyme trouvee sur une source fiable, affiche comme tel, pas suppose absent.
- **Aucun audit no-logs independant publie** : Windscribe (seulement des audits d'application
  par Leviathan Security en 2021/2022, pas du no-logs) et PrivadoVPN (aucun audit en six ans
  d'activite) — les deux fiches l'affichent explicitement avec un encart d'alerte
  (`.encart.alerte` dans `style.css`), genere automatiquement par `generer_avis.py` des que
  la chaine `"aucun audit"` (insensible a la casse) apparait dans `audit_no_logs`.

## Identite visuelle

Theme sombre "console de securite" (`site/css/style.css`) : fond quasi-noir (`--fond:
#0a0e13`), accent emeraude/menthe `--accent: #24e6a8` (confiance/chiffrement), violet
`--violet: #9d8cf6` en accent secondaire (vie privee), police monospace systeme pour les
donnees techniques/chiffres (`--font-mono`), aucune police chargee depuis un CDN externe —
coherent avec le principe deja applique a sql.js/bzip2.js/Leaflet ailleurs dans la famille
(rien de charge depuis un CDN tiers), et delibere ironique-a-eviter pour un site qui parle de
vie privee. **Volontairement distinct de tous les autres sites de la famille** : aucun n'a de
theme sombre — PrixDuMetre (vert sapin/terre cuite), ValeurEcole (marine/or), PleinMalin
(asphalte/orange), RisqueCommune web (ardoise/ocre), ConvCollectives web (grenat/ardoise).
Meme raisonnement anti-"template duplique" pour une eventuelle regie publicitaire future que
documente dans le CLAUDE.md de PrixDuMetre.

## Verifie pour de vrai (2026-08-07)

- Serveur statique local (`python -m http.server`) : les 18 pages (accueil, comparatif,
  methodologie, confidentialite, 3 guides, 10 fiches fournisseur) + `data/vpns.json` +
  `css/style.css` + `js/app.js` + `robots.txt` + `sitemap.xml` toutes en 200.
- Script de verification de liens (Python, meme methode que les autres sites de la famille) :
  210 liens internes `href`/`src` verifies sur l'ensemble des pages generees, **0 lien casse**.
- Logique de tri du tableau comparatif (`site/js/app.js`) rejouee dans un harnais Node contre
  les vraies donnees de `vpns.json` (pas de navigateur disponible dans cet environnement,
  meme limite documentee sur les autres sites de la famille) : tri par prix croissant et par
  nombre de serveurs decroissant tous deux corrects, `Infinity`/`-1` geres proprement pour les
  valeurs manquantes (elles finissent toujours en fin de liste, jamais melangees au milieu par
  erreur de comparaison `undefined`).
- Les 10 fiches generees par `generer_avis.py` inspectees individuellement : encart d'alerte
  present et correct sur les 2 fiches sans audit (Windscribe, PrivadoVPN), absent sur les 8
  autres.

## Non verifie

- Rendu reel dans un navigateur (interaction avec le tri du tableau, responsive mobile) —
  extension Chrome non testee sur ce projet specifiquement a la date d'ecriture. A verifier
  avant de considerer le site pret pour du trafic reel.
- Aucun compte Cloudflare Pages ni depot GitHub crees pour ce projet a la date d'ecriture —
  voir "Deploiement" ci-dessous pour ce qui reste a faire par le mainteneur.

## Publicite AdSense (2026-08-07)

`site/ads.txt` ajoute avec le meme identifiant editeur que le reste de la famille de sites
(`pub-4671241466590955`, deja verifie actif sur PrixDuMetre/ValeurEcole/PleinMalin/InfraRoute
web) — reutilise tel quel, jamais un nouvel identifiant invente.

**Site ajoute au compte AdSense existant** (pas un nouveau compte — connexion via le compte
Google du mainteneur deja associe, `penatit.contact@gmail.com`) : `comparatif-vpn.pages.dev`
apparait desormais dans la liste des sites du compte `pub-4671241466590955`, statut "Examen
requis". La balise fournie par AdSense pour cette verification
(`<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4671241466590955" crossorigin="anonymous"></script>`)
a ete inseree juste avant `</head>` sur les 18 pages du site (verifie par grep + servi
localement), et ajoutee au gabarit de `build/generer_avis.py` pour que les 10 fiches
regenerees la conservent automatiquement.

**Ce qui reste bloque pour le mainteneur, pas pour Cowork** : le compte AdSense affiche un
bandeau "Action requise : vous devez verifier votre compte de paiement AdSense" — verification
d'identite/paiement qui touche des donnees bancaires/personnelles, hors de portee de cet
environnement (entree de coordonnees bancaires explicitement interdite). Sans cette
verification de compte ET sans que Google approuve le site apres examen (delai variable,
generalement plusieurs jours), aucune annonce ne s'affichera reellement meme si la balise est
deja en place.

## Deploiement — ce qui reste a faire par le mainteneur

Cet environnement n'a ni identifiants GitHub (pas de `git push` possible), ni acces API
Cloudflare pour la gestion de Pages (seul un connecteur MCP limite est disponible, qui ne
couvre pas la creation de projets Pages) — meme limite que documentee sur les autres sites de
la famille cree/redesigne cette meme periode. Le depot local est initialise et commite
(`git init` + premier commit, 29 fichiers, verifie via `git show --stat`), mais :

1. **Creer le depot GitHub** `dlastes/comparatif-vpn` (prive, comme les autres) et `git push`
   depuis une machine ou les identifiants du mainteneur sont deja configures.
2. **Creer le projet Cloudflare Pages** (dashboard, dossier de sortie = `site`, aucune commande
   de build — tout est pre-genere et commite).
3. **Ajouter le secret `CLOUDFLARE_API_TOKEN`** dans les parametres GitHub Actions du depot,
   pour que `.github/workflows/deploy.yml` (deja pret, meme pattern que PleinMalin) puisse
   deployer automatiquement a chaque push.
4. Une fois en ligne : ajouter le site a Google Search Console (verification HTML-file, meme
   procedure que les autres sites) et soumettre `sitemap.xml`.

**Detail technique laisse en l'etat** : la branche locale s'appelle `master`, pas `main`
(une tentative de renommage via `git branch -m` a echoue — le montage Windows de cet
environnement a laisse des fichiers `.lock` orphelins dans `.git/` apres le premier commit,
non supprimables meme en `rm -f` malgre des permissions `rwx` normales, memes symptomes que
le warning `unable to unlink` deja documente sur `mon-autre-app` cette meme session, mais ici
bloquant plutot que non-fatal). `.github/workflows/deploy.yml` a ete elargi pour accepter un
push sur `main` OU `master` (`on: push: branches: [main, master]`) afin que le deploiement
fonctionne quel que soit le nom de branche final — cette modification, elle, n'a pas pu etre
commitee pour la meme raison (verifiable via `git diff` : un seul fichier modifie, non commite).
Le mainteneur peut soit pousser tel quel (`master`, le workflow le couvre), soit renommer la
branche en `main` depuis son propre git (aucun probleme de verrou attendu hors de ce montage)
avant de pousser, puis recommiter le fichier `deploy.yml` elargi si souhaite.

## Reste a faire

- [ ] Test reel en navigateur (extension Chrome).
- [ ] Depot GitHub + push (mainteneur).
- [ ] Projet Cloudflare Pages + secret `CLOUDFLARE_API_TOKEN` (mainteneur).
- [ ] Search Console + sitemap une fois en ligne.
- [ ] Cloudflare Web Analytics une fois le projet Pages cree.
- [ ] Decision d'achat de domaine (`.fr`/`.com`) ou maintien en `*.pages.dev`.
- [ ] Inscription aupres de reseaux d'affiliation une fois un trafic reel etabli (voir
  "Pourquoi ce projet existe").
