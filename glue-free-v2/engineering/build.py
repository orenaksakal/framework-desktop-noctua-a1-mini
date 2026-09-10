"""Experimental glue-free Noctua panel remix. CC BY-NC-SA 4.0; units mm.
Run with dependencies in requirements.txt. Physical validation is still required.
"""
import json,math,hashlib,argparse
from pathlib import Path
import numpy as np,trimesh,manifold3d as md
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=HERE.parent
T=np.array([[1,0,0,233.55294799804688],[0,0,-1,185.2586669921875],[0,-1,0,104.08545684814453],[0,0,0,1.]])
F=np.diag([1.,-1.,1.,1.])
checks={}; files={}
def box(x0,x1,y0,y1,z0,z1):return md.Manifold.cube([x1-x0,y1-y0,z1-z0]).translate([x0,y0,z0])
def union(items):return md.Manifold.batch_boolean(items,md.OpType.Add)
def tm(s):
 m=s.simplify(.001).to_mesh();t=trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3],np.asarray(m.tri_verts),process=True)
 t.update_faces(t.nondegenerate_faces(height=1e-8));t.update_faces(t.unique_faces());t.remove_unreferenced_vertices();return t
def solid(m):return md.Manifold(md.Mesh(np.asarray(m.vertices,dtype=np.float32),np.asarray(m.faces,dtype=np.uint32)))
def xz_prism(p,y0,y1):
 # CrossSection XY becomes physical XZ; extrusion maps into +Y.
 s=md.CrossSection([p]).extrude(y1-y0)
 return s.transform(np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0]],dtype=float))
def local_system(clearance=.20):
 # Original minimum skin 2.0 mm. Rails reach depth 2.8 mm; latch/head reaches 4.0 mm.
 pads=[]; cuts=[]; shoes=[]
 for x in [-6.5,6.5]:
  pads.append(box(x-4.2,x+4.2,-.8,20.0,1.,2.75))
  channel=[(x-3.2,1.),(x+3.2,1.),(x+3.2,1.4),(x+1.8,2.8),(x+1.8,5.),(x-1.8,5.),(x-1.8,2.8),(x-3.2,1.4)]
  cuts.append(xz_prism(channel,0,18.2))
  # Top-loading window for the key's two feet, then a 10 mm slide into the rails.
  cuts.append(box(x-3.25,x+3.25,-.05,8.5,1.,5.))
  # Standard horizontal clearance .20 mm; slope clearance is larger at the transition.
  wide=3.2-clearance; narrow=1.8-clearance
  profile=[(x-wide,1.2),(x+wide,1.2),(x+wide,1.3),(x+narrow,2.7),(x+narrow,4.),(x-narrow,4.),(x-narrow,2.7),(x-wide,1.3)]
  shoes.append(xz_prism(profile,10,18))
 # Crossbar runs above rail caps, leaving .20 mm nominal vertical clearance.
 bar=box(-8.1,8.1,15,18,3.,4.)
 arm=box(-.5,.5,3.4,16.,3.,4.)
 # Root widens toward the crossbar to reduce an abrupt root corner.
 root=md.CrossSection([[(-.5,13.5),(.5,13.5),(1.3,15.5),(-1.3,15.5)]]).extrude(1.).translate([0,0,3.])
 barb=md.CrossSection([[(.4,3.4),(1.35,3.4),(1.35,3.9),(.4,5.2)]]).extrude(1.).translate([0,0,3.])
 catch=box(.9,2.8,1.,3.2,.9,4.)
 key=union(shoes+[bar,arm,root,barb])
 return union(pads+[catch]),union(cuts),key,union(shoes+[bar]),union([arm,root,barb])

def pose(s,x,y,angle):return s.rotate([0,0,angle]).translate([x,y,0])
locations=[(45.,v,0.) for v in [12.,45.,85.,125.,165.]]+[(u,35.,90.) for u in [80.,130.,180.]]
path=ROOT/'originals/framework_desktop_noctua_side_panel.stl'
m=trimesh.load(path);assert m.is_watertight;m.apply_transform(T);original=solid(m)
add,cut,key,rigid,flex=local_system()
assert key.volume()>100 and len(key.decompose())==1
new=original
for x,y,a in locations:
 # Check the original substrate and original ventilation remain under solid-border placement.
 foot=pose(box(-11,11,-.8,20,0,1.),x,y,a)
 assert (foot-original).volume()<.01,(x,y,'substrate')
 new=(new+pose(add,x,y,a))-pose(cut,x,y,a)
R,A=new.split_by_plane([1,0,0],45.)
C,B=R.split_by_plane([0,1,0],35.)
parts={'01_panel_A_glue_free':A,'02_panel_B_glue_free':B,'03_panel_C_glue_free':C}
assert abs(sum(p.volume() for p in parts.values())-new.volume())<.01
for region in [box(65,210,48,185,-1,9),box(-1,220,-1,205,-.1,.9)]:
 assert ((new^region)-(original^region)).volume()<.01
 assert ((original^region)-(new^region)).volume()<.01
# Check unmodified original mounting protrusions are retained.
mounts=original^box(-1,220,-1,205,2.81,9)
assert (mounts-new).volume()<.01
for x,y,a in locations:
 assert (pose(key,x,y,a)^new).volume()<.01,(x,y,'key collision')
 # Rigid load-bearing parts slide without intersecting panel/rails.
 for travel in np.linspace(-10,0,21):
  assert (pose(rigid.translate([0,float(travel),0]),x,y,a)^new).volume()<.01,(x,y,'rigid path',travel)
 # Key can be inserted vertically in the loading window.
 for rise in np.linspace(0,5,11):
  assert (pose(key.translate([0,-10,float(rise)]),x,y,a)^new).volume()<.01,(x,y,'loading path',rise)
