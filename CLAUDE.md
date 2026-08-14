# CLAUDE.md — Kotodama Finance

Contexto permanente del proyecto. Sobrevive a la compactación y al reinicio de
sesión. Si algo de acá contradice lo que parece razonable a primera vista, gana
esto: cada punto está donde está porque ya se probó lo contrario y falló.

Complementa al `README.md`, que documenta el sitio para cualquiera. Este archivo
documenta **las decisiones y su porqué**, que es lo que se pierde al compactar.

---

# Compact instructions

Al compactar, preservar siempre:

1. **Las decisiones cerradas y su motivo** (sección siguiente). El motivo importa
   más que la decisión: sin él, alguien las "arregla" y reintroduce el bug.
2. **El estado de los cabos abiertos**, con lo que ya se midió de cada uno.
3. **El flujo de guardas antes de commitear**, y que ninguna se saltea.
4. **Los hallazgos de método**: qué métricas engañaron y por qué. Están al final.

Se puede descartar: el detalle de cómo se llegó a cada número, los intentos
fallidos ya corregidos, y las capturas intermedias.

---

## Estado

- Rama de trabajo: **`redesign-trust`**. `rebuild-static` está congelada.
- **La vista explotada del cubo está INTEGRADA acá (2026-08-05)**: el merge
  `cube-exploded` → `redesign-trust` lo decidió explícitamente el autor, tras
  dos verificaciones previas (móvil emulado y no-divergencia). Fue
  fast-forward sobre `0693216` — la rama venía rebaseada — con las cuatro
  guardas corridas DESPUÉS del merge. **La rama `cube-exploded` se borró**
  (local y origin): tras el fast-forward no tenía historia propia, y un
  puntero viejo se lee como trabajo pendiente que no existe. El registro
  completo de sus decisiones (las cinco tandas) está en la sección de la
  vista explotada, más abajo.
- **`main` no se toca a mano — la escribe solo `tools/make-deploy.py`**.
  Publica kotodamafinance.com, y **desde el 2026-08-06 sirve EL SITIO NUEVO:
  LA PUBLICACIÓN YA OCURRIÓ** — deploy `824fada` generado del fuente
  `6dc8214` (tag `v1-published`), verificado en el dominio real.
- El sitio es estático: sin backend, sin frameworks, sin build step.
- Último cierre: **2026-08-14 (cierra el día, después del ensayo): LA COPIA
  DERIVADA DE CLAUDE.md EN ONEDRIVE + LA REGLA DE CITAR EL REGISTRO — SIN
  deploy: el artefacto de main NO cambió.** El problema (pedido del autor,
  con evidencia): el Claude del chat de diseño NO llega a C:\Dev — su
  alcance es la carpeta de Claude en OneDrive — y armaba prompts a ciegas
  sobre el archivo que tiene las respuestas: en una sola sesión preguntó
  TRES cosas ya registradas (el criterio de tags, el sitemap en robots.txt,
  el charset), tres investigaciones redundantes. Lo nuevo: **la copia
  ENTERA de CLAUDE.md, generada por `tools/make-copia-claudemd.py`** en la
  carpeta de Kotodama Finance de OneDrive (`kotodama_CLAUDE_copia.md`, al
  lado del context.md), con encabezado DERIVADA que declara fecha, commit y
  título del fuente, **gatillo en el COMMIT** — no en el deploy: CLAUDE.md
  cambia en tandas sin deploy, el punto del autor — y **el olvido cazado
  por check-structure** (compara la copia contra HEAD:CLAUDE.md; en otra
  máquina sin OneDrive se omite con aviso). Entera y no extracto: un
  criterio de selección es el que deriva. Probada en verde y en rojo (17
  casos) y pasada por revisión adversarial (3 lentes + refutadores): 2
  hallazgos confirmados por reproducción, los 2 corregidos antes de
  commitear — el encabezado ahora se verifica RECONSTRUYÉNDOLO con la
  plantilla compartida del generador, y la lectura fallida en OneDrive
  degrada a rojo con nombre — ver la decisión nueva, primera de la lista. Y **la regla de citar el registro** entró a «Otras reglas
  vigentes» (pedido del autor): ante una pregunta sobre el repo, si ya está
  registrado se responde CITÁNDOLO — «esto ya estaba escrito en X» — no
  re-derivándolo. Guardas: structure y modes en verde.
- Último cierre anterior: **2026-08-14 (después del título del fuente): EL
  ENSAYO DEL ROLLBACK EN
  SECO — EJECUTADO ENTERO, con el dominio intacto (verificado byte a byte
  después del push).** Decisión del autor: variante en seco; sus dos
  razones extra quedaron en el README junto a la variante en vivo (la
  ventana «15-30 min» es la del caso feliz — el precedente del deploy 2 la
  vuelve «hasta un día» si la cola de Pages se traba, y ahí perder la
  verificación de Search Console deja de ser improbable—, y el IMAJ viejo
  servido en /method/ durante la ventana es un error citable en la página
  que abre un reclutador). Los cuatro pasos, cada uno con su evidencia:
  **(1)** `--fuente v1-published` REAL — el commit de rollback `d46ffa0`
  en main local (Fuente `6dc8214`, cuatro avisos esperables, «main
  intacta» contra la Fuente del deploy 11 antes de apilar; y el formato
  nuevo del mensaje ESTRENÓ con un rollback: «Publicar: La rama de
  deploy...», el título del fuente de aquel día). **(2)** la preview del
  sitio VIEJO verificada 22/22: byte a byte contra la punta-rollback, SIN
  la meta de Search Console y SIN JSON-LD (confirmado en frío), la flecha
  con href, /sitemap/ + seguros + favicon-192 en 404, toushin.or.jp de
  vuelta en /method/, sitemap de 13 URLs, notas en 404, y CERO comentarios
  — el stripper VIGENTE transforma también un fuente viejo. **(3)** la
  VUELTA desde HEAD: `verificar_main_intacta` vio el ROLLBACK en la punta,
  dio «intacta» regenerando desde v1-published — el detector ejercido en
  el estado exacto de una emergencia real — y apiló `d619e20`. **(4)** la
  preview del estado restaurado verificada 15/15, con LA PRUEBA DURA: el
  OID del árbol de la vuelta == el OID del árbol del deploy 11
  (restauración EXACTA, no aproximada) — Search Console, JSON-LD, la
  flecha-div y las tres rutas de vuelta. El push publicó la punta (árbol
  idéntico al servido — el dominio no vio ni un byte distinto, verificado
  en vivo al primer intento) y los dos commits del ensayo quedaron en la
  historia de main como registro fechado. **LO QUE EL ENSAYO NO PROBÓ,
  escrito a pedido del autor**: que Pages construya y sirva un árbol viejo
  (la única fase no ensayada — la de menor incertidumbre y toda la
  exposición), y el loop humano bajo presión. Guardas: structure, modes y
  pendulum (0.0959) en verde antes del push.
- Último cierre anterior: **2026-08-14 (todavía más tarde): el título del fuente en
  el mensaje del deploy — SIN deploy: el artefacto de main NO cambió; el
  formato estrena con el próximo.** El autor aceptó ENTERA la refutación
  del esquema last-good y cerró: **los tags quedan como están**, y el
  arreglo del menú ilegible es el NOMBRE en el mensaje — la primera línea
  del commit de deploy pasa a ser «Publicar: <título del fuente>», con lo
  que `git log --oneline main` es el menú de rollback legible.
  VERIFICADO ANTES DE TOCAR, como pidió: el detector de hotfix y
  `verificar_main_intacta` NO dependen de la primera línea (leen solo la
  línea `Fuente:` anclada y comparan árboles). Probado en CLON AISLADO
  (T1-T5): título normal y raro (kanji, comillas, %, largo, y un
  «Fuente: <hash40>» adentro que NO fabrica marca), hotfix frenando,
  retrigger «intacta», fuente sin título cayendo al formato viejo. Los
  deploys viejos conservan su mensaje — la historia no se reescribe. Ver
  el bullet nuevo en la decisión de la rama de deploy; el README
  («Rollback») quedó al día. Guardas: check-structure y --solo-verificar
  en verde.
- Último cierre anterior: **2026-08-14 (más tarde): la previsualización del
  artefacto — SIN deploy: el artefacto de main NO cambió.** El hueco que
  cierra (pedido del autor): desde el deploy 8 EL SERVIDO NO ES EL FUENTE
  y no había forma humana de VER el sitio como va a quedar antes del push.
  Lo nuevo: **`python tools/make-deploy.py --previsualizar`** sirve la
  punta LOCAL de main en :8001 desde un worktree efímero — ver el bullet
  nuevo en la decisión de la rama de deploy, que registra las TRES trampas
  medidas (el autocrlf del checkout que metía 288 CRLF, el bind de Windows
  que NO detecta el puerto ocupado — wildcard y loopback conviven y la
  preview robaba el tráfico de localhost—, y el buffer del encabezado). El
  procedimiento del README pasó a SIETE pasos: el 4 es la previsualización
  humana, y dice explícito que se navega EL ARTEFACTO, no el árbol de
  trabajo. Probado ejecutando en verde y en rojo, y pasado por revisión
  adversarial (3 lentes + refutadores): 10 hallazgos confirmados por
  reproducción, los 10 corregidos antes de commitear — el detalle vive en
  el bullet de la decisión. `--solo-verificar` sigue exit 0. **Y la pregunta de los TAGS DE ROLLBACK quedó CONTESTADA al
  autor en el chat, SIN implementar (su instrucción)**: el criterio
  vigente está escrito (hitos, no rutina; un tag no se mueve), los dos
  tags viejos ya no son puntos de retorno operativos (son historia — un
  rollback ahí perdería Search Console, JSON-LD, favicons y las
  correcciones de bugs), y la recomendación fue ponerle NOMBRE a cada
  deploy en el MENSAJE del commit de main (hoy los once dicen lo mismo) en
  vez de un tag móvil «last-good», que acá es ceremonia. *(La decidió el
  mismo día: aceptada e implementada — ver el cierre de arriba.)*
- Antes, el 2026-08-14: **la flecha del hero sin enlace — EL
  UNDÉCIMO DEPLOY, EJECUTADO ENTERO Y VERIFICADO EN VIVO: deploy
  `c9740a1` de fuente `87eb8b0`.** Decisión del autor: la flecha del hero
  dejó de ser el enlace a #cube y es un `<div>` decorativo — aria-hidden,
  sin destino, visualmente idéntico. El motivo: el camino hacia abajo es
  SCROLLEAR, y el enlace PERJUDICABA a quien lo usaba — el aterrizaje
  calibrado de #cube saltea el encabezado del cubo (correcto desde la
  nav, que ya sabe adónde va; malo para quien baja por primera vez);
  «The Cube» sigue en la nav. Con el enlace se fueron el aria-label
  «Scroll to the cube», el `:hover` dorado y la tabulación — **ver la
  decisión de anclas, actualizada**. main.js no dependía del enlace
  (cero referencias, verificado ANTES de sacarlo) y no se tocó chrome
  comparado (baseline 36 intacto, sin regenerar). De paso: el comentario
  del token `--c-text-muted-2` listaba a la flecha como consumidor y era
  FALSO (va en mist con alfa) — corregido; como vive dentro del `:root`,
  la og-image se regeneró DOS veces con PNG byte-idéntico (sha256) y
  lock resellado. La revisión adversarial pre-deploy (4 lentes +
  refutadores) dio el cambio LIMPIO en accesibilidad, CSS/JS y guardas,
  y confirmó 3 hallazgos de REGISTRO, corregidos antes de commitear: la
  lista «corregida» del token seguía incompleta (3 de 5 consumidores);
  «dieciséis páginas» en dos comentarios era el conteo-que-caduca que el
  deploy 8 prohibió (quedó «todas las páginas» — el número además era
  falso contra el fuente, que tiene 18 con nav); y «deploy 11» estaba
  escrito ANTES de que el deploy existiera (la convención numera solo
  deploys ejecutados). Guardas: cinco en verde (pendulum 0.0963, ready
  `2` esperado) + check-modes contra el árbol real de main servido en
  :8000. Verificado en vivo 23/23: portada Y styles.css BYTE A BYTE
  idénticos a los blobs de main, la flecha servida como `<div
  aria-hidden>` sin href ni aria-label, cero «Scroll to the cube», cero
  `hero__scroll:hover` en el CSS servido, Search Console con su token,
  JSON-LD parseando (description sin la frase temporal), nav con The
  Cube → /#cube, import map y gc-pixel vivos, notas y /CLAUDE.md en 404.
- Antes, el 2026-08-10 (más tarde): **el recorte de la description
  del schema — EL DÉCIMO DEPLOY, EJECUTADO ENTERO Y VERIFICADO EN VIVO:
  deploy `bef16be` de fuente `0e77701`.** Corrección del autor sobre el
  deploy 9: «We begin with Japan.» SALE de la description del JSON-LD — es
  el estado transitorio del proyecto y la definición de la ENTIDAD no
  lleva lo temporal (Japón es el primer nodo, no el tema — el criterio de
  siempre) — mientras la meta description y el hero LA CONSERVAN:
  describen la página de hoy, no la entidad. La regla de derivación quedó
  actualizada en la decisión del JSON-LD (el patrón de la og-image con la
  puntuación: misma fuente, divergencia deliberada y ACOTADA, anotada en
  los dos lados; el recorte se mantiene al re-derivar). Guardas: cinco en
  verde (pendulum 0.0961, ready `2` esperado, baseline 36 intacto) +
  check-modes contra el árbol real de main servido en :8000. Verificado
  en vivo: portada BYTE A BYTE idéntica al blob de main (15.133 bytes),
  la description servida SIN la frase y la meta description servida CON
  ella, **validator.schema.org contra el dominio: Organization, 0
  errores, 0 advertencias**; notas y /CLAUDE.md en 404, Search Console
  intacta, seguros y sitemap en statu quo.
- Antes, el 2026-08-10: **el JSON-LD de Organization en la
  portada — EL NOVENO DEPLOY, EJECUTADO ENTERO Y VERIFICADO EN VIVO:
  deploy `1279c87` de fuente `1ef1bd8`.** El disparador, con evidencia: el AI
  Overview de Google citaba LinkedIn (con el «currently in initial
  development» de antes del lanzamiento) porque el dominio no daba su
  definición en formato máquina. Lo publicado: el bloque schema.org
  Organization en el `<head>` de la portada, y solo ahí — entre la meta de
  Search Console y el bloque de iconos, FUERA de los bloques comparados—,
  con la description IDÉNTICA a la meta description (deriva del hero: tres
  textos, una sola fuente), logo la 512 maciza, sameAs X + LinkedIn, y SIN
  alternateName (ァ y ナ no están en el subset — el matiz y la vuelta, en
  la decisión). **Ver la decisión nueva, primera de la lista**, que
  registra además: la REFUTACIÓN de la premisa del segundo hash de CSP (el
  bloque es un DATA BLOCK no ejecutable — `script-src` no lo alcanza; el
  único hash sigue siendo el del import map), la supervivencia BYTE A BYTE
  en el contrato del deploy (generalizada a todas las páginas y todos los
  bloques, probada en rojo), y el hallazgo ALTA de la revisión adversarial
  de 5 lentes, reproducido y corregido (la prosa del comentario citaba los
  literales que la precondición 3c prohíbe y abría un match fantasma que
  frenaba todo deploy en falso — reformulada; REGLA NUEVA: esos literales
  no se escriben en comentarios de un HTML publicable). Validación:
  `json.loads` sobre el artefacto Y sobre lo servido, el vocabulario
  oficial de schema.org descargado (las cinco propiedades con su dominio
  en regla), las cuatro URLs absolutas en 200, y **validator.schema.org
  contra el dominio EN VIVO: Organization, 0 errores, 0 advertencias**.
  Verificación en vivo 21/21: portada BYTE A BYTE idéntica al blob de
  main, meta de Search Console con su token, las cuatro rutas de notas y
  /CLAUDE.md en 404, seguros 200+noindex, sitemap.xml con 14 URLs.
  Guardas: cinco en verde (pendulum 0.0963, ready `2` esperado, baseline
  36 intacto) + check-modes corrido ADEMÁS contra el árbol real de main
  servido en :8000. El texto de reemplazo del §3 (dos scripts inline; el
  JSON-LD NO suma hash a la CSP) quedó ENTREGADO al autor — su archivo lo
  pega él.
- Antes, el 2026-08-08 (después del deploy 8, el cierre del día): **la
  tanda de los CUATRO FRENTES — SIN deploy: el artefacto de main NO
  cambió.** **(1) La rama `maintenance` también sirve SIN comentarios**:
  el generador reusa EL MISMO `transformar()` del deploy (una
  implementación, no dos), la rama quedó regenerada (`1b80019`, con su
  historia) y verificada sobre el HTML RESULTANTE, y check-maintenance
  suma cero-`<!--` y cero-`/*`-en-`<style>` probadas EN ROJO — ver la
  actualización en su decisión. **Pusheada a origin con autorización del
  autor (junto con redesign-trust): la rama de emergencia remota ya es la
  versión sin comentarios.** **(2) El DISEÑO del acople de check-ready,
  ENTREGADO — y el autor APROBÓ EL DISEÑO A el mismo día: la guarda está
  IMPLEMENTADA y probada en rojo** — ver la decisión nueva, primera de la
  lista («La guarda de placeholders indexables»): página INDEXABLE del
  artefacto no puede llevar placeholders TODO (la inversa de
  `noindex_olvidado` — seguros con su noindex pasa, la tarjeta de sector
  habría frenado), con el conteo COMPARTIDO vía `_guardas.placeholders_de`
  y AVISO en vez de freno bajo `--fuente`, las dos condiciones suyas.
  **(3) El RE-BARRIDO de seguridad, medido sobre EL ARTEFACTO** (los
  blobs de main del deploy 8 + la maintenance regenerada, como la regla
  «el servido no es el fuente» exige) **y el texto fechado ENTREGADO al
  autor** — limpio: 84 `_blank` todos con noopener (80→84 = los DOS del
  footer × las dos páginas nuevas desde el barrido viejo, /sitemap/ y
  seguros — nada más cambió), 0 formularios, 0 handlers, 0 `style=`, 1
  tercero por página (el pixel), el import map único inline (67 bytes
  post-strip), 0 sumideros en el JS de la casa Y en el vendor.
  **(4) Los pendientes de este archivo, partidos en DOS GRUPOS con dueño
  distinto** (EJECUTABLES POR CODE / ESPERAN A MANUEL — ver AL RETOMAR;
  el DNS anotado como frente aparte). Guardas de la tanda: cinco en
  verde (pendulum 0.0963, ready `2` esperado, baseline 36 intacto).
- Antes, el 2026-08-08 (lo más tarde del día): **la tanda de CERO
  COMENTARIOS EN LO SERVIDO — EL OCTAVO DEPLOY, EJECUTADO ENTERO Y
  VERIFICADO EN VIVO 39/39: deploy `f7d2b3f` de fuente `b5bc838`.**
  Requisito sine qua non del autor: ningún comentario HTML/CSS/JS viaja al
  dominio — el filtro por tipo no veía lo que vive DENTRO de archivos
  publicados (216 comentarios / 76,3 KB en las 16 páginas; styles.css era
  DOS TERCIOS comentarios). La solución es LA TRANSFORMACIÓN en
  make-deploy.py (el fuente NO se tocó: los comentarios siguen pegados a la
  línea que explican) con su guarda de contenido — la decisión completa,
  PRIMERA de la lista, que incluye **LA REGLA NUEVA CON NOMBRE: EL SERVIDO
  NO ES EL FUENTE** (toda verificación de bytes servidos va contra el
  ARTEFACTO; todo diagnóstico del dominio reproduce la transformación antes
  de concluir). El diseño se aprobó con sus cuatro decisiones (vendor sin
  transformar por el @license; los DOS comentarios GLSL del shader
  reescritos EN INGLÉS en el fuente — siguen sirviéndose, son strings del
  programa; la doble regeneración diagnóstica — el estreno pasó SIN
  --pisar, con el diagnóstico «deploy PRE-TRANSFORMACIÓN» exacto;
  robots.txt/sitemap.xml fuera de alcance). **Probado antes de confiar**:
  17 fixtures + 11 mutaciones dirigidas en rojo, E2E de 21 casos sobre rama
  descartable (ambos modos de hotfix frenando), y una revisión adversarial
  de 12 agentes que confirmó 8 hallazgos por reproducción — los 8
  corregidos, DOS de ellos ALTOS que mataban el rollback documentado
  (`--fuente v1-published`/`v1-content-complete` frenaban por exigir
  incondicional la meta de Search Console y el bloque de iconos; ahora la
  presencia rige solo desde HEAD y el chrome exigido SE DERIVA del fuente —
  re-verificado: los dos tags publican). **La verificación en vivo aplicó
  la regla nueva por primera vez**: las 16 páginas y los 4 CSS/JS servidos
  BYTE A BYTE contra los blobs de main, cero `<!--`, la meta de Search
  Console con su token, seguros 200+noindex, gc-pixel, import map,
  three.module.js sha256 intacto con su @license, sitemap.xml byte-idéntico
  (14 URLs), las notas y /CLAUDE.md en 404. Guardas: cinco en verde
  (pendulum 0.0951, ready `2` esperado, baseline 36 intacto). De paso
  quedaron cerradas las DOS verificaciones sueltas de la tanda: el charset
  YA ESTABA (`<meta charset="UTF-8">` primera etiqueta del head en las 18 —
  la premisa del DOM no reproducía contra el fuente crudo) y el comentario
  de la nav con «ocho páginas» + atribución a check-ready se corrigió en
  las NUEVE páginas que lo llevaban (sin número a propósito: el conteo en
  un comentario es el fingerprint que caduca — este caso lo probó) más el
  «las otras ocho» de la 404. Y la observación menor del deploy 5 (la
  palabra «TODOs» en ver-código de /hajime/yorozu/) quedó DISUELTA: ningún
  comentario viaja. La rama maintenance sigue emitiendo comentarios — tanda
  aparte, acordada.
- Antes, el mismo día: **2026-08-08 (todavía más tarde), la tanda de las ANCLAS DE
  LA PORTADA — EL SÉPTIMO DEPLOY, EJECUTADO ENTERO Y VERIFICADO EN EL
  DOMINIO: deploy `525c58d` de fuente `ac6d7d0`.** El bug (capturas del
  autor): las anclas de la nav aterrizaban con demasiado aire — #method con
  ~191px de franja vacía y #cube mostrando encabezado+párrafo con el cubo
  cortado 305px (1440×900). **ANTES de tocar se verificó la estabilidad del
  destino, como pidió él**: cinco cargas frescas por ancla en dos viewports
  — dispersión 0px, drift post-aterrizaje 0px, clic idéntico a carga — la
  hipótesis del lazy-init quedó DESCARTADA (la reserva del layout 3D hace
  su trabajo); los píxeles entre sus capturas de iPhone son la barra de URL
  del visual viewport, no la página. **La solución está en la decisión de
  anclas (actualizada): scroll-margin-top POR SECCIÓN, derivado de la MISMA
  var(--pad-top) del padding** — #cube con margen NEGATIVO deliberado (el
  aterrizaje pasa de largo el encabezado: conmutador arriba, cubo ENTERO
  debajo) más el término de cabecera de texto medido (con cap min(6vw,87px)
  y base móvil gorda: el error del ajuste va SIEMPRE al aire). **Verificado
  EJECUTANDO en 25 anchos (320–2560): peor gap del toggle +6.3px — nunca
  bajo la nav**; reduced-motion aterriza idéntico. Resultado a 1440×900:
  toggle a 18px de la nav, cubo entero (765<900), encabezado afuera; METHOD
  a 12px con las tres tarjetas enteras (652) y «How we work» asomando
  (724); About mismo criterio; footer SIN tocar (clampeado por el fin del
  documento, correo visible). A 390: toggle a 38px, cubo entero (582<844),
  rótulos a 16px. **VERIFICADO EN VIVO contra el dominio: 23/23** — las
  cuatro anclas por carga directa en los dos viewports Y los dos accesos a
  #cube (clic de nav y flecha del hero), más la meta de google-site-
  verification SERVIDA con su token intacto y los cuatro archivos de notas
  fuera del artefacto (confirmados en la lista de excluidos del
  --solo-verificar). Guardas: cinco en verde (pendulum 0.0964, ready `2`
  esperado, baseline 36 sin regenerar — no se tocó chrome comparado, solo
  CSS). El comentario de #cube-view en index.html quedó actualizado en el
  fuente (el viejo decía que la nav aterrizaba en el título «por el
  contexto» — ya no) y viaja en el próximo deploy.
- Antes, el mismo día: **2026-08-08 (más tarde), la tanda de SEARCH CONSOLE +
  FUENTES — EL SEXTO DEPLOY, EJECUTADO ENTERO Y VERIFICADO EN EL DOMINIO:
  deploy `e20289e` de fuente `0398d9f`**, procedimiento del README completo
  (cinco guardas en verde con `2` esperado de ready y pendulum sano en
  0.0964; guarda del deploy con main intacta; check-modes contra el árbol
  REAL de main servido en :8000), push de main Y de redesign-trust. Lo
  publicado: **(1) la meta `google-site-verification` con el token REAL en
  la portada** — entre `twitter:card` y el bloque de iconos, FUERA de los
  tres bloques comparados (re-confirmado contra el bloque de iconos nuevo
  del deploy 5: la comparación empieza en el `<link>` del .ico), token
  verificado carácter por carácter en el fuente Y en el HTML SERVIDO —
  esto EJECUTA el 4B que estaba preparado *(y CERRÓ: la propiedad quedó
  VERIFICADA por Google el mismo 2026-08-08 — prefijo de URL sobre
  https://kotodamafinance.com/, método etiqueta HTML. **LA META NO SE
  TOCA**: si desaparece del `<head>` de la portada, se pierde la
  verificación)*; **(2) IMAJ renombrado y re-dominado**:
  資産運用業協会 / www.imaj.or.jp (la fusión del 1/4/2026; la sigla IMAJ
  sigue siendo correcta), cero restos de toushin.or.jp ni del nombre viejo
  en el servido; **(3) Mizuho renombrado con el patrón de «Bank of Japan —
  Financial System Report»**: «Mizuho Bank — みずほ経済インサイト» (la
  publicación tras la raya, en japonés con `lang="ja"` porque es su único
  nombre) y みずほ銀行 en la línea secundaria — decisión del autor
  verificando el sitio en navegador real: «Mizuho Research Institute» no
  se nombra ahí y los informes se firman por AUTOR; el 403 era muro
  anti-bot, mismo caso que BIS y 大和総研 — URL y tier intactos, cero
  restos del nombre viejo en el servido. EDINET ya estaba en disclosure2
  desde el deploy 5: re-verificado, cero restos. **Cero regeneración de
  subset**: todos los glifos de los nombres nuevos ya estaban cubiertos
  (la lista de 50 entidades los trajo) — lo dijo la guarda de cobertura,
  no se asumió. **Los cuatro archivos del sistema de notas siguen AFUERA
  del artefacto y en 404 en el dominio** (verificado en el worktree Y en
  vivo), /CLAUDE.md y /tools/ en 404. La observación del comentario ancla
  de /hajime/yorozu/ (la palabra «TODOs» en ver-código) SIGUE tal cual: el
  autor no la incluyó en esta tanda. Y el dato pedido antes de empezar:
  **el barrido de seguridad del estático NO se corrió en esta rama** desde
  el de 2026-08-06 (§3 del doc de infraestructura del autor) — nada que
  este deploy invalide; el re-barrido, cuando se haga, va sobre lo servido
  desde hoy.
- Antes, el mismo día: **2026-08-08, la tanda del DEPLOY SIN CONTENIDO —
  EJECUTADA ENTERA Y PUBLICADA: deploy `b78cf0b` de fuente `41c9d32` (el
  QUINTO), procedimiento del README completo (cinco guardas en verde con
  `2` esperado de ready, guarda del deploy, check-modes contra el árbol
  REAL de main servido en :8000), push de main Y de redesign-trust (el
  fuente trazable en origin), y VERIFICADO EN EL DOMINIO**: el fondo de la
  nav opaco al scrollear y transparente arriba (medido con navegador
  contra el dominio a 390), rótulos en una línea con Contact adentro
  (right 378 de 390), leyenda indivisible, /sitemap/ sin autoenlace (0 en
  el bloque del mapa, 1 en el footer), JILI como tier 2 y ÚLTIMO de
  Insurance en el servido, EDINET a disclosure2 sin resto de la vieja,
  /favicon-192x192.png en 200 con su `<link sizes="192x192">` en la
  portada servida, **los CUATRO binarios grandes sha256-idénticos a los
  locales** (la maciza servida, no caché vieja), /hajime/yorozu/ sin la
  tarjeta en lo renderizado, seguros en statu quo (200 + noindex,follow),
  **y la exclusión de notas verificada DEL LADO SERVIDO: /notes/,
  /hajime/nota-ejemplo/, /assets/js/notes.js y /notes/search-index.json
  en 404**, /CLAUDE.md y /tools/ en 404, www→apex 301, sitemap.xml
  servido con 14 URLs y cero menciones. **UNA observación menor
  reportada**: el comentario ancla de /hajime/yorozu/ contiene la PALABRA
  «TODO» (meta-mención: «el marcado con TODOs se retiró») visible solo en
  ver-código — si el criterio estricto del autor la alcanza, son dos
  palabras a reformular en el próximo deploy. El detalle de la tanda: Lo hecho, cada
  uno con su commit y las guardas en verde: **(1)** el artefacto se
  desacopló del contenido — `notes/`, `hajime/nota-ejemplo/` y
  `assets/js/notes.js` en `NO_PUBLICABLES` como exclusión TEMPORAL (41
  publicables; `notes/search-index.json` salió de `CONTRATO` mientras
  tanto; el pase de estreno en la decisión de notas deshace todo esto);
  **(2)** los tres bugs de móvil de las capturas de iPhone, reproducidos a
  390 ANTES de tocar y verificados EJECUTANDO — ver la decisión nueva de
  la nav («La nav con fondo propio»); **(3)** el autoenlace de /sitemap/
  fuera del renderizado (la exclusión vive en `mapa_bloque()`, la guarda
  la siguió sola — sitemap.xml byte-idéntico); **(4)** EDINET APLICADO a
  disclosure2 en /method/ (era propuesta; IMAJ quedó pendiente entonces —
  **CERRADO en el deploy 6**, ver el cierre de arriba);
  **(5)** 4B preparado sin ejecutar: la meta de Search Console va en
  index.html entre `twitter:card` y el comentario de iconos — FUERA de los
  tres bloques comparados — cuando Manuel pase el token (**EJECUTADO en el
  deploy 6** con el token real, ver arriba). **LA TARJETA DE SECTOR — el freno que apareció y cómo lo resolvió el
  autor**: vive DENTRO de /hajime/yorozu/index.html — página publicada—,
  así que la selección por archivos no podía excluirla: el deploy la
  habría publicado con sus DOS TODOs en castellano visibles sin que
  ninguna guarda frene (la de castellano exime «TODO», make-deploy no
  cuenta placeholders, check-ready no está acoplado). **Su decisión
  (2026-08-08): el MARCADO salió del archivo — comentarla se descartó
  porque el TODO seguía visible en ver-código**. Baseline 38 → 36; el
  patrón y el pase de reposición, en la decisión de la tarjeta. El mapa no
  la necesita mientras seguros siga noindex — verificado en
  `mapa_bloque()`: una tarjeta a página no listada se ignora y seguros no
  está en `paginas_publicas()`. **Y la respuesta a su pregunta del
  artefacto: /hajime/yorozu/japan/seguros/ SÍ viaja en el deploy** — está
  en los 41 publicables y responde 200 en el dominio DESDE EL DEPLOY 4
  (2026-08-07), a propósito y verificado entonces: publicado e invisible
  (noindex, sin enlaces, fuera de sitemap y mapa) no es lo mismo que no
  publicado, y quedó confirmado de nuevo hoy contra el dominio. El favicon: el autor rechazó
  la apilada original («pierde por presencia») y APROBÓ la variante MACIZA
  sobre la segunda hoja de renders — implementada: ver la actualización
  2026-08-08 en la decisión del favicon (dos marcas por tamaño, cuatro
  superficies grandes unificadas, URLs intactas, el 192 píxel-idéntico al
  aprobado). La tarjeta de sector salió del MARCADO por su decisión
  (baseline 36; el patrón y el pase de reposición quedan — ver su
  decisión). NADA de esta tanda está pusheado; el deploy 5 real y el push
  los confirma él tras el reporte de guardas + --solo-verificar.
