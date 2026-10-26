# Agente de prospección (guía tododeia · Apify)

Todo corre en TU computadora. Esta carpeta trae la configuración; los datos (`leads/`, `correos/`, `reportes/`, `memoria/`) están en `.gitignore` y nunca se suben al repo público.

## Puesta en marcha (en tu Mac)
1. Cuenta gratis en apify.com (US$5/mes sin tarjeta).
2. `cd prospeccion && claude mcp add --transport http apify https://mcp.apify.com`
3. `claude` → `/mcp` → autoriza Apify.
4. Edita los `[PENDIENTE]` y el presupuesto en `CLAUDE.md`; corrige `perfil-cliente.md`.
5. Prueba: `/ronda` mirando cada paso (la primera vez pide 10 leads, no 50).
6. Programarlo: ajusta rutas en `scripts/com.synka.prospeccion.plist`, cópialo a `~/Library/LaunchAgents/`, `launchctl load`. Dispáralo antes a mano: `bash scripts/ronda.sh`.
7. Antes de enviar: dominio aparte con SPF/DKIM/DMARC, 5–10 correos/día al inicio, verificar rebotes < 2 %.

Pausa, tope y apagado: ver `COMO-APAGARLO.md`.

## Comandos
- Playbook a mano (en orden): `/p1-entrevista` · `/p2-prueba10` · `/p3-leads50` · `/p4-enriquecer` · `/p5-calificar` · `/p6-correos` · `/p7-seguimientos` · `/p8-aprender`
- Agente: `/ronda [ciudad o nicho]` · `/parte` · `/auditoria`
