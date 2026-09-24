'use strict';
const navItems=[...document.querySelectorAll('[data-view]')];
const chapters=[...document.querySelectorAll('.chapter')];
const cards=[...document.querySelectorAll('.card, .concept-depth, .anatomy-study, .protocol-guide, .layer-guide, .iot-guide, .topology-guide, .session-guide, .api-guide, .web-deep-guide, .network-deep-guide, .forensic-guide, .remote-guide, .attack-study, .security-guide')];
const panels=[...document.querySelectorAll('.bookpanel')];
const search=document.getElementById('search');
const result=document.getElementById('result');
let view='guide';
const index=new Map(cards.map(c=>[c,c.textContent.toLowerCase()]));
function render(){
 const q=search.value.trim().toLowerCase();
 const isReference=q.length>0||view==='all'||chapters.some(s=>s.dataset.chapter===view);
 panels.forEach(p=>{p.hidden=!(isReference?p.id==='reference':p.id===view)});
 let count=0;
 cards.forEach(c=>{const match=(q.length>0||view==='all'||c.dataset.chapter===view)&&index.get(c).includes(q);c.hidden=!match;if(match)count++});
 chapters.forEach(s=>s.hidden=![...s.querySelectorAll('.card, .concept-depth, .anatomy-study, .protocol-guide, .layer-guide, .iot-guide, .topology-guide, .session-guide, .api-guide, .web-deep-guide, .network-deep-guide, .forensic-guide, .remote-guide, .attack-study, .security-guide')].some(c=>!c.hidden));
 navItems.forEach(n=>{if(!q&&n.dataset.view===view)n.setAttribute('aria-current','page');else n.removeAttribute('aria-current')});
 document.getElementById('empty').hidden=!isReference||count>0;
 result.textContent=isReference?`${count} of ${cards.length} study entries${q?' · searching all chapters':''}`:'Offline handbook · choose a chapter or start a guided lab';
 document.getElementById('clear').hidden=!q;
}
function selectView(next){view=next;search.value='';render();window.scrollTo({top:0,behavior:'auto'})}
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
