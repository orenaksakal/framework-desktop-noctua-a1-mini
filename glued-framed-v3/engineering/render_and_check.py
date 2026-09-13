from pathlib import Path
import json,math,re,hashlib
import numpy as np,trimesh
from PIL import Image,ImageDraw,ImageFont
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--reference-dir',type=Path,required=True);parser.add_argument('--slicer-dir',type=Path,required=True);args=parser.parse_args()
out=Path(__file__).resolve().parents[1]
f=lambda n:ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',n)
b=lambda n:ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',n)
bg='#f7f6f2';ink='#263932'
im=Image.new('RGB',(1560,1090),bg);d=ImageDraw.Draw(im)
d.text((45,30),'Glued V3.1 / a deliberate frame',font=b(38),fill=ink)
d.text((45,85),'Actual mesh rendering — appearance and fit still need a PETG sample.',font=f(24),fill=ink)
m=trimesh.load(args.reference_dir/'assembly.stl');scale=3.15;ox=55;oy=165
for ix in np.argsort(-m.triangles[:,:,2].mean(1)):
 t=m.triangles[ix];n=m.face_normals[ix]
 if n[2]>.001:continue
 depth=float(t[:,2].mean());shade=75 if depth<.02 else 52 if depth<.25 else 65
 d.polygon([(ox+x*scale,oy+y*scale) for x,y,z in t],fill=(shade,shade+3,shade+4))
d.text((55,825),'Outside face / one colour',font=b(25),fill=ink)
d.text((55,868),'Two real joins + matching decorative lines.',font=f(22),fill=ink)
d.text((55,902),'0.80 mm opening / 0.24 mm recess.',font=f(22),fill=ink)
d.text((810,168),'Concealed alignment lip',font=b(29),fill=ink)
# Exact CAD cross-section, enlarged. Depth points inward/downward here.
s=115;cx=1040;cy=385
# Base A plus its triangular lip; B minus receiving relief. Outer groove deducted schematically.
left=[(-1.8,0),(-.4,0),(-.16,.24),(0,.24),(0,1.2),(.8,2),(-1.8,2)]
right=[(0,.24),(.16,.24),(.4,0),(3,0),(3,2),(1,2),(0,1)]
for p,c in [(left,'#859e91'),(right,'#b7c5bc')]:d.polygon([(cx+x*s,cy+z*s) for x,z in p],fill=c)
d.text((810,278),'Exterior',font=f(22),fill=ink)
d.line((810,310,1410,310),fill='#909a91',width=2)
d.text((810,660),'Interior',font=f(22),fill=ink)
d.text((810,712),'The angled overlap sits behind the groove.',font=f(21),fill=ink)
d.text((810,750),'It is open on the inside; this still needs glue.',font=f(21),fill=ink)
d.text((810,803),'Lips fit between the eight original glue keys.',font=f(21),fill=ink)
d.text((810,841),'No added thickness inside the computer.',font=f(21),fill=ink)
d.text((810,887),'0.76 mm backing below the groove at each lap.',font=f(20),fill=ink)
d.line((45,968,1515,968),fill='#c8cec8',width=2)
d.text((45,994),'Print the small joint first. Glue on a protected flat surface; keep adhesive out of the front grooves.',font=f(23),fill=ink)
im.save(out/'design-and-joint.png')

