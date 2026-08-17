# SYNKA — Inventario de assets e identidad

Fase 1 del desarrollo del sitio. Este documento registra **qué existe**, **de dónde sale**
y **qué se reproduce en código**. La fuente de verdad es
`SYNKA Manual de Marca.dc.html` (Manual de Identidad v1.0, 2026).

Origen: `Identidad visual Synka.zip` → descomprimido en `_source/`.

---

## 1. Documentos de marca recibidos

| Archivo | Qué aporta | Rol |
|---|---|---|
| `SYNKA Manual de Marca.dc.html` | Manual de identidad v1.0 completo, 11 capítulos | **Fuente de verdad** |
| `SYNKA Presentación de Marca.dc.html` | Territorio, concepto, símbolo, arquitectura | Estrategia |
| `SYNKA Identidad.dc.html` | Sistema de identidad extendido | Referencia |
| `SYNKA Kit Digital.dc.html` | LinkedIn, firma de correo, favicon | Producción digital |
| `SYNKA Sitio.dc.html` | **Diseño del sitio ya maquetado** | **Dirección de arte web** |
| `logo/LEEME.txt` | Índice de archivos, colores y 10 reglas mínimas | Especificación técnica |
| `firma-correo.html` | Firma de correo en tabla HTML | Producción |

`SYNKA Sitio.dc.html` es la pieza clave: ya define la dirección de arte del sitio
(navy dominante, eyebrows en mono, retícula de 1px, cero radios). El sitio se construye
**a partir de ese diseño**, no de una interpretación nueva.

---

## 2. Logotipo e isotipo

**Símbolo:** Convergencia (3A). Cuatro chevrones idénticos apuntando al mismo punto,
rotados a 0°, 90°, 180° y 270°. Cada brazo está partido por color: superior navy/blanco,
inferior a color.

**Geometría exacta** (retícula 100 × 100, tomada del SVG oficial):

```
polygon superior: 36,50  8,22  8,39  19,50
polygon inferior: 36,50  8,78  8,61  19,50
rotaciones: rotate(90|180|270 50 50)
```

Brazo: 28 unidades a 45°, grosor perpendicular 11.
Rombo central: las puntas se detienen a 14 unidades del centro. **No se rellena nunca.**

| Archivo | Uso |
|---|---|
| `logo/isotipo-bicolor.svg` | Principal. Navy + teal, sobre fondo claro |
| `logo/isotipo-negativo.svg` | Blanco + teal vivo. **Solo sobre navy** |
| `logo/isotipo-mono-negro.svg` | Una tinta, fondo claro |
| `logo/isotipo-mono-blanco.svg` | Una tinta, fondo oscuro no-navy |
| `logo/horizontal-bicolor.svg` | Lockup horizontal con descriptor |
| `logo/horizontal-negativo.svg` | Lockup horizontal sobre navy |
| `logo/horizontal-mono-negro.svg` | Lockup una tinta |
| `logo/vertical-bicolor.svg` | Lockup vertical (espacio más alto que ancho) |
| `logo/favicon-16.svg`, `favicon-32.svg` | Brazo engordado para que el rombo no se cierre |
| `logo/divisiones/isotipo-*.svg` | 6 divisiones, brazo inferior a color |
| `logo/divisiones/isotipo-*-negativo.svg` | 6 divisiones, **obligatorias sobre navy** |

**Advertencia registrada en `LEEME.txt`:** los lockups horizontales y vertical llevan
la palabra SYNKA como *texto vivo* en Archivo. En el sitio esto no es un problema
porque Archivo se sirve auto-hospedada desde `assets/fonts/`.

### Reproducido en código
El isotipo se reproduce **inline como SVG** en el header, el hero y el footer —
no como `<img>`— por tres razones: permite animar los cuatro brazos por separado
(concepto de sincronización), evita cuatro peticiones de red, y hereda `currentColor`
donde conviene. La geometría es copia literal del SVG oficial, sin redibujar.

