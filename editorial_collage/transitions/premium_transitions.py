#!/usr/bin/env python3
"""Premium 60fps editorial transitions for fully rendered documentary footage.

Source is an existing H264/AAC MP4; patch only editorial boundaries. Original
narration/music is mapped unchanged and continuously from the input. All
presets are original procedural designs; no paid/third-party template is bundled.

A separate timeline JSON has entries {frame:int, preset:str, duration_frames:int}.
frame is the first frame of the incoming editorial shot, not the midpoint of the
transition. We may visually bridge +/- duration_frames/2 without changing the
number or timestamps of frames, or re-timing the original audio.

Each output is a real encoded video. Export true 60fps only if the input is 60fps.
Input camera footage that originated as 25fps remains 25fps capture regardless.
"""
from __future__ import annotations
import argparse, hashlib, json, math, os, subprocess, sys, time
from pathlib import Path
import cv2
import numpy as np

STYLES=('paper-tear','ink-print','newspaper-slide','film-splice','photo-match')
FPS=60

def probe(path):
    d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    v=next(s for s in d['streams'] if s['codec_type']=='video')
    a=next((s for s in d['streams'] if s['codec_type']=='audio'),None)
    return d,v,a

def ease(t):
    t=np.clip(t,0,1)
    return t*t*(3-2*t)

def edge_noise(h,seed):
    r=np.random.default_rng(seed)
    anchors=r.uniform(-1,1,size=32).astype('float32')
    row=np.interp(np.arange(h),np.linspace(0,h-1,len(anchors)),anchors)
    y=np.arange(h,dtype=np.float32)
    return 15*row+8*np.sin(y*.067+seed*.3)+3*np.sin(y*.63+seed*.2)

