"""Build the lab website. Python 3.10+, standard library only."""
from pathlib import Path
from html import escape
import json, re, shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'
OUT.mkdir(exist_ok=True)
generated=set()
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def e(s): return escape(str(s),quote=True)
def plain(s): return re.sub('<[^>]+>','',s).strip()
people=sorted([load(p.relative_to(ROOT)) for p in (ROOT/'content/people').glob('*.json')],key=lambda p:p.get('order',0))
news=sorted([load(p.relative_to(ROOT)) for p in (ROOT/'content/news').glob('*.json')],key=lambda n:n['date'],reverse=True)
pages={p.stem:load(p.relative_to(ROOT)) for p in (ROOT/'content/pages').glob('*.json')}
publications=load('content/publications.json')
# The canonical list drives the publication page and member associations.
publication_sections=[[{'type':'heading','level':1,'text':'Publications'}],
    [{'type':'heading','level':2,'text':'Papers in progress'},
     {'type':'paragraph','html':'<a href="work-in-progress.html">Preprints and ongoing research ↗</a>'}]]
for section in dict.fromkeys(p['section'] for p in publications):
    bb=[{'type':'heading','level':2,'text':section}]
    for category in dict.fromkeys(p['category'] for p in publications if p['section']==section):
        if category: bb.append({'type':'heading','level':3,'text':category})
        bb.append({'type':'list','ordered':False,'items':[p['html'] for p in publications if p['section']==section and p['category']==category]})
    publication_sections.append(bb)
pages['publications']['sections']=publication_sections
nav=[('index','Home'),('research','Research'),('people','People'),('publications','Publications'),('projects','Projects'),('news','News')]
def route_person(p): return 'jeonggyu-huh.html' if p['id']=='jeonggyu-huh' else 'person-'+p['id']+'.html'
def analytics_tag():
    measurement_id=load('content/site.json').get('google_analytics_measurement_id','')
    if not measurement_id: return ''
    if not re.fullmatch(r'G-[A-Z0-9]+',measurement_id):
        raise ValueError('Invalid Google Analytics measurement ID')
    return f"""<script>
(function () {{
  // Count visits to the published site only, excluding local previews.
  if (window.location.hostname !== 'huhjeonggyu.github.io') return;
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () {{ window.dataLayer.push(arguments); }};
  gtag('js', new Date());
  gtag('config', '{measurement_id}');
  var tag = document.createElement('script');
  tag.async = true;
  tag.src = 'https://www.googletagmanager.com/gtag/js?id={measurement_id}';
  document.head.appendChild(tag);
}})();
</script>"""

def shell(slug,title,body,active=None):
    links=''.join(f'<a href="{key}.html" '+('aria-current="page"' if (active or slug)==key else '')+f'>{label}</a>' for key,label in nav)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">{analytics_tag()}<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} · SKKU MLFE Lab</title><meta name="description" content="Machine Learning & Financial Engineering at Sungkyunkwan University. Research, people, publications and news from the MLFE Lab.">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg"><link rel="stylesheet" href="assets/style.css">
