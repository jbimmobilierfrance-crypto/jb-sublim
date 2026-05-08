#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply all 8 changes to index.html — JB Sublim 08/05/2026"""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ══════════════════════════════════════════════════════════
# 1. SECTION REORDER — tarifs juste après before-after
# ══════════════════════════════════════════════════════════
tarifs_pat = r'\n\n<section class="tarifs-launch"[^>]*>.*?</section>'
m = re.search(tarifs_pat, html, re.DOTALL)
if not m:
    sys.exit('ERROR: tarifs section not found')
tarifs_block = m.group(0)
html = html.replace(tarifs_block, '', 1)

# Insérer après la section before-after (avant problem)
html = re.sub(
    r'(</section>)(\s*\n\s*<section class="problem")',
    r'\1' + tarifs_block + r'\2',
    html, count=1
)
print('✓ Section tarifs déplacée après avant/après')

# ══════════════════════════════════════════════════════════
# 2. TÉMOIGNAGES — entre leviers et process
# ══════════════════════════════════════════════════════════
temo_section = '''

<section class="temoignages" id="temoignages">
  <div class="container">
    <div class="section-label">ILS NOUS ONT FAIT CONFIANCE</div>
    <h2 class="section-title">
      Des propriétaires.<br>
      <em>Des résultats réels.</em>
    </h2>

    <div class="temo-grid">

      <div class="temo-card fade-in">
        <div class="temo-header">
          <div class="temo-avatar">
            <img src="[PHOTO_1]" alt="[Prénom 1]" class="temo-photo">
          </div>
          <div class="temo-meta">
            <div class="temo-name">[Prénom 1]</div>
            <div class="temo-location">[Ville] · [Type de bien]</div>
          </div>
        </div>
        <div class="temo-stars">★★★★★</div>
        <blockquote class="temo-quote">"[Témoignage à remplir — résultat, émotion, transformation]"</blockquote>
        <div class="temo-result">+[X]% de revenus en [Y] jours</div>
      </div>

      <div class="temo-card fade-in">
        <div class="temo-header">
          <div class="temo-avatar">
            <img src="[PHOTO_2]" alt="[Prénom 2]" class="temo-photo">
          </div>
          <div class="temo-meta">
            <div class="temo-name">[Prénom 2]</div>
            <div class="temo-location">[Ville] · [Type de bien]</div>
          </div>
        </div>
        <div class="temo-stars">★★★★★</div>
        <blockquote class="temo-quote">"[Témoignage à remplir — résultat, émotion, transformation]"</blockquote>
        <div class="temo-result">+[X]% de revenus en [Y] jours</div>
      </div>

      <div class="temo-card fade-in">
        <div class="temo-header">
          <div class="temo-avatar">
            <img src="[PHOTO_3]" alt="[Prénom 3]" class="temo-photo">
          </div>
          <div class="temo-meta">
            <div class="temo-name">[Prénom 3]</div>
            <div class="temo-location">[Ville] · [Type de bien]</div>
          </div>
        </div>
        <div class="temo-stars">★★★★★</div>
        <blockquote class="temo-quote">"[Témoignage à remplir — résultat, émotion, transformation]"</blockquote>
        <div class="temo-result">+[X]% de revenus en [Y] jours</div>
      </div>

    </div>
  </div>
</section>'''

html = re.sub(
    r'(</section>)(\s*\n\s*<section class="process")',
    r'\1' + temo_section + r'\2',
    html, count=1
)
print('✓ Section témoignages ajoutée entre leviers et process')

# ══════════════════════════════════════════════════════════
# 3. HERO — vidéo ronde + CTA Calendly + WhatsApp secondaire
# ══════════════════════════════════════════════════════════

# Vidéo sous le titre
old_sub = '    <p class="hero-sub">'
new_sub = '''    <div class="hero-video-wrap">
      <video class="hero-video" autoplay loop muted playsinline>
        <source src="/videos/intro-jamil.mp4" type="video/mp4">
      </video>
    </div>
    <p class="hero-sub">'''
html = html.replace(old_sub, new_sub, 1)

