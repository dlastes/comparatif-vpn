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

**Refonte du 2026-08-08 — perime, la section qui suit remplace celle-ci.** Le theme sombre
"console de securite" d'origine (fond quasi-noir `#0a0e13`, accent emeraude) a ete juge par le
mainteneur "vieux et sombre" apres comparaison avec des sites concurrents du secteur, avec deux
demandes explicites : un vrai logo (il n'y en avait pas, seulement le wordmark texte
"comparatif.vpn") et un rendu plus impactant. Le principe "anti-template-duplique" (rester
visuellement distinct des autres sites de la famille dlastes) reste vrai avec la nouvelle
palette indigo/violet — aucun autre site de la famille ne l'utilise.

**Theme actuel** (`site/css/style.css`) : fond clair (`--fond: #f6f7fb`), cartes blanches avec
ombre douce, accent indigo `--accent: #4f46e5` + violet en degrade secondaire, emeraude pour
les badges "Audite"/rouge-corail pour "Non audite" (le code couleur confiance/alerte est
inchange, seul le fond a change de sombre a clair). Police systeme uniquement, toujours aucune
police ni CDN externe. **Logo ajoute** : `site/img/logo.svg` (bouclier + coche, degrade
indigo/violet, genere directement en SVG — pas d'appel a un outil de rendu externe), insere en
`<img>` dans le header de chacune des 19 pages HTML du site (markup identique partout, remplace
en une seule passe). `?v=3` → `?v=4` sur les liens `style.css`/`app.js` de toutes les pages pour
casser le cache.

**Important : la discipline "jamais de donnee inventee" (voir plus bas) est restee intacte.**
L'"impact" visuel vient de la mise en forme (badges colores, rangs numerotes en pastille dans
"Nos selections", CTA "Site officiel" en bouton plein, premiere ligne du tableau surlignee) —
aucune note /10 ni "meilleur choix" fabriquee n'a ete ajoutee, contrairement au pattern courant
chez les comparateurs VPN concurrents (dont un site de reference cite par le mainteneur pour
l'inspiration visuelle, dont le contenu — notes, formulations marketing — n'a pas ete repris,
seuls des principes de mise en page generiques l'ont ete : cartes blanches, badges pilule,
hierarchie typographique forte).

