#!/usr/bin/env python3
"""Match paid-free creator MOV animations ONLY to source-SRT aligned collage chapters."""
import argparse,json,pathlib,sys

TARGETS=[
 ("42,000","Burst Circle.mov","red"),
 ("6,000","Arrow Side.mov","gold"),
 ("36,000","Burst Circle.mov","red"),
 ("PAPER RECORDS","Curly Arrow 2.mov","charcoal"),
 ("OWNERSHIP","Curly Arrow 3.mov","red"),
 ("REGISTRATION","Curly Arrow 2.mov","gold"),
 ("STEP 01","Check Mark.mov","red"),
 ("STEP 02","Check Mark.mov","gold"),
 ("STEP 03","Check Mark.mov","red"),
 ("STEP 04","Check Mark.mov","gold"),
 ("PRESERVE","Curly Arrow 4.mov","red"),
 ("VERIFY","Arrow Side.mov","charcoal")
]
def main():
 p=argparse.ArgumentParser();p.add_argument("--report",required=True);p.add_argument("--output",required=True);a=p.parse_args()
 report=json.loads(pathlib.Path(a.report).read_text())
 parts=report["parts"];events=[];used=set()
 for title,source,color in TARGETS:
  candidates=[q for q in parts if q.get("kind")=="collage" and title in q.get("theme","").upper()
              and int(q["start"]) not in used and int(q["frames"])>=90]
  if not candidates:
   print("Not found — optional cue:",title,file=sys.stderr)
   continue
  q=candidates[0];start=int(q["start"]);used.add(start)
  frame=start+min(int(q["frames"]*.31),int(q["frames"])-72)
  n=sum(1 for c in parts if c["kind"]=="collage" and int(c["start"])<start)
  title_left=n%8 not in (1,3,6)
  x=.30 if title_left else .54
  y=.39 if title.startswith("STEP ") else .27
  e={"file":source,"at":round(frame/60,3),"duration":1.1,
     "x":x,"y":y,"scale":.13,
     "opacity":.43 if "Burst" in source else .55,
     "color":color,"context":q["theme"],"chapter_frame":start}
  events.append(e)
 events.sort(key=lambda e:e["at"])
 if len(events)<8:raise RuntimeError(f"Too few source-aligned scenes: {len(events)}")
 pathlib.Path(a.output).write_text(json.dumps({"events":events,"policy":"collage scenes only"},indent=2)+"\n")
 print("SOURCE-LINKED CREATOR ANIMATION INSERTS:",len(events))
 for e in events:print(e["context"],e["at"],e["file"])
if __name__=="__main__":main()
