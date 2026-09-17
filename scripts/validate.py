"""Check generated links and source associations. Standard library only."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import json, sys
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'
errors=[]
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.refs=[];self.ids=set();self.h1=0;self.imgs=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if tag=='h1':self.h1+=1
        if tag in ['a','link'] and a.get('href'):self.refs.append(a['href'])
        if tag in ['img','script'] and a.get('src'):self.refs.append(a['src'])
        if tag=='img' and not a.get('alt'):self.imgs.append(a.get('src'))
pages={}
for p in OUT.glob('*.html'):
    parser=Page();parser.feed(p.read_text(encoding='utf-8-sig'));pages[p.name]=parser
    if parser.h1!=1:errors.append(f'{p.name}: expected one h1')
    if parser.imgs:errors.append(f'{p.name}: missing image alternative text')
for name,p in pages.items():
    for ref in p.refs:
        u=urlparse(ref)
        if u.scheme or u.netloc:continue
        if u.path.startswith('/'):errors.append(f'{name}: root-absolute link breaks repository hosting: {ref}');continue
        target=(OUT/unquote(u.path)).resolve() if u.path else OUT/name
        if not target.is_relative_to(OUT.resolve()) or not target.is_file():errors.append(f'{name}: broken local link {ref}')
        elif u.fragment and target.suffix=='.html' and u.fragment not in pages[target.name].ids:errors.append(f'{name}: missing fragment {ref}')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
members=[read(p) for p in (ROOT/'content/people').glob('*.json')]
ids=[p['id'] for p in members]
if len(set(ids))!=len(ids):errors.append('Duplicate member id')
for n in [read(p) for p in (ROOT/'content/news').glob('*.json')]:
    for member in n.get('members',[]):
        if member not in ids:errors.append(f'Unknown news member: {member}')
    if not any(b['type'] in ['paragraph','list'] for sec in n['sections'] for b in sec):errors.append(f'News body missing: {n["id"]}')
    if n.get('end_date','9999')<n['date']:errors.append(f'Invalid news date range: {n["id"]}')
pubs=read(ROOT/'content/publications.json')
if len({p['id'] for p in pubs})!=len(pubs):errors.append('Duplicate publication id')
for p in pubs:
    for member in p.get('members',[]):
        if member not in ids:errors.append(f'Unknown publication member: {member}')
if errors:
    print('\n'.join(errors));sys.exit(1)
print(f'Validated {len(pages)} pages, {len(members)} members/alumni, {len(pubs)} publication records, all local links and member associations.')

