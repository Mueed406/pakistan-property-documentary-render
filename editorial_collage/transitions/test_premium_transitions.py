import json, tempfile, unittest
from pathlib import Path
import numpy as np
from premium_transitions import MatteFX, STYLES, load_plan, boundaries_from_report

class TransitionTests(unittest.TestCase):
    def test_styles_render_2_distinct_frames_without_clipping(self):
        a=np.zeros((180,320,3),np.uint8);a[:,:,0]=110
        b=np.zeros_like(a);b[:,:,2]=190
        fx=MatteFX(320,180)
        for style in STYLES:
            frame=fx.render(a,b,.5,style,seed=301)
            self.assertEqual(frame.shape,a.shape)
            self.assertTrue(frame.dtype==np.uint8)
            self.assertTrue(np.any(frame!=a),style)
            self.assertTrue(np.any(frame!=b),style)
            self.assertTrue(np.array_equal(fx.render(a,b,0,style),a))
            self.assertTrue(np.array_equal(fx.render(a,b,1,style),b))
    def test_plan_validates_spacing(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'plan.json'
            p.write_text(json.dumps({'transitions':[{'frame':60,'duration_frames':32,'preset':'paper-tear'},{'frame':70,'duration_frames':32,'preset':'ink-print'}]}))
            with self.assertRaises(ValueError):load_plan(p)
            p.write_text(json.dumps({'transitions':[{'frame':60,'duration_frames':32,'preset':'paper-tear'},{'frame':300,'duration_frames':32,'preset':'ink-print'}]}))
            self.assertEqual(len(load_plan(p)),2)
    def test_report_selects_real_cuts_and_restricted_count(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'report.json'
            parts=[]
            for i in range(1,100):parts.append({'kind':'stock' if i%2 else 'collage','start':i*600,'frames':600})
            p.write_text(json.dumps({'parts':parts,'duration_seconds':1100}))
            results=boundaries_from_report(p,max_events=8,min_spacing=14)
            self.assertLessEqual(len(results),8)
            self.assertTrue(all(result['frame']>0 for result in results))
            planpath=Path(d)/'auto_plan.json'
            planpath.write_text(json.dumps({'transitions':results}))
            self.assertEqual(len(load_plan(planpath)),len(results))

if __name__=='__main__':unittest.main()