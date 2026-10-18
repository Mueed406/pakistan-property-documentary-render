"""Install hash-verified official Sketchfab 1.8.0 into THIS Blender user profile.

Run only with Blender Python:
blender --background --python install_sketchfab_blender.py -- --zip FILE.zip

Only installs / enables the verified official addon, no credentials. Requires
an authorized user invocation; NEVER auto-run from checking out repository.
"""
import bpy
import addon_utils
import hashlib
import argparse
import sys
import zipfile
from pathlib import Path, PurePosixPath

argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
parser=argparse.ArgumentParser()
parser.add_argument("--zip",required=True)
args=parser.parse_args(argv)
path=Path(args.zip).expanduser().resolve()
sha=hashlib.sha256(path.read_bytes()).hexdigest()
expected="a6be9e8348a67b66faa236c7aba4c4980db0bda76ab5db17eddd077f66ca71d7"
if sha!=expected:
    raise RuntimeError("Official Sketchfab ZIP SHA256 MISMATCH; refusing to execute")
with zipfile.ZipFile(path) as archive:
    names=archive.namelist()
    if any(PurePosixPath(n).is_absolute() or ".." in PurePosixPath(n).parts for n in names):
        raise RuntimeError("Unsafe ZIP paths")
    if not any(n.endswith("/__init__.py") for n in names):
        raise RuntimeError("Invalid Blender add-on ZIP")
before={m.__name__ for m in addon_utils.modules(refresh=True)}
print("SKETCHFAB_OFFICIAL_ZIP_SHA256_OK",sha)
try:
    bpy.ops.preferences.addon_install(filepath=str(path),overwrite=True)
except Exception as exc:
    raise RuntimeError("Blender add-on installation failed; try the official Edit > Preferences > Install from Disk flow") from exc

after=addon_utils.modules(refresh=True)
candidates=[]
for mod in after:
    name=mod.__name__
    descriptor=getattr(mod,"bl_info",{}) or {}
    title=str(descriptor.get("name",""))
    if "sketchfab" in name.lower() or "sketchfab" in title.lower():
        candidates.append(name)
if not candidates:
    raise RuntimeError("ZIP installed but Sketchfab module was not detected. Check Blender Add-ons UI.")
selected=next((n for n in candidates if n not in before),candidates[-1])
print("SKETCHFAB_MODULE_FOUND",selected)
try:
    bpy.ops.preferences.addon_enable(module=selected)
except Exception as exc:
    raise RuntimeError("Sketchfab module installed but could not be enabled; check addon compatibility and dependencies") from exc
if selected not in bpy.context.preferences.addons.keys():
    raise RuntimeError("Sketchfab addon enable operation did not persist in Blender preferences")
bpy.ops.wm.save_userpref()
print("SKETCHFAB_ADDON_ENABLED_AND_SAVED",selected)
print("SKETCHFAB_ACCOUNT_LOGIN_STILL_REQUIRED_FROM_BLENDER_UI")
