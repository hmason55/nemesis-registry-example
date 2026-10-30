import hashlib
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

BUILD = Path(__file__).resolve().parents[1] / 'build_package.py'

class PackageTests(unittest.TestCase):
    def test_exact_identity_checksum_and_reproducible_text_only_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for version in ('0.1.0', '0.1.0-build.7'):
                command = [sys.executable, str(BUILD), version]
                subprocess.run(command, cwd=root, check=True, capture_output=True)
                path = root / 'dist' / ('nemesis.registry.example-' + version + '.zip')
                original = path.read_bytes()
                with zipfile.ZipFile(path) as archive:
                    self.assertEqual(set(archive.namelist()), {'NEMESIS.data', 'README.txt'})
                    manifest = archive.read('NEMESIS.data').decode()
                    self.assertIn('id=nemesis.registry.example\n', manifest)
                    self.assertIn('version=' + version + '\n', manifest)
                    self.assertIsNone(archive.testzip())
                    self.assertTrue(all(member.create_system == 3 for member in archive.infolist()))
                self.assertEqual((root/'dist/SHA256SUMS').read_text().split()[0], hashlib.sha256(original).hexdigest())
                subprocess.run(command, cwd=root, check=True, capture_output=True)
                self.assertEqual(path.read_bytes(), original)

    def test_invalid_versions_cannot_name_output_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            for version in ('../outside', 'v0.1.0', '0.1.0;echo bad', '0.1'):
                result = subprocess.run([sys.executable, str(BUILD), version], cwd=directory, capture_output=True)
                self.assertNotEqual(result.returncode, 0)
            self.assertFalse((Path(directory)/'dist').exists())

if __name__ == '__main__':
    unittest.main()
