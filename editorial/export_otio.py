#!/usr/bin/env python3
"""Export real shot decisions to professional OpenTimelineIO JSON (OTIO).

This enables reuse in editor applications supporting OTIO or its optional
AAF/FCP XML adapters. Does not misrepresent OTIO as preserving custom FFmpeg
color/transitions/effects; those require an editorial finishing pass.
"""
import argparse,json
from pathlib import Path

def build(source,target,fps=25):
 import opentimelineio as otio
 shots=json.loads(Path(source).read_text(encoding="utf8-sig"))
 if isinstance(shots,dict):shots=[shots]
 if not isinstance(shots,list):raise ValueError("Expected JSON list of shots or one shot object")
 if not shots:raise RuntimeError("No edit decisions")
 timeline=otio.schema.Timeline(name="Pakistan Property Group Documentary / Picture Edit")
 track=otio.schema.Track(name="Real Stock Footage",kind=otio.schema.TrackKind.Video)
 timeline.tracks.append(track)
 for i,item in enumerate(shots):
  path=Path(item["source"]).resolve()
  if not path.is_file():raise FileNotFoundError("Missing footage: "+str(path))
  begin=float(item["start"]);duration=float(item["duration"])
  if duration<=0 or begin<0:raise ValueError("Invalid shot duration/start")
  clip=otio.schema.Clip(name=str(item.get("description",item.get("id",i))))
  clip.media_reference=otio.schema.ExternalReference(target_url=path.as_uri())
  clip.source_range=otio.opentime.TimeRange(
   start_time=otio.opentime.RationalTime(round(begin*fps),fps),
   duration=otio.opentime.RationalTime(round(duration*fps),fps))
  clip.metadata["source_id"]=item.get("id")
  clip.metadata["story_act"]=item.get("category")
  clip.metadata["documentary_note"]="Footage is illustrative; provenance in stock manifest"
  track.append(clip)
 target=Path(target);target.parent.mkdir(parents=True,exist_ok=True)
 otio.adapters.write_to_file(timeline,str(target))
 print("EXPORTED",len(shots),"editable OTIO shots:",target)
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--decisions",required=True)
 p.add_argument("--out",default="renders/pakistan_property_timeline.otio")
 a=p.parse_args();build(a.decisions,a.out)
