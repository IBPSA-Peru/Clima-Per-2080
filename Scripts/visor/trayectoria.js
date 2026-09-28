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
