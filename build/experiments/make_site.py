# -*- coding: utf-8 -*-
"""Made the site folder from draft 2.9, once (11 November 2026):

    site/site.css        every style that was inside the page
    site/en/index.html   the English page: 2.9 without its styles and scripts
    site/index.html      the Portuguese page: the same page, translated

site/site.js was written by hand from the scripts in 2.9, with every word a
script writes in both languages. From here on the two pages and the two shared
files are edited directly: do not run this again, it would overwrite them.
For the record only, like the other scripts here."""
import io, os, re, sys, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = 'elite-wellness-landing_2-9.html'
SITE_URL = 'https://example.com/'   # [PLACEHOLDER: the real address once the page goes live]


def sub(s, old, new, n=1):
    assert s.count(old) == n, '%d x %r' % (s.count(old), old[:80])
    return s.replace(old, new)


def wa(msg):
    return 'https://wa.me/351926565836?text=' + urllib.parse.quote(msg, safe='!')


# ---------------------------------------------------------------- styles
def styles(s):
    head = s.split('<body>', 1)[0]
    blocks = re.findall(r'<style([^>]*)>(.*?)</style>', head, re.S)
    names = ['the page', 'prices', 'classes grid', 'polish', 'the full price list']
    assert len(blocks) == len(names), len(blocks)
    todo = re.search(r'\.pr-todo\{[^}]*\}', io.open(os.path.join(ROOT, 'pricing.css'), encoding='utf-8').read()).group(0)
    out = ['/*\n  ELITE WELLNESS: every style of the page. Both pages load this one file:\n'
           '  index.html (Portuguese) and en/index.html (English). A change here shows in both.\n'
           '  The design rules (colours, fonts, when volt is allowed, how buttons look) are in CLAUDE.md.\n*/\n']
    for (attrs, css), name in zip(blocks, names):
        css = css.strip('\n')
        while css.count('}') > css.count('{'):          # a stray closing brace would swallow the next rule
            i = css.rindex('}'); css = css[:i] + css[i + 1:]
        out.append('\n/* ==================== %s ==================== */\n%s\n' % (name, css.rstrip()))
        if name == 'the page':
            out.append('\n/* the small "todo" mark on a question that is still open */\n%s\n' % todo)
    out.append('\n/* the language button is a link to the other page */\n.lang-btn{text-decoration:none}\n')
    return ''.join(out)


# ---------------------------------------------------------------- the page without styles and scripts
def page(s, lang):
    base = '' if lang == 'pt' else '../'
    head, body = s.split('<body>', 1)
    head = re.sub(r'<style[^>]*>.*?</style>\n?', '', head, flags=re.S)
    head = sub(head, '<link rel="stylesheet" href="pricing.css">\n', '<link rel="stylesheet" href="%ssite.css">\n' % base)
    head = sub(head, '<link rel="alternate" hreflang="en" href="https://example.com/">\n<link rel="alternate" hreflang="pt-PT" href="https://example.com/pt">\n',
               '<link rel="canonical" href="%s">\n<link rel="alternate" hreflang="pt-PT" href="%s">\n<link rel="alternate" hreflang="en" href="%sen/">\n<link rel="alternate" hreflang="x-default" href="%s">\n'
               % (SITE_URL + ('' if lang == 'pt' else 'en/'), SITE_URL, SITE_URL, SITE_URL))
    head = sub(head, '"url":"https://example.com/",', '"url":"%s",' % (SITE_URL + ('' if lang == 'pt' else 'en/')))
    body = re.sub(r'\n*<script\b.*?</script>', '', body, flags=re.S)
    body = sub(body, '</body>', '\n<!-- the data (prices, timetable, reviews), then everything the page does -->\n'
               '<script src="%sprices.js"></script>\n<script src="%sschedule.js"></script>\n<script src="%sreviews.js"></script>\n<script src="%ssite.js"></script>\n</body>' % (base, base, base, base))
    s = head + '<body>' + body
    s = sub(s, '    <!-- on the live site this links to the Portuguese page (/pt); here it toggles to demo the interaction -->\n'
               '    <button class="lang-btn" type="button" id="lang-btn" aria-label="Mudar para português">PT</button>',
            '    <!-- the other language: the same page, the same section -->\n' +
            ('    <a class="lang-btn" id="lang-btn" href="en/" hreflang="en" lang="en" aria-label="Switch to English">EN</a>' if lang == 'pt' else
             '    <a class="lang-btn" id="lang-btn" href="../" hreflang="pt-PT" lang="pt" aria-label="Mudar para português">PT</a>'))
    if base:
        s = re.sub(r'(?<=["\'(])(?=assets/)', base, s)
        s = re.sub(r'(?<=[0-9][wx], )(?=assets/)', base, s)
    return s


