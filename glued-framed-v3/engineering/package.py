"""Package V3.1 only when all six files have matching verification receipts."""
from pathlib import Path
import hashlib,json,zipfile,shutil
OUT=Path(__file__).resolve().parents[1];ROOT=OUT.parent
geometry=json.loads((OUT/'validation.json').read_text())
assert geometry['revision']=='3.1'
names={p.name for p in OUT.glob('*.stl')};assert len(names)==6
assert set(geometry['files'])==names
records=[]
for filename in ['slicing-validation.json','toolpath-validation.json']:
 rows=json.loads((OUT/filename).read_text())
 assert len(rows)==len(names) and {r['file'] for r in rows}==names,filename
 records.append({r['file']:r for r in rows})
for name in sorted(names):
 digest=hashlib.sha256((OUT/name).read_bytes()).hexdigest()
 assert geometry['files'][name]['sha256']==digest,name
 sliced,paths=[r[name] for r in records]
 assert sliced['sha256']==paths['sha256']==digest,name
 assert sliced['gcode_sha256']==paths['gcode_sha256'],name
 assert sliced['exit_code']==0 and paths['inside_A1_mini_bed'],name
assert (OUT/'04_duct_unchanged.stl').read_bytes()==(ROOT/'04_duct_whole.stl').read_bytes()
zip_path=ROOT/'downloads/noctua-a1-mini-glued-framed-v3.1-STLs.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(OUT.rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts:z.write(p,p.relative_to(ROOT))
 z.write(ROOT/'LICENSE.md','LICENSE.md')
with zipfile.ZipFile(zip_path) as z:assert z.testzip() is None
# Keep earlier links useful without continuing to distribute the thin V3 recess.
shutil.copy2(zip_path,zip_path.with_name('noctua-a1-mini-glued-framed-v3-STLs.zip'))
print(f'Validated {len(names)} STL files; packaged {zip_path.stat().st_size:,} bytes: {zip_path}')
