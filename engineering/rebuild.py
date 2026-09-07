"""Noctua panel remix. Source + derived output: CC BY-NC-SA 4.0. Units mm."""
import sys, json, hashlib, math
from pathlib import Path
# Install dependencies from requirements.txt before running this optional generator.
import numpy as np, trimesh, manifold3d as md
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient
BASE=Path(__file__).resolve().parent; OUT=BASE/'regenerated'; OUT.mkdir(exist_ok=True); (BASE/'work').mkdir(exist_ok=True)
SRC=BASE.parent/'originals'  # Original Noctua STL files bundled with this repository
report={'units':'mm','source':{},'parts':{},'checks':{},'joint':{'pocket_floor_depth':1.0,'key_thickness':0.8,'key_side_clearance':0.20,'key_installed_depth':[1.1,1.9],'count':8}}
T=np.array([[1,0,0,233.55294799804688],[0,0,-1,185.2586669921875],[0,-1,0,104.08545684814453],[0,0,0,1.]])
# Internal design coordinates use a reflection to match the top-down drawing.
# Every printed panel receives a second reflection, so source->print is a proper rotation.
F=np.diag([1.,-1.,1.,1.])
def tomd(mesh):
 return md.Manifold(md.Mesh(np.asarray(mesh.vertices,dtype=np.float32),np.asarray(mesh.faces,dtype=np.uint32)))
def totm(s):
 m=s.to_mesh(); return trimesh.Trimesh(vertices=np.asarray(m.vert_properties)[:,:3],faces=np.asarray(m.tri_verts),process=True)
def box(lo,hi):return md.Manifold.cube(np.array(hi)-lo).translate(lo)
def source(name):
 p=SRC/name;report['source'][name]=hashlib.sha256(p.read_bytes()).hexdigest();m=trimesh.load(p)
 assert m.is_watertight and m.is_winding_consistent and m.volume>0
 return m
m=source('framework_desktop_noctua_side_panel.stl');m.apply_transform(T);original=tomd(m);assert str(original.status())=='Error.NoError'
# Butterfly pocket: 20 x 12 mm, 8 mm-wide waist.
poly=Polygon([(-10,-6),(-3,-4),(3,-4),(10,-6),(10,6),(3,4),(-3,4),(-10,6)])
def cross(poly):return md.CrossSection([list(orient(poly, sign=1.0).exterior.coords)[:-1]])
def key(clearance=.20):return cross(poly.buffer(-clearance,join_style=2)).extrude(.8)
locations=[(45,y,0) for y in [15,55,95,135,175]]+[(x,35,90) for x in [80,130,180]]
pockets=[];installed=[]
for x,y,angle in locations:
 pocket=cross(poly).extrude(8).rotate([0,0,angle]).translate([x,y,1])
 # Full skin under every pocket is solid up to 1.95 mm; no vent or exterior pierced.
 skin=cross(poly).extrude(1.95).rotate([0,0,angle]).translate([x,y,0])
 assert (skin-original).volume()<.002,(x,y,'insufficient skin', (skin-original).volume())
 k=key().rotate([0,0,angle]).translate([x,y,1.1])
 assert (k-original).volume()<.002
 pockets.append(pocket);installed.append(k)
