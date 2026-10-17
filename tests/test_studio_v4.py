"""Regression tests for autonomous studio v4, no network or paid services."""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from production import studio_pipeline as sp
from production import youtube_private_upload as yu


class StudioV4Tests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder=Path(self.temp.name)/"film-project"
        args=["init","--project",str(self.folder),"--title","Verified 6m Movie","--minutes","6"]
        self.assertEqual(sp.main(args),0)
        self.spec=json.loads((self.folder/"project.json").read_text(encoding="utf8"))

    def test_defaults_safe_and_distinct_durations(self):
        self.assertEqual(self.spec["duration_seconds"],360)
        self.assertEqual(self.spec["fps"],60)
        self.assertEqual(self.spec["production_mode"],"free")
        self.assertFalse(self.spec["youtube"]["auto_publish"])
        self.assertFalse(self.spec["premium_generation_allowed"])
        self.assertEqual(self.spec["youtube"]["visibility"],"private")
        self.assertFalse((self.folder/"output"/"full.mp4").exists())
        for minutes in (5,9):
            path=Path(self.temp.name)/("length-"+str(minutes))
            code=sp.main(["init","--project",str(path),"--title","Another Subject",
                          "--minutes",str(minutes)])
            self.assertEqual(code,0)
            data=json.loads((path/"project.json").read_text())
            self.assertEqual(data["duration_seconds"],minutes*60)
            self.assertEqual(data["inputs"]["scene_plan"],"storyboard.json")

    def test_deny_unapproved_inputs(self):
        self.assertEqual(sp.main(["preflight","--project",str(self.folder)]),2)
        report=json.loads((self.folder/"output"/"preflight.json").read_text())
        self.assertFalse(report["ready"])
        self.assertTrue(any("narration" in s for s in report["errors"]))
        self.assertEqual(sp.main(["package","--project",str(self.folder),
                                  "--video",str(self.folder/"missing.mp4")]),2)

    def test_cache_changes_with_input(self):
        infile=self.folder/"story.txt"
        infile.write_text("first")
        first=sp.fingerprint([infile],{"fps":60})
        self.assertEqual(first,sp.fingerprint([infile],{"fps":60}))
        self.assertNotEqual(first,sp.fingerprint([infile],{"fps":30}))
        infile.write_text("second")
        self.assertNotEqual(first,sp.fingerprint([infile],{"fps":60}))

    def test_rights_manifest_required_fields(self):
        self.assertTrue(sp.audit_rights({"assets":[]}))
        self.assertTrue(sp.audit_rights({"assets":[{"path":"img.png"}]}))
        full={"path":"img.png","source_url":"https://example.com/image",
              "license":"CC0","sha256":"abc","usage":"illustrative"}
        self.assertFalse(sp.audit_rights({"assets":[full]}))
        full["usage"]="actual-investigation-evidence"
        self.assertTrue(sp.audit_rights({"assets":[full]}))

    def test_video_metadata_qc(self):
        video=self.folder/"valid.mp4"; video.write_bytes(b"x"*8192)
        fake={"streams":[
          {"codec_type":"video","codec_name":"h264","width":1920,"height":1080,
           "avg_frame_rate":"60/1","nb_frames":"21600"},
          {"codec_type":"audio","codec_name":"aac"}],
          "format":{"duration":"360.000"}}
        with patch.object(sp,"ffprobe",return_value=fake):
            report=sp.validate_video(video,self.spec)
            self.assertTrue(report["passed"])
            fake["streams"][0]["avg_frame_rate"]="25/1"
            report=sp.validate_video(video,self.spec)
            self.assertFalse(report["passed"])
            self.assertTrue(any("FPS" in i for i in report["issues"]))

    def test_no_youtube_upload_without_explicit_approval(self):
        f=self.folder/"film.mp4";f.write_bytes(b"x"*800000)
        manifest={"video_path":str(f),"channel_id":"UCdQu7MU5dHhaClhkCdG2BKg",
                  "privacyStatus":"private","title":"Title",
                  "description":"Source-cited description", "made_for_kids":False,
                  "approved_for_publish":False}
        path=self.folder/"manifest.json";path.write_text(json.dumps(manifest))
        with self.assertRaises(SystemExit):
            yu.main(["--manifest",str(path),"--channel-id",
                     "UCdQu7MU5dHhaClhkCdG2BKg","--execute"])
        manifest["approved_for_publish"]=True
        path.write_text(json.dumps(manifest))
        self.assertEqual(yu.main(["--manifest",str(path),"--channel-id",
                                  "UCdQu7MU5dHhaClhkCdG2BKg"]),0)
        # Explicit --execute without required secrets must stop before API SDK import.
        with patch.dict("os.environ",{},clear=True):
            with self.assertRaises(SystemExit):
                yu.main(["--manifest",str(path),"--channel-id",
                         "UCdQu7MU5dHhaClhkCdG2BKg","--execute"])
        self.assertFalse((self.folder/"youtube_private_upload_receipt.json").exists())


if __name__=="__main__":
    unittest.main()
