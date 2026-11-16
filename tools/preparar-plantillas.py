#!/usr/bin/env python3
"""Convierte el HTML guardado de un artefacto de Claude en una plantilla
autónoma (sin dependencias de Claude ni de Google Fonts).

Uso:
  python3 tools/preparar-plantillas.py sistema ARCHIVO_ARTEFACTO.html
  python3 tools/preparar-plantillas.py panel   ARCHIVO_ARTEFACTO.html

Escribe _source/app/<producto>.html. Las plantillas son la fuente única:
tools/nuevo-cliente.py las copia a la carpeta de cada cliente.
"""
import re, sys, pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DESTINO = {"sistema": "sistema-30-dias.html", "panel": "panel-comercial.html"}

FUENTES = """<style>
@font-face{font-family:'Archivo';font-style:normal;font-weight:300 700;font-display:swap;src:url('/assets/fonts/archivo-var-latin.woff2') format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'Archivo';font-style:normal;font-weight:300 700;font-display:swap;src:url('/assets/fonts/archivo-var-latin-ext.woff2') format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:'IBM Plex Mono';font-style:normal;font-weight:400 500;font-display:swap;src:url('/assets/fonts/plexmono-400-latin.woff2') format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'IBM Plex Mono';font-style:normal;font-weight:400 500;font-display:swap;src:url('/assets/fonts/plexmono-400-latin-ext.woff2') format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
</style>"""

# Descarga real de archivos cuando no existe la función de Claude.
DESCARGA = ("const _b=new Blob([data],{type:/\\.csv$/.test(name)?'text/csv;charset=utf-8':'application/json;charset=utf-8'}),"
            "_u=URL.createObjectURL(_b),_a=document.createElement('a');_a.href=_u;_a.download=name;document.body.appendChild(_a);_a.click();"
            "setTimeout(()=>{_a.remove();URL.revokeObjectURL(_u)},1000);toast('Archivo descargado');return true;")

def main():
    if len(sys.argv) != 3 or sys.argv[1] not in DESTINO:
        sys.exit(__doc__)
    prod, origen = sys.argv[1], pathlib.Path(sys.argv[2])
    h = origen.read_text(encoding="utf-8")

    m = re.search(r"<title>(.*?)</title>", h, re.S)
    titulo = m.group(1).strip()
    h = h.replace(m.group(0), "", 1)
    h = re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\s*', "", h)
    h = re.sub(r'<link rel="preconnect"[^>]*>\s*', "", h)
    h = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>\s*', "", h)

    head_extra = (f"<title>{titulo} · SYNKA</title>"
                  '<meta name="robots" content="noindex, nofollow">'
                  '<meta name="referrer" content="no-referrer">'
                  '<meta name="theme-color" content="#002B49">'
                  '<link rel="icon" href="/assets/logo/favicon-32.svg" type="image/svg+xml">'
                  '<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32">'
                  '<link rel="apple-touch-icon" href="/assets/img/avatar-1024.png">'
                  '<link rel="preload" href="/assets/fonts/archivo-var-latin.woff2" as="font" type="font/woff2" crossorigin>'
                  + FUENTES)
    assert "</head>" in h
    h = h.replace("</head>", head_extra + "</head>", 1)
    h = h.replace("<!doctype html><html>", '<!doctype html><html lang="es-MX">', 1)

    # Respaldo: descarga real en lugar de la ventana de copiar texto.
    marca = "const fb=$('#fb');fb.innerHTML=`<div class=\"card\"><h3>${esc(name)}</h3>"
    assert h.count(marca) == 1, "no se encontró saveFile"
    h = h.replace(marca, DESCARGA + "\n " + marca, 1)

    destino = RAIZ / "_source" / "app" / DESTINO[prod]
    destino.write_text(h, encoding="utf-8")
    print("OK", destino.relative_to(RAIZ), len(h), "bytes")

main()