# ---------------------------------------------------------------- Portuguese
Q = [   # question, answer (html)
    ('Can I train without a membership?', 'Posso treinar sem ser sócio?',
     '<p>Yes. A day pass is €12 and a week pass is €40.90, sports insurance included. Walk in and pay at reception.</p>',
     u'<p>Sim. Um passe diário custa 12 € e um passe semanal custa 40,90 €, com seguro desportivo incluído. Aparece e paga na receção.</p>'),
    ('Do I need to book?', 'É preciso marcar?',
     '<p>No. Just come by during opening hours.</p>', '<p>Não. Basta aparecer durante o horário de abertura.</p>'),
    ('Do you speak English?', 'Falam inglês?',
     '<p>Yes, English and Portuguese.</p>', '<p>Sim, português e inglês.</p>'),
    ('Are there showers and lockers?', 'Há duches e cacifos?',
     "<p>Yes. Showers and lockers in both changing rooms. The lockers need your own lock; if you don't have one, you can buy one at reception.</p>",
     '<p>Sim. Há duches e cacifos nos dois balneários. Os cacifos precisam de cadeado; se não tiveres um, podes comprar na receção.</p>'),
    ('Do you provide towels?', 'Dão toalhas?',
     '<p>No. Bring your own towel, water and trainers. If you forget your towel, you can buy one at reception.</p>',
     '<p>Não. Traz a tua toalha, água e ténis. Se te esqueceres da toalha, podes comprar uma na receção.</p>'),
    ('Is there air conditioning?', 'Há ar condicionado?',
     "<p>No. The full height glass doors open onto the outdoor deck, so the air moves. It's how the gym was designed.</p>",
     '<p>Não. As portas de vidro a toda a altura abrem para o deck exterior, por isso o ar circula. O ginásio foi pensado assim.</p>'),
    ('Do you have a squat rack?', 'Têm rack de agachamento?',
     '<p>Yes. Two squat racks, Smith machines and a full free weight setup.</p>',
     '<p>Sim. Dois racks de agachamento, máquinas Smith e uma zona completa de pesos livres.</p>'),
    ('Are you open on public holidays?', 'Abrem aos feriados?',
     "<p>No. We're closed on all Portuguese public holidays and on Lagos's municipal holiday (27 October).</p>",
     '<p>Não. Fechamos em todos os feriados nacionais e no feriado municipal de Lagos (27 de outubro).</p>'),
]

LEGEND = [
    ('Reception', 'Pay here, towels and locks', 'Receção', 'Pagamentos, toalhas e cadeados'),
    ('Changing rooms', 'Lockers and showers, plus a WC', 'Balneários', 'Cacifos e duches, e um WC'),
    ('Studio', 'Mats, stretching and classes', 'Estúdio', 'Colchões, alongamentos e aulas'),
    ('Free weights', 'Dumbbells and benches, in two spots', 'Pesos livres', 'Halteres e bancos, em dois sítios'),
    ('Machines', 'Resistance machines, a leg press and two cable stations', 'Máquinas', 'Máquinas de musculação, uma prensa de pernas e duas estações de cabos'),
    ('Lifting racks', 'A squat stand, a landmine and a pull up rig', 'Racks', 'Um suporte de agachamento, um landmine e uma estrutura de elevações'),
    ('Bikes', 'Indoor bikes for cycling and cardio', 'Bicicletas', 'Bicicletas indoor para cycling e cardio'),
    ('Cardio', 'Treadmills, a stair climber and a rower', 'Cardio', 'Passadeiras, um simulador de escadas e um remo'),
    ('Outdoor deck', 'Open air training and classes', 'Deck exterior', 'Treino e aulas ao ar livre'),
]

