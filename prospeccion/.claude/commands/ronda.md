---
description: Corre una ronda completa de prospección. Argumento opcional: ciudad o nicho (ej. /ronda dentistas Guadalajara)
argument-hint: [ciudad o nicho opcional]
---
1. Si existe `PAUSA`, anota en `memoria/bitacora.md` que estabas pausado y termina.
2. Lee `CLAUDE.md`, `perfil-cliente.md` y `memoria/`. Calcula el gasto del mes (bitácora) vs. presupuesto. Si ya llegó, detente y repórtalo.
3. Búsqueda de esta ronda: $ARGUMENTS (si está vacío, la siguiente búsqueda no agotada de `perfil-cliente.md` en la primera ciudad pendiente).
4. Lanza el subagente `prospector`; luego `verificador`; luego `redactor`; luego `vigilante`.
5. Agrega a `memoria/ya-contactados.csv` los negocios que ya tienen borrador (no los enviados: enviar lo hace el humano). Agrega línea a `memoria/bitacora.md`.
6. Escribe `reportes/YYYY-MM-DD.md`: rondas, gasto vs presupuesto, leads nuevos, n grado A, top 10 (negocio, ciudad, contacto, por qué), urgentes primero, correos listos con asunto, y lo que se atoró (errores incluidos).
7. NO envíes nada. Cierra con una pregunta: qué apruebo hoy.
