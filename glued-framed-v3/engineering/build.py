"""Glued framed V3. Independent Noctua remix, CC BY-NC-SA 4.0. Units mm.
Physical seam appearance, fit, strength and thermal performance are unverified.
"""
from pathlib import Path
import json,hashlib,math,argparse,shutil
import numpy as np,trimesh,manifold3d as md
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient
HERE=Path(__file__).resolve().parent; OUT=HERE.parent; ROOT=OUT.parent
T=np.array([[1,0,0,233.55294799804688],[0,0,-1,185.2586669921875],[0,-1,0,104.08545684814453],[0,0,0,1.]])
F=np.diag([1.,-1.,1.,1.])
def box(x0,x1,y0,y1,z0,z1):return md.Manifold.cube([x1-x0,y1-y0,z1-z0]).translate([x0,y0,z0])
def union(s):return md.Manifold.batch_boolean(s,md.OpType.Add)
def solid(m):return md.Manifold(md.Mesh(np.asarray(m.vertices,dtype=np.float32),np.asarray(m.faces,dtype=np.uint32)))
def mesh(s):
 m=s.simplify(.001).to_mesh();t=trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3],np.asarray(m.tri_verts),process=True)
 t.update_faces(t.nondegenerate_faces(height=1e-8));t.update_faces(t.unique_faces());t.remove_unreferenced_vertices();return t

def xz(p,y0,y1):return md.CrossSection([p]).extrude(y1-y0).transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0]],float))
def pose(s,x,y,a):return s.rotate([0,0,a]).translate([x,y,0])
source=ROOT/'originals/framework_desktop_noctua_side_panel.stl'
m=trimesh.load(source);m.apply_transform(T);original=solid(m)
poly=Polygon([(-10,-6),(-3,-4),(3,-4),(10,-6),(10,6),(3,4),(-3,4),(-10,6)])
def cross(p):return md.CrossSection([list(orient(p,sign=1).exterior.coords)[:-1]])
def key(c=.2):return cross(poly.buffer(-c,join_style=2)).extrude(.8)
keys_at=[(45,y,0) for y in [15,55,95,135,175]]+[(x,35,90) for x in [80,130,180]]
pockets=union([pose(cross(poly).extrude(8).translate([0,0,1]),*p) for p in keys_at])
modified=original-pockets
# Flat-bottom decorative channels: .80 mm face opening, .32 mm floor, .24 mm deep.
# The left/top runs contain the real seams; right/bottom complete the grille frame.
profile=[(-.4,-.1),(.4,-.1),(.4,0),(.16,.24),(-.16,.24),(-.4,0)]
grooves=union([xz(profile,-1,202).translate([45,0,0]),
 pose(xz(profile,45,217),0,35,-90),
 xz(profile,35,194).translate([210,0,0]),
 pose(xz(profile,45,210),0,194,-90)])
# A -90-degree rotation maps local +Y into global +X, local +X into -Y.
modified=modified-grooves
R,A=modified.split_by_plane([1,0,0],45)
C,B=R.split_by_plane([0,1,0],35)
parts={'A':A,'B':B,'C':C}
# Short open-back scarf laps. The male underside grows at 45 degrees in face-down printing.
# Female recess remains open inward: these align and overlap; glue is still required.
male=xz([(-.6,.6),(0,.6),(1.4,2),(-.6,2)],-5,5)
female=xz([(0,.4),(1.6,2),(1.6,9),(0,9)],-6.6,6.6)
laps=[(45,29,0,'A','B'),(45,77,0,'A','C'),(45,117,0,'A','C'),(45,157,0,'A','C'),(45,191,0,'A','C'),
      (106,35,90,'B','C'),(156,35,90,'B','C'),(199,35,90,'B','C')]
# 90 degrees maps local +X into global +Y: B overlaps into C.
for x,y,a,owner,target in laps:
 add=pose(male,x,y,a);cut=pose(female,x,y,a)
 assert (add-original).volume()<.01,(x,y,'lip outside original envelope')
 assert (add^pockets).volume()<.01,(x,y,'lip touches key pocket')
 parts[owner]=parts[owner]+add;parts[target]=parts[target]-cut
assembled=union(list(parts.values()))
checks={}
for i,p in enumerate(parts.values()):
 for q in list(parts.values())[i+1:]:assert (p^q).volume()<.001
checks['parts_do_not_intersect']=True
# Assemble face-down: B approaches A from +X; then C approaches from +X/+Y.
# Longitudinal relief at lap ends permits the final two-edge insertion.
for travel in np.linspace(0,5,51):
 assert (parts['B'].translate([float(travel),0,0])^parts['A']).volume()<.001,('B insertion',travel)
 assert (parts['C'].translate([float(travel),float(travel),0])^(parts['A']+parts['B'])).volume()<.001,('C diagonal insertion',travel)
