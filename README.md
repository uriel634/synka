# SYNKA — Sitio web

Sitio oficial de SYNKA. HTML estático, sin build, sin dependencias de terceros
en tiempo de ejecución.

La identidad visual **no se rediseñó**. Todo sale del Manual de Identidad SYNKA
v1.0 y del diseño `SYNKA Sitio` incluidos en `_source/`. El registro de qué se
tomó y por qué está en [INVENTARIO-ASSETS.md](INVENTARIO-ASSETS.md).

---

## Ejecutar en local

```bash
python3 -m http.server 4321 --directory synka-web
```

Después, abrir <http://localhost:4321>.

---

## Estructura

```
synka-web/
├── index.html                  Homepage completa
├── soluciones/                 6 landings de división (generadas)
│   ├── estructura.html  comercial.html  procesos.html
│   └── operacion.html   personas.html   control.html
├── css/synka.css               Sistema de interfaz completo, 19 secciones
├── js/
│   ├── config.js               ← ÚNICO archivo a editar para producción
│   └── synka.js                Navegación, diagnóstico, formulario, analítica
├── assets/
│   ├── fonts/                  Archivo variable + IBM Plex Mono, auto-hospedadas
│   ├── logo/                   SVG oficiales sin modificar
│   └── img/                    Favicons, avatar, imagen Open Graph
├── tools/gen-soluciones.py     Genera las 6 landings y el sitemap
├── robots.txt  sitemap.xml  site.webmanifest
├── INVENTARIO-ASSETS.md        Fase 1: inventario y decisiones de marca
└── _source/                    Entregable de identidad original, intacto
```

---

## Antes de publicar

Todo se configura en **`js/config.js`**. No hay credenciales inventadas: los
identificadores están vacíos y el sitio funciona sin ellos.

| Variable | Qué poner | Si se deja vacío |
|---|---|---|
| `correo` | Correo real | Queda el placeholder del manual |
| `telefono` | Formato E.164 | El bloque de teléfono se oculta solo |
| `whatsapp` | Solo dígitos | El botón de WhatsApp no se muestra |
| `linkedin` | URL del perfil | El enlace se oculta |
| `gtmId` / `ga4Id` | ID de contenedor | No se carga ningún script de analítica |
| `endpointFormulario` | URL que recibe el POST | El formulario compone un correo |

Además, buscar y reemplazar en los HTML si el dominio final no es `synka.mx`:
`https://synka.mx` aparece en `canonical`, Open Graph, JSON-LD, `robots.txt` y
`sitemap.xml`. En `tools/gen-soluciones.py` se cambia en la constante `SITIO`.

**Datos que siguen siendo placeholder del manual** y hay que confirmar:
`hola@synka.mx`, `+52 000 000 0000`, `/company/synka`, y `areaServed: México`
en el JSON-LD.

---

## Regenerar las landings de división

Las seis páginas comparten estructura y solo cambian en contenido y color de
rama. Se generan desde un solo sitio para que no puedan divergir:

```bash
python3 synka-web/tools/gen-soluciones.py
```

Editar los textos en el diccionario `DIVISIONES` del script y volver a ejecutar.
El comando también reescribe `sitemap.xml`.

---

## Reglas de marca codificadas

Estas no son decisiones de gusto: salen del manual y están fijadas en el CSS.

- **`border-radius: 0` en todo el sitio y cero sombras.** Regla 7 del manual:
  «sin sombra, degradado, contorno ni volumen». La separación se hace con
  filetes de 1px, nunca con elevación.
- **El brazo superior del isotipo siempre es navy o blanco**; el inferior lleva
  el color. Los SVG en línea copian la geometría oficial sin redibujarla.
- **El rombo central nunca se rellena.**
- **Teal vivo `#00C9B7` solo sobre navy.**
- **El descriptor no aparece por debajo de 24px de alto de logotipo** (regla 9),
  por eso el header muestra solo la palabra.
- Tipografía: Archivo 700 títulos (tracking −2%), 400 texto, 300 divisiones,
  IBM Plex Mono 400 para datos y eyebrows. Sustitución Arial Narrow / Arial,
  como manda el manual. Nunca Helvetica, Inter ni Roboto.

### El fondo claro: gris frío en lugar de arena

El manual fija Arena `#E8E3D9` como fondo de documento (26 % de la paleta), pero
el sitio usa **`#EEF1F4`**, un gris muy claro y frío.

No es una salida de marca: el capítulo 03 admite el isotipo bicolor «sobre
blanco, arena o **gris muy claro**». Se eligió por tres razones concretas:

1. El arena es cálido y tira a beige junto al navy. El gris frío acompaña al
   navy en vez de competir con él, y lee más minimalista.
