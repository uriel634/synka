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

## Calendario (resumen)

| Semana | Acción | Canal |
|---|---|---|
| 0 · 2–8 nov | Pendientes 1–6 de arriba | Técnico |
| 1 | LinkedIn de Uriel y de la empresa; banco de 12 posts; primeros 5 contactos/día | LinkedIn |
| 2 | Revisar flujo del Radar con GA4 en vivo; primeras 3 publicaciones | Sitio, LinkedIn |
| 3 | Lanzar Meta y Google con presupuesto de prueba; outreach 15/día | Pago, outreach |
| 4 | Retirar o redirigir sitios VESTRA; primeras reuniones de alianza | Técnico, alianzas |
| 5 | Artículo "7 señales de que tu empresa depende de ti" | Blog |
| 6 | Primeros 2 diagnósticos con testimonio | Ventas |
| 7 | Optimización: apagar el 50 % peor de anuncios | Pago |
| 8 | Webinar de 40 min + artículo de ventas | Webinar, blog |
| 9–10 | Publicar caso 1; enviar el Radar a la base de contactos | Todos |
| 11 | Artículo de división | Blog |
| 12 | Informe de resultados y decisión de escalar | Interno |

Deja ~20 % del calendario libre para oportunidades.

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