checks['planar_assembly_sweep_samples_per_part']=51

# No new exterior envelope, no additional internal thickness, source ventilation retained.
assert (assembled-original).volume()<.01
checks['within_original_envelope']=True
vent=box(65,209.5,48,185,-1,9)
assert ((original^vent)-(assembled^vent)).volume()<.01
checks['main_grille_region_unchanged']=True
mounts=original^box(-1,220,-1,205,2.81,9)
assert (mounts-assembled).volume()<.01
checks['original_mounting_protrusions_retained']=True
# A continuous original slice remains behind every decorative groove.
skin=original^box(-1,220,-1,205,.25,.39)
assert (skin-assembled).volume()<.001
checks['original_skin_slice_0_25_to_0_39_mm_retained']=True
checks['export_simplification_tolerance_mm']=.001
# Outer surfaces differ only where the deliberately recessed channels were cut.
outer=box(-1,220,-1,205,-.1,.39)
assert (((original-grooves)^outer)-(assembled^outer)).volume()<.001
checks['exterior_unchanged_outside_decorative_channels']=True
# Check the actual modified under-pocket floor at all eight seam/key crossings.
for x,y,a in keys_at:
 floor=pose(box(-.12,.12,-2,2,.25,.99),x,y,a)
 assert (floor-assembled).volume()<.001,(x,y,'thin or absent pocket floor')
 k=pose(key().translate([0,0,1.1]),x,y,a)
 assert (k^assembled).volume()<.001
checks['minimum_skin_under_key_at_groove_mm']=.76
checks['glue_keys_fit_without_collision']=True
checks['groove_opening_mm']=.8;checks['groove_depth_mm']=.24
checks['lip_projection_mm']=1.4;checks['lap_vertical_clearance_mm']=.2
checks['lap_end_clearance_mm']=1.6;checks['added_internal_thickness_mm']=0
files={}
def save(name,s,reflect=True,angle=0,expected=1):
 t=mesh(s)
 if reflect:t.apply_transform(F)
 if angle:t.apply_transform(trimesh.transformations.rotation_matrix(math.radians(angle),[0,0,1]))
 t.apply_translation(-t.bounds[0]);p=OUT/(name+'.stl');t.export(p)
 t=trimesh.load(p);ss=solid(t)
 assert t.is_watertight and t.is_winding_consistent and t.volume>0 and str(ss.status())=='Error.NoError',name
 assert len(ss.decompose())==expected,(name,len(ss.decompose()))
 assert np.all(t.extents<=np.array([176,176,180])),(name,t.extents)
 files[p.name]={'size_mm':t.extents.tolist(),'solid_components':expected,'watertight':True,'consistent_winding':True,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
for letter,label in [('A','logo_strip'),('B','upper_strip'),('C','main_grille')]:save(f'0{ord(letter)-64}_panel_{letter}_{label}',parts[letter],angle=45 if letter=='A' else 0)
# Coupon includes actual vertical seam, lip at y77 and glue key at y95.
l=parts['A']^box(31,47,68,105,0,9);r=parts['C']^box(45,59,68,105,0,9)
save('00_PRINT_FIRST_framed_glued_joint',union([l.translate([-31,-68,0]),r.translate([-25,-68,0]),key().translate([17,46,0])]),expected=3)
save('05_keys_standard_PRINT_ONCE_8_keys',union([key().translate([24*(i%4),16*(i//4),0]) for i in range(8)]),reflect=False,expected=8)
shutil.copy2(ROOT/'04_duct_whole.stl',OUT/'04_duct_unchanged.stl')
files['04_duct_unchanged.stl']={'sha256':hashlib.sha256((OUT/'04_duct_unchanged.stl').read_bytes()).hexdigest(),'unchanged_from':'../04_duct_whole.stl'}
(OUT/'validation.json').write_text(json.dumps({'status':'PROTOTYPE: physical glued sample required','source_panel_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'checks':checks,'key_locations':keys_at,'lap_locations':laps,'files':files},indent=2))
parser=argparse.ArgumentParser();parser.add_argument('--reference-dir',type=Path);args=parser.parse_args()
if args.reference_dir:
 args.reference_dir.mkdir(parents=True,exist_ok=True)
 for name,s in [('assembly',assembled),('coupon_left',l),('coupon_right',r),('original',original)]:mesh(s).export(args.reference_dir/(name+'.stl'))
print(json.dumps(files,indent=2))
