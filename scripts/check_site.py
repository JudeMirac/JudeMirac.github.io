"""Check internal portfolio links, source totals, and publication state."""
import csv
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT=Path(__file__).resolve().parents[1]
errors=[]
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.ids=set();self.titles=0;self.h1s=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids: errors.append('Duplicate HTML id '+a['id'])
            self.ids.add(a['id'])
        if tag=='h1': self.h1s+=1
        if tag=='title': self.titles+=1
        if tag in ['a','link','script','img','iframe']:
            ref=a.get('href') or a.get('src')
            if ref:self.links.append(ref)
        if tag=='img' and 'alt' not in a:errors.append('Image missing alt')
        if tag=='iframe' and not a.get('title'):errors.append('Iframe missing title')

pages={}
for f in ROOT.rglob('*.html'):
    p=Page();p.feed(f.read_text());pages[f.resolve()]=p
    assert p.h1s==1 and p.titles==1,f'Heading/title issue: {f}'
for f,p in pages.items():
    for ref in p.links:
        url=urlsplit(ref)
        if url.scheme or url.netloc:continue
        target=(f.parent/unquote(url.path)).resolve() if url.path else f
        if target.is_dir():target=target/'index.html'
        if not target.exists():errors.append(f'{f.name}: missing {ref}')
        elif url.fragment and target in pages and url.fragment not in pages[target].ids:
            errors.append(f'{f.name}: missing fragment {ref}')

data=json.loads((ROOT/'data/transportation-summary.json').read_text())
with (ROOT/'tableau/transportation-trips.csv').open() as f:rows=list(csv.DictReader(f))
assert len(rows)==650
assert sum(int(r['valid_pickup']) for r in rows)==556
assert sum(int(r['on_time_flag']) for r in rows if r['on_time_flag'])==319
assert sum(int(r['late_flag']) for r in rows if r['late_flag'])==155
assert sum(int(r['cancelled_flag']) for r in rows)==51
assert all('first_name' not in r and 'license_number' not in r for r in rows)
assert data['summary']['valid_pickups']==556
assert round(data['summary']['otp'],1)==57.4
assert [c['risk'] for c in data['contractors'] if c['id']==8]==['No valid trips']
for f in pages:
    text=f.read_text()
    for token in ['57.4','155','7.8','556']:
        assert token in text,f'{f.name}: missing verified metric {token}'
assert not errors,errors
print(f'PASS: {len(pages)} HTML pages, all local links and fragments, data reconciliation, no driver PII in exports.')
print('Tableau state:', 'pending URL' if 'url: ""' in (ROOT/'assets/tableau-config.js').read_text() else 'URL configured; live verification required')
