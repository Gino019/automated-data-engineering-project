"""Render a truthful static, data-derived dashboard illustration from local synthetic preview."""
import json
from pathlib import Path
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'site/data/metrics.json').read_text())
W,H=1600,900
im=Image.new('RGB',(W,H),'#080d1a'); g=ImageDraw.Draw(im)
font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold_path='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(n,b=False):return ImageFont.truetype(bold_path if b else font_path,n)
def text(x,y,s,n=20,color='#ffffff',bold=False):g.text((x,y),s,font=font(n,bold),fill=color)
def rounded(x,y,w,h,fill='#121b30',outline='#2b3853',radius=19):g.rounded_rectangle((x,y,x+w,y+h),radius=radius,fill=fill,outline=outline,width=2)
# Sidebar
g.rectangle((0,0,250,H),fill='#101427');text(33,36,'✦ FlowForge',30,'#f0eaff',True);text(34,77,'DATA ENGINEERING',14,'#9b90d9')
for j,title in enumerate(['▦ Overview','◈ Pipeline lineage','⬡ Data quality','▤ Curated data']):
 y=180+j*67
 if j==0:rounded(19,y-9,212,54,'#2d2152','#7358a2',10)
 text(38,y,title,18,'#dfd4fb' if j==0 else '#9daccc')
text(30,840,'Synthetic preview only',16,'#a8b9d0')
text(295,37,'DATA WORKSPACE / OVERVIEW',19,'#b9c8ea',True)
text(295,98,'FlowForge DE',43,'#fafaff',True);text(641,105,'|  Curated sales intelligence',22,'#b5a1f4')
text(295,161,'Dashboard generated from a deterministic synthetic source dataset',18,'#9eafc8')
records=d['rows'];s={'revenue':sum(x['revenue'] for x in records),'orders':sum(x['orders'] for x in records),'profit':sum(x['profit'] for x in records)}
items=[('Total Revenue',f'${s["revenue"]:,.0f}'),('Completed Orders',f'{s["orders"]:,}'),('Gross Profit',f'${s["profit"]:,.0f}'),('Profit Margin',f'{s["profit"]/s["revenue"]*100:.1f}%')]
for j,(label,val) in enumerate(items):
 x=295+j*316;rounded(x,220,297,140);text(x+20,242,label,17,'#a6b8d8');text(x+20,280,val,32,'#f6f5ff',True);text(x+20,327,'Verified synthetic preview',11,'#9eb2d7')
rounded(295,383,934,290);rounded(1248,383,316,290)
text(316,400,'Monthly Revenue Trend',21,'#fff',True);text(1266,400,'Revenue by Category',18,'#fff',True)
month=defaultdict(float)
cat=defaultdict(float)
for r in records:month[r['month']]+=r['revenue'];cat[r['category']]+=r['revenue']
monthly=sorted(month.items());max_val=max(v for k,v in monthly)
coords=[]
for i,(m,v) in enumerate(monthly):
 x=336+int(i*854/(len(monthly)-1));y=630-int((v/max_val)*160);coords.append((x,y))
for k in range(4):
 y=630-k*47;g.line((338,y,1180,y),fill='#293652',width=1)
g.line(coords,fill='#9d80f8',width=5)
for x,y in coords:g.ellipse((x-3,y-3,x+3,y+3),fill='#5ddbe5')
for k in range(0,len(monthly),4):text(335+int(k*854/(len(monthly)-1)),644,monthly[k][0],12,'#9aaed0')
colors=['#9477ff','#56d4e7','#698efa','#e58ecb']
for i,(catname,val) in enumerate(sorted(cat.items(),key=lambda e:-e[1])):
 y=451+i*49;text(1266,y,catname,15,'#c9d2ed');g.rounded_rectangle((1267,y+23,1530,y+34),radius=5,fill='#263653');g.rounded_rectangle((1267,y+23,1267+int(263*val/max(cat.values())),y+34),radius=5,fill=colors[i]);text(1442,y,f'${val/1000:.0f}k',13,'#e4edff')
rounded(295,699,1269,123)
text(319,720,'PIPELINE PROVENANCE',17,'#d4bafd',True)
text(319,760,f'Sources: {d["quality"]["raw_orders"]:,} orders / {d["quality"]["customers"]} customers / {d["quality"]["products"]} products',17,'#c3cee5')
text(319,793,'Preview generated locally (dbt pipeline must be verified in GitHub Actions)',14,'#95aed1')
text(296,856,'FIGURE: Synthetic dashboard preview • Not a deployed application screenshot',15,'#8799b9')
im.save(ROOT/'docs/images/04-dashboard-preview.png')
print('dashboard image',ROOT/'docs/images/04-dashboard-preview.png')
