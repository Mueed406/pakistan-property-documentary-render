"""Offline contract checks; zero Gemini API requests."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from gemini_tts_lab import PASSAGE,prompt,payload,save_response
class TestGeminiUrdu(unittest.TestCase):
 def test_urdu_caveats(self):
  self.assertIn("بیالیس ہزار",PASSAGE)
  self.assertIn("حتمی فیصلہ نہیں",PASSAGE)
 def test_preserves_passage(self):
  self.assertEqual(prompt("Charon").count(PASSAGE),1)
  self.assertIn("VERBATIM",prompt("Schedar"))
 def test_api_payload(self):
  p=payload("Charon")
  self.assertEqual(p["generationConfig"]["responseModalities"],["AUDIO"])
  self.assertEqual(p["generationConfig"]["speechConfig"]["voiceConfig"]["prebuiltVoiceConfig"]["voiceName"],"Charon")
 def test_reject_wrong_voice(self):
  with self.assertRaises(ValueError):prompt("Unapproved")
 def test_fail_closed_missing_audio(self):
  with self.assertRaises(ValueError):save_response({"candidates":[{"content":{"parts":[{"text":"nothing"}]}}]},Path("/tmp/never_created.wav"))
if __name__=="__main__":unittest.main()