# CTA hero : Calendly + WhatsApp secondaire
old_hero_actions = '    <div class="hero-actions">\n      <a href="https://wa.me/33658797037?text=Bonjour%20Jamil%2C%20j%27aimerais%20un%20diagnostic%20gratuit%20de%20mon%20annonce%20Airbnb." class="btn-primary" target="_blank"><span>Diagnostic gratuit →</span></a>\n      <a href="#calculateur" class="btn-secondary">Calculer mon potentiel</a>\n    </div>'
new_hero_actions = '''    <div class="hero-actions">
      <a href="[LIEN_CALENDLY_À_INSÉRER]" class="btn-primary btn-calendly" target="_blank"><span>Réserver mon appel stratégique →</span></a>
      <a href="#calculateur" class="btn-secondary">Calculer mon potentiel</a>
    </div>
    <div class="hero-wa-secondary">
      <a href="https://wa.me/33658797037?text=Bonjour%20Jamil%2C%20j%27ai%20une%20question%20urgente." target="_blank" class="wa-secondary-link">
        <svg viewBox="0 0 24 24" fill="currentColor" width="13" height="13"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>
        Question urgente — WhatsApp
      </a>
    </div>'''
if old_hero_actions in html:
    html = html.replace(old_hero_actions, new_hero_actions, 1)
    print('✓ Hero CTAs mis à jour')
else:
    print('⚠ Hero actions block not matched exactly — skipping')

# ══════════════════════════════════════════════════════════
# 4. BA-CTA — Calendly
# ══════════════════════════════════════════════════════════
html = re.sub(
    r'(<div class="ba-cta">)\s*<a\s+href="https://wa\.me/[^"]*"\s+class="btn-primary"\s+target="_blank"\s*>\s*Diagnostic gratuit →\s*</a>',
    r'\1\n      <a href="[LIEN_CALENDLY_À_INSÉRER]" class="btn-primary btn-calendly" target="_blank">Réserver mon appel stratégique →</a>',
    html, count=1
)
print('✓ BA-CTA mis à jour')

# ══════════════════════════════════════════════════════════
# 5. CTA FINAL — Calendly + WhatsApp secondaire
# ══════════════════════════════════════════════════════════
html = re.sub(
    r'<a href="https://wa\.me/33658797037\?text=Bonjour%20Jamil%2C%20j%27aimerais%20un%20diagnostic%20gratuit%20de%20mon%20annonce%20Airbnb\." class="btn-whatsapp" target="_blank">.*?</a>',
    '<a href="[LIEN_CALENDLY_À_INSÉRER]" class="btn-primary btn-calendly" target="_blank"><span>Réserver mon appel stratégique →</span></a>',
    html, count=1, flags=re.DOTALL
)
# Remplacer le btn-secondary email par WhatsApp secondaire
html = html.replace(
    '<a href="mailto:jbimmobilier.france@gmail.com" class="btn-secondary">jbimmobilier.france@gmail.com</a>',
    '<a href="https://wa.me/33658797037?text=Bonjour%20Jamil%2C%20j%27ai%20une%20question%20urgente." class="btn-secondary" target="_blank">Question sur WhatsApp</a>',
    1
)
print('✓ CTA final mis à jour')