- Antes: **2026-08-07 (todavía más tarde), la tanda de auditoría +
  el SISTEMA DE NOTAS + la tarjeta de sector — construido y commiteado
  LOCAL, SIN deployar y SIN push (instrucción de la sesión).** La
  auditoría, verificada contra el fuente antes de tocar: JILI a Tier 2 y al
  final de Insurance (la propia página declara «official primary first»);
  el CTA `#cube-open` con nombre accesible por defecto («Open Hajime →»,
  que el JS reescribe); el registro del enlace a /musubi/ corregido (dice
  «underneath», no «behind», y los DOS accesos conviven — el `<a>` es la
  capa sin cubo); la lista de cadenas duplicadas completa («First analysis
  on the way» es TRIPLE: hero + /hajime/ + FACES de main.js); y la tabla
  de las 49 URLs de /method/ verificada — dos correcciones PROPUESTAS sin
  aplicar (EDINET→disclosure2; toushin.or.jp→imaj.or.jp con la entidad
  RENOMBRADA: hoy es 資産運用業協会) *(EDINET se aplicó en el deploy 5;
  IMAJ y Mizuho, en el 6 — ver el Último cierre)*, Mizuho en 403 a
  clientes automatizados + nombre a decidir (unidad dentro del banco desde
  el 1/4/2026) *(decidido por el autor para el deploy 6: Mizuho Bank —
  みずほ経済インサイト)*, BIS y Daiwa rechazan automatización (no es rot). El sistema
  de notas completo y el patrón de tarjeta de sector: ver las DOS
  decisiones nuevas, primeras de la lista. **Son DIECIOCHO páginas**
  (/notes/ y la nota-fixture, ambas noindex), el sitemap sigue en 14 URLs,
  **baseline en 38** (13 nuevos deliberados) y `check-ready` en `2`
  esperado. Antes, el mismo día: **el mapa del sitio: la
  SUBPÁGINA /sitemap/ — y esto REVIERTE el bloque en los quince footers
  del mismo día, por decisión del autor** («aprobé el diseño y me equivoqué
  al aprobarlo»: un árbol de quince entradas repetido en las quince
  páginas es demasiado footer, y crece con cada sección). El árbol completo
  vive en /sitemap/ (molde de /method/, generado por `make-sitemap.py` en
  la misma corrida que el XML) y el footer volvió a lo que era MÁS el
  enlace «Site map» en su línea de abajo, junto al ©. Se conservó todo lo
  que seguía siendo correcto: la fuente única de URLs (mismo conjunto que
  sitemap.xml — seguros AFUERA mientras lleve su noindex), los nombres del
  `face-page__romaji`, romaji solo, ORDEN_SITIO con abort, la marca de
  notas, `mapa_desactualizado()` en check-structure (ahora contra la
  página), y las cinco correcciones de la revisión adversarial de 12
  agentes. **Los DIECISIETE rojos se re-probaron sobre la arquitectura
  nueva**, y **el hallazgo del ancla Contact quedó RESUELTO por la propia
  reversión, medido**: a 1280×720 el correo vuelve a aterrizar visible
  (y≈436–462) — la nav no se tocó. El orden de los grupos lo fijó el autor
  el mismo día sobre las capturas: **The Site primero**. **PUBLICADO ESE
  MISMO DÍA con su confirmación: deploy `1c25d62` de fuente `8ed6e58` —el
  CUARTO—, procedimiento del README completo** (cuatro guardas en verde con
  `2` esperado de ready, la guarda del deploy, y check-modes contra el
  árbol REAL de main servido en :8000) **y VERIFICADO EN EL DOMINIO**:
  /sitemap/ sirviendo con The Site primero, el enlace del footer en la
  portada, las notas en 404, www→apex en 301. **Y el deploy intermedio
  previsto OCURRIÓ: el andamiaje de seguros quedó SERVIDO por primera vez,
  invisible como se diseñó** — 200 en el dominio CON su meta noindex y
  CERO menciones en el sitemap.xml servido, verificado exactamente contra
  el escenario que motivó el noindex. Ver la decisión, la primera de la
  lista.
  Antes, el mismo día: **el andamiaje de la capa 1 de
  seguros**: `/hajime/yorozu/japan/seguros/` con el molde de /method/ —
  apertura + nueve secciones con subtítulo y prosa, todo placeholder (25,
  baseline actualizado; `check-ready` en `2` esperado). Sin kanji ni marca
  de agua (no hay kanji cerrado; no se inventa), vuelta a /hajime/yorozu/,
  y **con `noindex` mientras sea placeholder** — la exclusión del sitemap
  derivada de la meta (13 URLs hoy) y el olvido inverso con guarda probada
  en rojo; el árbol de URLs llega a cuatro niveles por primera vez. NO
  deployado a propósito: se publica cuando el autor pase el texto. El
  enlace desde /hajime/yorozu/ quedó pendiente de su aprobación. Ver su
  decisión. Antes, el mismo día: **las
  tarjetas de las subcaras en /hajime/**:
  tres tarjetas `.face-page__cards` debajo del párrafo (que no se tocó) —
  太一 Taichi · 万 Yorozu · 幽玄 Yūgen, cada una con la línea de función de su
  destino, reusando `.face-card` sin punto de estado — y los nombres en prosa
  DE VUELTA a `i.name` sin enlace: la regla `.name`-no-enlaza quedó UNIFORME
  en todo el sitio. El detalle y los porqués, en la decisión de las
  subpáginas de Hajime; verificado midiendo a 1440/1920/800/700/600 (una
  fila de tres, apiladas bajo 640, pies parejos, sin desborde, cero JS) y
  capturas enviadas al autor. La description de /hajime/ sigue válida (nombra
  las tres líneas que ahora son tarjetas). Antes, el mismo día: el retrigger
  que destrabó el deploy 2 — ver más abajo en este mismo bloque. Antes,
  el **2026-08-06 (después de publicar), la tanda de cuatro
  ajustes del autor**: el titular del hero SIN puntos (el `<br>` ya separa;
  corte re-verificado midiendo: línea 1 en 907px contra el tope de 990,
  margen 83 — la garantía se ensanchó; **la og-image CONSERVA los puntos a
  propósito**: dibuja el titular en UNA línea y ahí el punto es el separador,
  anotado en `LINEA` del script); el justificado EXTENDIDO al About de la
  portada (era omisión del pase original, no decisión — medido su gate en la
  columna de 36rem: máx 13.1px, cero sobre 16; Method queda afuera: su única
  prosa es lead y tarjetas, texto de display); y los dos párrafos del perfil
  profesional de /sugao/ con **insurance operations** sumado al arco (primero
  operations, después risk management — la secuencia real; la enumeración del
  arco a guiones; descriptions derivadas ajustadas igual). **El SEGUNDO
  deploy (`03f9f79`, de fuente `b8be22e`) quedó SERVIDO EL 2026-08-07 VÍA
  RETRIGGER, y los cuatro cambios están VERIFICADOS EN EL DOMINIO**
  (titular sin puntos, About justificado, /sugao/ con operations, las dos
  descriptions — todos contra el origen, con cache-buster). Lo que pasó: el
  primer build falló en «Deploy to GitHub Pages» (build en verde, falla del
  lado de GitHub) y su re-run quedó ENCOLADO ~24 h sin poder cancelarse
  («Failed to cancel workflow»), con GitHub Status sin incidente — cola
  trabada, no algo del repo (los cuatro runs anteriores habían completado
  bien). Lo destrabó un **commit VACÍO en `main`** (`00c4a00`, decisión del
  autor): dispara un run nuevo que entra en cola limpia — completó en verde
  al instante. **La forma que lo hace seguro es regla desde ahora y
  REEMPLAZA al «NO fabricar commits para retriggerear» que decía acá**: ver
  el punto nuevo en la decisión de la rama de deploy. Antes, el mismo
  día: **LA PUBLICACIÓN: EL SITIO ESTÁ VIVO EN
  kotodamafinance.com.** El procedimiento de «Publicar» del README se siguió
  completo y alcanzó tal como está escrito: cinco guardas en verde (pendulum
  con su métrica sana, 0.0965), `make-deploy` → `824fada`, `check-modes` en
  verde contra el árbol real de `main`, push con confirmación explícita del
  autor, build de Pages en verde (~10 min, más lento que lo usual), y
  verificado EN EL DOMINIO: portada y rutas nuevas en 200, las notas en 404
  (/CLAUDE.md, /README.md, /tools/, /docs/, maelstrom), CNAME+HTTPS
  intactos, www→apex en 301, y el pixel disparando desde el dominio con la
  exclusión de IP re-confirmada por header. Tag **`v1-published`** en el
  commit fuente `6dc8214`. Se publicó ANTES de los pasos 2-4 del DNS a
  propósito — ver AL RETOMAR. El mismo día, antes: **la rama de deploy:
  `main` pasa a GENERARSE con
  `tools/make-deploy.py` — el sitio solo, sin las notas—, con la guarda
  probada EN ROJO (R1-R5 y los cuatro estados de la detección de hotfix) y
  `main()` corrido de punta a punta sobre un ref descartable, tras una
  revisión adversarial de 22 agentes con 10 hallazgos corregidos** — ver su
  decisión, que es la primera de la lista. El
  mismo día, antes: **el favicon: 言 solo en oro sobre navy, juego
  completo (ico/svg/pngs/apple/android/manifest) con el 16px tratado y
  medido, y el bloque de iconos vigilado por check-structure** — ver su
  decisión. El mismo día, antes: **la tanda del cuerpo — la lista de
  /method/ al ANCHO COMPLETO (columnas adaptativas) y el cuerpo de prosa
  JUSTIFICADO, con el análisis de elementos estructurados cerrado** — ver
  «El cuerpo» en las decisiones. El mismo día, antes: el halo (B) probado y DESCARTADO, la
  marca de agua (A) aprobada. El 2026-08-05: el bloque 5 de /musubi/, los
  kanji de las subcaras (太一 · 万 · 幽玄), la tarjeta de LibraryThing y las
  tres subpáginas de Hajime — **LA REDACCIÓN DEL SITIO ESTÁ TERMINADA** y
  las tandas tipográficas que siguieron. **Árbol limpio y todo pusheado** en
  `redesign-trust`, con las guardas corridas (structure y modes en verde,
  pendulum en verde, **ready en `0`: LISTO PARA PUBLICAR** — ver el punto
  siguiente).
  *(Este bloque no puede nombrar su propio commit, así que siempre queda uno
  atrás: `git log -1 redesign-trust` es la respuesta exacta. El ancla fija que no
  deriva es el tag.)*
- **EL BASELINE VOLVIÓ A SALIR DE CERO A PROPÓSITO (2026-08-07), y desde
  el 2026-08-08 está en 36**: 25 del andamiaje de la capa 1 de seguros —
  la primera página sectorial, `/hajime/yorozu/japan/seguros/`, cuyo texto
  escribe el autor aparte — **más 11 del sistema de notas** (8 de la
  nota-fixture, 3 de /notes/). *(El 2026-08-07 llegó a 38 con los 2 de la
  tarjeta de sector; el 2026-08-08 la tarjeta salió del marcado — ver su
  decisión — y quedó 36 en tres páginas.)*
  **`check-ready` sale `2` y ES LO ESPERADO** (era 6 del
  código 2; la historia completa sigue en el docstring de `check-ready.py`).
  **El andamiaje quedó SERVIDO desde el deploy 4 (2026-08-07), invisible
  a propósito**: noindex, sin enlaces entrantes, fuera del mapa y del
  sitemap — verificado en el dominio. El TEXTO sigue pendiente. Más
  placeholders que los 38 del baseline sí es regresión — el baseline dice
  el techo acordado. *(Antes: el sitio había vuelto a cero
  placeholders el 2026-08-05 — la redacción terminada por segunda vez, con
  la que se publicó — y `2` significó regresión desde entonces hasta este
  andamiaje.)*
- **Ahora son DIECIOCHO páginas** (2026-08-07, más tarde: /notes/ y la
  nota-fixture /hajime/nota-ejemplo/, las dos con noindex; antes ese día,
  /sitemap/ y el andamiaje de seguros). El sitemap tiene **14 URLs
  mientras las noindex sigan siéndolo** (fuera quedan la 404, seguros,
  /notes/ y la nota-fixture; el conteo sube al sacar cada meta — todo
  derivado) y **el árbol de URLs llega a CUATRO niveles** — verificado que
  nada asume profundidad máxima: guardas y generadores descubren por
  `rglob` y derivan de directorios.
- **Trabajos pendientes de este lado: NINGUNO (los dos anotados el
  2026-08-08 se CERRARON el mismo día, más tarde)**: el re-barrido de
  seguridad se midió sobre EL ARTEFACTO (main + maintenance) y el texto
  fechado quedó entregado al autor (su archivo lo pega él); el diseño del
  acople de check-ready quedó entregado con sus costos — la elección es
  del autor, ver el bullet siguiente. Ver sus filas en los cabos.
- **Decisiones del autor pendientes: UNA (la tarjeta de sector)** — *(la
  del ENSAYO DEL ROLLBACK se CERRÓ el mismo 2026-08-14: eligió EN SECO
  con sus dos razones anotadas en el README, y el ensayo se EJECUTÓ
  entero — ver el Último cierre; la
  del NOMBRADO de los deploys se CERRÓ el mismo 2026-08-14: el autor
  aceptó la refutación del esquema last-good ENTERA («importaba ceremonia
  de contextos con equipo», sus palabras), LOS TAGS QUEDAN COMO ESTÁN, y
  el título del fuente en el mensaje del deploy quedó IMPLEMENTADO Y
  PROBADO — ver el bullet nuevo en la decisión de la rama de deploy. La
  del acople de check-ready se cerró el 2026-08-08: diseño A
  implementado.)* **El
  TÍTULO y la LÍNEA DE FUNCIÓN de la tarjeta de sector** en
  /hajime/yorozu/: el PATRÓN está construido (la variante sin kanji — ver
  la decisión del patrón de sector), pero **desde el 2026-08-08 el MARCADO
  está FUERA del archivo** (decisión del autor: TODOs visibles en
  ver-código de una página publicada no van); al pasar él el título, la
  tarjeta se reescribe — el pase de reposición está en esa decisión.
  *(Esto reemplaza al «cómo enlaza /hajime/yorozu/ a seguros», que era la
  pendiente anterior: la respuesta fue esta tarjeta.)* **La VUELTA de una
  nota se CERRÓ el 2026-08-08: «← All notes», a /notes/, MÁS el rótulo de
  cara enlazado en la cabecera** — implementado en el molde, con el rótulo
  dentro del contrato y su guarda probada en rojo; ver la decisión del
  sistema de notas, que quedó actualizada. Además esperan TEXTO suyo: la capa
  1 de seguros, y la description y el gloss de /notes/ — pases de
  redacción, no decisiones. Las dos
  anteriores se cerraron el 2026-08-05: los kanji de las subcaras (**太一 Taichi · 万
  Yorozu · 幽玄 Yūgen**, dictados por el autor desde la tabla del cubo de su
  `context.md` — entonces se creyó no localizable y se copiaron literales de
  su mensaje, la misma regla de no inventar; **hoy el archivo SÍ está
  localizado**: ver el puntero en la decisión del andamiaje de seguros), y
  **el logo de LibraryThing, que
  ya está puesto**: va el archivo oficial EN SU PALETA ORIGINAL, sin alterar
  — criterio nuevo del autor que REVIERTE el monocromo en oro y DISUELVE el
  pendiente de permiso de marca (usar la marca tal cual se distribuye es lo
  que cualquier guía permite). Ver la decisión de tarjetas de perfil.

**Lo que dejó la última tanda (la revisión de quince puntos)**, todo integrado
en las decisiones de abajo: las anclas de la nav aterrizando con el layout ya
estable (la hidratación del cubo insertaba ~406px DESPUÉS del aterrizaje — se
arregló con la reserva del layout 3D en la carga, más `scroll-margin` para el
footer y el ancla `#cube-view` para «Back to the Cube»); el lazy-init que en
realidad no difería nada (el hero mide exactamente 100vh y tocar el fold cuenta
como intersecar — `rootMargin` pasó a `-1px` abajo); la costura cubo→About en
140px y el margen del hint en 12; la lista de fuentes de la portada sin japonés
y con el enlace centrado; la lista de /method/ con el japonés como línea
secundaria bajo el inglés; el footer a dos columnas sin «Platform», con la
bajada sin «Japan's» y sin el rótulo 免責事項; seis correcciones de texto que
des-anclan el proyecto de Japón como tema; los rótulos de vuelta por origen;
`user-select: none` en la grilla clip; y dos reportes que NO reproducían contra
el servidor (ayuda 3D con texto de grilla, subpáginas «descentradas») — otra
vez el patrón de la copia vieja en el navegador del autor.

**La tanda anterior** (mismo día): la rama `maintenance` con su generador y su
guarda; la regla de credenciales, escrita antes de que exista la primera; Zen
Kaku embebido en el cartel; y las dos declaraciones de procedencia de `/method/`
reducidas a una línea.

**Tres tags — la serie está completa:**

- `v1-dark` — la versión navy+oro con el cubo Three.js, con registro visual en
  `docs/v1-dark/`.
- **`v1-content-complete`** — el sitio terminado de contenido, y **el punto de
  restauración de la migración de DNS**. Apunta a `fb38ffb`, que era el último
  estado verificado en verde al crearlo. **No se mueve** aunque el trabajo siga:
  ver la regla más abajo.
- **`v1-published`** — la publicación (2026-08-06). Apunta a `6dc8214`, el
  **commit FUENTE del primer deploy** — no a `main`: el commit de `main`
  (`824fada`) es un snapshot generado y lleva el hash cruzado en su mensaje;
  el que pasó por las guardas es el fuente. El nombre lo fijó el autor:
  v1 y no v2, porque es la primera publicación del MISMO sitio que
  `v1-content-complete` ya marcaba terminado — la numeración de versiones y
  el hito de publicación son ejes distintos, y la v2 queda libre para un
  cambio mayor real (el dashboard, o la migración a PaaS).

**Existe una rama `maintenance`, lista y NO activa.** No se ve desde acá y
ninguna de las cuatro guardas la mira; su decisión cerrada está más abajo.

### AL RETOMAR, EMPEZAR ACÁ

**Levantar el servidor en `:8000` y correr `python tools/check-structure.py`
—tiene que dar verde—.** Si da rojo, eso es lo primero: algo cambió fuera de
sesión.

**EL SITIO ESTÁ PUBLICADO (2026-08-06; último deploy: el 11 — la flecha
del hero sin enlace, decorativa — 2026-08-14, verificado en vivo 23/23
byte a byte contra el artefacto; desde el deploy 8 rige LA REGLA
«EL SERVIDO NO ES EL FUENTE», ver la decisión «CERO comentarios en lo
SERVIDO»).**

**LOS PENDIENTES VAN EN DOS GRUPOS CON DUEÑO DISTINTO** (partidos el
2026-08-08 a pedido del autor — antes eran una bolsa y al retomar parecía
haber seis cosas trabadas):

**EJECUTABLES POR CODE (no dependen de nadie más): hoy NINGUNO.** Los
tres que había se cerraron el mismo 2026-08-08, más tarde: la rama
`maintenance` sin comentarios en lo que sirve (ver su decisión y la de la
transformación), el re-barrido de seguridad del estático (medido sobre EL
ARTEFACTO y entregado el texto fechado al autor — su archivo lo pega él)
y el diseño del acople de check-ready (entregado con costos; la elección
es suya, ver el grupo siguiente).

**ESPERAN A MANUEL (Code no puede avanzarlos):**
(1) el TÍTULO y la LÍNEA DE FUNCIÓN de la tarjeta de sector — decisión
abierta, ver su bullet en Estado; (2) la description y el gloss de
/notes/ — redacción suya; (3) el TEXTO de la capa 1 de seguros — su
andamiaje ya está servido con noindex, invisible; (4) la PRIMERA NOTA
REAL — el sistema está construido, el pase de estreno vive en la decisión
de notas. *(Las DOS que estuvieron acá unas horas el 2026-08-14 se
CERRARON el mismo día: el ENSAYO DEL ROLLBACK — eligió EN SECO y se
ejecutó entero, ver el Último cierre y el README — y el NOMBRADO de los
deploys para el rollback: el autor aceptó
la recomendación, los tags quedan como están, y el título del commit
fuente ya viaja en la primera línea del mensaje del deploy — ver el
bullet en la decisión de la rama de deploy. La del acople de check-ready
se cerró el 2026-08-08: diseño A implementado.)*

**EL DNS ES OTRO FRENTE, FUERA DEL REPO — no es pendiente de Code**: los
pasos 2-4 de la migración (el detalle, más abajo en esta misma sección).

**SEARCH CONSOLE QUEDÓ VERIFICADO (2026-08-08,
confirmado por Google)**: propiedad de prefijo de URL sobre
https://kotodamafinance.com/, método etiqueta HTML — **la meta
`google-site-verification` de la portada NO SE TOCA: si desaparece del
`<head>`, se pierde la verificación** (la regla vive también en el
comentario junto a la meta en index.html). La
publicación (el paso 5) se ejecutó **ANTES de los pasos 2-4, por decisión del
autor, y el orden es correcto**: una transferencia de registrador NO cambia
los nameservers — Namecheap sigue sirviendo la zona durante los ~5 días de la
transferencia a Xserver, ya en curso—, y publicar antes deja días de sitio
nuevo funcionando sobre el DNS actual como **línea de base** para cuando se
cambie la delegación: si algo se rompe en el paso 4, se sabe que el sitio
servía bien sobre la zona vieja. Quedan los pasos 2-4, todos fuera de este
repo.

**PASO 0 — HECHO. Ya se sabe dónde está el DNS**: **Namecheap BasicDNS**, con
los seis registros del `.com` documentados (cuatro `A` de GitHub Pages, el
`CNAME` de `www`, y el `TXT`/SPF del forwarding). **DNSSEC ya se desactivó**,
antes de transferir. El detalle vive fuera del repo.

**PASO 1 — HECHO (2026-08-04). iCloud+ ya corre en el DNS de Namecheap,
verificado por el autor: recibe y responde.** Con esto el correo dejó de
depender del forwarding de Namecheap, que era lo que moría al salir del
registrador — `contact@kotodamafinance.com` ya sobrevive a la transferencia, y
con él la única vía de contacto de la página de mantenimiento. El detalle de la
configuración vive fuera del repo, en el `.md` de infraestructura del autor.

**ORDEN VIGENTE — Y OJO, CAMBIÓ. Éste reemplaza al anterior**, que decía
transferir → correo → merge:

1. ~~Configurar iCloud+ en el DNS de Namecheap, y verificar que recibe y
   responde.~~ **HECHO.**
2. **Transferir el registro a Xserver.** Los nameservers **no** cambian con la
   transferencia. **EN CURSO desde el 2026-08-06 (~5 días).** ← **EL FRENTE
   ACTIVO**
3. **Cargar la zona completa en Xserver y verificarla** consultando sus NS
   **directamente**, sin tocar todavía la delegación. Ojo: la zona a cargar
   ahora incluye los registros de iCloud+ (MX/SPF/DKIM), no los seis del
   inventario del paso 0 — el inventario vigente es el de después del paso 1.
4. **Recién ahí, cambiar los nameservers.**
5. ~~Generar `main` + push + tag en el commit FUENTE.~~ **HECHO 2026-08-06 —
   ejecutado ANTES que 2-4, a propósito** (ver el párrafo de arriba: la
   transferencia no mueve los nameservers y el sitio publicado es la línea
   de base del cambio de delegación). El procedimiento de «Publicar» del
   README se siguió completo y alcanzó sin improvisar; el registro está en
   «Último cierre» del Estado. Para deploys FUTUROS, ese procedimiento
   sigue siendo el vigente.

**Por qué el correo fue PRIMERO, que era el cambio de fondo.** El forwarding de
Namecheap **muere al salir del registrador**, y `contact@kotodamafinance.com`
está publicado en el sitio, en LinkedIn, en X y **en la propia página de
mantenimiento** — donde además es el **único** enlace que tiene. O sea que si el
correo se caía durante la obra, se caía junto con la única vía de contacto que
queda cuando el sitio está abajo. Por eso se resolvió antes de mover nada — y
quedó resuelto.

**Por qué 2, 3 y 4 están separados.** Que los nameservers no cambien con la
transferencia es lo que permite partirlo: se puede **cargar la zona en Xserver y
probarla contra sus propios NS mientras Namecheap sigue sirviendo el tráfico
real**. Así el único paso que mueve tráfico —el 4— se hace contra una zona ya
verificada, y deja de ser «cambiar y ver qué pasa». Cada paso se comprueba solo,
que es lo que hace el fallo diagnosticable.

**El sitio está listo Y publicado.** Si alguien retoma, las preguntas
vigentes: «¿en qué paso del DNS estamos?» (fuera del repo), «¿llegó
el texto de la capa 1 de seguros?» (andamiaje listo, servido con noindex
desde el deploy 4), «¿llegó la primera nota?» — el sistema de notas está
CONSTRUIDO entero y sin deployar (2026-08-07, ver su decisión) —, y «¿pasó
el autor el título de la tarjeta de sector, o la description y el gloss
de /notes/?» (redacciones suyas). Los dos trabajos de Code anotados el
2026-08-08 se CERRARON ese mismo día (el re-barrido, entregado; el diseño
del acople, entregado, APROBADO e implementado como la guarda de
placeholders indexables): dentro del repo los frentes son esas redacciones
suyas, no construcción nueva. *(Todo pusheado:
la tanda de notas fue con el deploy 5 y el cierre de la vuelta de una nota
—`fb0f61c`— se pushó el mismo 2026-08-08 con autorización del autor, solo
a redesign-trust: nada de esto entra al artefacto hasta el estreno de
/notes/. Los push siguen pidiendo su confirmación, como siempre.)*

La revisión legal del `免責事項` **no es un pendiente**: se decidió publicar sin
ella.

**Sin decidir dentro del sitio queda UNA cosa (desde el 2026-08-08)**: el
título y la línea de función de la tarjeta de sector en /hajime/yorozu/ (el
patrón existe; el marcado se repone junto con su texto). *(La de TOOLING
que estuvo acá unas horas — el nombrado de los deploys, 2026-08-14 — se
cerró el mismo día: aceptada e implementada.)* La decisión del
acople de check-ready se CERRÓ el mismo día — diseño A aprobado e
implementado, ver la decisión primera de la lista. La vuelta de una nota
se CERRÓ el 2026-08-08 — «← All notes» más el rótulo de cara enlazado en
la cabecera; ver la decisión del sistema de notas. Lo anterior — cómo
enlaza /hajime/yorozu/ a seguros — se cerró con la tarjeta; el `domain` de
las tarjetas de la portada, antes.

**Para cualquier deploy futuro, releer primero** las secciones «Antes de
publicar» y «Publicar» del README: son las cuatro guardas MÁS la del deploy
(que corre sola dentro de `make-deploy.py`), y `check-ready` no mira el
comportamiento del cubo ni la física. El primer deploy las siguió tal cual y
el procedimiento alcanzó.

**Y durante toda la obra, la rama `maintenance` es la red.** Es lo que se
publica si hay que dejar el sitio abajo mientras se mueve el DNS; está lista y
se activa cambiando la rama de Pages. Su única vía de contacto es ese mismo
correo — la otra razón por la que el paso 1 fue primero, y con él hecho, la red
ya tiene el contacto asegurado.

### Cabos abiertos vigentes — el resumen corto

Ninguno bloquea publicar (lo publicado no cambia). Cada uno tiene su
sección con el detalle.

| Cabo | Estado |
|---|---|
| ~~Re-barrido de seguridad del estático~~ | **CERRADO 2026-08-08 (el mismo día que se anotó)**: medido sobre EL ARTEFACTO —los blobs de main (deploy 8) y la rama maintenance regenerada—, como la regla «el servido no es el fuente» exige, y el texto con fecha nueva ENTREGADO al autor (su archivo lo pega él, no se edita). Resultado limpio: 84 `_blank` todos con noopener (80→84 = las DOS páginas nuevas desde el barrido viejo, /sitemap/ y seguros, × los 2 del footer — nada más cambió), 0 formularios, 0 handlers, 0 style=, 1 tercero por página (el pixel), import map único inline (67 bytes post-strip), 0 sumideros en el JS de la casa Y en el vendor. |
| ~~Acople de check-ready al deploy~~ | **CERRADO 2026-08-08: el autor aprobó el diseño A y la guarda quedó IMPLEMENTADA** — `verificar_placeholders_indexables` en make-deploy: página INDEXABLE del artefacto no puede llevar placeholders TODO (la inversa de `noindex_olvidado`; seguros con su noindex pasa, la tarjeta de sector habría frenado), conteo COMPARTIDO vía `_guardas.placeholders_de`, FRENA desde HEAD y AVISA bajo `--fuente`. Probada en rojo end-to-end (worktree descartable con commit real). Ver la decisión, primera de la lista. |
| **Capa 1 de seguros: el TEXTO** | **el frente activo (2026-08-07)**: andamiaje listo en `/hajime/yorozu/japan/seguros/` con 25 placeholders esperando el texto del autor, **con `noindex` mientras tanto** (exclusión del sitemap derivada; al redactar: sacar la meta + regenerar sitemap.xml y /sitemap/ —mismo comando— + baseline — el olvido tiene guarda). **Servido con su noindex desde el deploy 4 (2026-08-07): 200 en el dominio, fuera del sitemap servido — invisible, verificado.** La tarjeta desde /hajime/yorozu/: el PATRÓN existe (2026-08-07) pero **su marcado salió del archivo el 2026-08-08** (los TODOs quedaban visibles en ver-código de una página publicada) — **se repone junto con el título del autor**, y al sacar el noindex vuelve a ser requisito del mapa. Ver la decisión del patrón de sector. |
| **Sistema de notas** | **construido completo, SIN deployar (2026-08-07)**: contrato de metadatos, molde con nota-fixture, `make-notes.py` (feed entre centinelas + listado + índice), /notes/ con buscador (segunda página con JS), guarda en check-structure probada en NUEVE rojos, excepción de deploy por ruta exacta. Todo noindex, feed vacío, cero enlaces entrantes. **La vuelta y el rótulo de cara se CERRARON el 2026-08-08** («← All notes» a /notes/; `note-face` en el contrato, cinco rojos más — ver la decisión). **Se estrena con la primera nota real** — el pase completo está en su decisión (primera de la lista). |
| ~~Redacción de Hajime~~ | **CERRADA 2026-08-05**: los 15, con texto del autor. Baseline en cero, `check-ready` en `0`. Cualquier placeholder nuevo es regresión. |
| ~~Logo de LibraryThing~~ | **CERRADO 2026-08-05**: va el archivo oficial en su paleta original, sin alterar — criterio nuevo que disuelve el pendiente de permiso (ver la decisión de tarjetas y `assets/img/README.md`). |
| ~~Kanji de Taichi/Yorozu/Yūgen~~ | **CERRADO 2026-08-05**: 太一 · 万 · 幽玄, del `context.md` del autor. Aplicados en h1 y `<title>` con el patrón de las caras; subset regenerado (太/幽/玄 eran nuevos). |
| **Móvil** | **nunca medido en dispositivo real.** Congelado por decisión del autor. Mediciones: la de escritorio, y la EMULACIÓN de la vista explotada (2026-08-05, `docs/mediciones/explotada-movil-emulada.md` — verde del lado CPU; no reemplaza al dispositivo real). |
| **Maelstrom** | apartado en `assets/css/maelstrom.css`, **no lo carga nadie** —ahora con guarda en `check-modes`—, reactivable. Al retomarlo, empezar por el **bug de la variante táctil** —definía keyframes sin blur y nunca los asignaba—, no por recalibrar. |
| ~~Vista explotada del cubo~~ | **INTEGRADA 2026-08-05**: mergeada a esta rama por decisión del autor, guardas en verde después del merge. Lo que sigue siendo posterior a publicar es la v2 (corrientes de agua) — sólo si el autor la pide. |
| **Dieta de fuentes** | **~79 KB disponibles** quitando features que el sitio no usa. **Decidido: no se hace ahora.** Se revisa si el CSS llega a usar `font-feature-settings`, `font-variant` o `small-caps`. |
| **Guarda de castellano** | **incompleta a propósito, y lo dice en su salida.** Cubre diacríticos y una lista de palabras; se le escapa castellano sin ninguna de las dos. Al agregar una página, leer su superficie además de correrla. |
| **Rama `maintenance`** | **existe, está lista y NO está activa.** Se activa cambiando la rama que publica Pages. **Desde el 2026-08-08 sirve SIN comentarios**: el generador pasa el HTML por el MISMO `transformar()` de make-deploy (regenerada: `1b80019`; check-maintenance suma cero-`<!--` y cero-`/*`-en-`<style>`, probadas en rojo). **Pusheada a origin ese mismo día con autorización del autor** — la rama de emergencia remota ya es la versión sin comentarios. Ver la decisión cerrada más abajo. |
| **Respaldo de `_dev/` y `_ref/`** | **HECHO 2026-08-06**: `kotodama_respaldo_dev-ref_2026-08-06.zip` (40,8 MB, 85/85 entradas verificadas) en la carpeta del proyecto en OneDrive — repetir por hito con el mismo patrón de nombre fechado. Dos hechos verificados que cierran los miedos de fondo, para no re-preguntarlos: **(1) `_ref/` no era única copia** — los 5 archivos son byte-idénticos (sha256) a copias dentro de `Kotodama Finance website.zip` en OneDrive; **(2) el merge NO borra archivos sin versionar** — git no toca untracked en merge ni checkout; el único riesgo era el disco, y quedó cubierto. Versionarlos se descartó: publicaría ~40 MB de capturas (y las fotos de WhatsApp) en el repo público. |
| **`@media print`** | **nadie lo miró, pendiente SIN urgencia** (anotado 2026-08-06, pedido del autor): los navegadores quitan los fondos al imprimir y el texto claro queda sobre papel blanco. La única candidata real es /disclaimer/, que nadie imprime. No bloquea publicar. |
| **Safari** | **sin verificar, riesgo aceptado** (2026-08-06): no corre en Windows. Firefox SÍ pasó un humo completo el mismo día (justificado —ahí con partición de palabras real: Firefox trae diccionarios de hyphens—, marca de agua vertical, multicol de /method/ en 2 columnas, lazy-init, cubo, folio con input confiable, vista explotada). El dato de método que dejó: geckodriver cuelga la creación de sesión en esta máquina — se manejó Firefox por Marionette directo, y un PointerEvent sintético con pointerId inventado muere en setPointerCapture ANTES de deseleccionar: para probar el arrastre hace falta input confiable (WebDriver:PerformActions), no eventos sintéticos. |
| ~~Link rot en /method/~~ | **CERRADO 2026-08-06, aprobado por el autor**: los 3 rotos se corrigieron **en los dos lugares** — /method/ y `§Fuentes de Datos Mapeadas` del `kotodama_finance_context.md` (la fuente de verdad de la que la lista se deriva: corregir solo la página lo habría reintroducido en la próxima derivación). Zenginkyo → `/en/statistics/`; GIAJ → `sonpo.or.jp/en/`; LIAJ → `seiho.or.jp/english/` — las tres verificadas en 200 tras el cambio. **Daiwa cerró después, con un TERCER modo de falla** (verificado a mano por el autor desde Japón, 2026-08-06): el apex `dir.co.jp` NO resuelve —sin registros A/AAAA—, solo existe `www.dir.co.jp`, que va por Imperva con geo-bloqueo fuera de Japón. Corregido en los dos lugares. **EL PATRÓN: son CUATRO enlaces mal anotados de la MISMA lista** (§Fuentes del context.md) — no es casualidad: esa lista se escribió sin verificar contra la fuente, y un dato viejo cuesta poco mientras es interno pero pasa a ser error citable al salir a /method/. **La pasada del catálogo completo CORRIÓ el 2026-08-06 (45 URLs): CERO rot nuevo** — los cuatro corregidos eran todo el rot real. El hallazgo estructural: **el catálogo escribe los dominios SIN www y en el Japón institucional el apex normalmente NO tiene registro A** (25 de 45) — la trampa Daiwa es la convención por defecto de la lista; las 25 variantes www verificadas vivas por HTTP. **Las dos decisiones se ejecutaron el mismo día con aprobación del autor**: el catálogo quedó NORMALIZADO a la forma www verificada viva (26 menciones; la convención quedó escrita arriba de la lista: «el catálogo guarda la forma que RESPONDE, no el nombre canónico»), y la nota envejecida de webland reescrita con el hecho actual fechado. **La nota gemela de tokiorisk se corrigió igual, con aprobación del autor** — hoy tokiorisk no resuelve ni con www; era la TERCERA nota-sobre-terceros caducada, y el patrón con sus tres casos quedó en los hallazgos de método. Nada pendiente en el catálogo. |

---

## Decisiones cerradas — no rediscutir

### La copia derivada de CLAUDE.md en OneDrive: el registro al alcance del Claude del chat

**2026-08-14, pedido del autor — SIN deploy: nada de esto toca el artefacto.**
El problema, con evidencia: el Claude del chat de diseño NO puede leer
CLAUDE.md — vive en C:\Dev, fuera de su alcance; él solo llega a la carpeta
de Claude en OneDrive — así que armaba prompts a ciegas sobre el archivo que
tiene las respuestas: en una sola sesión preguntó el criterio de tags (estaba
escrito), si robots.txt declaraba el sitemap (estaba desde julio) y si el
charset existía (estaba). Tres de tres, y cada una costó una investigación.

- **La copia va ENTERA, no un extracto — y el motivo es el criterio**: un
  extracto necesita un criterio escrito de qué entra, y ese criterio es el
  que deriva (el pedido del autor lo anticipó). «Entero» no tiene criterio
  que mantener; lo que al lector no le sirva no le estorba, y lo que un
  extracto omitiera costaría exactamente la investigación que esto evita.
  El encuadre lo hace el ENCABEZADO, no la selección: dice que las
  instrucciones operativas de adentro (guardas, commits, deploys, AL
  RETOMAR) van dirigidas a Claude Code dentro del repo — para el lector de
  la copia son registro de decisiones, no órdenes.
- **Destino**: `kotodama_CLAUDE_copia.md` en la carpeta de Kotodama Finance
  de OneDrive (la misma del context.md — la ruta exacta vive en
  `COPIA_CLAUDEMD` de `tools/_guardas.py`). El nombre lleva «copia» a
  propósito; el encabezado abre con «COPIA DERIVADA — la fuente de verdad
  vive en el repo», declara commit (hash completo), título y fecha del
  fuente más la fecha de generación, avisa que NO se edita a mano, y cierra
  con una marca fija que separa encabezado de cuerpo.
- **La genera `tools/make-copia-claudemd.py`, SIEMPRE del CLAUDE.md de
  HEAD** (los bytes del blob — sin autocrlf: lo copiado es lo commiteado,
  byte a byte), y **ABORTA si el CLAUDE.md del árbol difiere de HEAD**:
  «commitear primero» — una copia de un estado sin commitear haría mentir
  al encabezado que declara fecha y commit. La escribe VOS (Code) directo
  en OneDrive: Claude tiene lectura ahí y este lado escritura — pasársela a
  Manuel para pegar sería el paso manual donde se desactualizaría (su
  propia precisión).
- **El gatillo es el COMMIT, no el deploy** (el punto del autor: CLAUDE.md
  cambia en tandas que no terminan en deploy — la de la previsualización,
  por ejemplo): tras cada commit que toque CLAUDE.md, correr el generador.
  Está anotado también en el flujo obligatorio, y **el olvido tiene
  guarda**: check-structure compara la copia contra HEAD:CLAUDE.md — misma
  derivación que el generador, el patrón del mapa — y FRENA nombrando el
  comando. Compara contra HEAD y no contra el árbol A PROPÓSITO: a mitad de
  una tanda (CLAUDE.md editado sin commitear) la copia legítima es la del
  commit anterior y la guarda sigue en verde; el rojo aparece recién si el
  commit se hizo y la regeneración se olvidó — exactamente el olvido a
  cazar. Como check-structure corre también AL RETOMAR, una copia vieja no
  sobrevive al arranque de una sesión.
- **En otra máquina (sin la carpeta de OneDrive) la guarda se OMITE con
  aviso, no falla**: la copia es un artefacto de esta máquina, no del repo
  — el mismo trato que el puntero al context.md.
- **Probada en verde y en rojo (17 casos)**: cuerpo byte a byte igual al
  blob, marca única, commit declarado; byte mutado (edición a mano), marca
  perdida, copia ausente, hash falseado, prosa del encabezado reescrita,
  contenido prependido y lectura fallida frenan nombrando cada uno; carpeta
  inexistente se omite; el abort del generador con árbol sucio NO toca la
  copia (sha idéntico antes/después); la regeneración vuelve al verde; y el
  caso real de esta máquina — CLAUDE.md del árbol en CRLF por autocrlf —
  genera en verde (la normalización antes de comparar existe por eso).
- **La revisión adversarial (3 lentes + refutadores, 15 agentes) confirmó
  DOS hallazgos por reproducción — corregidos antes de commitear**: (1) el
  ENCABEZADO quedaba fuera de la comparación — un hash falseado, la prosa
  reescrita o contenido prependido pasaban en VERDE, contradiciendo el
  «cualquier edición es divergencia» del docstring; el cierre es la
  plantilla compartida `encabezado_copia()` en `_guardas`: el generador la
  escribe y la guarda la RECONSTRUYE para comparar (el patrón del mapa,
  aplicado también al encabezado) — lo único legítimamente variable es la
  fecha de generación, que se lee de la propia copia. (2) Una lectura
  fallida del archivo (lock del sync de OneDrive, deshidratado por Files
  On-Demand — el único archivo que las guardas leen fuera del repo) mataba
  check-structure con traceback crudo enmascarando las secciones
  siguientes; ahora degrada a rojo CON NOMBRE — sigue siendo fail-closed, y
  reintentar resuelve. Los otros 9 hallazgos fueron refutados con
  reproducción (latentes, teóricos o convención uniforme del repo).
- **La copia NO se edita nunca — se regenera.** La guarda ve cualquier
  edición como divergencia, y es lo correcto: «arreglar» la copia en vez de
  la fuente es exactamente la deriva que la marca DERIVADA existe para
  evitar. Si esto contradice al CLAUDE.md del repo, gana el repo.
- **La segunda copia (README) quedó DECIDIDA el mismo día: NO por ahora**
  (el autor, 2026-08-14): esperar a ver si con la copia de CLAUDE.md el
  problema sigue apareciendo. **El criterio de reapertura quedó escrito**:
  si Claude vuelve a preguntar algo que vivía en el README, el mismo
  mecanismo se extiende — recién ahí, no antes.

### El JSON-LD de Organization en la portada: la definición de la entidad, desde el dominio

**2026-08-10, instrucción del autor — el deploy 9.** El disparador, con
evidencia: el AI Overview de Google describía el proyecto citando LinkedIn
como fuente — descripción correcta salvo el estado, «currently in initial
development», texto de antes del lanzamiento — porque el dominio no daba su
propia definición en formato máquina y Google la completaba con lo de
afuera. La fuente de un AI Overview no se puede forzar; lo que sí se puede
es dar la definición desde el propio dominio, que es el hueco que llenaba
LinkedIn.

- **Un `<script type="application/ld+json">` con schema.org Organization en
  el `<head>` de la PORTADA, y solo ahí** — entre la meta de Search Console
  y el bloque de iconos: FUERA de los tres bloques que compara
  `chrome_divergente` (el de iconos empieza en el `<link>` del .ico), el
  mismo lugar y por el mismo motivo que la meta de Search Console.
- **La description NO se redactó: DERIVA de la meta description — que a su
  vez deriva del hero — CON UN RECORTE deliberado del autor (2026-08-10,
  deploy 10): va SIN la frase final «We begin with Japan.»** La frase es el
  estado transitorio del proyecto, y la definición de la ENTIDAD no lleva
  lo temporal (Japón es el primer nodo, no el tema — el criterio de
  siempre). La meta description y el hero SÍ la conservan: describen la
  página de hoy, no la entidad. Es el patrón de la og-image con la
  puntuación: misma fuente, divergencia deliberada y ACOTADA, anotada en
  los dos lados. Si el hero cambia, cambian los tres textos — y el recorte
  se mantiene al re-derivar; la dependencia está anotada en los dos
  comentarios del `<head>`.
- **NADA que no esté ya publicado en el sitio** (regla del autor): sin
  dirección, sin teléfono, sin fecha de fundación, sin founder — el
  desajuste entre datos estructurados y lo visible penaliza. Campos: name,
  url, logo (la 512 maciza 言霊, URL absoluta), description, sameAs (los
  perfiles de X y LinkedIn del footer). Las cuatro URLs verificadas en 200.
- **El alternateName 言霊ファイナンス quedó AFUERA**: ァ (U+30A1) y ナ
  (U+30CA) no están en el subset de Zen Kaku — medido contra la cmap con 猫
  de control — y la regla del autor era no usarlo sin cobertura. El matiz
  para el día que se reabra: el contenido de `<script>` NO se renderiza
  (`texto_visible()` lo excluye, la guarda de cobertura ni lo mira), así que
  técnicamente entraría sin regenerar nada; entra si el autor lo decide.
- **Es el SEGUNDO script inline de la portada** (el otro: el import map),
  **pero NO suma hash a la CSP futura — la premisa del segundo hash se
  verificó y NO se sostiene**: es un DATA BLOCK (tipo no ejecutable), el
  navegador no lo ejecuta y `script-src` no lo alcanza; el único hash de
  `script-src` sigue siendo el del import map, y Google lee el marcado con
  o sin CSP. El inventario del §3 quedó actualizado (texto entregado al
  autor, que lo pega él). Ver la decisión de la CSP, que registra la
  refutación.
- **El stripper lo deja crudo — CONFIRMADO ejecutando, no leyendo**: el
  bloque sobrevive BYTE A BYTE a `transformar()`, el comentario de arriba
  no viaja, y la precondición 3c (el CONTENIDO del bloque no puede traer
  `<!--` ni `</script`) lo cubre — el JSON no los trae. **La supervivencia
  entró al CONTRATO con nombre** en la guarda del deploy: cada bloque
  ld+json del fuente tiene que aparecer idéntico en el artefacto, en TODAS
  las páginas y TODOS los bloques (finditer — la revisión señaló que la
  primera versión miraba solo el primero de index.html), frena nombrando la
  pieza, y va condicionado al FUENTE, como el import map (los fuentes
  viejos no lo tienen: un rollback publica el sitio de aquel día como era).
  Probada en rojo: bloque mutado y bloque ausente, los dos frenan.
- **EL HALLAZGO ALTA de la revisión adversarial (workflow de 5 lentes +
  refutadores, 2026-08-10), reproducido por dos lentes y CORREGIDO — y es
  regla desde ahora**: la precondición 3c escanea el fuente CRUDO con un
  regex ciego a comentarios, así que un COMENTARIO cuya prosa escriba los
  literales de la etiqueta de apertura de script / apertura de comentario /
  cierre de script abre un match FANTASMA (arranca en el literal del
  comentario y cierra en el `</script>` REAL de un bloque de más abajo) y
  FRENA todo deploy en falso — le pasó a la primera versión del comentario
  del propio bloque, que citaba esos literales al documentar la
  precondición. Mi prueba no lo vio porque probó `transformar()` y no la
  precondición, y `--solo-verificar` lee HEAD, donde el comentario no
  existía. **La corrección fue reformular la prosa** (el precedente exacto
  del comentario del andamiaje de seguros con el quirk de
  `placeholders()`); hacer 3c consciente de comentarios se descartó — un
  regex ingenuo reintroduciría el borde double-escaped que 3c existe para
  vigilar, y la pasada posicional del stripper ahí sería más maquinaria
  para un caso que una regla de redacción cierra. **LA REGLA: en los
  comentarios de un HTML publicable no se escriben esos literales.** Está
  anotada también en el propio comentario del bloque.
- **Validado de verdad, no a ojo**: `json.loads` sobre los bytes del
  ARTEFACTO; el tipo y las cinco propiedades contra el vocabulario oficial
  de schema.org DESCARGADO (existen todas y su domainIncludes cubre
  Organization; logo admite URL como valor); las cuatro URLs absolutas en
  200. Un JSON-LD mal formado no avisa — Google lo ignora en silencio y el
  hueco queda igual que antes—, por eso la validación y el contrato de
  supervivencia son parte del cambio, no adorno.

### La guarda de placeholders indexables: el deploy FRENA lo que check-ready solo informaba

**2026-08-08, diseño A del acople de check-ready, APROBADO E IMPLEMENTADO
el mismo día** (el diagnóstico y los diseños descartados quedaron en la
entrega al autor; acá va lo vigente). El hueco que cierra: check-ready
informa pero no frenaba nada (make-deploy no lo miraba; el acople era el
paso humano del README), y la tarjeta de sector casi publica sus dos TODO
en una página viva con las cinco guardas en verde — la atajó la decisión
del autor, no una guarda.

- **El criterio: una página INDEXABLE del artefacto no puede llevar
  placeholders TODO.** «Viaja + tiene placeholders» no distingue nada —
  seguros viaja con 25 a propósito—; la marca que distingue es la META
  noindex, que el andamiaje deliberado YA lleva por decisión (capa 1 de
  seguros). Un fragmento incompleto dentro de una página terminada nunca
  puede llevar noindex sin desindexarla: exactamente el caso tarjeta. Es
  **la inversa de `noindex_olvidado`** (sin placeholders ⇒ sin noindex);
  juntas cierran el iff andamiaje⟺noindex. No hizo falta metadato nuevo.
- **Las dos condiciones del autor, cumplidas**: (1) bajo `--fuente` AVISA
  y publica — un rollback publica el sitio de aquel día como era (la
  lección de los dos rollbacks que la tanda del stripper rompió por
  exigencias incondicionales); la severidad la decide `main()`, la función
  solo devuelve hallazgos. (2) El conteo NO se reimplementó:
  `placeholders()` de `_guardas` se partió en **`placeholders_de(html)`**
  —la derivación única, sobre texto— y el envoltorio de árbol de siempre;
  check-ready/check-structure y el deploy cuentan con LA MISMA función.
  El refactor no movió el conteo (verificado: 36 en 3 páginas, seguros 25).
- **Mide el ARTEFACTO, no el fuente**: los bytes transformados — lo que se
  mide es lo que se sirve, y el quirk de placeholders-dentro-de-comentarios
  no puede disparar ahí porque el artefacto no tiene comentarios.
- **Probada EN ROJO end-to-end**: el freno desde HEAD con un commit REAL
  en un worktree descartable (un TODO en /musubi/ → exit 1 nombrando
  página y conteo — el primer intento corrió el make-deploy VIEJO del
  checkout del worktree y dio verde: había que copiar el script editado,
  el test se corrigió), el aviso bajo `--fuente` contra el mismo commit
  (exit 0 con la línea de aviso), las dos familias de placeholder y el
  skip por noindex en sintéticos, HEAD real en verde, y los DOS tags de
  rollback publicando.
- **check-ready NO cambió y sigue siendo otra cosa**: informa el progreso
  de redacción sobre el árbol de trabajo (18 páginas, exit 2 esperado).
  La guarda nueva es la puerta de embarque sobre el artefacto. No hay
  acople de códigos de salida — lo acoplado es la INVARIANTE.

### CERO comentarios en lo SERVIDO: el deploy TRANSFORMA — y EL SERVIDO YA NO ES EL FUENTE

**2026-08-08, requisito del autor (condición sine qua non, no preferencia).
REVIERTE el «los comentarios se quedan en lo servido» de la decisión de la
rama de deploy.** El deploy filtraba por TIPO de archivo, así que las notas
de trabajo que viven DENTRO de los HTML/CSS/JS publicados —los comentarios,
en castellano— viajaban enteras al dominio: era un hueco del filtro, no una
decisión. Medido antes de tocar: **216 comentarios / 76,3 KB en las 16
páginas servidas** (la portada: 41 / 14 KB, el 48% de sus bytes);
**styles.css llevaba DOS TERCIOS del archivo en comentarios** (63,6 de 95,4
KB); main.js 14 de 22 KB; cube.js 26,6 de 48,7.

- **LA REGLA CON NOMBRE — EL SERVIDO NO ES EL FUENTE.** Desde el deploy 8
  hay una transformación en el medio: el HTML/CSS/JS publicado YA NO es
  reproducible desde el fuente por copia. **Toda verificación futura de
  bytes servidos se compara contra el ARTEFACTO (el árbol de `main`), nunca
  contra `redesign-trust`; y cualquier diagnóstico de algo raro en el
  dominio tiene que REPRODUCIR la transformación antes de concluir** (leer
  el blob de `main`, o regenerar con `make-deploy.py --solo-verificar`).
  Los diagnósticos DOM-contra-red del registro que comparan contra el
  fuente cargan con esta salvedad desde ahora; el fingerprint del conteo de
  `view-transition` (0 en el vigente) sobrevive tal cual — no vive en
  comentarios.
- **Los comentarios NO se tocan en el fuente, nunca**: quedan pegados a la
  línea que explican, que es donde cumplen su función. La eliminación vive
  en `make-deploy.py` (`transformar()` + `quitar_comentarios_*`), al
  generar el artefacto. Nada se archiva ni se muda a un `.md` aparte.
- **Qué transforma**: los `.html/.css/.js` publicables (hoy 20: 16 páginas
  + styles.css + main/cube/background). **Qué NO, y por qué**:
  `assets/vendor/` (el primer comentario de three.module.js es su
  `@license` MIT, que exige conservarse — sigue en la clase OID-idéntico);
  el contenido de `<script>`/`<style>` (texto crudo; los inline del sitio
  —el import map y, desde el 2026-08-10, el JSON-LD de Organization, los
  dos en la portada— son JSON sin comentarios); los template literals de
  los JS (su contenido es un STRING del programa — el caso real es el GLSL
  de background.js, cuyos DOS comentarios de cola SIGUEN sirviéndose: el
  autor los hizo reescribir EN INGLÉS en el fuente, porque quitarlos sería
  editar el shader cerrado); y `sitemap.xml`/`robots.txt` (no son HTML; sus
  comentarios son superficie deliberada en inglés — confirmado por él).
- **Los rellenos por lenguaje son semántica, no prolijidad**: en HTML el
  comentario se quita A NADA (`foo<!-- -->bar` renderiza «foobar»); en CSS
  y JS un `/* */` es SEPARADOR de tokens (`a/* */b` son DOS) y se reemplaza
  por UN espacio; el `//` muere en su `\n`, que se conserva — el ASI no se
  altera. La línea que queda solo-espacios se va entera; la que conserva
  contenido se recorta al final.
