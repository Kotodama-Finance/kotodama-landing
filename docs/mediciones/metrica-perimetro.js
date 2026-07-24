window.__setup = () => {
  const N = 300;
  // DOS lienzos: uno vacío para leer el alfa (la silueta exacta) y otro
  // prellenado con el fondo real para leer color. Dibujar sobre un lienzo vacío
  // hacía que "afuera" fuese transparente (luminancia 0) en vez del fondo, y que
  // el antialias dorado del borde se contara como fondo brillante.
  const c2 = document.createElement('canvas'); c2.width = N; c2.height = N;
  const ctx = c2.getContext('2d', { willReadFrequently: true });
  const c3 = document.createElement('canvas'); c3.width = N; c3.height = N;
  const ctxB = c3.getContext('2d', { willReadFrequently: true });
  const L = (r,g,b) => 0.2126*r + 0.7152*g + 0.0722*b;

  window.__pose = (cube, cv, rx, ry, depths, umbrales) => {
    cube.setRotation(rx, ry); cube.render();
    ctx.clearRect(0,0,N,N); ctx.drawImage(cv,0,0,N,N);
    const d = ctx.getImageData(0,0,N,N).data;          // alfa = silueta
    // fondo real: el color computado detrás del escenario en la página
    ctxB.fillStyle = window.__bg; ctxB.fillRect(0,0,N,N); ctxB.drawImage(cv,0,0,N,N);
    const dc = ctxB.getImageData(0,0,N,N).data;        // color compuesto
    const A = (x,y) => d[(y*N+x)*4+3];
    const dentro = (x,y) => x>=0 && y>=0 && x<N && y<N && A(x,y) > 200;

    // perimetro 4-conexo: pixel del objeto con algun vecino fuera
    const per = [];
    for (let y=1; y<N-1; y++) for (let x=1; x<N-1; x++) {
      if (!dentro(x,y)) continue;
      if (dentro(x+1,y) && dentro(x-1,y) && dentro(x,y+1) && dentro(x,y-1)) continue;
      // normal hacia adentro por gradiente de la mascara en ventana 5x5
      let nx=0, ny=0;
      for (let j=-2;j<=2;j++) for (let i=-2;i<=2;i++) if (dentro(x+i,y+j)) { nx+=i; ny+=j; }
      const m = Math.hypot(nx,ny) || 1;
      per.push({x, y, nx: nx/m, ny: ny/m});
    }
    if (per.length < 20) return null;

    const res = {};
    for (const prof of depths) {
      const dl = [];              // |dL| por punto del perimetro
      const bgs = [];             // luminancia del fondo local
      for (const p of per) {
        const ix = Math.round(p.x + p.nx*prof), iy = Math.round(p.y + p.ny*prof);
        // ADENTRO: exigir alfa 255. Con alfa parcial el pixel es mezcla de cubo
        // y fondo, y el contraste sale falsamente bajo en todo el contorno.
        if (!dentro(ix,iy) || d[(iy*N+ix)*4+3] < 255) { dl.push(null); continue; }
        // AFUERA: caminar hacia afuera hasta el primer pixel con alfa 0. El
        // antialias del borde mide 1-3px y en angulos rasantes mas; tomarlo como
        // fondo fue lo que dio "fondo" entre 4 y 50 en una pagina plana.
        let ox=-1, oy=-1;
        for (let k=3; k<=14; k++) {
          const cx = Math.round(p.x - p.nx*k), cy = Math.round(p.y - p.ny*k);
          if (cx<0||cy<0||cx>=N||cy>=N) break;
          if (d[(cy*N+cx)*4+3] === 0) { ox=cx; oy=cy; break; }
        }
        if (ox < 0) { dl.push(null); continue; }
        const i = (iy*N+ix)*4, o = (oy*N+ox)*4;
        // FONDO LOCAL, medido justo por fuera sobre la composición real
        const lin = L(dc[i],dc[i+1],dc[i+2]), lout = L(dc[o],dc[o+1],dc[o+2]);
        bgs.push(lout);
        dl.push(Math.abs(lin - lout));
      }
      const validos = dl.filter(v => v !== null);
      if (!validos.length) continue;
      const orden = [...validos].sort((a,b)=>a-b);
      const salida = { perim: per.length, medianaDL: +orden[Math.floor(orden.length/2)].toFixed(1),
                       bgMin: +Math.min(...bgs).toFixed(1), bgMax: +Math.max(...bgs).toFixed(1) };
      for (const u of umbrales) {
        const falla = dl.map(v => v !== null && v < u);
        const pct = 100 * falla.filter(Boolean).length / validos.length;
        // tramo contiguo mas largo: componentes conexas (8-vec) sobre los que fallan
        const idx = new Map(); per.forEach((p,k)=>idx.set(p.x+','+p.y,k));
        const visto = new Uint8Array(per.length); let mayor = 0;
        for (let k=0;k<per.length;k++) {
          if (!falla[k] || visto[k]) continue;
          let n = 0; const pila = [k]; visto[k] = 1;
          while (pila.length) {
            const q = pila.pop(); n++;
            const pq = per[q];
            for (let j=-1;j<=1;j++) for (let i=-1;i<=1;i++) {
              const v = idx.get((pq.x+i)+','+(pq.y+j));
              if (v !== undefined && falla[v] && !visto[v]) { visto[v]=1; pila.push(v); }
            }
          }
          if (n > mayor) mayor = n;
        }
        salida['u'+u] = { pct: +pct.toFixed(1), contig: +(100*mayor/validos.length).toFixed(1) };
      }
      res['d'+prof] = salida;
    }
    return res;
  };

  window.__barrerRx = (rx, depths, umbrales) => {
    const cube = window.__cube, cv = document.querySelector('#stage canvas');
    const acc = {};
    for (let ry=0; ry<360; ry+=15) {
      const r = window.__pose(cube, cv, rx, ry, depths, umbrales);
      if (!r) continue;
      for (const dk in r) {
        acc[dk] = acc[dk] || { peorPct:{}, peorContig:{}, peorRy:{}, medianas:[], bgMin:1e9, bgMax:-1e9 };
        const a = acc[dk], s = r[dk];
        a.medianas.push(s.medianaDL);
        a.bgMin = Math.min(a.bgMin, s.bgMin); a.bgMax = Math.max(a.bgMax, s.bgMax);
        for (const u of umbrales) {
          const k='u'+u;
          if (!(k in a.peorPct) || s[k].pct > a.peorPct[k]) { a.peorPct[k]=s[k].pct; a.peorRy[k]=ry; }
          if (!(k in a.peorContig) || s[k].contig > a.peorContig[k]) a.peorContig[k]=s[k].contig;
        }
      }
    }
    for (const dk in acc) {
      const m = acc[dk].medianas.sort((a,b)=>a-b);
      acc[dk].medianaDL = +m[Math.floor(m.length/2)].toFixed(1);
      delete acc[dk].medianas;
    }
    return { rx, ...acc };
  };
  return 'listo';
};