# ══════════════════════════════════════════════════════════
# 6. FORMULAIRE DE QUALIFICATION dans tarifs
# ══════════════════════════════════════════════════════════
qualify_html = '''
      <div class="qualify-form" id="qualifyForm">
        <div class="qualify-header">30 secondes · Personnalisez votre accompagnement</div>

        <div class="qualify-q">
          <div class="qualify-q-label">Combien de biens souhaitez-vous optimiser ?</div>
          <div class="qualify-options" data-q="biens">
            <button type="button" class="qualify-opt" data-val="1">1 bien</button>
            <button type="button" class="qualify-opt" data-val="2-3">2–3 biens</button>
            <button type="button" class="qualify-opt" data-val="4+">4+ biens</button>
          </div>
        </div>

        <div class="qualify-q">
          <div class="qualify-q-label">Votre annonce est-elle déjà en ligne ?</div>
          <div class="qualify-options" data-q="enligne">
            <button type="button" class="qualify-opt" data-val="oui">Oui, elle est active</button>
            <button type="button" class="qualify-opt" data-val="non">Non, je lance bientôt</button>
          </div>
        </div>

        <div class="qualify-q">
          <div class="qualify-q-label">Budget pour l'optimisation ?</div>
          <div class="qualify-options" data-q="budget">
            <button type="button" class="qualify-opt" data-val="low">Moins de 500€</button>
            <button type="button" class="qualify-opt" data-val="mid">500 – 1 500€</button>
            <button type="button" class="qualify-opt" data-val="high">Plus de 1 500€</button>
          </div>
        </div>

        <div class="qualify-q">
          <div class="qualify-q-label">Disponible pour un appel dans les 7 prochains jours ?</div>
          <div class="qualify-options" data-q="dispo">
            <button type="button" class="qualify-opt" data-val="oui">Oui</button>
            <button type="button" class="qualify-opt" data-val="non">Pas cette semaine</button>
          </div>
        </div>

        <a href="[LIEN_CALENDLY_À_INSÉRER]" class="pack-launch-cta qualify-cta" id="qualifyCta" target="_blank" aria-disabled="true">
          Réserver mon appel stratégique →
        </a>

        <div class="qualify-low-budget" id="qualifyLowBudget">
          <p>Le Pack Optimisation démarre à 490€. Laissez votre email — on vous contacte dès que l'offre correspond à votre budget.</p>
          <form action="https://formspree.io/f/VOTRE_ID_FORMSPREE" method="POST" class="qualify-email-form" target="_blank">
            <input type="email" name="email" placeholder="votre@email.com" required>
            <button type="submit">Me tenir informé →</button>
          </form>
        </div>
      </div>

'''

# Remplacer le bouton original pack-launch-cta par le formulaire + bouton intégré
html = re.sub(
    r'<a\s+href="https://wa\.me/[^"]*r%C3%A9server[^"]*"\s+class="pack-launch-cta"\s+target="_blank"\s*>\s*Réserver un créneau →\s*</a>',
    qualify_html.strip(),
    html, count=1
)
print('✓ Formulaire de qualification ajouté')

# ══════════════════════════════════════════════════════════
# 7. CALCULATEUR — email gate avant résultat
# ══════════════════════════════════════════════════════════
old_calc_btn = '''      <button class="calc-button" onclick="calculerPotentiel()">
        Calculer mon potentiel
      </button>

      <div class="calc-result" id="calc-result" style="display:none;">'''

new_calc_btn = '''      <button class="calc-button" onclick="calculerPotentiel()">
        Calculer mon potentiel
      </button>

      <div class="calc-email-gate" id="calcEmailGate" style="display:none;">
        <p class="calc-gate-text">Votre estimation est prête.</p>
        <p class="calc-gate-sub">Entrez votre email pour accéder à votre résultat :</p>
        <form class="calc-gate-form" id="calcGateForm">
          <input type="email" id="calcGateEmail" placeholder="votre@email.com" required autocomplete="email">
          <button type="submit">Voir mon potentiel →</button>
        </form>
        <p class="calc-gate-note">Résultat immédiat · Pas de spam</p>
      </div>

      <div class="calc-result" id="calc-result" style="display:none;">'''

html = html.replace(old_calc_btn, new_calc_btn, 1)
print('✓ Email gate calculateur ajouté')

# ══════════════════════════════════════════════════════════
# 8. BANNIÈRE — date dynamique
# ══════════════════════════════════════════════════════════
old_banner_text = '''    <span class="launch-banner-text">
      <span class="launch-banner-icon">✦</span>
      <strong>Juin & Juillet déjà en cours</strong> —
      3 créneaux disponibles avant la haute saison ·
      <em>Tarif actuel : 490€</em>
    </span>'''

new_banner_text = '''    <span class="launch-banner-text">
      <span class="launch-banner-icon">✦</span>
      Prochain créneau disponible :
      <strong id="bannerNextSlot">chargement…</strong>
      · <em>490€ au lieu de 790€</em>
    </span>'''

html = html.replace(old_banner_text, new_banner_text, 1)
print('✓ Bannière dynamique configurée')

