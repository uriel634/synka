# Automatización: qué se puede dejar en piloto automático y qué no

**Objetivo:** que el marketing te quite menos de **90 minutos por semana**.

## Lo que sí puedo hacer y lo que no

| Puedo (ya está hecho) | No puedo |
|---|---|
| Escribir y dejar listos todos los textos, imágenes y calendario | Entrar a tus cuentas (Instagram, LinkedIn, Google, Formspree) |
| Generar las imágenes de los carruseles con la marca | Programar las publicaciones por ti |
| Preparar el CSV para importar en una herramienta | Crear las cuentas de anuncios o de analítica |
| Dejar el sitio midiendo y capturando leads | Responder mensajes o comentarios |

Por tanto, «automatizar» aquí significa: **programar todo en un solo bloque semanal** y que los leads entren solos a una hoja con un aviso. Nada de lo que sigue requiere programar código.

---

## Nivel 1 · Gratis: programar desde las propias plataformas

Es lo más simple y no depende de terceros. Revisa que cada función esté disponible en tu tipo de cuenta.

| Qué | Dónde | Cómo |
|---|---|---|
| Instagram de Uriel y de SYNKA (carruseles, reels, historias) | **Meta Business Suite** (planner) | Cuentas profesionales o de creador, vinculadas. Se programa cada pieza con su texto e imágenes de `calendario/semana-N.md`. Para los reels, invita a `@synkamx` como **colaborador** al programar. |
| LinkedIn de Uriel | Programador nativo de LinkedIn | «Programar publicación» al redactar. Para los carruseles, sube las 9 imágenes en el orden indicado, o conviértelas en un PDF. |
| Perfil de Empresa en Google | El propio perfil | Las publicaciones se pueden programar o publicar a mano (4 en el mes). |
| Primer comentario con el enlace (LinkedIn) | A mano, 30 segundos | LinkedIn no suele permitir programar el comentario. Es la única parte manual diaria. |

**Instagram no admite enlaces en los pies de foto.** Por eso todo remite a «enlace en la bio»: cambia el enlace de la biografía solo cuando el calendario lo indique (ver las notas de cada semana).

## Nivel 2 · Una herramienta para todo (opcional, bajo costo)

Metricool, Buffer, Later o similares permiten ver y programar todos los canales en un solo lugar.

- El archivo `calendario/calendario-publicaciones.csv` trae semana, fecha, hora (CDMX), cuenta, formato, texto, archivos y enlace con UTM, listo para importar o consultar.
- Antes de pagar, **verifica en el plan gratuito de cada una**: número de cuentas, número de publicaciones programadas, soporte de LinkedIn personal y de reels, y si programa el primer comentario.
- Si Meta Business Suite y el programador de LinkedIn te alcanzan, no necesitas este nivel.

## Nivel 3 · Los leads entran solos

Hoy cada solicitud llega por correo desde Formspree. Para que no dependa de que revises el correo:

1. **Filtro en Gmail:** asunto que contenga `Lead radar` o `Solicitud de diagnóstico` → etiqueta «Lead» + marcar importante. Activa la notificación del celular solo para esa etiqueta.
2. **Hoja de seguimiento:** importa `marketing/plantillas/leads.csv` en Google Sheets. Los campos que manda el sitio (`nombre`, `empresa`, `colaboradores`, `whatsapp`, `email`, `resultado`, `mas_debil`, `utm_*`) coinciden con las columnas.
3. **Que la fila se llene sola (opcional):** Formspree puede conectarse con Zapier o Make hacia Google Sheets. Cada envío agrega una fila. Verifica qué integración permite tu plan de Formspree.
4. **Respuesta en menos de 1 hora hábil.** El mensaje 0 de `05-nurture.md` está escrito con variables (`{nombre}`, `{resultado}`, `{mas_debil}`): cópialo, pégalo y envía. Si más adelante quieres automatizarlo, el correo del día 0 es el mejor candidato.

## Lo que NO conviene automatizar

- **Mensajes de outreach en LinkedIn con herramientas de automatización.** Las condiciones de LinkedIn las prohíben y pueden restringir tu cuenta. Los guiones de `03-outreach.md` se envían a mano, 15 por día.
- **Comentarios y mensajes directos de Instagram.** Son tu relación con la audiencia: respóndelos tú.
- **Seguir y dejar de seguir de forma masiva.** Perjudica la cuenta.

---

## Tu rutina semanal (≈ 90 minutos, domingo o lunes)

| Min | Qué |
|---|---|
| 30 | **Grabar 2 reels** de `guiones-reels.md` (si grabas los 7 de un tirón una sola vez, esto se reduce a 0 durante cuatro semanas) |
| 20 | **Programar en Meta Business Suite:** los dos reels (con colaboración), el carrusel de SYNKA y las historias de la semana |
| 15 | **Programar en LinkedIn** las 3 publicaciones de la semana |
| 15 | **Leads:** revisar la hoja, calificar, responder los pendientes |
| 10 | **Números:** GA4 (visitas al Radar y `generate_lead`) y visualizaciones de cada pieza |

Además, 5 minutos al día para el primer comentario de LinkedIn y para responder comentarios.

## Cómo dejar de hacer cosas

Las piezas del calendario las puedo regenerar. Cuando algo funcione, se repite; cuando no, se cambia el texto o la imagen:

- **Cambiar un texto o imagen de carrusel:** se edita `tools/gen-carruseles.py` y se vuelve a ejecutar.
- **Cambiar el calendario:** se edita `tools/gen-calendario.py` y se vuelve a ejecutar.

Pídeme cualquiera de los dos cambios y los hago, o dime «hazme el mes 2» y preparo las 4 semanas siguientes con lo aprendido.
