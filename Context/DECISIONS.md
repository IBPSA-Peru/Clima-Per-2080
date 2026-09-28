# DECISIONS.md

## D-01 · Ubicacion del proyecto
Raiz en `PROJECTS\P2\03_AUDITORIA_CLIMA_Archivos_EPW_Peru\`. Ver SUP-01.
Todas las rutas internas son relativas (SOP-01 §M-WEB y §5).

## D-02 · La descarga se ejecuta en Windows, no en el sandbox
El sandbox del agente no tiene salida a climate.onebuilding.org. Verificado con curl
sobre 4 hosts: solo pypi.org responde. El catalogo si se pudo leer por web_fetch
(modo texto), pero web_fetch devuelve vacio ante un .zip.
Decision: generar `Scripts\DESCARGAR_CLIMA.bat`, que corre en la maquina del usuario.
Alternativas descartadas:
  - Conducir Chrome para bajar los 40 zips: dejaria los archivos en Downloads, fuera
    de las carpetas montadas, y exigiria moverlos uno por uno.
  - Traer los zips en base64 por javascript_tool del navegador: ~600 KB de texto por
    archivo x 40 archivos. Inviable y fragil.
El .bat es idempotente y re-ejecutable, que es lo que pide H1 del SOP-02.

## D-03 · Cinco ventanas TMYx por ciudad, no dos
Ver SUP-04. El analisis de vintage gana potencia estadistica.

## D-04 · Estaciones elegidas para altiplano y costa norte
Juliaca-Manco (847350) y Huanchaco-Pinillos (845010, aeropuerto de Trujillo).
Ver SUP-03. Chiclayo (844520) queda identificado como reserva.

## D-05 · Java
El sandbox trae OpenJDK 11. Future Weather Generator v4.x requiere Java 17. Por tanto
FWG no se ejecutara en el sandbox ni aunque tuviera red: correra en Windows o no correra.
Si no corre, el Paso 3 degrada a "auditoria de lineas base" segun lo previsto en el prompt.

## D-06 · El motor de analisis se escribe y valida ANTES de tener los datos
El Paso 4 no depende de la descarga. Se escribio `Scripts/analizar_epw.py` con un
modo `--autotest` que genera un EPW sintetico de propiedades conocidas (media 20 C,
ciclo diurno de +-5 C, pico a las 15:00-16:00, anos fuente 2010-2021) y comprueba
que el motor las recupera. 8 de 8 comprobaciones pasan.
Asi, cuando lleguen los EPW reales, un resultado raro se atribuye al dato y no al codigo.

Dos comprobaciones fallaron en la primera corrida y AMBAS eran errores del test:
  1. `hora_pico`: el EPW rotula las horas 1..24, donde la etiqueta h cubre el
     intervalo que termina a las h:00. El pico de 15:00-16:00 se rotula 16, no 15.
  2. `gh_enfriamiento_b18`: el EPW guarda el bulbo seco con un decimal. El valor
     esperado hay que calcularlo sobre la serie redondeada. La diferencia era de
     69.6 C-h sobre 23798 C-h, o sea 0.3 % — puro redondeo de formato.
Se corrigio el test, no el motor (SOP-02 B3: el resultado inesperado era el hallazgo).

## D-07 · Autocorrelacion sobre serie constante devuelve NaN, no un numero
En el autotest la media diaria es exactamente constante, asi que la autocorrelacion
no esta definida. El motor devuelve NaN. Es lo correcto: un 0.0 o un 1.0 ahi seria
un dato inventado (SOP-02 A1).

## D-08 · Atipicos detectados en la ventana 2004-2018 de las ciudades andinas
Al comparar cada ventana contra la mediana de su propia ciudad, tres archivos se
apartan y los tres son la MISMA ventana en las TRES ciudades de altura:

| Ciudad | Elevacion | Ventana | Media anual | Mediana de la ciudad | Diferencia |
|---|---|---|---|---|---|
| Arequipa | 2562 m | 2004-2018 | 14.68 C | 13.48 C | +1.20 C |
| Cusco | 3310 m | 2004-2018 | 12.29 C | 9.33 C | +2.96 C |
| Juliaca | 3826 m | 2004-2018 | 7.77 C | 9.39 C | -1.62 C |

Juliaca 2004-2018 ademas trae autocorrelacion de la media diaria 0.377 frente a 0.85
en sus otras cuatro ventanas: no es solo un sesgo de nivel, es otra estructura temporal.
Un patron que aparece en las tres estaciones de altura y en ninguna de la costa apunta
a cobertura METAR pobre en los Andes durante ese periodo, no a clima.

NO se descartan los archivos. Se declaran y se excluye la ventana 2004-2018 de las
ciudades andinas del ajuste del Analisis A, reportando ambos ajustes (con y sin).
Esto va al informe como hallazgo, no como problema a maquillar (SOP-02 B3).

## D-09 · FWG v4.2.0 no tiene bandera SSP: emite los cuatro escenarios de una vez
Verificado ejecutando `java -jar FutureWeatherGenerator_v4.2.0.jar -h` en la maquina
del usuario (log completo en `Context/log_fwg.txt`).

Entorno confirmado, no supuesto:
  - Java 17.0.19 LTS (Microsoft build) en C:\Program Files\Microsoft\jdk-17.0.19.10-hotspot
  - JAR en C:\Users\Usuario\Downloads\FutureWeatherGenerator_v4.2.0.jar, 3 680 843 597 bytes

Las opciones de CLI son: -c / -g / -u como accion; -epw, -epw2; y como opcionales
-output_type, -models, -ensemble, -temp_shift_winter/summer, -smooth_hours,
-output_folder, -model_unzipped_folder, -multithread, -grid_interpolation_method,
-epw_dictionary_limits, -solar_correction, -diffuse_method, -uhi,
-save_epw_comparison, -save_errors_warnings, -save_model_variables.

NO hay `-ssp` ni `-year` ni `-horizon`. El escenario y el horizonte no se piden:
una sola pasada de `-g` emite los 4 SSP (126, 245, 370, 585) x 2 horizontes
(2050, 2080) = 8 archivos de ensemble. Se conservan los 8 porque no cuestan extra;
el analisis usa ssp245 y ssp585 a 2050, que es lo que pide el prompt.

El log dice "Successfully generated MRI_ESM2_0_ssp370_2050.epw (0 KB)" para cada
modelo individual. Eso NO es un fallo: los archivos por modelo no se materializan
cuando `-ensemble=true`. El entregable son los 8 `*_Ensemble_*.epw` de ~1.58 MB.

## D-10 · Los escenarios generados van a Data\, no a Input\
El prompt pide dejarlos en `Input\clima\{ciudad}\`. SOP-01 declara `Input\`
INMUTABLE y de solo lectura, y define M-DATA precisamente para "resultados de
simulacion": salidas de computo costoso, regenerables en teoria y caras en la practica.
Un escenario morfado es exactamente eso.
Se dejan en `Data\escenarios_v1\{ciudad}\` con sufijo de version (G1). Gana el SOP
sobre el prompt porque el usuario instruyo explicitamente seguir los SOP.

## D-11 · Base del morphing: la ventana 2011-2025
El prompt dice "sobre el TMYx de VENTANA RECIENTE" y cita "sufijo tipo TMYx.2009-2023"
como ejemplo de nomenclatura. Se usa 2011-2025, que es la mas reciente disponible.
Motivo: el proyecto entero trata de cuanto sesgo introduce el vintage del archivo.
Morfar desde la base menos envejecida (centroide 2017.6 frente a 2013.8 de 2009-2023)
minimiza justo el artefacto que el Analisis A esta midiendo.

## D-12 · Verificacion fisica del piloto de Lima — PASA
Base: TMYx.2011-2025, T=19.63 C, W=11.65 g/kg, 174 h sobre 26 C, GH_enf_b24=1227 C-h.

| Escenario 2050 | dT (C) | dW (g/kg) | %/K observado | Desvio vs C-C (pp) | Sospechoso |
|---|---|---|---|---|---|
| ssp126 | +1.24 | +1.09 | 7.60 | +1.40 | no |
| ssp245 | +1.51 | +1.36 | 7.73 | +1.53 | no |
| ssp370 | +1.76 | +1.56 | 7.64 | +1.44 | no |
| ssp585 | +1.99 | +1.81 | 7.79 | +1.59 | no |

Los cuatro quedan bajo el umbral de 4 pp. La humedad sigue a la temperatura de forma
consistente con Clausius-Clapeyron.

Estructura temporal preservada, que es lo que debe hacer un morphing (y lo que lo
distingue de una sintesis estocastica):

| Archivo | Autocorr lag1 | Rango diario (C) | Racha calida max (dias) |
|---|---|---|---|
| Base TMYx.2011-2025 | 0.982 | 4.46 | 18 |
| ssp245 2050 | 0.982 | 4.34 | 18 |
| ssp585 2050 | 0.981 | 4.32 | 18 |

Nota para el informe (SOP-02 F1): bajo ssp245 a 2050 las horas sobre 26 C pasan de
174 a 630 al ano. Es un factor de 3.6, pero sobre una base de 174 h, o sea del 2.0 %
al 7.2 % del ano. El multiplicador solo no dice nada util.

## D-13 · Compuerta visual de las figuras (SOP-02 I2 / I3)
Se generaron las 8 figuras y se MIRARON en hoja de contacto. Tres fallaron la
compuerta en la primera revision y se corrigieron; tras la segunda revision, cinco
pasan y tres siguen con defectos. Se agotaron los dos reintentos que permite C1,
asi que se PARA y se reporta lo observado en vez de seguir iterando.

APROBADAS (copiadas a Final Results\figuras\):
  fig2 perfiles mensuales, fig3 delta-T por ciudad, fig5 autocorrelacion y rachas,
  fig6 psicrometrica de Lima, fig8 convergencia de metodos.

NO APROBADAS (se quedan en Temp\renders\, fuera de los entregables):
  fig1 elevacion vs temperatura — las etiquetas de Lima, Piura y Trujillo se
    encabalgan. Las tres estaciones estan entre 32 y 35 m, asi que el rotulado
    inline no cabe por mucho que se desplace. ARREGLO CORRECTO: sustituir los
    rotulos inline por una leyenda lateral, o un inset ampliando la franja 0-100 m.
  fig4 carga de enfriamiento — al mover la leyenda arriba a la izquierda para
    liberar la etiqueta de Arequipa, ahora tapa las de Iquitos (20907/33724) y
    Piura (15873/22352). ARREGLO CORRECTO: leyenda fuera del area de ejes, arriba.
  fig7 vintage — resuelto lo principal (los tres atipicos quedan rotulados y las
    leyendas ya no tapan a Cusco), pero "Arequipa 2007-2021", "Arequipa 2009-2023"
    y "Cusco 2011-2025" siguen pisandose alrededor de x=29-31, y=1.0. ARREGLO
    CORRECTO: rotular solo los tres atipicos de D-08 y omitir el resto.

Ninguno de los tres defectos afecta a un NUMERO. Son fallos de legibilidad, no de
calculo: los valores que grafican salen de Data\analisis_cuatro_v1.json, que esta
verificado. El informe puede citar las cifras aunque la figura no este aprobada.

## D-14 · Tercera pasada de figuras: las tres corregidas
D-13 dejo fig1, fig4 y fig7 sin aprobar tras dos rondas. La tercera pasada NO fue un
reintento del mismo enfoque —eso es lo que C1 prohibe— sino el cambio de diseno que
D-13 ya identificaba como el arreglo correcto:
  fig1: rotulado inline sustituido por leyenda. Tres ciudades entre 32 y 35 m no se
        pueden rotular dentro del grafico; el problema era el metodo, no el offset.
  fig4: leyenda sacada FUERA del area de ejes. Dentro tapaba etiquetas se pusiera
        donde se pusiera: no habia hueco.
  fig7: se rotulan SOLO los tres atipicos de D-08 en vez de todo lo que superaba
        0.9 C. Menos etiquetas, cero encabalgamiento, y destaca el hallazgo.
Revisadas de nuevo: las tres pasan. Las 8 estan en Final Results\figuras\.

## D-15 · Activado M-WEB: visor HTML autocontenido
Procedimiento de SOP-01 §3 seguido en orden:
  1. DECLARAR   M-WEB anadido a MODULOS ACTIVOS e HISTORIAL en P0.md (v1.1.0).
  2. CREAR      Final Results\web\.
  3. BARRIDO    Recorrido Temp\ y Final Results\ buscando archivos servibles mal
                ubicados: NINGUNO. El modulo se activa sobre carpeta limpia, no hay
                migracion pendiente. Las figuras PNG se quedan en figuras\ porque son
                evidencia de verificacion (I4), no producto servible; el visor las
                embebe en base64, no las enlaza.
  4. VERSIONAR  Fila v1.1.0 en el changelog del README.
  5. AGENTE     Bloque M-WEB de SOP-02 aplicable a partir de aqui.

FORMATO: un unico archivo HTML autocontenido, 706 KB. Figuras en base64 y datos como
JSON inline. Sin CDN, sin servidor, sin dependencias: se abre con doble clic, funciona
sin internet y se puede enviar por correo. Verificado que no contiene ninguna URL externa.

FUENTE vs COMPILADO: el HTML es SALIDA DE BUILD. La fuente es Scripts\generar_visor.py.
No se edita a mano; se regenera. Es idempotente (SOP-02 H1).

VERIFICACION (compuerta M-VISUAL I2, parcial):
  - Estructural: los 4 ids que el JS busca existen; el script pasa `node --check`.
  - Funcional sin DOM: ejecutado el JS con un document simulado, produce 8 filas de
    tabla, 8 barras de grafico y 32 puntos de dispersion. Esto descarta el modo de
    fallo tipico —error de JS que deja los contenedores vacios y la pagina a medias.
  - NO se pudo mirar renderizado. La extension de Chrome no abre file://, playwright
    no instala en el sandbox (sin permisos), y el acceso de lectura al navegador de la
    maquina expiro sin respuesta. Dos intentos por via, se para (C1).
  QUEDA PENDIENTE que un humano lo abra y confirme el aspecto visual. El riesgo residual
  es estetico (espaciados, colores), no funcional: el contenido esta verificado.

## D-16 · Rediseno completo del visor: de informe con tabla a piezas interactivas
El primer visor (D-15) era un informe maquetado: tabla ordenable y las 8 figuras PNG
embebidas. Critica del usuario, aceptada: no era interactivo, no habia mapa, y el dato
no se veia transformarse. Se rehizo entero.

QUE CAMBIA
  - CERO imagenes en las escenas interactivas. Todo se dibuja como SVG desde el dato
    en tiempo de carga. El archivo baja de 706 KB a 81 KB pese a tener mas contenido.
  - MAPA de Peru con contorno real (world.geo.json, dominio publico) y las 8 estaciones
    proyectadas por su lat/lon verdadera. Cuatro metricas conmutables; al cambiarlas los
    circulos transicionan de color. Clic en una estacion abre su ficha.
  - NUBE PSICROMETRICA ANIMADA de Lima: 1460 horas del ano interpolando de su posicion
    de hoy a la de 2050 con requestAnimationFrame. Es el dato transformandose, no un
    grafico de antes y despues.
  - Escenas con entrada por IntersectionObserver, navegacion lateral, contadores que
    cuentan, contorno del pais que se dibuja solo, lineas de perfil con stroke-dashoffset.
  - Paleta: fondo casi negro azulado y escala divergente frio->calor. El color codifica
    dato, nunca decora.

DECIDIDO NO USAR FIGMA. El usuario ofrecio conectar una herramienta de diseno. Se
descarto: el conector no esta autenticado, y el entregable es codigo que debe
regenerarse por script. Un mockup habria anadido un paso manual entre el dato y la
pagina, que es justo lo que el proyecto evita.

ARQUITECTURA: plantilla.css + plantilla.js + payload_v1.json, ensamblados por
generar_visor.py. El HTML sigue siendo salida de build; ahora la fuente esta separada
por tipo en vez de vivir en cadenas dentro del generador.

COMPUERTA VISUAL (I2) — esta vez SI se miro. Como no hay navegador disponible, se
extrajo cada escena ejecutando el JS con un DOM simulado en node y se rasterizo con
cairosvg. Tres defectos encontrados y corregidos:
  1. El radio del circulo y su color codificaban LA MISMA variable. Redundante, y
     amontonaba las cuatro estaciones del sur unas sobre otras. Radio fijo, color
     lleva la metrica.
  2. La nube psicrometrica tenia el dominio fijado a mano: un tercio del lienzo vacio.
     Ahora se calcula de los datos de ambos estados, para que el eje no salte durante
     la animacion.
  3. Los rotulos de perfiles mensuales se pisaban (Tacna/Trujillo, Juliaca/Cusco) y en
     el mapa el rotulo de la estacion seleccionada se montaba sobre su propio halo, que
     crece al seleccionarla. Des-colision por barrido vertical y offset medido desde el
     borde del circulo, no desde el centro.
QUEDA PENDIENTE que un humano lo abra: el rasterizado no ejecuta CSS de layout ni las
animaciones, asi que scroll, transiciones y responsive no estan verificados.

## D-17 · Visor v3: la narrativa se invierte y se procesan los horizontes 2030 y 2080
Critica del usuario, aceptada entera: la pagina anteponia el METODO al RESULTADO. Los
KPI de portada decian "40 archivos" y "r2 = 0.13" cuando lo que se busca es una cifra
en grados. Un lector con la pregunta "cuanto va a subir" no la encontraba.

CAMBIO DE ORDEN. Ahora: 01 el dato -> 02 por ciudad -> 03 que implica -> 04 es fiable
-> 05 limites. La discusion de fiabilidad pasa a ser una respuesta a una pregunta ya
planteada, no un preambulo. Se estructura como plegables con veredicto visible
(Si / No / Mas o menos), al estilo del sitio de referencia ai-2040.com.

HORIZONTES. Se procesaron los 32 EPW de 2080 que llevaban generados desde el Paso 3 sin
analizar. El selector ofrece Hoy / 2030 / 2050 / 2080 y al cambiarlo las ocho tarjetas y
el mapa INTERPOLAN al nuevo valor en 900 ms.
  2030 es INTERPOLACION LINEAL entre la linea base y 2050, no salida del modelo: FWG
  v4.2.0 no emite ese horizonte. Marcado como tal en el selector, en un aviso y en el
  CSV. Como el calentamiento no es lineal en el tiempo, ese valor probablemente se queda
  corto. Un numero interpolado sin marcar seria un dato inventado (SOP-02 A1/A2).

TIPOGRAFIA. Pila encabezada por Futura, como pidio el usuario. Futura no es fuente web
ni se puede empotrar sin licencia, asi que la pila cae en 'Century Gothic' —presente en
esta maquina porque tiene Office— que es la geometrica equivalente. En macOS usa Futura
real. Sin CDN de fuentes: el archivo sigue siendo autocontenido.

ICONOS. SVG de trazo, geometricos, en linea. Ninguna dependencia.

PALETA. Se abandona el fondo oscuro por papel calido: es una pieza editorial de lectura
larga, no un panel de control. La escala divergente frio->calor queda reservada a
codificar temperatura.

AUDITORIA DE ACCESIBILIDAD (WCAG 2.1 AA). Contrastes calculados, no estimados a ojo.
Tres fallos encontrados y corregidos bajando SOLO la luminosidad, conservando tono y
saturacion:
  | Uso | Antes | Ratio | Despues | Ratio |
  |---|---|---|---|---|
  | texto terciario y ejes | #7b8595 | 3.31:1 | #656f7e | 4.51:1 |
  | naranja cuando es texto | #e2622f | 3.09:1 | #bd491a | 4.51:1 |
  | borde de control (1.4.11) | #c4bcac | 1.67:1 | #988a6f | 3.00:1 |
El naranja vivo #e2622f se conserva para RELLENOS de dato, donde no aplica el minimo de
texto. Se separo la variable: --calor para relleno, --calor-tx para texto.
Ademas: `prefers-reduced-motion` desactiva todas las animaciones, el tooltip es
aria-live, y los grupos de control llevan role y aria-label.

COMPUERTA VISUAL (I2). Rasterizado de nuevo. Dos defectos hallados y corregidos: el
titulo de la barra de escala del mapa se cortaba contra el borde del viewBox, y la
etiqueta de divergencia se montaba sobre el valor de la barra de FWG (se sustituyo por
una llave con corchetes por encima de ambas barras).

## D-18 · Los tres horizontes en TODAS las proyecciones, y un capitulo de metodo
Peticion del usuario: las proyecciones deben verse a 2030, 2050 y 2080 en todas partes,
no solo en el selector.

ERROR DE ETIQUETA CORREGIDO — el mas grave de esta sesion. La nube psicrometrica decia
"2080 - SSP5-8.5" en su boton y en su indicador de estado, pero los datos que animaba eran
de LIMA_ssp585_2050.epw. Etiqueta incorrecta sobre dato correcto: exactamente el tipo de
fallo que no lanza ningun error y que un lector no puede detectar. Se descubrio al
extender la nube a cuatro estados.
Ahora el payload trae los CUATRO: hoy, 2030 (interpolado punto a punto), 2050 y 2080, y la
animacion los recorre en secuencia con botones para saltar a cualquiera.

ANADIDO
  - Portada: cuatro cifras (hoy / 2030 / 2050 / 2080) en vez de tres, coloreadas por su
    propia temperatura, con la marca "interp." en 2030.
  - Trayectoria por ciudad: linea de la ciudad seleccionada desde su ano centroide hasta
    2080, con los dos escenarios superpuestos y el horizonte activo resaltado. Es la vista
    que faltaba: hace visible que las dos trayectorias se separan a partir de 2050.
  - Capitulo 04 "Como": diagrama de seis pasos —descargar, leer cabecera, medir, morfar,
    comparar, verificar— con iconos de trazo, entrada escalonada y la cifra concreta de
    cada paso. Los capitulos posteriores se renumeraron.

DETALLE TECNICO: los colores del diagrama estaban en `hsl(H S% L%)` (sintaxis CSS Color 4,
sin comas). Los navegadores la leen, pero el rasterizador que uso para la compuerta visual
no, y salian todos negros. Se paso a hex explicito: garantiza el mismo color en cualquier
motor Y permite verificarlo de verdad. Un color que no puedo comprobar es un color que no
puedo aprobar.

REESTRUCTURACION DEL PAYLOAD. Se separo `Scripts/preparar_payload.py` del generador: antes
el payload se armaba dentro de generar_visor.py mezclando extraccion de datos con
maquetacion. Ahora preparar_payload.py -> Data/web/payload_v3.json -> generar_visor.py.
El contorno de Peru se extrajo a Data/web/peru_contorno.json para no llevarlo incrustado
en el codigo.

## D-19 · Climograma mensual, portada animada y capitulo de metodo interactivo
Tres peticiones del usuario en una tanda, todas aceptadas.

1. CLIMOGRAMA MENSUAL. "Es dificil para un peruano entender la temperatura actual si no
hablamos de maximos y minimos." Correcto: una media anual de 19.6 C no se percibe; lo que
se nota es la maxima de febrero y la minima de agosto.
Se anadio al payload, por ciudad / escenario / horizonte:
  - media de las MAXIMAS DIARIAS y de las MINIMAS DIARIAS de cada mes  <- lo que se percibe
  - maximo y minimo ABSOLUTOS del mes                                  <- el record
Se reportan las dos cosas porque no son lo mismo y confundirlas es un error comun.
El grafico superpone la franja de hoy (gris) y la del horizonte activo (color), con flechas
del desplazamiento y rotulos del mes mas calido y mas frio. Lima: la maxima media de febrero
pasa de 27.2 C hoy a 28.6 C en 2050 y 29.2 C en 2080.
Se coloco ARRIBA del capitulo 02, antes del mapa: es la vista que de verdad se entiende.

2. PORTADA. El icono suelto no sostenia la cabecera. Se sustituyo por un mini climograma de
Lima que respira en bucle entre hoy y 2080. Es el mismo dato del capitulo 02 en miniatura:
decorativo en apariencia, informativo de hecho.

3. CAPITULO DE METODO INTERACTIVO. Era un diagrama estatico. Ahora los seis pasos son
clicables y cada uno despliega sus cifras reales: cuantos archivos, que se comprobo, que
salio. El paso 6 muestra los cuatro escenarios con su %/K observado contra el 6.2 teorico.
Fuente unica: la constante PASOS alimenta a la vez las tarjetas y el panel de detalle.

DOS DEFECTOS PROPIOS, HALLADOS EN LA COMPUERTA VISUAL Y CORREGIDOS
  a) El climograma coloreaba cada franja de futuro segun su temperatura, pero la leyenda
     mostraba un unico naranja. Incoherencia: el lector no puede saber que significa el
     verde de julio. Se paso a color unico para el futuro — la POSICION ya codifica la
     temperatura, el color solo separa hoy de futuro.
  b) Las tarjetas del metodo llevaban dos lineas de texto largo que se desbordaban sobre
     las vecinas. Se redujeron a titulo + un dato corto; el detalle vive en el panel.

UN ERROR DE PROGRAMACION QUE HABRIA DEJADO LA PAGINA EN BLANCO
El arranque (`portada(); pintar(); ... metodo();`) habia quedado a mitad del archivo, antes
de la declaracion `let pasoSel`. En JavaScript eso es un ReferenceError por temporal dead
zone: la pagina no habria pintado NADA. No lo detecto ningun linter — lo detecto el arnes
que ejecuta el JS con un DOM simulado en node antes de dar por buena la compilacion.
El arranque se movio al final del archivo, con el motivo escrito en un comentario.
Este es el argumento a favor de esa verificacion: es barata y caza fallos totales.

## D-20 · Climograma con los cuatro horizontes simultaneos; icono de portada restaurado
Correccion de dos decisiones mias equivocadas, ambas señaladas por el usuario.

1. El climograma mostraba SOLO el horizonte activo contra hoy. El usuario queria ver 2030,
2050 y 2080 a la vez, y tiene razon: la gracia de esta vista es la PROGRESION, no la
comparacion de dos estados. Ahora cada mes lleva cuatro franjas —hoy, 2030, 2050, 2080— en
calor creciente, con borde negro en el horizonte activo del selector.
   Lima, febrero: la maxima media pasa de 27.2 C a 29.2 C (+2.0 C de hoy a 2080).
   Iquitos, septiembre: de 32.7 C a 35.8 C (+3.1 C).

2. ELIMINE EL ICONO DE PORTADA CUANDO SE ME PIDIO CAMBIARLO. El usuario dijo que le parecia
atractivo como caratula y que solo queria otro; yo lo borre y lo sustitui por el mini
climograma. Error de lectura de la peticion: "cambialo" no es "quitalo".
Restaurado, ahora animado: nucleo con halo, rayos que giran muy lento (26 s por vuelta) y
una onda inferior en azul frio que oscila. El mini climograma se conserva ademas: no eran
excluyentes.

ERRORES PROPIOS DE ESTA TANDA
  a) Al reescribir el bloque del metodo quedaron DOS definiciones de `metodo()` y dos de
     `const MICO`. En JavaScript la segunda declaracion de un `const` es SyntaxError: la
     pagina no habria cargado. Lo caza el arnes de node, no un linter.
  b) Al deduplicar por indice de texto borre por error la version NUEVA del climograma y
     deje la vieja, que es la que se publico un momento. Se detecto porque el arnes cuenta
     las franjas: esperaba 48 y encontro 12. Un conteo esperado en la verificacion vale mas
     que una inspeccion a ojo.
  c) El rotulo "hoy 27.2°" caia dentro de las barras. Movido encima del valor de 2080 con
     una flecha que los relaciona.

LECCION APUNTADA: editar codigo por reemplazo de subcadena sobre un archivo que ya he
parcheado varias veces produce duplicados silenciosos. Para bloques enteros conviene
localizar por indice de linea y reemplazar el rango completo.

## D-21 · Caratula: el sol de los doce meses
Tercera lectura de la misma peticion, y la correcta. El usuario nunca quiso quitar el sol
grande de entrada: lo queria del MISMO TAMANO pero con otra forma y con interaccion. Mis
dos intentos anteriores fallaron por leer mal: primero lo elimine, luego lo devolvi como
un icono de 26 px en el kicker, que no es una caratula.

SOLUCION: un sol de 440 px hecho con el dato. Doce rayos, uno por mes, cada uno trazado del
radio de la minima media diaria al de la maxima. Parece un sol porque literalmente lo es
—doce radios en torno a un centro— pero la forma la dicta la temperatura, no un icono.
  - Cicla solo entre los cuatro horizontes; el nucleo muestra la media anual y el ano.
  - Cuatro botones para saltar a un horizonte y uno de pausa.
  - Cada rayo responde al cursor: se engorda y muestra su mes con minima y maxima.
  - La escala de radio es COMUN a los cuatro horizontes. Con escala propia por horizonte
    el sol "respiraba" por el eje y no por el dato, que habria sido enganoso.
Lima: el anillo entero se desplaza de 19.7 C (hoy) a 21.9 C (2080) sin cambiar de forma,
que es exactamente lo que dice el analisis — el morphing desplaza, no reestructura.

La portada pasa a dos columnas: texto y cifras a la izquierda, sol a la derecha. En movil
el sol va primero. Las cifras grandes se redujeron de 116 px a 64 px para no competir con el.

DEFECTO CORREGIDO EN LA COMPUERTA: los rotulos de los meses caian justo en el borde del
viewBox y se cortaban ENE, JUL, ABR y OCT. Se amplio el viewBox con margen negativo.

LECCION: tres intentos sobre la misma peticion. Las dos primeras veces cambie el ARTEFACTO
sin releer que se pedia de el. "Cambialo" no era "quitalo" ni "hazlo pequeno": era
"conserva el papel de caratula, cambia la forma, anade interaccion".

## D-22 · Climograma conmutable: la leyenda es el control
La leyenda pasa de decorativa a funcional. Cada horizonte es un boton: clic lo enciende o
lo apaga, doble clic lo aisla, y hay un "Todos". Con UN solo horizonte activo, cada mes
muestra sus cifras de maxima y minima; con varios encendidos no caben y solo se rotula el
mes mas calido.

DOS DECISIONES QUE PARECEN DETALLE Y NO LO SON
  1. El EJE NO CAMBIA al encender o apagar series. Se calcula sobre los cuatro horizontes
     siempre. Si se recalculara con lo visible, las barras se moverian sin que el dato
     haya cambiado, y el lector leeria un cambio que no existe.
  2. NO se puede apagar el ultimo horizonte encendido. Un grafico vacio no informa de nada
     y deja al usuario sin saber que hacer.

Verificado por conteo, no a ojo: 4 activos -> 48 franjas; 2 -> 24; 1 -> 12 franjas y 12
cifras; intentar apagar el ultimo -> siguen 12.

TERCERA VEZ QUE COMETO EL MISMO ERROR DE EDICION
Reemplace el bloque del climograma tomando como limite superior el bloque del metodo,
asumiendo que iba DESPUES. Va antes. El resultado fue `L[:ini] + nuevo + L[fin:]` con
fin < ini, que duplico ~100 lineas: dos `const MICO` y dos `function climograma`. La
segunda declaracion de un `const` es SyntaxError y la pagina no habria cargado.

REGLA QUE ADOPTO A PARTIR DE AQUI: al reemplazar un bloque por indices, comprobar
`assert fin > ini` ANTES de escribir. Es una linea y evita el fallo que ya me ha costado
tres veces. Lo caza el arnes de node, pero conviene no producirlo.

## D-23 · La nube dejaba de decir nada: el color duplicaba el eje X
El usuario pregunto que significan los colores y los puntos de la nube psicrometrica.
La pregunta era el diagnostico: NO SIGNIFICABAN NADA NUEVO. El color codificaba la
temperatura, que es exactamente lo que ya dice la posicion horizontal. Informacion
duplicada ocupando el unico canal libre que quedaba.

CORREGIDO. El color ahora codifica el MES, con un conmutador a HORA DEL DIA. Los dos son
informacion que no estaba en ningun eje, y los dos explican la forma de la nube:
  - Por mes: los de invierno (azules) se agrupan frios y secos a la izquierda; los de
    verano (rojos) calidos y humedos a la derecha. La diagonal ES la estacionalidad.
  - Por hora: aparece el ciclo diurno dentro de cada estacion.
Se anadio leyenda clicable —aislar un mes o una franja horaria— y un parrafo que dice
explicitamente que cada punto es UNA HORA del ano, una de cada seis, y que significa cada
eje. El payload volvio a llevar mes y hora por punto; los habia perdido al reescribirlo.

## D-24 · Climograma: bandas y linea, no barras
Peticion del usuario: linea con umbral mostrando media, maxima y minima; mas grande; con
leyenda que incluya el rango de temperaturas.

Las barras funcionaban para comparar meses sueltos pero rompian la CONTINUIDAD del ano: el
clima no son doce cajas independientes, es una curva. Ahora, por horizonte:
  - banda semitransparente entre la minima y la maxima medias diarias
  - lineas de puntos en el borde de la banda
  - linea solida de 3 px con la media mensual, con punto en cada mes
Tamano de 1160x560 frente a 1080x430.

LEYENDA EN DOS PARTES, porque son dos preguntas distintas:
  1. QUE ES CADA TRAZO: muestras dibujadas de la linea y de la banda, no texto suelto.
  2. RANGO POR HORIZONTE: minima y maxima del ano, en que mes cae cada una, y la amplitud.
     Lima hoy va de 15.2 a 27.2 C con amplitud de 12.0 C; en 2080, de 17.5 a 29.2 C.
Por defecto se encienden solo HOY y 2080: con los cuatro las bandas se solapan y el
contraste que importa —cuanto se mueve el clima— se pierde en la maranha.

Verificado por conteo: 2 horizontes -> 2 poligonos y 2 lineas de media; todos -> 4.

## D-25 · El sol vuelve al tamano de caratula
Al pasar la portada a dos columnas (D-21) el sol quedo encajonado en la columna derecha:
440 px de lienzo dentro de un contenedor de 460, cuando antes ocupaba el ancho del texto.
Se pedia una caratula y quedo un acompanamiento.

  - Lienzo del sol: 440 -> 560 px; radios 64-196 -> 86-252 px; grosor de rayo 17 -> 21 px.
  - Contenedor: 460 -> 660 px de ancho maximo.
  - Rejilla de la portada: la columna del sol pasa de .95fr a 1.18fr, con minimo de 420 px.
  - El `wrap` general de 1140 -> 1240 px para que quepa sin apretar el texto.
  - Tipografia del nucleo proporcional: 26 -> 36 px la cifra.
  - Para compensar, el titular baja de 58 a 50 px y las cifras grandes de 64 a 48. El sol
    manda; el texto acompana. Antes competian.

## D-26 · El sol no se veia: opacity:0 esperando una animacion desactivada
El usuario reportaba que el sol "no carga grande". No era tamano: NO SE PINTABA.

CAUSA. `#heroViz{opacity:0; animation:aparece ... forwards}` combinado con
`@media(prefers-reduced-motion:reduce){*{animation:none!important}}`. Si el sistema
tiene las animaciones desactivadas —muy comun en Windows— la animacion nunca corre y el
elemento se queda en opacity:0 PARA SIEMPRE. Invisible, sin ningun error.

