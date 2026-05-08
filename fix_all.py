#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix all 5 issues reported by user — JB Sublim 08/05/2026"""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CALENDLY = 'https://calendly.com/jbimmobilier-france/appel-strategique-jb-sublim'

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ══════════════════════════════════════════════════════════
# 1. SECTION TÉMOIGNAGES — double-vérification
# ══════════════════════════════════════════════════════════
if '<section class="temoignages"' in html:
    html = re.sub(
        r'\n*<section class="temoignages"[^>]*>.*?</section>\n*',
        '\n', html, count=1, flags=re.DOTALL
    )
    print('✓ Section témoignages supprimée')
else:
    print('— Témoignages déjà absent')

# ══════════════════════════════════════════════════════════
# 2. BOUTON FLOTTANT — WhatsApp → Calendly
# ══════════════════════════════════════════════════════════
# Remplace l'intégralité du bouton flottant
OLD_FLOAT = re.search(
    r'<a href="https://wa\.me/[^"]*"\s+class="whatsapp-float".*?</a>',
    html, re.DOTALL
)
if OLD_FLOAT:
    NEW_FLOAT = '''<a href="{CAL}"
   class="calendly-float"
   target="_blank"
   rel="noopener"
   aria-label="Réserver mon appel stratégique">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="22" height="22">
    <rect x="3" y="4" width="18" height="18" rx="2"/>
    <path d="M16 2v4M8 2v4M3 10h18"/>
    <path d="M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01"/>
  </svg>
  <span class="calendly-float-label">Réserver mon appel</span>
</a>'''.format(CAL=CALENDLY)
    html = html[:OLD_FLOAT.start()] + NEW_FLOAT + html[OLD_FLOAT.end():]
    print('✓ Bouton flottant → Calendly')
else:
    print('⚠ Bouton flottant non trouvé')

# CSS : remplacer whatsapp-float par calendly-float (couleur or/anthracite)
html = re.sub(
    r'/\* ── FLOATING WHATSAPP.*?(?=/\* ──)',
    '''/* ── FLOATING CALENDLY ── */
.calendly-float {
  position: fixed;
  bottom: 32px;
  right: 32px;
  z-index: 999;
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--anthracite);
  color: var(--ivory);
  text-decoration: none;
  padding: 14px 20px;
  border-radius: 50px;
  font-size: 12px;
  letter-spacing: 1.5px;
  font-weight: 500;
  font-family: var(--sans);
  box-shadow: 0 4px 20px rgba(74, 70, 62, 0.35);
  animation: floatPulse 3s ease-in-out infinite;
  transition: background 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease, gap 0.2s ease;
}
.calendly-float:hover {
  background: var(--gold-deep);
  transform: translateY(-3px);
  box-shadow: 0 8px 28px rgba(184, 146, 74, 0.45);
  gap: 12px;
}
.calendly-float svg { flex-shrink: 0; }
.calendly-float-label { white-space: nowrap; }

@keyframes floatPulse {
  0%, 100% { box-shadow: 0 4px 20px rgba(74, 70, 62, 0.35); }
  50% { box-shadow: 0 4px 28px rgba(74, 70, 62, 0.5); }
}

''',
    html, count=1, flags=re.DOTALL
)
# Mobile override
html = html.replace(
    '.whatsapp-float { bottom: 20px; right: 20px; padding: 14px 16px; }',
    '.calendly-float { bottom: 20px; right: 20px; padding: 14px 16px; }'
)
html = html.replace(
    '.whatsapp-float-label { display: none; }',
    '.calendly-float-label { display: none; }'
)
print('✓ CSS bouton flottant mis à jour')

# ══════════════════════════════════════════════════════════
# 3. CALCULATEUR — suppression complète (HTML + nav + CSS + JS)
# ══════════════════════════════════════════════════════════

# 3a. Nav link
html = re.sub(r'\s*<li><a href="#calculateur">Calculateur</a></li>', '', html)
print('✓ Nav : lien Calculateur supprimé')

# 3b. Hero "Calculer mon potentiel" button
html = re.sub(
    r'\s*<a href="#calculateur" class="btn-secondary">Calculer mon potentiel</a>',
    '', html
)
print('✓ Hero : bouton secondaire Calculateur supprimé')

# 3c. Calculateur section HTML
html = re.sub(
    r'\n*<section class="calculateur-simple"[^>]*>.*?</section>\n*',
    '\n', html, count=1, flags=re.DOTALL
)
print('✓ Section calculateur supprimée')