# ══════════════════════════════════════════════════════════
# CSS — tous les nouveaux styles
# ══════════════════════════════════════════════════════════
new_css = '''
/* ── HERO VIDEO ── */
.hero-video-wrap {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  overflow: hidden;
  margin: 0 auto 32px;
  border: 2px solid var(--gold-tint-strong);
  box-shadow: 0 8px 32px rgba(184, 146, 74, 0.20);
  opacity: 0;
  animation: fadeUp 0.7s ease forwards 0.4s;
}
.hero-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* ── HERO WA SECONDAIRE ── */
.hero-wa-secondary {
  margin-top: 14px;
  text-align: center;
}
.wa-secondary-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  letter-spacing: 1px;
  color: var(--slate);
  text-decoration: none;
  border-bottom: 1px solid var(--line);
  padding-bottom: 1px;
  transition: color 0.2s ease, border-color 0.2s ease;
}
.wa-secondary-link:hover { color: var(--gold-deep); border-color: var(--gold); }

/* ── TÉMOIGNAGES ── */
.temoignages {
  padding: 100px 24px;
  background: var(--ivory-warm);
}
.temo-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-top: 56px;
}
.temo-card {
  background: #FFFFFF;
  border: 1px solid var(--line-strong);
  border-radius: 4px;
  padding: 32px 28px;
  display: flex;
  flex-direction: column;
  gap: 0;
}
.temo-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 16px;
}
.temo-avatar {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--cream);
  flex-shrink: 0;
  border: 2px solid var(--gold-tint-strong);
}
.temo-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.temo-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--anthracite);
  margin-bottom: 2px;
}
.temo-location {
  font-size: 11px;
  color: var(--muted);
  letter-spacing: 0.5px;
}
.temo-stars {
  color: var(--gold);
  font-size: 13px;
  letter-spacing: 2px;
  margin-bottom: 14px;
}
.temo-quote {
  font-family: 'Cormorant Garamond', serif;
  font-size: 17px;
  font-style: italic;
  color: var(--graphite);
  line-height: 1.65;
  margin-bottom: 20px;
  flex: 1;
}
.temo-result {
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--green);
  background: var(--green-soft);
  padding: 5px 12px;
  border-radius: 2px;
  align-self: flex-start;
}

/* ── FORMULAIRE DE QUALIFICATION ── */
.qualify-form {
  margin-bottom: 32px;
  padding: 32px;
  background: var(--ivory-warm);
  border: 1px solid var(--line-strong);
  border-radius: 4px;
  text-align: left;
}
.qualify-header {
  font-size: 11px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--gold-deep);
  font-weight: 700;
  margin-bottom: 24px;
  text-align: center;
}
.qualify-q {
  margin-bottom: 20px;
}
.qualify-q-label {
  font-size: 13px;
  color: var(--graphite);
  font-weight: 500;
  margin-bottom: 10px;
  line-height: 1.5;
}
.qualify-options {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.qualify-opt {
  padding: 9px 18px;
  border: 1px solid var(--line-strong);
  border-radius: 2px;
  background: #FFFFFF;
  font-family: 'Montserrat', sans-serif;
  font-size: 12px;
  font-weight: 400;
  color: var(--graphite);
  cursor: pointer;
  transition: all 0.18s ease;
  letter-spacing: 0.3px;
}
.qualify-opt:hover {
  border-color: var(--gold);
  color: var(--gold-deep);
}
.qualify-opt.selected {
  background: var(--anthracite);
  border-color: var(--anthracite);
  color: var(--ivory);
  font-weight: 500;
}
.qualify-cta {
  display: block;
  width: 100%;
  text-align: center;
  margin-top: 24px;
  transition: all 0.3s ease;
}
.qualify-cta[aria-disabled="true"] {
  opacity: 0.4;
  cursor: not-allowed;
  pointer-events: none;
}
.qualify-cta:not([aria-disabled]) {
  opacity: 1;
  pointer-events: auto;
}
.qualify-low-budget {
  display: none;
  margin-top: 24px;
  padding: 20px;
  background: var(--cream);
  border-radius: 3px;
  text-align: center;
}
.qualify-low-budget p {
  font-size: 13px;
  color: var(--graphite);
  line-height: 1.7;
  margin-bottom: 16px;
}
.qualify-email-form {
  display: flex;
  gap: 8px;
  max-width: 400px;
  margin: 0 auto;
}
.qualify-email-form input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid var(--line-strong);
  border-radius: 2px;
  font-family: 'Montserrat', sans-serif;
  font-size: 13px;
  background: #FFFFFF;
  color: var(--anthracite);
  outline: none;
}
.qualify-email-form input:focus { border-color: var(--gold); }
.qualify-email-form button {
  padding: 10px 20px;
  background: var(--anthracite);
  color: var(--ivory);
  border: none;
  border-radius: 2px;
  font-family: 'Montserrat', sans-serif;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
  letter-spacing: 0.5px;
  transition: background 0.2s ease;
}
.qualify-email-form button:hover { background: var(--gold-deep); }

/* ── CALCULATEUR EMAIL GATE ── */
.calc-email-gate {
  padding: 32px 24px;
  background: var(--ivory-warm);
  border: 1px solid var(--line-strong);
  border-radius: 4px;
  text-align: center;
  margin-top: 8px;
}
.calc-gate-text {
  font-family: 'Cormorant Garamond', serif;
  font-size: 22px;
  color: var(--anthracite);
  margin-bottom: 4px;
}
.calc-gate-sub {
  font-size: 13px;
  color: var(--graphite);
  margin-bottom: 20px;
}
.calc-gate-form {
  display: flex;
  gap: 8px;
  max-width: 380px;
  margin: 0 auto 12px;
}
.calc-gate-form input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid var(--line-strong);
  border-radius: 2px;
  font-family: 'Montserrat', sans-serif;
  font-size: 13px;
  background: #FFFFFF;
  color: var(--anthracite);
  outline: none;
  min-width: 0;
}
.calc-gate-form input:focus { border-color: var(--gold); }
.calc-gate-form button {
  padding: 12px 20px;
  background: var(--gold-deep);
  color: var(--ivory);
  border: none;
  border-radius: 2px;
  font-family: 'Montserrat', sans-serif;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  letter-spacing: 1px;
  transition: background 0.2s ease;
}
.calc-gate-form button:hover { background: var(--anthracite); }
.calc-gate-note {
  font-size: 11px;
  color: var(--muted);
  letter-spacing: 0.5px;
}

/* ── MOBILE ── */
@media (max-width: 768px) {
  .temo-grid { grid-template-columns: 1fr; gap: 16px; }
}
@media (max-width: 640px) {
  .hero-video-wrap { width: 160px; height: 160px; margin-bottom: 24px; }
  .qualify-form { padding: 20px 16px; }
  .qualify-opt { padding: 10px 14px; font-size: 13px; }
  .qualify-email-form { flex-direction: column; }
  .calc-gate-form { flex-direction: column; }
  .calc-gate-form button { width: 100%; }
}
'''

