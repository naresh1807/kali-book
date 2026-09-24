(()=>{
 'use strict';
 const root=document.documentElement,button=document.getElementById('theme-toggle');
 const system=matchMedia('(prefers-color-scheme: dark)');let explicit=false;
 try{explicit=['light','dark'].includes(localStorage.getItem('fieldbook-theme'));}catch{}
 function apply(mode){root.dataset.theme=mode;const next=mode==='dark'?'light':'dark';button.textContent=next==='light'?'Light mode':'Dark mode';button.setAttribute('aria-label','Switch to '+next+' mode');button.title='Switch to '+next+' mode';}
 apply(root.dataset.theme||'dark');
 button.addEventListener('click',()=>{const mode=root.dataset.theme==='dark'?'light':'dark';explicit=true;apply(mode);try{localStorage.setItem('fieldbook-theme',mode);}catch{}});
 system.addEventListener('change',e=>{if(!explicit)apply(e.matches?'dark':'light');});
 window.addEventListener('storage',e=>{if(e.key==='fieldbook-theme'){explicit=e.newValue==='dark'||e.newValue==='light';apply(explicit?e.newValue:(system.matches?'dark':'light'));}});
})();