# 3d. CSS blocks for calculator
# Block 1: /* ── CALCULATEUR ── */ (the original old one)
html = re.sub(
    r'/\* ── CALCULATEUR ── \*/.*?(?=/\* ──)',
    '', html, count=1, flags=re.DOTALL
)
# Block 2: /* ─── CALCULATEUR SIMPLE ─── */
html = re.sub(
    r'/\*[\s─]*CALCULATEUR SIMPLE[\s─]*\*/.*?(?=/\* ──)',
    '', html, count=1, flags=re.DOTALL
)
# Block 3: /* ── CALCULATEUR EMAIL GATE ── */
html = re.sub(
    r'/\* ── CALCULATEUR EMAIL GATE ── \*/.*?(?=/\* ──)',
    '', html, count=1, flags=re.DOTALL
)
# Mobile calc overrides inside media queries
html = re.sub(r'\s*\.calc-[^\n}]*\n', '\n', html)
html = re.sub(r'\s*\.calculator[^\n}]*\n', '\n', html)
print('✓ CSS calculateur supprimé')

# 3e. JS: calculerPotentiel function + keypress listener
html = re.sub(
    r'// CALCULATEUR SIMPLE\nfunction calculerPotentiel.*?}\s*\n\s*document\.getElementById\(\'revenu-actuel\'\)\?\.addEventListener\(\'keypress\'[^\)]+\)[^;]*;\s*\n',
    '', html, count=1, flags=re.DOTALL
)
# JS: calc email gate IIFE
html = re.sub(
    r'\(function\(\) \{\s*var pending = false;\s*var origCalculer = window\.calculerPotentiel;.*?\}\)\(\);\s*\n',
    '', html, count=1, flags=re.DOTALL
)
print('✓ JS calculateur supprimé')

# ══════════════════════════════════════════════════════════
# 4. BANDEAU — texte statique (supprimer "chargement…")
# ══════════════════════════════════════════════════════════
OLD_BANNER_TEXT = '''      <span class="launch-banner-icon">✦</span>
      Prochain créneau disponible :
      <strong id="bannerNextSlot">chargement…</strong>
      · <em>490€ au lieu de 790€</em>'''

NEW_BANNER_TEXT = '''      <span class="launch-banner-icon">✦</span>
      3 créneaux disponibles avant la haute saison · <em>490€ au lieu de 790€</em>'''

if OLD_BANNER_TEXT in html:
    html = html.replace(OLD_BANNER_TEXT, NEW_BANNER_TEXT, 1)
    print('✓ Bandeau : texte statique appliqué')
else:
    print('⚠ Bandeau texte non trouvé exactement — tentative regex')
    html = re.sub(
        r'Prochain créneau disponible\s*:?\s*<strong[^>]*>chargement[^<]*</strong>\s*·\s*',
        '3 créneaux disponibles avant la haute saison · ',
        html
    )
    print('✓ Bandeau : regex appliqué')

# Supprimer le JS du bandeau dynamique
html = re.sub(
    r'// BANNIÈRE — prochain créneau dynamique\s*\(function\(\).*?\}\)\(\);\s*\n',
    '', html, count=1, flags=re.DOTALL
)
print('✓ JS bannière dynamique supprimé')

# ══════════════════════════════════════════════════════════
# 5. MENU "NOUS CONTACTER" → Calendly
# ══════════════════════════════════════════════════════════
html = re.sub(
    r'<a href="#contact" class="nav-cta">Nous contacter</a>',
    '<a href="{CAL}" class="nav-cta" target="_blank" rel="noopener">Nous contacter</a>'.format(CAL=CALENDLY),
    html
)
print('✓ Nav : "Nous contacter" → Calendly')

# ══════════════════════════════════════════════════════════
# Vérifications finales
# ══════════════════════════════════════════════════════════
checks = {
    'temoignages section': '<section class="temoignages"' not in html,
    'calculateur section': 'class="calculateur-simple"' not in html,
    'nav calculateur link': 'href="#calculateur">Calculateur' not in html,
    'chargement banner': 'chargement' not in html,
    'whatsapp-float HTML': 'class="whatsapp-float"' not in html,
    'calendly-float HTML': 'class="calendly-float"' in html,
    'nous contacter → calendly': 'href="#contact"' not in html,
}
print()
print('=== VÉRIFICATIONS ===')
all_ok = True
for name, ok in checks.items():
    print(f'  [{"OK" if ok else "FAIL"}] {name}')
    if not ok: all_ok = False

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

if all_ok:
    print('\n✅ Tout appliqué — index.html sauvegardé.')
else:
    print('\n⚠ Certains points à vérifier manuellement.')
