import json,subprocess,datetime
from email.utils import parsedate_to_datetime
links=json.load(open('links.json'))
urls={}
for g in links.get('groups',{}).values():
    for it in g.get('items',[]): urls[it['url']]=1
out={}
for u in urls:
    r=subprocess.run(['curl','-sL','-D','-','-o','/dev/null','-w','%{http_code}','--max-time','20',u],capture_output=True,text=True)
    code=int((r.stdout.strip().splitlines() or ['0'])[-1] or 0)
    lm=''
    for line in r.stdout.splitlines():
        if line.lower().startswith('last-modified:'): lm=line.split(':',1)[1].strip()
    e={'ok':code in (401,403) or 200<=code<400,'code':code}
    if lm:
        try: e['modified']=parsedate_to_datetime(lm).isoformat()
        except Exception: pass
    out[u]=e
try: old=json.load(open('status.json')).get('links')
except Exception: old=None
if old!=out:
    json.dump({'checked':datetime.datetime.utcnow().isoformat()+'Z','links':out},open('status.json','w'),indent=2)
