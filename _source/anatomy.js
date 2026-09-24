(() => {
 'use strict';
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const all=[];
 document.querySelectorAll('[data-anatomy]').forEach(figure=>{
  const parts=[...figure.querySelectorAll('.an-part')];
  const choices=[...figure.querySelectorAll('.an-choice')];
  const info=[...figure.querySelectorAll('.an-info')];
  const play=figure.querySelector('[data-an-action="play"]');
  const status=figure.querySelector('.an-status');
  let current=0,timer=null;
  const visible=()=>!document.hidden&&!figure.closest('[hidden]');
  function pause(){if(timer!==null)clearInterval(timer);timer=null;figure.classList.remove('is-touring');play.textContent='Play guided tour';play.setAttribute('aria-pressed','false');}
  function select(n){current=n;parts.forEach((p,i)=>{p.classList.toggle('is-selected',i===n);p.setAttribute('aria-pressed',String(i===n));});choices.forEach((p,i)=>p.setAttribute('aria-pressed',String(i===n)));info.forEach((p,i)=>p.hidden=i!==n);status.textContent=`Part ${n+1} of ${info.length}: ${info[n].querySelector('h4').textContent}`;}
  function pick(n){pause();select(n);}
  parts.forEach((p,i)=>{p.addEventListener('click',()=>pick(i));p.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();pick(i);}});});
  choices.forEach((p,i)=>p.addEventListener('click',()=>pick(i)));
  figure.querySelector('[data-an-action="next"]').addEventListener('click',()=>pick((current+1)%info.length));
  figure.querySelector('[data-an-action="reset"]').addEventListener('click',()=>pick(0));
  play.addEventListener('click',()=>{
   if(timer!==null){pause();return;}
   all.forEach(x=>x.pause());if(reduced.matches)return;
   if(current===info.length-1)select(0);
   play.textContent='Pause tour';play.setAttribute('aria-pressed','true');figure.classList.add('is-touring');
   timer=setInterval(()=>{if(!visible()){pause();return;}select(current+1);if(current===info.length-1)pause();},5500);
  });
  function motion(){pause();play.hidden=reduced.matches;}
  all.push({pause,visible});motion();select(0);reduced.addEventListener('change',motion);
  figure.querySelector('.an-toolbar').hidden=false;
 });
 new MutationObserver(()=>all.forEach(x=>{if(!x.visible())x.pause();})).observe(document.querySelector('main'),{attributes:true,subtree:true,attributeFilter:['hidden']});
 document.addEventListener('visibilitychange',()=>{if(document.hidden)all.forEach(x=>x.pause());});
 window.addEventListener('beforeprint',()=>all.forEach(x=>x.pause()));
})();
