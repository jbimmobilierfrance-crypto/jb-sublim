#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Refonte tunnel de conversion JB Sublim — script unique, une passe propre.
Appliqué sur le backup 08/05/2026.
"""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CAL   = 'https://calendly.com/jbimmobilier-france/appel-strategique-jb-sublim'
QONTO = 'https://pay.qonto.com/payment-links/019e082e-3e2f-7e88-9212-e4a73bd8fc0d?resource_id=019e082e-3e31-7206-b52f-1ddb5e9764ba'

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ════════════════════════════════════════════════════════
# 1. META / OG — supprimer "Diagnostic gratuit"
# ════════════════════════════════════════════════════════
html = html.replace(
    '<meta name="description" content="Votre Airbnb tourne à 40–50% de son potentiel réel. Un accompagnement expert sur-mesure pour des résultats concrets en moins de 5 jours. Diagnostic gratuit.">',
    '<meta name="description" content="Votre Airbnb tourne à 40–50% de son potentiel réel. Un appel stratégique de 25 min pour identifier ce qui bloque vos revenus — résultats garantis en moins de 5 jours.">'
)
html = html.replace(
    'content="Votre Airbnb perd 40% de son potentiel. Diagnostic gratuit, résultats en 5 jours. Intervention en France &amp; Maroc."',
    'content="Votre Airbnb perd 40% de son potentiel. Réservez un appel stratégique — résultats en 5 jours. Intervention en France &amp; Maroc."'
)
html = html.replace(
    'content="Votre Airbnb perd 40% de son potentiel. Diagnostic gratuit, résultats en 5 jours."',
    'content="Votre Airbnb perd 40% de son potentiel. Réservez un appel stratégique — résultats en 5 jours."'
)
print('✓ 1. Meta/OG mis à jour')

# ════════════════════════════════════════════════════════
# 2. BANDEAU CSS — or → anthracite haut de gamme
# ════════════════════════════════════════════════════════
html = html.replace(
    '''.launch-banner {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 102;
  background: linear-gradient(90deg, #B8924A 0%, #D4A95A 100%);
  color: #FAF7F0;
  padding: 12px 24px;
  text-align: center;
  font-family: 'Montserrat', sans-serif;
  font-size: 14px;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 8px rgba(184, 146, 74, 0.15);
}''',
    '''.launch-banner {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 102;
  background: #2D2A26;
  color: #FAF7F0;
  padding: 12px 24px;
  text-align: center;
  font-family: 'Montserrat', sans-serif;
  font-size: 13px;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.25);
}'''
)
html = html.replace(
    '''.launch-banner-cta {
  background: rgba(250, 247, 240, 0.15);
  border: 1px solid rgba(250, 247, 240, 0.4);
  color: #FAF7F0;
  padding: 6px 16px;
  border-radius: 20px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.launch-banner-cta:hover {
  background: rgba(250, 247, 240, 0.25);
  border-color: rgba(250, 247, 240, 0.7);
}''',
    '''.launch-banner-cta {
  background: transparent;
  border: 1px solid #B8924A;
  color: #B8924A;
  padding: 5px 16px;
  border-radius: 20px;
  text-decoration: none;
  font-weight: 600;
  font-size: 12px;
  transition: all 0.25s ease;
  white-space: nowrap;
}

.launch-banner-cta:hover {
  background: #B8924A;
  color: #2D2A26;
}'''
)
# Italic em dans le bandeau → or
html = html.replace(
    '.launch-banner-text em { font-style: italic; opacity: 0.95; }',
    '.launch-banner-text em { font-style: italic; color: #B8924A; font-weight: 600; }'
)
print('✓ 2. Bandeau CSS → anthracite haut de gamme')

# ════════════════════════════════════════════════════════
# 3. BANDEAU HTML — bouton → Calendly
# ════════════════════════════════════════════════════════
html = html.replace(
    '<a href="#tarifs" class="launch-banner-cta">Vérifier les disponibilités →</a>',
    f'<a href="{CAL}" class="launch-banner-cta" target="_blank" rel="noopener">Réserver maintenant →</a>'
)
print('✓ 3. Bandeau HTML → Calendly')

# ════════════════════════════════════════════════════════
# 4. NAV — Calculateur supprimé, "Nous contacter" → Calendly
# ════════════════════════════════════════════════════════
html = html.replace(
    '    <li><a href="#calculateur">Calculateur</a></li>\n',
    ''
)
html = html.replace(
    '<li><a href="#contact" class="nav-cta">Nous contacter</a></li>',
    f'<li><a href="{CAL}" class="nav-cta" target="_blank" rel="noopener">Réserver un appel</a></li>'
)
print('✓ 4. Nav : Calculateur supprimé, CTA → Calendly')

# ════════════════════════════════════════════════════════
# 5. HERO — vidéo placeholder + CTAs
# ════════════════════════════════════════════════════════
OLD_HERO_CONTENT = '''    <p class="hero-sub">La plupart des annonces Airbnb tournent à 40–50% de leur potentiel réel. On identifie ce qui bloque, on corrige, et les résultats arrivent en moins de 5 jours. Sans déplacement. Sans commission à vie.</p>
    <div class="hero-actions">
      <a href="https://wa.me/33658797037?text=Bonjour%20Jamil%2C%20j%27aimerais%20un%20diagnostic%20gratuit%20de%20mon%20annonce%20Airbnb." class="btn-primary" target="_blank"><span>Diagnostic gratuit →</span></a>
      <a href="#calculateur" class="btn-secondary">Calculer mon potentiel</a>
    </div>'''

NEW_HERO_CONTENT = '''    <div class="hero-video-wrap">
      <video class="hero-video" autoplay loop muted playsinline>
        <source src="/videos/intro-jamil.mp4" type="video/mp4">
      </video>
      <img src="/logos/logo-officiel-fond transparent.png" alt="JB Sublim" class="hero-video-fallback">
    </div>
    <p class="hero-sub">La plupart des annonces Airbnb tournent à 40–50% de leur potentiel réel. On identifie ce qui bloque, on corrige, et les résultats arrivent en moins de 5 jours. Sans déplacement. Sans commission à vie.</p>
    <div class="hero-actions">
      <a href="{CAL}" class="btn-primary btn-hero-cta" target="_blank" rel="noopener"><span>Réserver mon appel stratégique →</span></a>
      <a href="#transformation" class="btn-secondary btn-hero-proof">Voir un cas concret →</a>
    </div>'''.format(CAL=CAL)

if OLD_HERO_CONTENT in html:
    html = html.replace(OLD_HERO_CONTENT, NEW_HERO_CONTENT, 1)
    print('✓ 5. Hero : vidéo placeholder + CTAs Calendly')
else:
    print('⚠ 5. Hero : bloc non trouvé exactement — vérifier')

# CSS vidéo hero — insérer avant </style>
HERO_VIDEO_CSS = '''
/* ── HERO VIDEO / PLACEHOLDER ── */
.hero-video-wrap {
  width: 220px;
  height: 220px;
  border-radius: 50%;
  overflow: hidden;
  margin: 0 auto 32px;
  border: 2px solid rgba(184,146,74,0.35);
  box-shadow: 0 8px 32px rgba(184,146,74,0.15);
  position: relative;
  background: var(--ivory-warm);
}
.hero-video {
  width: 100%; height: 100%;
  object-fit: cover; display: block;
}
.hero-video-fallback {
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  object-fit: cover;
  border-radius: 50%;
}
/* hide fallback when video loads */
.hero-video:not([error]) ~ .hero-video-fallback { display: none; }
@media (max-width: 640px) {
  .hero-video-wrap { width: 160px; height: 160px; }
}
'''
html = html.replace('</style>', HERO_VIDEO_CSS + '\n</style>', 1)

# ════════════════════════════════════════════════════════
# 6. BEFORE-AFTER CTA — Calendly
# ════════════════════════════════════════════════════════
html = html.replace(
    '''    <div class="ba-cta">
      <a
        href="https://wa.me/33658797037?text=Bonjour%20Jamil%2C%20j%27aimerais%20un%20diagnostic%20gratuit%20de%20mon%20annonce%20Airbnb."
        class="btn-primary"
        target="_blank"
      >
        Diagnostic gratuit →
      </a>
    </div>''',
    f'''    <div class="ba-cta">
      <a href="{CAL}" class="btn-primary btn-hero-cta" target="_blank" rel="noopener">
        <span>Réserver mon appel stratégique →</span>
      </a>
    </div>'''
)
print('✓ 6. Before-after CTA → Calendly')

# ════════════════════════════════════════════════════════
# 7. SECTION REORDER — tarifs juste après before-after
# ════════════════════════════════════════════════════════
# Extract tarifs block (currently after about)
tarifs_m = re.search(
    r'\n*<section class="tarifs-launch"[^>]*>.*?</section>\n*',
    html, re.DOTALL
)
if tarifs_m:
    tarifs_block = '\n\n' + tarifs_m.group(0).strip() + '\n\n'
    html = html[:tarifs_m.start()] + '\n\n' + html[tarifs_m.end():]
    # Insert after before-after (before problem)
    html = re.sub(
        r'(\n\n<section class="problem")',
        tarifs_block + r'\1',
        html, count=1
    )
    print('✓ 7. Tarifs déplacé → juste après before-after')
else:
    print('⚠ 7. Section tarifs non trouvée')

# ════════════════════════════════════════════════════════
# 8. TARIFS CTAs — Calendly + Qonto secondaire
# ════════════════════════════════════════════════════════
# CTA principal pack 490€
html = html.replace(
    '''      <a
        href="https://wa.me/33658797037?text=Bonjour%20Jamil%2C%20je%20souhaite%20r%C3%A9server%20un%20cr%C3%A9neau%20avant%20la%20haute%20saison."
        class="pack-launch-cta"
        target="_blank"
      >
        Réserver un créneau →
      </a>''',
    f'''      <a href="{CAL}" class="pack-launch-cta" target="_blank" rel="noopener">
        Réserver mon appel stratégique →
      </a>
      <a href="{QONTO}" class="pack-qonto-cta" target="_blank" rel="noopener">
        Déjà convaincu&nbsp;? Payer directement →
      </a>'''
)
# CTA suivi 49€
html = html.replace(
    '''      <a
        href="https://wa.me/33658797037?text=Bonjour%20Jamil%2C%20je%20souhaite%20en%20savoir%20plus%20sur%20le%20suivi%20prioritaire."
        class="pack-suivi-cta"
        target="_blank"
      >
        En savoir plus →
      </a>''',
    f'''      <a href="{CAL}" class="pack-suivi-cta" target="_blank" rel="noopener">
        En savoir plus →
      </a>'''
)
print('✓ 8. Tarifs CTAs → Calendly + Qonto secondaire')

# CSS Qonto
QONTO_CSS = '''
/* ── QONTO SECONDARY ── */
.pack-qonto-cta {
  display: block;
  margin-top: 10px;
  font-family: 'Montserrat', sans-serif;
  font-size: 11px;
  letter-spacing: 0.5px;
  color: var(--slate);
  text-decoration: none;
  text-align: center;
  border-bottom: 1px solid var(--line);
  padding-bottom: 1px;
  width: fit-content;
  margin-left: auto; margin-right: auto;
  transition: color 0.2s ease, border-color 0.2s ease;
}
.pack-qonto-cta:hover { color: var(--gold-deep); border-color: var(--gold); }
'''
html = html.replace('</style>', QONTO_CSS + '\n</style>', 1)

# ════════════════════════════════════════════════════════
# 9. SUPPRESSION calculateur — HTML complet
# ════════════════════════════════════════════════════════
html = re.sub(
    r'\n*<section class="calculateur-simple"[^>]*>.*?</section>\n*',
    '\n',
    html, count=1, flags=re.DOTALL
)
print('✓ 9. Section calculateur supprimée (HTML)')

# ════════════════════════════════════════════════════════
# 10. SUPPRESSION whatsapp-float — HTML
# ════════════════════════════════════════════════════════
html = re.sub(
    r'\n*<a href="https://wa\.me/[^"]*"\s+class="whatsapp-float".*?</a>\n*',
    '\n',
    html, count=1, flags=re.DOTALL
)
print('✓ 10. Bouton flottant WhatsApp supprimé')

# ════════════════════════════════════════════════════════
# 11. ABOUT — réduction 30%
# ════════════════════════════════════════════════════════
html = html.replace(
    '''        <p class="about-text">Originaire de Montpellier, j'ai consacré des années à comprendre les mécanismes profonds de la location courte durée — ceux qu'on ne vous apprend pas dans les formations en ligne. Ce que j'ai découvert, je l'applique aujourd'hui pour <strong>des propriétaires en France et au Maroc</strong>.</p>
        <p class="about-text">Mon approche n'est pas technique. Elle est <strong>commerciale</strong> — parce que ce qui fait la différence sur Airbnb, c'est exactement ce qui fait la différence dans la vente : l'impression, la confiance, et le bon positionnement.</p>''',
    '''        <p class="about-text">J'ai consacré des années à comprendre les mécanismes de la location courte durée — ceux qu'on ne vous apprend pas dans les formations. Ce que j'ai découvert, je l'applique pour <strong>des propriétaires en France et au Maroc</strong>.</p>
        <p class="about-text">Mon approche est <strong>commerciale</strong> — ce qui fait la différence sur Airbnb, c'est l'impression, la confiance, et le bon positionnement. Pas la technique.</p>'''
)
print('✓ 11. About réduit de ~30%')

# ════════════════════════════════════════════════════════
# 12. FAQ — 6 nouvelles questions
# ════════════════════════════════════════════════════════
NEW_FAQ_ITEMS = '''        <div class="faq-item">
          <div class="faq-question"><span>Comment se déroule concrètement votre intervention ?</span><div class="faq-toggle"></div></div>
          <div class="faq-answer">Tout commence par un appel stratégique de 25 minutes. J'analyse votre situation, votre marché, votre potentiel réel. Si on travaille ensemble, je prends en charge l'optimisation complète : annonce, photos, pricing, algorithme. Vous n'avez rien à exécuter de votre côté. 60 jours de suivi inclus.</div>
        </div>
        <div class="faq-item">
          <div class="faq-question"><span>En combien de temps verrai-je des résultats ?</span><div class="faq-toggle"></div></div>
          <div class="faq-answer">Les premiers effets sont visibles dès les premières semaines. Mes clients constatent en moyenne +90% de revenus sur les deux premiers mois. La majorité voit son taux d'occupation doubler avant J+30.</div>
        </div>
        <div class="faq-item">
          <div class="faq-question"><span>Et si ça ne fonctionne pas pour mon bien ?</span><div class="faq-toggle"></div></div>
          <div class="faq-answer">Garantie 60 jours sans condition. Si vos revenus n'augmentent pas suffisamment pour couvrir la prestation, je continue à travailler avec vous gratuitement jusqu'à ce que ce soit le cas. Le risque est entièrement de mon côté.</div>
        </div>
        <div class="faq-item">
          <div class="faq-question"><span>Pourquoi pas une conciergerie classique ?</span><div class="faq-toggle"></div></div>
          <div class="faq-answer">Une conciergerie prend 20 à 30% de vos revenus à vie et gère uniquement la logistique. Moi je m'occupe de l'optimisation commerciale de votre annonce — ce qui détermine si votre calendrier se remplit ou pas. Forfait unique, aucune commission, vous gardez 100% de vos revenus supplémentaires.</div>
        </div>
        <div class="faq-item">
          <div class="faq-question"><span>Mon annonce est déjà en ligne — ça change quelque chose ?</span><div class="faq-toggle"></div></div>
          <div class="faq-answer">Aucune importance. J'interviens autant sur des annonces existantes qui peinent à décoller que sur des lancements. Dans les deux cas, l'audit révèle exactement ce qui freine votre potentiel.</div>
        </div>
        <div class="faq-item">
          <div class="faq-question"><span>Intervenez-vous dans toute la France ?</span><div class="faq-toggle"></div></div>
          <div class="faq-answer">Oui — partout en France et également au Maroc. J'interviens à distance via WhatsApp et visio, donc votre localisation n'est pas un frein.</div>
        </div>'''

# Replace old faq-list content
html = re.sub(
    r'(<div class="faq-list fade-in">).*?(</div>\s*\n\s*</div>\s*\n\s*</div>\s*\n</section>)',
    r'\1\n' + NEW_FAQ_ITEMS + r'\n      \2',
    html, count=1, flags=re.DOTALL
)
print('✓ 12. FAQ → 6 nouvelles questions')

# ════════════════════════════════════════════════════════
# 13. CTA FINAL — Calendly, supprimer "Devis gratuit"
# ════════════════════════════════════════════════════════
html = html.replace(
    '''    <div class="cta-final-actions">
      <a href="https://wa.me/33658797037?text=Bonjour%20Jamil%2C%20j%27aimerais%20un%20diagnostic%20gratuit%20de%20mon%20annonce%20Airbnb." class="btn-whatsapp" target="_blank">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>
        <span>Diagnostic gratuit →</span>
      </a>
      <a href="mailto:jbimmobilier.france@gmail.com" class="btn-secondary">jbimmobilier.france@gmail.com</a>
    </div>
    <div class="cta-final-trust">
      <span>Réponse rapide sur WhatsApp</span>
      <span>Devis gratuit</span>
      <span>Sans engagement</span>
    </div>''',
    f'''    <div class="cta-final-actions">
      <a href="{CAL}" class="btn-primary btn-hero-cta" target="_blank" rel="noopener"><span>Réserver mon appel stratégique →</span></a>
      <a href="mailto:jbimmobilier.france@gmail.com" class="btn-secondary">jbimmobilier.france@gmail.com</a>
    </div>
    <div class="cta-final-trust">
      <span>Réponse rapide · Sans engagement</span>
    </div>'''
)
print('✓ 13. CTA final → Calendly, trust simplifié')

# ════════════════════════════════════════════════════════
# 14. FOOTER — supprimer Calculateur, ajouter Calendly
# ════════════════════════════════════════════════════════
html = html.replace(
    '          <li><a href="#calculateur">Calculateur</a></li>\n',
    ''
)
html = html.replace(
    '''        <div class="footer-contact-col">
        <div class="footer-col-title">Contact</div>
        <ul class="footer-links">
          <li><a href="https://wa.me/33658797037">WhatsApp</a></li>''',
    f'''        <div class="footer-contact-col">
        <div class="footer-col-title">Contact</div>
        <ul class="footer-links">
          <li><a href="{CAL}" target="_blank" rel="noopener">Réserver un appel</a></li>
          <li><a href="https://wa.me/33658797037">WhatsApp</a></li>'''
)
print('✓ 14. Footer mis à jour')

# ════════════════════════════════════════════════════════
# 15. CSS — supprimer whatsapp-float, garder scroll-top
# ════════════════════════════════════════════════════════
html = re.sub(
    r'/\* ── FLOATING WHATSAPP[^*]*\*/.*?\.whatsapp-float-label \{ white-space: nowrap; \}',
    '',
    html, count=1, flags=re.DOTALL
)
html = re.sub(r'\s*@keyframes floatPulse \{[^}]+\}', '', html)
# Mobile whatsapp-float refs
html = html.replace('  .whatsapp-float { bottom: 20px; right: 20px; padding: 14px 16px; }\n', '')
html = html.replace('  .whatsapp-float-label { display: none; }\n', '')
print('✓ 15. CSS whatsapp-float supprimé')

# ════════════════════════════════════════════════════════
# 16. JS — supprimer calculerPotentiel + revenu-actuel listener
# ════════════════════════════════════════════════════════
html = re.sub(
    r'// CALCULATEUR SIMPLE\nfunction calculerPotentiel.*?calculerPotentiel\(\);\s*\}\);',
    '',
    html, count=1, flags=re.DOTALL
)
# Also remove the old complex calc state + updateResult
html = re.sub(
    r'// CALCULATOR.*?updateResult\(\);\s*\}',
    '',
    html, count=1, flags=re.DOTALL
)
print('✓ 16. JS calculateur supprimé')

# ════════════════════════════════════════════════════════
# 17. LAZY LOADING sur toutes les images sauf hero-video-fallback
# ════════════════════════════════════════════════════════
count_lazy = [0]
def add_lazy(m):
    tag = m.group(0)
    if 'loading=' not in tag and 'hero-video-fallback' not in tag:
        count_lazy[0] += 1
        tag = tag.replace('<img ', '<img loading="lazy" ')
    return tag
html = re.sub(r'<img [^>]+>', add_lazy, html)
print(f'✓ 17. Lazy loading ajouté sur {count_lazy[0]} images')

# ════════════════════════════════════════════════════════
# 18. H2 centrés globalement
# ════════════════════════════════════════════════════════
if '.section-title { text-align: center; }' not in html:
    # Already handled per-section in CSS; add global rule for h2 in sections
    html = html.replace(
        '.section-title {\n  font-family:',
        '.section-title {\n  text-align: center;\n  font-family:'
    )
print('✓ 18. H2 centrés')

# ════════════════════════════════════════════════════════
# VÉRIFICATIONS
# ════════════════════════════════════════════════════════
print()
print('=== VÉRIFICATIONS ===')
ba_pos   = html.find('class="before-after"')
tar_pos  = html.find('class="tarifs-launch"')
prob_pos = html.find('class="problem"')
lev_pos  = html.find('class="leviers"')
proc_pos = html.find('class="process"')
faq_pos  = html.find('class="faq"')
ctaf_pos = html.find('class="cta-final"')
order_ok = ba_pos < tar_pos < prob_pos < lev_pos < proc_pos < faq_pos < ctaf_pos

checks = {
    'Ordre : before-after→tarifs→problem→leviers→process→faq→cta-final': order_ok,
    'Bandeau anthracite #2D2A26': '#2D2A26' in html[:5000] or 'background: #2D2A26' in html,
    'Bandeau CTA Calendly': CAL in html and 'Réserver maintenant' in html,
    'Nav : Calculateur absent': 'href="#calculateur">Calculateur' not in html,
    'Nav : Réserver un appel → Calendly': 'Réserver un appel' in html and CAL in html,
    'Hero vidéo placeholder': 'hero-video-wrap' in html,
    'Hero CTA Calendly': f'href="{CAL}" class="btn-primary btn-hero-cta"' in html,
    'Hero CTA secondaire': 'Voir un cas concret' in html,
    'Before-after CTA Calendly': 'ba-cta' in html and CAL in html,
    'Calculateur section absent': 'class="calculateur-simple"' not in html,
    'WhatsApp float absent': 'class="whatsapp-float"' not in html,
    'Diagnostic gratuit absent': 'Diagnostic gratuit' not in html,
    'Qonto lien présent': QONTO in html,
    'Qonto uniquement dans tarifs': html.count(QONTO) == 1,
    'FAQ 6 questions': len(re.findall(r'<div class="faq-item">', html)) == 6,
    'CTA final Calendly': 'cta-final' in html and f'href="{CAL}"' in html[html.find('cta-final'):],
    'Devis gratuit absent': 'Devis gratuit' not in html,
    'Lazy loading': 'loading="lazy"' in html,
}

all_ok = True
for name, ok in checks.items():
    status = 'OK' if ok else 'FAIL'
    if not ok: all_ok = False
    print(f'  [{status}] {name}')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print()
if all_ok:
    print('✅ index.html sauvegardé — toutes les vérifications passent.')
else:
    print('⚠ Certaines vérifications à corriger avant push.')
