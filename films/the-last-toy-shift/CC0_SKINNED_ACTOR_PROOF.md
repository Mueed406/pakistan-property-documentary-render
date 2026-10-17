# A genuinely skinned actor — technical proof only

Source: official Three.js examples, `RobotExpressive.glb` by Tomás Laulhé; edits by Don McCurdy. The project's [official README](https://github.com/mrdoob/three.js/blob/dev/examples/models/gltf/RobotExpressive/README.md) declares **CC0 1.0**.

Pinned source commit: [`eba30de865cfbf31ac736f792defd9a60ff28d57`](https://github.com/mrdoob/three.js/tree/eba30de865cfbf31ac736f792defd9a60ff28d57)

Pinned raw SHA-256: `047f5e5fb3bb6d378bd1df16ca6137f2a596c99b3a1b5690b4020c05aaf6f319`. Size reported by source: 463,988 bytes.

To acquire and verify (actual networking and checks required):
```bash
cd films/the-last-toy-shift
node scripts/acquire-cc0-rig.mjs
npm run render -- --mode=rigproof --start=1800 --end=2040 --width=360 --height=640
```

This runs a real skeletal `SkinnedMesh` with an embedded `Running` animation in the same shared factory camera space. It replaces a segmented primitive with a **genuine weighted skeletal GLB only for technical validation**, not with the final plush horror character. It cannot clear `RIGHTS_GATE.json`, isn't a Huggy Wuggy asset, and should never be promoted as a finished trailer or impersonation of Mob Entertainment.

Do not change final release authorization or the canonical 11-shot manifest based on this proof. No scraped gameplay or proprietary voices have been downloaded. The real artistic creature must still be designed and legally cleared, its actual mesh/rig verified and shot geography blocked around its scale.