2. Sube el contraste del acero de **4.41 (que no pasaba AA) a 4.97**. La paleta
   dejó de necesitar excepciones.
3. El retrato de dirección está tomado sobre concreto gris frío. Sobre arena
   desentonaba; sobre este gris se integra.

Como efecto, el texto de párrafo sobre fondo claro pasó de `#3A3730` (un
marrón oscuro) a **navy**. El sitio quedó con dos tintas y nada más, que es lo
que pide el manual: «Navy y teal. Nada más compite.»

Arena sigue definida como token (`--arena`) y reservada para impresión y
documento. El fondo del sitio es `--fondo-claro`.

### Fotografía

Tres imágenes, todas bajo el mismo tratamiento.

| Imagen | Dónde | Origen |
|---|---|---|
| `uriel-520/1040.jpg` | Nosotros | **Real.** Retrato de dirección |
| `estructura-900/1600.jpg` | Fondo del hero | Generada (arquitectura, sin personas ni texto) |
| `documentacion-800/1400.jpg` | Banda en Método | Generada (documentos en retícula) |

**Tratamiento unificado.** Toda foto pasa por `filter: grayscale(1) contrast(1.08)`
más una capa navy en `mix-blend-mode: color`. El resultado es un monocromo de
marca: la fotografía entra en la paleta de dos tintas en vez de introducir un
tercer color, y el conjunto se lee como un sistema y no como un collage. Si
mañana entra una foto nueva, se integra sola.

**El velo del hero está medido, no estimado.** La foto va bajo navy al 88 %.
Muestreando los píxeles reales de la imagen, el gris más claro es 247, lo que
da un fondo de peor caso `rgb(30, 67, 94)`. Sobre él: titular blanco 10.4,
párrafo `#8FB4C9` 4.72, eyebrow teal vivo 4.97. Todo AA, con el promedio real
en 6.04. Si se cambia esa foto por una más clara hay que volver a medir: el
margen del párrafo es de 0.22 puntos.

Las imágenes generadas son **atmosféricas, no documentales**: arquitectura y
materiales, sin personas, sin texto legible y sin nada que pueda leerse como
«este es nuestro equipo» o «este es un cliente». La única fotografía que afirma
algo es el retrato, y es real.

Las dos del hero y de Método se comprimen agresivamente (calidad 34–40) porque
van veladas o en escala de grises: el detalle fino no se percibe.

### Profundidad sin sombras

Para que las secciones no leyeran como bloques planos de color se añadió
`.seccion--signo`: mete el isotipo a gran escala, sangrado por el borde y al
3.5–4.5 % de opacidad. Es la versión monocromática del manual —los dos brazos
unidos en una punta continua—, así que no hay dibujo nuevo, va como data-URI
(cero peticiones) y el logotipo en sí sigue plano, sin sombra ni degradado,
como manda la regla 7.

El retrato de dirección se enmarca en pastilla navy, en línea con la regla 8.

### Tres restricciones de contraste

Auditadas sobre color renderizado, no sobre la teoría. Están comentadas en el CSS:

1. **Acero `#4A6B84` solo sobre fondo claro.** Sobre navy da 2.59:1. El texto
   secundario sobre navy usa `#8FB4C9` (6.62:1), color que ya viene en el
   descriptor del `horizontal-negativo.svg` oficial.
2. **Teal sobre fondo claro es filete, nunca texto** (2.94 sobre blanco, 2.30
   sobre arena). Los eyebrows sobre arena van en navy con filete teal.
3. **Los botones teal llevan texto `#00221C`**, nunca blanco (blanco sobre teal
   da 2.94).

Consecuencia de diseño: la sección de Soluciones va **sobre navy**, porque los
colores de división en su valor claro no alcanzan AA sobre blanco (Procesos
2.94, Personas 3.16). Sobre navy, los seis valores negativos dan entre 4.95 y
6.96.

---

## Método SYNKA: 3 fases y 6 pasos

El manual define el método en **3 fases**; el brief pedía **6 pasos**. El sitio
muestra las dos capas en vez de elegir una:

| Fase del manual | Pasos |
|---|---|
| FASE 01 · Diagnóstico | 01 Diagnosticar |
| FASE 02 · Diseño | 02 Estructurar · 03 Sistematizar |
| FASE 03 · Implementación | 04 Implementar · 05 Controlar · 06 Autonomizar |

---

## Diagnóstico interactivo

Ocho preguntas, tres respuestas (Sí / A veces / No), puntuación de 0 a 16.

