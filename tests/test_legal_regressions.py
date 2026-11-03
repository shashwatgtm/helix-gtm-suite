import unittest,json,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'tests/legal-fixture.json').read_text(encoding='utf-8'))
class LegalRegression(unittest.TestCase):
 def test_M059_employment_scope(self):
  for rel in DATA['files']:
   s=(ROOT/rel).read_text(encoding='utf-8-sig')
   self.assertNotIn('India: Enforceable for senior employees',s)
   if 'covenant review template' in s:self.assertIn('during employment from restraints after termination',s);self.assertIn('actual agreement',s);self.assertIn('statutory exceptions',s)
 def test_M060_no_invented_circular(self):
  for rel in DATA['files']:
   s=(ROOT/rel).read_text(encoding='utf-8-sig');self.assertNotIn('RBI/2026/23',s);self.assertNotIn('Guidelines (Jan 2026)',s)
 def test_M061_no_invented_update(self):
  for rel in DATA['files']:
   s=(ROOT/rel).read_text(encoding='utf-8-sig');self.assertNotIn('effective April 1, 2026',s);self.assertNotIn('New: Monthly submission to RBI',s)
   self.assertIn('check the current rule',s);self.assertIn('official',s.lower())
 def test_M103_no_blanket_kyc_or_retention(self):
  for rel in DATA['files']:
   s=(ROOT/rel).read_text(encoding='utf-8-sig');self.assertNotIn('Large loans (>₹50K)',s);self.assertNotIn('Recording stored 10 years',s)
   if 'KYC applicability worksheet' in s:self.assertIn('account type and onboarding mode',s);self.assertIn('event that starts the period',s)
 def test_reviewed_frontmatter_unchanged(self):
  for rel,want in DATA['frontmatter'].items():
   s=(ROOT/rel).read_bytes().decode('utf-8-sig');fm=re.match(r'\A---\r?\n.*?\r?\n---',s,re.S)[0];self.assertEqual(hashlib.sha256(fm.encode()).hexdigest(),want)
if __name__=='__main__':unittest.main()