# Local surrogate containing the same rails, floor and latch used for motion checks.
receiver=(box(-14,14,-2,22,0,2)+add)-cut
assert (key^receiver).volume()<.001
checks['unflexed_reverse_motion_collision_mm3']=(key.translate([0,-.5,0])^receiver).volume()
assert checks['unflexed_reverse_motion_collision_mm3']>.01
checks['upward_removal_collision_mm3']=(key.translate([0,0,.5])^receiver).volume()
assert checks['upward_removal_collision_mm3']>.01
# Each receiver half is captured across the seam by its own dovetail foot.
rr,ll=receiver.split_by_plane([1,0,0],0)
checks['left_half_pull_apart_collision_mm3']=(ll.translate([-.5,0,0])^key).volume()
checks['right_half_pull_apart_collision_mm3']=(rr.translate([.5,0,0])^key).volume()
assert checks['left_half_pull_apart_collision_mm3']>.01
assert checks['right_half_pull_apart_collision_mm3']>.01
for i,(x,y,a) in enumerate(locations):
 for x2,y2,a2 in locations[i+1:]:assert (pose(key,x,y,a)^pose(key,x2,y2,a2)).volume()<.001
checks['installed_keys_do_not_collide_with_each_other']=True
# A bowed tongue is a geometric clearance check only, not an FEA/material validation.
flexmesh=tm(flex);v=flexmesh.vertices.copy();t=np.clip((15.5-v[:,1])/12.1,0,1)
v[:,0]-=.7*(t*t*(3-t)/2)
flexmesh.vertices=v;deflected=solid(flexmesh)
assert str(deflected.status())=='Error.NoError'
releasekey=rigid+deflected
for travel in np.linspace(-10,0,41):
 assert (releasekey.translate([0,float(travel),0])^receiver).volume()<.002,('deflected motion',travel)
checks.update({'main_grille_unchanged':True,'exterior_first_0_9_mm_unchanged':True,'original_mounting_protrusions_retained':True,'assembled_parts_partition_without_volume_loss':True,'all_8_keys_clear_panel_when_locked':True,'rigid_slide_sweep_samples_per_joint':21,'vertical_loading_samples_per_joint':11,'deflected_tongue_sweep_samples':41,'deflected_tongue_tip_displacement_mm':.7,'motion_check_is_geometric_not_FEA':True,'STL_export_simplification_max_surface_movement_mm':0.001,'maximum_depth_from_exterior_mm':4.,'maximum_added_depth_over_2mm_skin_mm':2.,'physical_case_clearance_unverified':True})
assert np.linalg.det((F@T)[:3,:3])==1

def export(name,s,angle=0,invert=False,count=1):
 assert str(s.status())=='Error.NoError' and s.volume()>0
 mesh=tm(s);mesh.apply_transform(F)
 if invert:mesh.apply_transform(trimesh.transformations.rotation_matrix(math.pi,[1,0,0]))
 if angle:mesh.apply_transform(trimesh.transformations.rotation_matrix(math.radians(angle),[0,0,1]))
 mesh.apply_translation(-mesh.bounds[0]);p=OUT/(name+'.stl');mesh.export(p)
 test=trimesh.load(p);ss=solid(test)
 assert test.is_watertight and test.is_winding_consistent and test.volume>0,(name,mesh.is_watertight,test.is_watertight,str(ss.status()),len(mesh.faces),len(test.faces))
 assert str(ss.status())=='Error.NoError' and len(ss.decompose())==count
 assert np.all(test.extents<=[174,174,180]),(name,test.extents)
 files[p.name]={'size_mm':test.extents.tolist(),'components':count,'triangles':len(test.faces),'watertight':True,'consistent_winding':True,'volume_mm3':float(test.volume),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
for name,p in parts.items():export(name,p,angle=45 if '_A_' in name else 0)
export('04_sliding_keys_PRINT_ONCE_8_keys',union([key.translate([24*(i%4),28*(i//4),0]) for i in range(8)]),invert=True,count=8)
# Actual panel coupon: two halves of the joint at (45,85), packed apart for printing.
a=A^box(31,45,83,107,0,8);b=C^box(45,59,83,107,0,8)
export('00a_PRINT_FIRST_receiver_halves',union([a.translate([-31,-83,0]),b.translate([-25,-83,0])]),count=2)
export('00b_PRINT_FIRST_sliding_key',key,invert=True)
for clearance,label in [(.10,'snug'),(.30,'loose')]:
 alt=local_system(clearance)[2];export('optional_key_'+label,alt,invert=True)
(OUT/'validation.json').write_text(json.dumps({'status':'EXPERIMENTAL: print joint coupons before full panels','source_panel_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'joint_origins_uv_angle_deg':locations,'slide_distance_mm':10,'checks':checks,'files':files},indent=2))
print(json.dumps({'checks':checks,'files':files},indent=2))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--reference-dir',type=Path);args=parser.parse_args()
 if args.reference_dir:
  args.reference_dir.mkdir(parents=True,exist_ok=True)
  tm(new).export(args.reference_dir/'assembled_panel.stl');tm(receiver).export(args.reference_dir/'receiver.stl');tm(key).export(args.reference_dir/'locked_key.stl')