html = html.replace('</style>\n</head>', new_css + '</style>\n</head>', 1)
print('✓ CSS ajouté')

# ══════════════════════════════════════════════════════════
# JS — date dynamique + formulaire qualification + email gate
# ══════════════════════════════════════════════════════════
new_js = '''
// BANNIÈRE — prochain créneau dynamique
(function() {
  const el = document.getElementById('bannerNextSlot');
  if (!el) return;
  const jours = ['dimanche','lundi','mardi','mercredi','jeudi','vendredi','samedi'];
  const mois = ['janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre'];
  const now = new Date();
  const d = new Date(now);
  d.setDate(d.getDate() + 2); // au moins 2 jours d'avance
  // Trouver le prochain mardi (2) ou jeudi (4)
  while (d.getDay() !== 2 && d.getDay() !== 4) d.setDate(d.getDate() + 1);
  el.textContent = jours[d.getDay()] + ' ' + d.getDate() + ' ' + mois[d.getMonth()];
})();

// FORMULAIRE DE QUALIFICATION
(function() {
  const form = document.getElementById('qualifyForm');
  if (!form) return;
  const cta = document.getElementById('qualifyCta');
  const lowBudget = document.getElementById('qualifyLowBudget');
  const answers = {};
  const required = ['biens', 'enligne', 'budget', 'dispo'];

  form.querySelectorAll('.qualify-options').forEach(function(group) {
    const q = group.dataset.q;
    group.querySelectorAll('.qualify-opt').forEach(function(btn) {
      btn.addEventListener('click', function() {
        group.querySelectorAll('.qualify-opt').forEach(function(b) { b.classList.remove('selected'); });
        btn.classList.add('selected');
        answers[q] = btn.dataset.val;
        update();
      });
    });
  });

  function update() {
    const allDone = required.every(function(k) { return answers[k]; });
    if (answers.budget === 'low') {
      cta.style.display = 'none';
      lowBudget.style.display = 'block';
    } else {
      cta.style.display = 'block';
      lowBudget.style.display = 'none';
      if (allDone) {
        cta.removeAttribute('aria-disabled');
      } else {
        cta.setAttribute('aria-disabled', 'true');
      }
    }
  }
})();

// CALCULATEUR — email gate
(function() {
  var pending = false;
  var origCalculer = window.calculerPotentiel;

  window.calculerPotentiel = function() {
    var gate = document.getElementById('calcEmailGate');
    var result = document.getElementById('calc-result');
    var input = document.getElementById('revenu-actuel');
    var value = parseFloat(input.value);

    if (!value || value <= 0) {
      input.style.boxShadow = '0 0 0 2px #dc2626';
      setTimeout(function() { input.style.boxShadow = ''; }, 1500);
      return;
    }

    // Stocker la valeur pour après la gate
    pending = value;
    result.style.display = 'none';
    gate.style.display = 'block';
    gate.scrollIntoView({ behavior: 'smooth', block: 'center' });
  };

  document.getElementById('calcGateForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    var email = document.getElementById('calcGateEmail').value;
    if (!email || !pending) return;

    // Envoi Formspree (async, non bloquant)
    fetch('https://formspree.io/f/VOTRE_ID_FORMSPREE', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify({ email: email, revenu: pending, source: 'calculateur' })
    }).catch(function() {});

    // Masquer gate, afficher résultat
    document.getElementById('calcEmailGate').style.display = 'none';

    // Recalculer et afficher
    var gainSuffix = document.getElementById('calc-gain-suffix');
    var gainAlt = document.getElementById('calc-gain-alt');
    var result = document.getElementById('calc-result');
    var cta = document.querySelector('.calc-cta-whatsapp');

    if (pending < 300) {
      document.getElementById('calc-current').textContent = '— €';
      document.getElementById('calc-target').textContent = '— €';
      document.getElementById('calc-gain').textContent = '';
      if (gainSuffix) gainSuffix.style.display = 'none';
      if (gainAlt) gainAlt.style.display = 'inline';
    } else {
      var target = Math.round(pending * 1.7);
      var gainAnnuel = (target - pending) * 12;
      document.getElementById('calc-current').textContent = pending.toLocaleString('fr-FR') + ' €';
      document.getElementById('calc-target').textContent = target.toLocaleString('fr-FR') + ' €';
      document.getElementById('calc-gain').textContent = '+' + gainAnnuel.toLocaleString('fr-FR') + ' €';
      if (gainSuffix) gainSuffix.style.display = 'inline';
      if (gainAlt) gainAlt.style.display = 'none';
      if (cta) {
        cta.href = '[LIEN_CALENDLY_À_INSÉRER]';
        cta.textContent = 'Réserver mon appel stratégique →';
      }
    }
    result.style.display = 'flex';
    result.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });
})();
'''

html = html.replace('</script>', new_js + '\n</script>', 1)
print('✓ JS ajouté (bannière dynamique + formulaire + email gate)')

# ══════════════════════════════════════════════════════════
# CALC CTA — mettre à jour le texte Diagnostic gratuit
# ══════════════════════════════════════════════════════════
html = html.replace(
    '>Diagnostic gratuit →\n        </a>\n        <p class="calc-disclaimer">',
    '>Réserver mon appel stratégique →\n        </a>\n        <p class="calc-disclaimer">',
    1
)

# Écriture finale
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('\n✅ Toutes les modifications appliquées.')
