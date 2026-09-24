(() => {
 'use strict';
 const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
 const controllers = [];
 document.querySelectorAll('[data-visual]').forEach(figure => {
  const controls=figure.querySelector('.cv-controls');
  const play=figure.querySelector('[data-cv="play"]');
  const status=figure.querySelector('.cv-status');
  const nodes=[...figure.querySelectorAll('.cv-node')];
  const steps=[...figure.querySelectorAll('.cv-steps li')];
  let current=0, timer=null;
  const visible=()=>!document.hidden && !figure.closest('[hidden]');
  function draw(){
   nodes.forEach((n,i)=>n.classList.toggle('is-active',i===current));
   steps.forEach((n,i)=>{n.classList.toggle('is-active',i===current);if(i===current)n.setAttribute('aria-current','step');else n.removeAttribute('aria-current');});
   status.textContent=`Step ${current+1} of ${steps.length}: ${steps[current].querySelector('strong').textContent}`;
  }
  function pause(){if(timer!==null)clearInterval(timer);timer=null;figure.classList.remove('is-playing');play.textContent='Play';play.setAttribute('aria-pressed','false');}
  function next(){current=(current+1)%steps.length;draw();}
  play.addEventListener('click',()=>{
   if(timer!==null){pause();return;}
   controllers.forEach(c=>c.pause());
   if(reduced.matches){next();return;}
   if(current===steps.length-1)current=0;
   draw();figure.classList.add('is-playing');play.textContent='Pause';play.setAttribute('aria-pressed','true');
   timer=setInterval(()=>{if(!visible()){pause();return;}if(current===steps.length-1){pause();return;}next();if(current===steps.length-1)pause();},3500);
  });
  figure.querySelector('[data-cv="next"]').addEventListener('click',()=>{pause();next();});
  figure.querySelector('[data-cv="reset"]').addEventListener('click',()=>{pause();current=0;draw();});
  function motion(){pause();play.hidden=reduced.matches;controls.title=reduced.matches?'Reduced motion: use Next step for manual progression.':'';}
  controllers.push({pause,visible});controls.hidden=false;motion();draw();reduced.addEventListener('change',motion);
 });
 // Chapter navigation, searching, background tabs and printing stop playback.
 new MutationObserver(()=>controllers.forEach(c=>{if(!c.visible())c.pause();})).observe(document.querySelector('main'),{subtree:true,attributes:true,attributeFilter:['hidden']});
 document.addEventListener('visibilitychange',()=>{if(document.hidden)controllers.forEach(c=>c.pause());});
 window.addEventListener('beforeprint',()=>controllers.forEach(c=>c.pause()));
})();
