// Render our local token specimens. No upstream scripts, APIs, or remote resources are executed.
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {pathToFileURL} from "node:url";
import {spawn} from "node:child_process";

const queue = JSON.parse(fs.readFileSync(process.argv[2], "utf8")).previews;
const profile = fs.mkdtempSync(path.join(os.tmpdir(), "figcraft-collection-render-"));
const port = 10000 + Math.floor(Math.random() * 1000);
const chrome = spawn(process.env.CHROMIUM || "chromium", ["--headless=new", `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`, "--no-first-run", "about:blank"], {stdio:"ignore"});
const delay = ms => new Promise(r => setTimeout(r, ms));
let ws;
try {
  let targets;
  for (let i=0; i<100 && !targets; i++) {
    await delay(100);
    targets = await fetch(`http://127.0.0.1:${port}/json`).then(r=>r.json()).catch(()=>null);
  }
  if (!targets) throw new Error("Chromium did not start");
  ws = new WebSocket(targets.find(t=>t.type==="page").webSocketDebuggerUrl);
  await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject;});
  let id=0;
  const pending = new Map();
  ws.onmessage = ({data}) => {const message=JSON.parse(data), entry=pending.get(message.id); if(entry){pending.delete(message.id);message.error?entry.reject(new Error(JSON.stringify(message.error))):entry.resolve(message.result);}};
  const send = (method,params={}) => new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});ws.send(JSON.stringify({id:n,method,params}));});
  await send("Page.enable");
  await send("Emulation.setDeviceMetricsOverride", {width:1080,height:720,deviceScaleFactor:1,mobile:false});
  await send("Network.enable");
  await send("Network.setBlockedURLs", {urls:["http://*","https://*"]});
  for (let i=0; i<queue.length; i++) {
    const job=queue[i];
    if (!job.html.endsWith(".html") || !job.image.endsWith(".webp")) throw new Error("Unexpected preview path");
    const url=pathToFileURL(job.html).href;
    await send("Page.navigate",{url});
    let loaded = false;
    for (let attempt=0; attempt<100 && !loaded; attempt++) {
      const status=await send("Runtime.evaluate",{expression:`location.href === ${JSON.stringify(url)} && document.readyState === 'complete'`,returnByValue:true});
      loaded=!!status.result?.value;
      if (!loaded) await delay(50);
    }
    if (!loaded) throw new Error("Preview did not load: "+job.html);
    const ready = await send("Runtime.evaluate",{expression:"document.fonts.ready.then(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(() => r(true)))))",awaitPromise:true,returnByValue:true});
    if (ready.exceptionDetails) throw new Error("Preview failed: "+job.html);
    const check = job.kind === "design-system"
      ? "document.documentElement.scrollWidth <= 1080 && document.documentElement.scrollHeight <= 720 && document.querySelectorAll('[data-component]').length >= 6 && [...document.querySelectorAll('[data-component],footer')].every(el => {const r=el.getBoundingClientRect();return r.width>0 && r.height>0 && r.right<=1080 && r.bottom<=720;}) && document.fonts.check('14px Specimen')"
      : "document.documentElement.scrollWidth <= 1080 && document.querySelector('footer').getBoundingClientRect().bottom <= 720 && getComputedStyle(document.querySelector('.metric')).fontSize === '46px' && getComputedStyle(document.querySelector('.bar')).height === '105px'";
    const layout = await send("Runtime.evaluate", {expression:check,returnByValue:true});
    if (!layout.result?.value) throw new Error("Broken preview layout: " + job.html);
    const screenshot = await send("Page.captureScreenshot",{format:"webp",quality:90});
    fs.writeFileSync(job.image,Buffer.from(screenshot.data,"base64"));
    if ((i+1)%20===0 || i===queue.length-1) console.log(`${i+1}/${queue.length} rendered`);
  }
} finally {
  ws?.close();
  const gone=new Promise(resolve=>chrome.once("exit",resolve));
  chrome.kill();await gone;
  fs.rmSync(profile,{recursive:true,force:true,maxRetries:5,retryDelay:100});
}