---

## 3. Color

### Paleta base (manual, cap. 07)

| Token | Hex | Rol | Proporción |
|---|---|---|---|
| Navy | `#002B49` | Estructura. Fondos, títulos, texto principal | 60 % |
| Teal | `#00A99B` | Sincronía. Acento, brazo inferior, filetes | 4 % |
| Teal vivo | `#00C9B7` | **Solo pantalla y solo sobre navy** | — |
| Acero | `#4A6B84` | Texto secundario **sobre fondo claro** | 10 % |
| Arena | `#E8E3D9` | Fondo de documento | 26 % |

### Colores de división (manual, cap. 09)

| División | Sobre fondo claro | Sobre navy (negativo) |
|---|---|---|
| ESTRUCTURA | `#0F6FD1` | `#4FA3F0` |
| COMERCIAL | `#D8552B` | `#F0845B` |
| PROCESOS | `#00A99B` | `#00C9B7` |
| OPERACIÓN | `#6B4EE6` | `#9C86F5` |
| PERSONAS | `#B8892A` | `#D9AC55` |
| CONTROL | `#0E7A66` | `#39C4A6` |

### Valores de interfaz tomados del diseño oficial del sitio

No son colores nuevos: se extraen de `SYNKA Sitio.dc.html` y del descriptor de
`horizontal-negativo.svg`.

| Hex | Uso | Origen |
|---|---|---|
| `#8FB4C9` | Texto secundario **sobre navy** | descriptor del lockup negativo oficial |
| `#123A57` | Filete de 1px sobre navy | `SYNKA Sitio.dc.html` |
| `#3A3730` | Texto de párrafo sobre arena/blanco | `SYNKA Sitio.dc.html` |
| `#00221C` | Texto sobre botón teal | `SYNKA Sitio.dc.html` |
| `#E7E5DE` | Filete de 1px sobre blanco | `SYNKA Sitio.dc.html` |

### Auditoría de contraste WCAG — tres reglas duras

Medido sobre la paleta real. Estas restricciones condicionan el diseño:

| Par | Ratio | Veredicto |
|---|---|---|
| Blanco s/ navy | 14.57 | AA / AAA |
| `#8FB4C9` s/ navy | 6.62 | AA |
| **Acero s/ navy** | **2.59** | **Falla** |
| Teal vivo s/ navy | 6.96 | AA |
| **Teal s/ blanco** | **2.94** | **Falla como texto** |
| **Teal s/ arena** | **2.30** | **Falla como texto** |
| **Blanco s/ teal** | **2.94** | **Falla** |
| `#00221C` s/ teal | 5.74 | AA |
| Navy s/ arena | 11.39 | AA / AAA |
| `#3A3730` s/ arena | 9.28 | AA / AAA |
| Acero s/ blanco | 5.63 | AA |

**Regla 1.** El acero es texto secundario **solo sobre fondo claro**. Sobre navy se usa
`#8FB4C9`.
**Regla 2.** El teal sobre fondo claro es **filete y acento, nunca texto**. Los eyebrows
sobre arena/blanco van en navy, con un filete teal encima.
**Regla 3.** Los botones teal llevan texto `#00221C`, nunca blanco.

Divisiones sobre navy: 4.95 – 6.96, todas AA.
Divisiones sobre blanco: Procesos 2.94 y Personas 3.16 **fallan**.
→ Por eso la sección de Soluciones va sobre navy, tal como en el diseño original.
Sobre fondo claro los colores de división solo aparecen como barra o filete, nunca
como texto.

---

## 4. Tipografía

**Archivo** (Omnibus-Type, Google Fonts) y **IBM Plex Mono**.
Auto-hospedadas en `assets/fonts/` como woff2, subconjunto latin + latin-ext.
Archivo se sirve como **fuente variable 300–700 en un solo archivo** (35 KB).