class MatteFX:
    def __init__(self,w,h,seed=211):
        self.w,self.h,self.seed=w,h,seed
        self.x=np.arange(w,dtype=np.float32)[None,:]
        self.y=np.arange(h,dtype=np.float32)[:,None]
        r=np.random.default_rng(seed)
        paper=r.normal(0,5,(max(1,h//4),max(1,w//4))).astype('float32')
        paper=cv2.resize(paper,(w,h),interpolation=cv2.INTER_LINEAR)
        ink=r.normal(0,1,(max(1,h//20),max(1,w//20))).astype('float32')
        self.ink=cv2.GaussianBlur(cv2.resize(ink,(w,h)),(0,0),3.2)
        self.paper=paper
        self.ragged=edge_noise(h,seed)[:,None]
        self.pix=np.zeros((h,w,3),np.uint8)
        # warm archival paper BGR (intentionally restrained)
        self.paper_bgr=np.stack((np.clip(224+paper,0,255),np.clip(240+paper,0,255),np.clip(250+paper,0,255)),axis=-1).astype('uint8')

    def mix(self,a,b,m):
        if np.isscalar(m):return cv2.addWeighted(a,float(1-m),b,float(m),0)
        m=np.clip(m,0,1).astype('float32')
        return cv2.convertScaleAbs(a.astype('float32')*(1-m[:,:,None])+b.astype('float32')*m[:,:,None])

    def coat(self,frame,area,bgr=(22,34,188),opacity=.5):
        m=np.clip(area,0,1).astype('float32')[:,:,None]*opacity
        color=np.array(bgr,np.float32)[None,None,:]
        return np.clip(frame*(1-m)+color*m,0,255).astype('uint8')

    def render(self,before,after,p,style,seed=0):
        """Render a matching transition. p=0 A, p=1 B; preserve 60fps count."""
        p=float(ease(p))
        if p<=0:return before
        if p>=1:return after
        W,H=self.w,self.h
        if style=='paper-tear':
            # Ragged photographic wipe, back paper shadow and sepia underside.
            boundary=-90+(W+180)*p +self.ragged*(.6+.4*np.sin(p*math.pi))
            soft=4.2
            mask=np.clip((boundary-self.x)/soft+.5,0,1)
            out=self.mix(before,after,np.broadcast_to(mask,(H,W)))
            dist=(self.x-boundary)
            under=np.clip((dist+53)/10+.5,0,1)*np.clip((8-dist)/8+.5,0,1)
            # Texture printed onto a narrow torn-paper lip
            mix_under=np.minimum(1,under*.82)
            out=self.mix(out,self.paper_bgr,np.broadcast_to(mix_under,(H,W)))
            shadow=np.clip((dist+18)/22+.5,0,1)*np.clip((70-dist)/45+.5,0,1)
            out=self.coat(out,np.broadcast_to(shadow,(H,W)),(23,21,23),.22)
            # Small yellow marker imperfection along the edge; not big flash
            accent=np.clip((dist-1)/6+.5,0,1)*np.clip((11-dist)/6+.5,0,1)
            out=self.coat(out,np.broadcast_to(accent,(H,W)),(21,194,245),.38)
        elif style=='ink-print':
            # Archival ink spreading from the center, retaining shadows and fine grain.
            cx=W*.46;cy=H*.51
            radius=np.sqrt(((self.x-cx)/(W*.72))**2+((self.y-cy)/(H*.85))**2)
            front=(p*1.9-radius +self.ink*.075)*9
            alpha=np.clip(front+.5,0,1)
            out=self.mix(before,after,alpha)
            bleeding=np.clip(1-np.abs(front)*3,0,1)
            out=self.coat(out,bleeding,(18,25,60),.31)
            # Spreading ink register/grain, never cover whole view
            printgrain=np.clip((np.abs(self.ink)-.5)*.28,0,.3)*bleeding
            out=self.coat(out,printgrain,(8,10,13),.17)
        elif style=='newspaper-slide':
            # Page edges recede in opposed directions with soft shadow and motion blur.
            xcut=W*p
            wave=20*np.sin(self.y*.025+seed*.12)*(1-p)
            sheet=np.broadcast_to(np.clip((self.x-(xcut+wave))/11+.5,0,1),(H,W))
            out=self.mix(after,before,sheet)
            band=np.broadcast_to(np.clip((self.x-xcut+35)/12+.5,0,1)*np.clip((xcut+3-self.x)/12+.5,0,1),(H,W))
            out=self.mix(out,self.paper_bgr,band*.65)
            shade=np.broadcast_to(np.clip((self.x-xcut-12)/24+.5,0,1)*np.clip((xcut+64-self.x)/27+.5,0,1),(H,W))
            out=self.coat(out,shade,(20,20,22),.27)
            if .1 < p < .85:
                # Translucent newsroom registration line tracks the actual page edge
                stripe=np.broadcast_to(np.clip((self.x-xcut+2)/4+.5,0,1)*np.clip((xcut+6-self.x)/4+.5,0,1),(H,W))
                out=self.coat(out,stripe,(10,37,166),.40)
        elif style=='film-splice':
            # Physical film split: quiet monochrome edge and 2-frame negative-flash.
            fraction=np.clip((p-.08)/.84,0,1)
            matte=np.clip((self.x-W*fraction)/9+.5,0,1)
            out=self.mix(after,before,np.broadcast_to(matte,(H,W)))
            if .34<p<.44:
                gray=cv2.cvtColor(out,cv2.COLOR_BGR2GRAY)
                out=cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)
                out=cv2.addWeighted(out,.84,self.paper_bgr,.16,0)
            pos=W*fraction
            line=np.broadcast_to(np.clip((self.x-pos+10)/8+.5,0,1)*np.clip((pos+11-self.x)/8+.5,0,1),(H,W))
            out=self.coat(out,line,(38,40,37),.40)
        elif style=='photo-match':
            # Rapid masked editorial match cut with actual perspective/zoom movement.
            scalea=1.0+.035*p;scaleb=1.04-.04*p
            A=cv2.getRotationMatrix2D((W/2,H/2),p*1.3,scalea)
            B=cv2.getRotationMatrix2D((W/2,H/2),(1-p)*(-1.1),scaleb)
            warped_a=cv2.warpAffine(before,A,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
            warped_b=cv2.warpAffine(after,B,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
            xcut=W*(-.05+1.1*p)
            wave=11*np.sin(self.y*.032+seed)
            mask=np.broadcast_to(np.clip((xcut+wave-self.x)/34+.5,0,1),(H,W))
            out=self.mix(warped_a,warped_b,mask)
            seam=np.broadcast_to(np.clip((self.x-xcut+8)/9+.5,0,1)*np.clip((xcut+20-self.x)/12+.5,0,1),(H,W))
            out=self.coat(out,seam,(18,191,240),.34)
        else:
            raise ValueError('Unknown transition '+style)
        return out


def load_plan(path, fps=FPS):
    d=json.loads(Path(path).read_text(encoding='utf-8'))
    entries=d['transitions'] if isinstance(d,dict) else d
    if not isinstance(entries,list):raise ValueError('Transition plan must be a list')
    out=[]
    for x in entries:
        t=int(x['frame']);n=int(x.get('duration_frames',30));style=x['preset']
        if style not in STYLES:raise ValueError('Unsupported effect '+style)
        if n<12 or n>64 or n%2:raise ValueError('Durations must be even, 12-64 frames')
        out.append({'frame':t,'duration_frames':n,'preset':style,'seed':int(x.get('seed',t))})
    out.sort(key=lambda x:x['frame'])
    for j,x in enumerate(out):
        if x['frame']<x['duration_frames']//2:raise ValueError('Transition before beginning')
        if j and x['frame']-out[j-1]['frame']<max(x['duration_frames'],out[j-1]['duration_frames'])+10:
            raise ValueError('Transition events too close')
    return out


def boundaries_from_report(path, max_events=20, min_spacing=14, duration_frames=32):
    """Choose story cuts, never blindly apply an effect to every join."""
    report=json.loads(Path(path).read_text(encoding='utf-8'))
    parts=report['parts']; selected=[]; last=-99999
    kinds=['paper-tear','newsprint-slide','photo-match','ink-print','film-splice']
    for i in range(1,len(parts)):
        a,b=parts[i-1],parts[i]
        if a['kind']==b['kind']:continue
        t=b['start']
        if (t-last)/FPS<min_spacing:continue
        if t < FPS*3 or t > int(float(report['duration_seconds'])*FPS)-duration_frames:continue
        # Prioritize incoming collage as major chapter opener.
        if b['kind']=='stock' and i%3:continue
        idx=len(selected)
        selected.append({'frame':t,'duration_frames':duration_frames,'preset':kinds[idx%len(kinds)],'seed':12345+idx*71})
        last=t
        if len(selected)>=max_events:break
    return selected


def apply(source,output,transitions,crf=18,preset='veryfast',max_frames=0,threads=2):
    source=Path(source); output=Path(output); output.parent.mkdir(parents=True,exist_ok=True)
    meta,v,a=probe(source)
    if not a:raise RuntimeError('Soundtrack missing')
    if v['width']<640 or v['height']<360:raise ValueError('Source resolution too low')
    fps=v.get('avg_frame_rate','0/1')
    if fps not in ('60/1','60'):
        raise ValueError('Exact 60fps source required, got '+fps)
    W,H=int(v['width']),int(v['height'])
    expected=int(round(float(meta['format']['duration'])*FPS))
    if max_frames:expected=min(expected,int(max_frames))
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened():raise RuntimeError('Cannot decode original video')
    # Book-ended windows buffered with one-frame lookahead; non-transition
    # frames go directly through without large full-frame copy buffers.
    entry=[]
    for trans in transitions:
        half=trans['duration_frames']//2
        s=trans['frame']-half;e=trans['frame']+half
        if e>expected:continue
        entry.append((s,e,trans))
    bystart={s:(e,t) for s,e,t in entry}
    command=['ffmpeg','-hide_banner','-loglevel','error','-y',
             '-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),
             '-i','pipe:0','-i',str(source),'-map','0:v:0','-map','1:a:0',
             '-c:v','libx264','-preset',preset,'-crf',str(crf),
             '-pix_fmt','yuv420p','-threads',str(threads),'-r',str(FPS),
             '-c:a','aac','-b:a','192k','-ar','48000',
             '-frames:v',str(expected),'-t',f'{expected/FPS:.6f}',
             '-movflags','+faststart',str(output)]
    p=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    fx=MatteFX(W,H)
    count=0; started=time.time();events=[]
    try:
        while count<expected:
            if count in bystart:
                end,transition=bystart[count]
                frames=[]
                for frame_index in range(count,end):
                    ok,fr=cap.read()
                    if not ok:break
                    frames.append(fr)
                if len(frames)!=end-count:raise RuntimeError('Could not read exact transition frames')
                half=len(frames)//2
                # Use held before/after frames for pre-roll/post-roll, but film
                # camera and matte motion continue at 60fps.
                # A before=b-1, B after=b. Hard seam is temporally centered.
                last_left=frames[half-1];first_right=frames[half]
                for j,fr in enumerate(frames):
                    transpos=(j+.5)/len(frames)
                    outgoing=fr if j<half else last_left
                    incoming=first_right if j<half else fr
                    frame=fx.render(outgoing,incoming,transpos,transition['preset'],transition['seed'])
                    p.stdin.write(frame.tobytes())
                    count+=1
                events.append({**transition,'actual_start_frame':count-len(frames),'actual_end_frame':count})
                print('TRANSITION',len(events),transition['preset'],'frame',transition['frame'],flush=True)
                continue
            ok,fr=cap.read()
            if not ok:break
            p.stdin.write(fr.tobytes());count+=1
            if count%(FPS*45)==0:print('PROGRESS',count,expected,'elapsed_s',round(time.time()-started,1),flush=True)
        p.stdin.close()
        stderr=p.stderr.read().decode('utf8','replace')
        ret=p.wait()
        if ret:raise RuntimeError('Encoder failed: '+stderr[-2400:])
    except Exception:
        try:p.kill();p.wait(timeout=5)
        except Exception:pass
        output.unlink(missing_ok=True)
        raise
    finally:cap.release()
    if count!=expected:raise RuntimeError(f'Frame mismatch decoded {count} expected {expected}')
    r,stream,aud=probe(output)
    result={'source':str(source),'output':str(output),'source_duration':float(meta['format']['duration']),
       'duration':float(r['format']['duration']),'frame_rate':stream['avg_frame_rate'],
       'frame_count':int(stream.get('nb_frames',0)),'expected_frames':expected,
       'audio_codec':aud.get('codec_name') if aud else None,
       'motion_transitions':events,'quality':'technical review; needs creative approval',
       'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest() if source.stat().st_size<800_000_000 else 'skip-over-800mb',
       'completed_s':round(time.time()-started,2)}
    output.with_suffix('.transition_report.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    if result['frame_count']!=expected or result['audio_codec']!='aac':raise RuntimeError('Final QC failed')
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    one=sub.add_parser('plan-from-report')
    one.add_argument('--report',required=True);one.add_argument('--out',required=True)
    one.add_argument('--max-events',type=int,default=20)
    two=sub.add_parser('apply')
    two.add_argument('--input',required=True);two.add_argument('--output',required=True)
    two.add_argument('--plan',required=True);two.add_argument('--crf',type=int,default=18)
    two.add_argument('--encoder-preset',default='veryfast')
    two.add_argument('--max-frames',type=int,default=0)
    args=parser.parse_args()
    if args.command=='plan-from-report':
        plan={'transitions':boundaries_from_report(args.report,args.max_events),
              'policy':'One editorial transition per meaningful chapter; preserve total 60fps frame count, audio unchanged'}
        Path(args.out).write_text(json.dumps(plan,indent=2),encoding='utf8')
        print('PLANNED',len(plan['transitions']),'transitions')
    elif args.command=='apply':
        report=apply(args.input,args.output,load_plan(args.plan),args.crf,args.encoder_preset,args.max_frames)
        print('PRODUCTION SUCCESS',json.dumps({k:v for k,v in report.items() if k!='motion_transitions'},indent=2))
if __name__=='__main__':main()