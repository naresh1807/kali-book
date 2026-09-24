from pathlib import Path
import json,zipfile,hashlib,re,html
from urllib.parse import unquote,urlsplit
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parent
BOOK=ROOT.parent
PUBLIC=ROOT/'public'
PUBLIC.mkdir(exist_ok=True)
# Explicit file selection prevents publishing source backups or browser profiles.
page=(BOOK/'START HERE.html').read_text(encoding='utf-8')
links='<div class="callout"><strong>Download and study offline</strong><p><a href="downloads/kali-fieldbook.html" download>Offline interactive book</a> · <a href="downloads/lab-examples.zip" download>All lab example files (ZIP)</a> · <a href="downloads/handbook.md" download>Markdown book</a> · <a href="downloads/learning-path.md" download>Study plan</a></p><p>Extract the examples on your own computer. Python and Node.js labs run locally; this website displays the handbook.</p></div>'
page=page.replace('<section class="bookpanel" id="guide">','<section class="bookpanel" id="guide">'+links,1)
page=page.replace('LOCAL EDITION · SEPT 2026','WEB EDITION · SEPT 2026')
page=page.replace('No account or installation.<br>Copy commands; never auto-run.','Read online or download.<br>Interactive diagrams included.')
# Hosting doesn't need access to a specific Windows drive or personal VM path.
(PUBLIC/'index.html').write_text(page,encoding='utf-8')
d=PUBLIC/'downloads';d.mkdir(exist_ok=True)
for src,dst in [('START HERE.html','kali-fieldbook.html'),('Kali Command Handbook.md','handbook.md'),('Learning Path.md','learning-path.md')]:
 (d/dst).write_bytes((BOOK/src).read_bytes())
allowed={'.py','.js','.mjs','.cjs','.html','.md','.txt','.json','.jsonl','.yaml','.gz'}
files=[]
for p in sorted((BOOK/'examples').rglob('*')):
 if p.is_file() and p.suffix in allowed and not any(x.startswith('.') or x=='__pycache__' for x in p.relative_to(BOOK/'examples').parts):files.append(p)
with zipfile.ZipFile(d/'lab-examples.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(p,p.relative_to(BOOK).as_posix())
# Preserve the handbook's linked README; executable examples are downloadable ZIP contents.
readme=PUBLIC/'examples'/'advanced-casebook'/'README.md';readme.parent.mkdir(parents=True,exist_ok=True)
readme.write_bytes((BOOK/'examples/advanced-casebook/README.md').read_bytes())
(PUBLIC/'404.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found</title><body><main><h1>Page not found</h1><p><a href="/">Return to the Kali Fieldbook</a></p></main></body></html>',encoding='utf-8')
(PUBLIC/'robots.txt').write_text('User-agent: *\nAllow: /\n',encoding='utf-8')
# Validate every local hyperlink before deployment.
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  for name in ('href','src'):
   value=a.get(name,'');u=urlsplit(value)
   if not value or u.scheme or u.netloc or value.startswith('#'):continue
   target=PUBLIC/unquote(u.path.lstrip('/'))
   assert target.is_file(),f'Missing local target: {value}'
Links().feed(page)
assert page.count('class="chapter-visual"')==45
assert page.count('<article class="card"')==499
manifest={str(p.relative_to(PUBLIC)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in PUBLIC.rglob('*') if p.is_file()}
assert not any('_source' in x or '__pycache__' in x or 'before-' in x for x in manifest)
(ROOT/'build-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(f'Hosting build checked: {len(manifest)} public files, {len(files)} lab files in ZIP, 499 lessons, 45 diagrams.')

import subprocess,sys
subprocess.run([sys.executable,str(ROOT/'audit_public.py')],check=True)