# Parse extrusion path coordinates, including arc extrema. Ignore printer start/end routines.
records=[];firstlayers={}
sliced=json.loads((out/'slicing-validation.json').read_text())
expected={p.name for p in out.glob('*.stl')}
assert {r['file'] for r in sliced}==expected and len(sliced)==len(expected)
for receipt in sorted(sliced,key=lambda r:r['file']):
 path=args.slicer_dir/Path(receipt['file']).stem/'plate_1.gcode'
 assert hashlib.sha256((out/receipt['file']).read_bytes()).hexdigest()==receipt['sha256']
 assert hashlib.sha256(path.read_bytes()).hexdigest()==receipt['gcode_sha256']
 x=y=e_pos=0.;z=None;active=False;pts=[];lines=[];role='';relative_e=False
 for line in path.read_text().splitlines():
  if line.startswith('; Z_HEIGHT:'):z=float(line.split(':')[1]);active=True
  if line.startswith('; FEATURE:'):
   role=line.split(':')[1].strip()
   if z is not None:active=role!='Custom'
  if line.startswith('M83'):relative_e=True
  if line.startswith('M82'):relative_e=False
  if line.startswith('G92 E'):e_pos=float(line.split('E')[1].split()[0])
  if not line.startswith(('G0 ','G1 ','G2 ','G3 ')):continue
  v={k:float(n) for k,n in re.findall(r'([XYEIJ])(-?(?:\d+(?:\.\d*)?|\.\d+))',line.split(';')[0])}
  nx=v.get('X',x);ny=v.get('Y',y)
  extrusion=v.get('E',0) if relative_e else v.get('E',e_pos)-e_pos
  if 'E' in v:e_pos=e_pos+v['E'] if relative_e else v['E']
  if active and extrusion>0 and ('X'in v or 'Y'in v):
   p=[(x,y),(nx,ny)]
   if line.startswith(('G2 ','G3 ')):
    cx=x+v.get('I',0);cy=y+v.get('J',0);r=math.hypot(x-cx,y-cy);a=math.atan2(y-cy,x-cx);e=math.atan2(ny-cy,nx-cx);ccw=line.startswith('G3 ')
    sweep=(e-a)%(2*math.pi) if ccw else -((a-e)%(2*math.pi));sweep=sweep or (2*math.pi if ccw else -2*math.pi)
    angles=list(np.linspace(a,a+sweep,max(2,int(abs(sweep)*r*2)+2)))
    for c in [0,math.pi/2,math.pi,3*math.pi/2]:
     delta=(c-a)%(2*math.pi) if ccw else -((a-c)%(2*math.pi))
     if abs(delta)<=abs(sweep):angles.append(a+delta)
    p=[(cx+r*math.cos(t),cy+r*math.sin(t)) for t in sorted(angles,reverse=not ccw)]
   pts+=p
   if z<=.21:lines.extend((p1,p2,role) for p1,p2 in zip(p,p[1:]))
  x,y=nx,ny
 p=np.array(pts);lo=p.min(0);hi=p.max(0);assert np.all(lo>=.25) and np.all(hi<=179.75),(path,lo,hi)
 records.append({'file':receipt['file'],'sha256':receipt['sha256'],'gcode_sha256':receipt['gcode_sha256'],'model_support_brim_extrusion_bounds_mm':[lo.tolist(),hi.tolist()],'inside_A1_mini_bed':True});firstlayers[path.parent.name]=lines
(out/'toolpath-validation.json').write_text(json.dumps(records,indent=2))
image=Image.new('RGB',(1500,1120),bg);d=ImageDraw.Draw(image);d.text((40,25),'V3.1 / actual first-layer toolpaths',font=b(35),fill=ink)
for i,(name,lines) in enumerate(list(firstlayers.items())[:6]):
 ox=40+(i%3)*490;oy=135+(i//3)*465;s=2.1
 d.text((ox,oy-38),name.split('_')[0]+' / '+['Glued joint test','Panel A','Panel B','Panel C','Unchanged duct','Eight glue keys'][i],font=b(23),fill=ink)
 d.rectangle((ox,oy,ox+180*s,oy+180*s),fill='white',outline='#9ca89f',width=2)
 for p,q,role in lines:d.line((ox+p[0]*s,oy+(180-p[1])*s,ox+q[0]*s,oy+(180-q[1])*s),fill='#ba8547' if 'Support' in role else '#bdc1ba' if 'Brim'in role else '#36594c',width=1)
d.text((40,1070),'A1 mini · 0.4 mm nozzle · PETG HF · 0.16 mm layers · supplied orientations',font=f(23),fill=ink);image.save(out/'slicer-preview.png')
