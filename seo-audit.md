# SYNKA — Auditoría SEO

Fecha: 2026-08-16 · Sitio auditado en vivo (`synka.mx` / `zynka.pages.dev`)

Todo lo de aquí está **medido sobre el sitio publicado**, no estimado. Los
comandos usados quedan indicados para poder repetir la medición.

---

## Resumen

| Capa | Estado |
|---|---|
| SEO técnico on-page | **Sólido.** Títulos, meta, encabezados, canonical, schema y velocidad, correctos |
| Configuración de servidor | **2 fallos reales.** Soft-404 y caché desactivada |
| Indexación | **Cero.** Google todavía no sabe que el sitio existe |
| Autoridad | **Cero.** Dominio nuevo, sin enlaces entrantes |
| Contenido | **Insuficiente** para las búsquedas objetivo. 9 páginas, todas comerciales |

**Diagnóstico en una línea:** la base técnica está bien construida y evita
perder posiciones por errores, pero no gana ninguna. Lo que falta no es
optimización: es indexación, contenido y enlaces.

---

## 1 · Lo que ya está bien

Medido página por página en las 9 URLs publicadas:

| Comprobación | Resultado |
|---|---|
| Títulos únicos | 9/9, entre 54 y 63 caracteres |
| Meta descripciones únicas | 9/9, entre 143 y 160 caracteres |
| Un solo `h1` por página | 9/9 |
| Jerarquía de encabezados sin saltos | Verificado |
| Canonical correcto y sin redirección | 9/9, apuntan a `synka.mx` sin `.html` |
| Duplicados de título o descripción | Ninguno |
| `sitemap.xml` | 9 URLs, válido, referenciado en `robots.txt` |
| `robots.txt` | Permite el rastreo completo |
| Schema.org | Organization, ProfessionalService, WebSite, Service, BreadcrumbList, WebApplication |
| `lang="es-MX"` | Presente |
| HTTPS | Activo, certificado de Cloudflare |
| Peso de carga | 99 KB móvil / 139 KB escritorio, cero terceros |
| Responsive | Auditado en 360, 768, 1024 y 1440 px |
| Accesibilidad | 0 fallos de contraste sobre color renderizado |

Sobre la velocidad: no hay una sola petición a dominios externos. Las
tipografías se auto-hospedan y el isotipo va como SVG en línea. Eso es una
ventaja real y poco común frente a la competencia del sector.

---

## 2 · Fallos reales encontrados

### 2.1 · Soft-404 — **prioridad alta**

Cualquier URL inexistente devuelve **HTTP 200** y sirve la portada.

```bash
curl -s -o /dev/null -w "%{http_code}" https://synka.mx/no-existe-esta-pagina
# devuelve 200, debería devolver 404
```

**Por qué importa.** Google interpreta que cada dirección inventada es una
página real con contenido duplicado de la portada. Con el tiempo eso diluye la
señal del dominio y desperdicia presupuesto de rastreo. Es el problema técnico
más serio del sitio.

**Corrección:** añadir `404.html` en la raíz. Cloudflare Pages lo sirve
automáticamente con el código 404 correcto.

### 2.2 · Caché desactivada en todos los recursos — **prioridad alta**

```
cache-control: public, max-age=0, must-revalidate
```

Esa cabecera aplica igual al HTML que a las tipografías, el CSS y las imágenes.
Cada visita revalida **todos** los archivos contra el servidor, incluidas las
fuentes de 35 KB que no cambian nunca.

**Por qué importa.** Afecta directamente a las Core Web Vitals, que son factor
de posicionamiento. La segunda visita de un usuario debería ser casi
instantánea y hoy no lo es.

**Corrección:** archivo `_headers` con caché larga para `assets/` y corta para
el HTML.

### 2.3 · Metadatos sociales incompletos — prioridad media

- `og:image:alt` solo está en la portada; falta en las otras 8 páginas
- `twitter:image:alt` no está en ninguna

No afecta al posicionamiento, pero sí a la accesibilidad de las tarjetas al
compartir enlaces, que es justo lo que va a pasar con los diagnósticos.

### 2.4 · Datos de contacto ausentes del schema — prioridad media

El bloque `Organization` declara nombre, logo, descripción y eslogan, pero no
`contactPoint` ni `sameAs`. Ahora que existen correo y teléfono reales,
conviene declararlos: es lo que alimenta el panel de conocimiento de Google.

### 2.5 · Cabeceras de seguridad mínimas — prioridad baja

Solo está `referrer-policy`. Faltan `strict-transport-security`,
`x-frame-options` y `permissions-policy`. No es un factor de posicionamiento
directo, pero sí de confianza y se resuelve en el mismo archivo `_headers`.

---

## 3 · El problema de fondo: nadie sabe que existes

El sitio se publicó hoy. **Google no lo ha rastreado.** No está indexado y no
aparece en ninguna búsqueda, y eso no se arregla con optimización on-page.

