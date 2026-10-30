"""Build a deterministic, text-only NEMESIS registry test fixture."""
import hashlib
import re
import sys
import zipfile
from pathlib import Path

version = sys.argv[1]
if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:-build\.[0-9]+)?", version):
    raise SystemExit("Use a numeric version such as 0.1.0")
output = Path("dist")
output.mkdir(exist_ok=True)
archive = output / f"nemesis.registry.example-{version}.zip"
files = {
    "NEMESIS.data": f"[nemesis]\nid=nemesis.registry.example\nname=NEMESIS Registry Example\nversion={version}\ndescription=Text-only staging registry fixture\n",
    "README.txt": "NEMESIS staging registry example.\nText-only fixture; no APK, scripts, services, or vehicle changes.\nRedistribution is permitted for registry testing.\n",
}
with zipfile.ZipFile(archive, "w") as package:
    for name, content in files.items():
        member = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
        member.compress_type = zipfile.ZIP_DEFLATED
        member.external_attr = 0o100644 << 16
        package.writestr(member, content.encode("utf-8"), compresslevel=9)
digest = hashlib.sha256(archive.read_bytes()).hexdigest()
(output / "SHA256SUMS").write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
print(f"Built {archive.name}: {archive.stat().st_size} bytes, SHA-256 {digest}")
