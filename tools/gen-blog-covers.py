#!/usr/bin/env python3
"""Genera las portadas del blog (1200x630 para compartir, 640 para tarjetas).

Uso:  python3 tools/gen-blog-covers.py
Requiere Chromium headless (se busca en /opt/pw-browsers) y Pillow.
Para agregar un artículo, añade una entrada a ARTICULOS y vuelve a correrlo.
"""
import glob, html, os, subprocess, sys, tempfile
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUENTES = os.path.join(RAIZ, 'assets', 'fonts')
SALIDA = os.path.join(RAIZ, 'assets', 'img', 'blog')

# slug, etiqueta, título, color de acento (variante "sobre navy" de la división)
ARTICULOS = [
    ('empresa-que-depende-del-dueno', 'Blog · Dependencia del dueño',
     '¿Tu empresa depende de ti? Por qué eso tiene un límite', '#4FA3F0'),
    ('como-delegar-en-mi-empresa', 'Blog · Delegación',
     'Cómo empezar a delegar sin que todo se caiga', '#D9AC55'),
    ('documentar-procesos-sin-burocracia', 'Blog · Procesos',
     'Cómo documentar los procesos de tu empresa sin volverla burocrática', '#00C9B7'),
    ('ventas-sin-depender-del-dueno', 'Blog · Ventas',
     'Cómo hacer que tus ventas no dependan de que tú cierres todo', '#F0845B'),
    ('senales-empresa-depende-del-dueno', 'Blog · Dependencia del dueño',
     '7 señales de que tu empresa depende de ti', '#9C86F5'),
]

ISOTIPO = '''<g><polygon points="36,50 8,22 8,39 19,50" fill="{a}"/><polygon points="36,50 8,78 8,61 19,50" fill="{b}"/></g>'''
def isotipo(a, b):
    brazo = ISOTIPO.format(a=a, b=b)
    return ''.join(f'<g transform="rotate({r} 50 50)">{brazo}</g>' for r in (0, 90, 180, 270))

PLANTILLA = '''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Archivo;font-weight:100 900;src:url("file://{f}/archivo-var-latin.woff2") format("woff2")}}
@font-face{{font-family:Archivo;font-weight:100 900;src:url("file://{f}/archivo-var-latin-ext.woff2") format("woff2");unicode-range:U+0100-02BA}}
@font-face{{font-family:Mono;src:url("file://{f}/plexmono-400-latin.woff2") format("woff2")}}
*{{box-sizing:border-box;margin:0}}
html,body{{width:1200px;height:630px;background:#002B49;overflow:hidden}}
.c{{position:relative;width:1200px;height:630px;background:#002B49;font-family:Archivo,Arial,sans-serif;color:#fff}}
.marca{{position:absolute;right:-110px;top:50%;transform:translateY(-50%);width:640px;height:640px;opacity:.5}}
.barra{{position:absolute;left:72px;top:96px;width:64px;height:6px;background:{acento}}}
.et{{position:absolute;left:72px;top:122px;font-family:Mono,monospace;font-size:22px;letter-spacing:.2em;text-transform:uppercase;color:{acento}}}
h1{{position:absolute;left:72px;top:182px;width:760px;font-weight:600;font-size:{tam}px;line-height:1.08;letter-spacing:-.02em}}
.pie{{position:absolute;left:72px;bottom:56px;display:flex;align-items:center;gap:18px}}
.pie svg{{width:52px;height:52px}}
.pie span{{font-weight:700;font-size:34px;letter-spacing:.12em}}
</style></head><body><div class="c">
<svg class="marca" viewBox="0 0 100 100">{grande}</svg>
<div class="barra"></div><div class="et">{etiqueta}</div><h1>{titulo}</h1>
<div class="pie"><svg viewBox="0 0 100 100">{chico}</svg><span>SYNKA</span></div>
</div></body></html>'''

def chrome():
    for patron in ('/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell',
                   '/opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell',
                   '/opt/pw-browsers/chromium-*/chrome-linux/chrome',
                   '/opt/pw-browsers/chromium-*/chrome-linux64/chrome'):
        hallados = sorted(glob.glob(patron))
        if hallados:
            return hallados[-1]
    sys.exit('No se encontró Chromium headless')

def main():
    os.makedirs(SALIDA, exist_ok=True)
    nav = chrome()
    for slug, etiqueta, titulo, acento in ARTICULOS:
        tam = 62 if len(titulo) < 60 else 54
        pagina = PLANTILLA.format(
            f=FUENTES, acento=acento, tam=tam, etiqueta=html.escape(etiqueta),
            titulo=html.escape(titulo),
            grande=isotipo('rgba(255,255,255,.07)', 'rgba(0,201,183,.16)'),
            chico=isotipo('#FFFFFF', '#00C9B7'))
        with tempfile.TemporaryDirectory() as tmp:
            ruta = os.path.join(tmp, 'c.html'); png = os.path.join(tmp, 'c.png')
            open(ruta, 'w', encoding='utf-8').write(pagina)
            subprocess.run([nav, '--headless', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                            '--force-device-scale-factor=1', '--window-size=1200,630',
                            f'--screenshot={png}', 'file://' + ruta],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            im = Image.open(png).convert('RGB').crop((0, 0, 1200, 630))
        base = os.path.join(SALIDA, slug)
        im.save(base + '.png', optimize=True)
        im.resize((640, 336), Image.LANCZOS).save(base + '-640.webp', quality=82, method=6)
        print(slug, os.path.getsize(base + '.png') // 1024, 'KB png ·',
              os.path.getsize(base + '-640.webp') // 1024, 'KB webp')

if __name__ == '__main__':
    main()
