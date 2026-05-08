#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Patch links and placeholders — Calendly, Qonto, logo placeholder, temo cleanup"""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CALENDLY = 'https://calendly.com/jbimmobilier-france/appel-strategique-jb-sublim'
QONTO    = 'https://pay.qonto.com/payment-links/019e082e-3e2f-7e88-9212-e4a73bd8fc0d?resource_id=019e082e-3e31-7206-b52f-1ddb5e9764ba'

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ══════════════════════════════════════════════════════════
# 1. Remplace tous les placeholders Calendly
# ══════════════════════════════════════════════════════════
count = html.count('[LIEN_CALENDLY_À_INSÉRER]')
html = html.replace('[LIEN_CALENDLY_À_INSÉRER]', CALENDLY)
print(f'✓ Calendly : {count} occurrences remplacées')

# ══════════════════════════════════════════════════════════
# 2. Qonto CTA secondaire — dans tarifs, après le bouton Calendly
# ══════════════════════════════════════════════════════════
OLD_CTA_BLOCK = '''        <a href="{CAL}" class="pack-launch-cta qualify-cta" id="qualifyCta" target="_blank" aria-disabled="true">
          Réserver mon appel stratégique →
        </a>'''.format(CAL=CALENDLY)

NEW_CTA_BLOCK = '''        <a href="{CAL}" class="pack-launch-cta qualify-cta" id="qualifyCta" target="_blank" aria-disabled="true">
          Réserver mon appel stratégique →
        </a>
        <a href="{QONTO}" class="qonto-secondary-cta" target="_blank" rel="noopener">
          Déjà convaincu&nbsp;? Payer directement →
        </a>'''.format(CAL=CALENDLY, QONTO=QONTO)

if OLD_CTA_BLOCK in html:
    html = html.replace(OLD_CTA_BLOCK, NEW_CTA_BLOCK, 1)
    print('✓ Qonto CTA secondaire ajouté dans tarifs')
else:
    print('⚠ Bloc CTA tarifs non trouvé — vérifier manuellement')

# ══════════════════════════════════════════════════════════
# 3. Hero : vidéo → logo placeholder
# ══════════════════════════════════════════════════════════
OLD_VIDEO = '''    <div class="hero-video-wrap">
      <video class="hero-video" autoplay loop muted playsinline>
        <source src="/videos/intro-jamil.mp4" type="video/mp4">
      </video>
    </div>'''

NEW_VIDEO = '''    <div class="hero-video-wrap hero-video-placeholder">
      <img src="/logos/logo-officiel-fond transparent.png" alt="JB Sublim" class="hero-logo-img">
    </div>'''

if OLD_VIDEO in html:
    html = html.replace(OLD_VIDEO, NEW_VIDEO, 1)
    print('✓ Hero : logo placeholder à la place de la vidéo')
else:
    print('⚠ Bloc vidéo hero non trouvé — vérifier manuellement')

# ══════════════════════════════════════════════════════════
# 4. Témoignages : cards propres "Témoignage à venir"
# ══════════════════════════════════════════════════════════
CLEAN_TEMO_GRID = '''    <div class="temo-grid">

      <div class="temo-card temo-pending fade-in">
        <div class="temo-stars">★★★★★</div>
        <blockquote class="temo-quote temo-coming">&laquo;&nbsp;Témoignage à venir&nbsp;&raquo;</blockquote>
        <div class="temo-result temo-result-pending">Premier client en cours d'intégration</div>
      </div>

      <div class="temo-card temo-pending fade-in">
        <div class="temo-stars">★★★★★</div>
        <blockquote class="temo-quote temo-coming">&laquo;&nbsp;Témoignage à venir&nbsp;&raquo;</blockquote>
        <div class="temo-result temo-result-pending">Premier client en cours d'intégration</div>
      </div>

      <div class="temo-card temo-pending fade-in">
        <div class="temo-stars">★★★★★</div>
        <blockquote class="temo-quote temo-coming">&laquo;&nbsp;Témoignage à venir&nbsp;&raquo;</blockquote>
        <div class="temo-result temo-result-pending">Premier client en cours d'intégration</div>
      </div>

    </div>'''

OLD_TEMO_GRID = re.search(
    r'<div class="temo-grid">.*?</div>\s*</div>\s*</section>',
    html, re.DOTALL
)
if OLD_TEMO_GRID:
    old_block = OLD_TEMO_GRID.group(0)
    new_block = CLEAN_TEMO_GRID + '\n  </div>\n</section>'
    html = html.replace(old_block, new_block, 1)
    print('✓ Témoignages : placeholders nettoyés')
else:
    print('⚠ temo-grid non trouvé — vérifier manuellement')

# ══════════════════════════════════════════════════════════
# 5. CSS — Qonto CTA + hero logo img + temo-pending
# ══════════════════════════════════════════════════════════
CSS_PATCH = '''
/* ── QONTO SECONDARY CTA ── */
.qonto-secondary-cta {
  display: block;
  text-align: center;
  margin-top: 10px;
  font-size: 11px;
  letter-spacing: 0.5px;
  color: var(--slate);
  text-decoration: none;
  border-bottom: 1px solid var(--line);
  padding-bottom: 1px;
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
  transition: color 0.2s ease, border-color 0.2s ease;
}
.qonto-secondary-cta:hover { color: var(--gold-deep); border-color: var(--gold); }

/* ── HERO LOGO PLACEHOLDER ── */
.hero-logo-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  border-radius: 50%;
}

/* ── TEMO PENDING CARDS ── */
.temo-pending { border: 1px dashed var(--line); background: transparent; }
.temo-coming {
  color: var(--slate);
  font-style: italic;
  opacity: 0.6;
  font-size: 15px;
}
.temo-result-pending {
  font-size: 11px;
  color: var(--slate);
  opacity: 0.5;
  letter-spacing: 0.5px;
}
'''

if CSS_PATCH.strip() not in html:
    html = html.replace('</style>', CSS_PATCH + '\n</style>', 1)
    print('✓ CSS : Qonto + logo placeholder + temo-pending ajouté')
else:
    print('— CSS déjà présent')

# ══════════════════════════════════════════════════════════
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('\n✅ Patch appliqué — index.html sauvegardé.')