Verifie visuellement le 2026-08-08 : accueil, une fiche VPN (`avis/nordvpn.html`),
`comparatif.html`, `guides/index.html`, largeur mobile (390px) et desktop (1400px) — Playwright
headless (extension Chrome indisponible dans cet environnement), 0 erreur console, logo present
sur les 19 pages (verifie par comptage), aucun residu de l'ancien theme sombre (`color-scheme:
dark` absent du CSS).

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

- Aucun compte Cloudflare Pages ni depot GitHub crees pour ce projet a la date d'ecriture —
  voir "Deploiement" ci-dessous pour ce qui reste a faire par le mainteneur.

## Refonte accueil : tableau immediat + logos (2026-08-07, suite de session)

Retour du mainteneur apres verification en navigateur : la page d'accueil cachait le
comparatif derriere du texte marketing ("blabla") et un clic vers `/comparatif.html` — pas ce
qu'on attend d'un site dont la seule raison d'etre est le tableau. Corrige :

- **Le tableau comparatif est maintenant rendu directement sur `index.html`**, juste apres un
  H1 + une phrase d'intro (avant : un hero avec paragraphe + 2 boutons CTA renvoyant vers une
  page separee). Toujours triable au clic sur une colonne (`site/js/app.js`, inchange dans sa
  logique de tri).
- **Rendu statique du tableau (SEO)** : les lignes du `<tbody>` sont desormais generees a la
  build (`build/generer_tableau.py`, nouveau script) et injectees dans `index.html` ET
  `comparatif.html` entre des marqueurs `<!-- TABLEAU:DEBUT/FIN -->`, plutot que rendues
  uniquement par un `fetch()` cote client comme avant. Un crawler qui n'execute pas le JS (ou
  avec delai) voyait "Chargement..." a la place du contenu qui justifie la page — corrige.
  `app.js` reste necessaire pour le tri interactif : il regenere le meme balisage au clic sur
  une colonne (les deux chemins de rendu — Python a la build, JS au clic — doivent rester en
  phase, voir le format identique des deux `<td>` "Fournisseur").
- **Logos ajoutes** : `site/img/logos/<id>.png` (80x80, convertis via Pillow depuis le favicon
  officiel de chaque fournisseur — `favicon.ico` standard pour 8 d'entre eux, chemin
  specifique trouve dans le `<head>` de leur site pour Surfshark et IVPN qui n'exposent pas de
  `/favicon.ico` classique). Utilises dans le tableau, les nouvelles fiches courtes de
  l'accueil et l'entete des pages `/avis/<id>.html`. Domaines verifies un par un (requete
  reelle, code 200) avant de servir de source aux logos et aux nouveaux liens "Site officiel".
- **Nouveau champ `site_officiel`** dans `site/data/vpns.json` pour chacun des 10
  fournisseurs, et lien "Site officiel ↗" (`rel="nofollow noopener sponsored"`) ajoute dans
  chaque ligne du tableau et chaque fiche — annonce dans le CLAUDE.md d'origine
  ("les liens vers chaque fournisseur pointent vers leur site officiel") mais jamais
  effectivement implemente jusqu'ici. `rel="sponsored"` pose par anticipation d'une
  eventuelle inscription a un programme d'affiliation future (voir "Pourquoi ce projet
  existe") — recommandation Google pour ce type de lien, sans attendre d'avoir un vrai code
  de tracking a poser dessus.
- **Nouvelle section "Chaque fournisseur en detail"** sur l'accueil (`site/index.html`,
  generee par le meme script) : une carte par fournisseur avec logo, badge audite/non audite,
  et une description tiree de `juridiction_note` (deja sourcee, jamais de nouveau texte
  invente pour l'occasion) — repond au "description de chaque avec logo" demande, sans
  ajouter de champ non sourced au JSON.
- Sections "Trois selections" et "Guides" repoussees apres le tableau et les fiches courtes
  (avant : entre le hero et le comparatif) — elles restent sur la page, juste plus bas.
- `ASSET_VERSION` (build/config.py) passe de 1 a 2, `?v=1` -> `?v=2` sur toutes les pages
  ecrites a la main (methodologie/confidentialite/guides) : cache-busting CSS/JS, meme
  convention documentee dans le CLAUDE.md de ValeurEcole.

**Verifie** : les 3 pages generatrices (`generer_avis.py`, `generer_tableau.py`,
`generer_sitemap.py`) relancees avec succes ; 280 liens internes verifies (0 casse, meme
methode que les autres sites de la famille) ; capture d'ecran Playwright (accueil desktop et
mobile 390px, page de tri sur `/comparatif.html` — le tri fonctionne toujours apres clic,
teste avec la colonne prix) ; rendu de `/avis/mullvad.html` avec logo + lien officiel.
**Toujours non verifie** : rendu reel sur un vrai navigateur/appareil mobile (Playwright
headless seulement, extension Chrome indisponible dans cet environnement).

## Section "Notre avis" par fiche (2026-08-07, meme session — demande SEO explicite)

Chaque page `/avis/<id>.html` a maintenant un paragraphe editorial substantiel ("Notre avis
sur <nom>", nouveau champ `notre_avis` dans `vpns.json`, rendu par `generer_avis.py` juste
apres les statistiques cle, avant la section Juridiction) — objectif explicite du mainteneur :
du contenu long et unique par page pour le referencement, la ou le tableau seul ne fournit que
des donnees tabulaires. **Discipline "jamais de donnee inventee" respectee** : chaque avis ne
fait que synthetiser des faits DEJA presents et sources ailleurs dans la meme fiche
(audit_no_logs, juridiction, note_supplementaire, paiement_anonyme, prix) — aucun nouveau fait
numerique n'a ete introduit, seulement une mise en perspective editoriale (ex : Proton VPN est
le seul a ne pas etre RAM-only, PIA est aux Etats-Unis mais a un vrai precedent FBI 2016,
Windscribe et PrivadoVPN sont les deux seuls sans audit no-logs independant). Verifie : rendu
via `generer_avis.py`, un extrait affiche visuellement correct sur `/avis/pia.html`
(capture Playwright), 280 liens internes toujours intacts apres regeneration.

## Accueil enrichi : selections etendues, FAQ, 4e guide (2026-08-07, meme session)

Retour du mainteneur : le site restait "assez vide" compare aux vrais comparateurs VPN
(top10vpn.com, security.org, tomsguide.com...) — recherche rapide confirmant leur pattern
commun : selections par cas d'usage, FAQ, guides pedagogiques en plus du tableau brut. Ajoute
en respectant la meme discipline de sourcing (rien de nouveau invente, tout derive de
`vpns.json` deja sourced) :

- **2 selections editoriales de plus** (`site/index.html`) : "Le plus grand reseau"
  (CyberGhost, 11 500 serveurs/100 pays — deja dans `vpns.json`) et un "Point de vigilance"
  qui flague explicitement Windscribe et PrivadoVPN comme les deux seuls fournisseurs sans
  audit no-logs independant — un signal negatif assume plutot que masque, coherent avec la
  regle "jamais de donnee inventee, jamais de manque cache non plus".
- **Section FAQ sur l'accueil** (4 questions : legalite du VPN en France, ce qu'un audit
  no-logs prouve reellement, poids de la juridiction, comment choisir) — contenu general de
  litteratie VPN, chaque reponse renvoie vers le guide correspondant pour approfondir plutot
  que de dupliquer le contenu.
- **4e guide** : `site/guides/vpn-gratuit.html` ("VPN gratuit : bonne ou mauvaise idee ?"),
  contraste Proton VPN (audit annuel, modele freemium adosse a un ecosysteme payant) vs
  PrivadoVPN (seul fournisseur sans aucun audit en six ans) — les deux seuls a offrir un tier
  gratuit dans ce comparatif. Ajoute a `web/build/generer_sitemap.py` (liste figee, a completer
  manuellement a chaque nouveau guide — pas de decouverte automatique du dossier `guides/`).
- `.faq-item` ajoute a `style.css` (variante sombre du meme pattern que MesAides).
- `ASSET_VERSION` 2 -> 3 (`?v=2` -> `?v=3` sur toutes les pages, y compris regenerees).

Verifie : 301 liens internes (0 casse), capture Playwright des nouvelles sections (selections
etendues + FAQ), 0 erreur console.

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

## Déploiement

**Périmé, la section ci-dessous la remplace** : le dépôt GitHub `dlastes/comparatif-vpn`
existe, le déploiement fonctionne. La branche locale est bien restée `master` (jamais
renommée), couverte par le `on: push: branches: [main, master]` du workflow.

Vérifié pour de vrai le 2026-08-08 (`git log`, contenu réel du workflow, `wrangler pages
project list` / `wrangler pages deployment list` — jamais supposé depuis cette doc).

- **Mécanisme** : `.github/workflows/deploy.yml` (nommé différemment des autres sites de la
  famille, qui utilisent `deploy-cloudflare-pages.yml`) + `cloudflare/wrangler-action@v3`.
  Déclenché sur push vers `main` **ou** `master`. **Node 20 pinné explicitement**
  (`actions/setup-node@v4`, `node-version: 20`, ajouté le 2026-08-08 par le mainteneur
  directement via l'éditeur web GitHub — absent à la création du fichier, cause d'un échec
  quasi certain sur le premier push une fois le runner par défaut passé à Node 24, qui casse la
  résolution du binaire natif `@cloudflare/workerd-linux-64` dont dépend `wrangler-action@v3` —
  **ne jamais retirer cette étape**, même bug que sur les 7 autres sites de la famille ce
  même jour).
- **Build** : aucun — `site/` est un site statique pré-généré, committé tel quel. Commande :
  `wrangler pages deploy site --project-name=comparatif-vpn`.
- **Projet Cloudflare Pages** : `comparatif-vpn` (confirmé via `wrangler pages project list`),
  domaine `comparatif-vpn.pages.dev`.
- **Branche de production réelle côté Cloudflare** : `master` (confirmé via `wrangler pages
  deployment list --project-name=comparatif-vpn` — `Environment: Production`).
- **Intégration git native Cloudflare** : toujours active en parallèle du workflow (2
  déploiements Production distincts observés à quelques minutes d'écart pour le même commit,
  après l'ajout du fix Node 20). Pas cassé, juste redondant — un double build à chaque push.
- **Secret `CLOUDFLARE_API_TOKEN`** : repo GitHub `dlastes/comparatif-vpn` → Settings → Secrets
  and variables → Actions. Existence confirmée indirectement : le workflow a produit un
  déploiement Production réussi après l'ajout du fix Node 20 (contenu vérifié en ligne).

## Reste a faire

- [ ] Test reel en navigateur (extension Chrome).
- [ ] Depot GitHub + push (mainteneur).
- [ ] Projet Cloudflare Pages + secret `CLOUDFLARE_API_TOKEN` (mainteneur).
- [ ] Search Console + sitemap une fois en ligne.
- [ ] Cloudflare Web Analytics une fois le projet Pages cree.
- [ ] Decision d'achat de domaine (`.fr`/`.com`) ou maintien en `*.pages.dev`.
- [ ] Inscription aupres de reseaux d'affiliation une fois un trafic reel etabli (voir
  "Pourquoi ce projet existe").