- **La garantía no se debilitó, y la pieza que lo sostiene es la GUARDA 4
  (contenido)**: la identidad recomputada es TAUTOLÓGICA ante un bug del
  stripper (los dos lados salen de la misma función) y check-modes solo
  navega la portada y /hajime/. Por eso la guarda del deploy verifica el
  contenido por derivaciones INDEPENDIENTES: cero comentarios contados por
  html.parser, mismo stream de eventos fuente↔artefacto (tags y atributos
  EXACTOS, texto normalizado), `texto_visible` idéntico, el chrome idéntico
  ENTRE páginas del artefacto (los marcadores ahora viven en
  `_guardas.BLOQUES_CHROME`, compartidos con chrome_divergente — una sola
  lista), el contrato de supervivencia con nombre (la meta de Search
  Console, el import map, el gc-pixel por página, las noindex, el @license
  del vendor) y la igualdad de tokens en CSS/JS. **Probada EN ROJO**: 11
  mutaciones dirigidas (cada una frena nombrando la pieza), 17 fixtures del
  stripper con las líneas trampa REALES del repo (regex tras `||` en
  main.js, `*/` dentro de un regex, el template GLSL opaco, string con URL,
  CSS con `/*` en string, UTF-8 cortado, NUL), y un E2E de 21 casos sobre
  rama descartable.
- **verificar_main_intacta regenera por la MISMA puerta
  (`arbol_publicable`) y ganó la DOBLE REGENERACIÓN DIAGNÓSTICA** (decisión
  del autor: nada de `--pisar` a ciegas ante un mismatch esperado): si la
  punta de main coincide con la regla VIEJA (filtrado solo), es un deploy
  pre-transformación — INTACTA, se publica encima sin pisar; un hotfix a
  mano no coincide con NINGUNA de las dos regeneraciones y frena, en sus
  dos modos (con y sin marca `Fuente:`), los dos probados en el E2E.
- **`hash-object -w --stdin` SIN `--path`, a propósito**: con `--path` git
  aplicaría el filtro clean de autocrlf y el determinismo entre máquinas
  moriría por el mismo riesgo CRLF que el plumbing existe para eliminar.
  Efecto lateral asumido: también las corridas de verificación escriben
  objetos sueltos en la base (inofensivo; los junta el gc).
- **Los centinelas del feed, del listado y del mapa NO necesitaron
  excepción, y no es casualidad**: generadores y guardas leen y escriben
  SOLO el fuente, que los conserva; el artefacto no los consume (notes.js
  empareja por `data-url`; ningún JS lee nodos de comentario). Se eliminan
  del artefacto como cualquier comentario.
- **Cierra de paso la observación menor del deploy 5**: la palabra «TODOs»
  del comentario ancla de /hajime/yorozu/ ya no viaja al dominio — ningún
  comentario viaja.
- **La rama `maintenance` quedó AFUERA en el deploy 8 a sabiendas — y se
  CERRÓ el mismo día, en su tanda aparte (2026-08-08)**: su generador
  ahora pasa el HTML por el MISMO `transformar()` de acá (una
  implementación, no dos que derivan), regenerada y probada — ver la
  actualización en la decisión de la rama `maintenance`.

### La nav con fondo propio en CSS: opaco por defecto, scroll-driven como mejora

**2026-08-08, decisión del autor (opción B) — y REEMPLAZA al mecanismo
`is-scrolled` de main.js, que se retiró CON su CSS y su token
`--nav-scrim`.** El bug: la nav es fixed y transparente, el fondo lo ponía
el JS al scrollear — y solo la portada carga JS, así que en las páginas de
prosa el texto se dibujaba encima del de la nav (capturas de iPhone en
/musubi/ y /method/; reproducido a 390px antes de tocar).

- **El reparto, y EL ORDEN NO ES NEGOCIABLE**: fondo OPACO (`--c-navy` +
  filete oro) como default en CSS puro; la transparencia sobre el hero es
  MEJORA PROGRESIVA con `animation-timeline: scroll()` dentro de
  `@supports`, cero JS (keyframe solo-`from`; el `to` implícito es el valor
  base — una sola fuente del estado final). Escrito al revés, el navegador
  sin soporte hereda el bug; escrito así, hereda una barra sólida sobre el
  hero — falla visible y benigna. Quien «restaure» is-scrolled o vuelva la
  transparencia al default está reintroduciendo el bug silencioso.
- **Verificado EJECUTANDO, no leyendo tablas** (Chrome headless):
  transparente a scroll 0, `rgba(4,13,24,0.5)` a 60px (la animación
  PROGRESA), opaco a 600; el fallback (animación anulada) opaco SIEMPRE;
  `prefers-reduced-motion` emulado → la regla global `animation: none` la
  apaga y queda el opaco, correcto. **Safari de iOS NO se pudo ejecutar en
  esta máquina (el riesgo aceptado de siempre)**: si su soporte falta o
  falla, el @supports lo deja en opaco — el modo de fallo es el diseñado.
  Longhands a propósito: el shorthand `animation` resetea
  `animation-timeline` (trampa de orden anotada en el CSS).
- **La compresión de la nav en teléfono (≤480px)**: nowrap en los rótulos
  («The Cube» partía a dos líneas), padding 12 / gap 8 / 0.72rem / 0.02em,
  y **`flex-shrink: 0` + nowrap en la marca 言霊** — el flex la aplastaba
  (caja de 27-51px para ~54 de contenido: kanji envuelto o superpuesto).
  Medido: una línea por rótulo y Contact adentro a 390/375/360 (right
  378/363/348, nav 62.2px de alto — `--nav-h` y las anclas no se tocaron);
  1440 sin cambios. **A 320px la fila sigue sin entrar (corte visible,
  asumido)** — los caminos descartados: nav a dos filas (cambia `--nav-h` y
  corre TODOS los destinos de ancla) y esconder o achicar el kanji (el
  autor lo quiere como está). Los CINCO rótulos quedan.
- **La leyenda de /method/**: cada par cuadrado+rótulo es una unidad
  (`.sources__legend-item`, inline-flex nowrap); si no entran, se apilan
  ENTEROS. Semántica intacta: lleno = Official, hueco = Attributed.

### El sistema de notas: contrato, molde, generador y archivo — construido, SIN deployar

**2026-08-07, decidido por el autor; construido completo en esta sesión.**
Lo que él trajo cerrado y NO se reabre: la ruta del archivo es **/notes/**
(hoy TODO nombre japonés en una URL es un elemento del cubo — seis caras,
tres subcaras, Musubi como núcleo—: el mapeo no tiene excepciones y un
nombre japonés que no sea cara ni núcleo lo rompería; además la marca ya
diseñada es `kotodama-type=note` — si el tipo es note, la colección es
/notes/; se descartó /archive/, que nombra «lo viejo» a una página que
también tiene lo más nuevo); las notas viven en **/hajime/`<slug>`/**, NO
bajo el árbol sectorial; y **el resumen ES el párrafo lead** — sin campo
summary aparte y sin override: un solo texto no puede contradecirse con el
del feed, y si un lead no funciona suelto como gancho, se reescribe el lead.

- **El contrato de metadatos: TODO sale del HTML de la nota, cero archivos
  laterales** (el criterio de make-sitemap, que ya lee el noindex de la
  propia página): tipo → la meta `kotodama-type=note`; cara → `<meta
  name="kotodama-face">` (una de las seis); título → el `<h1>`; slug → el
  directorio; fecha → `<time datetime="YYYY-MM-DD">` **visible al lector Y
  legible por máquina — el primer elemento temporal del sitio: ninguna otra
  página muestra fecha, y feed y archivo ordenan por él**; resumen → el
  lead con la clase **`note-lead`** (la clase del CONTRATO; la puesta es
  `face-page__lead`, separadas a propósito: si la puesta cambia, el
  contrato no se toca). El contrato vive y se valida en
  `_guardas.notas_publicables()`, que ABORTA nombrando página y campo.
- **UN generador — `tools/make-notes.py` —, UNA pasada, TRES salidas**: el
  feed de la portada, el listado de /notes/ y `notes/search-index.json`.
  **La portada va con CENTINELAS** (`FEED DE NOTAS` / `FIN DEL FEED DE
  NOTAS`): el generador reemplaza SOLO ese bloque — si escribiera
  index.html entero, la portada pasaría a ser artefacto derivado y editarla
  a mano sería el mismo modo de falla que `main` ya mitiga con el detector
  de hotfix. El feed va DESPUÉS del cubo y ANTES del About, y su fondo es
  EL MISMO `--c-surface-cube` a propósito: el degradado de apertura del
  About parte de ese color, así que la costura medida cubo→About no se
  rompe — se extiende. Formato del ítem: título + el lead como resumen +
  «Read more →»; muestra **las últimas 3** (`FEED_MAX`, perilla anotada:
  el feed es escaparate, no segundo archivo — el antecedente es el mapa en
  los quince footers, que murió por crecer sin tope) y «All notes →» al
  archivo. **REGLA DURA, cumplida: el feed REFERENCIA la nota, nunca copia
  el cuerpo.** **Caso cero notas: el bloque queda en SOLO centinelas** —
  ninguna caja vacía en la portada. Es el estado actual del repo.
- **Qué entra a las tres salidas: el criterio es `paginas_publicas()`** —
  el MISMO del sitemap y del mapa. Una nota con noindex (andamiaje) no
  existe para ningún consumidor. Un criterio, cero casos especiales.
- **La guarda es `notas_desactualizadas()`, en check-structure** (sección
  «Notas»), y compara los TRES artefactos contra la MISMA derivación que
  usa el generador — el patrón del mapa, sin segunda implementación.
  **Probada EN ROJO con nueve casos**: feed tocado a mano, centinelas
  perdidos (portada y /notes/), nota publicable con título TODO, nota sin
  `kotodama-face`, nota declarada fuera de /hajime/`<slug>`/, citar la meta
  en un comentario NO reclasifica (sin_comentarios), índice tocado a mano,
  y la excepción del deploy (abajo). **El abort de make-notes quedó
  verificado todo-o-nada por hashes**: nada se escribe si algo falla.
- **/notes/ es LA SEGUNDA PÁGINA CON JavaScript del sitio, a sabiendas**
  (decisión del autor): «cero JS» es propiedad de las páginas de LECTURA,
  no de una herramienta, y el archivo con buscador es una herramienta — el
  precedente es la portada, que carga JS por el cubo. El buscador
  (`assets/js/notes.js`) filtra por título Y CONTENIDO **el listado que ya
  está en el HTML** (lo escribe el generador: crawlers sin JS lo leen
  igual — la regla del contenido en el HTML no se rompe); el contenido
  viene del índice JSON, emparejado por `data-url`. El campo de búsqueda
  nace `hidden` y el script lo destapa sólo con el índice cargado Y filas
  que buscar; si el fetch falla, la página es el listado completo. Sus
  strings entraron a la guarda de castellano (`superficie_publicada`).
  **El listado sale al ANCHO COMPLETO con el tratamiento de la lista de 50
  fuentes de /method/** (column-width 26rem, mismas constantes — criterio
  ya establecido: se escanea, no se lee renglón a renglón) y el rotulado
  por ítem usa el vocabulario de /method/ trasladado: la CARA en el
  registro de `sources__ja` (oro, chico) y la FECHA en el de
  `sources__note` (muted) — **el romaji de la cara como rótulo legible,
  porque lleno/hueco codifica DOS estados y acá hay seis caras**; un
  rótulo de texto no es un marcador mudo, así que no necesita leyenda.
- **El índice, MEDIDO**: 121 bytes vacío; con una nota simulada de ~1.500
  palabras, 9,8 KB (~9,6 KB por nota) → **20 notas ≈ 190 KB sin comprimir
  (~40 KB por el gzip de Pages)**. Crece lineal con el largo del texto:
  notas de ~700 palabras darían la mitad. Se re-mira si el archivo pasa de
  ~50 notas; la salida entonces es paginar el índice, no comprimir a mano.
- **La excepción del deploy: `PUBLICABLES_PESE_AL_TIPO =
  ("notes/search-index.json",)`** en make-deploy.py, documentada al lado
  de la de maelstrom.css porque es SU INVERSA: allá, material de trabajo
  en formato de sitio (.css), excluido por nombre; acá, un artefacto del
  sitio en formato de trabajo (.json), admitido por nombre. **La regla por
  tipo NO se abre** — probado: otros .json y .md siguen cayendo por el
  tipo. El índice entró además a CONTRATO: notes.js lo pide por `fetch`,
  que verificar_completo no ve (busca href/src/import, no strings).
- **NADA deployado y NADA enlazado desde lo publicado** (el precedente de
  seguros): /notes/ y la nota de ejemplo llevan noindex → fuera del
  sitemap, del mapa, del feed y del listado, sin enlaces entrantes — el
  feed real está VACÍO. **La nota de ejemplo (/hajime/nota-ejemplo/) es un
  FIXTURE del productor: se BORRA cuando exista la primera nota real, no
  se redacta** — su slug en castellano es deliberado, la misma regla que
  los TODO. `check-ready` sale `2` y es lo esperado; **`noindex_olvidado`
  NO se dispara** porque las dos páginas nuevas tienen placeholders
  legítimos — se disparará, correctamente, si alguien las redacta y deja
  la meta, que es exactamente su función.
- **AL ESTRENAR /notes/ (con la primera nota real)**: borrar la nota de
  ejemplo, sacar el noindex de /notes/ (con su comentario), redactar su
  description y su gloss, **sumar `"notes"` a ORDEN_SITIO en _guardas.py**
  — sin ese lugar consciente, make-sitemap ABORTA nombrando la página: es
  el flujo diseñado del mapa, no un olvido—, **sacar las TRES exclusiones
  temporales de `NO_PUBLICABLES` en make-deploy.py (`notes/`,
  `hajime/nota-ejemplo/`, `assets/js/notes.js`) y devolver
  `notes/search-index.json` a `CONTRATO`** (2026-08-08: el sistema quedó
  FUERA del artefacto hasta el estreno — ver la decisión del deploy sin
  contenido), regenerar sitemap y notas, y
  actualizar el baseline. **Y la cadena «First analysis on the way» caduca
  en sus TRES lugares a la vez** (ver la lista de duplicadas en /musubi/).
- **La VUELTA de una nota — CERRADA (2026-08-08, decisión del autor): «←
  All notes», a /notes/.** El argumento que la cerró: el criterio del
  ORIGEN no decide cuando hay DOS orígenes reales (el feed de la portada y
  /notes/), y ahí rige el rótulo por convención — el precedente de
  /disclaimer/ y /sitemap/. «All notes» sirve a los dos. Implementado en
  el molde (la nota-fixture).
- **Y el RÓTULO DE CARA enlazado en la cabecera (misma decisión, 2026-08-08)**:
  con «All notes» solo, la nota no mostraba por ningún lado a qué cara
  pertenece — lo declaran la URL y la meta `kotodama-face`, y el rótulo lo
  recupera para el lector Y enlaza a la cara. **El tratamiento es el del
  rótulo de cara del listado de /notes/, trasladado** (instrucción del
  autor: no inventar un patrón nuevo): romaji en oro — que acá lo da la
  regla global de `<a>`, **SIN CSS nuevo**: una regla vacía para
  `note-face` sería el patrón de reglas-sin-uso que este proyecto ya pagó
  dos veces (anotado junto a `.face-page__date` en el CSS) — en la línea
  de la fecha y en su mismo orden: **cara · fecha**. **La clase
  `note-face` entró al CONTRATO** (el precedente de `note-lead`): es la
  segunda copia visible del dato que ya declara la meta, y dos copias del
  mismo dato sin guarda derivan — `notas_publicables()` compara texto y
  href contra la meta y ABORTA nombrando la diferencia (el armado típico
  de una nota es copiar otra como molde y cambiar la meta: exactamente el
  olvido que esto vuelve rojo). **Probado EN ROJO con CINCO casos**: sin
  rótulo, texto que no coincide, href que no coincide, el correcto ENTRA,
  y href-antes-de-class tolerado (el precedente de `tarjetas_de()`). El
  fixture es noindex y la guarda no lo valida — por diseño (sus TODO
  abortarían); el molde ES la referencia del marcado.

### La tarjeta de SECTOR: la variante sin kanji — el patrón de la familia

**ACTUALIZACIÓN 2026-08-08 — EL MARCADO SALIÓ DEL ARCHIVO, por decisión
del autor: /hajime/yorozu/ viaja en el deploy y sus dos TODOs quedaban
visibles en ver-código de una página publicada — «un TODO en el HTML
servido no va en el sitio cuyo argumento entero es el rigor». Se descartó
comentarla: el quirk de `placeholders()`-cuenta-comentarios es un
mecanismo trabajando por accidente, no una garantía. LO QUE QUEDA VIVO es
el PATRÓN: `.face-card--sector` en el CSS y esta decisión — eso no se
tocó. EL PASE DE REPOSICIÓN, cuando el autor pase el título y la línea de
función: reescribir en `hajime/yorozu/index.html`, dentro de
`face-page__body` DESPUÉS del párrafo (el comentario ancla marca el
lugar), el `<ul class="face-page__cards">` con
`<a class="face-card face-card--sector" href="/hajime/yorozu/japan/seguros/">`
+ `face-card__title` + `face-card__meta > face-card__domain` — el marcado
exacto está en el commit `30dc0d9` —, actualizar el baseline (hoy 36) y
recordar que la tarjeta vuelve a ser REQUISITO del mapa al sacarle el
noindex a seguros. El registro de abajo describe la construcción original
del 2026-08-07.**

**2026-08-07, instrucción del autor; el TÍTULO y la LÍNEA DE FUNCIÓN los
define él y hoy son TODO — no se inventan ni se rellenan con algo que
parezca definitivo.** El problema real: las tarjetas de subcara son kanji +
romaji + línea de función, y el kanji es el elemento visual que las
sostiene — y una sección de sector NO tiene kanji, por decisión cerrada (la
escritura japonesa la cierra el autor; no se inventa). La forma existente
no servía, y la variante es nueva A PROPÓSITO: **`.face-card--sector`,
donde el TÍTULO ocupa el lugar visual del kanji** — display, cuerpo grande
(1.4rem), color de texto pleno: el ROL del kanji (el oro es del romaji, y
acá no hay pareja que distinguir) — con la línea de función debajo en el
registro de siempre (`__domain`). Borde, fondo y hover de `.face-card`: la
misma familia, un miembro sin kanji. **Es la primera de una familia que va
a crecer**: banca, mercados y todo sector futuro tienen el mismo problema y
usan esta variante — se definió una vez, acá. **Dos caminos descartados,
para que no vuelvan**: inventarle un kanji (contradice la decisión cerrada)
y dejar el hueco del kanji vacío (se lee como algo roto). La primera
instancia está en /hajime/yorozu/, debajo del párrafo (la prosa aprobada NO
se tocó), apuntando a la sección de seguros — y cierra de paso el requisito
del mapa: con la tarjeta puesta, sacar el noindex de seguros ya no aborta
por falta de tarjeta. **Ojo para el próximo deploy**: mientras el título
sea TODO, un deploy intermedio publicaría la tarjeta con castellano visible
en una página viva — el pase de la tarjeta va junto con el texto de
seguros, o antes si el autor pasa el título suelto.

### El mapa del sitio: la SUBPÁGINA /sitemap/ + enlace en el footer

**2026-08-07. La forma vigente REEMPLAZA al bloque en los quince footers,
que vivió unas horas: el autor lo aprobó, lo vio en capturas y lo revirtió
— «aprobé el diseño y me equivoqué al aprobarlo»: un árbol de quince
entradas repetido en las quince páginas es demasiado footer, y crece con
cada sección nueva.** Las decisiones de fondo NO cambiaron: mapa COMPLETO
con jerarquía visual (con cuatro niveles de URLs la navegación por
descubrimiento dejó de alcanzar; el antecedente es la columna «Platform»,
que se fue por listar dos de cinco — un mapa exhaustivo no tiene ese
defecto) y GENERADO — lo escribe `tools/make-sitemap.py` en la misma
corrida que sitemap.xml. Lo que cambió es el DESTINO: el árbol vive en
UNA página y el footer lleva sólo la puerta.

- **La ruta es `/sitemap/` a propósito**: comparte nombre con
  `/sitemap.xml` porque son DOS RENDERIZACIONES DE LA MISMA LISTA — el XML
  para las máquinas, la página para el lector. No hay colisión técnica
  (directorio contra archivo) y la rima de nombres es información real.
- **La página usa el molde de /method/**: cabecera sin kanji (no hay uno
  cerrado para «mapa del sitio» y no se inventa) y sin marca de agua (la
  marca es el kanji de la PROPIA página; sin kanji no hay marca). Título
  «Site map», línea de función «Every page, in one place». El árbol va en
  dos secciones con `face-page__subtitle` — **«The Site» PRIMERO y «The
  Cube» después, orden del autor (2026-08-07)** — y la jerarquía se dibuja
  con sangría y filete oro (`.map-list--sub`), sin tope de profundidad.
- **El enlace del footer va en la línea de abajo, junto al ©**: «© 2026
  Kotodama Finance · Open access · Site map». La barra inferior es la
  meta-navegación, donde un mapa del sitio se busca por convención, y no
  agrega ni un píxel arriba del bloque de marca. Es lo ÚNICO del mapa en
  el footer, está en las dieciséis páginas y lo vigila la identidad del
  footer (probado en rojo: sacarlo de una página da footer divergente).
- **La vuelta es «Back to the start» (`/`), y el criterio del origen SÍ la
  cubre**: a /sitemap/ se llega desde el footer de cualquier página, o sea
  que no hay origen único — exactamente el caso de /disclaimer/, que
  también se alcanza desde el footer global y ya tenía ese rótulo. No es
  una categoría nueva: es el precedente aplicado.
- **/sitemap/ va a sitemap.xml pero YA NO se lista a sí misma (2026-08-08,
  decisión del autor — REVIERTE el «se lista a sí misma» que decía acá)**:
  la entrada «Site map» enlazaba a la página que el lector ya está mirando
  y DESAPARECE del renderizado (no queda texto plano). La exclusión vive en
  `mapa_bloque()` — la única derivación, compartida con la guarda, que
  siguió el cambio sola (probado en rojo y en verde) — y es SOLO del HTML:
  `paginas_publicas()` intacta, sitemap.xml byte-idéntico con /sitemap/
  adentro (indexable legítima que Google ya conoce), el slug SIGUE en
  ORDEN_SITIO (sin su lugar, el abort de nivel superior frena la
  generación). El enlace del footer también es autoenlace en esa página y
  NO se tocó: arreglarlo rompería la identidad byte a byte de los
  dieciocho footers, que vale más.

