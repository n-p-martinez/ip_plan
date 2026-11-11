"""Build the app from the season workbook.
Usage: python3 build/build.py path/to/IP_Season_Plan_2026-27.xlsx
Writes web/plan.json and web/index.html (plan embedded for offline first launch)."""
import sys, json, datetime as dt, os, openpyxl
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
wb=openpyxl.load_workbook(sys.argv[1],data_only=True)
def d(v): return v.strftime('%Y-%m-%d') if hasattr(v,'strftime') else v
c=wb['Calendar']; cal=[]
for r in range(3,400):
    v=c.cell(r,1).value
    if not hasattr(v,'strftime'): break
    cal.append(dict(date=d(v),wk=c.cell(r,3).value,pr=c.cell(r,4).value,type=c.cell(r,5).value,name=c.cell(r,6).value,
        min=c.cell(r,7).value,target=c.cell(r,8).value,cad=c.cell(r,9).value,detail=c.cell(r,10).value,tag=c.cell(r,11).value,note=c.cell(r,12).value))
s=wb['Season']; season=[]
for r in range(10,60):
    v=s.cell(r,1).value
    if not isinstance(v,int): continue
    season.append(dict(wk=v,mon=d(s.cell(r,2).value),phase=s.cell(r,3).value,type=s.cell(r,4).value,focus=s.cell(r,5).value,
        h10=s.cell(r,6).value,gym=s.cell(r,7).value,h12=s.cell(r,9).value,h15=s.cell(r,10).value,wt=s.cell(r,11).value,tests=s.cell(r,12).value,notes=s.cell(r,13).value))
wt=dict(start=[s['C4'].value,d(s['D4'].value)],mid=[s['C5'].value,d(s['D5'].value)],goal=[s['C6'].value,d(s['D6'].value)])
t=wb['Week templates']; tmpl={}; cur=None
for r in range(3,120):
    a=t.cell(r,1).value; day=t.cell(r,2).value
    if a: cur=a.split(' (')[0]; tmpl[cur]=[]
    if day and cur: tmpl[cur].append(dict(day=day,pr=t.cell(r,3).value,name=t.cell(r,4).value,min=t.cell(r,5).value,detail=t.cell(r,6).value))
z=wb['Zones']
zones=[dict(name=z.cell(r,1).value,lo=z.cell(r,4).value,hi=z.cell(r,5).value,base=z.cell(r,6).value,use=z.cell(r,7).value) for r in range(12,21)]
nums=dict(ftp=z['B6'].value,p4=z['B7'].value,cp=z['B8'].value,wp=z['B9'].value,p20=z['B4'].value)
gears=[[z.cell(r,k).value for k in range(1,8)] for r in range(48,70) if isinstance(z.cell(r,1).value,(int,float)) and isinstance(z.cell(r,2).value,(int,float))]
grid=[[z.cell(r,k).value for k in range(1,6)] for r in range(36,48) if z.cell(r,1).value in (296,285,280)]
ts=wb['Tests']
tests=[dict(when=ts.cell(r,1).value,block=ts.cell(r,2).value,p5=ts.cell(r,3).value,p60=ts.cell(r,4).value,p4=ts.cell(r,5).value,cad=ts.cell(r,6).value,p20=ts.cell(r,7).value,ftp=ts.cell(r,8).value,cp=ts.cell(r,9).value,wp=ts.cell(r,10).value,note=ts.cell(r,12).value) for r in range(4,11)]
rv=wb['Review log']; reviews=[]
for r in range(4,60):
    if not hasattr(rv.cell(r,1).value,'strftime'): break
    reviews.append(dict(date=d(rv.cell(r,1).value),period=rv.cell(r,2).value,changes=rv.cell(r,6).value))
seed=json.load(open(os.path.join(ROOT,'build','seed.json')))
for k in seed['log']: seed['log'][k].setdefault('updated',1)
for k in seed['weight']: seed['weight'][k].setdefault('updated',1)
data=dict(version=dt.datetime.now().strftime('%Y-%m-%dT%H:%M'),cal=cal,season=season,wt=wt,tmpl=tmpl,zones=zones,nums=nums,gears=gears,grid=grid,tests=tests,reviews=reviews,seed=seed)
js=json.dumps(data,separators=(',',':'),default=str)
open(os.path.join(ROOT,'web','plan.json'),'w').write(js)
tpl=open(os.path.join(ROOT,'build','app.template.html')).read()
open(os.path.join(ROOT,'web','index.html'),'w').write(tpl.replace('__PLAN__',js.replace('</','<\\/')))
# bump the service worker cache name so installed web apps pick up new code
sw=open(os.path.join(ROOT,'build','sw.template.js')).read().replace('__VER__',data['version'])
open(os.path.join(ROOT,'web','sw.js'),'w').write(sw)
print('built plan version',data['version'],'days',len(cal))
