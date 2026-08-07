// ComparatifVPN — comparatif.html : charge site/data/vpns.json et affiche un
// tableau triable. Dataset volontairement petit (10 fournisseurs) : pas besoin
// de sql.js comme sur les autres sites de la famille, un simple fetch + rendu
// JS suffit et reste plus simple a maintenir pour ce volume de donnees.

let VPNS = [];
let triColonne = null;
let triSensInverse = false;

function euroDepuisPrix(vpn) {
  // Convertit au mieux vers un ordre de grandeur EUR pour permettre un tri
  // coherent entre devises (affichage : on garde toujours la devise source
  // reelle, cette conversion ne sert qu'au tri, jamais affichee comme un prix).
  const prix = vpn.prix_mensuel_engagement_usd ?? vpn.prix_mensuel_engagement_eur;
  if (prix == null) return Infinity;
  if (vpn.devise_source === "USD") return prix * 0.92; // ordre de grandeur, pas un taux de change engage
  return prix;
}

function formaterPrix(vpn) {
  const val = vpn.prix_mensuel_engagement_usd ?? vpn.prix_mensuel_engagement_eur;
  if (val == null) return '<span class="non-renseigne">non communique</span>';
  const symbole = vpn.devise_source === "USD" ? "$" : "€";
  return `${val.toFixed(2)} ${symbole}/mois`;
}

function formaterAudit(vpn) {
  if (!vpn.audit_no_logs) return '<span class="non-renseigne">non renseigne</span>';
  const nonAudite = /aucun audit/i.test(vpn.audit_no_logs);
  const classe = nonAudite ? "badge-non-audite" : "badge-audite";
  const libelle = nonAudite ? "Non audite" : "Audite";
  return `<span class="badge ${classe}">${libelle}</span> <span class="audit-detail">${vpn.audit_no_logs}</span>`;
}

function formaterServeurs(vpn) {
  const parts = [];
  if (vpn.nb_serveurs) parts.push(`${vpn.nb_serveurs.toLocaleString("fr-FR")} serveurs`);
  if (vpn.nb_pays) parts.push(`${vpn.nb_pays} pays`);
  else if (vpn.nb_emplacements) parts.push(`${vpn.nb_emplacements} emplacements`);
  if (parts.length === 0) return '<span class="non-renseigne">non communique</span>';
  return parts.join(", ");
}

function rendreTableau() {
  const corps = document.getElementById("corps-comparatif");
  if (!corps) return;
  let lignes = [...VPNS];

  if (triColonne) {
    lignes.sort((a, b) => {
      let va, vb;
      if (triColonne === "prix") { va = euroDepuisPrix(a); vb = euroDepuisPrix(b); }
      else if (triColonne === "nom") { va = a.nom; vb = b.nom; }
      else if (triColonne === "juridiction") { va = a.juridiction; vb = b.juridiction; }
      else if (triColonne === "serveurs") { va = a.nb_serveurs ?? -1; vb = b.nb_serveurs ?? -1; }
      if (typeof va === "string") return triSensInverse ? vb.localeCompare(va) : va.localeCompare(vb);
      return triSensInverse ? vb - va : va - vb;
    });
  }

  corps.innerHTML = lignes.map(v => `
    <tr>
      <td class="nom-vpn">
        <a href="/avis/${v.id}.html" class="lien-fournisseur">
          <img src="${v.logo}" alt="" width="28" height="28" class="logo-vpn" loading="lazy">
          ${v.nom}
        </a>
      </td>
      <td class="prix">${formaterPrix(v)}</td>
      <td>${v.juridiction}</td>
      <td>${formaterAudit(v)}</td>
      <td>${formaterServeurs(v)}</td>
      <td>${v.paiement_anonyme ? v.paiement_anonyme : '<span class="non-renseigne">non communique</span>'}</td>
      <td><a href="${v.site_officiel}" rel="nofollow noopener sponsored" target="_blank" class="lien-officiel">Site officiel ↗</a></td>
    </tr>
  `).join("");
}

function initTri() {
  document.querySelectorAll("th[data-tri]").forEach(th => {
    th.addEventListener("click", () => {
      const colonne = th.getAttribute("data-tri");
      if (triColonne === colonne) triSensInverse = !triSensInverse;
      else { triColonne = colonne; triSensInverse = false; }
      rendreTableau();
    });
  });
}

async function initComparatif() {
  const corps = document.getElementById("corps-comparatif");
  if (!corps) return;
  try {
    const reponse = await fetch("/data/vpns.json");
    const donnees = await reponse.json();
    VPNS = donnees.vpns;
    initTri();
    rendreTableau();
  } catch (e) {
    corps.innerHTML = `<tr><td colspan="6">Erreur de chargement des donnees.</td></tr>`;
  }
}

document.addEventListener("DOMContentLoaded", initComparatif);