- **Los nombres salen del `face-page__romaji` de cada página** — el nombre
  con que la página se presenta en su h1: corto, sin kanji, sin
  transformación. El `<title>` se descartó como fuente: habría que pelarle
  « — Kotodama Finance» Y el kanji («Hajime 肇»), o sea derivar
  transformando. La portada va como **«Home», constante del generador**: su
  h1 es el titular del hero, no un nombre.
- **Romaji solo, sin kanji**: en una lista densa el kanji junto al romaji
  sólo duplicaría el nombre de al lado — la prueba exacta del japonés
  ornamental que rige la prosa de /hajime/ — y la nav ya escribe «Musubi»
  pelado. Consecuencia buena: el bloque no obliga a regenerar ningún subset.
- **Dos grupos, The Site primero**: «The Site» — Home, Musubi, Method,
  Site map, Disclaimer—; «The Cube» — las seis caras en el orden de la
  grilla de la portada, con las subcaras anidadas. La 404 no entra.
  **El futuro de Yorozu quedó SIMULADO Y MEDIDO (2026-08-07)**: seguros
  redactada más una página de QUINTO nivel aparecen anidadas donde
  corresponde (Insurance bajo Yorozu salteando /japan/ sin página;
  Solvency bajo Insurance) y la sangría se lee bien a 1440 y a 375 — no
  hay que cambiar la forma con la profundidad. Y **una página nueva bajo
  una cara NO aparece sola**: el abort de la tarjeta rige a TODA
  profundidad (probado en los dos niveles) — el flujo por sección nueva
  es página → tarjeta en el padre → `make-sitemap`, y es fricción
  correcta — **con el argumento que la justifica de verdad, en palabras
  del autor (2026-08-07): el orden del mapa se DERIVA del orden de las
  tarjetas — sin tarjeta no hay orden derivable, y caer a alfabético
  sería una decisión de presentación que no tomó nadie. La fricción es
  consecuencia del diseño, no un chequeo agregado encima.** (La tarjeta
  además es la puerta de navegación que igual habría que crear.) Anotado
  también en el comentario del mapa en `_guardas.py`.
- **TODO el orden se deriva, salvo uno**: las caras van en el orden de las
  tarjetas de la grilla; los hijos de una página, en el orden en que el
  PADRE los presenta como tarjetas `.face-card`. Lo único no derivable es el
  orden del nivel superior no-cara (un orden es una decisión de
  presentación): vive en `ORDEN_SITIO` (`tools/_guardas.py`) **con abort**:
  una página sin lugar FRENA la generación nombrándola, sin escribir nada —
  todo-o-nada; un mapa que adivina publicaría el hueco idéntico en todas las
  páginas. Agregar una página normal no toca nada a mano: correr
  `make-sitemap`; el olvido lo caza check-structure («Mapa del sitio en el
  footer»).
- **El conjunto de URLs es EXACTAMENTE el del sitemap**:
  `paginas_publicas()` en `_guardas` es la fuente común de los dos
  artefactos — no pueden divergir. Por eso **HOY el mapa NO lista el
  andamiaje de seguros, y es a propósito**: su noindex de placeholder lo
  saca de los dos; listarlo habría enlazado una página de TODOs,
  deshaciendo la huérfana-a-sabiendas por la puerta del mapa.
  Entra solo, junto con el sitemap, cuando el texto llegue y la meta se
  vaya. («Incluye la sección sectorial» se cumple en cuanto exista como
  contenido, no como andamiaje.)
- **Consecuencia para el pase de redacción de seguros**: al sacar el
  noindex, `make-sitemap` ABORTA hasta que /hajime/yorozu/ presente la
  página como tarjeta — el generador exige que todo hijo sea tarjeta de su
  padre. La tarjeta pendiente de aprobación del autor dejó de ser sólo
  navegación: es requisito del mapa. Si el autor decidiera NO querer la
  tarjeta, ahí se diseña la alternativa (no antes).
- **Las notas futuras NO entran al mapa — lo trajo resuelto el autor**: con
  veinte notas el footer sería una lista larga en todas las páginas. En su
  lugar irá LA PÁGINA DE ARCHIVO cuando exista, **por existencia, no por
  comentario**: es una página normal — el descubrimiento la encuentra y el
  abort obliga a ubicarla conscientemente en `ORDEN_SITIO`. Se eligió
  condicional-por-existencia y no una entrada comentada porque el bloque se
  REGENERA: un comentario en la salida se pisaría en la próxima corrida, y
  la condición tiene que vivir en el código que corre, no en algo que
  alguien deba acordarse de descomentar. Las notas SÍ van a sitemap.xml
  (son contenido indexable); sólo el mapa las resume en el archivo.
- **Nota vs. subcara — la respuesta a la pregunta del autor: la ruta sola
  NO alcanza, la distinción es DECLARADA.** Una nota y una subcara viven al
  mismo nivel bajo /hajime/, así que cada nota llevará
  `<meta name="kotodama-type" content="note">` en su propio HTML, **desde
  la primera**. La marca convierte el olvido en rojo: una página bajo una
  cara que no sea tarjeta de su padre ni declare la marca ABORTA la
  generación con instrucciones. No se puede crear una nota silenciosamente
  mal clasificada. Y la marca tendrá un segundo consumidor —el índice JSON
  del buscador del archivo—, así que olvidarla también dejaría la nota
  fuera de la búsqueda: fallo visible, no silencioso.
- **Las guardas: el enlace lo cubre la identidad del footer que ya
  existía** (`chrome_divergente`; por lo mismo, el pixel de GoatCounter
  sigue AFUERA del footer), y el árbol lo cubre `mapa_desactualizado()`,
  que compara /sitemap/ contra EXACTAMENTE lo que el generador escribiría
  hoy — misma función, sin segunda implementación. **Probado EN ROJO con
  DIECISIETE casos, re-corridos ENTEROS sobre la arquitectura de
  subpágina**: árbol viejo; footer sin el enlace en una página
  (divergente); abort por página sin tarjeta, por nivel superior sin
  lugar, por tarjeta duplicada y por tarjeta comentada (el mensaje nombra
  la página en todos); nota excluida sin abortar y DENTRO del sitemap;
  citar la meta de nota en un comentario NO reclasifica;
  href-antes-de-class tolerado; /sitemap/ sin marcadores y /sitemap/
  ausente, nombradas; todo-o-nada verificado por hashes (XML y páginas
  intactos tras un abort).
- **La revisión adversarial (12 agentes, mismo día) dejó CINCO
  correcciones**, todas reproducidas antes de corregirse: (1) la escritura
  pasó a todo-o-nada DE VERDAD — todas las inyecciones se derivan en
  memoria ANTES de escribir el primer byte, y una página sin punto de
  inserción aborta nombrándola; antes, un `ValueError` crudo a mitad del
  loop dejaba el XML actualizado y los footers divergentes, exactamente lo
  que el comentario del script prometía imposible. (2) Las regex del mapa
  y del noindex miran MARCADO VIVO (`sin_comentarios()`): una tarjeta
  comentada ya no evade el abort, y un comentario que meramente CITA la
  meta de nota ya no saca la página del mapa en silencio — era el agujero
  de `placeholders()`-en-comentarios con la polaridad invertida: allá
  falso positivo ruidoso, acá salida incorrecta muda en todas las páginas.
  (`placeholders()` conserva su quirk A PROPÓSITO: cambiarlo movería el
  baseline.) (3) Una tarjeta duplicada al mismo destino ABORTA — antes
  publicaba la entrada repetida con todas las guardas en verde, porque la
  guarda compara contra la misma derivación. (4) `tarjetas_de()` tolera
  orden de atributos y clases compuestas — antes `href` antes de `class`
  abortaba con diagnóstico FALSO («no la presenta como tarjeta», con la
  tarjeta a la vista); el precedente de tolerancia ya estaba en
  RE_ROMAJI_H1. (5) El mensaje del abort de nivel superior ya no manda a
  un callejón: un `.html` suelto en la raíz no puede ubicarse vía
  ORDEN_SITIO (que sólo genera candidatos de directorio) y ahora el
  mensaje da las salidas reales. El sexto hallazgo —el ancla Contact
  aterrizando con el correo bajo el fold a 1280×720— quedó DISUELTO por la
  reversión a /sitemap/: re-medido con el footer compacto, el correo
  vuelve a aterrizar visible (y≈436–462 contra 720) y la nav no se tocó.
- De paso, `RE_NOINDEX` quedó unificado en `_guardas` (tres copias inline
  del mismo regex → una constante).

### El andamiaje de la capa 1 de seguros — /hajime/yorozu/japan/seguros/

**2026-08-07, por instrucción del autor: SOLO estructura con placeholders —
el texto lo escribe él aparte y se publica cuando esté.** La capa 1 de la
sección de seguros japoneses: marco regulatorio y estructura del mercado,
escrita con fuentes primarias y SIN depender de la base de datos — por eso
sale antes que cualquier dashboard.

- **El `context.md` del autor SÍ está en esta máquina (localizado
  2026-08-07, corrige el «no está» que decía el registro de los kanji)**:
  `C:\Users\vivom\OneDrive\Documents\Claude\Projects\Home Server\Kotodama
  Finance\kotodama_finance_context.md` — fuera del alcance del MCP de
  documentos (su allowlist es solo el repo; probablemente por eso no se
  encontró antes), editable con las herramientas locales. La decisión del
  noindex quedó anotada allá ese día, a pedido del autor, en §Sitio web F1
  (buscar «noindex MIENTRAS HAYA PLACEHOLDERS» — es la marca de
  idempotencia acordada). Mismo trato que siempre: sus decisiones se copian
  literales, no se reinterpretan.
- **La ruta viene del context.md del autor (§Yorozu) y no se rediscute**:
  país ARRIBA del sector, todo anidado bajo /hajime/. Y
  **/hajime/yorozu/japan/ NO lleva página, decisión aceptada**: da 404 y
  está bien — nadie tipea ese segmento a mano, se llega desde
  /hajime/yorozu/, y un índice de un solo elemento es estructura por si
  acaso. Se crea cuando existan bancos y mercados. NO crear esa página ni
  un redirect.
- **El molde es el de /method/, no el de las caras**: apertura + NUEVE
  secciones (`face-page__section` + `face-page__subtitle` + prosa
  adentro). Nueve secciones no entran en el molde corto de una cara. El
  breakout `--wide` de la lista de fuentes de /method/ NO se aplicó al
  andamiaje a propósito: se decide con el texto, si la sección 9 trae una
  lista comparable — está anotado en el HTML.
- **Sin kanji en la cabecera y sin marca de agua lateral, y no son
  faltas**: no hay un kanji cerrado para esta sección y la escritura
  japonesa la cierra el autor, siempre — no se inventa. La cabecera usa el
  patrón de /method/ (título sin kanji + línea de función), que existe
  para las páginas que no son caras del cubo; y la marca de agua es el
  kanji de la PROPIA página, así que sin kanji no hay marca — tampoco se
  sustituye con el logo 言霊 (criterio ya decidido con /method/). Si el
  autor cierra un kanji algún día, entran los dos juntos.
