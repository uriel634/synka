---
name: enriquecer-leads
description: Completar huecos de correo/teléfono/redes de un CSV de leads sin inventar datos, marcando origen y confianza.
---
# Enriquecer leads
- Para filas sin correo/teléfono/redes, usa el actor adecuado: crawler del sitio del negocio (página de contacto) o scraper de la red que sí usa. Lotes de 10; estima costo antes del primer lote.
- Agrega columnas `origen_correo` (scraper original | sitio web | red social | no encontrado) y `confianza` (alta = correo en sitio oficial; media = directorio/red; baja = genérico tipo info@/contacto@).
- Sin correo verificable → "sin dato"; sigue en la lista con su teléfono.
- **Prohibido** generar correos por patrón. Prohibido deducir.
- Negocio cerrado/renombrado/sitio inexistente → "descartado" con motivo.
- Cierra con: n alta, n media, n solo teléfono. Aviso: dominios "acepta todo" = dudosos; verificar el correo antes de enviar (rebote < 2 %).
