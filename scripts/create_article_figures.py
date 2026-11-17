"""Generate reproducible editorial illustrations (not fabricated CI success screenshots)."""
from pathlib import Path
import cairosvg
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'/'images'
OUT.mkdir(parents=True,exist_ok=True)

def svg(name,txt):
 (OUT/f'{name}.svg').write_text(txt,encoding='utf-8')
 cairosvg.svg2png(bytestring=txt.encode(),write_to=str(OUT/f'{name}.png'),output_width=1600,output_height=900)

base='''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900"><defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#080e20"/><stop offset="1" stop-color="#252056"/></linearGradient><linearGradient id="purple"><stop stop-color="#5f7ef7"/><stop offset="1" stop-color="#ad6cf7"/></linearGradient></defs><rect width="1600" height="900" fill="url(#bg)"/><circle cx="1410" cy="190" r="270" fill="#5b3c9c" opacity=".15"/><circle cx="80" cy="780" r="290" fill="#00d8f0" opacity=".08"/>'''
def t(x,y,string,size=32,color='#e7eafa',weight='500'):
 import html
 return f'<text x="{x}" y="{y}" font-family="DejaVu Sans,Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{html.escape(string)}</text>'
def block(x,y,w,h,title,desc,idx,accent='#9176f5'):
 s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="23" fill="#141e38" stroke="{accent}" stroke-width="3"/>'
 s+=f'<rect x="{x+22}" y="{y+22}" width="48" height="44" rx="12" fill="{accent}" opacity=".22"/>'
 s+=t(x+35,y+54,str(idx),25,accent,'700')+t(x+24,y+105,title,28,'#ffffff','700')+t(x+24,y+145,desc,17,'#a4bad9')
 return s

s=base+t(80,107,'FlowForge DE | DATA PIPELINE ARCHITECTURE',37,'#fff','700')+t(80,156,'From deterministic CSV inputs to tested data marts and public analytics',23,'#a4b6d7')
items=[('EXTRACT','Python / CSV',1),('LOAD','DuckDB raw',2),('TRANSFORM','dbt staging + fact',3),('PUBLISH','JSON + Pages',4)]
for i,(a,b,j) in enumerate(items):
 x=60+i*398;s+=block(x,272,352,208,a,b,j)
 if i<3:s+=t(x+358,386,'→',42,'#35dfdc','700')
s+=f'<rect x="81" y="577" width="1438" height="176" rx="24" fill="#0b172c" stroke="#303e73" stroke-width="2"/>'
s+=t(120,642,'AUTOMATION:',28,'#42dde8','700')+t(350,642,'GitHub Actions — push / manual / scheduled daily',25,'#fff')
s+=t(120,700,'Quality gates: Python tests + dbt tests + verified output  •  No AWS required',22,'#a8c2df')
s+=t(80,837,'Architecture illustration — FlowForge DE',18,'#8e99b9')+'</svg>'
svg('02-architecture',s)

s=base+t(80,108,'TRANSFORMATION LAYERS | DBT LINEAGE',37,'#fff','700')+t(80,158,'A traceable, testable path from raw sources to a curated sales mart',22,'#a4b6d7')
for i,(title,desc) in enumerate([('RAW SOURCES','Orders • Customers • Products'),('STAGING','Type casting • status cleanup'),('FACT TABLE','Completed orders • revenue • profit'),('MART','Month × Region × Category')]):
 x=55+400*i;s+=block(x,275,355,228,title,desc,i+1)
 if i<3:s+=t(x+359,404,'→',39,'#35dfdc','700')
s+=f'<rect x="74" y="593" width="1452" height="175" rx="20" fill="#1b2445" stroke="#404f84"/>'
s+=t(110,657,'QUALITY TESTS',28,'#41dce9','700')
s+=t(110,706,'Unique IDs  •  Non-null fields  •  Foreign-key relationships  •  Accepted statuses',22,'#f4f6ff')
s+=t(75,840,'Conceptual illustration — exact model names are implemented in the repository',18,'#9baed1')+'</svg>'
svg('03-dbt-lineage',s)

s=base+t(80,105,'CI/CD | AUTOMATED DATA PIPELINE',39,'#fff','700')+t(80,154,'Example pipeline stages — check GitHub Actions for actual run status',22,'#b2c1df')
steps=[('01','CHECKOUT','GitHub repository'),('02','VALIDATE','Python pytest'),('03','INGEST','CSV → DuckDB'),('04','TRANSFORM','dbt build + tests'),('05','EXPORT','Aggregated JSON'),('06','DEPLOY','GitHub Pages')]
for i,(num,title,detail) in enumerate(steps):
 col=i%3;row=i//3;x=90+510*col;y=260+231*row;s+=block(x,y,462,170,title,detail,num)
 if col<2:s+=t(x+465,y+103,'→',32,'#36ddec')
s+=t(90,831,'Workflow diagram — not an actual success screenshot',21,'#9aaccb')+'</svg>'
svg('05-ci-workflow-illustration',s)

s=base+t(80,107,'DATA QUALITY | ENGINEERING VALIDATION',36,'#fff','700')+t(80,157,'Test strategy for a reliable data pipeline',23,'#a0b5d8')
quality=[('VALIDATION 01','Unique order and dimension IDs'),('VALIDATION 02','Required fields cannot be null'),('VALIDATION 03','Orders reference known dimensions'),('VALIDATION 04','Order status in allowed values'),('VALIDATION 05','Non-negative revenue and costs'),('VALIDATION 06','Fact totals reconcile with published mart')]
for i,(a,b) in enumerate(quality):
 col=i%2;row=i//2;x=82+745*col;y=239+190*row
 s+=f'<rect x="{x}" y="{y}" width="696" height="154" rx="19" fill="#171f3b" stroke="#364b6b" stroke-width="2"/>'
 s+=t(x+30,y+58,'✓',39,'#47e3b8','700')+t(x+99,y+60,a,23,'#d6bcff','700')+t(x+99,y+104,b,22,'#edf5ff')
s+=t(84,847,'Validation strategy illustration — actual test results must be verified in CI',18,'#9aaccb')+'</svg>'
svg('06-data-quality',s)

# Use existing user-approved cover generation, scaled into the article set
source=Path('/mnt/data/a_polished_high_contrast_neon_tech_infographic_ba.png')
if source.exists():
 im=Image.open(source).convert('RGB'); im.resize((1600,900),Image.Resampling.LANCZOS).save(OUT/'01-cover.png')
print('Created editorial figures:', [x.name for x in sorted(OUT.glob('*.png'))])