REGLA QUE ADOPTO: ningun contenido arranca en opacity:0 esperando una animacion. Se
anima DESDE 0 con `from{opacity:0}` para que el estado final sea el visible, y la regla
de movimiento reducido incluye un rescate explicito que devuelve opacity:1.

MISMO FALLO, MAS GRAVE, EN LAS SECCIONES. `section{opacity:0}` + clase `.vis` que anade
el IntersectionObserver. Si el JS fallaba en cualquier punto anterior, la pagina entera
quedaba en blanco —y ya me habia pasado dos veces con errores de sintaxis—. Ahora las
secciones son visibles por defecto y la entrada animada solo se activa si el script
llega a poner `<body class="anim">`. Degradacion elegante en vez de pantalla vacia.
Se anadio ademas `aspect-ratio:1/1` al SVG del sol para que reserve el cuadrado.

## D-27 · Datos observados: hasta donde llega este material
El usuario pregunto si hay datos mas antiguos y fehacientes para trazar una curva.
Los hay, y ya estaban en el proyecto sin usar: las CINCO ventanas TMYx de cada ciudad,
cada una situada en su ano centroide. Son datos medidos (METAR ensamblado), con
centroides que van de 1986.9 a 2018.9 segun la ciudad. 40 puntos observados en total.

Se anadieron a la trayectoria, a la izquierda de una linea que marca la frontera entre
medido y proyectado.