Las preguntas 5 a 8 están redactadas en positivo («¿Tus ventas tienen un proceso
definido?»), así que en ellas un «Sí» **resta** dependencia. Eso lo resuelve el
campo `invierte` de cada pregunta en `js/synka.js`. Verificado: todo «Sí» en las
primeras cuatro y todo «No» en las últimas cuatro da 16 (ALTO); el patrón
inverso da 0 (BAJO).

Cada pregunta está mapeada a una división, y el resultado señala **la rama con
más dependencia acumulada**, enlazando a su landing. Si ninguna rama acumula
dependencia, el panel de foco se oculta: no se afirma un hallazgo que no existe.

Umbrales configurables en `config.js` (`umbralMedio`, `umbralAlto`).

---

## Escalera de diagnóstico

Tres instrumentos, tres profundidades. Comparten motor (`js/quiz.js`) y sistema
visual, así que el prospecto nunca sale del sitio ni cambia de experiencia.

| Nivel | Instrumento | Responde | Ruta |
|---|---|---|---|
| 0 · Gancho | Autoevaluación de dependencia · 8 preguntas | ¿Mi empresa depende de mí? | `/#diagnostico` |
| 1 · Mapa | **Radar SYNKA** · 21 preguntas | ¿**Cuál** división es el cuello de botella? | `/diagnostico/radar.html` |
| 2 · Detalle | **Diagnóstico Comercial** · 10 preguntas | ¿**Qué** dentro de esa división? | `/diagnostico/comercial.html` |

Los dos instrumentos nuevos son la reconstrucción nativa de las herramientas que
ya existían en `uriel634.github.io` (Radar Empresarial y Diagnóstico Comercial™).
**Las preguntas, ayudas, opciones y puntajes se conservan literales.** Lo que
cambió es la capa de presentación y, sobre todo, el idioma del resultado.

### El re-corte: de 5 dimensiones a 6 divisiones

El Radar medía Finanzas, Estrategia, Ventas, Talento y Operaciones. Eso no
correspondía a nada comprable: alguien terminaba con "Operaciones 40 %" y no
había a dónde mandarlo. Ahora cada pregunta apunta a una división y el resultado
enlaza a su landing.

| Dimensión original | Preguntas | Se reparte en |
|---|---|---|
| Finanzas | 1–4 | CONTROL |
| Estrategia | 5–8 | ESTRUCTURA (5,6) · CONTROL (7,8) |
| Ventas | 9–13 | COMERCIAL |
| Talento | 14–17 | ESTRUCTURA (14) · OPERACIÓN (15) · PERSONAS (16,17) |
| Operaciones | 18–21 | PROCESOS (18,20) · OPERACIÓN (19,21) |

El mapa vive en `MAPA_RADAR`, dentro de `tools/gen-datos-diagnostico.py`.
Para cambiar a qué división apunta una pregunta se edita ahí y se regenera:

```bash
python3 synka-web/tools/gen-datos-diagnostico.py
python3 synka-web/tools/gen-diagnosticos.py
```

**Dos cosas que conviene saber del re-corte:**

- **"Finanzas" no tiene división propia en SYNKA** y se plegó dentro de CONTROL.
  Es una decisión consciente. Si a futuro hay una división financiera, se
  reasignan esas cuatro preguntas y ya.
- **El reparto quedó desigual**: CONTROL 6 preguntas, COMERCIAL 5, ESTRUCTURA 3,
  OPERACIÓN 3, PERSONAS 2, PROCESOS 2. El resultado se normaliza a porcentaje,
  así que la comparación entre divisiones es válida, pero las de dos preguntas
  son más ruidosas. Lo ideal a futuro es llevar el banco a 3–4 por división.

### Añadir el instrumento de otra división

El motor es genérico. Para construir, por ejemplo, el diagnóstico de SYNKA
PROCESOS: se añade un banco en `gen-datos-diagnostico.py` con la misma forma que
el comercial, se registra el instrumento en `INSTRUMENTOS` dentro de
`gen-diagnosticos.py`, y se regenera. El hexágono, el semáforo, las barras, los
eventos y la accesibilidad ya vienen resueltos.

### Detalles corregidos respecto al original

- **El máximo del Diagnóstico Comercial es 49, no 50.** La pregunta 6 (Cierre)
  tiene 4 puntos como mejor opción, no 5. El motor calcula el máximo en vez de
  declararlo, así que el score es honesto. Si la intención era que fueran 50,
  basta subir esa opción a 5 en `_source/preguntas/comercial.json` y regenerar.
- **Ninguna cifra de autoridad se trasladó.** Las páginas originales declaraban
  "73 % de las empresas quiebran", "+5,000 empresas evaluadas", "200 empresas",
  "+15 años", "+$50M en facturación" y secciones de "Casos de Éxito". Quedaron
  fuera hasta que se verifiquen. Nota: "+5,000 empresas evaluadas" y "más de 200
  empresas" convivían en la misma página y se contradicen.
