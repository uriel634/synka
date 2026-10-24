# SYNKA · Campaña "¿Cuánto depende de ti tu empresa?"

Plan de 90 días (2 nov 2026 – 31 ene 2027) para posicionar SYNKA y generar solicitudes de diagnóstico.
Este directorio es el paquete de trabajo del equipo de marketing.

> **Aviso sobre los números.** No hay datos históricos de tráfico ni de conversión (GA4 sigue sin configurar).
> Las metas son hipótesis para calibrar en las primeras 4 semanas, no benchmarks.
> Supuestos: presupuesto ≈ 20,000 MXN/mes, mercado México, PyMEs de 5 a 100 colaboradores.

## Archivos

| Archivo | Para qué sirve |
|---|---|
| [`01-medicion-y-setup.md`](01-medicion-y-setup.md) | Lo que bloquea todo: GA4, Search Console, UTM, hoja de leads, aviso de privacidad |
| [`02-linkedin.md`](02-linkedin.md) | Perfil, 12 publicaciones listas y ritmo semanal |
| [`03-outreach.md`](03-outreach.md) | Guiones de LinkedIn y WhatsApp, objeciones, calificación |
| [`04-anuncios.md`](04-anuncios.md) | Meta Ads y Google Ads: segmentación, textos, reglas de apagado |
| [`05-nurture.md`](05-nurture.md) | Secuencia de 4 mensajes después del Radar, por división |
| [`06-alianzas-y-perfiles.md`](06-alianzas-y-perfiles.md) | Perfil de Empresa en Google, alianzas con contadores/abogados/cámaras |
| [`perfiles-instagram.md`](perfiles-instagram.md) | Biografías, enlaces con UTM y limpieza del contenido de la marca anterior en las dos cuentas de Instagram |
| [`guiones-reels.md`](guiones-reels.md) | 7 guiones de reels para grabar en una sola sesión |
| [`calendario/`](calendario/) | **Calendario del mes de lanzamiento:** `semana-1.md` a `semana-4.md` con texto listo para copiar, y un CSV para importar |
| [`visuales/`](visuales/) | **25 imágenes listas para subir** (carruseles 1080×1350): `senales/`, `frases/`, `ventas/` |
| [`automatizacion.md`](automatizacion.md) | Qué se puede programar, cómo, y tu rutina semanal de ≈ 90 minutos |
| [`plantillas/leads.csv`](plantillas/leads.csv) | Encabezados de la hoja de seguimiento de leads (importar en Google Sheets) |

## Diagnóstico: por qué no llegan leads

1. **Nadie sabe que existe SYNKA.** Sin indexación, sin enlaces, dominio nuevo. El plan previo era solo SEO (3–12 meses).
2. **No se mide.** `gtmId` y `ga4Id` vacíos en `js/config.js`.
3. **El Radar no capturaba nada.** Quien terminaba las 21 preguntas veía su resultado y se iba. *(Corregido en código, ver abajo.)*
4. **CTA de alto compromiso.** El botón principal pedía un formulario de 8 campos a un desconocido. *(Corregido: el CTA principal ahora es el Radar.)*
5. **Sin prueba social.** Sin casos, sin LinkedIn de empresa. *(Pendiente: depende de ti, ver `06`.)*
6. **Marca VESTRA anterior** con siete sitios vivos compitiendo. *(Pendiente: ver `seo-audit.md`.)*

## Ya hecho en el sitio (esta rama)

- **Formulario de lead en el resultado del Radar y del Diagnóstico Comercial.** Nombre, empresa, WhatsApp, email y tamaño.
  Envía por Formspree junto con resultado, nivel, división más débil, perfil por eje y atribución.
- **Atribución por canal.** `utm_*`, `gclid`, `fbclid`, referrer y página inicial se guardan en la sesión y viajan en cada lead
  (formulario de la portada incluido).
- **Evento `generate_lead`** en ambos formularios (para marcarlo como evento clave en GA4).
- **CTA principal de la portada = Radar** ("Mide tu dependencia en 5 minutos"); "Solicita tu diagnóstico" queda como enlace secundario.
- **Artículo «7 señales de que tu empresa depende de ti»** (`/blog/senales-empresa-depende-del-dueno`): con portada, resumen,
  7 señales con primer paso cada una, preguntas frecuentes (schema FAQPage), tarjeta en el índice, sitemap, `llms.txt` y enlace desde el artículo hermano.
- **Carruseles, calendario y guiones** de `marketing/` (generados con `tools/gen-carruseles.py` y `tools/gen-calendario.py`).
- **Instagram de SYNKA y de Uriel** declarados en el schema del sitio (`sameAs`).
- **Correo de respaldo unificado** a `contacto@synka.mx` (antes `hola@` en el HTML estático; con JavaScript ya se reescribía desde `config.js`).