LO QUE SE ADVIERTE EN LA PROPIA PAGINA, porque sin esto el grafico enganaria:
las ventanas SE SOLAPAN entre si y cada una es un ano TIPICO compuesto, no una
observacion anual. Suavizan la variabilidad real. Sirven para ver el orden de magnitud
del movimiento observado, no para calcular una tendencia.

Y el contraste que dibujan es informativo por si mismo:
  Lima: las cinco ventanas medidas se separan 0.50 C entre si; la proyeccion sube 2.2 C.
  Iquitos: se separan 0.18 C; la proyeccion sube 2.5 C bajo SSP2-4.5 y 4.5 bajo SSP5-8.5.
Ademas la serie de Lima NO es monotona —1999: 19.28, 2011: 19.78, 2018: 19.63— que es la
misma dispersion sin senal que encontro el Analisis A con r2 de 0.13.

PARA UNA SERIE HISTORICA DE VERDAD haria falta otra fuente: registros de estacion de
SENAMHI o un reanalisis con paso anual. Ninguna es alcanzable desde este entorno.
Queda anotado como el dato que mas mejoraria el trabajo.

## D-28 · Barras clicables
Clic en cualquier barra fija esa ciudad Y ese horizonte a la vez, y arrastra consigo el
mapa, la ficha, el climograma y la trayectoria. La ciudad activa lleva fondo. Se anadio
orden por temperatura, por cuanto sube, por elevacion o por nombre, y bajo cada ciudad
el incremento a 2080 en grados. Ordenar por "cuanto sube" pone a Juliaca primera con
+2.7 C, y por temperatura a Iquitos: el mismo grafico responde dos preguntas distintas.

