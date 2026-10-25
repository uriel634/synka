# 01 · Medición y configuración

Sin esto no se lanza ningún anuncio. Tiempo estimado: 2–3 horas.

## 1. Google Analytics 4

1. Crear propiedad en analytics.google.com → flujo de datos web → `https://synka.mx`.
2. Copiar el ID de medición (`G-XXXXXXXXXX`) y pegarlo en `js/config.js`:
   ```js
   ga4Id: 'G-XXXXXXXXXX',
   ```
3. Publicar. El sitio ya emite todos los eventos; con el ID empiezan a contarse.
4. En **Administrar → Eventos**, marcar como **evento clave**: `generate_lead`.
5. En **Administrar → Definiciones personalizadas**, crear dimensiones de evento:
   `origen`, `nivel`, `mas_debil`, `utm_source`, `utm_campaign`, `instrumento`.

### Eventos que el sitio ya emite

| Evento | Cuándo | Parámetros útiles |
|---|---|---|
| `cta_clic` | Clic en cualquier botón con `data-cta` | `cta`, `seccion` |
| `whatsapp_clic` | Clic al WhatsApp | `destino` |
| `scroll_profundidad` | 25/50/75/90 % | `porcentaje` |
| `diagnostico_iniciado` | Primera respuesta | `instrumento` |
| `diagnostico_pregunta` | Cada pregunta | `pregunta`, `puntos` |
| `diagnostico_terminado` | Pantalla de resultado | `nivel`, `porcentaje`, `mas_debil`, `eje_*` |
| `formulario_enviado` | Intento de envío | `origen`, `colaboradores` |
| `formulario_exito` | Formspree respondió OK | `origen` |
| `formulario_error` | Validación o fallo | `motivo`, `origen` |
| **`generate_lead`** | Lead capturado (**evento clave**) | `origen`, `nivel`, `mas_debil`, `utm_source`, `utm_campaign` |

### Exploración de embudo (crear en GA4 → Explorar)

`page_view /diagnostico/radar` → `diagnostico_iniciado` → `diagnostico_terminado` → `generate_lead`

Lectura: si cae entre 1 y 2, el problema es la promesa o la primera pregunta; entre 2 y 3, la longitud (21 preguntas);
entre 3 y 4, el formulario o la oferta de la sesión.

## 2. Google Search Console

1. search.google.com/search-console → **Dominio** → `synka.mx`.
2. Verificar con registro TXT en Cloudflare DNS (≈ 2 minutos).
3. **Sitemaps** → enviar `https://synka.mx/sitemap.xml`.
4. **Inspección de URL** → solicitar indexación de: portada, `/diagnostico/radar`, `/diagnostico/comercial`, `/blog/` y los 4 artículos.
5. Revisar semanalmente: páginas indexadas, consultas, errores.

> El `sitemap.xml` ya incluye `/blog/` y los 4 artículos (14 URLs en total).

## 3. Convención de UTM

Todos los enlaces que se publiquen o se envíen llevan UTM. Formato: minúsculas, sin espacios, guiones.

`https://synka.mx/diagnostico/radar?utm_source={fuente}&utm_medium={medio}&utm_campaign={campaña}&utm_content={pieza}`

| Canal | utm_source | utm_medium | utm_campaign (ejemplo) |
|---|---|---|---|
| Publicación LinkedIn | `linkedin` | `social` | `radar-nov26` |
| Mensaje directo LinkedIn | `linkedin` | `outreach` | `radar-nov26` |
| WhatsApp | `whatsapp` | `outreach` | `radar-nov26` |
| Meta Ads | `meta` | `paid` | `radar-nov26` |
| Google Ads | `google` | `cpc` | `radar-nov26` |
| Correo / nurture | `correo` | `email` | `nurture-radar` |
| Alianzas | `alianza-{nombre}` | `referral` | `alianzas-nov26` |
| Perfil de Empresa en Google | `google` | `organic` | `gbp` |

`utm_content` identifica la pieza (`post-07`, `anuncio-dolor-a`, `guion-1`).
El sitio guarda estos parámetros al entrar y los manda con el lead, así que **cada solicitud en Formspree dice qué canal la trajo**.

## 4. Hoja de seguimiento de leads

Hasta que haya CRM, una hoja de cálculo. Columnas:

`fecha · nombre · empresa · colaboradores · whatsapp · email · origen (formulario) · instrumento · resultado · mas_debil · utm_source · utm_campaign · utm_content · calificado (sí/no) · motivo si no · primer contacto · diagnóstico agendado · propuesta · cierre · monto · notas`

**Calificado** = dueño o dirección, 5–100 colaboradores, México, problema real de dependencia.
Registrar el **motivo de descarte**: es la mejor información para ajustar la segmentación de anuncios.

## 5. Aviso de privacidad (pendiente, antes de cargar analítica o píxeles)

El sitio recoge nombre, WhatsApp y correo, y los formularios dicen "usamos tus datos únicamente para contactarte". Al activar GA4 o píxeles de Meta/Google se añaden datos de navegación.
Antes de gastar en anuncios:

- Publicar una página de **aviso de privacidad** (responsable, finalidades, cómo ejercer derechos ARCO, contacto) y enlazarla en el pie y junto a los formularios.
- Valorar un aviso de cookies para analítica y publicidad.

No es asesoría legal: conviene que lo revise quien lleve lo jurídico de SYNKA.

## 6. Formspree

- El correo de cada lead llega con asunto `Lead radar — {empresa} ({resultado})` o `Solicitud de diagnóstico — {empresa}`.
- Crear una regla en el correo para etiquetar `Lead`, y que el celular avise.
- **Regla de oro: contestar en menos de 1 hora hábil.** El contacto en la primera hora es el factor que más mueve la conversión de leads fríos.
- Revisar el plan de Formspree: límite de envíos mensuales y exportación a hoja de cálculo.

## 7. Tags de anuncios (después de lo anterior)

Vía Google Tag Manager (`gtmId` en `config.js`): píxel de Meta y etiqueta de conversión de Google Ads, ambos disparados por el evento `generate_lead`.
