# Cómo frenar o apagar el agente

**Pausa (reversible):** crea un archivo vacío llamado `PAUSA` en esta carpeta (`touch PAUSA`). Bórralo para reanudar.

**Tope de gasto:** el agente se detiene solo al llegar al presupuesto mensual de `CLAUDE.md` y lo reporta. Sube/baja el número ahí.

**Apagar la tarea programada (macOS):**
```
launchctl unload ~/Library/LaunchAgents/com.synka.prospeccion.plist
rm ~/Library/LaunchAgents/com.synka.prospeccion.plist
launchctl list | grep synka     # no debe mostrar nada
```
**Cambiar día/hora:** edita `Weekday/Hour/Minute` en el .plist, haz `unload` y luego `load`.
**Ver si corrió:** `reportes/` (un log por día) y `memoria/bitacora.md`.

**Cerrar la llave de Apify:** `claude mcp remove apify` y, en apify.com → Settings → API & Integrations, revoca el token.
