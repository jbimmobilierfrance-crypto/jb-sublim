#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Refonte tunnel de conversion — JB Sublim
Objectif : chaque élément pousse vers Calendly. Aucune autre sortie.
"""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CALENDLY = 'https://calendly.com/jbimmobilier-france/appel-strategique-jb-sublim'
QONTO    = 'https://pay.qonto.com/payment-links/019e082e-3e2f-7e88-9212-e4a73bd8fc0d?resource_id=019e082e-3e31-7206-b52f-1ddb5e9764ba'

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ══════════════════════════════════════════════════════════
# 1. META / OG — supprimer "Diagnostic gratuit"
# ══════════════════════════════════════════════════════════
html = re.sub(
    r'(content="[^"]*)\bDiagnostic gratuit\b([^"]*")',
    lambda m: m.group(1) + 'Appel stratégique sur-mesure' + m.group(2),
    html
)
# Meta description
html = re.sub(
    r'<meta name="description" content="[^"]*">',
    '<meta name="description" content="Votre Airbnb tourne à 40–50% de son potentiel réel. Un accompagnement expert sur-mesure — appel stratégique de 25 min. Résultats garantis en moins de 5 jours.">',
    html
)
print('✓ Meta/OG — Diagnostic gratuit supprimé')

# ══════════════════════════════════════════════════════════
# 2. BANDEAU — texte tunnel + lien Calendly
# ══════════════════════════════════════════════════════════
OLD_BANNER_INNER = re.search(r'<div class="launch-banner-inner">.*?</div>\s*<button', html, re.DOTALL)
if OLD_BANNER_INNER:
    NEW_BANNER_INNER = '''<div class="launch-banner-inner">
    <span class="launch-banner-text">
      <span class="launch-banner-icon">✦</span>
      3 créneaux disponibles avant la haute saison &nbsp;·&nbsp; <em>490€ au lieu de 790€</em>
    </span>
    <a href="{CAL}" class="launch-banner-cta" target="_blank" rel="noopener">Réserver maintenant →</a>
  </div>
  <button'''.format(CAL=CALENDLY)
    html = html[:OLD_BANNER_INNER.start()] + NEW_BANNER_INNER + html[OLD_BANNER_INNER.end()-len('<button'):]
print('✓ Bandeau → Calendly')

# ══════════════════════════════════════════════════════════
# 3. HERO — CTA secondaire "Voir un cas concret →"
# ══════════════════════════════════════════════════════════
OLD_HERO_ACTIONS = '''    <div class="hero-actions">
      <a href="{CAL}" class="btn-primary btn-calendly" target="_blank"><span>Réserver mon appel stratégique →</span></a>
    </div>
    <div class="hero-wa-secondary">
      <a href="https://wa.me/33658797037?text=Bonjour%20Jamil%2C%20j%27ai%20une%20question%20urgente." target="_blank" class="wa-secondary-link">
        <svg viewBox="0 0 24 24" fill="currentColor" width="13" height="13"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>
        Question urgente — WhatsApp
      </a>
    </div>'''.format(CAL=CALENDLY)

NEW_HERO_ACTIONS = '''    <div class="hero-actions">
      <a href="{CAL}" class="btn-primary btn-calendly" target="_blank" rel="noopener"><span>Réserver mon appel stratégique →</span></a>
      <a href="#transformation" class="btn-secondary hero-proof-cta">Voir un cas concret →</a>
    </div>'''.format(CAL=CALENDLY)

if OLD_HERO_ACTIONS in html:
    html = html.replace(OLD_HERO_ACTIONS, NEW_HERO_ACTIONS, 1)
    print('✓ Hero — CTA secondaire "Voir un cas concret" ajouté, WA supprimé')
else:
    # Fallback: just remove WA block and add secondary button
    html = re.sub(
        r'<div class="hero-wa-secondary">.*?</div>',
        '', html, count=1, flags=re.DOTALL
    )
    html = re.sub(
        r'(<div class="hero-actions">.*?btn-calendly[^<]*</a>)\s*</div>',
        r'\1\n      <a href="#transformation" class="btn-secondary hero-proof-cta">Voir un cas concret →</a>\n    </div>',
        html, count=1, flags=re.DOTALL
    )
    print('✓ Hero — CTA secondaire ajouté (fallback)')

# ══════════════════════════════════════════════════════════
# 4. SECTION REORDER — tarifs après leviers (avant process)
# ══════════════════════════════════════════════════════════
# Extract tarifs section
tarifs_m = re.search(r'\n*<section class="tarifs-launch"[^>]*>.*?</section>\n*', html, re.DOTALL)
if tarifs_m:
    tarifs_block = tarifs_m.group(0).strip()
    html = html.replace(tarifs_m.group(0), '\n\n', 1)
    # Insert before process section
    html = re.sub(
        r'(\n)(<section class="process")',
        '\n\n' + tarifs_block.replace('\\', '\\\\') + r'\n\n\2',
        html, count=1
    )
    print('✓ Tarifs déplacé : leviers → tarifs → process')
else:
    print('⚠ Section tarifs non trouvée')

# ══════════════════════════════════════════════════════════
# 5. PROBLEM SECTION — garder tel quel (déjà 3 blocs, 2 phrases)
# ══════════════════════════════════════════════════════════
print('— Problem section conservée (déjà conforme)')

# ══════════════════════════════════════════════════════════
# 6. FAQ — 6 nouvelles questions exactes
# ══════════════════════════════════════════════════════════
NEW_FAQ_LIST = '''      <div class="faq-list fade-in">

        <div class="faq-item">
          <div class="faq-question"><span>Comment se déroule concrètement votre intervention&nbsp;?</span><div class="faq-toggle"></div></div>
          <div class="faq-answer">Tout commence par un appel stratégique de 25 minutes. J'analyse votre situation, votre marché, votre potentiel réel. Si on travaille ensemble, je prends en charge l'optimisation complète : annonce, photos, pricing, algorithme. Vous n'avez rien à exécuter de votre côté. 60 jours de suivi inclus.</div>
        </div>

        <div class="faq-item">
          <div class="faq-question"><span>En combien de temps verrai-je des résultats&nbsp;?</span><div class="faq-toggle"></div></div>
          <div class="faq-answer">Les premiers effets sont visibles dès les premières semaines. Mes clients constatent en moyenne +90% de revenus sur les deux premiers mois. La majorité voit son taux d'occupation doubler avant J+30.</div>
        </div>

        <div class="faq-item">
          <div class="faq-question"><span>Et si ça ne fonctionne pas pour mon bien&nbsp;?</span><div class="faq-toggle"></div></div>
          <div class="faq-answer">Garantie 60 jours sans condition. Si vos revenus n'augmentent pas suffisamment pour couvrir la prestation, je continue à travailler avec vous gratuitement jusqu'à ce que ce soit le cas. Le risque est entièrement de mon côté.</div>
        </div>

        <div class="faq-item">
          <div class="faq-question"><span>Pourquoi pas une conciergerie classique&nbsp;?</span><div class="faq-toggle"></div></div>
          <div class="faq-answer">Une conciergerie prend 20 à 30% de vos revenus à vie et gère uniquement la logistique (entrées/sorties, ménage). Moi je m'occupe de l'optimisation commerciale de votre annonce — ce qui détermine si votre calendrier se remplit ou pas. Forfait unique, aucune commission, vous gardez 100% de vos revenus supplémentaires.</div>
        </div>

        <div class="faq-item">
          <div class="faq-question"><span>Mon annonce est déjà en ligne — ça change quelque chose&nbsp;?</span><div class="faq-toggle"></div></div>
          <div class="faq-answer">Aucune importance. J'interviens autant sur des annonces existantes qui peinent à décoller que sur des lancements. Dans les deux cas, l'audit révèle exactement ce qui freine votre potentiel.</div>
        </div>

        <div class="faq-item">
          <div class="faq-question"><span>Intervenez-vous dans toute la France&nbsp;?</span><div class="faq-toggle"></div></div>
          <div class="faq-answer">Oui — partout en France et également au Maroc. J'interviens à distance via WhatsApp et visio, donc votre localisation n'est pas un frein.</div>
        </div>

      </div>'''

# Replace the existing faq-list
html = re.sub(
    r'<div class="faq-list fade-in">.*?</div>\s*\n\s*</div>\s*\n\s*</div>\s*\n</section>',
    NEW_FAQ_LIST + '\n    </div>\n  </div>\n</section>',
    html, count=1, flags=re.DOTALL
)
print('✓ FAQ — 6 nouvelles questions appliquées')

# ══════════════════════════════════════════════════════════
# 7. CTA FINAL — aligner avec le hero (tunnel strict)
# ══════════════════════════════════════════════════════════
NEW_CTA_FINAL = '''<section class="cta-final" id="contact">
  <div class="cta-final-content">
    <div class="eyebrow center">Passez à l'action</div>
    <h2 class="cta-final-title">Votre annonce perd des<br><em>réservations</em> chaque jour</h2>
    <p class="cta-final-sub">Un appel de 25 minutes pour tout comprendre — sans engagement, sans déplacement. Jamil analyse votre situation et vous dit exactement ce qui freine vos revenus.</p>
    <div class="cta-final-actions">
      <a href="{CAL}" class="btn-primary btn-calendly" target="_blank" rel="noopener"><span>Réserver mon appel stratégique →</span></a>
    </div>
    <div class="cta-final-trust">
      <span>Appel 25 min — gratuit</span>
      <span>Résultats garantis 60 jours</span>
      <span>Sans engagement</span>
    </div>
  </div>
</section>'''.format(CAL=CALENDLY)

html = re.sub(
    r'<section class="cta-final"[^>]*>.*?</section>',
    NEW_CTA_FINAL,
    html, count=1, flags=re.DOTALL
)
print('✓ CTA final — tunnel strict, WhatsApp secondaire retiré')

# ══════════════════════════════════════════════════════════
# 8. LAZY LOADING sur toutes les images sauf la première
# ══════════════════════════════════════════════════════════
img_count = [0]
def add_lazy(m):
    img_count[0] += 1
    tag = m.group(0)
    if img_count[0] == 1:
        return tag  # première image (LCP) — pas de lazy
    if 'loading=' not in tag:
        tag = tag.replace('<img ', '<img loading="lazy" ')
    return tag

html = re.sub(r'<img [^>]+>', add_lazy, html)
print(f'✓ Lazy loading ajouté sur {img_count[0]-1} images (1 LCP préservée)')

# ══════════════════════════════════════════════════════════
# 9. VÉRIFICATIONS
# ══════════════════════════════════════════════════════════
print()
print('=== VÉRIFICATIONS ===')
# Section order
ba = html.find('class="before-after"')
pb = html.find('class="problem"')
lv = html.find('class="leviers"')
tr = html.find('class="tarifs-launch"')
pc = html.find('class="process"')
ab = html.find('class="about"')
fq = html.find('class="faq"')
cf = html.find('class="cta-final"')
order_ok = ba < pb < lv < tr < pc < ab < fq < cf
print(f'  [{"OK" if order_ok else "FAIL"}] Ordre sections : before-after→problem→leviers→tarifs→process→about→faq→cta')

checks = {
    'Diagnostic gratuit supprimé (meta/og)': 'Diagnostic gratuit' not in html[:2000],
    'calendly-float présent': 'class="calendly-float"' in html,
    'whatsapp-float absent': 'class="whatsapp-float"' not in html,
    'Voir un cas concret': 'Voir un cas concret' in html,
    'FAQ 6 questions': html.count('faq-item') == 6,
    'CTA final tunnel': 'Appel 25 min — gratuit' in html,
    'Lazy loading': 'loading="lazy"' in html,
}
for name, ok in checks.items():
    print(f'  [{"OK" if ok else "FAIL"}] {name}')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print()
print('✅ Tunnel complet — index.html sauvegardé.')