- **La vuelta va a /hajime/yorozu/** («Back to Yorozu»): el criterio de
  los rótulos por ORIGEN, extendido un nivel — las caras vuelven al cubo,
  las subcaras a /hajime/, las secciones de un sector a su subcara.
- **25 placeholders, baseline actualizado, `check-ready` en `2`
  ESPERADO** (era 5 de su docstring). Los títulos de las nueve secciones
  en los TODO son DE TRABAJO — los definitivos van con el texto.
- **El enlace desde /hajime/yorozu/ QUEDA PENDIENTE DEL AUTOR**: es una
  página con texto aprobado y no se toca sin su visto bueno. Hasta
  entonces la página nueva queda huérfana a sabiendas (ninguna guarda
  exige enlaces entrantes).
- **NOINDEX MIENTRAS SEA PLACEHOLDER (2026-08-07, decidido con el autor)**:
  el riesgo de indexación era cero mientras el andamiaje no estuviera
  deployado, pero un deploy intermedio (un ajuste a otra página antes del
  texto) lo publicaría, y el sitemap es exactamente cómo Google descubre
  URLs sin enlaces entrantes — una página de TODOs en los resultados, en la
  primera sección de contenido real, es el peor lugar. **EL DEPLOY
  INTERMEDIO OCURRIÓ el mismo día (el del mapa del sitio, deploy 4) y la
  meta hizo su trabajo, verificado en el dominio**: la ruta responde 200
  con el noindex puesto y no aparece en el sitemap.xml servido. La página lleva
  `noindex, follow` (el patrón de la 404) y **la exclusión del sitemap se
  DERIVA de esa meta** — `make-sitemap` la lee de la propia página, sin
  lista a mano (hoy: 13 URLs). **Las tres direcciones tienen guarda y las
  tres se probaron EN ROJO**: noindex listado en el sitemap frena
  `check-structure` (la contradicción de siempre); sacar el noindex sin
  regenerar el sitemap frena `check-structure` («falta en el sitemap»); y
  **el olvido silencioso — redactar la página y dejar el noindex, que la
  publicaría invisible para siempre con todo en verde — frena `check-ready`
  con código 1** (`noindex_olvidado()` en `_guardas`: una página sin
  placeholders no puede llevar noindex, salvo la 404). AL REDACTAR: sacar
  la meta con su comentario, regenerar el sitemap, actualizar el baseline.
  El aviso de método que dejó la prueba: la primera simulación del rojo
  quitó el texto «TODO» pero dejó los `class="todo"` — la página seguía
  contando placeholders y el rojo no salía; redacción real = texto Y clases
  fuera. Provocar de verdad el momento en que pasaría.
- Un hallazgo del armado, anotado también en el HTML: **el atributo
  literal de la clase de placeholder entre comillas cuenta para
  `placeholders()` AUNQUE esté dentro de un comentario** — esa guarda no
  filtra comentarios. El primer conteo dio 26 por eso; reformulado el
  comentario, 25 — sin la reformulación, `check-ready` nunca habría
  vuelto a 0 al terminar la redacción.

### La rama de deploy: `main` publica SOLO el sitio — el paso 5 dejó de ser merge

**Decidido por el autor e IMPLEMENTADO el 2026-08-06.** GitHub Pages publica
la rama entera, así que el merge de `redesign-trust` habría servido
`CLAUDE.md`, `tools/` y `docs/` desde kotodamafinance.com — las notas de
trabajo en la misma URL que la credencial profesional del autor. Desde ahora
**`main` es una rama-artefacto que se GENERA con `tools/make-deploy.py`**,
igual que `maintenance`: un artefacto derivado no se mantiene, se regenera.

- **Descartadas, y por qué**: repo privado (Pages no publica repos privados
  en cuenta gratuita; se reevalúa si algún día hay plan de pago) y sacar las
  notas del repo (Code perdería su memoria entre sesiones — lo que salvó el
  retomado tras el crash; costo demasiado alto).
- **Qué tapa y qué NO, explícito a pedido del autor**: tapa las notas como
  **documentos con URL propia** en el dominio. **Y desde el 2026-08-08
  TAMBIÉN las menciones dentro de lo servido: la política «los comentarios
  se quedan» quedó REVERTIDA por el autor** — el deploy los elimina del
  artefacto (ver la decisión de la transformación, primera de la lista; el
  fuente los conserva). Lo que sigue sin taparse es el repo público en
  GitHub, donde la rama de desarrollo sigue visible (limitación aceptada;
  efecto lateral bueno: la default branch es `main`, así que quien cae al
  repo ve solo el sitio).
- **La lista autoritativa de exclusión es `NO_PUBLICABLES` en el script**
  (acá se resume, no se duplica): `CLAUDE.md`, `README.md`, `.gitignore`,
  `docs/`, `tools/`, `assets/img/README.md`, y **`assets/css/maelstrom.css`
  — el único caso límite, decidido por el autor**: no es CSS del sitio
  apartado sino material de trabajo en formato `.css` (su encabezado es
  documentación de calibración con el bug táctil). Como la regla por tipo no
  caza un `.css`, está en la lista explícita CON el motivo anotado y la
  guarda además lo verifica **por nombre**. Hoy (2026-08-07, con el
  andamiaje de seguros): 40 publicables, 32 excluidos (el 32 cuenta al
  propio `make-deploy.py` — por eso el script y esta nota entraron en EL
  MISMO commit: por separado había una ventana en que el doc afirmaba 32 y
  el script imprimía 31. El conteo de referencia es siempre el que imprime
  el script).
- **La guarda corre DENTRO del script, todo-o-nada, y se probó EN ROJO antes
  de confiar en su verde** (2026-08-06 — los tres casos pedidos por el autor,
  más lo que agregó la revisión adversarial del mismo día: 22 agentes, 10
  hallazgos confirmados por reproducción, todos corregidos): (1) **completo**
  — sitemap→páginas, referencias de HTML/CSS/JS/import map resueltas dentro
  del árbol (comillas dobles Y simples, srcset, `url()` en `<style>` inline —
  las tres formas que la primera versión no veía, cada una con su rojo),
  infra de Pages; probada quitando `sugao/index.html`: frenan LAS DOS ramas,
  el sitemap y la extracción. (2) **sin notas** — por TIPO (cero
  `.md`/`.py`/`.json`) además de por ruta, con un `.woff2` colado en `tools/`
  como rojo (un `.py` pasaba por el tipo y dejaba la rama de ruta sin
  ejercitar — hallazgo de la revisión). (3) **identidad** — OID ajeno Y ruta
  extra inyectada (la única defensa contra un `.css`/`.png` colado, que
  sin-notas no ve). Más: exclusión sin efecto FRENA desde HEAD, la detección
  de main se probó en sus CUATRO estados (intacta / hotfix / marca-con-árbol-
  ajeno / **Fuente fuera de la base de objetos**, que antes moría con el
  fatal crudo sin dejar usar `--pisar`), un «Fuente: <texto>» casual en un
  mensaje NO cuenta como deploy (el detector usa EL MISMO regex que la marca,
  no un substring), y **`main()` corre de punta a punta en la prueba** sobre
  un ref descartable — árbol sucio, deploy completo con `update-ref`
  compare-and-swap, idempotencia, freno de hotfix y `--pisar` — porque el
  cableado que solo se estrena el día del deploy es exactamente «una variante
  que sólo se LEE».
- **`main` NADIE la edita a mano — y el script lo detecta antes de pisar**:
  cada commit de deploy declara su fuente (`Fuente: <hash40>` en el
  mensaje); antes de publicar, el script regenera el árbol desde ese hash y
  lo compara con el de la punta de `main`. Si no coinciden —hotfix a mano, o
  reglas de exclusión cambiadas desde ese deploy—, FRENA señalando el diff;
  `--pisar` publica igual, a sabiendas.
- **La excepción única, ejecutada el 2026-08-07: el commit vacío de
  RETRIGGER.** Si un build de Pages queda encolado del lado de GitHub y no
  se puede cancelar («Failed to cancel workflow»), un commit vacío en
  `main` dispara un run nuevo que entra en cola limpia — destrabó el
  deploy 2 al instante (`00c4a00`). **El mensaje DEBE declarar la misma
  `Fuente:` del deploy vigente, con el hash COMPLETO**: el commit vacío
  conserva el árbol solo, y con la marca puesta `verificar_main_intacta`
  da «intacta» y el próximo deploy sigue de largo; SIN la marca, ese
  deploy frena creyendo que hubo edición a mano (es el cuarto estado de la
  detección: punta sin marca con deploys en la historia). Verificado
  EJECUTANDO `make-deploy.py` contra la punta nueva ANTES del push
  («intacta» + «ya está en este contenido»), no deducido. Se fabrica con
  `git commit --allow-empty -F <mensaje>` en un worktree temporal de
  `main`, sin tocar el árbol de trabajo. El re-run desde la UI de Actions
  sigue siendo la primera opción; esto es para cuando la cola misma está
  trabada — y no es vía para NINGÚN otro cambio: contenido va siempre por
  desarrollo → guardas → make-deploy.
- **El tag de publicación va en el commit FUENTE de `redesign-trust`** —el
  que pasó por las guardas—, con el hash cruzado en el mensaje del commit de
  `main`: trazabilidad en las dos direcciones. `v1-content-complete` no se
  mueve.
- **Rollback**: `python tools/make-deploy.py --fuente <commit-bueno>` + push.
  El procedimiento concreto, escrito para el día del apuro, está en el
  README («Publicar»). La red para BAJAR el sitio sigue siendo `maintenance`.
  **Y el rollback se PROBÓ contra `v1-content-complete`, que dejó una regla
  medida, no deducida**: ese tag es anterior al juego completo de favicons y
  a `assets/img/` entero, su sitio era consistente igual (su HTML no los
  referenciaba), y la primera versión de la guarda —un freno único— bloqueaba
  ese rollback legítimo dos veces. La partición vigente: bajo `--fuente` lo
  DURO es lo que rompe Pages o publica notas (CNAME/.nojekyll/index/404,
  tipos de trabajo, referencias rotas) y el CONTRATO del sitio de hoy
  (favicons, manifest, og-image, robots, sitemap) solo AVISA — el sitio de
  ese día se publica como era.
- **`--previsualizar` (2026-08-14, pedido del autor): el paso de MIRAR el
  artefacto con ojos humanos, ANTES del push.** El hueco que cierra: desde
  el deploy 8 el árbol de trabajo NO es lo que se sirve, y check-modes
  contra main es automático y navega dos páginas — no había forma de VER el
  sitio completo como va a quedar. El modo NO genera nada (la corrida sin
  flags ya dejó el artefacto como punta local de `main`): la sirve desde un
  worktree efímero `_dev/preview` en `127.0.0.1:8001` — **el 8001 A
  PROPÓSITO: el :8000 es del árbol de trabajo** (desarrollo y guardas, y el
  flujo del deploy lo baja y lo relevanta); en su puerto propio la preview
  convive con todo eso. Ctrl+C cierra y borra el worktree; los restos de un
  kill duro se barren al arrancar la siguiente corrida. Es modo EXCLUSIVO
  (ignora los demás flags) y UNA preview a la vez (dos compartirían el
  worktree). **Tres trampas medidas en la construcción, no deducidas**:
  (1) el checkout del worktree aplicaba autocrlf y la preview servía 288
  CRLF que el artefacto no tiene — va con `-c core.autocrlf=false`: lo que
  se navega es BYTE A BYTE lo que Pages sirve; (2) **en Windows el bind NO
  detecta el puerto ocupado** — un wildcard (`0.0.0.0`/`::`, lo que abre
  `python -m http.server`) y el loopback conviven como bindings DISTINTOS
  sin error, y la preview le robaba el tráfico de localhost al servidor de
  desarrollo en silencio (además SO_REUSEADDR, que HTTPServer trae puesto,
  deja bindear hasta el puerto idéntico) — la ocupación se detecta
  CONECTANDO (sonda antes de armar nada) y el flag va apagado; (3) el
  encabezado con flush, porque redirigido quedaba invisible detrás del log
  de requests. El paso quedó como el 4 del procedimiento del README
  («Publicar», hoy siete pasos) y en la lista «Lo que sigue» que imprime el
  deploy. Probado EJECUTANDO: lo servido byte a byte contra los blobs de
  main (con el árbol de trabajo sirviendo distinto en :8000 a la vez, la
  prueba de que es el artefacto), notas de trabajo en 404, Ctrl+C y puerto
  ocupado limpian, el kill duro se recupera solo, no escribe nada, y el
  camino del deploy sigue en verde tras el cambio. **La revisión
  adversarial (3 lentes + refutadores, 2026-08-14) confirmó 10 hallazgos
  por reproducción — los 10 corregidos antes de commitear**, y dejó tres
  reglas del modo: el barrido de restos cubre TRES formas (worktree vivo
  con doble --force por el caso locked; prune SIEMPRE — no gateado por
  exists(), que salteaba justo la cura del worktree-sin-directorio; rmtree
  del directorio que nunca fue worktree); **la URL impresa es 127.0.0.1 y
  NO localhost** (localhost puede resolver a ::1 primero y con un listener
  solo-::1 el navegador mostraría OTRO contenido creyendo mirar el
  artefacto — reproducido); y `--puerto` valida isdecimal + rango 1-65535
  (70000 moría con OverflowError crudo; 0 servía en un puerto efímero con
  URL inutilizable; «²» pasaba isdigit y reventaba el int). La preview
  además es una FOTO de la punta de main al abrirla — tras otro
  make-deploy se cierra y se relanza; está en el docstring y en el paso 4
  del README.
- **El mensaje del deploy lleva el TÍTULO del commit fuente (2026-08-14,
  propuesta de Code ACEPTADA por el autor — el cierre de su pregunta por
  los tags de rollback)**: la primera línea es «Publicar: <título del
  fuente>», y con eso `git log --oneline main` ES el menú de rollback
  legible — once deploys decían exactamente lo mismo y elegir un rollback
  era excavar hexadecimales. Lo que la respuesta descartó, con acuerdo
  explícito del autor («importaba ceremonia de contextos con equipo», sus
  palabras): el tag móvil «last-good» (todo deploy sale verificado, así
  que el puntero coincidiría SIEMPRE con la punta y no informa nada; y el
  día que un deploy resulte malo después, el last-good ya lo siguió — más
  el choque con «UN TAG NO SE MUEVE») y el tag por deploy (rutina, contra
  el criterio escrito). **Los tags de hito quedan como están.**
  VERIFICADO ANTES DE TOCAR, como pidió: el detector de hotfix y
  `verificar_main_intacta` NO dependen de la primera línea — leen SOLO la
  línea `Fuente:` (MARCA_FUENTE, regex anclado a comienzo de línea) y
  comparan ÁRBOLES regenerados. Probado en CLON AISLADO (T1-T5): subject
  con el título; un título raro (largo, kanji, comillas, %, y un
  «Fuente: <hash40>» ADENTRO) viaja entero SIN fabricar marca falsa — el
  prefijo «Publicar: » garantiza que nunca quede a comienzo de línea—;
  el hotfix a mano sigue frenando; el retrigger vacío sigue «intacta»; y
  una fuente sin título cae al formato viejo (degradación visible). El
  título viaja SIN truncar a propósito: recortarlo sería un truncado
  silencioso, y el largo lo disciplina el commit fuente. Los deploys
  viejos conservan su mensaje genérico — la historia no se reescribe, el
  menú se puebla hacia adelante.
- **Byte-idéntico por construcción — DESDE EL 2026-08-08, MÓDULO LA
  TRANSFORMACIÓN**: el deploy reusa los blobs del commit fuente para todo lo
  no transformable (plumbing, sin checkout, sin riesgo CRLF) y los
  `.html/.css/.js` publicables pasan por el stripper de comentarios — ver la
  decisión de la transformación, primera de la lista, que es también donde
  vive la regla «el servido no es el fuente». Lo que puede fallar ya no es
  solo la SELECCIÓN sino también la transformación, y las DOS tienen guarda
  dentro del deploy (identidad en dos clases + la guarda 4 de contenido). El
  día de publicar se agrega UNA corrida de `check-modes` contra el árbol de
  `main` servido en `:8000` (la única de navegador contra el artefacto real;
  navega la portada y /hajime/ — el resto lo cubre la guarda 4) y, tras el
  push, los 404 de las notas comprobados EN EL DOMINIO — la propiedad que
  motivó todo esto, verificada donde importa.

### Analytics: GoatCounter en modo PIXEL, en las CATORCE — IMPLEMENTADO

*(Desde el 2026-08-07 son QUINCE: toda página nueva entra con su pixel, y
el andamiaje de seguros lo lleva con `p=/hajime/yorozu/japan/seguros/`. El
registro de abajo describe la implementación original sobre 14.)*

**Decidido por el autor el 2026-08-06, contra la documentación primaria del
servicio (leída del repo arp242/goatcounter; goatcounter.com estaba caído ese
día — dato en sí mismo). IMPLEMENTADO EL MISMO DÍA**, con la cuenta
`realshinka` creada y las exclusiones configuradas por el autor ANTES del
primer push. El registro de la ejecución, primero; las reglas con las que se
hizo, después:

- **La forma final**: `<img src="https://realshinka.goatcounter.com/count?p=/ruta"
  alt="" width="1" height="1" loading="eager" class="gc-pixel">` antes de
  `</body>` en las 14. La clase (y no `style=` inline) conserva el «`style=`
  en lo publicado: 0» del inventario de seguridad; el `loading="eager"` es
  contrato, no default — un pixel lazy solo mediría si entra al viewport; el
  `alt=""` lo saca del árbol de accesibilidad (el criterio LibraryThing).
- **EL HALLAZGO DEL CAMINO: un absoluto SIN anclas extiende el documento.**
  La primera versión (`position:absolute` a secas) sumaba EXACTAMENTE 1px de
  scrollHeight en las 14 — el absoluto queda en su posición estática, después
  del footer, y ese píxel alarga la página. Lo cazó la medición contra línea
  base pre-pixel; anclado a `top:0;left:0` (bajo la nav) quedó idéntico. Quien
  toque `.gc-pixel` creyendo que las anclas sobran, lo reintroduce.
- **Verificado midiendo (2026-08-06)**: las 14 disparan exactamente UNA
  petición con su `p=` correcto — interceptada por red, no leída del HTML—,
  el endpoint responde 202 `image/gif`, y el layout quedó byte-idéntico a la
  línea base.
- **La no-contaminación de las guardas la confirmó EL PROPIO SERVIDOR**:
  `X-Goatcounter: ignored because "126.117.178.175" is in the IP ignore
  list`, y esa es la IP pública de esta máquina. **Caveat de dos partes**: la
  exclusión de navegador vive en el perfil y las guardas usan perfiles
  frescos — la de IP es el único escudo que las cubre—, y si el ISP rota la
  IP, caduca en silencio: re-verificar la lista al cambiar de conexión.

Las reglas con las que se ejecutó (cumplidas):

- **Pixel `<img>` puro en las catorce páginas, NO la variante mixta**
  (count.js en portada + pixel en subpáginas). Elegido por simplicidad: el
  reparto por canal del lanzamiento sale de los clics que reportan los
  propios posts de X y LinkedIn — no vale dos mecanismos por recuperar el
  referrer. Conserva «cero JS en las subpáginas»; rompe «cero terceros», a
  sabiendas.
- **Lo que el pixel NO mide, textual de su doc**: referrer y tamaño de
  pantalla (llenar `r=` requiere JS). **Las visitas únicas SÍ se conservan**:
  GoatCounter las computa del lado del servidor (sitio+UA+IP, ventana de 8 h,
  solo en memoria).
- **LO QUE SE MIDA ES UN PISO, NO UN CENSO**: el propio autor de GoatCounter
  estima **~⅓ de pageviews perdidas por adblockers** (bloquean
  goatcounter.com; el dominio custom NO lo evita — solo el self-hosting, que
  queda como opción para el PaaS). Vale igual para pixel y para JS. No
  «corregir» números contra otras fuentes creyendo que el pixel está roto.
- **Ejecución: commit propio, ANTES de la publicación a `main`** — toca las 14
  páginas y así las cuatro guardas lo validan antes de producción. El `<img>`
  va **FUERA de los bloques comparados de nav y footer** (lleva `p=/ruta`
  distinto por página: adentro rompería `check-ready`), antes de `</body>`,
  con `width="1" height="1"` y posición absoluta para no sumar layout.
- **Prerrequisito duro: ignorar-la-IP-propia configurado ANTES del primer
  push con pixel.** El pixel no tiene la exclusión de localhost que trae
  count.js: cada corrida de `check-modes` y cada sesión de desarrollo
  contaría como visita. **CUMPLIDO y verificado por header del servidor.**
- **La revisión de seguridad quedó actualizada** en el `.md` de
  infraestructura del autor (§3: de «0 cargas de terceros» a «1 por página»,
  fechado), y la CSP del PaaS necesita `img-src` con
  `realshinka.goatcounter.com` (su doc lo pide) — anotado allá y acá.
- **La retención quedó CONFIRMADA al crear la cuenta: 0 = nunca borrar** —
  cierra la duda que su doc dejaba abierta, y es lo que Cloudflare no ofrecía
  (30 días). El panel confirmó además Sessions activo (únicas server-side,
  funcionan con pixel) y descartó el custom domain (no evita adblockers, lo
  avisa el propio panel). El riesgo restante para la serie de meses es que es
  el servicio gratuito de una persona: lo desactivan el export CSV/API y la
  salida a self-hosted.

### NINGUNA CREDENCIAL ENTRA AL REPO. Nunca.

Ninguna clave, token ni secreto se commitea. **Ni siquiera en un commit que
después se borra**: git guarda el historial, así que un archivo commiteado y
después ignorado **sigue siendo accesible**. Agregarlo al `.gitignore` no lo
saca de la historia — sólo evita el próximo.

**Y este repo es PÚBLICO, o sea que «se commiteó» equivale a «se publicó».** No
hay ventana entre una cosa y la otra: en cuanto el push termina, el objeto está
servido por GitHub y puede haber sido clonado, indexado o barrido por un bot que
justamente busca eso.

**Dónde van**: en variables de entorno, o en un archivo **ignorado desde el
primer día** —antes de escribirle nada adentro—. El `.gitignore` ya trae los
patrones típicos (`.env`, `*.key`, `*.pem`, `secrets.*`, `credentials.*`,
`*.token`), probados en las dos direcciones. **Pero eso es una red, no el
mecanismo**: sólo ataja el descuido de nombre previsible, y una key pegada
dentro de un `.py` cualquiera pasa igual.

**El error típico tiene nombre y es «sólo para probar».** Se pega la key en el
código para ver si el endpoint responde, con la intención de sacarla antes de
commitear. Cuando el commit sale, ya es tarde: lo único que queda por hacer es
rotarla. Si hace falta probar, la variable de entorno funciona igual de rápido.

**Va a importar pronto**, y por eso está escrito antes de que exista el primer
archivo: el pipeline de datos necesita la key de **不動産情報ライブラリ**
(solicitada desde abril de 2024), la de **J-Quants**, y las que vengan.

**SI PASA IGUAL, EL ORDEN ES: ROTAR PRIMERO, LIMPIAR DESPUÉS.** Y conviene tener
claro por qué, porque el instinto es al revés. Reescribir la historia
—`filter-repo`, `force-push`— **no des-publica nada**: lo que ya estuvo arriba
pudo haber sido copiado, y GitHub conserva objetos alcanzables por forks y por
la API un tiempo. La única acción que revoca el acceso de verdad es **invalidar
la credencial en el proveedor**. La limpieza del historial es prolijidad
posterior, reescribe commits, y **se decide con el autor** — nunca de oficio.

**Estado verificado al 2026-08-04**: se auditó el historial completo —78 commits,
todas las ramas y el tag— y **no hay ni hubo nunca** credenciales, `.env`,
`.ttf`, `_ref/` ni ningún archivo sensible. Ese cero es el punto de partida: de
acá en más, cualquier hallazgo es nuevo y hay que tratarlo como incidente.

### Los seis nombres de las caras
`肇 Hajime` · `素顔 Sugao` · `渡世 Tosei` · `家紋 Kamon` · `鳥居 Torii` ·
`絆 Kizuna`. **Cerrados por el autor.** No se traducen, no se reinterpretan, no
se proponen alternativas. Su kanji, romaji, gloss, dominio y estado vienen del
archivo de referencia y se copian literalmente.

### `[hidden] { display: none !important; }`
Está al principio de `styles.css` y **no se borra**. Varias clases del sitio
fijan `display` (`.btn`, `.status`, `.cube__stage`, `.cube__toggle`), y una
clase le gana por especificidad a la regla `[hidden]` del navegador: el elemento
seguía visible pese a estar marcado como oculto. Rompió el toggle del cubo una
vez y el botón de entrada otra. Se arregla para toda la clase de bug, no caso
por caso.

**Rompería `hidden="until-found"`** si algún día se usa. Para excluirlo:
`[hidden]:not([hidden="until-found"]) { display: none !important; }`.

### Romaji: Inter en el cubo, Cormorant en el resto
**No es una inconsistencia, son medios distintos.** En la grilla y las páginas
es texto del DOM a ~1.05rem, plano y de frente: Cormorant funciona y es la voz
de marca. En el cubo es una textura horneada a ~12px de altura de mayúscula, con
relieve grabado y escorzo — ahí Cormorant se deshace (medido a tamaño real: el
romaji de las caras laterales era ilegible). Inter tiene asta uniforme y x-height
alta, que es lo que aguanta ese tamaño.

Además va **confinado al cubie inferior central**: las juntas caen a 1/3 y 2/3 y
ocultan ~21px de la textura. Un kanji grande absorbe el corte; el romaji no —
una junta le borraría un asta entera.

### Péndulo en rx; herencia de dirección sólo en ry
`rx` no gira libre: oscila (centro 18°, amplitud 20°). Con rx libre el cubo daba
vueltas completas y el romaji aparecía invertido — un kanji dado vuelta se lee
como forma, texto latino dado vuelta se lee como error.

La **fase avanza siempre** y la velocidad objetivo sigue una posición ideal, sin
ramas, clamps ni reinicios. Una versión anterior reseteaba la fase al llegar al
límite y el péndulo quedaba con media excursión: reiniciar el movimiento en un
punto es exactamente lo que hay que evitar.

**La herencia de dirección quedó sólo en `ry`.** En `rx` manda la fase del
péndulo; un signo heredado del último tiro pelearía contra la oscilación.

Consecuencia asumida: `鳥居` y `絆` (arriba y abajo) no se muestran solas en
reposo. Se llega por arrastre o por la grilla.

### Encuadre de cámara ANISOTRÓPICO — esto REEMPLAZA a la esfera envolvente

**Cambió el 2026-08-04, a pedido del autor.** La esfera completa (`√3·S`) pagaba
~8 % de distancia por la pose de vértice arriba, que **es inalcanzable**: el
cubo no tiene roll (`rotation.z` siempre 0, order `'YXZ'`), y como `ry` no
cambia la coordenada vertical, la altura máxima real es `√2·S` — arista arriba,
`rx≈45°`. Fórmula vigente, en `frameCamera()`:

```
d_vertical   = M · S · (√2/tan(halfV) + 1)
d_horizontal = M · √3·S / sin(halfH)
camera.z     = max(d_vertical, d_horizontal)
```

Sigue siendo una **garantía geométrica, no un ajuste empírico**, y cubre TODAS
las rotaciones alcanzables: péndulo, snap (`rx=±90`) y **arrastre manual sin
acotar**. El hallazgo que salió del cálculo: restringir al arco del péndulo
**no ganaba nada** — el máximo vertical está en `rx=45°` y el arco llega a 44°,
o sea que ya contiene el peor caso. Por eso **cambiar `PEND_AMP` no invalida el
encuadre**; lo único que lo invalida es **introducir roll**, y ese día vuelve
la esfera (`√3·S/sin(min(halfV,halfH))`). Está anotado en `frameCamera()`.

**«Con seno, no tangente» ya no es la regla entera**: la vertical va con
tangente A PROPÓSITO (acota un punto concreto — la arista más alta, a radio S
del eje, cuyo peor azimut la acerca S a la cámara: de ahí el «+1»), y la
horizontal sigue con seno (radio de revolución, `ry` libre). Quien "corrija" la
tangente a seno aleja la cámara sin ganar nada.

Verificado con barrido de 360 poses: cero recortes, margen mínimo **17 px**
exactamente en el peor caso teórico. Efecto en la portada: el cubo pasó de 442
a **483 px** de alto (71 % → 78 % del canvas). El aire restante (~137 px) es la
reserva para las poses de arista arriba, que el arrastre sí alcanza — no es
recortable por encuadre. Números y condiciones en `docs/mediciones/encuadre.md`.

**Manda la condición más exigente de las dos**: en apaisado la vertical, en uno
más alto que ancho la horizontal. Es la misma variable que queda sin medir en
móvil, donde el escenario cambia de proporción.

### Los números del cubo se leen del código, y se tabulan en UN solo lugar

Constantes de geometría, luces, material, colores y física **viven en
`assets/js/cube.js` y en el `:root` de `styles.css`**. Ésa es la única fuente de
verdad. El README los tabula en «El cubo: parámetros vigentes» para poder
consultarlos sin leer el fuente; **ningún otro documento los repite**, por la
misma razón por la que el `免責事項` completo vive en un solo lugar: dos copias de
un número derivan, y la copia vieja se lee como si fuera la actual.

Ya pasó. **`docs/v1-dark/README.md` daba `hemi 2.2 · key 1.8 · rim 0.4 · back
0.8` y fondo de sección `#020509`**, que son los valores del tag y no los de hoy
(`hemi 3.5 · key 2.9 · rim 0.65 · back 1.3` sobre `--c-surface-cube` = `#05111d`;
las intensidades subieron justamente al aclarar ese fondo). Ahora ese archivo
dice en su encabezado que es histórico. **Al leer un `.md` con números del cubo,
la pregunta es siempre de cuándo son.**

### El import map vive en `index.html` y no se hereda

`cube.js` importa `three` como especificador desnudo; quien lo resuelve es el
import map de `index.html`. **No se comparte entre documentos**: una página nueva
que monte el cubo necesita su propia copia, con la ruta relativa corregida a su
profundidad (`/ja/index.html` necesitaría `../assets/vendor/three.module.js`).
Hoy es la única página publicable con JavaScript — todas las demás no cargan
ningún script—, así que agregar una página **no** obliga a tocarlo salvo que esa
página quiera el cubo. Detalle completo en el README, sección «El import map».

### `snap` es el movimiento; `parked` es el estado en que queda

Seleccionar una cara **detiene el cubo indefinidamente**, y eso es deliberado:
`snapTo()` pone `parked = true`, y mientras esté puesto la velocidad objetivo de
los dos ejes es 0. **No vuelve a arrancar solo** cuando termina el `hold`. El
único que lo revive es un arrastre nuevo, que es la misma acción que deshace la
selección y repliega el folio — o sea que el cubo se mueve exactamente cuando no
hay una cara elegida, y se queda quieto cuando sí.

Consecuencias que ya se aprovechan: con el cubo `parked` el render bajo demanda
no redibuja **ningún** cuadro, así que un cubo detenido no consume GPU; y el
ángulo objetivo pasa por `nearest()`, que elige el equivalente a ±180° del actual
para que no desenrolle vueltas enteras yendo al mismo lado.

### El lazy-init difiere CREAR el contexto, no dibujarlo

Hay **dos `IntersectionObserver` sobre `#cube`** y se confunden fácil, porque
miran el mismo elemento y hacen cosas distintas: el de `main.js` decide **cuándo
existe** el contexto WebGL, el de `cube.js` sólo pausa el loop cuando la sección
sale de pantalla.

Lo que se difiere no es el costo de dibujar —la geometría es trivial— sino el de
**crear el segundo contexto**: memoria de GPU, compilación de shaders y armado
del pipeline. Ese costo se paga una sola vez y **no lo evitan ni el render bajo
demanda ni la pausa por visibilidad**, porque para pausar un contexto primero hay
que crearlo.

Va con **`rootMargin: '0px 0px -1px 0px'` — margen NEGATIVO abajo — y el signo
es la corrección de una premisa que resultó falsa.** Este archivo decía «la
sección arranca ~20px debajo del fold, con margen 0 no interseca en la carga» —
y ya no era cierto: el hero mide **exactamente** `100vh`, la sección del cubo
**toca el fold en la carga**, y para el observer dos rects que comparten el
borde **intersecan**. Medido en la tercera tanda del 2026-08-04: con margen
`0px` el canvas existía antes de scrollear — el lazy-init no difería nada y
nadie lo había notado, porque ninguna guarda miraba el estado pre-hidratación.
El `-1px` encoge el viewport observado lo justo para que tocar el borde no
cuente. **Si alguien "mejora" esto agregando un `rootMargin` positivo generoso,
desactiva la optimización entera sin que se note** — y ahora `check-modes` sí
lo nota, porque mide que el canvas NO exista antes del scroll.

**Y EL LAYOUT DEL MODO 3D NO ESPERA A LA HIDRATACIÓN — es otra decisión, y
protege las anclas.** `main.js` reserva en la carga el layout 3D completo
(`setView('3d')`: escenario vacío con su alto de CSS, toggle visible y cableado,
grilla recortada, ayuda de 3D). Sin la reserva, el escenario y el toggle
aparecían recién al resolver el import de Three.js e insertaban **~406px + 59px
de alto ARRIBA de `#about`/`#method`/`#footer` DESPUÉS de que el ancla
aterrizara** — los destinos de la nav quedaban corridos exactamente eso, y
`scroll-margin-top` no puede arreglar un destino que se mueve después del
aterrizaje. Lo diferido sigue siendo lo caro (crear el contexto WebGL); lo que
se adelanta es sólo la geometría de la página. Si la hidratación falla, el
`catch` revierte a la grilla y esconde el toggle. `check-modes` verifica que la
altura del documento sea estable al hidratar, midiendo ANTES y DESPUÉS — con
detección de verde vacío si la medición pre-hidratación llega tarde.

**Tres reglas que la reserva arrastra, cerradas al día siguiente de escribirla**
(auditoría instrumentada + análisis adversarial, mismo día):

- **La hidratación re-aplica el modo VIGENTE, no `'3d'` fijo.** El toggle está
  vivo desde la reserva, así que el usuario puede elegir la grilla mientras el
  import de Three.js resuelve — y el `setView('3d')` incondicional de la
  versión inicial le pisaba la elección. `stage.hidden` es el modo. Verificado
  con red a 40KB/s: la elección sobrevive al import.
- **`initCube` devolviendo null se trata como fallo (throw)**: con la reserva
  puesta, el `return` silencioso de antes dejaba el escenario visible y VACÍO
  para siempre, sin catch y sin reintento. Hoy es camino muerto (initCube o
  devuelve el cubo o lanza), pero la semántica de fallo tiene que ser segura
  por defecto.
- **El camino de fallo se EJECUTA en la guarda, no se lee**: `check-modes`
  fuerza la hidratación a fallar (cube.js bloqueado por CDP) y verifica el
  estado del fallback completo, y además lee la ayuda ANTES del scroll — el
  momento que un usuario ve primero, que ninguna otra comprobación cubría.
  Las dos probadas en rojo con `main.js` mutilado antes de confiar en su
  verde (sin el bloque del hint: 3 fallas; sin la reversión del catch: 4).

**EL FINGERPRINT DE UN `main.js` VIEJO EJECUTANDO** (para el diagnóstico
DOM-contra-red): `15edc84` hizo DOS cosas a la vez — agregó la escritura del
hint a `setView()` Y cambió el baseline del HTML al texto de grilla. Un
`main.js` anterior corriendo contra el HTML vigente da **cubo 3D funcional con
el hint de grilla congelado**, sin ningún error de consola: el síntoma exacto.
La prueba de un segundo, desde la pestaña afectada: **alternar Grid↔3D con el
toggle — si el texto de la ayuda no cambia, el módulo ejecutado es
pre-`15edc84`**. Y ojo con el instrumento: `fetch(..., {cache:'reload'})` mide
la RED, no el módulo EJECUTADO — un module script se evalúa una vez por
documento (module map), y la caché heurística de Chrome (sin `Cache-Control`,
el 10% del Last-Modified) puede servir el módulo viejo aun tras un F5, porque
desde 2017 el reload normal sólo revalida el documento principal. El que
delata al módulo ejecutado es
`performance.getEntriesByType('resource')` sobre main.js (`transferSize: 0` =
salió de caché) y `performance.timeOrigin` (¿la pestaña cargó antes del push?).

### Las anclas aterrizan con el layout ya estable — y cada destino tiene el suyo

Cerrado en la revisión de quince puntos (2026-08-04); **ACTUALIZADA el
2026-08-08 con la calibración POR SECCIÓN de las anclas de la portada**
(decisión del autor sobre capturas — deploy 7); **y el 2026-08-14 la flecha
del hero DEJÓ DE SER ENLACE** (decisión del autor — deploy 11; ver el
bullet de #cube):

- **La regla global `scroll-margin-top: calc(var(--nav-h) + 12px)`** (= 96px)
  sobre `section`, **`footer`** y `.cube__layout` SIGUE, y es la que rige en
  las subpáginas. El footer va listado aparte porque no es `<section>` y era
  el único destino de la nav sin margen. **La nav real mide 65.7px a 1440 y
  62.2 a 390 (re-medida 2026-08-08, tras el fondo opaco del deploy 5 — el
  «63px» anterior quedó viejo).**
- **Desde el 2026-08-08 las TRES secciones de la portada llevan margen
  PROPIO, derivado del padding** (la misma `var(--pad-top)` que usa el
  padding — una sola fuente, cero copias): el aire de #method (~191px de
  franja) y #about era el padding-top de la sección sumado al respiro.
  Ahora el rótulo aterriza a ~12px de la nav (16 en móvil), con las tres
  tarjetas de method enteras y «How we work» asomando a 1440×900.
- **#cube lleva margen NEGATIVO DELIBERADO (decisión del autor): el
  aterrizaje PASA el encabezado** — conmutador 3D/Grid arriba, cubo ENTERO
  debajo, «Six faces...» y su párrafo fuera de pantalla, arriba. Esto
  REEMPLAZA al «quien llega por primera vez necesita el contexto» que decía
  acá: el contexto queda scrolleando hacia arriba. La nav SIGUE apuntando a
  `/#cube` (no crear otra ancla — y NO re-apuntarla a `/#cube-view`: los dos
  anclas tienen margen distinto a propósito). **La flecha del hero DEJÓ DE
  SER ENLACE el 2026-08-14 (decisión del autor — deploy 11): es decorativa,
  aria-hidden, sin destino, visualmente idéntica.** El motivo, que es lo que
  hay que recordar antes de «reponerle» el href: el camino hacia abajo es
  SCROLLEAR, y el enlace PERJUDICABA a quien lo usaba — este aterrizaje
  calibrado deja el encabezado «Six faces...» fuera de pantalla, correcto
  para quien viene de la nav (ya sabe adónde va) pero le salteaba la
  explicación del cubo justo al lector que bajaba por primera vez. Con el
  enlace se fueron el aria-label «Scroll to the cube» (un decorativo no se
  anuncia como acción), el `:hover` dorado del CSS (color de acción sin
  destino) y la tabulabilidad; el destino no desaparece — «The Cube» sigue
  en la nav de todas las páginas. El margen suma un término por la ALTURA DE LA CABECERA DE
  TEXTO, que CSS no puede medir: ajuste lineal sobre alturas MEDIDAS, con
  `min(6vw, 87px)` capeando donde los clamps de fuente topan y base móvil
  más gorda (el reflow del texto es un serrucho de ±31px) — **el error va
  SIEMPRE al aire: verificado ejecutando en 25 anchos (320–2560), peor gap
  +6.3px, el toggle nunca bajo la nav**. El detalle vive en el comentario
  del CSS («Las anclas de la PORTADA»); si se toca la cabecera del cubo
  (texto, cuerpos, márgenes), re-medir ese término.
- **La estabilidad del destino quedó verificada ANTES de calibrar** (pedido
  del autor): cinco cargas frescas por ancla, dos viewports — dispersión
  0px, drift 0px, clic idéntico a carga, reduced-motion idéntico. Los
  píxeles de diferencia entre capturas de iPhone son la barra de URL del
  visual viewport, no la página.
- **«Back to the Cube» apunta a `/#cube-view`** (el ancla de `.cube__layout`),
  con su margen de 96px intacto — no se tocó. El footer aterriza CLAMPEADO
  por el fin del documento (el margen no influye; queda como red) con el
  correo visible.
- La condición que hace que todo esto funcione es la **reserva del layout 3D**
  (ver la decisión del lazy-init): sin altura estable, el destino se corre
  después del aterrizaje y ningún scroll-margin lo salva. Es también lo que
  la verificación de estabilidad del 2026-08-08 confirmó midiendo.

### Rótulos de vuelta según el ORIGEN — criterio cerrado

Las páginas que se abren **desde el cubo** vuelven al cubo; las que se abren
desde otro lado vuelven a donde se llega. Concretamente: las seis caras →
«Back to the Cube» (`/#cube-view`); las tres subpáginas de Hajime → «Back to
Hajime» (`/hajime/`); `/musubi/`, `/method/`, `/disclaimer/` y la 404 →
«Back to the start» (`/`). Antes había cuatro rótulos distintos apuntando a
cuatro lugares sin criterio común («Back to the method summary», «Back to
Kotodama Finance»…).

### El footer quedó en dos columnas — la «Platform» se fue

Enlazaba a The Cube y Method: dos de cinco secciones, las dos ya presentes en
la nav. Una selección arbitraria que duplica navegación no orienta. El footer
es marca + bajada, «Reach us» y «Follow» — y la bajada dice «Where economic
currents become visible», sin «Japan's»: el motor es global y Japón es el
primer nodo, no el tema (la misma corrección de la revisión que pasó por el
About, /sugao/ p3 y /kizuna/ p2).

### Las tres subpáginas de Hajime son ANDAMIAJE deliberado

`/hajime/taichi/` (macro), `/hajime/yorozu/` (sectorial), `/hajime/yugen/`
(transparencia). Estructura de cara —línea de función + lead + un párrafo—,
**ya redactadas (2026-08-05) con texto del autor, tal cual lo dictó**: «The
macro picture» / «Sector by sector» / «Public money», descriptions derivadas
del texto. **Los tres nombres en la prosa de `/hajime/` van en `<i
class="name">` SIN enlace, y LA PUERTA a las subpáginas son las TARJETAS
`.face-page__cards` debajo del párrafo (2026-08-07, decisión del autor)** —
esto REVIERTE los enlaces `a.name` del 2026-08-05: como enlaces dorados
dentro de la prosa se leían como énfasis, no como puertas, y el lector no
descubría las subpáginas. (El motivo de aquellos enlaces —«se destacaban sin
llevar a ninguna parte»— quedó disuelto: como `i.name` ya no se destacan, y
el destino está en las tarjetas de al lado.) Las tarjetas reusan `.face-card`
TAL CUAL —el vocabulario de las seis de la portada: las subcaras son caras un
nivel abajo—, SIN punto de estado (ese vocabulario es el «qué hay» de las
seis, y acá las tres están igual) y SIN descripción propia: el párrafo
explica, y el descriptor es la línea de función del DESTINO literal (su
`.face-page__gloss`) — la tarjeta y la página dicen lo mismo. Tres columnas
(219px por tarjeta, medido a 1440 y 1920), a una bajo 640px; `height: 100%`
en la tarjeta para que los pies de la fila queden parejos cuando los
descriptores parten distinto (hallazgo de la revisión adversarial, medido en
la ventana 641-730px: dispersión 19px → 0). Las reglas `a.name` se borraron
del CSS CON los elementos.

**El efecto secundario vale más que el cambio, señalado por el autor**: al
sacar los enlaces del párrafo, la excepción de marcado de /musubi/ dejó de
ser excepción. La convención queda uniforme — `.name` en prosa no enlaza en
ninguna página — y desaparece la nota que había que mantener explicando por
qué en un lado sí y en otro no. **Es una simplificación real, no cosmética:
una regla sin excepciones no necesita documentación defensiva.** (Sus
palabras, 2026-08-07 — el criterio vale para futuras decisiones de marcado:
si una regla necesita una nota que explique la excepción, la alternativa
que elimina la excepción compra además la eliminación de la nota.)

Dos compromisos del texto que NO son redacción libre, anotados en los HTML:

- **«This is not a watchdog» (Yūgen) es un COMPROMISO del autor**, no una
  negación de relleno: su `context.md` define esa cara como contemplativa,
  no watchdog. No se saca por parecer innecesario — fija el límite de lo que
  esa línea de trabajo hace.
- **El cierre de Taichi («the parts only mean something against the whole»)
  rima A PROPÓSITO con el subtítulo de /musubi/ («Nothing means anything
  alone»)**: el mismo principio bajando a una cara. Dos copias deliberadas
  sin guarda que las compare — si se redacta una, mirar la otra. Anotado en
  los dos lados, igual que las frases del cubo.

- **Los kanji se cerraron el 2026-08-05** — esto reemplaza el «sin kanji a
  propósito» que decía acá: **太一 Taichi · 万 Yorozu · 幽玄 Yūgen**, dictados
  por el autor desde la tabla del cubo de su `context.md` (entonces se creyó
  que el archivo no estaba en esta máquina y se copiaron literales de su
  mensaje — la misma regla de no inventar, con otra fuente; hoy el archivo
  está localizado — ver la decisión del andamiaje de seguros). En h1 y `<title>`/`og:title` con el patrón de
  las seis caras: kanji grande + romaji al lado, la línea de función debajo,
  sin gloss traducido. Entraron con regeneración de subset: **太/幽/玄 eran
  nuevos; 一 y 万 ya estaban** (一次資料, 百万円). Verificado contra cmap con
  猫 de control de ausencia; features y conservados intactos.
- **Los nombres en la prosa de /hajime/ quedaron en ROMAJI SOLO, y es
  decisión, no falta** (regía para los enlaces de entonces y sigue rigiendo
  para los `i.name` de hoy): dentro de la oración inglesa, el kanji junto al
  romaji sólo duplicaría el nombre de al lado — la prueba exacta del japonés
  ornamental. El kanji vive donde el nombre se presenta como título — el h1 y
  `<title>` de la subpágina y, desde el 2026-08-07, su tarjeta en /hajime/ —,
  igual que las seis caras: ninguna mención en prosa del sitio lleva kanji.
  Anotado junto a los nombres en /hajime/.
- **La guarda de castellano exime el texto que EMPIEZA con «TODO»** — se agregó
  en esta tanda, porque los placeholders son castellano deliberado (regla de
  este archivo) y la guarda los habría marcado: era una regla del proyecto
  peleando contra otra. La exención es angosta: castellano sin esa marca sigue
  siendo hallazgo.
- **En /musubi/ los nombres `.name` NO enlazan, y no hay que "emparejarlos"**
  — ahora son nueve, con dos razones que no hay que mezclar: los seis del
  marco no tienen página (enlazarlos prometería páginas que no existen), y
  los tres de Hajime del bloque 5 SÍ la tienen pero ahí se presentan como
  sistema conceptual, no como destinos. **Desde el 2026-08-07 esto dejó de
  ser excepción y es LA REGLA UNIFORME del sitio: `.name` en prosa no enlaza
  en NINGUNA página** — en /hajime/ la puerta son las tarjetas. Está anotado
  en el HTML de /musubi/, en el de /hajime/ y en el CSS (el bloque «LOS
  ENLACES a.name SE FUERON», junto a `.face-page__body .name`).

### La tanda tipográfica y de logos del 2026-08-05 — seis pedidos del autor

- **Escala global al 112.5% (18px de raíz)** — el cuerpo se veía chico. Todo
  el sitio mide en rem, así que es UNA perilla y la escala relativa se
  conserva. **Las columnas de prosa pasaron de px a rem** (45rem la
  subpágina, 47.5 el About, 55 el hero, 70 los marcos de método y footer):
  en px no acompañaban a la letra y agrandar la fuente no reducía el vacío
  lateral, que era el efecto buscado. OJO con el hero: su caja estaba en px
  por una razón medida (el corte por dos píxeles del titular) y en rem esa
  garantía escala CON el titular — está anotado en el CSS. El cubo y su
  `--maxw` NO se tocaron.
- **Títulos de las 13 subpáginas al DOBLE y CENTRADOS** (cabecera entera:
  eyebrow, título, gloss; el lead y el cuerpo siguen a la izquierda). La
  frase de la 404 subió acotada por ancho (verificado: una línea).
  **El romaji quedó EN EL PUNTO MEDIO (3.7rem a 1440), veredicto del autor
  sobre las capturas doble-contra-medio** — cierra la serie 3.4 → 4 → 3.7.
  El hallazgo del camino: **el «gigante» del primer pase era el eje, no el
  tamaño** — se había juzgado con alineación baseline, y con el ecuador la
  pareja equilibra. Ese centrado quedó CONFIRMADO con la misma decisión.
- **El romaji alinea al ECUADOR del kanji, no a su baseline**
  (`align-items: center` en `.face-page__title`): con baseline no
  compartían eje y la pareja se veía desproporcionada. line-height 1 en el
  kanji hace caja = em, así que centro de caja ≈ centro visual del glifo.
  Medido: diff de centros 0.0px en /hajime/, /sugao/ y /hajime/yugen/.
- **Los subtítulos (`.face-page__subtitle`) quedaron en 2.75rem (49.5px),
  NO al doble — la escala propuesta para reconstruir la jerarquía** tras el
  «h1 enorme y el resto plano» del autor. El doble (4rem=72px) se probó
  primero y quedaba MÁS GRANDE que el romaji del h1 (66.6): jerarquía
  invertida — probable causa de que «todo lo demás quedara plano»: dos
  gigantes y el resto uniforme. La escalera vigente a 1440:
  **129.6 (kanji) / 66.6 (romaji) / 49.5 (h2) / 30.6 (lead) / 27 (gloss) /
  18.4 (cuerpo)** — seis niveles. La línea de función subió de 1.15rem a
  esos 27px por lo mismo. De paso, a 49.5 los subtítulos de /musubi/
  vuelven a UNA línea; el `line-height: 1.15` + `text-wrap: balance` que
  destapó el doble QUEDAN (heredaban el 1.6 del body — interlineado de
  prosa en cuerpo de titular; protegen los anchos angostos). Los
  `.sources__group` de /method/ quedan COMO ESTÁN — **el autor los miró y
  lo confirmó**: taxonomía de lista densa, no subtítulos de sección.
- **LA CABECERA ESCALA CON EL VIEWPORT; el cuerpo no** (2026-08-05). La
  queja real del autor no era la columna angosta —77 CPL, ya medido— sino
  que la página «parece una versión móvil sin ajustar a PC», y la causa
  era que la cabecera medía LO MISMO a 1440 que a 2560. Además ya estaba
  centrada respecto de la página (columna centrada ⇒ mismo centro,
  medido): lo que faltaba no era centrarla sino que USE el ancho. Kanji
  `clamp(5rem, 9vw, 10rem)` — 9vw da EXACTAMENTE los 129.6px aprobados a
  1440, 172.8 a 1920, tope 180 desde 2000px—; romaji 4.625vw (66.6 a
  1440, 88.8 a 1920, tope 5.15rem ≈ 0.515 del kanji); gloss 1.875vw (27 →
  36). El cuerpo, el lead y los h2 NO escalan: viven en la columna. Costo
  asumido: entre ~1000 y 1440px la cabecera es algo menor que antes (9vw
  < el tope viejo) — escala con la página, que es el punto. La 404 no se
  tocó: su frase está acotada por el ancho de la columna (verificado: una
  línea).
- **«Read the full method →» al pie de la COLUMNA IZQUIERDA** — REVIERTE el
  centrado bajo las dos columnas; como hijo de `.method__how` no se estira
  al fondo de la columna de fuentes.
- **El aire tras los nombres `.name`** (entonces los enlaces de /hajime/,
  que el 2026-08-07 volvieron a `i.name` — la corrección sigue vigente
  porque vive en la clase): el espacio SIEMPRE estuvo
  (4,5px de avance, medido) — la cursiva de `.name` es OBLICUA SINTÉTICA
  (Inter no carga itálica) y la última letra pintaba sobre el espacio.
  Margen de 0.14em, no padding (el padding estiraba el subrayado del enlace
  de entonces). 7,6px
  después, medido. **La corrección del mismo día lo llevó a LA CLASE
  ENTERA** (`.face-page__body .name`, no sólo los enlaces): el culpable es la
  oblicua, que afecta igual a los nueve `i.name` de /musubi/ — medido
  antes: 5,02px ante palabra y **0,00px ante coma** («Okeanos,» y
  «Aeolus,», la letra inclinada apoyaba sobre la coma); después: 7,58 y
  2,56 (la corrección itálica clásica). **Las tres subcaras NO usan
  `.name`** — sus nombres van en prosa plana por la decisión del romaji
  solo—, así que ahí no había nada pegado; si algún día llevan el marcado,
  la regla ya las cubre.
- **Logos de las fuentes de la portada: NINGUNA fila lleva logo — esto
  REEMPLAZA el «sólo la FSA» del mismo día.** La FSA era la única con
  archivo oficial utilizable y estuvo puesta unas horas; el autor la quitó
  en la corrección siguiente: **cuatro filas sin logo y una con queda más
  raro que la columna pareja**. La investigación de los cinco NO se tiró —
  vive en `assets/img/README.md` (qué publica cada uno y por qué no sirve:
  BOJ sólo fondo opaco —limpiarlo = alterarlo, prohibido—, EDINET no tiene
  logo, bis.org rechaza conexiones, Damodaran sin marca; el PNG de la FSA
  queda en la historia, commit `ca96c72`) junto con el criterio de
  reposición: si alguna publica un archivo oficial utilizable, se repone
  con el criterio LibraryThing. **Que nadie lo "complete" con SVGs de
  Wikipedia**: no son el archivo oficial. La regla `.sources__logo` se
  borró con el `<img>` — una regla sin usar es legal y silenciosa, y este
  proyecto ya pagó ese costo dos veces.
- **El © del footer QUEDA** — aclarado por el autor: © es copyright del
  contenido (existe sin registro); marca registrada sería ®/™. Sin cambios.
- **El texto y el vacío a los costados — MEDIDO, no tocado** (pedido del
  autor en la corrección: separar «no me llegó el cambio» de «sigue
  angosto»). **La columna de 45rem mide 77 caracteres por línea completa**
  (primer párrafo largo de /musubi/, bisección con Range hasta el salto de
  renglón — el promedio por párrafo subestima: cuenta la última línea
  corta). 77 ya está en el TECHO del rango cómodo (45–75, ideal ~66):
  ensanchar a 50rem da ~83–85 y a 55rem ~96 — **no hay margen de ensanche;
  el vacío lateral a 1920/2560 es el costo de una medida legible, no una
  columna tacaña**. El fingerprint para diagnosticar copia vieja en
  consola, sobre cualquier subpágina: raíz y body `18px` y
  `.face-page` maxWidth `810px` (la copia vieja da `16px`/`720px`). Ojo:
  esos números describen el estado VIGENTE — si el veredicto cambia la
  escala, cambian con ella. **El fingerprint se corrió y dio 18px/810px:
  Manuel veía la versión vigente — copia vieja DESCARTADA para este
  caso** (la primera vez que el patrón DOM-contra-red se descarta
  midiendo en vez de confirmarse). **El centrado se re-midió a
  1440/1920/2560** (sospecha del autor tras el pase a rem): left = right
  EXACTOS en `.face-page`, `.hero__inner`, `.about__inner`,
  `.method__wrap` y `.footer__top` en los tres anchos.
- **Los dos pendientes del autor de esta tanda se CERRARON el 2026-08-06:**
  (1) la cabecera escalando con el viewport **FUNCIONÓ, confirmado por el
  autor** — el diagnóstico correcto era que la cabecera medía lo mismo a
  1440 que a 2560, no el centrado; (2) su calibración en vivo de los
  costados terminó con **el halo descartado y la marca de agua aprobada**
  — ver la decisión de los costados, que quedó reescrita con ese
  resultado.

### Los costados de las subpáginas: quedó SOLO la marca de agua — cerrada

**De las tres opciones propuestas se implementaron dos (A+B, 2026-08-05) y
la calibración en vivo del autor (2026-08-06) dejó UNA**: la marca de agua.
El detalle operativo y el registro de lo descartado viven en el comentario
de `.face-page__watermark` en `styles.css`. Las reglas que no hay que
romper:

- **A) La marca de agua es el kanji de LA PROPIA cara**, vertical, en el
  centro del vacío izquierdo — mismo vocabulario y MISMA opacidad (0.045)
  que `.about__watermark` de la portada. **Aprobada explícitamente por el
  autor, al valor default.** Sólo en las diez páginas con kanji propio.
  **/method/, /disclaimer/ y la 404 no llevan nada, y NO se sustituye con
  el logo 言霊**: es la marca del sitio, no el nombre de la página — que
  unas páginas sean caras del cubo y otras no es información real
  (criterio del autor). **Tampoco se duplica a la derecha**: el segundo
  kanji enfrentado se descartó — dos marcas iguales encaradas se leen
  como marco decorativo, no como marca, y sería el mismo relleno que
  falló con el halo.
- **B) La atmósfera lateral se IMPLEMENTÓ, SE PROBÓ Y SE DESCARTÓ
  (2026-08-06)** — dos radiales oro/bruma en `.page::before` con perilla
  `--halo-alpha`. El autor la probó de 0 a 0.5: **a 0.05 no aportaba nada
  (el costado seguía leyéndose como sobrante) y a valores visibles se
  veía como dos manchas radiales feas. No hay punto intermedio que
  sirva.** La regla y su token se borraron; si alguien propone «un
  degradado sutil en los costados», es esto y ya se vio.
- **La perilla que queda es TOKEN (`--wm-alpha`), no parámetro de URL, a
  propósito**: leer `?wm=` necesita JavaScript y las subpáginas no
  cargan ninguno (verificado: `document.scripts.length` = 0) — el mismo
  argumento que descartó el interruptor runtime de la transición.
  Calibración en vivo por consola:
  `document.documentElement.style.setProperty('--wm-alpha', '0.07')`.
- **La opción C (el mar en las subpáginas) se evaluó y se DESCARTÓ con el
  autor, sin implementar**: C1 vivo rompía la propiedad de cero JS en las
  subpáginas — «esa propiedad no se rompe por un fondo», sus palabras—;
  C2 estático eran ~100 KB contra la restricción explícita de peso, más
  un artefacto derivado con lock que mantener. Si alguien la propone de
  nuevo, ésa es la respuesta.
- **El hallazgo del camino: `white-space: nowrap` no es opcional.** Sin
  él, los nombres de DOS glifos partían en DOS columnas verticales
  (medido: ancho 647px ≈ 2 font-size, invadiendo la columna 46px, y
  leyéndose al revés): con `top: 50%` el alto disponible para la línea es
  media pantalla y en `vertical-rl` la línea rompe contra el ALTO. Es el
  mismo remedio que ya usaba la marca del About. La marca va con
  `z-index: -1` (el contenido del footer entra en la zona del vacío al
  scrollear y no debe recibir tinte) y se oculta bajo 1200px.

El frente que este cierre abrió —el CUERPO— se resolvió al día siguiente:
ver la sección que sigue.

### El cuerpo: la lista de /method/ al ancho, el justificado, y el análisis

