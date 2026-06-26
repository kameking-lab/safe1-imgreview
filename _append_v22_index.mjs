// append a row to gen_event_v22/event_index_v22.csv (append-only, non-destructive)
// usage: node _append_v22_index.mjs <num> <type> <posture> <arrow> <g1> <g2>
import fs from "node:fs";
import path from "node:path";
const BASE="C:/Users/kanet/20260522/safe1";
const [num,type,posture,arrow,g1,g2]=process.argv.slice(2);
const csv=path.join(BASE,"gen_event_v22","event_index_v22.csv");
const header="元番号,元の事故の型,危険姿勢の内容,矢印が示す事故への流れ,google_1,google_2\n";
function parseLine(line){const o=[];let c="",q=false;for(let i=0;i<line.length;i++){const ch=line[i];
  if(q){if(ch==='"'){if(line[i+1]==='"'){c+='"';i++;}else q=false;}else c+=ch;}
  else{if(ch===','){o.push(c);c="";}else if(ch==='"'){q=true;}else c+=ch;}}o.push(c);return o;}
if(!fs.existsSync(csv))fs.writeFileSync(csv,header);
const existing=fs.readFileSync(csv,"utf8").split(/\r?\n/).some(l=>parseLine(l)[0]===String(num));
if(existing){console.log("index row already exists for",num,"- skip");process.exit(0);}
const esc=s=>`"${String(s).replace(/"/g,'""')}"`;
fs.appendFileSync(csv,[num,type,posture,arrow,g1,g2].map(esc).join(",")+"\n");
console.log("index appended for",num);
