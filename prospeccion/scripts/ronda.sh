#!/bin/bash
# Dispara una ronda en modo no interactivo. Lo invoca launchd (ver com.synka.prospeccion.plist).
# Rutas y entorno explícitos: launchd no carga tu perfil de terminal.
set -u
DIR="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE_BIN="${CLAUDE_BIN:-$HOME/.local/bin/claude}"   # ajusta con: which claude
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
cd "$DIR" || exit 1
mkdir -p reportes
OUT="reportes/corrida-$(date +%F).log"
[ -f PAUSA ] && { echo "$(date -Iseconds) pausado" >> memoria/bitacora.md; exit 0; }
# Auth sin humano: ejecuta una vez `claude setup-token` y exporta CLAUDE_CODE_OAUTH_TOKEN
# (o guárdalo en ~/.synka-prospeccion.env, permisos 600).
[ -f "$HOME/.synka-prospeccion.env" ] && . "$HOME/.synka-prospeccion.env"
"$CLAUDE_BIN" -p "/ronda" \
  --max-turns 60 \
  --max-budget-usd 3 \
  --allowedTools "Read,Write,Edit,Glob,Grep,mcp__apify" \
  >> "$OUT" 2>&1