<script src="assets/site.js" defer></script></head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="container header-inner"><a class="brand" href="index.html" aria-label="SKKU MLFE Lab home"><span class="brand-mark">M<span>↗</span></span><span><strong>MLFE<span class="brand-lab"> LAB</span></strong><small>SUNGKYUNKWAN UNIVERSITY</small></span></a>
<button class="menu-toggle" aria-controls="main-nav" aria-expanded="false">Menu <span aria-hidden="true">☰</span></button>
<nav id="main-nav" aria-label="Main navigation">{links}</nav></div></header>
<main id="main">{body}</main>
<footer><div class="container footer-inner"><div><a class="footer-brand" href="index.html">SKKU MLFE Lab</a><p>Machine Learning &amp; Financial Engineering Lab</p></div></div></footer>
</body></html>'''
def write(slug,title,body,active=None):
    generated.add(slug+'.html')
    (OUT/(slug+'.html')).write_text(shell(slug,title,body,active),encoding='utf-8')
def image(src,alt,cls='',loading='lazy'):
    return f'<img src="{e(src)}" alt="{e(alt)}" class="{cls}" loading="{loading}" decoding="async">'
def render_block(b,context=''):
    t=b['type']
    if t=='heading':
        level=max(2,min(4,b.get('level',2)))
        return f'<h{level}>{e(b["text"])}</h{level}>'
    if t=='paragraph': return '<p>'+b['html']+'</p>'
    if t=='list':
        tag='ol' if b.get('ordered') else 'ul'
        return '<'+tag+'>'+''.join('<li>'+s+'</li>' for s in b['items'])+'</'+tag+'>'
    if t=='image': return '<figure><a href="'+e(b['src'])+'" aria-label="Open full-size image">'+image(b['src'],b.get('alt') or context)+'</a></figure>'
    if t=='embed': return '<p><a href="'+e(b['src'])+'">'+e(b.get('title','View embedded material'))+' ↗</a></p>'
    return ''
def render_sections(sections,context='',skip_title=True):
    out=[]
    for i,bb in enumerate(sections):
        if skip_title and i==0 and all(b['type']=='heading' for b in bb): continue
        out.append('<section class="prose-section">'+''.join(render_block(b,context) for b in bb)+'</section>')
    return ''.join(out)
def page_top(kicker,title,subtitle='',crumb=''):
    return f'<div class="page-top container">{crumb}<p class="eyebrow">{e(kicker)}</p><h1>{e(title)}</h1>'+ (f'<p class="page-subtitle">{e(subtitle)}</p>' if subtitle else '')+'</div>'
def display_date(n):
    start=n['date'].replace('-','.')
    return start+' – '+n['end_date'].replace('-','.') if n.get('end_date') else start
def news_card(n):
    pic=next((b['src'] for sec in n['sections'] for b in sec if b['type']=='image'),'')
    visual=image(pic,n['title']) if pic else '<div class="news-type">AQFC<span>2026</span></div>'
    return f'<article class="news-card"><a class="news-photo" href="news-{n["id"]}.html">{visual}</a><div class="news-meta"><time datetime="{n["date"]}">{display_date(n)}</time><span>{e(n["category"])}</span></div><h3><a href="news-{n["id"]}.html">{e(n["title"])}</a></h3><p>{e(n.get("subtitle",""))}</p></article>'
def home():
    site=load('content/site.json')
    intro=[site['introduction_en'],site['introduction_ko']]
    intro=[re.sub(r'^[😀😆]\s*','',s) for s in intro]
    body=f'''<section class="hero"><div class="container"><p class="eyebrow"><span class="tiny-line"></span> SKKU · DEPARTMENT OF MATHEMATICS</p><h1>Machine learning.<br><span>Financial engineering.</span></h1><div class="hero-bottom"><p>Machine Learning &amp; Financial Engineering Lab</p><a class="text-link" href="research.html">Explore our research <span>↗</span></a></div></div></section>
