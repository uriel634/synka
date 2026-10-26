---
name: sacar-leads
description: Cómo sacar leads con actores de Apify: elegir actor, estimar costo, guardar CSV sin repetir contactos.
---
# Sacar leads
1. Lee `perfil-cliente.md` y `CLAUDE.md` (presupuesto, tope, ciudad).
2. Elige el actor. Negocios locales: `compass/crawler-google-places` (~$4/1,000), o `lukaskrivka/google-maps-with-contact-details` (~$5/1,000, busca correo en el sitio). B2B: `harvestapi/linkedin-company-employees` (~$3/1,000). Personas: `harvestapi/linkedin-profile-search`. Facebook (`apify/facebook-page-contact-information`, ~$13/1,000) solo con filtro fino.
3. **Antes de correr:** di el actor, los parámetros exactos y el costo estimado. Si supera el tope de la ronda o el presupuesto restante del mes (suma `memoria/bitacora.md`), detente.
4. Primera búsqueda de una zona/nicho nuevo: corre solo 10 como prueba. Si < 7 de 10 califican, corrige la búsqueda.
5. Guarda en `leads/YYYY-MM-DD.csv` (nunca sobrescribas; si existe, usa sufijo `-2`) con columnas exactas:
`negocio | contacto | puesto | telefono | correo | sitio_web | instagram | linkedin | ciudad | rating | resenas | senal_de_calificacion | fuente | fecha`
6. Dato ausente = "sin dato". `fuente` = actor exacto. `senal_de_calificacion` = razón concreta según el perfil.
7. Omite todo negocio presente en cualquier CSV de `leads/` o en `memoria/`.
8. Reporta: cuántos traen teléfono, correo y ambos; y si la cosecha sirve.
