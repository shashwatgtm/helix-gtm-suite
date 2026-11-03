import unittest,json,subprocess,tarfile,io,zipfile,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ArchiveRegression(unittest.TestCase):
 def test_every_draft_archive_matches_its_canonical_Git_sources(self):
  tree=subprocess.check_output(['git','-C',str(ROOT),'write-tree'],text=True).strip()
  raw=subprocess.check_output(['git','-C',str(ROOT),'archive','--format=tar',tree,'skills'])
  with tarfile.open(fileobj=io.BytesIO(raw)) as t:source={m.name:t.extractfile(m).read() for m in t if m.isfile()}
  rows=json.loads((ROOT/'tests/archive-inventory.json').read_text(encoding='utf-8'))
  for row in rows:
   p=ROOT/row['file'];self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),row['sha256'])
   skill=p.stem;expected={name.removeprefix('skills/'):body for name,body in source.items() if name.startswith('skills/'+skill+'/')}
   with zipfile.ZipFile(p) as z:
    self.assertIsNone(z.testzip());self.assertEqual(set(z.namelist()),set(expected))
    for name,body in expected.items():self.assertEqual(z.read(name),body,name)
if __name__=='__main__':unittest.main()
