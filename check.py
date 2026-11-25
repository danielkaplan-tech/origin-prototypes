import json,subprocess,datetime
links=json.load(open('links.json'))
urls={}
for g in links.get('groups',{}).values():
    for it in g.get('items',[]): urls[it['url']]=1
out={}
for u in urls:
    r=subprocess.run(['curl','-sL','-o','/dev/null','-w','%{http_code}','--max-time','20',u],capture_output=True,text=True)
    code=int(r.stdout or 0)
    out[u]={'ok':code in (401,403) or 200<=code<400,'code':code}
try: old=json.load(open('status.json')).get('links')
except Exception: old=None
if old!=out:
    json.dump({'checked':datetime.datetime.utcnow().isoformat()+'Z','links':out},open('status.json','w'),indent=2)