- **Sin Tailwind, sin Inter, sin emojis.** El manual prohíbe Inter de forma
  explícita. La iconografía son los seis isotipos de división y el rombo.
- **El resultado no inventa hallazgos.** Si ninguna división queda por debajo
  del umbral, no se señala un "punto débil" que no existe.

### Semáforo

Construido con la propia paleta de divisiones, no con colores nuevos: COMERCIAL
para crítico, PERSONAS para irregular, CONTROL para sólido. Los tres pasan AA
sobre navy. Umbrales en `js/quiz.js` (`SEMAFORO`): <40 % crítico, <70 %
irregular, resto sólido.

## Analítica

Capa única en `dataLayer`, compatible con GTM y GA4. Si no hay ID configurado
los eventos se acumulan igual y no se pierde el contrato de medición.

| Evento | Cuándo |
|---|---|
| `cta_clic` | Clic en cualquier CTA (con nombre, sección y texto) |
| `whatsapp_clic` | Clic en un enlace de WhatsApp |
| `scroll_profundidad` | 25 / 50 / 75 / 100 % |
| `diagnostico_iniciado` | Primera respuesta |
| `diagnostico_pregunta` | Cada respuesta |
| `diagnostico_terminado` | Con puntuación, nivel y rama de foco |
| `formulario_enviado` · `formulario_exito` · `formulario_error` | Envío |

---

## Rendimiento

Primera carga completa de la homepage:

| Recurso | gzip |
|---|---|
| `index.html` | 9.2 KB |
| `css/synka.css` | 8.8 KB |
| `js/synka.js` + `config.js` | 6.8 KB |
| Archivo (variable 300–700) | 35 KB |
| IBM Plex Mono 400 | 10 KB |
| **Total** | **≈ 70 KB en 6 peticiones** |

- **Cero peticiones a terceros.** Las fuentes se auto-hospedan; no hay llamada a
  Google Fonts.
- **Cero imágenes en la homepage**: el isotipo va como SVG en línea, lo que
  además permite animar los cuatro brazos por separado.
- Archivo se sirve como **una sola fuente variable** en lugar de cuatro estáticas.

En producción conviene además activar en el servidor: compresión brotli o gzip,
`Cache-Control: public, max-age=31536000, immutable` para `assets/fonts/`, y
HTTP/2.

---

## Movimiento

Solo dos efectos, y los dos explican el concepto de la marca:

1. **Convergencia del isotipo**: los cuatro brazos entran desplazados hacia
   afuera y se alinean, revelando el rombo central. Es literalmente la idea del
   manual: «el centro no está impreso, existe porque las cuatro partes están
   alineadas».
2. **Entrada escalonada** de los elementos de una retícula: partes de un sistema
   que aparecen en secuencia.

Nada decorativo. Todo bajo `IntersectionObserver`, con `unobserve` tras
disparar. `prefers-reduced-motion: reduce` desactiva ambos y deja todo visible.

---

## Accesibilidad

Verificado en navegador sobre color renderizado y geometría real:

- **0 fallos de contraste** en 188 elementos de texto de la homepage, incluido
  el estado con el resultado del diagnóstico visible.
- Un solo `h1` por página, jerarquía de encabezados sin saltos.
- Todos los campos con `label`; los SVG decorativos con `aria-hidden`.
- Objetivos táctiles ≥ 24px (WCAG 2.2 · 2.5.8).
- Menú móvil con `aria-expanded`, cierre con `Escape` y al pulsar un enlace.
- Anillo de foco visible propio, con variante para fondo claro.
- Enlace «saltar al contenido».
- El resultado del diagnóstico se anuncia por `aria-live` y recibe el foco.

---

## Sin JavaScript

El sitio sigue siendo legible y contactable:

- Todo el contenido está en el HTML; nada se inyecta por JS.
- El diagnóstico muestra las ocho preguntas en una lista y remite al formulario.
- Los datos de contacto están visibles junto al formulario.

---

## Qué falta, y por qué no se inventó

- **Casos de éxito.** La sección tiene la estructura completa (problema,
  intervención, resultado, testimonio) con marcadores de «pendiente de
  publicación». No hay clientes, cifras, porcentajes, logotipos ni testimonios
  inventados.
- **Fotografía.** El entregable de identidad no incluye ninguna. El sitio se
  sostiene con tipografía, color y el signo, que es coherente con el territorio
  «coordinación» del manual.
- **Imagen Open Graph.** No existía. Se compuso a 1200 × 630 a partir del PNG
  oficial `horizontal-negativo.png`, que ya trae Archivo real y el área de
  respeto correcta. No se re-tipografió el logo.
