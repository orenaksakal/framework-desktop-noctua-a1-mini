from pathlib import Path
import json,subprocess,hashlib
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--scratch-dir',required=True,type=Path);args=parser.parse_args()
repo=Path(__file__).resolve().parents[2];out=repo/'glued-framed-v3';scratch=args.scratch_dir.resolve();scratch.mkdir(parents=True,exist_ok=True)
root=Path('/Applications/BambuStudio.app/Contents/Resources/profiles/BBL');idx={p.stem:p for p in root.rglob('*.json')}
def load(name):
 o=json.loads(idx[name].read_text());m=load(o['inherits']) if o.get('inherits') else {}
 for i in o.get('include',[]):m.update(load(i))
 m.update(o);m.pop('inherits',None);m.pop('include',None);return m
machine=load('Bambu Lab A1 mini 0.4 nozzle');process=load('0.16mm Optimal @BBL A1M');filament=load('Bambu PETG HF @BBL A1M')
process.update(json.loads((repo/'engineering/verified-process-overrides.json').read_text()))
process.update({'name':'Noctua glued framed V3.1 0.16','enable_support':'0','brim_type':'outer_only','brim_width':'2','brim_object_gap':'0.15','elefant_foot_compensation':'0.15','enable_prime_tower':'0','curr_bed_type':'Textured PEI Plate'})
for name,o in [('machine',machine),('process',process),('filament',filament)]: (scratch/(name+'.json')).write_text(json.dumps(o))
summary=[]
validated=json.loads((out/'validation.json').read_text())['files']
assert set(validated)=={p.name for p in out.glob('*.stl')}
for p in sorted(out.glob('*.stl')):
 assert hashlib.sha256(p.read_bytes()).hexdigest()==validated[p.name]['sha256'],p
 proc=dict(process)
 # Original mounting features still need automatic supports on full panels.
 if '_panel_' in p.name or '_duct_' in p.name:proc['enable_support']='1'
 cfg=scratch/(p.stem+'.json');cfg.write_text(json.dumps(proc))
 target=scratch/p.stem;target.mkdir(exist_ok=True)
 # Remove only this verifier's previous G-code to prevent a stale-output pass.
 for old in target.glob('plate_*.gcode'):old.unlink()
 cmd=['/Applications/BambuStudio.app/Contents/MacOS/BambuStudio','--debug','2','--load-settings',str(scratch/'machine.json')+';'+str(cfg),'--load-filaments',str(scratch/'filament.json'),'--orient','0','--arrange','1','--slice','0','--outputdir',str(target),str(p)]
 with (scratch/(p.stem+'.log')).open('w') as log:r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,timeout=120)
 log=(scratch/(p.stem+'.log')).read_text();assert r.returncode==0,(p,log)
 codes=list(target.glob('*.gcode'));assert len(codes)==1;g=codes[0].read_text();assert '; EXECUTABLE_BLOCK_END' in g
 entry={'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'gcode_sha256':hashlib.sha256(codes[0].read_bytes()).hexdigest(),'settings_sha256':{name:hashlib.sha256(file.read_bytes()).hexdigest() for name,file in [('machine',scratch/'machine.json'),('process',cfg),('filament',scratch/'filament.json')]},'exit_code':r.returncode,'supports_enabled':proc['enable_support']=='1','header':g[:g.index('; HEADER_BLOCK_END')].splitlines()[1:],'warnings':[l for l in log.splitlines() if '[warning]' in l or '[error]' in l]}
 summary.append(entry);print(json.dumps(entry),flush=True)
(out/'slicing-validation.json').write_text(json.dumps(summary,indent=2))