Verificado en navegador: Radar completo → formulario → payload con UTM, eventos `formulario_enviado`, `formulario_exito`, `generate_lead`, sin errores de consola; contraste del bloque 12.85:1.

## Pendiente que solo puedes hacer tú (cuentas y decisiones)

| # | Acción | Dónde |
|---|---|---|
| 1 | Crear GA4 y pegar `G-XXXXXXXXXX` | `js/config.js` → `ga4Id` |
| 2 | Verificar `synka.mx` en Search Console y enviar sitemap | `01` |
| 3 | Crear el Perfil de Empresa en Google | `06` |
| 4 | Publicar aviso de privacidad **antes** de cargar GA4 o píxeles | `01` |
| 5 | Crear la página de empresa en LinkedIn y pegar la URL | `js/config.js` → `linkedin` |
| 6 | Confirmar que `contacto@synka.mx` existe y que alguien lo lee a diario | — |
| 7 | Crear cuentas de Meta Ads y Google Ads | `04` |
| 8 | Cambiar las biografías y los enlaces de Instagram, y archivar el contenido de la marca anterior | `perfiles-instagram.md` |
| 9 | Grabar los reels (una sesión de 45–60 min) | `guiones-reels.md` |
| 10 | Programar la primera semana (ver `automatizacion.md`) | `calendario/semana-1.md` |
| 11 | Fusionar la rama y desplegar el sitio **el lunes 9 de noviembre** (el artículo lleva esa fecha) | — |

## Calendario del mes de lanzamiento (detalle en `calendario/`)

| Semana | Foco | LinkedIn (3/sem.) | Instagram | Otros |
|---|---|---|---|---|
| **1 · 9–13 nov** | Lanza el artículo «7 señales» | Carrusel de las 7 señales · prueba de una pregunta · invitación al Radar | SYNKA: carrusel «7 señales» · Uriel: historias + reel R1 | Artículo publicado el lun 9 · Perfil de Empresa en Google |
| **2 · 16–20 nov** | Las 7 frases | Carrusel de frases · «Juan» · el equipo no es el problema | SYNKA: carrusel frases · Uriel: reels R2 y R3 | Perfil de Empresa en Google |
| **3 · 23–27 nov** | Ventas · arranque de anuncios | Carrusel «¿Tus ventas dependen de ti?» · delegar · organigrama real | SYNKA: carrusel ventas · Uriel: reels R4 y R5 | Artículo 2 pendiente de redactar · inicio de Meta y Google Ads |
| **4 · 30 nov–4 dic** | Consolidar y medir | Documentar sin burocracia · lo que hacemos distinto · dependencia vs. sistema | Uriel: reels R6 y R7 | Revisión de las 4 semanas (vie 4 dic) |

Aproximadamente 7–9 piezas por semana. Con la rutina de `automatizacion.md` son ≈ 90 minutos.

### Calendario editorial del blog (un artículo cada 2 semanas, uno por división)

| Cuándo | Artículo | División | Estado |
|---|---|---|---|
| Lun 9 nov | 7 señales de que tu empresa depende de ti | General (pilar) | **Escrito y listo** |
| Lun 23 nov | El organigrama real: quién decide de verdad en tu empresa | Estructura | Pendiente |
| Lun 7 dic | Los 5 números que un dueño debería ver sin preguntar | Control | Pendiente |
| Lun 11 ene | Perfil de puesto y evaluación en una PyME: por dónde empezar | Personas | Pendiente |
| Lun 25 ene | Estándares de servicio que se sostienen sin supervisión | Operación | Pendiente |

*(Corrección: el plan inicial incluía un «artículo de ventas» en la semana 8, pero ese ya existe: `ventas-sin-depender-del-dueno`.)*

## KPIs (hipótesis a 90 días)

| KPI | Meta |
|---|---|
| **Solicitudes de diagnóstico calificadas** (dueño/director, 5–100 colab., México) | 25 |
| Radar + Diagnóstico Comercial completados | 250 |
| Inicio → fin del Radar | ≥ 55 % |
| Costo por diagnóstico completado (pago) | ≤ 150 MXN |
| Costo por solicitud calificada | ≤ 2,000 MXN |
| Clientes cerrados | 3–5 |
| Enlaces entrantes | 10 |

Revisión semanal de 30 min (tráfico, costo por lead, respuestas) y mensual con decisión de presupuesto.

## Presupuesto mensual (≈ 20,000 MXN)

Meta Ads 9,000 · Google Ads 6,000 · Herramientas 1,500 · Producción 0–1,000 · Pruebas 1,500 · Contingencia 1,000.
Si el presupuesto es menor: quitar Google Ads y dejar LinkedIn + outreach + Meta bajo.
