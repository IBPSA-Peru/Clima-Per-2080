/* Visor de la auditoría climática — lógica.
   D = payload inyectado por generar_visor.py.
   Estructura narrativa: primero el número que se busca (temperatura por horizonte),
   después el examen de si ese número es fiable. */

const F=(x,d=2)=>x.toLocaleString('es-PE',{minimumFractionDigits:d,maximumFractionDigits:d});
const N=x=>Math.round(x).toLocaleString('es-PE');
const $=id=>document.getElementById(id);
const tip=$('tip');
const hov=(e,t)=>{tip.innerHTML=t;tip.style.opacity=1;
  tip.style.left=Math.min(e.clientX+14,innerWidth-250)+'px';tip.style.top=(e.clientY-42)+'px';};
const out=()=>tip.style.opacity=0;
const ease=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;

/* Escala divergente frío→calor, reservada a temperatura. */
function escala(v,a,b){
  const t=Math.max(0,Math.min(1,(v-a)/(b-a)));
  const p=[[43,111,158],[90,168,204],[168,196,190],[232,176,75],[226,98,47],[193,53,42]];
  const x=t*(p.length-1), i=Math.min(Math.floor(x),p.length-2), f=x-i;
  const c=p[i].map((v0,k)=>Math.round(v0+(p[i+1][k]-v0)*f));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
}

const HOR=['hoy','a2030','a2050','a2080'];
const HET={hoy:'Hoy',a2030:'2030',a2050:'2050',a2080:'2080'};
let hz='a2050', escen='s245', sel='Lima';

/* Interpola todas las tarjetas y el mapa entre el estado anterior y el nuevo. */
let animT=null;
function setH(h){
  if(h===hz) return;
  const desde=hz; hz=h;
  document.querySelectorAll('.horiz button').forEach(b=>b.classList.toggle('on',b.dataset.h===h));
  document.querySelectorAll('.migas a').forEach(a=>a.classList.remove('on'));
  if(animT) cancelAnimationFrame(animT);
  let t0=null;
  const paso=ts=>{ if(!t0)t0=ts; const k=Math.min((ts-t0)/900,1), e=ease(k);
    pintar(desde,hz,e); if(k<1) animT=requestAnimationFrame(paso); else animT=null; };
  animT=requestAnimationFrame(paso);
}
function setE(e){escen=e;
  document.querySelectorAll('#segE button').forEach(b=>b.classList.toggle('on',b.dataset.e===e));
  pintar(hz,hz,1); barras();}
function pick(n){
  sel=n;
  portada();
  pintar(hz,hz,1);
  barras();
  nube();
  solDibuja();
  document.querySelectorAll('#heroCiudades button').forEach(b=>b.classList.toggle('on',b.textContent===n));
  document.querySelectorAll('#nbCiudades button').forEach(b=>b.classList.toggle('on',b.textContent===n));
}

const G=(c,h)=>c[escen].H[h];
const mez=(a,b,k)=>a+(b-a)*k;

function animarCifra(el, fin, dur=360){
  if(!el) return;
  const ini = parseFloat(el.getAttribute('data-v')) || parseFloat(el.textContent.replace(',','.')) || 0;
  if(Math.abs(ini - fin) < 0.02){
    el.textContent = F(fin, 1);
    el.setAttribute('data-v', fin);
    return;
  }
  const t0 = performance.now();
  function step(t){
    const p = Math.min((t - t0) / dur, 1);
    const easeVal = p < 0.5 ? 4*p*p*p : 1 - Math.pow(-2*p + 2, 3) / 2;
    const cur = ini + (fin - ini) * easeVal;
    el.textContent = F(cur, 1);
    if(p < 1) requestAnimationFrame(step);
    else {
      el.textContent = F(fin, 1);
      el.setAttribute('data-v', fin);
    }
  }
  requestAnimationFrame(step);
}

/* ── portada ── */
function portada(){
  const c=D.ciudades.find(o=>o.n===sel)||D.ciudades[0];
  const L45=c.s245.H, L85=c.s585.H;
  if($('heroTit')) $('heroTit').innerHTML=`${c.n} tendrá <em>${F(L45.a2050.T,1)} °C</em> de media en 2050`;
  if($('heroSubtit')) $('heroSubtit').innerHTML=`Eso bajo el escenario central SSP2-4.5 (Trayectoria Socioeconómica Compartida Intermedia). Bajo el de estrés SSP5-8.5 (Muy Altas Emisiones), ${F(L85.a2050.T,1)} °C. Ocho ciudades peruanas, cuatro horizontes y una pregunta incómoda: ¿cuánto puedes fiarte de estos archivos?`;
  if($('grande')){
    const exist = $('grande').querySelectorAll('.cifra');
    if(exist.length === HOR.length){
      HOR.forEach((h, idx)=>{
        const v=L45[h].T, itp=D.interpolado.includes(h);
        const cifraEl = exist[idx];
        cifraEl.style.setProperty('--c', escala(v,14,26));
        animarCifra(cifraEl.querySelector('.n'), v);
        const lbl = cifraEl.querySelector('.c');
        if(lbl) lbl.innerHTML = `${h==='hoy'?c.n+' hoy':c.n+' en '+HET[h]}${itp?' <em>interp.</em>':''}`;
      });
    } else {
      $('grande').innerHTML=HOR.map(h=>{
        const v=L45[h].T, itp=D.interpolado.includes(h);
        return `<div class="cifra" style="--c:${escala(v,14,26)}">
          <span class="n" data-v="${v}">${F(v,1)}</span><span class="u">°C</span>
          <div class="c">${h==='hoy'?c.n+' hoy':c.n+' en '+HET[h]}${itp?' <em>interp.</em>':''}</div></div>`;
      }).join('');
    }
  }
}

