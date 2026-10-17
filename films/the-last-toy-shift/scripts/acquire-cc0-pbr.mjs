/**
 * PBR maps downloaded only from the OFFICIAL Poly Haven API / asset CDN.
 * Source asset: https://polyhaven.com/a/rusty_metal_sheet (CC0)
 * Author: Amal Kumar. Live API usage attribution: Powered by Poly Haven.
 * Every file MD5 must match the source file record; SHA-256 is written to
 * a machine-readable local manifest. Source binaries are NOT git-committed.
 */
import {createHash} from 'node:crypto';
import {readFileSync,existsSync,mkdirSync,writeFileSync} from 'node:fs';
const slug='rusty_metal_sheet',target='public/assets/pbr';
const req=async url=>{
 const res=await fetch(url,{headers:{'User-Agent':'LastToyShift-NoncommercialFanFilm/0.1 (+https://github.com/Mueed406/pakistan-property-documentary-render)'},signal:AbortSignal.timeout(90000)});
 if(!res.ok)throw new Error('Official API '+res.status+' '+url);
 return res;
};
const sha256=data=>createHash('sha256').update(data).digest('hex');
const md5=data=>createHash('md5').update(data).digest('hex');
const variants=await (await req('https://api.polyhaven.com/files/'+slug)).json();
const meta=await (await req('https://api.polyhaven.com/info/'+slug)).json();
const specs=[['diff','diff'],['nor_gl','nor_gl'],['rough','rough']];
const keys=Object.keys(variants);
mkdirSync(target,{recursive:true});
const manifests=[];
for(const [id,keyHint] of specs){
 let key=keys.find(x=>x.toLowerCase()===keyHint)
       ||keys.find(x=>x.toLowerCase().includes(keyHint));
 if(!key)throw new Error('Requested '+id+' PBR map missing; available='+keys.join(', '));
 const chosen=variants[key]?.['1k'];
 if(!chosen || !chosen.jpg?.url)throw new Error('Official 1k JPEG missing for '+key+' (variants: '+Object.keys(chosen||{}).join(',')+')');
 const record=chosen.jpg;
 const path=target+'/'+slug+'_'+id+'.jpg';
 let data;
 if(existsSync(path) && md5(readFileSync(path))===record.md5) data=readFileSync(path);
 else{
  data=Buffer.from(await (await req(record.url)).arrayBuffer());
  if(md5(data)!==record.md5)throw new Error('File MD5 failed for '+record.url);
  if(record.size && record.size!==data.length)throw new Error('Size mismatch for '+record.url);
  writeFileSync(path,data);
 }
 manifests.push({id,api_key:key,url:record.url,size:data.length,md5:md5(data),sha256:sha256(data),
                copyright:'Amal Kumar / Poly Haven',license:'CC0 1.0',license_url:'https://polyhaven.com/license',local_path:path});
 console.log('PASS',key,id,data.length,'bytes',sha256(data));
}
const registry={source_url:'https://polyhaven.com/a/'+slug,source_api:'https://api.polyhaven.com/files/'+slug,
 license:'CC0-1.0',credit:'Powered by Poly Haven; Rusty Metal Sheet by Amal Kumar',
 acquisition_date:'2026-10-18',provider_meta:{name:meta.name,authors:meta.authors,files_hash:meta.files_hash},files:manifests};
writeFileSync(target+'/CC0_rusty_metal_sheet_asset_manifest.json',JSON.stringify(registry,null,2)+'\n');