**Cerrado el 2026-08-06.** El test del autor —¿se lee renglón a renglón (se
queda en la columna) o se escanea (puede salir)?— aplicado a las catorce
páginas, con su veredicto sobre el resultado. **La conclusión general, que
es lo más valioso del análisis: el sitio tenía UN SOLO elemento
estructurado preso en la columna de lectura — la lista de /method/.** Para
las páginas de prosa pura la respuesta al vacío ya está dada (la marca de
agua y la cabecera que escala), y **la columna angosta es el formato
correcto de una página de prosa, no un defecto a corregir.** Ya está
medido qué NO arregla el vacío: ensanchar la columna (77 CPL, techo del
rango) y rellenar los costados (el halo).

- **La lista de /method/ salió al ANCHO COMPLETO** (variante elegida por el
  autor sobre la maqueta, contra la alternativa de 70rem). El modificador
  `face-page__section--wide` en el HTML; las reglas y sus porqués en el
  comentario del CSS. El h2 y la prosa de la sección QUEDAN en la columna:
  el salto marca dónde termina el argumento y empieza la referencia.
  **`column-width: 26rem` y NO `columns: 3`** — el conteo se adapta:
  2/3/4 columnas a 1440/1920/2560, medido, con la página bajando de
  10.401px a 7.747/7.272/6.739. Sin overflow horizontal, la lista de cinco
  de la portada intacta (flex, una por fila), sin breakout bajo 1200px
  (ahí `100vw - 128px` sería MÁS angosto que la columna).
- **Los NO del análisis, con el acuerdo del autor**: la portada no tiene el
  problema (sus secciones ya viven en marcos de 70rem y el mar y el cubo
  usan el ancho); **los títulos de /musubi/ NO salen de la columna** — un
  título se escanea PARA ENTRAR a la prosa que encabeza, y hacia la
  izquierda invadiría el vacío donde vive 産霊, la marca de agua aprobada;
  /disclaimer/ y toda la prosa, renglón a renglón, se quedan.
- **Las tarjetas de /sugao/: candidata EN POTENCIA, no-op hoy.** Con una
  sola tarjeta de 232px no cambia ni un píxel. Cuando sean cinco
  (5×232 + separaciones ≈ 1.230px contra 682 de columna: partirían en dos
  filas), el desborde a 70rem las pone en una. Ése es el momento de
  implementarlo, no antes.
- **El cuerpo de prosa quedó JUSTIFICADO** (`.face-page__body p`), a pedido
  del autor y tras pasar su gate: sin ríos. La medición (2026-08-06, a
  1920 sobre /musubi/ y /sugao/): espacio normal 5px, mediana justificada
  6.2–6.9, máxima 12.3, **cero separaciones sobre 16px** — a 77 CPL hay
  palabras de sobra por línea. El lead y el gloss quedan afuera (texto de
  display: menos palabras por línea es donde el justificado se agujerea).
  **El criterio de aceptación fue el caso SIN partición de palabras** —
  ver el hallazgo de hyphens en los hallazgos de método y el comentario
  junto a la regla. Si la columna se angosta alguna vez, esto se re-mide.
- **El justificado ALCANZÓ AL ABOUT de la portada el 2026-08-06**
  (`.about__body p`) — el pase original lo había dejado afuera por OMISIÓN,
  no por decisión (verificado contra este registro antes de tocar: nada lo
  eximía), y el autor lo notó como «sobra espacio a la derecha». Mismo
  criterio: el cuerpo sí; `.about__statement`, los leads y las tarjetas y
  pasos de Method quedan afuera (display). Como la columna del About es MÁS
  angosta (36rem, ~61 CPL contra 77), **se re-midió antes de aceptar**, como
  exige la regla de arriba: mediana 6.1–8.7px, máxima 13.1, cero sobre 16px.
  Con esto la portada no tiene más prosa de cuerpo sin justificar.

### El favicon: 言 solo en las superficies CHICAS, 言霊 MACIZA en las GRANDES

**ACTUALIZACIÓN 2026-08-08, aprobada por el autor sobre renders — esto
MATIZA el «言 solo en todo» de abajo: ahora son DOS marcas por tamaño, UNA
por superficie.** El disparador: Google mostraba el globo genérico en los
resultados (diagnóstico: los archivos estaban sanos — ico 16/32/48 + svg +
apple-touch 180, todo 200, robots abierto; la causa probable era retraso de
rastreo) y el autor decidió que el favicon que ve Google lleve la marca
completa. Las reglas nuevas:

- **Las superficies CHICAS (la pestaña) siguen con 言 solo**: ico, svg,
  16/32 png — a 16px dos kanji son dos manchas; la decisión original sigue
  valiendo donde se tomó. Regeneradas byte-idénticas (verificado por git).
- **Las superficies GRANDES llevan 言霊 MACIZA, las CUATRO unificadas**
  (condición del autor: no dos marcas según el dispositivo):
  `favicon-192x192.png` (NUEVO, con `<link rel="icon" sizes="192x192">` en
  las dieciocho páginas, dentro del bloque de iconos comparado),
  `android-chrome-192x192.png` (mismo contenido que el nuevo, byte-idéntico
  por construcción: un solo render), `android-chrome-512x512.png` y
  `apple-touch-icon.png`. **Ninguna URL existente se movió** — los archivos
  se reemplazaron en su lugar (Google cachea favicons entre rastreos).
- **La variante MACIZA** (`dibujar_maciza` en make-favicon.py, variante E
  de la tira): 言 arriba y 霊 abajo, trazo engrosado ~2% del lado POR LADO
  (+~50% de grosor, dilatación en el supersampleo), separación al 5% del
  lado, y la marca al 100% del CÍRCULO INSCRITO con **encaje por TINTA**
  (tol 0.985) — Google y Android recortan en círculo. La primera apilada
  (gap 10%, 94% del círculo, sin engrosar) la rechazó el autor: «pierde
  por PRESENCIA — columna fina y rayada»; la maciza busca masa, no leer 霊
  a 16px. Límite conocido: apilados, el ancho útil es ~45% del lienzo
  contra ~76% del kanji solo — no lo mueve ninguna calibración.
- **El 192 publicado es PÍXEL-IDÉNTICO al de la hoja que aprobó** (delta 0
  medido contra el render de la parada). El supersampleo se capea a ~1536
  en los tamaños grandes (el x8 a 512 tardaba minutos en el MaxFilter sin
  mover el resultado — anotado en el docstring).

El registro original del 2026-08-06, que sigue valiendo para las chicas:

**2026-08-06, especificación del autor.** El diseño ya era ése (la variante A
del generador, elegida en su momento); lo que esta tanda agregó es el juego
completo y la verificación medida. Las reglas:

- **言 solo, no 言霊**: dos kanji a 16px son dos manchas; 言 es el núcleo del
  nombre y no se despega del logo. **Fondo navy SÓLIDO, no transparente**:
  transparente, el kanji dorado desaparece sobre la barra clara de un
  navegador en modo claro. Colores = tokens (copiados en el script, la
  excepción documentada de siempre).
- **Ocho archivos generados** por `tools/make-favicon.py`: ico (16/32/48 — el
  48 va de más respecto del pedido «16 y 32», es para el acceso directo de
  Windows), svg (glifo como path), 16/32 png sueltos sin `<link>`, apple-touch
  180, android-chrome 192/512 sin `<link>` (los enlaza `site.webmanifest`), y
  el manifest — **en INGLÉS: se sirve tal cual, superficie publicada**, con
  `display: "browser"` a propósito (sitio de contenido, no app).
- **El 16px lleva tratamiento propio MEDIDO** (perfil de luminancia por fila):
  relleno 0.86 + UnsharpMask + tope por canal al oro. Sin él, 4 picos y
  separación pico-valle de 23 unidades sRGB (el punto fundido con el primer
  trazo); con él, **6 picos / 5 valles / separación 81, y el píxel más claro
  es EXACTAMENTE el oro** — el tope existe porque el enfoque desbordaba a
  amarillo pálido (255,255,146), la misma regla que la tinta de la esfera.
  Verificado sobre los archivos ESCRITOS, incluido el 16 de adentro del ico.
- **El bloque de iconos entró a `check-structure`**: cuatro `<link>` (ico,
  svg, apple-touch, manifest) idénticos carácter por carácter en todas las
  páginas, dentro de la misma comprobación del nav y el footer. **Probada en
  rojo antes de confiar en su verde** (manifest faltante y orden alterado:
  las dos detectadas).
- cmap verificada por costumbre: 言 presente, 猫 de control ausente.

### CSP por meta: evaluada y NO va — que nadie la agregue por completitud

**2026-08-06, revisión de seguridad de la etapa estática** (el informe completo
vive en `kotodama_infraestructura.md` del autor, §3 — TLS verde por conducta,
barrido limpio: 80 `_blank` todos con noopener, 0 formularios, 0 cargas de
terceros, 0 sumideros de inyección en el JS — **el «0 terceros» describe el
estado PRE-pixel: desde el pixel de GoatCounter del mismo día hay UNA carga
de terceros por página, adoptada a sabiendas; ver la decisión de analytics**).
La decisión que pertenece a ESTE repo: **no se pone `<meta http-equiv="Content-Security-Policy">`**, y el motivo
importa más que la decisión:

- La superficie de inyección del sitio es CERO (sin input, sin params
  reflejados — los `?explodeR=` van por `URLSearchParams` a `parseFloat`), así
  que el aporte real de una CSP acá es ~nulo; lo único valioso que daría un
  header —anti-clickjacking— la meta NO lo puede: `frame-ancestors` se ignora
  en meta CSP, y GitHub Pages no permite headers.
- El costo sí es real: **el único script inline EJECUTABLE del sitio es el
  import map**, y `script-src` exigiría su hash sha256 — **que caduca con
  cada edición del import map y rompe el cubo EN SILENCIO para todo
  visitante**. Exactamente la clase de rotura invisible que este proyecto no
  acepta. **El JSON-LD de Organization (2026-08-10) NO cambia esta cuenta, y
  se verificó antes de anotarlo**: es un DATA BLOCK — tipo no ejecutable—,
  el navegador no lo ejecuta y `script-src` no lo alcanza (el algoritmo de
  «prepare a script» corta antes del chequeo de CSP), y Google lee el
  marcado crudo con o sin CSP. La premisa «suma un segundo hash» se verificó
  y NO se sostiene — que nadie agregue ese hash «por completitud» a la CSP
  del PaaS: sería mantener un hash que no protege nada.
- **La batería completa de headers va al pasar a PaaS** (CSP con Report-Only
  primero, frame-ancestors, HSTS, nosniff, Referrer-Policy, COOP) — está
  anotada allá, con el detalle. Si alguien propone «sumar seguridad» al HTML
  antes de eso, la respuesta es este bloque.

### Tarjetas de perfil en /sugao/ — completa: logo oficial sin alterar y texto

El registro de perfiles personales va en **tarjetas** desde ya, aunque haya una
sola (LibraryThing): un enlace suelto sirve para uno, no para los cinco que
vienen (IMDb, MyAnimeList, Steam, GitHub). **Fila que envuelve con ancho fijo
(232px), no grilla auto-fill**: la grilla estiraría la tarjeta única al ancho
completo como un banner. **Sin slots vacíos ni «próximamente»**. La tarjeta
entera es el enlace. El LinkedIn del perfil profesional NO se convierte en
tarjeta: es credencial de esa sección, no parte del registro.

**EL LOGO VA EN SU PALETA ORIGINAL, SIN ALTERAR — criterio fijado por el
autor (ago 2026), y REVIERTE el «monocromo en oro, silueta con
`fill=currentColor`» que decía acá.** El motivo del cambio: recolorear la
marca de otro es apropiársela; los logos de instituciones ajenas se muestran
como ellas los publican. El costo aceptado es que entren colores ajenos a la
paleta navy/oro, y **lo controla el TAMAÑO (26px, un sello, no una mancha),
no el recoloreo**. Aplica también a los cuatro que vienen. Quien encuentre la
instrucción del oro en el historial: la vigente es ésta, no hay que
"corregirla" de vuelta.

**Y el cambio de criterio DISUELVE el pendiente de permiso de marca**: los
términos siguen ilegibles por vía automatizada (403 en /press y /topic/45089),
pero usar el archivo oficial tal cual se distribuye es exactamente lo que
cualquier guía de marca permite — eso es lo que hace el uso defendible sin
haberlos leído, y está anotado en `assets/img/README.md`, al lado del archivo.

Lo puesto, verificado midiendo (2026-08-05): `flat-logo-rounded_1024w.png`
oficial, byte-idéntico al original (sha256 comprobado), en
`assets/img/librarything-flat-logo-rounded_1024w.png`. **El SVG oficial NO
sirve** — dibuja la L como `<text>` con una tipografía que el visitante no
tiene (análisis del autor, anotado en el README de img). Esquinas del PNG ya
transparentes (alfa 0, medido); sobre la tarjeta: anillo exterior sin halo
(delta de luminancia 0.0 contra el fondo), esquinas a +1,9 unidades (el
antialias del redondeo — bajo el umbral de 3 unidades sRGB que este proyecto
ya fijó como invisible), centro exacto `#553B39`, nítido a @2x (1024px de
origen para 52px de dispositivo). El `alt` va **vacío a propósito**: el
nombre «LibraryThing» está al lado y un lector de pantalla lo diría dos veces.

**El texto de la tarjeta es del autor y va tal cual: «My Library at Home»**,
con esas mayúsculas. No se ajustó al patrón en minúscula de los descriptores
de las seis tarjetas del cubo porque ése es otro sistema (dominios comprimidos
que se leen entre seis); `.profile-card__what` no tiene hermanos todavía, y en
mayúsculas se lee como el nombre propio de la colección — el registro justo
para esta tarjeta. Con esto **/sugao/ quedó en cero placeholders** y el
baseline bajó a 15.

### `素顔 Sugao` es la persona entera, en su propia página — no una sección de la portada
Sugao es **la persona detrás del proyecto, completa**: perfil profesional y
perfil personal. **Se publica ya**, en `/sugao/` y sólo ahí.

**Sin introducción**: la página arranca directo en el perfil profesional, que es
lo que contesta la pregunta que trae el lector. Una apertura genérica antes de
eso sólo demora la respuesta.

**Dónde NO va.** Hubo una sección `#operator` en la **portada** con nombre, rol,
trayectoria y `免責事項`, al modo de un `運営者情報`. Se eliminó entera y **no se
reintroduce**: la portada no lleva nada de esto. Quien quiera saber quién está
detrás entra a la cara, que para eso está en el cubo.

Decisiones dentro de la página:
- **Sin foto, y sin hueco reservado para una.** La credibilidad la carga el
  enlace a **LinkedIn**, que es verificable; un retrato no aporta nada
  comprobable y hay que mantenerlo.
- **El perfil profesional va en PROSA, no en formato CV.** Una lista de puestos y
  fechas se lee como currículum y no contesta la pregunta que trae el lector, que
  es qué habilita a esta persona a publicar esto.
- **Sin slots vacíos** para los perfiles que todavía no entran (IMDb,
  MyAnimeList, Steam, GitHub). Un hueco reservado para algo que no está se lee
  como página incompleta. Cuando existan, se agregan a `.profile-links`.
- **El `免責事項` NO va en `/sugao/`.** Ver la regla de abajo.

**EL ARCHIVO DE REFERENCIA QUEDÓ ATRÁS EN LOS TRES CAMPOS.** Ya no queda nada de
Sugao que se copie literal de ahí:

| Campo | Referencia | Vigente |
|---|---|---|
| `gloss` | «the true face» | **«The person behind the platform»** |
| `status` | «Intro live · profiles deferred» | **«Live»** (`active`) |
| `domain` | «The human behind» | **«The person behind»** |

O sea que para esta cara **la regla de copiar literal del archivo de referencia
ya no aplica**: manda lo redactado. Vale la pena tenerlo presente antes de
"restaurar" un campo desde la referencia creyendo que se corrige una deriva —
y lo mismo vale para las otras cinco, ver la tabla de `domain` más abajo.

### La rama `maintenance` existe, está lista y NO está activa

**ACTUALIZACIÓN 2026-08-08 — TAMBIÉN SIRVE SIN COMENTARIOS.** La regla del
deploy 8 se extendió a esta rama en su tanda aparte, el mismo día: era la
rama que se activa justo cuando algo se rompió, o sea el peor momento para
descubrir que sirve notas de trabajo en castellano. El generador pasa el
HTML por **EL MISMO `transformar()` de make-deploy.py** (importado por
ruta; una implementación, no dos que derivan — criterio del autor), los
comentarios siguen viviendo en la PLANTILLA del script —el fuente— y la
procedencia («no editar a mano») queda donde siempre estuvo: el mensaje
del commit de la rama. El stripping va en `construir()` y no en
`publicar()` a propósito: `_dev/maintenance/` y la rama son el mismo
texto, que es lo que check-maintenance compara (base64 elididos).
`check-maintenance` suma DOS comprobaciones, probadas EN ROJO con una
rama rota al lado: cero `<!--` en el HTML, y cero `/*` en el CSS inline —
aparte, porque el stripper deja el contenido de `<style>` crudo a
propósito (raw text) y un comentario agregado ahí sobreviviría. La rama
quedó regenerada (`1b80019`, con su historia) y verificada sobre el HTML
RESULTANTE de la rama, no sobre la intención: cero comentarios, CNAME
idéntico al del sitio, mailto único, sin scripts ni formularios, los dos
HTML el mismo blob, fuentes cubiertas.

Un cartel para bajar el sitio a propósito durante una obra grande. **Rama
aparte**, huérfana, con cuatro archivos: `index.html`, `404.html` idéntico,
`CNAME` y `.nojekyll`. Se activa **cambiando la rama que publica GitHub Pages**
y se revierte igual — el sitio y `main` no se tocan en ningún momento. El
procedimiento completo está en el README.

**Que exista es justamente lo que hay que recordar**: no se ve desde `main` ni
desde `redesign-trust`, no aparece en el árbol de trabajo, y ninguna de las
cuatro guardas la mira. Un cartel de mantenimiento que nadie recuerda que existe
se reescribe desde cero el día que hace falta, que es el peor día para hacerlo.

**Tres cosas que parecen detalles y no lo son:**

- **La rama lleva `CNAME`, y por eso son cuatro archivos y no dos.** Cuando
  Pages publica una rama sin `CNAME`, **da de baja el dominio propio**, y
  reponerlo obliga a reaprovisionar el certificado HTTPS. Eso pasaría con el
  sitio ya caído. El `.nojekyll` es por lo mismo: que Pages suba archivos en vez
  de correr un build que no hace falta y puede fallar.
- **Los dos HTML son el MISMO blob.** La raíz sirve el cartel y cualquier otra
  ruta cae en el 404, que dice lo mismo; no hay que replicar las carpetas del
  sitio. Si se separan, la portada dice una cosa y el resto otra.
- **La rama se GENERA con `tools/make-maintenance.py`, no se edita.** El script
  escribe la rama con plumbing —sin checkout, sin mover `HEAD`—, así que corre
  con el árbol en cualquier estado. Ésa es la respuesta a «copiar el woff2 queda
  viejo / mantener uno propio duplica el trabajo»: **un artefacto derivado no se
  mantiene, se regenera**, igual que el sitemap, la og-image y los favicons.

**ZEN KAKU VA EMBEBIDO** — micro-subset de 1,46 KB con los siete glifos, dentro
del HTML. Verificado: los cinco del titular y los dos del logo se dibujan con
Zen Kaku Gothic New Medium, una sola cara. Se embebe porque **ésta es la página
que se muestra cuando algo salió mal**, y ahí que se vea distinta en cada máquina
es lo peor que puede pasar.

**守, 作 y 中 viven en el subset del SITIO aunque ninguna página los use**, y eso
no se poda: el generador de la rama sólo puede leer archivos del repo, así que si
leyera la TTF de origen —no versionada, a propósito— la rama dejaría de poder
regenerarse en otra máquina. Cuestan 0,3 KB. Es el mismo trato que 立方体 y
一次資料, reservados para /ja/, y la fórmula de derivación los preserva sola.
Está anotado en el `@font-face` de `styles.css`.

**EL HALLAZGO SIGUE VALIENDO AUNQUE EL PROBLEMA ESTÉ RESUELTO, y es lo que hay
que recordar: copiar el subset del sitio a la rama NO habría dado tofu.** Al
subset le faltaban tres de los cinco glifos del titular, pero el fallback de
fuentes es **por glifo**, así que el titular se dibuja entero y se ve bien.
Medido con `CSS.getPlatformFontsForNode`: `'Zen Kaku', sans-serif` daba
**2 glifos Zen Kaku + 3 Microsoft YaHei** — un titular en dos tipografías, una de
ellas **china**, que pasa cualquier inspección visual. Y `lang="ja"` **no es
decoración semántica**: con él el genérico cae en Noto Sans JP, sin él en
Microsoft YaHei; sigue puesto como red por si el `@font-face` no cargara.

`JA_EMBEBIDO` en el generador **no adivina**: si falta un glifo aborta
nombrándolo, precisamente porque la versión rota se ve bien.

**La guarda propia es `tools/check-maintenance.py`, y corre A DEMANDA** — al
tocar la rama y **antes de activarla**, no en cada commit. Las cuatro guardas
siguen siendo cuatro: ésta mira una rama que no cambia entre commits, así que
en el flujo de siempre sería ruido. Probada en las dos direcciones, con cuatro
ramas rotas armadas al lado.

### La vista explotada del cubo — INTEGRADA; la historia de sus decisiones

**Se desarrolló en la rama `cube-exploded`** (creada el 2026-08-05 desde
`6de21bd`, por instrucción del autor) **y se INTEGRÓ acá el 2026-08-05, por
su decisión explícita**, con dos verificaciones previas: la medición emulada
de móvil (`docs/mediciones/explotada-movil-emulada.md`) y la no-divergencia
(merge-base = punta de `redesign-trust`: fast-forward). **La rama se borró
después del merge** — sin historia propia tras el fast-forward, un puntero
viejo sólo invita a creer que hay trabajo pendiente ahí.

**Las condiciones bajo las que se trabajó** (cumplidas, quedan como registro
del método): `redesign-trust` intacta con las correcciones del sitio yendo
ahí y la rama rebaseándose encima — nunca al revés—; el merge como decisión
explícita de Manuel, no por estar «casi»; y las guardas corriendo igual en
la rama — `check-pendulum` verde en cada tanda.

**Qué es (primera versión, SIN corrientes de agua — van después si ésta
funciona; no se compensa la ausencia con otro efecto):** el cubo se abre a un
caparazón esférico —los 26 cubies viajan a un RADIO COMÚN, no en línea recta:
en línea recta el resultado es un cubo grande y hueco, porque las esquinas
siguen más lejos que los centros— con el núcleo en el centro: esfera de vidrio
dorada (transmission REAL: el vendor es **r160**, no el r128 que circulaba en
papeles — leído de REVISION en three.module.js). Clic en el núcleo →
/musubi/, único clicable explotado.
El control es el pie del cubo: «Explode the Cube» ↔ «Reassemble the Cube»
reemplaza al enlace «The idea underneath the cube →» en modo 3D (decisión del
autor). **Los dos accesos CONVIVEN, y no es un resto**: el `<a>` queda en el
HTML y es lo que se ve en modo grilla, en el fallback si la hidratación falla
y sin JS — o sea, el único camino a /musubi/ DESDE LA SECCIÓN DEL CUBO cuando
no hay WebGL (la nav y el clic en el núcleo son los otros dos, cada uno en su
capa). main.js sólo alterna cuál de los dos se ve (`setMore`). *(Corregido
2026-08-07: este registro decía «behind» — el texto real del sitio es
«underneath» — y describía el reemplazo sin decir que el enlace sigue siendo
la capa sin cubo.)* Explotar limpia la selección y cierra el folio; las caras dejan
de ser clicables; pasar a grilla rearma al instante; reduced-motion salta al
estado final sin transición y sin pulso (verificado midiendo, no leyendo).

**Correcciones del autor sobre la v1 (2026-08-05):**

- **Los kanji van EN LA SUPERFICIE de la esfera, no como sprites orbitando** —
  revierte la elección de la v1. La objeción que motivó los sprites (una
  textura clavada a la esfera se va de vista media órbita con el péndulo) se
  resuelve de otro modo: el péndulo no gira el núcleo; quien gira es el
  CASCARÓN de palabras, sobre su propio eje, lento (~35 s/vuelta) e
  independiente — las palabras desfilan y se leen todas, por turnos.
- **Explotado se esconden la ayuda y el toggle — visualmente**: la ayuda con
  `visibility` (conserva su caja: nada se mueve bajo el cursor), el toggle
  con `opacity`+`pointer-events` para que SIGA en el árbol de accesibilidad
  y reaparezca con `:focus-within` — la salida de teclado queda.

**Segunda tanda (2026-08-05, tras la calibración en vivo del autor) — REVIERTE
tres puntos de la primera; lo vigente es esto:**

- **Radios fijados: `EXPLODE_R` 5.0 y `CORE_R` 0.5** (antes 4.2/0.72).
  Caparazón bien abierto y núcleo chico es el punto donde se lee como plasma
  globe: a 5.0 las caras se agrupan menos que a 4.2, y el autor prefiere
  errar del lado del globo. `?explodeR=` y `?coreR=` siguen para recalibrar.
- **El material y el pulso VOLVIERON a la v1, tal cual** (emisiva 0.16→0.26,
  ±1.5% de escala). El boost de la primera tanda (0.10→0.55, ±3%) se probó,
  se MIDIÓ —el vaivén pasó de 34 a 73,9 unidades sRGB, senoidal limpio— y el
  autor lo DESCARTÓ por costo visual: con la emisiva alta la esfera dejaba
  de leerse como vidrio. **QUE EL PULSO NO SE PERCIBA ESTÁ BIEN**: el vidrio
  vale más que el pulso, y no se compensa por otra vía (ni escala, ni color,
  ni keyframes). Que nadie lo "arregle" de vuelta.
- **La tinta de los kanji dejó el navy** — daba contraste pero ensuciaba la
  esfera y rompía el sistema de color; el contraste tiene que salir del
  TEXTO. En esta tanda se fue al bronce oscuro (`#6b4906`, delta 39,9), y
  **la TERCERA tanda lo REVIRTIÓ**: fue interpretación equivocada de
  «dorado duro» — ver abajo, donde está la dirección vigente.
- **Los kanji, proporcionalmente MÁS chicos**: el factor de la textura bajó
  de 0.24 a 0.19, ADEMÁS del arrastre del núcleo (0.72→0.5 ya los achicaba
  solo).

**Tercera tanda (2026-08-05) — el modelo de expansión y el sentido de la
tinta:**

- **El RADIO COMÚN puro se quedó corto y el modelo pasó a ser INTERPOLADO.**
  La instrucción original del autor pedía radio común, y él mismo la
  corrigió al verla a 5.0: los centros de cara, que parten más cerca del
  centro, viajan DE MÁS y sobresalen del globo (a 2.6-4.2 no saltaba).
  `EXPLODE_MIX` (`?explodeMix=`, 0 radial - 1 común) mezcla los dos
  extremos, **normalizado por la ESQUINA**: a cualquier mix las esquinas
  terminan en `EXPLODE_R` y el factor sólo decide cuánto se meten centros y
  aristas — calibrar no cambia la silueta. **Default 0.65, del barrido
  capturado**: a 0.5 todavía se lee grilla cúbica, a 0.8 el centro superior
  ya se despega del arco.
- **La tinta es ORO LUMINOSO: más clara y más saturada que la esfera, no
  más oscura.** «Dorado más duro» significaba un oro que RESALTE brillando,
  no hundiéndose — la serie bronce (deltas −20,7/−30,0/−39,9) se midió y se
  descartó entera. Serie luminosa medida con el mismo método de máscara de
  diff: `#ffd24a` +14,2 (el más saturado y más oro) · `#fae59a` +21,9 ·
  `#fdf3cf` +27,2 (roza el techo: se lee blanco). El default fue `#fae59a`
  y **la cuarta tanda lo movió a `#ffd24a`**: el autor vio la E demasiado
  blanca. **El techo es regla**: si el trazo llega a blanco deja de ser
  dorado. Los deltas luminosos son más chicos que los del bronce porque el
  tone mapping comprime arriba — y aun así se leen mejor: en polaridad
  positiva el trazo brilla.

**Cuarta tanda (2026-08-05) — la medición de la silueta, y tres ajustes:**

- **La medición que pidió el autor, con veredicto.** (a) **No hay bug**:
  las posiciones de los 26 coinciden con la fórmula con error 0, en mix
  0.2/0.65/1.0. (b) La hipótesis óptica se confirma con un matiz: los
  centros NO proyectan más silueta que el resto (tamaño proyectado 70-95 px
  en las tres clases) — sobresalen **LOCALMENTE**: en la pose de carga el
  centro superior queda **+31 px por encima del arco de sus vecinos
  angulares**. Y el mix nunca pudo arreglarlo porque ese eje mueve centros
  y aristas JUNTOS: el exceso relativo casi no cambia — era el eje
  equivocado, como sospechó el autor. (c) **ACERCAR sólo los centros
  funciona; ACHICAR no**: a 0.85·R el peor exceso local queda en −5,6 px y
  el contorno de píxeles no muestra bulto en poses adversarias; achicados
  al 78% el exceso sigue en +25 px — lo domina la distancia del centro, no
  el tamaño del cubie. Y un aviso de método: la métrica de ventana angular
  (±30°) dio un +47 FALSO en una pose, midiendo contra un hueco sin
  vecinos de anillo — **el árbitro es el contorno de PÍXELES** (ahí: meseta
  de 231 px contra arcos de 240-250, sin bulto).
- **PROPUESTA que la quinta tanda APROBÓ E IMPLEMENTÓ** (ver abajo): los
  20 del anillo (esquinas y aristas) al radio pleno, los 6 centros a
  ~0.85·EXPLODE_R con parámetro de URL — y EXPLODE_MIX retirado, porque
  quedó medido que ese eje no arregla el bulto.
- **El giro de los kanji se INVIRTIÓ** (desfile derecha→izquierda: signo
  negativo en WORD_SPIN) y la velocidad quedó calibrable EN VIVO con
  `?wordSpin=` (segundos por vuelta), **default 18** — el ~35 s original
  era demasiado lento para el autor. Verificado midiendo: centroide de la
  tinta −50 px en 2,5 s, glifos sin espejar. La legibilidad en movimiento
  la juzga el autor en vivo, no una captura.
- **La tinta quedó en D `#ffd24a`** — la E resultó demasiado blanca.
  **ORO SOBRE CONTRASTE**, criterio del autor: D es la que se lee como oro
  puro, y +14,2 de delta alcanza porque en polaridad positiva el trazo
  brilla sobre la esfera.

**Quinta tanda (2026-08-05) — la propuesta aprobada, y los valores del
autor:**

- **El modelo de silueta quedó IMPLEMENTADO** (aprobación explícita del
  autor): anillo —esquinas y aristas— al radio pleno, los 6 centros de
  cara a `CENTER_F`·R (`?centerF=`, default **0.85**, el valor medido).
  **`EXPLODE_MIX` SE RETIRÓ**, con la anotación en cube.js para que nadie
  lo reponga creyendo que falta: interpolaba radial↔común para los 26 a la
  vez y quedó medido que no arregla el bulto — una perilla que no hacía lo
  que prometía. Y la aparente contradicción, cerrada por el autor: el
  modelo vigente parte del extremo mix=1 (radio común) y corrige sólo los
  centros — retirar la perilla no contradice haber elegido ese extremo
  como base.
- **Valores elegidos EN VIVO con el modelo nuevo**: `EXPLODE_R` **5.5** y
  `CORE_R` **0.7** — reemplazan 5.0/0.5, que se habían elegido con el
  radio común puro. Caparazón un poco más abierto, núcleo algo más grande.
- **`wordSpin` default 24 s** — probado en vivo contra 18 y 12: a 24 el
  desfile deja leer sin apurar.
- **La tinta D `#ffd24a`, CONFIRMADA** en vivo: se lee como oro, no como
  blanco. Sin cambios.

### El `免責事項`: el corto se repite, el completo vive una sola vez

Son **dos textos con dos reglas opuestas**, y confundirlas es lo que hay que
evitar:

- **El corto** —una línea: esto no es asesoramiento de inversión ni financiero—
  va en el **footer global**, o sea que **se repite en todas las páginas**. Esa
  repetición no es deriva: es su función. Una advertencia sólo sirve si está
  donde el lector está leyendo, no en una página a la que haya que llegar.
- **El completo** vive **UNA sola vez, en `/disclaimer/`**, y todo lo demás lo
  **enlaza**. Nunca se duplica. Dos copias de un texto legal derivan, y cuando
  derivan el sitio se contradice a sí mismo justo en lo único donde no puede
  permitírselo.

La prueba para saber cuál se está por escribir: si son más de una línea, va en
`/disclaimer/` y desde donde estabas se pone un enlace.

**`/disclaimer/` SE PUBLICA SIN REVISIÓN DE UN PROFESIONAL LEGAL JAPONÉS, POR
DECISIÓN DE MANUEL.** Esto **revierte** lo que decía este archivo antes, que
pedía revisión de un benrishi o abogado antes de publicar a `main`.

**Fue decisión, no olvido**, y conviene que quede así de explícito porque el
rastro invita a pensar lo contrario: hubo una marca `BORRADOR-SIN-REVISION-LEGAL`
en el HTML y una comprobación en `check-ready.py` que bloqueaban la publicación,
y **las dos se retiraron a propósito**. Quien las encuentre en el historial y
crea que se perdieron algo, no: se sacaron cuando la espera terminó.

**Lo que sostiene la decisión es el marco legal que verificó Manuel** —no una
evaluación mía, que no estoy en posición de hacer—:

- **La FIEA no aplica**: el sitio no da asesoría de inversión bajo contrato ni
  emite recomendaciones. Es la línea que separa publicar análisis de operar como
  asesor registrado, y el proyecto se mantiene del lado de publicar.
- **El 景表法** (representaciones engañosas) **queda cubierto por el principio de
  rigor de fuentes**: toda cifra sale de fuente primaria y es trazable al
  documento. Ahí el rigor no es sólo método editorial, también es la defensa.

Las dos cláusulas donde un texto sin revisar puede no sostener lo que promete
—ley aplicable y limitación de responsabilidad— siguen declaradas y siguen sin
validar por un tercero. **Eso se asumió con la decisión.** Si alguna vez cambia
el alcance del sitio —asesoría, recomendaciones, cualquier cosa bajo contrato—
esta decisión hay que reabrirla, porque el marco que la sostiene deja de aplicar.

Y una cláusula tiene fecha de vencimiento propia: **«Language»** dice hoy que
prevalece el inglés hasta que se designe otra versión como autoritativa. Cuando
exista `/ja/` hay que revisarla, porque la prevalencia puede invertirse.

**Para la plantilla futura de notas financieras** (no existe todavía, no hay nada
que construir hoy): cada nota tiene que llevar **el corto al pie**, igual que
cualquier otra página. No el completo.

### `href="#"` es andamiaje, y hay guarda para que no sobreviva
**Hoy no queda ninguno**: el de LinkedIn en `/sugao/`, que era el único, lo
completó el autor con la URL real. La guarda queda igual, para el próximo.

Mientras un ancla lleve adentro su placeholder, es andamiaje declarado y
`check-ready` ya impide publicar. Lo que `check-structure` ataja es el caso
**silencioso**: que alguien redacte el rótulo, borre el `TODO` y se olvide de
pegar la URL — ahí el placeholder desaparece, todo se pone verde y el enlace
queda muerto. La guarda falla **exactamente** en ese momento y no antes.

### No templetizar: verificar
El nav y el footer están **duplicados** en todas las páginas. No hay build step
que los comparta, y las alternativas eran peores (inyectar por JS rompe la regla
de contenido en el HTML; Jekyll sería un build step y choca con `.nojekyll`).
La duplicación es aceptable **si está vigilada**: `check-ready.py` verifica que
los bloques sean idénticos carácter por carácter. Por eso el nav usa rutas
absolutas.

### El bloque de estado + botón es un folio que se despliega
**Esto REVIERTE una decisión anterior.** Antes el bloque de entrada reservaba
su altura desde el inicio con `min-height`, para que aparecer el estado y el
botón al seleccionar una cara no empujara el layout. Ahora el folio arranca con
**altura cero** y se **despliega animado** al seleccionar; se repliega al
arrastrar (deseleccionar).