| Peso | Uso | Tracking |
|---|---|---|
| Archivo 700 | Logotipo (mayúsculas) | +3.5 % |
| Archivo 700 | Títulos | −2 %, interlínea 1.06–1.15 |
| Archivo 400 | Texto | normal |
| Archivo 400 | Descriptor (mayúsculas, acero) | +26 % |
| Archivo 300 | Nombre de división junto a SYNKA 700 | — |
| IBM Plex Mono 400 | Códigos, índices, datos, eyebrows | +.18 a +.2em |

Sustitución declarada por el manual cuando Archivo no carga: **Arial Narrow** en
títulos, **Arial** en texto. Prohibidas Helvetica, Inter y Roboto.
Reproducido en el `font-family` de respaldo.

---

## 5. Reglas mínimas reproducidas en código

De `LEEME.txt` y del capítulo 08 del manual:

1. Área de respeto = ancho del rombo = 14 % del alto del signo, en los cuatro lados.
2. Tamaño mínimo: isotipo 12 px pantalla · lockup horizontal 90 px.
3. Brazo superior siempre navy o blanco. El inferior lleva el color.
4. Rotación solo en múltiplos de 90°.
5. No cerrar ni rellenar el rombo central.
6. No alterar grosores ni separar los chevrones.
7. **Sin sombra, degradado, contorno ni volumen** → el sitio usa **`border-radius: 0`
   en todo** y no lleva ni una sombra. Separación por filetes de 1px, no por elevación.
8. Sobre fotografía, solo sobre pastilla navy sólida.
9. El descriptor no se usa por debajo de 24 px de altura de logotipo.
10. Teal vivo solo en pantalla y solo sobre navy.

---

## 6. Imágenes y piezas

| Archivo | Estado |
|---|---|
| `png/favicon-16/32/64.png` | Copiado a `assets/img/` |
| `png/isotipo-bicolor-512.png` | Copiado — Open Graph de respaldo |
| `png/avatar-1024.png` | Copiado — icono de app / maskable |
| `png/horizontal-*.png`, `vertical-bicolor.png` | Disponibles en `_source/`, no requeridos en web |
| `png/linkedin-portada-1584x396.png` | Pieza social, fuera del alcance del sitio |
| `uploads/Gemini_Generated_Image_.jpeg` | Imagen suelta sin rol declarado en el manual. **No se usa** |

**Faltantes reales, no inventados:**

- No hay **fotografía** de marca. El sitio se construye sin fotos: tipografía,
  color y el signo. Es coherente con el territorio "coordinación" del manual.
- No hay **imagen Open Graph** diseñada (1200 × 630). Se genera una a partir del
  lockup oficial sobre navy, sin alterar el logo.
- No hay **casos de éxito, cifras, testimonios ni logos de cliente**. Van como
  placeholder declarado. No se inventa ninguno.
- Datos de contacto en el manual son placeholder: `hola@synka.mx`,
  `+52 000 000 0000`, `/company/synka`. Se dejan como variables de configuración.

---

## 7. Contradicción detectada entre el prompt y el manual

El prompt pide un **Método SYNKA de 6 pasos**
(Diagnosticar · Estructurar · Sistematizar · Implementar · Controlar · Autonomizar).
El manual, en el capítulo 11, define el **Método SYNKA en 3 fases**
(Diagnóstico · Diseño · Implementación).

Por la regla 23 el manual manda. Resolución adoptada: se conservan **las 3 fases del
manual como estructura** y los **6 pasos del prompt como el detalle dentro de ellas**.

| Fase del manual | Pasos del prompt |
|---|---|
| FASE 01 · Diagnóstico | 01 Diagnosticar |
| FASE 02 · Diseño | 02 Estructurar · 03 Sistematizar |
| FASE 03 · Implementación | 04 Implementar · 05 Controlar · 06 Autonomizar |

Ninguna de las dos versiones se contradice: el sitio muestra las dos capas.
