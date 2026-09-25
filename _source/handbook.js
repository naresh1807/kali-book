'use strict';
const navItems=[...document.querySelectorAll('[data-view]')];
const chapters=[...document.querySelectorAll('.chapter')];
const cards=[...document.querySelectorAll('.card, .concept-depth, .anatomy-study, .protocol-guide, .layer-guide, .iot-guide, .topology-guide, .session-guide, .api-guide, .web-deep-guide, .network-deep-guide, .forensic-guide, .remote-guide, .attack-study, .security-guide, .malware-guide, .android-guide, .soc-guide, .redteam-guide')];
const panels=[...document.querySelectorAll('.bookpanel')];
const search=document.getElementById('search');
const result=document.getElementById('result');
const trackHashes={android:'#android-security',soc:'#soc-lessons',redteam:'#red-team'};
let view=Object.keys(trackHashes).find(k=>trackHashes[k]===location.hash)||'guide';
const index=new Map(cards.map(c=>[c,c.textContent.toLowerCase()]));
const toolProfiles=[...document.querySelectorAll('.tool-profile')];
function normalizeToolQuery(value){return value.toLowerCase().replace(/[^a-z0-9]+/g,' ').trim()}
function renderToolProfiles(query){
 const normalized=normalizeToolQuery(query);let found=0;
 toolProfiles.forEach(profile=>{
  const aliases=profile.dataset.toolAliases.split('|').map(normalizeToolQuery);
  const match=!!normalized&&aliases.some(alias=>(' '+normalized+' ').includes(' '+alias+' ')||(normalized.length>=3&&alias.startsWith(normalized)));
  profile.hidden=!match;if(match)found++;
 });
 document.getElementById('tool-search-results').hidden=found===0;
 return found;
}
function render(){
 const q=search.value.trim().toLowerCase();
 document.body.dataset.bookView=q?'search':view;
 const toolCount=renderToolProfiles(q);
 const isReference=q.length>0||view==='redteam'||view==='soc'||view==='android'||view==='all'||chapters.some(s=>s.dataset.chapter===view);
 panels.forEach(p=>{p.hidden=!(isReference?p.id==='reference':p.id===view)});
 let count=0;
 cards.forEach(c=>{const match=(q.length>0||view==='all'||(view==='redteam'&&c.classList.contains('redteam-guide'))||(view==='soc'&&c.classList.contains('soc-guide'))||(view==='android'&&c.classList.contains('android-guide'))||c.dataset.chapter===view)&&index.get(c).includes(q);c.hidden=!match;if(match)count++});
 chapters.forEach(s=>s.hidden=![...s.querySelectorAll('.card, .concept-depth, .anatomy-study, .protocol-guide, .layer-guide, .iot-guide, .topology-guide, .session-guide, .api-guide, .web-deep-guide, .network-deep-guide, .forensic-guide, .remote-guide, .attack-study, .security-guide, .malware-guide, .android-guide, .soc-guide, .redteam-guide')].some(c=>!c.hidden));
 navItems.forEach(n=>{if(!q&&n.dataset.view===view)n.setAttribute('aria-current','page');else n.removeAttribute('aria-current')});
 document.getElementById('empty').hidden=!isReference||count>0||toolCount>0;
 result.textContent=isReference?`${toolCount?toolCount+' tool guide'+(toolCount===1?'':'s')+' · ':''}${count} of ${cards.length} study entries${q?' · searching all chapters':''}`:'Offline handbook · choose a chapter or start a guided lab';
 document.getElementById('clear').hidden=!q;
}
function selectView(next){view=next;if(trackHashes[next])history.replaceState(null,'',trackHashes[next]);else if(Object.values(trackHashes).includes(location.hash))history.replaceState(null,'',location.pathname+location.search);search.value='';render();window.scrollTo({top:0,behavior:'auto'})}
navItems.forEach(b=>b.addEventListener('click',()=>selectView(b.dataset.view)));
search.addEventListener('input',render);
document.getElementById('clear').addEventListener('click',()=>{search.value='';render();search.focus()});
document.addEventListener('keydown',ev=>{if(ev.key==='/'&&ev.target.tagName!=='INPUT'&&ev.target.tagName!=='TEXTAREA'){ev.preventDefault();search.focus()}if(ev.key==='Escape'&&document.activeElement===search){search.value='';render();search.blur()}});
let toastTimer;
function notify(message){const t=document.getElementById('toast');t.textContent=message;t.hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>t.hidden=true,2600)}
document.addEventListener('click',async ev=>{const button=ev.target.closest('.copy');if(!button)return;const text=button.closest('.terminal').querySelector('code').textContent;try{if(!navigator.clipboard)throw Error('fallback');await navigator.clipboard.writeText(text);notify('Copied. Read it before running in Kali.')}catch{const ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.left='-9999px';document.body.appendChild(ta);ta.select();let ok=false;try{ok=document.execCommand('copy')}catch{}ta.remove();button.focus();notify(ok?'Copied. Read it before running in Kali.':'Copy unavailable: select the command and press Ctrl+C.')}});
let printState=[];
window.addEventListener('beforeprint',()=>{printState=[...document.querySelectorAll('details')].map(d=>[d,d.open]);printState.forEach(([d])=>d.open=true)});
window.addEventListener('afterprint',()=>{printState.forEach(([d,open])=>d.open=open)});
document.getElementById('print').addEventListener('click',()=>window.print());
render();

document.querySelectorAll('[data-lab]').forEach(button=>button.addEventListener('click',()=>{selectView('labs');document.getElementById('lab-'+button.dataset.lab)?.scrollIntoView({behavior:'auto',block:'start'});}));

document.querySelectorAll("[data-study-target]").forEach(button=>button.addEventListener("click",()=>{const target=document.getElementById(button.dataset.studyTarget);if(target){target.setAttribute("tabindex","-1");target.focus({preventScroll:true});target.scrollIntoView({behavior:"auto",block:"start"});}}));

window.addEventListener("hashchange",()=>{const next=Object.keys(trackHashes).find(k=>trackHashes[k]===location.hash);if(next)selectView(next)});