Por qué se pudo revertir sin traer de vuelta el salto de layout: el folio está
**debajo** del cubo y de la grilla. Lo que se desplaza al abrirlo es el enlace
a Musubi y lo que sigue —nunca el cubo ni la cara que el usuario
acaba de tocar—, así que **nada se mueve bajo el cursor**. Reservar el espacio
dejaba un hueco vacío permanente para algo que la mayor parte del tiempo no
está; el folio sólo ocupa lugar cuando hay algo que mostrar.

Detalles que ya se probó que importan:
- **Animado, no instantáneo.** Un cambio de altura de golpe se lee como página
  rota; con transición se lee como despliegue. Es condición, no adorno.
- **Se anima `grid-template-rows` de `0fr` a `1fr`**, no `height` a `auto`
  (`auto` no interpola sin `interpolate-size`, sólo-Chromium) ni una altura fija
  en px (número mágico: el texto del estado no está redactado y el botón cambia
  de ancho con cada cara). `1fr` resuelve a la altura real del contenido. Su
  modo de fallo es el correcto: un motor que no interpole `fr` salta de 0 a la
  altura final, que es justo lo que se pide con `prefers-reduced-motion`.
- La separación superior va como **margen del primer hijo**, no `padding` del
  contenedor con overflow: con `border-box` el padding es un piso de altura que
  no colapsa y el folio plegado medía 16px en vez de 0.
- `inert` viaja con el estado plegado: no basta con invisible, tampoco tabulable
  ni leído por lector de pantalla.

`check-modes.py` lo verifica: plegado al cargar, desplegado al seleccionar,
replegado al arrastrar, transición declarada sobre `grid-template-rows`, y **el
cubo no se mueve** al abrirse (que es la propiedad que hace seguro el cambio).

### La transición entre páginas (maelstrom) está RESERVADA, fuera del lanzamiento

**Hoy el sitio NO tiene transición.** Entrar a una cara es una navegación normal
del navegador: **corte seco, sin fundido de ningún tipo.** Se apartó por
decisión del autor —no terminaba de funcionar— y **no se borró**.

Medido, no deducido: en una subpágina, `.face-page`, `main`, `body` y `html`
computan `animation: none` y `opacity: 1`. **La única excepción es el hero de la
portada**, que sube y aparece con `kf-rise` durante 1.3 s — y **eso no es un
resto de la transición**: corre en cualquier carga de la portada, incluida la
primera, y existía antes. Se queda a propósito: la portada es la que recibe, y
que tenga vida al cargar mientras las subpáginas entran secas es la asimetría
buscada. Está anotado junto a la regla, porque ahora que no hay transición es lo
único que se mueve al llegar y se lee fácil como un olvido.

**Y `kf-rise` TAMBIÉN CORRE AL VOLVER CON EL BOTÓN ATRÁS**, que es el dato que
faltaba y el que explica por qué se confunde. Medido: entrar a una cara no anima
nada —en `/hajime/` sólo late `kf-pulse` en un punto de estado—, pero al volver
a la portada el hero sube y aparece durante 1,3 s. O sea que **lo único que se
parece a una transición de página aparece justo después de una navegación**, que
es exactamente cuando uno la atribuye a la transición. Si alguien reporta que
«el maelstrom sigue corriendo», éste es el primer candidato y se distingue en un
segundo: el maelstrom giraba y desenfocaba la **página entera**; `kf-rise` sólo
sube el hero, y sólo en la portada.

**Dónde está**: `assets/css/maelstrom.css`, entero y calibrado, **no enlazado
desde ninguna página**. Ese archivo lleva en su encabezado cómo reactivarla, los
valores medidos y el bug conocido. En `styles.css` quedó un comentario en el
lugar de donde salió.

**Que siga apartada ahora TIENE GUARDA**, dentro de `check-modes`: ninguna regla
de view-transition viva en la portada ni en una subpágina, nadie pide
`maelstrom.css`, y `/hajime/` entra seca. **No lee archivos, le pregunta al
navegador qué reglas están en efecto** — por eso ve con una sola comprobación
las formas de reponerla, en vez de una regla por vía. Verificada en rojo contra
**seis**: `@view-transition` inline, `::view-transition-old(root)` inline, un
`<link>` al `maelstrom.css` real, la regla anidada en un `@media`, un `@import`,
y una hoja adoptada por JS.

**Y HAY QUE SEGUIR `r.styleSheet`, NO SÓLO `r.cssRules`** — la primera versión de
esta guarda tenía justamente eso mal y vivió una hora. Una `CSSImportRule` no
expone `cssRules` sino `styleSheet`, así que recorrer sólo `cssRules` deja pasar
`@import url("maelstrom.css")`, **que es la vía de reactivación escrita en el
encabezado del propio `maelstrom.css`**: la guarda estaba ciega exactamente en
la puerta principal. Medido: con el `@import` puesto daba 0 hallazgos y con un
`<link>` equivalente daba 7. Lo mismo valía para `document.adoptedStyleSheets`,
que no aparece en `document.styleSheets`.

**Al reactivar la transición, esa comprobación hay que sacarla**: va a dar rojo,
y eso es lo que se busca. Una guarda que sólo se vio en verde no está verificada
—la misma trampa que dejó viva la variante táctil—, y ésta se probó rota antes
de confiar en ella.

**SI ALGUIEN VE EL MAELSTROM CORRIENDO, LA PRIMERA SOSPECHA ES UNA COPIA VIEJA
DE `styles.css` EN SU NAVEGADOR, NO UNA REGRESIÓN.** Y la regla ya no es sólo
del maelstrom: **el mismo día pasó DOS veces más, con otros dos síntomas** — la
ayuda del cubo mostrando el texto de grilla en modo 3D (un `main.js` viejo: el
servido contiene «Drag to turn…» y la guarda lo mide en verde) y las subpáginas
«descentradas» a 1920/2560 (medidas contra `:8000`: left = right exactos, 600 y
920px). Cuando un reporte visual no reproduce contra el servidor con perfil
limpio, el diagnóstico es DOM-contra-red, no una búsqueda de regresión.
Ya pasó, el 2026-08-04: la
consola devolvía **seis** reglas de view-transition mientras el servidor
entregaba un `styles.css` sin ninguna. Las dos cosas eran ciertas sobre archivos
distintos — **el maelstrom vivía DENTRO de `styles.css` hasta `af7c726`**, así
que cualquier copia anterior a ese commit las trae, y son exactamente esas seis.

**EL FINGERPRINT ES EL CONTEO DE `view-transition`, NO EL TAMAÑO**: el viejo
trae **9** ocurrencias en el texto; el vigente, **0**. Ese número sobrevive a
todo lo que rompe a los demás.

El tamaño ya falló acá DOS veces, de dos maneras distintas, y por eso no es la
referencia:

1. **Sin unidad no compara nada.** `wc -c` cuenta bytes; `(await
   res.text()).length` en la consola cuenta caracteres UTF-16, y los
   comentarios en castellano (~430 caracteres no-ASCII) hacen que difieran en
   cientos. Comparar el número de la consola contra el de `wc -c` hizo
   aparecer un tercer archivo que no existía.
2. **El número del VIGENTE deriva.** Se tabuló «47738 bytes = 47187
   caracteres» y a las pocas horas ya era falso: el commit siguiente agregó
   comentarios al CSS. Y deriva dos veces: con cada edición, y con el final de
   línea — el checkout de Windows sirve CRLF por `:8000` y el blob de git es
   LF, así que ni siquiera «el vigente de hoy» es un solo número. **Un
   fingerprint del archivo vigente caduca con el próximo commit; referencia
   fija sólo la da lo que no cambia**: el blob viejo (pre-`af7c726`, LF: 44054
   bytes = 43583 caracteres) y el conteo de arriba.

La comprobación que separa el DOM de la red, que es la pregunta real:

```js
(async () => { for (const s of document.styleSheets) {
  let dom = 0; try { dom = [...s.cssRules].filter(r => /view-transition/i.test(r.cssText)).length } catch {}
  const t = s.href ? await (await fetch(s.href, {cache:'reload'})).text() : '';
  console.log(s.href, '| VT en el DOM:', dom, '| VT en la red:', (t.match(/view-transition/gi)||[]).length, '| chars:', t.length);
} })()
```

**`VT en el DOM: 6` con `VT en la red: 0` es el diagnóstico completo**: el
archivo está bien y lo viejo está del lado del navegador. **Un `Ctrl+Shift+R` no
alcanza para descartarlo**: no toca los *Local Overrides* de DevTools, que
persisten una copia del archivo en el perfil y se sirven por encima de la red.
Descartar el service worker —`navigator.serviceWorker.getRegistrations()`— es
necesario y no es suficiente.

**`check-modes` no puede caer en esto**, y conviene saber por qué antes de
sospechar de su verde: borra su perfil de Chrome en cada corrida
(`shutil.rmtree(PROFILE)` antes de lanzarlo), así que arranca sin caché y sin
overrides. Mide contra el mismo `:8000` —`BASE` por defecto—, pero siempre
contra lo que el servidor entrega. Si la guarda y un navegador se contradicen,
**la copia vieja está en el navegador**.

**Por qué en un archivo y no detrás de un flag.** Es una transición **entre
documentos**: `@view-transition` tiene que estar en la página que se va **y** en
la que llega. **Todas las páginas menos la portada no cargan ningún
JavaScript** —
verificado: `document.scripts.length` es 0 en una subpágina—, así que un
interruptor en runtime obligaría a meter JS en todas. No es una preferencia de
estilo: es que la otra opción choca con una regla del proyecto.

Lo calibrado, para no rehacerlo a ojo: **rotación 46°** (era 14°), **escala
2.1** (era 1.3), **blur 4px** (era 16px), entrada desde **−38°** y 0.52, las dos
rotaciones en el **mismo sentido**. Y las **dos causas** de que la primera
versión se leyera como fundido y no como giro:

1. **El desenfoque tapaba el giro.** Una rotación se percibe por el ángulo de
   los BORDES, y 16px de blur son justo lo que los borra. Bajó a 4px.
2. **El fundido iba atado al giro**, así que la página estaba casi transparente
   antes de haber girado lo suficiente. Giro y fundido tienen que ser **dos
   animaciones con curvas distintas** sobre la misma capa. Juntarlas «para
   simplificar» reintroduce el problema.

**HAY UN BUG CONOCIDO Y ES EL PRIMER LUGAR DONDE MIRAR.** La variante táctil
**no hace lo que dice**: dentro de `@media (pointer: coarse)` se definen
`kf-maelstrom-out`/`in` —escala + fundido sin blur— pero **nunca se asignan**,
porque esas reglas sólo tocan `animation-duration`. El `animation-name` sigue
siendo `kf-maelstrom-spin-out`, que lleva `filter: blur(4px)`. O sea que **en un
teléfono corría la versión de escritorio con desenfoque**, apenas más rápida:
exactamente el costo que esa variante existía para evitar. Nunca se midió en un
dispositivo real, así que no se sabe cuánto de «no funcionaba bien» venía de
ahí. **Cualquier documento que diga «táctil sin blur» está describiendo la
intención, no lo que corría.**

**Lo que NO se fue con ella, y no son restos olvidados:**
- **La precarga (`rel=prefetch`) al seleccionar la cara.** Sirve igual sin
  transición, o se nota más: ahora el corte es seco, y un corte contra una
  página que todavía está bajando es el blanco entre una y otra.
- **El respaldo por `sessionStorage` del botón atrás.** Nunca tuvo que ver con
  la transición: restaura la **cara elegida** en el cubo. Verificado después de
  apartarla — `back_forward`, cara restaurada, folio abierto.

### Volver atrás restaura el cubo por dos caminos
Los dos hacen falta. **bfcache**: la página vuelve viva y entera sin ejecutar
nada; lo único que puede romperse es el contexto WebGL (el navegador libera la
GPU mientras está congelada), así que en `pageshow` con `persisted` se comprueba
`isContextLost()` y, si se perdió, se rehidrata. **Sin bfcache** (Chrome lo
descartó por memoria, o `Cache-Control: no-store` lo deshabilita —ojo, el
servidor de desarrollo manda `no-store`): la selección se restaura desde
`sessionStorage`, y **sólo** si la navegación fue `back_forward` — llegar a la
portada normalmente no debe elegir una cara en tu nombre.

### La capa de metadatos se genera y se vigila; nada se escribe a mano dos veces
`sitemap.xml` y `og-image.png` salen de scripts (`tools/make-sitemap.py`,
`tools/make-og-image.py`). El sitemap es la misma lista de URLs que ya existe
como directorios: se deriva en vez de copiarse, y `check-structure.py` verifica
que no le falte ninguna página. La imagen OG es **sólo tipografía** —llevaba el
cubo capturado del sitio y se sacó—, así que su script no necesita navegador, y
**lee los colores del `:root`** en vez de copiarlos: copiarlos haría que la
tarjeta derive de la paleta en silencio y que `:root` dejara de ser una entrada
real de la imagen.

- **`robots.txt` no bloquea crawlers de IA** — GPTBot, ClaudeBot, CCBot y demás.
  Es deliberado y está escrito en el archivo para que nadie los agregue "por las
  dudas": la descubribilidad por máquinas es objetivo del proyecto, la misma
  razón por la que el contenido va en el HTML.
- **Títulos y descriptions únicos por página, verificado.** Las seis subpáginas
  de las caras salieron del mismo molde y **compartían la description palabra
  por palabra**; eso hace que buscadores y crawlers las traten como duplicados y
  se queden con una. Ahora cada placeholder nombra su cara, y la guarda no deja
  que vuelvan a coincidir.
- **La 404 lleva `noindex` y queda fuera del sitemap**, y la guarda falla si una
  página con `noindex` aparece listada: son dos declaraciones que se contradicen.
  Usa rutas absolutas porque GitHub Pages la sirve ante URLs de cualquier
  profundidad. **Desde el 2026-08-07 el criterio es GENERAL y derivado**:
  `make-sitemap` excluye a cualquier página que declare `noindex` leyendo la
  meta de la propia página — el segundo caso es el andamiaje de seguros
  mientras sea placeholder (ver su decisión, que agrega la guarda del olvido
  inverso en `check-ready`).
- **`canonical`, `og:url` y `og:image` son ABSOLUTAS y autorreferentes**, con
  guarda. Quien arma la vista previa (LinkedIn, Slack, X) no es el navegador del
  lector y no resuelve rutas relativas: la tarjeta sale sin imagen. **El fallo no
  se ve en el sitio, se ve afuera**, que es por qué necesita guarda y no revisión
  visual. La 404 está exenta: no lleva ninguna de las tres, a propósito.
- **La og-image puede quedar vieja en silencio**: es un archivo, no una vista.
  `tools/og-image.lock.json` guarda el hash de sus ENTRADAS y la guarda avisa si
  alguna cambió. **La lista tiene que ser exacta en las dos direcciones**: una
  entrada de más avisa por cambios que no influyen —señal falsa, el mismo mal que
  partir `check-ready` vino a curar— y una de menos deja la imagen vieja en
  silencio. Hoy son: el script, el `:root` de styles.css, y las fuentes Inter y
  Zen Kaku. Salieron al sacar el cubo de la tarjeta: **cube.js** y **Cormorant**.
  Se hashea sólo el `:root` y no el CSS entero, que cambia por cosas ajenas.
- **Los archivos de texto del lock se hashean NORMALIZADOS; los binarios, por
  bytes.** `core.autocrlf=true` es el valor por defecto en Windows: git guarda
  LF y escribe CRLF al hacer checkout. Hasheando los bytes crudos del `.py`, la
  guarda avisaba «la og-image quedó vieja» con sólo **cambiar de rama y volver**
  —y también en cualquier **clon nuevo**—, sin que hubiera cambiado nada que
  mueva un píxel del PNG. Doblemente malo: es la señal falsa que esta guarda
  existe para no dar, y rompía justo el caso que motivó hashear contenido en vez
  de fechas, que era sobrevivir a un clon. Las fuentes siguen por bytes a
  propósito: son binarias, git no las convierte, y ahí el byte crudo sí es el
  contenido. Verificado en las dos direcciones: pasar el script a CRLF y a LF no
  avisa, y cambiar una línea de verdad sí.
- **La tarjeta se juzga a ~500 px, no a 1200**: es el ancho al que se ve en un
  feed. Ahí el nombre de la marca quedaba en ~10 px y era lo primero que se
  perdía; ahora va al doble de cuerpo y en blanco. Y la bajada usa **Inter, no
  Cormorant**, por lo mismo que el romaji del cubo: a ese tamaño las astas finas
  de una serif de display desaparecen. `--prueba` deja la versión reducida.
- **hreflang: sólo el patrón anotado en el README**, sin implementar, hasta que
  exista `/ja/`.

### Los placeholders de metadatos también se cuentan
Los `TODO` de `<title>` y de `content="…"` **no llevan `class="todo"`**, porque
no son elementos. Durante un tiempo no se contaron, y el sitio podía dar «LISTO
PARA PUBLICAR» con seis descriptions que decían *«TODO: descripción de esta
cara.»* — exactamente el fallo que la guarda existe para evitar. `placeholders()`
ahora cuenta las dos familias. Si aparece otra clase de placeholder que no sea
un elemento con clase, hay que agregarla ahí.

### El shader del mar es código cerrado
El GLSL de `assets/js/background.js` está calibrado a mano y **no se toca**. Su
paleta (`deep`, `mid`, `crest`) vive en constantes del fragment shader, **fuera
de `:root`** — es la única excepción a "ningún color literal fuera de `:root`".
Cambiar el color del mar exige editar el shader, y esos valores no se sincronizan
solos si cambia la paleta.

### En la versión inglesa no va japonés ornamental
La prueba es simple: **si el japonés sólo traduce la palabra inglesa que tiene
al lado, es textura y se saca.** Si es un nombre conceptual propio, se queda.

- **Se sacaron**: `The Cube · 立方体`, `Method · 一次資料`, los kanji que
  encabezaban las tres tarjetas del método (`一次資料` / `追跡可能` / `公開`),
  y —en la revisión de quince puntos— **el rótulo `免責事項`** (del footer de
  todas las páginas y del `<title>`/eyebrow de `/disclaimer/`: es la traducción
  de «disclaimer») y **los nombres japoneses de la lista de fuentes DE LA
  PORTADA** (sólo BOJ y FSA los tenían y la columna quedaba dispareja).