Además, `synka.mx` es un dominio **nuevo, sin historial ni un solo enlace
entrante**. En SEO la autoridad se acumula con el tiempo y con enlaces de otros
sitios. Hoy ese contador está en cero.

### Las tres acciones que sí desbloquean

**1 · Google Search Console.** Verificar el dominio y enviar el sitemap. Es lo
único verdaderamente urgente: pasa el rastreo de meses a días. Como el DNS está
en Cloudflare, la verificación por registro TXT toma dos minutos.

**2 · Perfil de Empresa en Google.** Gratis. Para búsquedas del tipo
«consultor de procesos [ciudad]» pesa más que cualquier ajuste on-page, y
muchas PyMEs buscan exactamente así.

**3 · Resolver la herencia de VESTRA.** Hay **siete sitios vivos** en GitHub
Pages con contenido parecido, de la misma autoría:

| Repositorio | Qué hacer |
|---|---|
| `radar-empresarial`, `diagnostico-comercial` | Redirigir — las redirecciones ya están preparadas en `redirecciones-vestra/` |
| `radarempresarial` | Parece duplicado de `radar-empresarial`: dos versiones vivas de la misma herramienta compitiendo entre sí |
| `radarventas`, `prediagnostico`, `Vestraleads` | Triar: si son VESTRA, entran al retiro |
| `crm-interlomas` | **No tocar** sin confirmar. Parece herramienta viva de un cliente |

Mientras esos sitios sigan arriba, compiten contra `synka.mx` por las mismas
búsquedas y mandan tráfico a una marca que ya no se usa.

---

## 4 · Contenido: la brecha más grande

Volumen de texto medido:

| Página | Palabras |
|---|---|
| Portada | ~1,610 |
| Landings de división | 430 – 500 |
| Diagnósticos | 430 – 480 |

Para páginas de servicio, 500 palabras es aceptable. El problema no es el
volumen: es **el tipo de página**.

Las palabras objetivo declaradas —«estandarización de procesos»,
«profesionalización de empresas», «procesos empresariales»— son **búsquedas
informativas**. Quien las teclea está aprendiendo, no comprando. Esas
posiciones no se ganan con páginas de servicio; se ganan con artículos que
respondan la pregunta.

Hoy el sitio tiene 9 páginas y las 9 son comerciales. Falta por completo la
capa que atrae a quien todavía no sabe que necesita a SYNKA.

**A favor:** los dos diagnósticos son exactamente el tipo de herramienta que la
gente enlaza y comparte. Los enlaces entrantes son lo que le falta al dominio,
y esas dos páginas son el activo con más probabilidad de conseguirlos.

---

## 5 · Expectativa realista

| Plazo | Qué esperar |
|---|---|
| 2 – 4 semanas | Aparecer al buscar «SYNKA» (búsqueda de marca) |
| 3 – 6 meses | Cola larga: frases específicas y poco competidas |
| 12+ meses | Términos de cabeza como «consultoría empresarial», solo con contenido sostenido |

Cualquiera que prometa plazos más cortos para un dominio nuevo en este sector
está exagerando.

---

## 6 · Plan por orden de impacto

### Correcciones rápidas — se implementan en código

- [ ] `404.html` para eliminar el soft-404
- [ ] `_headers` con caché larga en assets y cabeceras de seguridad
- [ ] `og:image:alt` y `twitter:image:alt` en las 8 páginas generadas
- [ ] `contactPoint` en el schema de Organization

### Esta semana — requieren cuentas del cliente

- [ ] Verificar `synka.mx` en Google Search Console y enviar el sitemap
- [ ] Crear el Perfil de Empresa en Google
- [ ] Configurar GA4 y pegar el ID en `js/config.js`
- [ ] Desplegar las redirecciones de VESTRA
- [ ] Triar los otros cinco repositorios con GitHub Pages activo

### Siguientes meses — trabajo sostenido

- [ ] Arquitectura de contenidos: un artículo por división, atacando la
      búsqueda informativa que le corresponde
- [ ] Conseguir los primeros enlaces: directorios sectoriales, cámaras,
      colaboraciones, difusión de los diagnósticos
- [ ] Publicar casos reales cuando haya autorización del cliente
- [ ] Completar `linkedin` en `js/config.js` y añadirlo como `sameAs`

---

## 7 · Cómo repetir esta auditoría

```bash
# Soft-404
curl -s -o /dev/null -w "%{http_code}\n" https://synka.mx/url-inexistente

# Caché de un recurso estático
curl -sI https://synka.mx/assets/fonts/archivo-var-latin.woff2 | grep -i cache

# Títulos y descripciones de todas las páginas
for p in "" soluciones/estructura soluciones/comercial soluciones/procesos \
         soluciones/operacion soluciones/personas soluciones/control \
         diagnostico/radar diagnostico/comercial; do
  curl -s "https://synka.mx/$p" | grep -o "<title>[^<]*</title>"
done
```