## D-29 · El sol al tamano de la primera version, texto a un lado
Tercer ajuste del mismo elemento, ahora con la proporcion que se pedia desde el principio:
  - Rejilla de portada: 0.62fr para el texto, 1.38fr para el sol (antes 0.82 / 1.18).
    El sol ocupa cerca de dos tercios del ancho.
  - Lienzo del sol: 560 -> 680 px. Contenedor: 660 -> 860 px. Radios 104-306 px.
    Grosor de rayo 26 px; cifra del nucleo 46 px.
  - El texto se estrecha a 14ch de titular y 40ch de subtitulo, y las cuatro cifras
    pasan a rejilla 2x2 para no estirar la columna izquierda.

## D-30 · Perdida de un archivo por timeout durante la escritura
`Scripts/visor/plantilla.js` quedo en 0 bytes: un heredoc de Python que reescribia el
archivo completo fue cortado por el limite de 45 s del shell A MITAD de la escritura.
El index.html construido antes seguia bien, pero la fuente se habia perdido.
Recuperado de `Backup/20260726_v1_COWORK_Auditoria_completa/Scripts/visor/plantilla.js`,
que estaba a un solo cambio de distancia. El backup por hito de SOP-01 no era burocracia:
fue lo que evito reescribir 580 lineas.

CAMBIO DE METODO: los archivos grandes ya no se reescriben dentro de un heredoc largo.
Se prepara el contenido en /tmp y se copia con `cp` en un comando aparte. Una escritura
interrumpida deja el temporal a medias, no el archivo de trabajo.