/* ── tarjetas por ciudad ── */
function tarjetas(desde,hasta,k){
  const d=[...D.ciudades].sort((a,b)=>G(b,'hoy').T-G(a,'hoy').T);
  $('rej').innerHTML=d.map(c=>{
    const T=mez(G(c,desde).T,G(c,hasta).T,k), d0=T-G(c,'hoy').T, col=escala(T,8,31);
    return `<div class="tarj ${c.n===sel?'on':''}" onclick="pick('${c.n}')">
      <div class="cinta" style="background:${col}"></div>
      <div class="cd">${c.n}</div><div class="zn">${c.zona} · ${N(c.elev)} m</div>
      <div class="tt" style="color:${col}">${F(T,1)}<span> °C</span></div>
      <div class="dd" style="color:${d0>.05?'var(--calor-tx)':'var(--tinta3)'}">
        ${d0>.05?`&#9650; +${F(d0)} °C sobre hoy`:'línea base'}</div></div>`;}).join('');
}

/* ── mapa ── */
function proj(lon,lat,W,H){
  const l0=-81.8,l1=-68.2,b0=-18.7,b1=0.4;
  return [(lon-l0)/(l1-l0)*W,(b1-lat)/(b1-b0)*H];
}
function mapa(desde,hasta,k){
  const W=520,H=700,R=13;
  let s=`<svg viewBox="-14 -16 ${W+258} ${H+34}">`;
  s+=`<path class="pais" d="${D.peru.map((p,i)=>(i?'L':'M')+proj(p[0],p[1],W,H).map(v=>v.toFixed(1)).join(' ')).join(' ')}Z"/>`;
  const LB={Arequipa:[-1,-24,'end'],Juliaca:[1,-9,'start'],Tacna:[1,20,'start'],
            Cusco:[-1,-9,'end'],Lima:[-1,3,'end'],Trujillo:[-1,3,'end'],
            Piura:[1,-22,'start'],Iquitos:[1,3,'start']};
  D.ciudades.forEach(c=>{
    const [x,y]=proj(c.lon,c.lat,W,H), T=mez(G(c,desde).T,G(c,hasta).T,k), col=escala(T,8,31);
    const on=c.n===sel; let [dx,dy,an]=LB[c.n]||[1,4,'start'];
    dx+=(an==='end'?-1:1)*((on?R*1.25:R)+8);
    s+=`<circle class="halo" cx="${x}" cy="${y}" r="${on?R*2.3:R*1.65}" fill="${col}"/>
        <circle class="est" cx="${x}" cy="${y}" r="${on?R*1.25:R}" fill="${col}"
          stroke="${on?'#12161f':'rgba(255,255,255,.75)'}" stroke-width="${on?2.4:1.4}"
          onclick="pick('${c.n}')"
          onmousemove="hov(event,'<b>${c.n}</b> · ${c.zona}<br>${F(T,1)} °C en ${HET[hz]}')"
          onmouseout="out()"/>
        <text class="enom" x="${x+dx}" y="${y+dy}" text-anchor="${an}"
          font-weight="${on?'700':'400'}" fill="${on?'#12161f':'#3d4657'}">${c.n}</text>
        <text class="lbl" x="${x+dx}" y="${y+dy+13}" text-anchor="${an}">${F(T,1)} °C</text>`;});
  const bx=W+52,by=110,bh=360;
  s+=`<text class="lbl2" x="${bx-4}" y="${by-20}">Temperatura media anual</text>
      <text class="lbl" x="${bx-4}" y="${by-5}">°C · ${HET[hz]}</text>
      <defs><linearGradient id="g1" x1="0" y1="1" x2="0" y2="0">`;
  for(let i=0;i<=10;i++) s+=`<stop offset="${i*10}%" stop-color="${escala(8+23*i/10,8,31)}"/>`;
  s+=`</linearGradient></defs><rect x="${bx}" y="${by}" width="14" height="${bh}" rx="7" fill="url(#g1)"/>`;
  for(let i=0;i<=4;i++) s+=`<text class="lbl" x="${bx+22}" y="${by+bh*i/4+4}">${N(31-23*i/4)}</text>`;
  s+=`</svg>`;
  $('mapa').innerHTML=s;
}

/* ── ficha ── */
function ficha(){
  const c=D.ciudades.find(o=>o.n===sel), h=G(c,hz), b=G(c,'hoy');
  const f=(l,v,up)=>`<div class="fila"><span>${l}</span><b class="${up?'up':''}">${v}</b></div>`;
  const dl=(v,u,d=2)=>hz==='hoy'?'':` <span style="color:var(--calor-tx)">(+${F(v,d)}${u})</span>`;
  $('ficha').innerHTML=`<h3>${c.n}</h3>
   <span class="zn">${c.zona} · ${N(c.elev)} m · ${HET[hz]}</span>
   ${f('Temperatura media anual',F(h.T,1)+' °C'+dl(h.T-b.T,' °C'),1)}
   ${f('Diseño calefacción (99.6 %)',(h.tcal!==undefined?F(h.tcal,1)+' °C'+dl(h.tcal-b.tcal,' °C',1):'—'))}
   ${f('Diseño refrigeración (0.4 %)',(h.tref!==undefined?F(h.tref,1)+' °C'+dl(h.tref-b.tref,' °C',1):F(h.p99,1)+' °C'))}
   ${f('Percentil 99 de bulbo seco',F(h.p99,1)+' °C'+dl(h.p99-b.p99,' °C',1))}
   ${f('Máxima del año',F(h.mx,1)+' °C'+dl(h.mx-b.mx,' °C',1))}
   ${f('Humedad absoluta',F(h.W,1)+' g/kg'+dl(h.W-b.W,' g/kg',1))}
   ${f('Horas sobre 26 °C',N(h.h26)+' h')}
   ${f('Grados-hora de enfriamiento',N(h.gh)+' °C·h')}
   ${f('Archivo base',c.y0.toFixed(0)+' · TMYx 2011-2025')}`;
}

function pintar(desde,hasta,k){tarjetas(desde,hasta,k);mapa(desde,hasta,k);ficha();climograma();trayectoria();}

/* ── barras: los cuatro horizontes por ciudad, clicables ──
   Clic en una barra selecciona esa ciudad Y ese horizonte a la vez, y todo lo demás
   —mapa, ficha, climograma, trayectoria— se mueve con ella. */
let brOrden='a2080';
function brSort(k){brOrden=k;
  document.querySelectorAll('#brSort button').forEach(b=>b.classList.toggle('on',b.dataset.k===k));
  barras();}
function brPick(n,h){sel=n; if(h!==hz){setH(h);} else {pintar(hz,hz,1);} barras();}

function barras(){
  const d=[...D.ciudades].sort((a,b)=> brOrden==='n' ? a.n.localeCompare(b.n)
    : brOrden==='elev' ? a.elev-b.elev
    : brOrden==='dif' ? (G(b,'a2080').T-G(b,'hoy').T)-(G(a,'a2080').T-G(a,'hoy').T)
    : G(b,brOrden).T-G(a,brOrden).T);
  const W=1160,H=430,ml=60,mr=24,mt=32,mb=76,iw=W-ml-mr,ih=H-mt-mb;
  const todos=d.flatMap(c=>HOR.map(h=>G(c,h).T));
  const y0=Math.floor(Math.min(...todos)-1), y1=Math.ceil(Math.max(...todos)+1);
  const Y=v=>mt+ih-(v-y0)/(y1-y0)*ih, bw=iw/d.length;
  let s=`<svg viewBox="0 0 ${W} ${H}">`;
  for(let g=Math.ceil(y0/5)*5;g<=y1;g+=5) s+=`<line class="gl" x1="${ml}" x2="${W-mr}" y1="${Y(g)}"
      y2="${Y(g)}"/><text class="lbl" x="${ml-9}" y="${Y(g)+4}" text-anchor="end">${g}</text>`;
  d.forEach((c,i)=>{
    const act=(c.n===sel);
    if(act) s+=`<rect x="${ml+i*bw+2}" y="${mt-6}" width="${bw-4}" height="${ih+6}" rx="8"
          fill="#12161f" opacity=".045"/>`;
    HOR.forEach((h,j)=>{
      const v=G(c,h).T, x=ml+i*bw+bw*.13+j*(bw*.185), w=bw*.165, y=Y(v);
      const vivo=(h===hz);
      s+=`<rect class="bar" x="${x}" y="${y}" width="${w}" height="${mt+ih-y}" rx="3"
            fill="${escala(v,8,31)}" opacity="${vivo?1:(act?.6:.34)}" style="cursor:pointer"
            onclick="brPick('${c.n}','${h}')"
            onmousemove="hov(event,'<b>${c.n}</b> · ${HET[h]}<br>${F(v,1)} °C · +${F(v-G(c,'hoy').T)} sobre hoy<br><i>clic para fijar</i>')"
            onmouseout="out()"/>`;
      if(vivo) s+=`<text class="val" x="${x+w/2}" y="${y-7}" text-anchor="middle"
            font-size="11">${F(v,1)}</text>`;});
    s+=`<text class="lbl2" x="${ml+i*bw+bw/2}" y="${mt+ih+20}" text-anchor="middle"
          font-weight="${act?'700':'400'}" style="cursor:pointer"
          onclick="brPick('${c.n}','${hz}')">${c.n}</text>
        <text class="lbl" x="${ml+i*bw+bw/2}" y="${mt+ih+34}" text-anchor="middle">${N(c.elev)} m</text>
        <text class="lbl" x="${ml+i*bw+bw/2}" y="${mt+ih+50}" text-anchor="middle"
          fill="var(--calor-tx)">+${F(G(c,'a2080').T-G(c,'hoy').T,1)} a 2080</text>`;});
  HOR.forEach((h,j)=>{const lx=ml+j*116;
    s+=`<rect x="${lx}" y="6" width="15" height="9" rx="2" fill="${escala(20+j*3,8,31)}"
          opacity="${h===hz?1:.4}"/>
        <text class="lbl" x="${lx+21}" y="14" font-weight="${h===hz?'700':'400'}"
          fill="${h===hz?'#12161f':'#656f7e'}" style="cursor:pointer"
          onclick="setH('${h}');barras()">${HET[h]}</text>`;});
  s+=`<line class="ax" x1="${ml}" x2="${W-mr}" y1="${mt+ih}" y2="${mt+ih}"/>
      <text class="lbl2" x="14" y="${mt+ih/2}" transform="rotate(-90 14 ${mt+ih/2})"
        text-anchor="middle">Temperatura media anual (°C)</text></svg>`;
  $('barras').innerHTML=s;
  $('brSort').innerHTML=[['a2080','temperatura'],['dif','cuánto sube'],['elev','elevación'],
    ['n','nombre']].map(([k,et])=>
    `<button class="${brOrden===k?'on':''}" data-k="${k}" onclick="brSort('${k}')">${et}</button>`).join('');
}


/* ── nube psicrométrica: cada punto es UNA HORA del año ──
   Antes el color codificaba la temperatura, que es lo mismo que el eje X: información
   duplicada que no decía nada. Ahora codifica el MES o la HORA DEL DÍA, que sí es
   información nueva y explica por qué la nube tiene la forma que tiene. */
let anim=null, prog=0, nbCol='mes', nbSel=-1;
const NHOR=['hoy','a2030','a2050','a2080'];
const MES3=['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'];
/* Escala de meses para hemisferio SUR: enero es verano. */
const MESCOL=['#c1352a','#d94f2b','#e2622f','#e8983c','#c9a94e','#8fa98a',
              '#5f9bb5','#3d8ab0','#4f93b3','#96a86a','#d3963a','#dc6b32'];
const horaCol=h=>escala(h<=13?h:26-h,0,13);   // medianoche fría, mediodía cálido

function nbSetCol(m){nbCol=m;
  document.querySelectorAll('#nbModo button').forEach(b=>b.classList.toggle('on',b.dataset.m===m));
  nube();}
function nbPick(i){nbSel=(nbSel===i?-1:i);nube();}

function nube(){
  const W=1100,H=470,ml=62,mr=26,mt=20,mb=54,iw=W-ml-mr,ih=H-mt-mb;
  const cNubes = (D.nubes && D.nubes[sel]) ? D.nubes[sel] : (D.nubes ? (D.nubes['Lima']||D.nubes) : {});
  const tod=NHOR.flatMap(k=>(cNubes && cNubes[k]) ? cNubes[k] : []);
  if(!tod.length) return;
  const xa=Math.floor(Math.min(...tod.map(p=>p[0]))-1),xb=Math.ceil(Math.max(...tod.map(p=>p[0]))+1);
  const ya=Math.floor(Math.min(...tod.map(p=>p[1]))-1),yb=Math.ceil(Math.max(...tod.map(p=>p[1]))+1);
  const X=v=>ml+(v-xa)/(xb-xa)*iw, Y=v=>mt+ih-(v-ya)/(yb-ya)*ih;
  let s=`<svg viewBox="0 0 ${W} ${H}">`;
  for(let g=Math.ceil(xa/2)*2;g<=xb;g+=2) s+=`<line class="gl" x1="${X(g)}" x2="${X(g)}" y1="${mt}"
      y2="${mt+ih}"/><text class="lbl" x="${X(g)}" y="${mt+ih+18}" text-anchor="middle">${g}</text>`;
  for(let g=Math.ceil(ya/2)*2;g<=yb;g+=2) s+=`<line class="gl" x1="${ml}" x2="${W-mr}" y1="${Y(g)}"
      y2="${Y(g)}"/><text class="lbl" x="${ml-9}" y="${Y(g)+4}" text-anchor="end">${g}</text>`;
  const seg=Math.min(Math.floor(prog),NHOR.length-2), fr=prog-seg;
  const A=cNubes[NHOR[seg]], B=cNubes[NHOR[seg+1]];
  A.forEach((p,i)=>{
    const q=B[i], mes=p[2], hora=p[3];
    const marcado = nbSel<0 || (nbCol==='mes'? mes===nbSel+1 : Math.floor(hora/4)===nbSel);
    const x=X(p[0]+(q[0]-p[0])*fr), y=Y(p[1]+(q[1]-p[1])*fr);
    s+=`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${marcado?2.6:1.8}"
          fill="${marcado?(nbCol==='mes'?MESCOL[mes-1]:horaCol(hora)):'#cfc9bd'}"
          opacity="${marcado?.72:.28}"/>`;});
  s+=`<text class="lbl2" x="${ml+iw/2}" y="${H-8}" text-anchor="middle">
        Temperatura de bulbo seco (°C) — qué tan caliente está el aire</text>
      <text class="lbl2" x="14" y="${mt+ih/2}" transform="rotate(-90 14 ${mt+ih/2})"
        text-anchor="middle">Humedad absoluta (g de vapor por kg de aire seco)</text></svg>`;
  $('nube').innerHTML=s;

  const ent=Math.round(prog);
  $('estado').innerHTML=Math.abs(prog-ent)<.02
    ? `<b>${HET[NHOR[ent]]}</b>${ent?' · '+D.nube_escenario:' · TMYx 2011-2025'}`
      +(D.interpolado.includes(NHOR[ent])?' · interpolado':'')
    : `${HET[NHOR[Math.floor(prog)]]} → ${HET[NHOR[Math.ceil(prog)]]}`;
  document.querySelectorAll('#nbPasos .pasoN').forEach((b,i)=>b.classList.toggle('on',i===ent&&Math.abs(prog-ent)<.02));

  // leyenda: qué es un punto, y el filtro por mes u hora
  const items = nbCol==='mes'
    ? MES3.map((m,i)=>[MESCOL[i],m,i])
    : [[horaCol(2),'0-3 h',0],[horaCol(6),'4-7 h',1],[horaCol(10),'8-11 h',2],
       [horaCol(14),'12-15 h',3],[horaCol(18),'16-19 h',4],[horaCol(22),'20-23 h',5]];
  $('nbLeg').innerHTML=items.map(([col,et,i])=>
    `<button class="nbChip ${nbSel===i?'on':(nbSel<0?'':'off')}" onclick="nbPick(${i})"
       title="Clic para aislar"><i style="background:${col}"></i>${et}</button>`).join('')
    +(nbSel>=0?`<button class="nbChip todos" onclick="nbPick(${nbSel})">Ver todo</button>`:'');
}
function reproducir(){
  if(anim){cancelAnimationFrame(anim);anim=null;$('btnN').lastChild.textContent=' Reanudar';return;}
  const ida=prog<1.5, p0=prog, p1=ida?3:0; let t0=null;
  $('btnN').lastChild.textContent=' Pausar';
  const paso=ts=>{ if(!t0)t0=ts; const k=Math.min((ts-t0)/(2200*Math.abs(p1-p0)||1),1);
    prog=p0+(p1-p0)*ease(k); nube();
    if(k<1) anim=requestAnimationFrame(paso);
    else{anim=null;prog=p1;$('btnN').lastChild.textContent=ida?' Volver a hoy':' Recorrer hasta 2080';}};
  anim=requestAnimationFrame(paso);
}
function irNube(i){
  if(anim){cancelAnimationFrame(anim);anim=null;}
  document.querySelectorAll('#nbPasos .pasoN').forEach((b,idx)=>b.classList.toggle('on', idx===i));
  const p0=prog; let t0=null;
  const paso=ts=>{
    if(!t0) t0=ts;
    const k=Math.min((ts-t0)/600,1);
    prog=p0+(i-p0)*ease(k);
    nube();
    if(k<1) requestAnimationFrame(paso);
    else { prog=i; nube(); }
  };
  requestAnimationFrame(paso);
}


/* ── vintage ── */
function vintage(){
  const d=D.vintage,W=1080,H=390,ml=58,mr=22,mt=22,mb=54,iw=W-ml-mr,ih=H-mt-mb;
  const X=v=>ml+(v-6)/28*iw, Y=v=>mt+ih-(v+1.4)/5.4*ih;
  let s=`<svg viewBox="0 0 ${W} ${H}">`;
  for(let g=-1;g<=4;g++) s+=`<line x1="${ml}" x2="${W-mr}" y1="${Y(g)}" y2="${Y(g)}"
      stroke="${g===0?'#c4bcac':'#d9d3c7'}"/><text class="lbl" x="${ml-9}" y="${Y(g)+4}"
      text-anchor="end">${g>0?'+':''}${g}</text>`;
  for(let g=10;g<=30;g+=5) s+=`<text class="lbl" x="${X(g)}" y="${mt+ih+20}" text-anchor="middle">${g}</text>`;
  const A=D.ajuste;
  s+=`<line x1="${X(6)}" y1="${Y(A.pendiente_C_por_ano*6+A.intercepto_C)}" x2="${X(34)}"
        y2="${Y(A.pendiente_C_por_ano*34+A.intercepto_C)}" stroke="#12161f" stroke-width="1.6"
        stroke-dasharray="7 5" opacity=".65"/>`;
  d.forEach((o,i)=>{const at=o.a&&o.v==='2004-2018';
    s+=`<circle cx="${X(o.x)}" cy="${Y(o.y)}" r="0" fill="${at?'#b3261e':(o.a?'#e8b04b':'#2b6f9e')}"
        stroke="#fff" stroke-width="1.3"
        onmousemove="hov(event,'<b>${o.c}</b> ${o.v}<br>${o.x>0?'+':''}${F(o.x,1)} años · ΔT ${o.y>0?'+':''}${F(o.y)} °C')"
        onmouseout="out()"><animate attributeName="r" from="0" to="${at?8:5.5}" dur=".5s"
        begin="${i*.03}s" fill="freeze"/></circle>`;
    if(at) s+=`<text class="lbl2" x="${X(o.x)+13}" y="${Y(o.y)+4}" fill="#b3261e" font-weight="700"
        opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".6s" begin="1.2s"
        fill="freeze"/>${o.c} 2004-2018</text>`;});
  s+=`<text class="lbl2" x="${ml+iw/2}" y="${H-8}" text-anchor="middle">
        Diferencia de año centroide contra el TMYx de periodo completo (años)</text>
      <text class="lbl2" x="12" y="${mt+ih/2}" transform="rotate(-90 12 ${mt+ih/2})"
        text-anchor="middle">ΔT aparente (°C)</text></svg>`;
  $('vint').innerHTML=s;
}

/* ── convergencia ── */
function converg(){
  const c=D.conv;
  const d=[['TMYx completo (1991-2020)','Centroide '+c.centroide_completo.toFixed(0)+' · Línea base',c.linea_base_completo_C,'#c4bcac'],
           ['TMYx reciente (2011-2025)','Centroide '+c.centroide_reciente.toFixed(0)+' · Línea base',c.linea_base_reciente_C,'#9aa4b0'],
           ['Meteonorm 2050 (CMIP5)','RCP8.5 · Síntesis estocástica',c.T_2050_meteonorm_rcp85_C,'#e8b04b'],
           ['FWG 2050 (CMIP6 / FWG v4.2)','SSP5-8.5 · Morphing climático',c.T_2050_fwg_ssp585_C,'#c1352a']];
  const W=1080,H=320,ml=58,mr=22,mt=32,mb=68,iw=W-ml-mr,ih=H-mt-mb;
  const Y=v=>mt+ih-(v-18.4)/3.8*ih, bw=iw/4;
  let s=`<svg viewBox="0 0 ${W} ${H}">`;
  for(let g=19;g<=22;g++) s+=`<line class="gl" x1="${ml}" x2="${W-mr}" y1="${Y(g)}" y2="${Y(g)}"/>
      <text class="lbl" x="${ml-9}" y="${Y(g)+4}" text-anchor="end">${g}</text>`;
  d.forEach(([t,sb,v,col],i)=>{const x=ml+i*bw+bw*.2,w=bw*.6,y=Y(v);
    s+=`<rect class="bar" x="${x}" y="${y}" width="${w}" height="${mt+ih-y}" rx="4" fill="${col}"/>
        <text class="val" x="${x+w/2}" y="${y-10}" text-anchor="middle" font-size="15">${F(v)} °C</text>
        <text class="lbl2" x="${x+w/2}" y="${mt+ih+20}" text-anchor="middle">${t}</text>
        <text class="lbl" x="${x+w/2}" y="${mt+ih+35}" text-anchor="middle">${sb}</text>`;});
  const xa=ml+2*bw+bw*.5,xb=ml+3*bw+bw*.5;
  const yTop=Math.min(Y(c.T_2050_meteonorm_rcp85_C),Y(c.T_2050_fwg_ssp585_C))-42;
  s+=`<line x1="${xa}" y1="${yTop+8}" x2="${xa}" y2="${Y(c.T_2050_meteonorm_rcp85_C)-24}"
        stroke="#12161f" stroke-width="1"/>
      <line x1="${xb}" y1="${yTop+8}" x2="${xb}" y2="${Y(c.T_2050_fwg_ssp585_C)-24}"
        stroke="#12161f" stroke-width="1"/>
      <line x1="${xa}" y1="${yTop+8}" x2="${xb}" y2="${yTop+8}" stroke="#12161f" stroke-width="1.4"/>
      <text x="${(xa+xb)/2}" y="${yTop-3}" text-anchor="middle" font-size="14" font-weight="700">
        ${c.divergencia_absoluta_C>0?'+':''}${F(c.divergencia_absoluta_C)} °C de diferencia metodológica</text>
      <line class="ax" x1="${ml}" x2="${W-mr}" y1="${mt+ih}" y2="${mt+ih}"/></svg>`;
  $('conv').innerHTML=s;
}

/* ── observador de capítulos ──
   La clase 'anim' se pone AQUI: si el script no llega, las secciones quedan visibles. */
document.body.classList.add('anim');
const io=new IntersectionObserver(es=>es.forEach(e=>{
  if(e.isIntersecting){e.target.classList.add('vis');
    document.querySelectorAll('.migas a').forEach(a=>
      a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id));}
}),{threshold:.22});
document.querySelectorAll('section').forEach(s=>io.observe(s));


/* ── trayectoria: lo OBSERVADO y lo PROYECTADO en el mismo eje ──
   A la izquierda, las cinco ventanas TMYx de la ciudad situadas en su año centroide:
   son datos medidos. A la derecha, las proyecciones. La frontera va marcada.
   OJO: las ventanas se solapan y cada una es un año TÍPICO, no una observación anual.
   No es una serie climática; es lo más atrás que llega este material. */
function trayectoria(){
  const c=D.ciudades.find(o=>o.n===sel);
  const W=1160,H=400,ml=64,mr=126,mt=36,mb=64,iw=W-ml-mr,ih=H-mt-mb;
  const obs=c.obs;
  const x0=Math.min(...obs.map(o=>o[0]))-3, x1=2084;
  const vals=['s245','s585'].flatMap(k=>HOR.map(h=>c[k].H[h].T)).concat(obs.map(o=>o[1]));
  const y0=Math.floor(Math.min(...vals)-.8), y1=Math.ceil(Math.max(...vals)+.8);
  const X=a=>ml+(a-x0)/(x1-x0)*iw, Y=v=>mt+ih-(v-y0)/(y1-y0)*ih;
  const anos=[c.y0,2030,2050,2080];
  let s=`<svg viewBox="0 0 ${W} ${H}">`;
  for(let g=Math.ceil(y0);g<=y1;g++) s+=`<line class="gl" x1="${ml}" x2="${ml+iw}" y1="${Y(g)}"
      y2="${Y(g)}"/><text class="lbl" x="${ml-10}" y="${Y(g)+4}" text-anchor="end">${g}</text>`;
  for(let a=1990;a<=2080;a+=10) if(a>x0) s+=`<text class="lbl" x="${X(a)}" y="${mt+ih+20}"
      text-anchor="middle">${a}</text>`;
  s+=`<line x1="${X(c.y0)}" x2="${X(c.y0)}" y1="${mt-8}" y2="${mt+ih}" stroke="#988a6f"
        stroke-width="1.2" stroke-dasharray="4 4"/>
      <text class="lbl" x="${X(c.y0)-9}" y="${mt-14}" text-anchor="end">medido</text>
      <text class="lbl" x="${X(c.y0)+9}" y="${mt-14}">proyectado</text>`;
  s+=`<polyline points="${obs.map(o=>X(o[0]).toFixed(1)+','+Y(o[1]).toFixed(1)).join(' ')}"
        fill="none" stroke="#8a8378" stroke-width="2" stroke-dasharray="3 3" opacity=".7"/>`;
  obs.forEach(o=>{s+=`<circle cx="${X(o[0])}" cy="${Y(o[1])}" r="5.5" fill="#8a8378"
        stroke="#fff" stroke-width="1.6" style="cursor:help"
        onmousemove="hov(event,'<b>TMYx ${o[2]}</b> · medido<br>centroide ${o[0]} · ${F(o[1],1)} °C')"
        onmouseout="out()"/>`;});
  [['s245','#2b6f9e','SSP2-4.5'],['s585','#c1352a','SSP5-8.5']].forEach(([k,col,et],j)=>{
    const pts=HOR.map((h,i)=>[X(anos[i]),Y(c[k].H[h].T)]);
    s+=`<path d="${pts.map((p,i)=>(i?'L':'M')+p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' ')}"
          fill="none" stroke="${col}" stroke-width="2.8" stroke-linejoin="round"/>`;
    pts.forEach((pt,i)=>{
      const v=c[k].H[HOR[i]].T, itp=D.interpolado.includes(HOR[i]);
      s+=`<circle cx="${pt[0]}" cy="${pt[1]}" r="${HOR[i]===hz?7:5}" fill="${itp?'#fff':col}"
            stroke="${col}" stroke-width="${itp?2.4:1.8}" style="cursor:pointer"
            onclick="setH('${HOR[i]}')"
            onmousemove="hov(event,'<b>${c.n}</b> · ${i?anos[i]:'hoy'} · ${et}${itp?' · interpolado':''}<br>${F(v,1)} °C · +${F(v-c[k].H.hoy.T)} sobre hoy')"
            onmouseout="out()"/>`;
      if(i===3) s+=`<text class="val" x="${pt[0]+12}" y="${pt[1]+4}" fill="${col}">${F(v,1)} °C</text>
            <text class="lbl" x="${pt[0]+12}" y="${pt[1]+17}">${et}</text>`;});});
  s+=`<circle cx="${ml+8}" cy="${mt+10}" r="5.5" fill="#8a8378" stroke="#fff" stroke-width="1.6"/>
      <text class="lbl" x="${ml+21}" y="${mt+14}">ventanas TMYx medidas · círculo hueco = interpolado
        · clic en un punto para cambiar de horizonte</text>
      <line class="ax" x1="${ml}" x2="${ml+iw}" y1="${mt+ih}" y2="${mt+ih}"/>
      <text class="lbl2" x="16" y="${mt+ih/2}" transform="rotate(-90 16 ${mt+ih/2})"
        text-anchor="middle">Temperatura media anual (°C)</text></svg>`;
  $('tray').innerHTML=s;
  const mn=Math.min(...obs.map(o=>o[1])), mx=Math.max(...obs.map(o=>o[1]));
  $('trayTit').innerHTML=`${c.n} · de ${obs[0][0].toFixed(0)} a 2080 &nbsp;
    <span style="font-weight:400;color:var(--tinta3);font-size:12px">las cinco ventanas
    medidas se separan ${F(mx-mn,2)} °C entre sí</span>`;
}

/* ── diagrama del método: seis pasos clicables ──
   Las tarjetas solo llevan título y un dato corto; el detalle va al panel de abajo.
   Meter dos líneas largas dentro de la tarjeta las desbordaba sobre las vecinas. */
const MICO={
  desc:'M12 3v11M7.5 10L12 14.5 16.5 10M4 18h16',
  cab:'M6 4h9l4 4v12H6zM15 4v4h4M9 12h7M9 16h5',
  med:'M4 19V9M9.5 19V5M15 19v-7M20.5 19v-4',
  mor:'M4 15c3-4 5-4 8 0s5 4 8 0M4 9c3-4 5-4 8 0s5 4 8 0',
  cmp:'M6 19V7M18 19V4M6 13h12M3 19h18',
  ver:'M4 12.5l5 5L20 6'};
const MCOL=['#1a4f6e','#2b6f9e','#3d8ab0','#7a9a86','#c78b3c','#bd491a'];
const MICN=['desc','cab','med','mor','cmp','ver'];
const MRES=['40 archivos EPW','8 760 h/archivo','~120 métricas','23 modelos GCM','2 métodos','1.59 pp máx'];

function metodo(){
  const W=1080,H=156, bw=(W-40)/6-12, bh=102, y=28;
  let s=`<svg viewBox="0 0 ${W} ${H}" style="width:100%;height:auto;display:block">`;
  PASOS.forEach((P,i)=>{
    const x=20+i*(bw+12), col=MCOL[i], act=(i===pasoSel);
    s+=`<g class="pg" opacity="${act?1:.65}" style="cursor:pointer" onclick="verPaso(${i})"
          onmousemove="hov(event,'Paso ${i+1} · ${P.t} — Clic para ver cifras y evidencias')"
          onmouseout="out()">
        <rect x="${x}" y="${y}" width="${bw}" height="${bh}" rx="10" fill="${act?'#ffffff':'#fcfaf6'}"
          stroke="${col}" stroke-width="${act?2.5:1.2}"/>
        <circle cx="${x+bw/2}" cy="${y-12}" r="14" fill="${col}"/>
        <text x="${x+bw/2}" y="${y-7}" text-anchor="middle" fill="#fff" font-size="12"
          font-weight="700">${i+1}</text>
        <path d="${MICO[MICN[i]]}" transform="translate(${x+bw/2-10},${y+14})"
          stroke="${col}" fill="none" stroke-width="1.8" stroke-linecap="round"
          stroke-linejoin="round"/>
        <text x="${x+bw/2}" y="${y+58}" text-anchor="middle" font-size="13.5" font-weight="700"
          fill="#12161f">${P.t}</text>
        <text x="${x+bw/2}" y="${y+78}" text-anchor="middle" font-size="11" font-weight="700"
          fill="${col}">${MRES[i]}</text>
        ${act?`<polygon points="${x+bw/2-7},${y+bh} ${x+bw/2+7},${y+bh} ${x+bw/2},${y+bh+7}" fill="${col}"/>`:''}
      </g>`;
    if(i<5) s+=`<path d="M${x+bw+1} ${y+bh/2}h10m-3-3 3 3-3 3" stroke="#988a6f"
          fill="none" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>`;
  });
  s+=`</svg>`;
  $('metodoPasos').innerHTML=s;
}

/* ── climograma: bandas y líneas, no barras ──
   Por horizonte: una banda semitransparente entre la mínima y la máxima medias
   diarias, y una línea sólida con la media mensual. La banda dice el rango que se
   vive cada día; la línea, el nivel del mes. */
const CGCOL={hoy:'#8a8378',a2030:'#d99b22',a2050:'#e2622f',a2080:'#b3261e'};
let cgVis={hoy:true,a2030:false,a2050:false,a2080:true};
function cgToggle(h){cgVis[h]=!cgVis[h];
  if(!HOR.some(x=>cgVis[x])) cgVis[h]=true; climograma();}
function cgSolo(h){HOR.forEach(x=>cgVis[x]=(x===h));climograma();}
function cgTodos(){HOR.forEach(x=>cgVis[x]=true);climograma();}

function climograma(){
  const c=D.ciudades.find(o=>o.n===sel), CG=c[escen].CG;
  const act=HOR.filter(h=>cgVis[h]);
  const M=['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'];
  const W=1160,H=560,ml=66,mr=132,mt=30,mb=76,iw=W-ml-mr,ih=H-mt-mb;
  // eje fijo sobre los CUATRO horizontes: no debe moverse al filtrar (ver D-22)
  const tod=HOR.flatMap(h=>[...CG[h].maxm,...CG[h].minm]);
  const y0=Math.floor(Math.min(...tod)-2), y1=Math.ceil(Math.max(...tod)+2);
  const X=i=>ml+i/11*iw, Y=v=>mt+ih-(v-y0)/(y1-y0)*ih;
  let s=`<svg viewBox="0 0 ${W} ${H}">`;
  const pasoY=(y1-y0)>26?4:2;
  for(let g=Math.ceil(y0/pasoY)*pasoY;g<=y1;g+=pasoY)
    s+=`<line class="gl" x1="${ml}" x2="${ml+iw}" y1="${Y(g)}" y2="${Y(g)}"/>
        <text class="lbl" x="${ml-10}" y="${Y(g)+4}" text-anchor="end">${g}</text>`;
  M.forEach((m,i)=>s+=`<line class="gl" x1="${X(i)}" x2="${X(i)}" y1="${mt}" y2="${mt+ih}"
      opacity=".55"/><text class="lbl2" x="${X(i)}" y="${mt+ih+22}" text-anchor="middle">${m}</text>`);
  act.forEach(h=>{
    const g=CG[h], col=CGCOL[h];
    const arriba=g.maxm.map((v,i)=>`${X(i).toFixed(1)},${Y(v).toFixed(1)}`).join(' ');
    const abajo=g.minm.map((v,i)=>`${X(i).toFixed(1)},${Y(v).toFixed(1)}`).reverse().join(' ');
    s+=`<polygon points="${arriba} ${abajo}" fill="${col}" opacity=".16"/>
        <polyline points="${arriba}" fill="none" stroke="${col}" stroke-width="1.4"
          stroke-dasharray="5 4" opacity=".85"/>
        <polyline points="${abajo}" fill="none" stroke="${col}" stroke-width="1.4"
          stroke-dasharray="5 4" opacity=".85"/>
        <polyline points="${g.media.map((v,i)=>X(i).toFixed(1)+','+Y(v).toFixed(1)).join(' ')}"
          fill="none" stroke="${col}" stroke-width="3" stroke-linejoin="round"/>`;
    g.media.forEach((v,i)=>s+=`<circle cx="${X(i)}" cy="${Y(v)}" r="3.6" fill="${col}"
          stroke="#fff" stroke-width="1.4"/>`);
    // etiqueta al final de cada serie
    s+=`<text class="val" x="${ml+iw+9}" y="${Y(g.media[11])+4}" fill="${col}"
          font-size="12.5">${HET[h]}</text>`;
  });
  // banda de lectura por mes
  for(let i=0;i<12;i++){
    const x0=X(i)-iw/22, an=iw/11;
    s+=`<rect x="${x0}" y="${mt}" width="${an}" height="${ih}" fill="transparent"
          onmousemove="hov(event,'<b>${M[i]}</b> · ${c.n}<br>`
      +act.map(h=>`${HET[h]}: media ${F(CG[h].media[i],1)} · ${F(CG[h].minm[i],1)} a ${F(CG[h].maxm[i],1)} °C`).join('<br>')
      +`')" onmouseout="out()"/>`;
  }
  s+=`<line class="ax" x1="${ml}" x2="${ml+iw}" y1="${mt+ih}" y2="${mt+ih}"/>
      <text class="lbl2" x="16" y="${mt+ih/2}" transform="rotate(-90 16 ${mt+ih/2})"
        text-anchor="middle">Temperatura de bulbo seco (°C)</text>
      <text class="lbl" x="${ml}" y="${H-14}">Hemisferio sur: verano en enero-marzo,
        invierno en junio-agosto.</text></svg>`;
  $('climo').innerHTML=s;
  $('climoTit').textContent=`${c.n} mes a mes · ${c.zona} · ${N(c.elev)} m`;

  // ── leyenda: qué es cada trazo, y el rango de cada horizonte encendido ──
  const guia=`<div class="cgGuia">
    <span><svg width="34" height="14"><line x1="1" y1="7" x2="33" y2="7" stroke="#3d4657"
      stroke-width="3"/></svg> Media del mes</span>
    <span><svg width="34" height="14"><rect x="1" y="2" width="32" height="10" rx="2"
      fill="#3d4657" opacity=".18"/><line x1="1" y1="3" x2="33" y2="3" stroke="#3d4657"
      stroke-width="1.3" stroke-dasharray="4 3"/><line x1="1" y1="11" x2="33" y2="11"
      stroke="#3d4657" stroke-width="1.3" stroke-dasharray="4 3"/></svg>
      Banda: mínima a máxima medias diarias</span></div>`;
  const rangos=act.map(h=>{
    const g=CG[h], mn=Math.min(...g.minm), mx=Math.max(...g.maxm);
    const iM=g.maxm.indexOf(mx), im=g.minm.indexOf(mn);
    return `<div class="cgRango" style="--c:${CGCOL[h]}">
      <b>${HET[h]}${D.interpolado.includes(h)?' · interp.':''}</b>
      <span>${F(mn,1)} a ${F(mx,1)} °C</span>
      <em>mín en ${M[im]} · máx en ${M[iM]} · amplitud ${F(mx-mn,1)} °C</em></div>`;}).join('');
  $('cgLeg').innerHTML=HOR.map(h=>
    `<button class="cgChip ${cgVis[h]?'on':''}" onclick="cgToggle('${h}')"
       ondblclick="cgSolo('${h}')" aria-pressed="${cgVis[h]}"
       title="Clic: encender o apagar · doble clic: ver solo este">
       <i style="background:${CGCOL[h]}"></i>${HET[h]}</button>`).join('')
    +`<button class="cgChip todos" onclick="cgTodos()">Todos</button>`;
  $('cgInfo').innerHTML=guia+`<div class="cgRangos">${rangos}</div>`;
}


/* Escala específica del dial solar: hacia 0 °C es azul y hacia 30 °C es rojo intenso */
function escalaSol(v){
  const t=Math.max(0,Math.min(1,v/30));
  const pal=[
    [0.00, [27,108,168]],   // 0 °C o menos: Azul intenso #1b6ca8
    [0.33, [82,162,197]],   // 10 °C: Azul cielo #52a2c5
    [0.60, [229,169,60]],   // 18 °C: Ámbar confort #e5a93c
    [0.80, [224,90,38]],    // 24 °C: Naranja térmico #e05a26
    [1.00, [186,18,18]]     // 30 °C+: Rojo intenso #ba1212
  ];
  for(let i=0;i<pal.length-1;i++){
    const [t0,c0]=pal[i], [t1,c1]=pal[i+1];
    if(t>=t0 && t<=t1){
      const f=(t-t0)/(t1-t0);
      const r=Math.round(c0[0]+(c1[0]-c0[0])*f);
      const g=Math.round(c0[1]+(c1[1]-c0[1])*f);
      const b=Math.round(c0[2]+(c1[2]-c0[2])*f);
      return `rgb(${r},${g},${b})`;
    }
  }
  return 'rgb(186,18,18)';
}

/* ── carátula: el sol de los doce meses ──
   Cada rayo es un mes. Va del radio de la mínima media diaria al de la máxima.
   Muestra la variación mensual para la ciudad seleccionada y responde a los botones de horizonte. */
let solH=0, solT=0, solPausa=true, solHover=-1, solAnimId=null;
function solAnim(){
  if(!solPausa){
    solT+=0.006;
    if(solT>=1){solT=0; solH=(solH+1)%HOR.length;}
    solDibuja();
    solAnimId=requestAnimationFrame(solAnim);
  }
}
function solDibuja(){
  const c=D.ciudades.find(o=>o.n===sel)||D.ciudades[0];
  const A=c.s245.CG[HOR[solH]], B=c.s245.CG[HOR[(solH+1)%HOR.length]];
  const k=ease(Math.min(solT*1.6,1));           // pausa al final de cada estado
  const M=['ENE','FEB','MAR','ABR','MAY','JUN','JUL','AGO','SEP','OCT','NOV','DIC'];
  const S=680, cx=S/2, cy=S/2, r0=100, r1=290;
  
  // Escala fija y absoluta de referencia común para todas las ciudades (-6 °C a 36 °C)
  const vmin=-6, vmax=36;
  const R=v=>r0+Math.max(0, Math.min(1, (v-vmin)/(vmax-vmin)))*(r1-r0);

  let s=`<svg viewBox="-46 -42 ${S+92} ${S+84}" role="img"
     aria-label="Sol de doce rayos: la temperatura mensual de ${c.n} en ${HET[HOR[solH]]}">`;

  // Anillos concéntricos de referencia con tinte sutil (azul en 0°, rojo en 30°)
  const anillos=[
    {t: 0, lbl: '0 °C', col: '#2b6f9e', dash: '3 3'},
    {t: 10, lbl: '10 °C', col: '#5a7f92', dash: '3 3'},
    {t: 20, lbl: 'Confort', col: '#a89c89', dash: '3 3'},
    {t: 30, lbl: '30 °C', col: '#bd491a', dash: '3 3'}
  ];

  // Definición de gradientes lineales para cada rayo
  s+=`<defs>`;
  for(let m=0;m<12;m++){
    const ang=(m/12)*Math.PI*2-Math.PI/2;
    const mx=A.maxm[m]+(B.maxm[m]-A.maxm[m])*k, mn=A.minm[m]+(B.minm[m]-A.minm[m])*k;
    const ra=R(mn), rb=R(mx);
    const x1=cx+Math.cos(ang)*ra, y1=cy+Math.sin(ang)*ra;
    const x2=cx+Math.cos(ang)*rb, y2=cy+Math.sin(ang)*rb;
    s+=`<linearGradient id="solRayGrad_${m}" x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="${escalaSol(mn)}"/>
      <stop offset="100%" stop-color="${escalaSol(mx)}"/>
    </linearGradient>`;
  }
  s+=`</defs>`;

  anillos.forEach(an=>{
    const r=R(an.t);
    s+=`<circle cx="${cx}" cy="${cy}" r="${r.toFixed(1)}" fill="none" stroke="${an.col}" stroke-width="1.1" stroke-dasharray="${an.dash}" opacity="0.6"/>`;
    s+=`<rect x="${(cx-26).toFixed(1)}" y="${(cy-r-7.5).toFixed(1)}" width="52" height="15" rx="3" fill="#f4f1ea" opacity="0.95"/>`;
    s+=`<text x="${cx}" y="${(cy-r+3.5).toFixed(1)}" text-anchor="middle" font-size="9.5" font-weight="600" fill="${an.col}" letter-spacing=".4">${an.lbl}</text>`;
  });

  for(let m=0;m<12;m++){
    const ang=(m/12)*Math.PI*2-Math.PI/2;
    const mx=A.maxm[m]+(B.maxm[m]-A.maxm[m])*k, mn=A.minm[m]+(B.minm[m]-A.minm[m])*k;
    const ra=R(mn), rb=R(mx), gr=solHover===m?1:.88;
    const x1=cx+Math.cos(ang)*ra, y1=cy+Math.sin(ang)*ra;
    const x2=cx+Math.cos(ang)*rb, y2=cy+Math.sin(ang)*rb;
    s+=`<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}"
          y2="${y2.toFixed(1)}" stroke="url(#solRayGrad_${m})" stroke-width="${solHover===m?32:26}"
          stroke-linecap="round" opacity="${gr}" style="cursor:pointer;transition:stroke-width .15s"
          onmouseenter="solHover=${m};solDibuja()" onmouseleave="solHover=-1;solDibuja()"
          onmousemove="hov(event,'<b>${M[m]}</b> · ${c.n} · ${HET[HOR[solH]]}<br>Mínima media: <b>${F(mn,1)} °C</b><br>Máxima media: <b>${F(mx,1)} °C</b><br>Oscilación: <b>${F(mx-mn,1)} °C</b>')"
          onmouseout="out()"/>`;
    const rt=r1+28;
    s+=`<text x="${(cx+Math.cos(ang)*rt).toFixed(1)}" y="${(cy+Math.sin(ang)*rt+4).toFixed(1)}"
          text-anchor="middle" font-size="13.5" letter-spacing="1.4"
          fill="${solHover===m?'#12161f':'#656f7e'}"
          font-weight="${solHover===m?'700':'400'}">${M[m]}</text>`;
  }
  const Tm=(A.media.reduce((a,b)=>a+b,0)/12)*(1-k)+(B.media.reduce((a,b)=>a+b,0)/12)*k;
  s+=`<circle cx="${cx}" cy="${cy}" r="${r0-10}" fill="#fbf9f5" stroke="#e2ddd2" stroke-width="1.2"/>
      <text x="${cx}" y="${cy-12}" text-anchor="middle" font-size="46" font-weight="700"
        fill="${escalaSol(Tm)}">${F(Tm,1)}°</text>
      <text x="${cx}" y="${cy+18}" text-anchor="middle" font-size="14" letter-spacing="2.4"
        fill="#656f7e">${HET[HOR[solH]].toUpperCase()}</text>
      <text x="${cx}" y="${cy+40}" text-anchor="middle" font-size="11.5" letter-spacing="1.6"
        fill="#9aa2ad">${c.n.toUpperCase()}</text></svg>`;
  $('heroViz').innerHTML=s;
  document.querySelectorAll('.solBtn').forEach((b,i)=>b.classList.toggle('on',i===solH));
}
function solIr(i){
  solH=i; solT=0; solPausa=true;
  if(solAnimId){cancelAnimationFrame(solAnimId); solAnimId=null;}
  $('solPlay').textContent='▶ Animar';
  solDibuja();
}
function solSeguir(){
  solPausa=!solPausa;
  $('solPlay').textContent=solPausa?'▶ Animar':'⏸ Pausar';
  if(!solPausa) solAnim();
  else if(solAnimId){cancelAnimationFrame(solAnimId); solAnimId=null;}
}

/* ── marco global IPCC y mapa mundial ── */
let ipccEsc='ssp126', ipccHz=2050, ipccPinSel=-1;

function escalaIPCC(dT){
  if(dT < 0.8) return '#fae27a';
  if(dT < 1.3) return '#f7b34e';
  if(dT < 1.8) return '#f09139';
  if(dT < 2.5) return '#ea7930';
  if(dT < 3.4) return '#d94326';
  if(dT < 4.5) return '#b01b22';
  if(dT < 6.0) return '#7a0c20';
  return '#4c0326';
}

function setIpccEsc(e){
  ipccEsc=e;
  document.querySelectorAll('#ipccEscen button').forEach(b=>b.classList.toggle('on',b.dataset.esc===e));
  ipccMapa();
  if(ipccPinSel>=0) verPin(ipccPinSel, false);
}

function setIpccHz(h){
  ipccHz=h;
  if($('ipccH2050')) $('ipccH2050').classList.toggle('on',h===2050);
  if($('ipccH2080')) $('ipccH2080').classList.toggle('on',h===2080);
  ipccMapa();
  if(ipccPinSel>=0) verPin(ipccPinSel, false);
}

function verPin(i, isClick=false){
  if(!D.ipcc || !D.ipcc.puntos || !D.ipcc.puntos[i]) return;
  if(isClick){
    ipccPinSel = (ipccPinSel === i ? -1 : i);
  }
  const curIdx = isClick && ipccPinSel === -1 ? 0 : (isClick ? ipccPinSel : i);
  const pt = D.ipcc.puntos[curIdx];
  const esc = D.ipcc.escenarios[ipccEsc];
  const dT_global = ipccHz===2050 ? esc.dT_2050 : esc.dT_2080;
  const dT_pt = dT_global * pt.m;
  if($('ipccPinDetail')){
    $('ipccPinDetail').innerHTML=`<b>📍 ${pt.n}:</b> Anomalía proyectada <b>+${F(dT_pt,1)} °C</b> en ${ipccHz} (${esc.nombre.split('·')[0]}). ${pt.desc}`;
    $('ipccPinDetail').classList.add('activo');
  }
  document.querySelectorAll('.ipccPin').forEach((el, idx) => {
    el.classList.toggle('on', idx === (ipccPinSel >= 0 ? ipccPinSel : i));
  });
}

function ipccMapa(){
  if(!D.ipcc) return;
  const ipcc=D.ipcc;
  const esc=ipcc.escenarios[ipccEsc];
  const dT_global = ipccHz===2050 ? esc.dT_2050 : esc.dT_2080;
  
  if($('ipccMapTit')) $('ipccMapTit').innerHTML=`Calentamiento Global Proyectado: ${esc.nombre} (Año ${ipccHz})`;
  if($('ipccMapSubtit')) $('ipccMapSubtit').innerHTML=`${esc.desc} · Concentración esperada de CO₂: ${esc.co2_2100}`;
  const p10 = ipccHz===2050 ? esc.p10_2050 : esc.p10_2080;
  const p90 = ipccHz===2050 ? esc.p90_2050 : esc.p90_2080;

  if($('ipccGlobalVal')) $('ipccGlobalVal').innerHTML=`+${F(dT_global,1)} °C <span style="font-size:12px;font-weight:600;color:var(--tinta3)">[P10: +${F(p10,1)}°, P90: +${F(p90,1)}°]</span>`;

  const W=ipcc.ancho, H=ipcc.alto;
  let s=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Mapa mundial de calentamiento proyectado IPCC AR6">`;
  
  // Fondo de océano con curvatura
  s+=`<rect x="0" y="0" width="${W}" height="${H}" rx="12" fill="#eaf2f8" stroke="#d5e2ec" stroke-width="1"/>`;
  
  // Líneas de latitud de referencia
  [-66.5, -23.5, 0, 23.5, 66.5].forEach(lat=>{
    const y=H/2 - (lat/90)*(H*0.44);
    s+=`<line x1="24" x2="${W-24}" y1="${y}" y2="${y}" stroke="${lat===0?'rgba(18,22,31,.2)':'rgba(18,22,31,.08)'}" stroke-width="${lat===0?1.2:0.8}" stroke-dasharray="${lat===0?'none':'4 3'}"/>`;
  });

  // Países coloreados según anomalía térmica regional
  ipcc.paises.forEach(p=>{
    const dT_pais = dT_global * p.m;
    const col = escalaIPCC(dT_pais);
    s+=`<path d="${p.d}" fill="${col}" stroke="#ffffff" stroke-width="0.5" opacity="0.94" style="cursor:pointer;transition:opacity .15s"
          onmouseenter="this.style.opacity='1'" onmouseleave="this.style.opacity='0.94'"
          onmousemove="hov(event,'<b>${p.n}</b><br>Calentamiento proyectado: <b>+${F(dT_pais,1)} °C</b><br>Escenario: ${esc.nombre.split('·')[0]} (${ipccHz})')"
          onmouseout="out()"/>`;
  });

  // Puntos clave de análisis (Perú, Amazonía, Ártico, Océanos)
  ipcc.puntos.forEach((pt,idx)=>{
    const dT_pt = dT_global * pt.m;
    const col = escalaIPCC(dT_pt);
    const isAct = (idx === ipccPinSel);
    s+=`<g class="ipccPin ${isAct?'on':''}"
          onclick="verPin(${idx}, true)"
          onmouseenter="verPin(${idx}, false)"
          onmouseleave="if(ipccPinSel>=0){verPin(ipccPinSel, false)}">
          <circle cx="${pt.x}" cy="${pt.y}" r="18" fill="transparent"/>
          <circle class="pinOuter" cx="${pt.x}" cy="${pt.y}" r="8.5"/>
          <circle class="pinCore" cx="${pt.x}" cy="${pt.y}" r="5.2" fill="${col}" stroke="#12161f" stroke-width="1.8"/>
          <circle cx="${pt.x}" cy="${pt.y}" r="1.6" fill="#ffffff"/>
        </g>`;
  });

  s+=`</svg>`;
  if($('ipccWorldMap')) $('ipccWorldMap').innerHTML=s;

  // Actualizar las tarjetas de los 4 escenarios en orden ssp1, ssp2, ssp3, ssp5
  if($('sspCardsGrid')){
    const keys=['ssp126','ssp245','ssp370','ssp585'];
    $('sspCardsGrid').innerHTML=keys.map(k=>{
      const e=ipcc.escenarios[k];
      const dT = ipccHz===2050 ? e.dT_2050 : e.dT_2080;
      const kP10 = ipccHz===2050 ? e.p10_2050 : e.p10_2080;
      const kP90 = ipccHz===2050 ? e.p90_2050 : e.p90_2080;
      const isAct = k===ipccEsc;
      return `<div class="sspCard ${isAct?'on':''}" onclick="setIpccEsc('${k}')" style="cursor:pointer">
        <h5 style="color:${isAct?'var(--acento)':'var(--tinta)'}">${e.nombre.split('·')[0]}</h5>
        <div class="sspCo2">CO₂: ${e.co2_2100} · <b>+${F(dT,1)} °C en ${ipccHz}</b></div>
        <div style="font-size:11.5px;color:var(--calor-tx);font-weight:600;margin-bottom:6px">Dispersión intermodelo: [+${F(kP10,1)}° a +${F(kP90,1)}°]</div>
        <p>${e.desc}</p>
      </div>`;
    }).join('');
  }
}

/* ── didáctica de impacto térmico: 4 niveles x 3 pilares visuales (Cuerpo, Edificio, Entorno) ── */
let impNivel = 's20'; // Por defecto +2.0 °C (trayectoria central 2050)

const IMP_DATA = {
  s10: {
    nivel: '+1.0 °C',
    cls: 'n1',
    color: '#9e6a00',
    tit: 'Línea Base Actual (Perú Hoy)',
    sub: 'Nivel ya alcanzado en el territorio nacional respecto a la era preindustrial.',
    cuerpo: {
      tit: 'Fisiología del Cuerpo Humano',
      estado: 'Termorregulación eficiente · Ritmo cardíaco recuperador nocturno',
      bullets: [
        '<b>Evaporación cutánea libre:</b> El gradiente de vapor permite que el sudor disipe el calor metabólico.',
        '<b>Recuperación nocturna:</b> Temperaturas de noche inferiores a 18 °C previenen el estrés cardiovascular.',
        '<b>Estrés térmico esporádico:</b> Olas de calor acotadas a pocos días en verano.'
      ]
    },
    edificio: {
      tit: 'Física de la Edificación',
      estado: 'Techos a 48 °C · Ventilación pasiva y sombras eficientes',
      bullets: [
        '<b>Arquitectura pasiva efectiva:</b> Aleros, persianas y masa térmica mantienen el confort interior.',
        '<b>Enfriamiento nocturno viable:</b> La ventilación cruzada de noche purga el calor acumulado en muros.',
        '<b>Demanda de refrigeración baja:</b> Ventiladores de techo son suficientes en la mayor parte del año.'
      ]
    },
    entorno: {
      tit: 'Entorno, Glaciares y Recursos',
      estado: 'Glaciares tropicales en retroceso (~35 %) · Cuencas reguladas',
      bullets: [
        '<b>Masa glaciar andina:</b> Presencia de glaciares por encima de los 4 800 msnm.',
        '<b>Caudal de estiaje sostenido:</b> Aporte hídrico estacional regular en las cuencas del Pacífico.',
        '<b>Surgencia de Humboldt activa:</b> Aguas costeras frías que sostienen la biomasa pesquera.'
      ]
    }
  },

  s15: {
    nivel: '+1.5 °C',
    cls: 'n2',
    color: '#b24b00',
    tit: 'Meta del Acuerdo de París (SSP1-2.6 · 2040–2050)',
    sub: 'Trayectoria de mitigación acelerada con estabilización de emisiones.',
    cuerpo: {
      tit: 'Fisiología del Cuerpo Humano',
      estado: 'Efecto vapor costero · Fatiga térmica y sensación de +3 °C',
      bullets: [
        '<b>Efecto vapor en la costa:</b> En Lima y Trujillo, la humedad relativa (>80 %) dificulta evaporar el sudor.',
        '<b>Sensación térmica amplificada:</b> En la piel se percibe como un aumento de hasta +3.0 °C.',
        '<b>Primeras noches cálidas:</b> Dificultad para conciliar el sueño sin ventilación continua.'
      ]
    },
    edificio: {
      tit: 'Física de la Edificación',
      estado: 'Techos a 55 °C · Duplicación de grados-hora de refrigeración',
      bullets: [
        '<b>Duplicación de grados-hora:</b> La energía térmica requerida para refrigerar se duplica.',
        '<b>Sobrecalentamiento en techos ligeros:</b> Calaminas alcanzan 55 °C e irradian calor al interior.',
        '<b>Ineficacia de sombras simples:</b> Se vuelve indispensable el aislamiento térmico continuo.'
      ]
    },
    entorno: {
      tit: 'Entorno, Glaciares y Recursos',
      estado: 'Pérdida del 50 % de masa glaciar · Olas de calor marinas',
      bullets: [
        '<b>Pico de agua superado (Peak Water):</b> Descenso progresivo en el caudal de estiaje en ríos de la costa.',
        '<b>Calentamiento del mar costero:</b> Aguas superficiales a 18 °C+ que desplazan la anchoveta al fondo.',
        '<b>Pérdida de nevados menores:</b> Extinción de glaciares por debajo de los 5 000 msnm.'
      ]
    }
  },

  s20: {
    nivel: '+2.0 °C',
    cls: 'n3',
    color: '#b3261e',
    tit: 'Umbral Crítico Proyectado (SSP2-4.5 · 2050)',
    sub: 'Trayectoria central del IPCC hacia 2050 si las emisiones globales no caen drásticamente.',
    cuerpo: {
      tit: 'Fisiología del Cuerpo Humano',
      estado: 'Noches tropicales (>20 °C) · Sobreesfuerzo cardiovascular crónico',
      bullets: [
        '<b>Noches tropicales permanentes (>20 °C):</b> El cuerpo no logra disipar calor durante el sueño.',
        '<b>Sobreesfuerzo cardiovascular crónico:</b> El corazón bombea al máximo toda la noche para enfriar la piel.',
        '<b>Deterioro cognitivo diurno:</b> Insomnio crónico que afecta el rendimiento escolar y laboral.'
      ]
    },
    edificio: {
      tit: 'Física de la Edificación',
      estado: 'Techos a 65 °C · Colapso del enfriamiento nocturno pasivo',
      bullets: [
        '<b>Colapso del enfriamiento nocturno:</b> El aire de noche (>20 °C) no logra desahogar los muros.',
        '<b>Aire acondicionado sanitario:</b> La climatización artificial deja de ser confort y pasa a salud.',
        '<b>Factura eléctrica triplicada:</b> Fuerte estrés sobre las redes de distribución urbana.'
      ]
    },
    entorno: {
      tit: 'Entorno, Glaciares y Recursos',
      estado: 'Deshielo irreversible bajo 5 200 m · Estrés hídrico en la costa',
      bullets: [
        '<b>Deshielo crítico irreversible:</b> Colapso casi total de glaciares de la Cordillera Central y Yauyos.',
        '<b>Racionamiento en época seca:</b> Grave merma de caudales para agua potable y agricultura costera.',
        '<b>Impacto económico:</b> Descenso en la captura de anchoveta y producción agroexportadora.'
      ]
    }
  },

  s30: {
    nivel: '+3.0 °C+',
    cls: 'n4',
    color: '#910b28',
    tit: 'Caso de Estrés Severo (SSP5-8.5 · 2080)',
    sub: 'Trayectoria extrema de combustibles fósiles sin control hacia fines de siglo.',
    cuerpo: {
      tit: 'Fisiología del Cuerpo Humano',
      estado: 'Límite de bulbo húmedo (28–30 °C+) · Riesgo de golpe de calor letal',
      bullets: [
        '<b>Límite de bulbo húmedo superado:</b> El aire saturado impide al 100% la disipación del calor metabólico.',
        '<b>Riesgo letal en reposo:</b> Sin climatización activa, la temperatura interna supera 40 °C en horas.',
        '<b>Mortalidad extrema:</b> Emergencia sanitaria recurrente en poblaciones de selva y costa norte.'
      ]
    },
    edificio: {
      tit: 'Física de la Edificación',
      estado: 'Viviendas inhabitables por la tarde · Sobrecarga y apagones en la red',
      bullets: [
        '<b>Viviendas inhabitables:</b> Casas tradicionales sin aislamiento se transforman en hornos (>36 °C).',
        '<b>Consumo energético desbordado:</b> Demanda de climatización multiplicada por 4 o 5.',
        '<b>Apagones masivos:</b> Colapso y cortes de suministro en subestaciones eléctricas urbanas.'
      ]
    },
    entorno: {
      tit: 'Entorno, Glaciares y Recursos',
      estado: 'Extinción masiva de glaciares (>85 %) · Severo racionamiento hídrico',
      bullets: [
        '<b>Extinción glaciar en el Perú:</b> Desaparición prácticamente total del hielo en la Cordillera Blanca.',
        '<b>Crisis hídrica metropolitana:</b> Racionamiento severo y déficit crónico en la cuenca del río Rímac.',
        '<b>Desertificación acelerada:</b> Colapso de valles agrícolas costeños e incendios forestales en sierra.'
      ]
    }
  }
};

function setImpactoNivel(k){
  impNivel = k;
  document.querySelectorAll('#impCtrl .impBtn').forEach(b => b.classList.toggle('on', b.dataset.imp === k));
  impactoDibuja();
}

function impactoDibuja(){
  const d = IMP_DATA[impNivel];
  if(!d) return;

  if($('impHeaderBox')){
    $('impHeaderBox').innerHTML = `
      <div>
        <h3>${d.tit}</h3>
        <p>${d.sub}</p>
      </div>
      <div class="impHeaderBadge" style="background:${d.cls==='n1'?'#fdf2d0':(d.cls==='n2'?'#fde3c7':(d.cls==='n3'?'#fad1bc':'#f7bcc4'))};color:${d.color}">${d.nivel}</div>
    `;
  }

  if($('impGrid3')){
    $('impGrid3').innerHTML = `
      <!-- Tarjeta 1: Cuerpo Humano -->
      <div class="impColCard">
        <h4>${d.cuerpo.tit}</h4>
        <div class="impColEstado" style="color:${d.color}">${d.cuerpo.estado}</div>
        <ul class="impUl">
          ${d.cuerpo.bullets.map(b => `<li class="impLi"><span class="impLiDot" style="background:${d.color}"></span><div>${b}</div></li>`).join('')}
        </ul>
      </div>

      <!-- Tarjeta 2: Física de la Edificación -->
      <div class="impColCard">
        <h4>${d.edificio.tit}</h4>
        <div class="impColEstado" style="color:${d.color}">${d.edificio.estado}</div>
        <ul class="impUl">
          ${d.edificio.bullets.map(b => `<li class="impLi"><span class="impLiDot" style="background:${d.color}"></span><div>${b}</div></li>`).join('')}
        </ul>
      </div>

      <!-- Tarjeta 3: Entorno y Recursos -->
      <div class="impColCard">
        <h4>${d.entorno.tit}</h4>
        <div class="impColEstado" style="color:${d.color}">${d.entorno.estado}</div>
        <ul class="impUl">
          ${d.entorno.bullets.map(b => `<li class="impLi"><span class="impLiDot" style="background:${d.color}"></span><div>${b}</div></li>`).join('')}
        </ul>
      </div>
    `;
  }
}

/* ── arranque ── */
portada(); pintar(hz,hz,1); barras(); nube(); vintage(); converg(); solDibuja(); ipccMapa(); impactoDibuja();