<section class="container intro-section"><div><p class="eyebrow">OUR RESEARCH</p><h2>Mathematical structure.<br>Real-world decisions.</h2></div><div class="intro-copy"><p>{intro[0]}</p><p lang="ko" class="muted">{intro[1]}</p></div></section>
<section class="container research-themes"><a href="research.html" class="theme"><span class="section-number">01</span><div><h3>Structure-preserving learning & control</h3><p>High-dimensional financial decision problems</p></div><span class="arrow">↗</span></a><a href="publications.html" class="theme"><span class="section-number">02</span><div><h3>Decision-focused asset pricing</h3><p>Financial machine learning</p></div><span class="arrow">↗</span></a></section>
<section class="news-section"><div class="container"><div class="section-title"><div><p class="eyebrow">FROM THE LAB</p><h2>Latest news</h2></div><a class="text-link" href="news.html">All news ↗</a></div><div class="news-grid">{''.join(news_card(n) for n in news[:3])}</div></div></section>
<section class="container people-callout"><div><p class="eyebrow">OUR PEOPLE</p><h2>Meet the MLFE Lab.</h2><p>Researchers in financial mathematics and machine learning.</p></div><a class="button" href="people.html">Meet our team ↗</a></section>'''
    write('index','Home',body)
def person_card(p):
    pic=image(p['image'],p['name']) if p['image'] else '<div class="portrait-initial">'+e(''.join(w[0] for w in p['name'].split()[:2]))+'</div>'
    return f'<article class="person-card"><a class="portrait" href="{route_person(p)}">{pic}</a><div class="person-summary"><h3><a href="{route_person(p)}">{e(p["name"])}</a></h3><p class="person-program">{e(p["program"])}</p>'+(''.join('<span class="role">'+e(r)+'</span>' for r in p['roles']))+'</div></article>'
def build_people():
    body=page_top('THE LAB','People','The people behind our research.')
    body+='<div class="container"><nav class="section-nav" aria-label="People sections"><a href="#faculty">Faculty & postdoc</a><a href="#graduate">Graduate students</a><a href="#undergraduate">Undergraduates</a><a href="#alumni">Alumni</a></nav>'
    for group,label,anchor in [('Principal Investigator','Principal investigator','faculty'),('Postdoctoral Researcher','Postdoctoral researcher','postdoc'),('Graduate Students','Graduate students','graduate'),('Undergraduate Students','Undergraduate students','undergraduate')]:
        pp=[p for p in people if p['group']==group]
        grid_class="people-grid" if group=="Principal Investigator" else "people-grid people-grid-compact"
        body+=f'<section class="people-section" id="{anchor}"><div class="section-title"><h2>{label}</h2><span class="count">{len(pp):02d}</span></div><div class="{grid_class}">'+''.join(person_card(p) for p in pp)+'</div></section>'
    body+='<section class="people-section" id="alumni"><div class="section-title"><h2>Alumni</h2></div><div class="alumni-list">'
    for p in people:
        if p['group']=='Alumni': body+=f'<div class="alumni-row"><h3 lang="ko">{e(p["name"])}</h3><span>{e(p["program"])}</span><time>{p.get("graduated","")}</time><span>{e(p.get("placement",""))}</span></div>'
    body+='</div></section><div class="contact-strip"><h2>Interested in joining us?</h2><a class="text-link" href="contact.html">Contact & research careers ↗</a></div></div>'
    write('people','People',body)
def build_profiles():
    for p in people:
        if p['group']=='Alumni': continue
        name=p['name']; slug='jeonggyu-huh' if p['id']=='jeonggyu-huh' else 'person-'+p['id']
        pic=image(p['image'],name,loading='eager') if p['image'] else '<div class="portrait-initial">'+e(''.join(w[0] for w in name.split()[:2]))+'</div>'
        profile_class="profile profile-pi" if p["id"]=="jeonggyu-huh" else "profile profile-member"
        identity=f'<p class="eyebrow">{e(p["group"])}</p><h1>{e(name)}</h1><p>{e(p["program"])}</p>'+''.join('<p class="role">'+e(r)+'</p>' for r in p['roles'])
        portrait=f'<div class="profile-photo">{pic}</div>'
        profile_header='<div class="profile-header">'+portrait+'<div class="profile-identity">'+identity+'</div></div>' if p['id']=='jeonggyu-huh' else portrait+identity
        body=f'<div class="container {profile_class}"><aside class="profile-aside">'+profile_header
        if p['id']=='jeonggyu-huh': body+='<p>Department of Mathematics<br>Sungkyunkwan University</p><p>Natural Science Building 1, #31313</p><a href="mailto:jghuh@skku.edu">jghuh@skku.edu</a><nav class="profile-links" aria-label="Principal investigator"><a href="talks.html">Talks ↗</a><a href="teaching.html">Teaching ↗</a><a href="publications.html">Publications ↗</a></nav>'
        body+='</aside><div class="prose profile-detail">'
        sections=pages['jeonggyu-huh']['sections'][1:] if p['id']=='jeonggyu-huh' else p['sections']
        body+=render_sections(sections,name,False)
        existing=str(p['sections'])
        related_papers=[paper for paper in publications if p['id'] in paper.get('members',[]) and plain(paper['html']).split(',')[0] not in existing]
        if related_papers and p['id']!='jeonggyu-huh':
            body+='<section class="prose-section"><h2>Publications & manuscripts</h2><ul>'+''.join('<li>'+paper['html']+'</li>' for paper in related_papers)+'</ul></section>'
        related=[n for n in news if p['id'] in n.get('members',[])]
        if related: body+='<section class="related-news"><h2>Lab news</h2>'+''.join(f'<a href="news-{n["id"]}.html"><time>{n["date"]}</time><span>{e(n["title"])}</span>↗</a>' for n in related)+'</section>'
        body+='</div></div>'
        write(slug,name,body,'people')
def build_articles():
    groups={'research':'research','bptt-costate':'research','publications':'publications','work-in-progress':'publications','talks':'people','teaching':'people','projects':'projects'}
    for slug,active in groups.items():
        p=pages[slug]
        relations={'research':[('research','Overview'),('bptt-costate','Why BPTT ≈ Costate?')],'publications':[('publications','Publications'),('work-in-progress','Work in progress')],'people':[('jeonggyu-huh','Principal investigator'),('talks','Talks'),('teaching','Teaching')]}
        subnav='<nav class="section-nav" aria-label="Related pages">'+''.join(f'<a href="{s}.html" '+('aria-current="page"' if s==slug else '')+f'>{t}</a>' for s,t in relations.get(active,[]))+'</nav>' if relations.get(active) else ''
        headings=[b['text'] for i,sec in enumerate(p['sections']) for b in sec if b['type']=='heading' and not (i==0 and all(x['type']=='heading' for x in sec))]
        body=page_top('MLFE LAB',p['title'])
        body+='<div class="container">'+subnav+'<div class="article-layout"><aside class="article-index"><p class="eyebrow">ON THIS PAGE</p>'
        if headings:
            body+=''.join(f'<a href="#section-{i}">{e(h)}</a>' for i,h in enumerate(headings))
        else: body+='<a href="#article">Research notes</a>'
        body+='</aside><article id="article" class="prose '+('note-images' if slug=='bptt-costate' else '')+'">'
        content=render_sections(p['sections'],p['title'])
        count=0
        def heading_id(m):
            nonlocal count
            ans='<'+m.group(1)+' id="section-'+str(count)+'">'+m.group(2)+'</'+m.group(1)+'>'
            count+=1
            return ans
        content=re.sub(r'<(h[234])>(.*?)</\1>',heading_id,content,flags=re.S)
        body+=content+'</article></div></div>'
        write(slug,p['title'],body,active)
def build_news():
    body=page_top('FROM THE LAB','News','Conferences, research, and life in the lab.')
    body+='<div class="container news-archive"><div class="news-grid">'+''.join(news_card(n) for n in news)+'</div></div>'
    write('news','News',body)
    for n in news:
        body=page_top(n['category'],n['title'],n.get('subtitle',''))
        body+='<article class="container prose news-detail"><time class="article-date" datetime="'+n['date']+'">'+display_date(n)+'</time>'+render_sections(n['sections'],n['title'],False)
        members=[p for p in people if p['id'] in n.get('members',[])]
        if members: body+='<div class="related-people"><h2>People</h2>'+''.join('<a href="'+route_person(p)+'">'+e(p['name'])+' ↗</a>' for p in members)+'</div>'
        body+='</article>'
        write('news-'+n['id'],n['title'],body,'news')
def build_contact():
    body=page_top('GET IN TOUCH','Contact','We welcome inquiries from prospective students.')
    body+='<div class="container contact-layout"><div class="contact-box"><h2>Jeonggyu Huh</h2><p>Associate Professor<br>Department of Mathematics<br>Sungkyunkwan University</p><a href="mailto:jghuh@skku.edu">jghuh@skku.edu ↗</a><p>Natural Science Building 1, #31313</p></div><div class="prose">'+render_sections(load('content/contact.json')['sections'])+'</div></div>'
    write('contact','Contact',body)
home()
build_people()
build_profiles()
build_articles()
build_news()
build_contact()
write('404','Page not found',page_top('404','Page not found','The page you are looking for could not be found.')+'<div class="container not-found"><a class="button" href="index.html">Back to home</a></div>')
shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
(OUT/'.nojekyll').touch()
# Only retire pages previously recorded as generated, never arbitrary user files.
manifest=OUT/'.generated-pages.json'
previous=json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else []
for name in set(previous)-generated:
    if re.fullmatch(r'[a-z0-9-]+\.html',name):
        target=(OUT/name).resolve()
        if target.parent==OUT.resolve() and target.exists(): target.unlink()
manifest.write_text(json.dumps(sorted(generated)),encoding='utf-8')
print(f'Built {len(list(OUT.glob("*.html")))} pages in docs/')

