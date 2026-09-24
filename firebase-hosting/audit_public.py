from pathlib import Path
import re,zipfile,gzip,ipaddress,json
ROOT=Path(__file__).resolve().parent
PUBLIC=ROOT/'public'
patterns=[r'(?i)DESKTOP-[A-Z0-9-]+',r'(?i)(?<![a-z])[a-z]:[\\/]',r'192\.168\.56\.',r'\b(?:240|480)\s?GB\b']
allowed={'127.0.0.1','0.0.0.0','10.0.0.0','172.16.0.0','172.31.255.255','192.168.0.0','255.255.255.192'}
nets=[ipaddress.ip_network(x) for x in ['192.0.2.0/24','198.51.100.0/24','203.0.113.0/24']]
checked=0
ips=set()
def inspect(name,data):
 global checked
 if name.endswith('.gz'):data=gzip.decompress(data)
 text=data.decode('utf-8-sig');checked+=1
 for pattern in patterns:assert not re.search(pattern,text),f'Private detail in {name}: {pattern}'
 for value in re.findall(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])',text):
  addr=ipaddress.ip_address(value);assert value in allowed or any(addr in net for net in nets),f'Unreviewed address in {name}'
  ips.add(value)
for p in PUBLIC.rglob('*'):
 if not p.is_file():continue
 if p.suffix=='.zip':
  with zipfile.ZipFile(p) as z:
   for name in z.namelist():inspect(name,z.read(name))
 else:inspect(str(p.relative_to(PUBLIC)),p.read_bytes())
print(f'Privacy PASS: {checked} published texts including ZIP/GZIP contents; addresses limited to reviewed protocol and documentation examples.')