- **Se quedan**: `素顔`, los seis nombres de las caras, los tres términos del
  núcleo, y **los nombres reales de los organismos en `/method/`** (`日本銀行`
  junto a Bank of Japan) — ahí no decoran: son el nombre por el que se llega a
  la fuente, y desde la revisión van como **línea secundaria bajo el nombre
  inglés**, no en columna propia. También quedan, con función y no como adorno:
  la marca de agua del About (`産霊　河川　言霊` — sostiene además el supuesto
  de glifos de la vista explotada), el selector `日本語（近日公開）` del footer
  (le habla al lector japonés), y las unidades `百万円/十億円/兆円` en la prosa
  de /method/ (son el contenido). **Todos los glifos retirados siguen en el
  subset para /ja/** — ver el @font-face.

**La versión japonesa se escribirá como ORIGINAL, no como traducción de ésta**:
ahí «The Cube» será katakana, no `立方体`. Por eso lo que se sacó no se tiró —
los glifos siguen en el subset a propósito. Ver la advertencia en el
`@font-face` de `styles.css` antes de regenerarlo.

### `/musubi/` explica la IDEA, no los nombres

**Esto reemplaza una premisa anterior.** La página nació como «el sistema de
nombres»: siete bloques sobre por qué hay nombres japoneses, cómo se deriva cada
uno, y una tabla con las seis caras y su razón. Se redactó entero de nuevo, en
**cuatro bloques** que explican la idea de la que sale la plataforma — el agua
(`Kasen`, `Okeanos`), el nombrar (`Kotodama`), el vínculo (`Musubi`) y quién es
el lector (`Odysseus`, `Aeolus`). **Desde el 2026-08-05 son CINCO**: el autor
sumó «How the reading divides» (la división de la lectura: `Taichi`, `Yorozu`,
`Yūgen`), entre el bloque del cubo y el del lector — el 3 explica por qué el
mapa es un cubo de caras al mismo nivel; el 5, cómo se divide el trabajo
DENTRO de una cara. Dos decisiones del bloque, anotadas junto al HTML:

- **Los tres nombres van en `.name` SIN enlace aunque SÍ tienen página** —
  acá se presentan como parte del sistema conceptual, no como destinos (el
  camino es /hajime/, de donde cuelgan). Era «la excepción más discutible del
  marcado» mientras en /hajime/ el mismo marcado sí enlazaba; **desde el
  2026-08-07 ya no es excepción sino la regla uniforme: `.name` en prosa no
  enlaza en ninguna página** — en /hajime/ la puerta son las tarjetas de las
  subcaras. Anotado también en el CSS, donde estaban las reglas de `a.name`.
- **Sin referentes filosóficos, a propósito**: el `context.md` respalda el
  bloque con Hegel, Jung, el yin-yang, Agustín y Amaterasu, y no se nombra
  ninguno — la página ya maneja seis conceptos de dos tradiciones, y cinco
  referencias más de otras tres la convierten en un ensayo, justo en la
  página cuya función es desactivar la lectura esotérica. Que nadie los
  agregue creyendo que faltan.

- **La tabla de las seis caras salió a propósito, no se perdió.** Cada cara dice
  lo suyo en su propia página; la tabla obligaba a mantener sincronizadas dos
  listas de la misma cosa.
- **La página no explica los nombres de las caras, y no hay que reponer eso.**
  Es la consecuencia buscada del punto anterior.
- **Los nombres del marco van en `<i class="name">`** (los seis originales y,
  desde el bloque 5, también Taichi/Yorozu/Yūgen), cursiva y a color de texto
  pleno. `<i>` y no `<em>` porque `<em>` es énfasis y un lector de pantalla
  lo entonaría; cada nombre se marca **una sola vez**, donde se lo presenta.
  Y no van en oro: el oro es de los subtítulos y los enlaces.
- **Usa `.face-page`, como las otras nueve subpáginas.** Antes usaba `.naming*`,
  que ya no existe: se borró con la tabla. De paso ganó el `<h1>` que le
  faltaba — era la única subpágina que no tenía, sólo un `<h2>`.
- **Dos frases del bloque 3 son las mismas que cierran el lead del cubo en la
  portada**, a propósito del autor. Son dos copias del mismo texto y **no hay
  guarda que las compare**: si se redacta una, hay que mirar la otra. Está
  anotado en el HTML de los dos lados.
- **La lista de cadenas duplicadas sin guarda, completa (2026-08-07)** —
  cuando se toque una, mirar las otras: (1) las dos frases del cubo de arriba
  (portada ↔ /musubi/); (2) el cierre de Taichi ↔ el subtítulo de /musubi/
  (registrado en la decisión de las subpáginas de Hajime); (3) **«First
  analysis on the way», que es TRIPLE, no doble**: el badge del hero
  (`index.html`), el estado de `/hajime/` y `FACES.hajime.status` en
  `assets/js/main.js` — el JS repinta el folio de la portada con ese texto,
  así que cambiar el HTML sin el JS deja la portada contradiciéndose sola.
  El día que salga la primera nota, esa cadena caduca en los TRES lugares a
  la vez.

### `/method/` es el desarrollo; la sección de la portada es el resumen
La sección `#method` de la portada **queda** —los tres pilares y los cuatro
pasos— y la nav «Method» **sigue apuntando ahí**, no a la subpágina. A
`/method/` se llega por un enlace al pie de esa sección.

**La lista taxativa de fuentes vive dentro de `/method/`, no en un `/sources/`
aparte.** Separarlas obligaría a mantener sincronizados el criterio y su
aplicación, que es exactamente lo que no debe poder divergir. La portada muestra
**cinco de ejemplo**, japonesas y globales, para que se vea que el alcance no es
sólo Japón.

### La frontera castellano/inglés es invisible, y por eso tiene guarda

El repo se trabaja en castellano y el sitio se publica en inglés. **El problema
es que la frontera no se ve**: un comentario en castellano es correcto, y la
misma frase dentro de un `content=` viaja en cada enlace compartido. Ya pasó —
`og:image:alt` decía «El cubo de seis caras de Kotodama Finance» **en las diez
páginas**, y se descubrió de casualidad.

**En inglés, sin excepción**: texto visible, `<title>`, `description`, todo
Open Graph y Twitter, los atributos que ve un usuario o un crawler (`alt`,
`aria-label`, `title`, `placeholder`), `sitemap.xml`, `robots.txt`, la 404, y
**los mensajes de `console.*` de `main.js` y `cube.js`**.

**En castellano, deliberado**: comentarios de HTML, CSS y JS; `tools/` y sus
mensajes; `CLAUDE.md`, `README.md`, `docs/`; `_ref/`.

**La línea que separa un comentario de un `console.warn`** es la que costó
pensar: un comentario no se ejecuta; un `console.warn` **sí** — es salida que el
programa produce en runtime, dirigida a quien mire la consola. Es interfaz,
aunque sea técnica.

**Y `robots.txt` y `sitemap.xml` no tienen «comentarios» en el sentido del
HTML**: esos archivos **no tienen versión renderizada**, así que quien abre
`/robots.txt` ve el archivo tal cual, comentarios incluidos. Ahí el comentario
es superficie publicada. Por eso el de `sitemap.xml` se arregló **en el
generador** (`make-sitemap.py`), no en el archivo: si no, vuelve a la próxima
corrida.

**Buscar acentos NO alcanza** — «el cubo de seis caras» no tiene ninguno. El
método que sirve es **aislar la superficie publicable, que es finita, y
revisarla entera**; sobre ese conjunto reducido un detector simple alcanza para
las regresiones. Está en `check-structure`.

**La guarda es incompleta a propósito y lo dice en su salida.** Se le escapó
`«no se pudo hidratar; se mantiene la grilla»` —ni un acento, ni una palabra de
su lista—, que apareció revisando a mano los `console.*`. **Una guarda que
aparenta completitud es peor que ninguna**: cubre la reincidencia de lo
conocido, y al agregar una página hay que leer su superficie igual.

### No redactar contenido
Sólo **andamiaje con placeholders `TODO`**, en castellano a propósito para que no
puedan confundirse con copy real (el sitio está en inglés). El texto final y la
versión japonesa son un pase aparte del autor. Tampoco se inventan explicaciones
del sistema filosófico ni las razones de los nombres.

### Otras reglas vigentes
- **Ante una pregunta sobre cómo funciona el repo — criterios, decisiones,
  porqués — PRIMERO mirar si ya está registrado** (este archivo, el README,
  los comentarios del fuente). Si lo está, responder CITÁNDOLO y decirlo
  explícito — «esto ya estaba escrito en X» — en vez de re-derivarlo o
  re-investigarlo. Pedido del autor (2026-08-14): el señalamiento le dice a
  él que la pregunta era redundante, y calibra al Claude del chat, que arma
  prompts sobre este registro vía la copia derivada de OneDrive (ver su
  decisión, primera de la lista).
- **Los rótulos de ayuda del cubo NO se cambian** — «Click a face to select
  it.» queda como está. Cerrado por el autor (2026-08-08); no volver a
  proponerlo.
- **Ningún color literal fuera de `:root`**, incluidos los que consume el JS
  (`cube.js` los lee con `getPropertyValue`, **sin fallback**: si falta un token
  falla con su nombre en vez de disfrazarlo con un hex de repuesto).
- **El contenido va en el HTML**, no inyectado por JS: la descubribilidad por
  crawlers de IA es objetivo del proyecto y esos crawlers no ejecutan JS.
- **La grilla de seis es la capa semántica**: nav de teclado y lo que leen los
  crawlers. En vista 3D se oculta con el patrón clip, **nunca** `display:none`.
  Al recibir foco se corre **al costado** del escenario, no encima: taparlo
  escondía justo lo que el usuario de teclado necesita ver. Y lleva
  **`user-select: none` mientras está recortada** (repuesto en `:focus-within`):
  sin eso, copiar la sección del cubo en 3D arrastraba las seis tarjetas
  invisibles al portapapeles. No toca accesibilidad — AT y foco no pasan por la
  selección — ni a los crawlers, que leen el DOM.
- **URLs por directorios** (`/musubi/`, `/hajime/`…), sin extensión.
- **Cada texto japonés nuevo obliga a regenerar el subset** de Zen Kaku. Ver
  README. **`document.fonts.check()` no sirve** para verificarlo: informa si la
  fuente está cargada, no si contiene el glifo.
- **Los dos comandos de subset NO son iguales, y unificarlos rompe uno.** El
  japonés va **sin** `--layout-features`; el latino, **con** `'*'`. Medido en
  las dos direcciones: con el flag, Zen Kaku pasa de 163 glifos a 258 y suma
  `aalt fwid ordn sups`; sin él, las latinas pierden 374 y 503 glifos. **Cada
  uno reproduce su archivo commiteado sólo con su propia forma.** La regla real
  no es «usar el flag» sino **que el comando escrito reproduzca el archivo que
  se sirve**, y eso se comprueba regenerando y comparando glifos y features.
- **Y el subset LATINO tiene el mismo problema, sin guarda que lo mire.** La
  verificación automática cubre sólo el japonés. Ya mordió dos veces con
  caracteres que uno da por sentados: los **paréntesis de ancho completo**
  （U+FF08/U+FF09), que no entran por el rango latino, y **ū (U+016B)** de
  «Yūgen», que no entraba en ninguno de los rangos declarados. **Al escribir
  romaji con macrón —ō, ū— verificar contra la `cmap` antes de publicar.**

---

## Flujo obligatorio antes de cada commit

Correr las guardas. **Si alguna falla, no commitear**: arreglar, o revertir al
último commit verde y avisar qué se revirtió y por qué. El objetivo es que todo
commit sea un punto de restauración seguro por construcción, no por suerte.

| Guarda | Cuándo | Costo | Se espera |
|---|---|---|---|
| `python tools/check-structure.py` | siempre | instantánea | **verde** |
| `python tools/check-modes.py` | siempre | ~40 s | **verde** |
| `python tools/check-pendulum.py` | antes de push, o al tocar la física | ~2–4 min | **verde** |
| `python tools/check-ready.py` | antes de publicar a `main` | instantánea | **`2` esperado** desde el 2026-08-07 (hoy 36: 25 de seguros + 11 de notas — la tarjeta de sector salió del marcado el 2026-08-08; `0` cuando todo eso quede redactado — era 7 del docstring) |

Las dos que usan navegador necesitan el sitio servido en `:8000`.

**La guarda del deploy no está en la tabla por lo mismo que
`check-maintenance`**: corre a demanda —dentro de `tools/make-deploy.py`, el
día de publicar—, no por commit. Las cuatro siguen siendo cuatro.

**Por qué `check-ready` no va en cada commit.** Está en rojo por diseño mientras
queden placeholders, y **una guarda siempre en rojo deja de ser señal**: uno se
entrena a ignorarla y el día que se rompa algo de verdad no lo ve. Por eso se
partió en dos, con códigos de salida distintos:

- `check-structure.py` — nav y footer idénticos, cobertura del subset, y **sin
  placeholders nuevos contra `tools/placeholders-baseline.json`**. Sale `0`/`1`.
  Ésta es la que tiene que estar verde siempre, así que su rojo significa algo.
- `check-ready.py` — ¿puede ir a `main`? Sale `0` listo, **`2` falta redacción
  (esperado, no es regresión)**, `1` algo roto de verdad.

Cuando se redacta un placeholder el conteo baja: la guarda lo informa y **no**
falla, pero hay que fijar el piso nuevo con
`python tools/check-structure.py --actualizar-baseline`.

**Tras cada commit que toque CLAUDE.md, regenerar la copia derivada de
OneDrive** (`python tools/make-copia-claudemd.py`): el gatillo es el commit
— no el deploy — y el olvido lo caza check-structure en la corrida
siguiente. Ver la decisión de la copia derivada, primera de la lista.

**Tags**: sólo en hitos, anotados. `v1-dark` (navy + oro con el cubo),
**`v1-content-complete`** (sitio terminado de contenido: cero placeholders,
`check-ready` en 0) y **`v1-published`** (la publicación, 2026-08-06 — en el
**commit FUENTE `6dc8214`**, no en `main`: el commit de `main` es un snapshot
generado fuera de la historia de desarrollo, y el que pasó por las guardas es
el fuente; el mensaje del commit de `main` lleva el hash cruzado). La serie
quedó completa; el próximo tag lo justifica un hito nuevo, no la rutina.

**UN TAG NO SE MUEVE.** Ya pasó la tentación y la respuesta quedó cerrada: el
mensaje de `v1-content-complete` describe el plan de DNS **anterior** al vigente,
y aun así **no se re-taguea**. Un tag anotado es un **registro fechado del estado
en ese commit**; si se reescribe cada vez que cambia el plan deja de ser un punto
de restauración y pasa a ser una copia peor de este archivo — que sí es el
documento vivo. Y `--force` sobre un tag ya empujado **rompe los clones ajenos**,
que siguen con el objeto viejo. Un mensaje de tag desactualizado no es deriva:
es historia, igual que `docs/v1-dark/README.md`.

`v1-content-complete` **es el punto al que volver si algo se rompe en la
migración de DNS.** Apunta al último estado verificado en verde y no al commit
donde se redactó el último placeholder (`2115a4e`): ahí el contenido ya estaba
completo pero `check-structure` estaba en rojo —la guarda del baseline se rompía
justo al llegar a cero— y se arregló recién en el commit siguiente. **Un punto
de restauración tiene que estar verde**, si no es una trampa.

---

## Cabos abiertos (lista viva)

**Estado al cierre de la sesión del 2026-08-03.** El andamiaje está completo
—once páginas, el cubo, la transición, la capa de metadatos y las guardas—,
**empezó la redacción**, y el registro técnico ya no tiene huecos.

### Hecho en esta sesión (2026-08-03): documentar desde el código

Sesión de documentación: **no se tocó ni una línea de comportamiento**. Se
cerraron los huecos del registro técnico leyendo el fuente, no los papeles.

- **README**: dos secciones nuevas, «El import map» y «El cubo: parámetros
  vigentes» (geometría, constantes, encuadre, luces, colores, péndulo,
  `snap`/`parked`, lazy-init), más el índice de `docs/mediciones/`.
- **`docs/mediciones/rendimiento.md`**, nuevo: la única medición de rendimiento
  que existe, de escritorio, fechada y con condiciones.
- **Divergencias resueltas contra el código**: `docs/v1-dark/README.md` daba como
  actuales unas luces y un fondo que son del tag, y quedó marcado como histórico
  punto por punto; `luz-arco.md` sí coincidía y quedó confirmado.
- **`cube.js`**: el encabezado decía «las luces van tintadas en oro» y era falso
  **desde el primer commit** (verificado con `git log -L` y `git log -S`: `hemi`
  y `key` nunca fueron doradas). Se sacó de ahí y el reparto real vive ahora en
  el bloque de luces, junto al código que lo aplica.

**La regla que dejó la sesión**: los números del cubo se leen del código y se
tabulan en un solo lugar. Ver la decisión cerrada correspondiente.

### Ya redactado: texto definitivo, versión de lanzamiento en inglés

- **El hero de la portada.** Titular y bajada nuevos.
- **`/sugao/` entera**: perfil profesional y personal, con LinkedIn (URL real) y
  LibraryThing. Sin introducción, sin foto y sin slots vacíos.
- **`/disclaimer/` completo** —ocho cláusulas— y **la línea corta del `免責事項`
  en el footer de las once páginas**.

La versión japonesa es un pase aparte y **se escribe como original, no
traduciendo de acá**.

### Andamiaje agregado en la sesión del 2026-07-25

- **`/method/`**, subpágina nueva, con placeholders. La sección `#method` de la
  portada **queda como resumen** y la nav sigue apuntando a ese ancla; a la
  subpágina se llega por «Read the full method →» al pie. La lista taxativa de
  fuentes vive **dentro** de `/method/`; no hay `/sources/`.
- **Cinco fuentes de ejemplo** en la portada: BOJ, FSA, EDINET, BIS y Damodaran
  Online, japonesas y globales.
- **Rótulos japoneses ornamentales retirados de la versión EN** (`立方体`,
  `一次資料`, `追跡可能`, `公開`). **Los glifos siguen en el subset** para
  `/ja/`, con una advertencia en el `@font-face` para que nadie los borre al
  regenerarlo.

### El único frente activo: la redacción — REABIERTO el 2026-08-07

**La redacción volvió a ser el frente activo, y es a propósito**: el
andamiaje de la capa 1 de seguros entró con 25 placeholders que esperan el
texto del autor (ver la decisión, primera de la lista). El baseline dice 25
y ése es el techo — más que eso es regresión. El sitio PUBLICADO no cambia
hasta ese pase.

*(Lo de abajo es el registro del estado anterior, 2026-08-05, con el que se
publicó:)* **Cero placeholders. La redacción terminó**, y con ella el único frente que
bloqueaba publicar. El baseline quedó en `0` — de ahora en más, cualquier
número distinto de cero que informe `check-structure` es una regresión, no
trabajo pendiente. Es un cambio de significado de esa guarda: hasta acá bajar
era progreso; ahora subir es un bug y no hay «bajar».

### La procedencia del texto se declara: UNA línea, y sólo en `/method/`

**Esto reemplaza una versión anterior de DOS bloques** —«How this is written» al
final de «What counts as a source», y un colofón al pie— que se retiraron por
decisión del autor. Hoy es **una sola línea**, en el lugar del primero:

> Credit where credit's due: This project would not have been possible without
> my AI assistant.

**«Credit where credit's due» va con WHERE.** La versión con «were» es un error
de tipeo y se lee como tal. Está anotado también en el HTML.

**Por qué en `/method/` y en ninguna otra parte.** Es donde se declara cómo se
produce lo que se publica, así que es donde corresponde decir cómo se produjo el
texto mismo. Un sitio que le exige trazabilidad al dato y no declara la de su
propia prosa tiene un punto ciego; y si alguien lo descubre después sin que esté
dicho, el daño al rigor es mayor que el costo de decirlo.

**No va al footer global**, aunque sea la clase de línea que suele ir ahí. El
footer se repite en todas las páginas y esto pertenece a la que habla del método.
Es la regla opuesta a la del `免責事項` corto, y por el mismo criterio: una
advertencia legal sirve donde el lector esté leyendo; una declaración de
procedencia sirve donde se explica el procedimiento.

**Va sin título propio, dentro del cuerpo de la sección.** Es una línea; un `h3`
encima la anunciaría como tema aparte cuando es el cierre de qué cuenta como
fuente. Con el colofón se fueron también `.face-page__minor` y `.colophon` del
CSS, que quedaron sin ningún elemento que las usara.

### La 404 rompe el patrón del kanji a propósito

Lleva **una frase** —`この航路はありません`— donde las seis caras llevan un
nombre en kanji. **No es una inconsistencia que haya que corregir.** Las caras
nombran algo que existe; esta página no es una cara del cubo y no tiene
contenido que nombrar: tiene una **ausencia**, y un sustantivo suelto no puede
decir «esto no existe». Quien la unifique a un kanji suelto por coherencia está
eligiendo la simetría por encima del sentido.

Por eso usa `.face-page__phrase` y no `.face-page__kanji`: ese otro tamaño llega
a 4rem porque está dimensionado para uno o dos glifos, y diez a ese cuerpo miden
más que el ancho de la página.

### `/method/`: la lista de fuentes se DERIVA del `context.md`

**No se mantiene una copia paralela.** La lista de 50 fuentes sale de
`§Fuentes de Datos Mapeadas` de `kotodama_finance_context.md`, que es la fuente
de verdad. Al actualizarla se parte de ese archivo, no de la página.

- **34 Tier 1** (primaria oficial) + **16 Tier 2** (primaria no-oficial
  atribuida), en 12 grupos por dominio, Tier 1 primero dentro de cada uno.
- **La marca de tier es un cuadrado lleno contra hueco, en oro**, con leyenda.
  Reusa el vocabulario de los puntos de estado de las caras porque ya está
  establecido; cuadrado y no círculo para que no se confunda con ellos.
- **Tres cosas quedan fuera, cada una por su motivo**: el Tier 3, que lo cubre
  un párrafo del texto; **EDINET DB y Yahoo Finance Japan**, que parsean y
  redistribuyen dato ajeno y por lo tanto son **secundarias** —publicarlas
  contradiría, en la misma pantalla, el principio que la página declara—; y
  `japan_insurance_v2.xlsx`, que es un archivo interno del proyecto.
- **Ninguna URL se completó de memoria.** Las 17 que el `context.md` no traía se
  buscaron, se verificaron y las aprobó el autor una por una. En una página cuyo
  argumento es que toda cifra es trazable, un enlace inventado sería el peor
  error posible.
- **El subset japonés casi se duplicó**: 149 → 288 códigos, 13,2 → 29,8 KB por
  peso. Es el costo de nombrar 50 entidades en japonés, y entró hiragana y
  katakana por primera vez.

### Las seis caras quedaron con un molde común — y el eyebrow se fue

Al redactarlas se unificó la cabecera con la de `/sugao/`: **`<h1>` con kanji y
romaji, línea de función en `.face-page__gloss`, y nada más.** El
`<p class="eyebrow">` se eliminó de las cinco.

Había **tres capas diciendo lo mismo**: el eyebrow (`Data / Analysis`), el gloss
(`«the beginning»`) y el lead, que abre glosando el nombre. Dos señales de que
sobraban: el eyebrow de `/tosei/` ya decía literal la línea de función que se le
iba a poner, y el significado del kanji que llevaba el gloss lo dice ahora el
lead en prosa, en las cinco.

### El `domain` de las tarjetas: comprimido, no idéntico — decisión cerrada

**Las seis tarjetas se reescribieron.** No para igualarlas a la línea de función
de su página, sino para que **cada una sea la versión COMPRIMIDA de la suya**:

| Cara | Tarjeta (portada) | Línea de función (página) |
|---|---|---|
| `肇 Hajime` | Data and analysis | Data and analysis |
| `素顔 Sugao` | The person behind | The person behind the platform |
| `渡世 Tosei` | Personal finance | Personal finance in Japan |
| `家紋 Kamon` | Community | Community and network |
| `鳥居 Torii` | Learning | Learning and resources |
| `絆 Kizuna` | Acting on it | Understanding to action |

**Que no sean idénticas es deliberado**, y es la parte que se pierde si alguien
las "unifica": **la tarjeta se lee de un vistazo entre seis, la línea de función
se lee sola y con calma.** Son dos trabajos distintos. Lo que sí tienen que
compartir es la raíz — quien va de la tarjeta a la página encuentra continuidad,
no dos nombres para lo mismo.

**Todas sin barra**, mismo registro corto. El patrón anterior estaba a medias:
tres con barra (`Data / Analysis`, `Learn / Resources`, `Act / Business`) y tres
sin ella.

**Estos valores YA NO salen del archivo de referencia**, que sigue diciendo
`Data / Analysis`, `The human behind`, `Connect`, `Learn / Resources` y
`Act / Business`. Ese archivo **no se editó a propósito**: es la instantánea del
landing original, y cambiarle un campo lo convertiría en un híbrido que no es ni
el original ni el estado actual — además de estar en `.gitignore`, o sea que la
edición ni siquiera quedaría versionada. **La defensa contra la deriva es esta
tabla**, que sí está versionada y sí se lee al empezar.

**El folio del cubo no muestra el `domain`.** `FACES` en `assets/js/main.js`
tiene `romaji`, `state` y `status`, nada más; el folio muestra el estado y el
botón. El `domain` vive únicamente en las seis tarjetas de la grilla.

**Al redactar `/method/`, aplicar también las dos notas de fuentes provisorias**
que hoy están en la portada, ya corregidas por el autor y anotadas en el
comentario del propio HTML: BIS → «Cross-border banking exposure»; Damodaran →
«Valuation datasets by sector and region».

### Los tres estados dicen QUÉ HAY, no qué importa — decisión cerrada

`5de4566`. **Sugao lleva `active` con el estado «Live»; Hajime bajó a `light` y
conserva «First analysis on the way».** Las otras cuatro no se tocaron.

Se lee al revés de lo que uno espera, y por eso conviene el motivo escrito:
Hajime es la cara del análisis, o sea el proyecto, así que el instinto es
dejarle el marcador más fuerte. Pero **Hajime no tiene todavía una línea
publicada y Sugao está entera.** El lead del cubo ya promete «One is live
today», y con el reparto anterior la grilla lo desmentía: el punto lleno estaba
en la cara vacía. Si alguien lo "arregla" devolviéndoselo a Hajime, vuelve a
haber dos caras leyéndose como la más fuerte y ninguna es la publicada.

**No se agregó un cuarto estado, y el porqué importa más que el resultado.** Se
evaluó un `live` propio y no había con qué distinguirlo:

- **La animación no sirve.** `prefers-reduced-motion: reduce` apaga todo con
  `animation: none !important`, así que dos puntos que sólo difieran por el
  pulso quedan idénticos justo para quien más necesita la señal.
- **Un color nuevo tampoco**: la paleta es navy + oro, y el vocabulario ya está
  agotado — lleno en oro, hueco en oro, hueco en gris.

Con tres estados y tres grados de «cuánto hay», alcanzaba con **cambiar quién
ocupa cada uno**. El sistema queda intacto.

Sigue abierta una decisión adyacente que ya estaba anotada: el `domain` de la
tarjeta («The human behind») sale del archivo de referencia, así que cambiarlo
es otra cosa.

### Cerrado en la sesión del 2026-08-04: los metadatos alcanzaron al hero

`bf70085`. El `<head>` de la portada y la tarjeta social seguían describiendo el
hero anterior. **Es el modo de fallo de fábrica de estas dos cosas**: no se ven
al mirar la página, así que sobreviven al reemplazo del texto que describen.

- `<title>` y `description`/`og:description` **derivados del hero**, con la
  dependencia anotada en el propio `<head>`.
- `LINEA` de `make-og-image.py` es ahora **el titular del hero, literal**;
  imagen regenerada y lock resellado. Verificada a 500 px. **Desde el
  2026-08-06 la única divergencia permitida es la PUNTUACIÓN**, confirmada
  por el autor con su regla: **el punto sale del hero porque el `<br>` hace
  su trabajo, y se queda en la tarjeta porque ahí el titular va en una sola
  línea y no hay salto que separe — MISMA REGLA, DOS RESULTADOS DISTINTOS
  SEGÚN EL MEDIO.** Parece una inconsistencia y no lo es; quien quiera
  «sincronizarlos» está aplicando la regla a medias. Anotado también en el
  propio script (`LINEA`) y en el comentario del hero en `index.html`.
- **`og:image:alt` describía «El cubo de seis caras», y la tarjeta no lleva el
  cubo desde que pasó a ser sólo tipografía.** Además estaba **en castellano**,
  la única cadena así fuera de los `TODO`, y viaja en cada enlace compartido.

Ese último deja un hueco que conviene tener presente: **`og-image.lock.json`
vigila las ENTRADAS de la imagen, no el TEXTO que la describe.** El alt puede
quedar mintiendo sin que ninguna guarda se entere, porque no es una entrada de
la composición. Hoy no hay guarda para eso y no está claro que valga una: la
única regla comprobable sería prohibir la cadena vieja, que caza este caso y
ningún otro.

El piso está fijado en `tools/placeholders-baseline.json`: **bajarlo es progreso,
subirlo es un bug**. Al redactar, correr
`python tools/check-structure.py --actualizar-baseline` para fijar el piso nuevo.
Incluye los `TODO` de `<title>` y `content="…"`, que no llevan `class="todo"`.

Y lo de siempre: **cada texto japonés nuevo obliga a regenerar el subset** de Zen
Kaku, verificando contra la tabla `cmap`. Ya frenó una vez, con el 迷 de la 404.

### Congelados por decisión del autor — no proponerlos

- **Móvil.** Sin medir en dispositivo real (degradación del cubo, el FOV
  horizontal que manda con el escenario más alto que ancho, el maelstrom táctil).
  Se retoma cuando el autor lo diga.

  **Hay dos mediciones de rendimiento y ninguna es de teléfono real**: la de
  escritorio, y la emulación móvil de la vista explotada (2026-08-05,
  `docs/mediciones/explotada-movil-emulada.md`: DPR 1.5 y sin antialias
  verificados EJECUTANDO, cadencia dentro del presupuesto de 60 Hz con CPU
  ×4 — pero la GPU era la de escritorio, así que no levanta este congelado).
  La de escritorio:
  `docs/mediciones/rendimiento.md` (julio de 2026, RTX 4060 Laptop a 165 Hz).
  Ahí sobra margen — la página completa mide lo mismo que no dibujar nada— y el
  único término que aparece es el shader del mar, que evalúa ruido por píxel a
  pantalla completa. **Ese resultado no dice nada de móvil**: el costo escala con
  los píxeles y una GPU de teléfono no tiene ese margen. La media resolución y
  el cap de 25 fps son **precaución, no medición**.

  Y el tercer ejemplo que estaba acá —«el maelstrom táctil sin blur»— **había
  que sacarlo, porque nunca fue cierto**: esa variante definía sus keyframes
  pero no los asignaba, así que en táctil corría la versión con desenfoque. Es
  el aviso más útil de todo este párrafo: una precaución que se documenta y no
  se verifica es indistinguible de una que no existe. La transición está hoy
  reservada; el detalle, en `assets/css/maelstrom.css`.
- **Vista explotada del cubo — YA NO ESTÁ CONGELADA: se construyó y está
  INTEGRADA** (2026-08-05, cinco tandas de calibración con el autor; el
  registro completo está en su sección). El núcleo muestra 産霊 · 河川 · 言霊
  horneados en la textura del cascarón (cube.js) y el clic lleva a
  `/musubi/`, como estaba decidido. La advertencia del subset sigue viva:
  los tres glifos están cubiertos porque viven en la marca de agua de la
  portada (`.about__watermark`) y `言`/`霊` son además el logo del nav —
  **si algún día se toca esa marca de agua, la cobertura de la textura del
  núcleo hay que re-verificarla contra la cmap**. Lo que queda para después
  de publicar es la **v2 (corrientes de agua)**, sólo si el autor la pide —
  no se compensa la ausencia con otro efecto.
- **Remolino ukiyo-e para la transición.** Ocho iteraciones fallidas entre Design
  y Claude: **el ruido procedural produce textura, no dibujo** — granulado, no la
  línea de una ola grabada. Requiere ilustrador humano o un enfoque distinto.
  **No reintentar con los mismos medios.** Y hoy la pregunta ni se plantea: la
  transición entera está **reservada y fuera del lanzamiento**, así que no hay
  nada que ilustrar hasta que se decida retomarla.

### Optimización disponible, decidida como NO — ~79 KB en las fuentes latinas

Los subsets latinos llevan features de OpenType que **el sitio no usa** —`smcp`,
`onum`, `dlig`, `ss01`…—, y con ellas 374 glifos de Inter y 503 de Cormorant.
Verificado: cero `font-feature-settings`, cero `font-variant`, cero `small-caps`
en todo el CSS y el HTML. Quitarlas baja las tres fuentes de **198 KB a 119 KB**.

**Decidido por el autor: no se hace ahora, y el motivo pesa más que el número.**
Esas features son exactamente el tipo de cosa que alguien usa después sin
acordarse de que se sacaron, y un ahorro que se paga con un fallo silencioso
más adelante no es un ahorro. (Decidido antes de publicar; publicado el sitio,
el argumento pesa aún más: el fallo sería en producción.)

**La condición para revisarlo**: si algún día el CSS usa `font-feature-settings`,
`font-variant` o `small-caps`, la optimización deja de estar disponible **y** hay
que regenerar comprobando que la feature concreta sobreviva. El detalle y la
tabla por archivo, en el README.

`liga`, `kern` y `calt` nunca estuvieron en juego: sobreviven al subset por
defecto y son las que el navegador aplica solo.

### Ideas anotadas, sin probar

- **Unabare de fondo en la og:image.** Usar un frame estático del mar,
  oscurecido, detrás de la tipografía. La tarjeta actual es legible pero
  **genérica**; el mar es lo que la haría reconocible como este proyecto y no
  como cualquier sitio financiero serio.
  *(«Unabare» es como el autor llama al shader del mar; el nombre no aparece en
  el código, donde es `background.js` / `#sea`.)*

  Lo que ya está resuelto para intentarlo: `initSea(canvas, reduce, stillTime)`
  dibuja **un solo frame** con `preserveDrawingBuffer: true`, que es justo lo que
  hace falta para poder leer los píxeles del canvas. `STILL_TIME = 12.0` es el
  instante elegido, y el tercer parámetro permite probar otros.

  **El costo a sopesar antes de empezar**: hoy `make-og-image.py` no necesita
  navegador ni servidor, que fue una ventaja explícita de sacar el cubo. Meter el
  mar la devuelve, y además reintroduce `background.js` como entrada de
  `og-image.lock.json`. No es un impedimento, pero es un intercambio, no una
  mejora gratis. Y el texto tiene que seguir leyéndose **a 500 px**: el mar es
  oscuro y de bajo contraste, así que probablemente haga falta oscurecerlo más de
  lo que parece necesario a tamaño completo.

### Depende de que exista `/ja/`

- **hreflang y versión japonesa**: patrón documentado en el README, sin
  implementar. Incluye `<html lang="ja">`, canonical de cada página a sí misma, y
  extender `make-sitemap.py` con `xhtml:link`.

### Cerrados en esta sesión — no reabrir

- ~~Luz a lo largo del arco del péndulo~~ — no había problema. La métrica decía
  «70% del perímetro con ΔL bajo» y era cierto, pero no significaba lo que
  parecía: el cuerpo del cubie (lum ~11.5) es **más oscuro que el fondo** (15.3),
  así que todo perímetro sin iluminar falla por construcción — y un objeto más
  oscuro que su fondo se lee como silueta. Lo que desaparece es ΔL ≈ 0, no ΔL
  chico y consistente. Cerrado por inspección visual, todo en
  `docs/mediciones/luz-arco.md`. **La pregunta era perceptual y binaria: si
  alguien sospecha que el cubo se pierde, se saca una captura, no un barrido.**
- ~~`favicon.ico` 404~~ — hay `.ico` (16/32/48), `.svg` y `apple-touch-icon`,
  generados por `tools/make-favicon.py`. Consola limpia.
- ~~Animación maelstrom~~ — implementada y calibrada dos veces, y después
  **apartada del lanzamiento** por decisión del autor. Reservada en
  `assets/css/maelstrom.css`; ver la decisión cerrada arriba. **Reabrirla es
  post-lanzamiento**, y ahí el punto de partida es el bug de la variante
  táctil, no una recalibración.
- ~~Capa de metadatos~~ — sitemap generado, robots abierto a los crawlers de IA,
  Open Graph completo, 404, y títulos/descriptions únicos verificados por guarda.

---

## Hallazgos de método (para no repetirlos)

Estas equivocaciones ya costaron tiempo. Todas fueron **métricas mal elegidas**
que produjeron conclusiones equivocadas:

- **Ratios de contraste WCAG entre dos navies casi negros**: pasar de 2.27× a
  4.20× eran 3 unidades sRGB sobre 255, invisibles. Medir en **unidades sRGB
  absolutas**, no en ratios.
- **"Brillo de la cara más oscura"**: castiga a los esquemas con más rango, que
  son los buenos. Usar **% de píxeles a menos de 3 unidades del fondo**.
- **Calibrar en una sola pose**: un esquema ganó por maximizar el rango en una
  pose fija, que es justo lo que produce luz inestable al girar. Medir en **2–3
  poses rotadas** y reportar la variación.
- **La cobertura de glifos NO se verifica en el navegador. Ninguna forma
  funciona, y ya se probaron tres.** `document.fonts.check()` da falsos
  positivos: informa si la fuente está cargada, no si contiene el glifo. Medir
  el **ancho** tampoco: los CJK son todos de 1em, así que un glifo presente y
  uno ausente miden exactamente lo mismo. Y comparar los **píxeles** contra un
  fallback tampoco: la cadena de respaldo de `"Zen Kaku", serif` resuelve a una
  fuente distinta de `serif` a secas, así que todo «difiere» y no distingue
  nada. **Verificar contra la tabla `cmap`**, que es la única fuente de verdad.

  Lo que salvó las dos últimas fue **incluir un glifo de control** que se sabe
  ausente (`猫`). Las dos métricas lo dieron como presente, y ahí se ve que
  fallan. **Sin control, las dos habrían pasado por confirmación.** Cuando el
  control se comporta mal, lo que está mal es la métrica, no el sujeto.
- **Leer un canvas WebGL fuera de su frame** devuelve vacío: da falsos negativos.
  Renderizar y leer en el mismo turno, o usar la captura compositada.
- **`Page.captureScreenshot` se cuelga durante una transición entre documentos.**
  El pedido queda esperando y revienta por timeout: no es que salga mal la
  captura, es que no vuelve. Para filmar una view transition hay que usar
  **`Page.startScreencast`**, que empuja cuadros como eventos en vez de
  responder pedidos. Y como los eventos llegan mezclados con las respuestas,
  conviene un hilo lector que consuma todo el socket: interrumpir un `recv()`
  por timeout para sondear deja media trama leída y cuelga lo que sigue.
  Para ver el detalle, `Animation.setPlaybackRate` ralentiza sin tocar el CSS,
  así que lo filmado sigue siendo la animación publicada.
- **En headless el loop del cubo corre a ~7–15 ticks/s, no a 30.** Las pruebas
  de física tienen que esperar **por ticks, no por reloj**.
- **Y las transiciones CSS tampoco siguen el reloj de pared en headless.** Misma
  trampa que la anterior, en otra forma, y muerde a cualquier medición de estado
  animado. Midiendo el folio 1,6 s después del clic dio **5 px de 97**: seguía a
  mitad del despliegue. Con `deviceScaleFactor=2` y dos contextos WebGL el
  compositor se atrasa muchísimo. **Esperar a que la propiedad se estabilice**
  —dos lecturas iguales seguidas— en vez de dormir un rato y dar por hecho que
  terminó. Lo delató que la captura mostraba el folio abierto y la medición
  decía que estaba cerrado: **cuando la captura y la métrica se contradicen, la
  sospechosa es la métrica.**
- **Un test roto se disfraza de bug de la página.** Si el JS de una guarda lanza,
  tiene que reventar el script, no devolver `undefined` en silencio.
- **El estado FINAL es un caso borde, y es el único que nunca se prueba.** El
  baseline de placeholders se leía con `if not base`, que confunde «archivo
  ausente» con «archivo que dice cero». Mientras quedaba un solo placeholder eso
  no se notaba; **al terminar la redacción el baseline legítimo pasó a ser `{}`
  y la guarda se rompió sin que nada estuviera mal**. Sobrevivió a decenas de
  corridas porque funcionaba en todos los estados menos en el último — y a ese
  se llega una sola vez. Cuando un contador puede llegar a cero, **cero tiene
  que ser distinguible de vacío**.
- **DOS GUARDAS DE NAVEGADOR A LA VEZ SE ARRUINAN, y una de las dos puede dar
  VERDE EN FALSO.** Lanzando `check-pendulum` en segundo plano y otra encima, la
  segunda murió con `ConnectionResetError` —se pelean el mismo Chrome— y la
  primera **terminó en 0 diciendo TODO OK**. Pero su número era
  `máx |vel| dentro 0.0000`, cuando lo sano es ~0.11: la ventana de medición
  quedó vacía y la comprobación pasó **por no tener nada que comprobar**.
  El rojo se ve; el verde vacío no. **Correrlas de a una**, y desconfiar de una
  métrica que da exactamente 0 donde antes daba otra cosa — un valor que no se
  parece a los anteriores es motivo de repetir la corrida, aunque el resultado
  sea el que uno quería.
- **Una variante que sólo se LEE no está verificada.** No es una métrica mal
  elegida: es la ausencia de métrica, disfrazada de código presente. La variante
  táctil del maelstrom definía sus keyframes sin blur y **nunca los asignaba**
  —sólo cambiaba `animation-duration`—, así que en teléfono corría la versión
  cara. **El CSS no protesta**: un `@keyframes` que nadie usa es legal y
  silencioso. Por eso la variante «existía» —se la podía leer, citar y
  documentar— y sobrevivió a dos calibraciones y a tres documentos que la daban
  por hecha. El mismo silencio dejó a `kf-fade` definido y sin usar.
  La prueba no es releer el bloque: es medir la propiedad efectiva en el modo
  que se quiere probar. Y el corolario incómodo: **una precaución documentada y
  nunca verificada es indistinguible de una que no existe** — la lista de
  precauciones de móvil tenía tres ítems y uno era falso.
- **«¿Se ve bien?» no mide la cobertura de glifos, porque el fallback de fuentes
  es POR GLIFO.** Un texto al que le faltan glifos en la fuente declarada **se
  dibuja entero igual**: el navegador va a buscar cada glifo ausente a otra
  familia, sin avisar y sin dejar hueco. Medido en la página de mantenimiento:
  `'Zen Kaku', sans-serif` sobre 保守作業中 dio **2 glifos Zen Kaku + 3 Microsoft
  YaHei** — dos tipografías en una palabra, una de ellas china, y a simple vista
  correcto. La métrica que sirve es **`CSS.getPlatformFontsForNode`**, que dice
  qué fuente REAL dibujó cada glifo; la cmap dice qué debería haber pasado, ésta
  dice qué pasó. Es la contracara del hallazgo de arriba: ahí el subset japonés
  se verificaba contra la cmap porque el navegador no sabía; acá el navegador es
  el único que sabe, porque la pregunta es sobre el fallback y no sobre el
  archivo. Y de paso: **`lang="ja"` decide si el genérico cae en una fuente
  japonesa o en una china** (Noto Sans JP con él, Microsoft YaHei sin él).
- **UNA LÍNEA QUE DECLARA HONESTIDAD ES EL PEOR LUGAR PARA UNA AFIRMACIÓN NO
  VERIFICADA.** El colofón de `/method/` ya no existe —se reemplazó por una
  línea de agradecimiento—, pero el criterio que lo redactó vale para lo que
  venga y por eso se guarda acá en vez de perderse con él. Decía *«the code is
  checked by automated guards»* y **no «reviewed by its author»**, porque el
  código no se revisa a mano: lo verifican las guardas que corren antes de cada
  commit. Poner «revisado por el autor» habría sido presumir un proceso que no
  ocurre, **justo en la frase que le pide al lector que confíe** — el error que
  el resto del sitio se prohíbe. Y los tiempos verbales eran parte de la
  afirmación: presente para las guardas, que siguen corriendo; pasado para el
  texto, que ya se revisó. La prueba antes de publicar una línea así es simple:
  **¿qué comprobación respalda cada verbo?** Si alguno no tiene ninguna, sobra.
- **«Regenerar y comparar bytes» parece la guarda perfecta para un artefacto
  generado, y acá no funciona.** El codificador woff2 **no es determinista**:
  tres corridas del mismo comando dan tres `sha1` distintos, y siguen dándolos
  fijando `head.modified` y con `PYTHONHASHSEED=0` — la diferencia arranca en el
  tamaño comprimido, o sea en Brotli. Una guarda así habría estado en rojo desde
  el primer día, que es la señal que uno aprende a ignorar. Lo que sí funciona
  es partir el artefacto: comparar la parte estable (el HTML con los base64
  elididos, verificado estable en tres corridas) y verificar la parte inestable
  por una propiedad y no por sus bytes (la `cmap` de la fuente). **Antes de
  escribir una guarda que compare salidas, correr el generador dos veces.**
- **PARA MEDIR QUE ALGO NO PASA, PRIMERO HAY QUE PROVOCAR EL MOMENTO EN QUE
  PASARÍA.** Buscando si la transición seguía viva, el primer intento clickeó la
  **tarjeta** de una cara y midió «no hubo transición». Era cierto y no
  significaba nada: la tarjeta hace `preventDefault()` —seleccionar y navegar son
  dos actos, navega el botón del folio—, así que **no hubo navegación**, y una
  transición entre documentos no puede ocurrir sin una. Es el mismo verde vacío
  que `máx |vel| dentro 0.0000`: la comprobación pasa por no tener nada que
  comprobar. Lo delató el propio script, que informaba `aterrizó en: /`.
  El segundo intento trajo la trampa opuesta: midiendo `getAnimations()` a 1,2 s
  del aterrizaje daba «nada corriendo», porque **una animación terminada
  desaparece de la lista**. Llegar tarde y no haber nada se ven idénticos. Se
  arregla muestreando desde `t=0` —0/80/250/600/1200 ms—, y ahí sí aparece lo
  que corre. **La pregunta útil no es «¿lo medí?» sino «¿mi medición podía haber
  dado otro resultado?»**
- **CUANDO DOS MEDICIONES SE CONTRADICEN Y LAS DOS ESTÁN BIEN HECHAS, NO ESTÁN
  MIRANDO EL MISMO ARCHIVO.** Yo medía cero reglas de view-transition por seis
  caminos y el autor veía seis en su consola, sobre la misma URL. El reflejo es
  desconfiar de una de las dos; lo que servía era preguntar **qué archivo mira
  cada una**. Servidor y árbol coincidían byte por byte —mismo `sha256`, cero
  ocurrencias— y el navegador tenía una copia anterior a `af7c726`, el commit
  que sacó el maelstrom de `styles.css`. La pregunta productiva no era «¿quién
  se equivoca?» sino «¿qué tendría que ser cierto para que las dos lo sean?».
  Y el corolario práctico: **para diagnosticarlo hace falta el `href` de la
  hoja, no la lista de reglas.** El primer comando que mandé devolvía
  `r.cssText` y por eso no distinguía nada — con las reglas solas, un archivo
  viejo y una regresión se ven idénticos.
- **UN FETCH MIDE LA RED; EL DOM MIDE LA EJECUCIÓN — y pueden estar los dos
  bien y contradecirse.** «`fetch(main.js, {cache:'reload'}) trae el texto
  correcto» convivía con «el DOM muestra el texto viejo», y las dos mediciones
  eran correctas: el fetch va a la red, pero el módulo que ESCRIBIÓ el DOM se
  evaluó una sola vez por documento (module map) y pudo salir de la caché
  heurística — sin `Cache-Control`, Chrome le da el 10% del Last-Modified de
  frescura y el reload normal no revalida subrecursos desde 2017. Para saber
  qué ejecutó, preguntarle a la ejecución: una huella observable de la versión
  (acá: si el hint cambia al alternar el toggle) o
  `performance.getEntriesByType('resource')` con su `transferSize`. Es la
  variante de «no están mirando el mismo archivo» donde el tercer archivo es
  el que corre en memoria.
- **UN FINGERPRINT NUMÉRICO SIN UNIDAD INVENTA ARCHIVOS QUE NO EXISTEN.** Cerrando
  lo anterior propuse distinguir el `styles.css` viejo del vigente por su tamaño,
  y di la referencia en **bytes** (`wc -c` → 47738) para una comprobación que
  corre en la consola y devuelve **caracteres UTF-16**
  (`(await res.text()).length` → 47187). Los 428 caracteres no-ASCII de los
  comentarios en castellano hacen 551 de diferencia, así que el número medido no
  coincidía con ninguna de las dos referencias y **la conclusión razonable pasó a
  ser «hay un tercer archivo»** — con un servidor y un worktree de más que buscar.
  No los había: era el mismo archivo medido con dos instrumentos distintos.
  La regla: **un número de referencia viaja con su unidad y con el comando que lo
  produce**, y si la comprobación va a correr en otro instrumento, la referencia
  se mide con *ése*. Lo delata tener tres números donde deberían ser dos, o una
  diferencia chica y estable que nadie sabe explicar.
  Y un corolario aparte: **el tamaño es un proxy, no la pregunta.** Lo que se
  quería saber era si el archivo trae las reglas, y eso se contesta contando
  `view-transition` en el texto que baja. Un proxy bien elegido igual contesta
  otra cosa.
  La segunda mordida llegó el mismo día, y es la otra mitad de la regla: **un
  fingerprint del archivo VIGENTE caduca con el próximo commit.** El «47187
  caracteres» corregido quedó tabulado como referencia y a las pocas horas ya
  era falso — el commit siguiente agregó comentarios al mismo CSS. La auditoría
  lo cazó antes que un lector. Referencia fija sólo la da lo que no cambia (un
  blob histórico, un conteo estructural); si el número describe el presente,
  hay que escribirle al lado cómo regenerarlo, no su valor.
- **UN GENÉRICO (`serif`, `sans-serif`) EN UN SVG QUE SE RASTERIZA ES UNA FUENTE
  INDETERMINADA.** El archivo se ve distinto según quién lo abra, sin que nada lo
  delate: el genérico resuelve contra las fuentes y la configuración de CADA
  entorno, y todos los renders «se ven bien». Medido el 2026-08-06 en el banner
  de LinkedIn (`kotodama_finance_banner.svg`, fuera del repo): el PNG viejo venía
  de un stack estilo Linux (kanji en Noto Sans JP, título en un gemelo métrico de
  Arial tipo Liberation Sans) y la re-rasterización en Chrome/Windows daba otra
  cosa — y para los kanji era **Microsoft YaHei, una fuente CHINA**, porque el
  `serif` genérico sin `lang` ni siquiera garantiza el idioma (la misma trampa del
  cartel de mantenimiento, en otro medio). El arreglo es doble: **nombrar la
  fuente** (con su gemelo métrico de Linux como fallback, para que el layout no
  se mueva entre entornos) **y dejar `lang="ja"` como red**. La métrica que lo
  decide es `CSS.getPlatformFontsForNode` — la única que dice qué fuente dibujó
  de verdad—; la identificación del render viejo salió de comparar máscaras de
  tinta contra candidatas (IoU 0.843 con Noto Sans JP, la siguiente a 0.68).
  Misma familia que el fallback por glifo y que `hyphens: auto`: se ve correcto,
  nada protesta, y la divergencia sólo aparece si dos entornos comparan sus
  salidas.
- **UNA NOTA FECHADA SOBRE EL ESTADO DE UN TERCERO CADUCA SOLA, Y NADA
  AVISA.** «El dominio viejo aún responde», «el sitio publica X», «la API no
  requiere key»: afirmaciones sobre un tercero que eran ciertas al escribirse
  y que el tercero invalida sin tocar ningún archivo nuestro. Ya son tres
  casos: el comentario del CSS de `.name` (cuando sus reglas eran `a.name`;
  hoy vive junto a `.face-page__body .name`), la nota de webland del catálogo
  («aún responde» — murió del todo, corregida ago 2026 con aprobación del
  autor) y la de tokiorisk (mismo texto, misma muerte — corregida el mismo
  día, también con aprobación). **El número es parte del diagnóstico: TRES
  casos del mismo patrón.** La regla:
  una nota sobre el estado de un tercero lleva FECHA, y al releerla la fecha
  es la advertencia — verificar antes de actuar sobre ella, porque a
  diferencia del código, acá no hay guarda posible: el estado vive en el
  servidor de otro.
- **`hyphens: auto` PUEDE NO HACER NADA, Y NADA LO DELATA.** Los
  diccionarios de partición de Chromium no vienen en el binario: llegan por
  component updater al PERFIL. Un perfil sin el componente —headless con
  perfil fresco, un Chromium embebido, un Chrome recién instalado—
  justifica sin partir una sola palabra, sin error y sin aviso; la
  propiedad computa `auto` igual. Medido el 2026-08-06: los DOS Chromium de
  esta máquina (el headless de las guardas y el del panel) dieron cero
  particiones. La prueba es un glifo de control tipográfico, familia del 猫
  de la cmap: caja de 80px con la palabra «hyphenation» (mide ~114px) — si
  desborda, no hay diccionario; si parte en sílabas, hay. Sin ese control,
  «puse hyphens: auto» pasa por verificado. Corolario de diseño: una página
  con justificado se acepta midiendo el caso SIN partición, porque una
  fracción real de los lectores no la va a tener.
