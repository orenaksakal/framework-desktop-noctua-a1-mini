"""Check that the stronger skin-volume assertion rejects the original V3 recess.
Run from any directory with the geometry dependencies available. Only scratch is written.
"""
from pathlib import Path
import tempfile,sys,traceback
source=Path(__file__).with_name('build.py')
text=source.read_text()
old=text.replace('male=xz([(-.6,1.2),(0,1.2),(.8,2),(-.6,2)],-5,5)', 'male=xz([(-.6,.6),(0,.6),(1.4,2),(-.6,2)],-5,5)').replace('female=xz([(0,1),(1,2),(1,9),(0,9)],-6,6)', 'female=xz([(0,.4),(1.6,2),(1.6,9),(0,9)],-6.6,6.6)')
assert old!=text
with tempfile.TemporaryDirectory(prefix='noctua-backing-') as scratch:
 sys.argv=[str(source),'--out-dir',scratch]
 try:exec(compile(old,str(source),'exec'),{'__name__':'__main__','__file__':str(source)})
 except AssertionError as error:
  tb=traceback.extract_tb(error.__traceback__)[-1]
  assert '(skin-assembled).volume()' in (tb.line or ''),tb
  print('PASS: original V3 recess is rejected by the full backing-volume check.')
 else:raise AssertionError('Original thin recess was incorrectly accepted')