cutters=md.Manifold.batch_boolean(pockets,md.OpType.Add)
modified=original-cutters
right,A=modified.split_by_plane([1,0,0],45)
C,B=right.split_by_plane([0,1,0],35)
parts={'01_panel_A_logo_strip':A,'02_panel_B_upper_strip':B,'03_panel_C_main_grille':C}
assembled=md.Manifold.batch_boolean(list(parts.values()),md.OpType.Add)
assert abs(assembled.volume()-modified.volume())<.01
assert (assembled-original).volume()<.01
vent_region=box([65,48,-1],[210,185,9])
assert ((original^vent_region)-(assembled^vent_region)).volume()<.01
mount_region=box([-1,-1,2.81],[220,205,9])
assert ((original^mount_region)-(assembled^mount_region)).volume()<.01
# Exterior layer exactly preserved by the split and pockets.
outer=box([-1,-1,-.1],[220,205,.9])
assert ((original^outer)-(assembled^outer)).volume()<.01
for k in installed: assert (k^assembled).volume()<.001
report['checks'].update({'source_watertight':True,'main_grille_region_entire_depth_unchanged':True,'mounting_features_beyond_2_81mm_depth_unchanged':True,'exterior_first_0_9mm_unchanged':True,'panel_parts_reassemble_without_volume_loss':True,'no_keys_protrude_beyond_original_panel':True,'keys_do_not_collide_with_panel':True,'minimum_solid_skin_before_pocketing_mm':1.95,'original_panel_volume_mm3':original.volume(),'removed_pocket_volume_mm3':original.volume()-modified.volume(),'source_to_print_transform_determinant':float(np.linalg.det((F@T)[:3,:3]))})
assert abs(np.linalg.det((F@T)[:3,:3])-1)<1e-9
manifest=[]
def save(name,s,reflection=False,angle=0,expected=1):
 assert str(s.status())=='Error.NoError'
 mesh=totm(s)
 if reflection:mesh.apply_transform(F)
 if angle:mesh.apply_transform(trimesh.transformations.rotation_matrix(math.radians(angle),[0,0,1]))
 mesh.apply_translation(-mesh.bounds[0])
 assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0
 path=OUT/(name+'.stl');mesh.export(path)
 # Validate the final binary STL after round-trip, not only the construction solid.
 check=trimesh.load(path);solid=tomd(check)
 assert check.is_watertight and check.is_winding_consistent and str(solid.status())=='Error.NoError'
 count=len(solid.decompose());assert count==expected,(name,count)
 assert all(check.extents<=np.array([174,174,180])),(name,check.extents)
 report['parts'][path.name]={'size_mm':check.extents.tolist(),'volume_mm3':float(check.volume),'watertight':True,'consistent_winding':True,'solid_components':count,'triangles':len(check.faces),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 return mesh
for name,s in parts.items():save(name,s,True,45 if 'panel_A' in name else 0)
# Duct proper rigid rotation: X, Z, -Y; broad outer flange down.
duct=source('framework_desktop_noctua_side_panel_duct.stl')
D=np.array([[1,0,0,146.04974365234375],[0,0,1,-18.850000381469727],[0,-1,0,88.9800033569336],[0,0,0,1.]])
assert np.linalg.det(D[:3,:3])==1
duct.apply_transform(D);save('04_duct_whole',tomd(duct))
keys=md.Manifold.batch_boolean([key().translate([24*(i%4),16*(i//4),0]) for i in range(8)],md.OpType.Add)
save('05_keys_standard_PRINT_ONCE_8_keys',keys,expected=8)
# Coupon copied from the actual A/C seam at (45,95), not a simplified surrogate.
left=(A^box([31,85,0],[45,105,8])).translate([-31,-85,0])
right=(C^box([45,85,0],[59,105,8])).translate([-25,-85,0])
coupon=md.Manifold.batch_boolean([left,right,key().translate([17,32,0])],md.OpType.Add)
save('00_PRINT_FIRST_joint_test',coupon,True,expected=3)
optional=OUT/'optional_keys';optional.mkdir(exist_ok=True)
for clearance,label in [(.10,'snug'),(.30,'loose')]:
 name=f'key_{label}_{clearance:.2f}mm_clearance'; save(name,key(clearance))
 (OUT/(name+'.stl')).replace(optional/(name+'.stl'))
 report['parts']['optional_keys/'+name+'.stl']=report['parts'].pop(name+'.stl')
report['joint']['locations_drawing_uv_rotation']=locations
(OUT/'validation.json').write_text(json.dumps(report,indent=2))
# Keep assembled geometry only as internal reference for diagrams, never as an accidental print file.
totm(assembled).export(BASE/'work/assembly.stl')
print(json.dumps(report,indent=2))