CARDS = [
    ('A coach pushing a weighted sled across the turf at Elite Wellness', 'Um treinador a empurrar um trenó com carga na relva sintética do Elite Wellness', 'Hybrid training', 'Aula híbrida'),
    ('A member pulling up on the TRX straps anchored to the wall at Elite Wellness', 'Um sócio a puxar nas fitas de TRX presas à parede, no Elite Wellness', 'Suspension training', 'Treino em suspensão'),
    ('Members doing an ab exercise on mats in a GAP class at Elite Wellness', 'Sócios a fazer um exercício de abdominais nos colchões, numa aula de GAP no Elite Wellness', 'Glutes, abs and legs', 'Glúteos, abdominais e pernas'),
    ('Members pedalling on the spin bikes in a Bike Elite class at Elite Wellness', 'Sócios a pedalar nas bicicletas, numa aula de Bike Elite no Elite Wellness', 'Indoor cycling', 'Ciclismo indoor'),
    ('An instructor and members balancing on one leg on their mats in a class at Elite Wellness', 'Uma instrutora e os sócios em equilíbrio numa perna, nos colchões, numa aula no Elite Wellness', 'Mat pilates', 'Pilates de solo'),
]


def portuguese(s):
    T = lambda old, new, n=1: sub(T.s, old, new, n)
    def t(old, new, n=1): T.s = sub(T.s, old, new, n)
    T.s = s
    # head
    t('<html lang="en">', '<html lang="pt-PT">')
    t('<title>Gym in Lagos, Algarve | Elite Wellness by Santos | Day passes and membership</title>',
      '<title>Ginásio em Lagos, Algarve | Elite Wellness by Santos | Passes diários e adesão</title>')
    t('content="Family run gym in Lagos, Portugal. Weights, machines, classes and an outdoor training deck. Day pass €12, week pass €40.90, membership from €13 every 2 weeks with direct debit. Open Mon to Fri 7:00 to 21:00, Sat 9:00 to 13:00."',
      u'content="Ginásio de família em Lagos, no Algarve. Pesos, máquinas, aulas e um deck exterior para treinar ao ar livre. Passe diário 12 €, passe semanal 40,90 €, adesão desde 13 € a cada 2 semanas por débito direto. Aberto de segunda a sexta das 7:00 às 21:00 e ao sábado das 9:00 às 13:00."')
    # header and menu
    t('<a class="nav-link" href="#classes">Classes</a>', '<a class="nav-link" href="#classes">Aulas</a>')
    t('<a class="nav-link" href="#prices">Prices</a>', '<a class="nav-link" href="#prices">Preços</a>')
    t('<a class="nav-link" href="#find-us">Location</a>', '<a class="nav-link" href="#find-us">Localização</a>')
    t('<a class="nav-cta" href="#prices">Join</a>', '<a class="nav-cta" href="#prices">Inscreve-te</a>')
    t('aria-label="Open menu"', 'aria-label="Abrir menu"')
    t('<span class="ml">Classes</span><span class="ms">What we run, and when</span>', '<span class="ml">Aulas</span><span class="ms">O que há e quando</span>')
    t('<span class="ml">Prices</span><span class="ms">Day pass €12 · Membership from €13</span>', u'<span class="ml">Preços</span><span class="ms">Passe diário 12 € · Adesão desde 13 €</span>')
    t('<span class="ml">Hours &amp; location</span>', '<span class="ml">Horário e localização</span>')
    t('<span class="ml">Reviews</span><span class="ms">4.8 from 153 on Google</span>', '<span class="ml">Avaliações</span><span class="ms">4,8 em 153 avaliações no Google</span>')
    t('<span class="ml">Good to know</span><span class="ms">Showers, towels, payment</span>', '<span class="ml">Bom saber</span><span class="ms">Duches, toalhas, pagamento</span>')
    t(wa('Hi! I have a question about the gym.'), wa('Olá! Tenho uma pergunta sobre o ginásio.'), 2)
    t('>WhatsApp us</a>', '>WhatsApp</a>')
    t('>Directions</a>', '>Como chegar</a>', 2)
    # hero
    t('aria-label="4.8 out of 5 from 153 Google reviews, opens Google Maps in a new tab"', 'aria-label="4,8 em 5, de 153 avaliações no Google; abre o Google Maps num novo separador"')
    t('4.8 · 153 Google reviews', '4,8 · 153 avaliações no Google', 2)
    t('<h1 class="hero-title">Train<br>In Lagos</h1>', '<h1 class="hero-title">Treina<br>em Lagos</h1>')
    t('A family run gym in Lagos. Weights, machines, classes and space to train outdoors.', 'Um ginásio de família em Lagos. Pesos, máquinas, aulas e espaço para treinar ao ar livre.')
    t('alt="The free weights at Elite Wellness: a rack of hex dumbbells on the gym floor"', 'alt="Os pesos livres do Elite Wellness: uma fila de halteres hexagonais na sala"')
    t('alt="A member holding a loaded barbell at the top of a deadlift at Elite Wellness"', 'alt="Um sócio a segurar uma barra carregada no topo de um peso morto, no Elite Wellness"')
    t('alt="Members reaching into a side stretch in a class in the studio at Elite Wellness"', 'alt="Sócios num alongamento lateral, numa aula no estúdio do Elite Wellness"')
    t('aria-label="Equipment"', 'aria-label="Equipamento"')
    t('Free weights &nbsp;//&nbsp; Resistance machines &nbsp;//&nbsp; Treadmills &nbsp;//&nbsp; Indoor bikes &nbsp;//&nbsp; Functional area &nbsp;//&nbsp; Outdoor training deck &nbsp;//&nbsp; Group classes &nbsp;//&nbsp;',
      'Pesos livres &nbsp;//&nbsp; Máquinas de musculação &nbsp;//&nbsp; Passadeiras &nbsp;//&nbsp; Bicicletas indoor &nbsp;//&nbsp; Zona funcional &nbsp;//&nbsp; Deck exterior &nbsp;//&nbsp; Aulas de grupo &nbsp;//&nbsp;', 2)
    # the gym
    t('<h2 class="section-header">The gym</h2>', '<h2 class="section-header">O ginásio</h2>')
    t('<span class="section-script">have a look around</span>', '<span class="section-script">dá uma vista de olhos</span>')
    t('<h3>Inside</h3>', '<h3>Interior</h3>')
    t('Free weights, resistance machines and cardio, including treadmills and indoor bikes, plus a studio for classes. Full height glass doors keep it bright and the air moving.',
      'Pesos livres, máquinas de musculação e cardio, com passadeiras e bicicletas indoor, e um estúdio para as aulas. As portas de vidro a toda a altura deixam entrar a luz e o ar.')
    t('<h3>Outside</h3>', '<h3>Exterior</h3>')
    t("An outdoor deck right outside the doors. When the weather's good, classes often move out there. That's how this gym started, and we never stopped.",
      'Um deck exterior mesmo à saída das portas. Com bom tempo, as aulas passam muitas vezes lá para fora. Foi assim que o ginásio começou, e nunca parámos.')
    t('aria-label="Floor plan of Elite Wellness: reception, changing rooms, class studio, free weights, machines, lifting racks, bikes, cardio and the outdoor area next to the park"',
      'aria-label="Planta do Elite Wellness: receção, balneários, estúdio de aulas, pesos livres, máquinas, racks, bicicletas, cardio e o deck exterior junto ao parque"')
    t('>entrance</text>', '>entrada</text>'); t('>park</text>', '>parque</text>')
    t('&larr; Swipe to look around &rarr;', '&larr; Desliza para ver &rarr;')
    t('<div class="pi-t">What\'s where</div><div class="pi-s">Tap any area on the plan</div>', '<div class="pi-t">O que há onde</div><div class="pi-s">Toca numa zona da planta</div>')
    t('aria-label="Previous area"', 'aria-label="Zona anterior"'); t('aria-label="Next area"', 'aria-label="Zona seguinte"')
    t('aria-label="What\'s where"', 'aria-label="O que há onde"')
    for i, (a, b, c, d) in enumerate(LEGEND):
        t('<span class="gl-t">%s</span><span class="gl-s">%s</span>' % (a, b), '<span class="gl-t">%s</span><span class="gl-s">%s</span>' % (c, d))
        lab = 'Outdoor area' if a == 'Outdoor deck' else a
        t('aria-label="%02d %s"' % (i + 1, lab), 'aria-label="%02d %s"' % (i + 1, c), 2 if a == 'Changing rooms' else 1)
    # classes
    t('<h2 class="section-header">Classes</h2>', '<h2 class="section-header">Aulas</h2>')
    t('<span class="section-script">included in the price</span>', '<span class="section-script">incluídas no preço</span>')
    for a, b, c, d in CARDS:
        t('alt="%s"' % a, 'alt="%s"' % b)
        t('<div class="class-tag">%s</div>' % c, '<div class="class-tag">%s</div>' % d)
    t('aria-label="Choose a class"', 'aria-label="Escolhe uma aula"')
    t('<h3 class="tt-title">This week</h3>', '<h3 class="tt-title">Esta semana</h3>')
    t('aria-label="Weekly class timetable"', 'aria-label="Horário semanal das aulas"')
    t('aria-label="Choose a day"', 'aria-label="Escolhe um dia"')
    t('>See the class timetable</a>', '>Ver o horário das aulas</a>')
    # prices
    t('<h2 class="section-header">Prices</h2>', '<h2 class="section-header">Preços</h2>')
    t('<span class="section-script">a few taps, one price</span>', '<span class="section-script">uns toques, um preço</span>')
    t('aria-label="Your plan"', 'aria-label="O teu plano"')
    # reviews and about
    t('<h2 class="section-header">Reviews</h2>', '<h2 class="section-header">Avaliações</h2>')
    t('aria-label="Google reviews"', 'aria-label="Avaliações no Google"')
    t('>Read our reviews on Google</a>', '>Lê as nossas avaliações no Google</a>')
    t('<span class="section-script">since 2020</span>', '<span class="section-script">desde 2020</span>')
    t('Elite Wellness is run by the Santos family: André, Joana and Ricardo, all qualified in physical education, and their father Jorge. It began as outdoor sessions on the Marina de Lagos during lockdown. The gym came later; the outdoor training never left.',
      'O Elite Wellness é gerido pela família Santos: o André, a Joana e o Ricardo, todos formados em Educação Física, e o pai, o Jorge. Começou com treinos ao ar livre na Marina de Lagos, durante o confinamento. O ginásio veio depois; o treino ao ar livre ficou.')
    t('aria-label="The Santos family"', 'aria-label="A família Santos"')
    # hours and location
    t('<h2 class="section-header">Hours &amp; location</h2>', '<h2 class="section-header">Horário e localização</h2>')
    t('<p class="find-label">Opening hours</p>', '<p class="find-label">Horário</p>')
    t('<span class="hr-d">Monday to Friday</span><span class="hr-t">07:00 to 21:00</span>', '<span class="hr-d">Segunda a sexta</span><span class="hr-t">07:00 às 21:00</span>')
    t('<span class="hr-d">Saturday</span><span class="hr-t">09:00 to 13:00</span>', '<span class="hr-d">Sábado</span><span class="hr-t">09:00 às 13:00</span>')
    t('<span class="hr-d">Sunday</span><span class="hr-t off">Closed</span>', '<span class="hr-d">Domingo</span><span class="hr-t off">Fechado</span>')
    t('<span class="hr-d">Public holidays</span><span class="hr-t off">Closed</span>', '<span class="hr-d">Feriados</span><span class="hr-t off">Fechado</span>')
    t('title="Map of Elite Wellness by Santos, Lagos"', 'title="Mapa do Elite Wellness by Santos, Lagos"')
    t('<p class="find-label">Where to find us</p>', '<p class="find-label">Onde estamos</p>')
    t('<p class="find-note">Free parking outside.</p>', '<p class="find-note">Estacionamento gratuito à porta.</p>')
    t('>Get directions</a>', '>Como chegar</a>')
    # good to know
    t('<h2 class="section-header">Good to know</h2>', '<h2 class="section-header">Bom saber</h2>')
    for qe, qp, ae, ap in Q:
        t('<summary>%s</summary>\n      %s' % (qe, ae), '<summary>%s</summary>\n      %s' % (qp, ap))
    t('<summary>Is there a minimum commitment?</summary>', '<summary>Há fidelização?</summary>')
    t('Not for day or week passes. Membership is paid every 2 weeks, from €13 with direct debit, plus the €24 sports insurance once a year.',
      u'Nos passes diários e semanais, não. A adesão paga-se a cada 2 semanas, desde 13 € por débito direto, mais o seguro desportivo de 24 € uma vez por ano.')
    t(wa("Hi! I'd like to ask about membership.").replace('%27', '%27'), wa('Olá! Gostava de saber mais sobre a adesão.'))
    t('>Ask us on WhatsApp</a>', '>Pergunta-nos no WhatsApp</a>')
    t('<summary>Do you do personal training?</summary>', '<summary>Fazem treino personalizado?</summary>')
    t('<p>Yes, one to one with a qualified coach. The price is agreed with your coach. <a href="%s" target="_blank" rel="noopener">Book a time on WhatsApp</a>.</p>' % wa('Hi! I would like to book a time to talk to a coach about personal training.'),
      '<p>Sim, individual, com um treinador qualificado. O preço é combinado com o teu treinador. <a href="%s" target="_blank" rel="noopener">Marca pelo WhatsApp</a>.</p>' % wa('Olá! Gostava de marcar uma conversa com um treinador sobre treino personalizado.'))
    # footer and the bar
    t('We speak Portuguese and English', 'Falamos português e inglês')
    t('<p class="ft-h">Explore</p>', '<p class="ft-h">Explorar</p>')
    t('<li><a href="#gym">The gym</a></li>', '<li><a href="#gym">O ginásio</a></li>')
    t('<li><a href="#classes">Classes</a></li>', '<li><a href="#classes">Aulas</a></li>')
    t('<li><a href="#prices">Prices</a></li>', '<li><a href="#prices">Preços</a></li>')
    t('<li><a href="#reviews">Reviews</a></li>', '<li><a href="#reviews">Avaliações</a></li>')
    t('<li><a href="#find-us">Hours and location</a></li>', '<li><a href="#find-us">Horário e localização</a></li>')
    t('<li><a href="#faq">Good to know</a></li>', '<li><a href="#faq">Bom saber</a></li>')
    t('<p class="ft-h">Social and press</p>', '<p class="ft-h">Redes e imprensa</p>')
    t('As featured in NiT</a>', 'Na NiT</a>')
    t('<li><a href="#faq">Terms of entry</a></li>', '<li><a href="#faq">Condições de entrada</a></li>')
    t('<span class="ft-soon">Privacy policy<sup', '<span class="ft-soon">Política de privacidade<sup')
    t('· Family run since 2020</span>', '· Gerido em família desde 2020</span>')
    t('id="bp-go">Get this</button>', 'id="bp-go">Quero este</button>')
    return T.s


if __name__ == '__main__':
    if os.path.exists(os.path.join(ROOT, 'site', 'index.html')) and '--again' not in sys.argv:
        sys.exit('site/index.html exists. The pages are edited by hand now; this script would overwrite them.')
    s = io.open(os.path.join(ROOT, SRC), encoding='utf-8').read()
    w = lambda f, t: io.open(os.path.join(ROOT, 'site', f), 'w', encoding='utf-8').write(t)
    w('site.css', styles(s))
    w('en/index.html', page(s, 'en'))
    w('index.html', portuguese(page(s, 'pt')))
    print('site/site.css, site/en/index.html, site/index.html')
