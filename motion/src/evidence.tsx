import React from 'react';
import {AbsoluteFill,OffthreadVideo,staticFile,interpolate,spring,useCurrentFrame,useVideoConfig} from 'remotion';
type Props={backgroundVideo:string;files:number;plots:number};
const calm='Noto Naskh Arabic, Segoe UI, Arial, sans-serif';
export const EvidenceMotion:React.FC<Props>=({backgroundVideo,files,plots})=>{
 const f=useCurrentFrame();const {fps}=useVideoConfig();
 const enter=spring({frame:f,fps,config:{damping:22,stiffness:95}});
 const count=interpolate(f,[33,131],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
 const pan=interpolate(f,[0,210],[-60,65]);
 const lots=Array.from({length:96},(_,i)=>{
  const x=i%12,y=Math.floor(i/12),ok=(i*17+13)%9===0;
  const show=interpolate(f,[12+i%15*2,43+i%15*2],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  return <div key={i} style={{position:'absolute',left:x*58,top:y*55,width:52,height:45,opacity:show,
    background:ok?'rgba(52,207,215,.22)':'rgba(225,227,228,.035)',
    border:'1.5px solid '+(ok?'#6DEAE4':'rgba(220,220,215,.36)'),
    boxShadow:ok?'0 0 18px rgba(52,220,214,.37)':'none',
    transform:'translateZ('+(ok?18:0)+'px)'}}/>;
 });
 return <AbsoluteFill style={{background:'#09131d',color:'#fff',fontFamily:calm}}>
  {backgroundVideo?<OffthreadVideo src={backgroundVideo.startsWith('http')?backgroundVideo:staticFile(backgroundVideo)} muted style={{width:'100%',height:'100%',objectFit:'cover',filter:'brightness(.55) saturate(.88) contrast(1.07)'}}/>:
  <AbsoluteFill style={{background:'radial-gradient(ellipse at 69% 50%,#294552 0,#0b1824 56%,#070e16 100%)'}}/>}
  <AbsoluteFill style={{background:'linear-gradient(90deg,rgba(6,12,18,.88),rgba(6,12,18,.19) 74%,rgba(3,6,9,.25))'}}/>
  <div style={{position:'absolute',top:72,left:100,color:'#8BCED5',fontSize:21,letterSpacing:6,fontFamily:'Arial,sans-serif',opacity:enter}}>PAKISTAN PROPERTY GROUP  •  INVESTIGATION</div>
  <div style={{position:'absolute',top:175,left:108,width:840,textAlign:'right',direction:'rtl',fontSize:71,fontWeight:800,textShadow:'0 7px 30px #000',transform:'translateY('+((1-enter)*55)+'px)',opacity:enter}}>
    فائل موجود ہے، زمین کہاں ہے؟
  </div>
  <div style={{position:'absolute',left:110,top:365,display:'flex',gap:50,fontFamily:'Arial,sans-serif',opacity:count}}>
    <div><div style={{fontSize:24,color:'#abc8ce'}}>REPORTED FILES</div><div style={{fontSize:98,color:'#E7B97F',fontWeight:800}}>{Math.round(count*files).toLocaleString('en-US')}</div></div>
    <div style={{borderLeft:'2px solid rgba(235,235,235,.3)',paddingLeft:42}}><div style={{fontSize:24,color:'#abc8ce'}}>PLOT CAPACITY</div><div style={{fontSize:98,color:'#65DBD7',fontWeight:800}}>{Math.round(count*plots).toLocaleString('en-US')}</div></div>
  </div>
  <div style={{position:'absolute',right:-60,top:270,width:740,height:540,transform:'perspective(1000px) rotateX(54deg) rotateZ(-26deg) translateX('+pan+'px)',transformStyle:'preserve-3d',filter:'drop-shadow(10px 24px 35px black)'}}>{lots}</div>
  <div style={{position:'absolute',left:112,top:613,fontSize:36,width:890,textAlign:'right',direction:'rtl',opacity:enter,lineHeight:1.6}}>
    یہ اعداد تحقیقاتی رپورٹ میں بیان کیے گئے الزامات ہیں۔
  </div>
  <div style={{position:'absolute',bottom:74,left:112,right:120,borderTop:'1px solid rgba(255,255,255,.23)',paddingTop:18,fontSize:23,fontFamily:'Arial,sans-serif',color:'#C9DDD9',opacity:enter}}>
    ILLUSTRATIVE EXPLANATION  •  NOT A COURT FINDING
  </div>
 </AbsoluteFill>;
};
