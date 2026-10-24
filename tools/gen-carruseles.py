#!/usr/bin/env python3
"""Genera los carruseles de redes (1080x1350, formato 4:5 de Instagram y LinkedIn).

Uso:  python3 tools/gen-carruseles.py [senales|frases|ventas]
Salida: marketing/visuales/<carrusel>/NN.png

Mismas reglas de marca que el sitio: navy de fondo, teal vivo solo sobre navy,
sin sombras, sin esquinas redondeadas, Archivo + IBM Plex Mono auto-hospedadas.
Para cambiar un texto se edita CARRUSELES y se vuelve a correr.
Requiere Chromium headless (/opt/pw-browsers) y Pillow.
"""
import glob, html, os, subprocess, sys, tempfile
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUENTES = os.path.join(RAIZ, 'assets', 'fonts')
SALIDA = os.path.join(RAIZ, 'marketing', 'visuales')

# Colores "sobre navy" de cada división (manual de marca, cap. 09)
EST, COM, PRO, OPE, PER, CON = '#4FA3F0', '#F0845B', '#00C9B7', '#9C86F5', '#D9AC55', '#39C4A6'
TEAL = '#00C9B7'

# Cada carrusel: portada, ítems y cierre. div = división (texto) y color del ítem.
CARRUSELES = {
    'senales': {
        'etiqueta': 'Dependencia del dueño',
        'portada': ('7 señales de que tu empresa depende de ti', 'Y cómo saber cuál pesa más', TEAL),
        'items': [
            ('Las decisiones esperan tu visto bueno',
             'Te preguntan precios, descuentos y prioridades que ya deberían tener respuesta.', 'ESTRUCTURA', EST),
            ('Si faltaras dos semanas, algo se detendría',
             'Imagina que te ausentas sin celular. Lo primero que aparece es tu mapa de riesgo.', 'OPERACIÓN', OPE),
            ('Hay procesos que solo una persona sabe hacer',
             '«Eso siempre lo ha hecho Juan». Si Juan se va, la función no se retrasa: desaparece.', 'PROCESOS', PRO),
            ('Cada quien lo hace a su manera',
             'Dos personas hacen lo mismo y lo entregan distinto. Nadie dijo cómo se ve «bien hecho».', 'PERSONAS', PER),
            ('Las ventas pasan por ti',
             'Tu empresa vende lo que tú alcanzas a cerrar.', 'COMERCIAL', COM),
            ('No sabes cómo va la empresa sin preguntar',
             'Para saber ventas, margen o cobranza tienes que pedirlo, esperar y dudar del número.', 'CONTROL', CON),
            ('Nadie sabe bien quién responde por qué',
             '«No sé quién es responsable». Todo problema sin dueño termina siendo tuyo.', 'ESTRUCTURA', EST),
        ],
        'cierre': ('¿Cuál pesa más en tu empresa?',
                   'Tres o más señales indican que la dependencia ya frena el crecimiento. Mídela con el Radar SYNKA.',
                   'Hacer el Radar SYNKA', '21 preguntas · 5 minutos · gratis'),
    },
    'frases': {
        'etiqueta': 'El punto de partida',
        'portada': ('7 frases que escuchas cuando tu empresa depende de ti', 'No son ejemplos: se oyen todos los días', TEAL),
        'items': [
            ('«Pregúntale al dueño.»', 'Las decisiones no tienen otro destino.', 'ESTRUCTURA', EST),
            ('«Eso siempre lo ha hecho Juan.»', 'El conocimiento vive en una sola persona.', 'PROCESOS', PRO),
            ('«Sin mí esto no funciona.»', 'Y por eso no puedes irte.', 'OPERACIÓN', OPE),
            ('«No sé quién es responsable.»', 'Los problemas sin dueño regresan a ti.', 'ESTRUCTURA', EST),
            ('«Cada quien lo hace diferente.»', 'La calidad depende de quién te atienda.', 'PERSONAS', PER),
            ('«No tenemos un proceso.»', 'Todo se resuelve improvisando.', 'PROCESOS', PRO),
            ('«No sabemos exactamente qué está pasando.»', 'Y nadie tiene el número.', 'CONTROL', CON),
        ],
        'cierre': ('No es falta de esfuerzo.',
                   'El dueño se convirtió en el sistema operativo de su empresa. Mide dónde se concentra la dependencia.',
                   'Hacer el Radar SYNKA', '21 preguntas · 5 minutos · gratis'),
    },
    'ventas': {
        'etiqueta': 'SYNKA Comercial',
        'portada': ('¿Tus ventas dependen de ti?', '5 señales y cómo medirlo', COM),
        'items': [
            ('Todas las cotizaciones pasan por ti', 'Tu equipo comercial consulta antes de enviar un precio.', 'COMERCIAL', COM),
            ('Tus mejores clientes solo hablan contigo', 'La relación está en ti, no en la empresa.', 'COMERCIAL', COM),
            ('No conoces tu conversión por etapa', 'Sabes cuánto vendiste, pero no dónde se cae el cliente.', 'COMERCIAL', COM),
            ('Si tú no estás, nadie cierra', 'El equipo prospecta, pero lo importante espera tu llamada.', 'COMERCIAL', COM),
            ('No puedes predecir los ingresos del mes', 'Vendes por rachas, sin un proceso ni un pipeline visible.', 'COMERCIAL', COM),
        ],
        'cierre': ('Mide tu sistema comercial',
                   'Seis áreas del sistema de ventas, con semáforo y las más débiles señaladas.',
                   'Hacer el Diagnóstico Comercial', '10 preguntas · 3 minutos · gratis'),
    },
}

ISOTIPO = '<g><polygon points="36,50 8,22 8,39 19,50" fill="{a}"/><polygon points="36,50 8,78 8,61 19,50" fill="{b}"/></g>'
def isotipo(a, b):
    brazo = ISOTIPO.format(a=a, b=b)
    return ''.join(f'<g transform="rotate({r} 50 50)">{brazo}</g>' for r in (0, 90, 180, 270))

PLANTILLA = '''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Archivo;font-weight:100 900;src:url("file://{f}/archivo-var-latin.woff2") format("woff2")}}
@font-face{{font-family:Archivo;font-weight:100 900;src:url("file://{f}/archivo-var-latin-ext.woff2") format("woff2");unicode-range:U+0100-02BA}}
@font-face{{font-family:Mono;src:url("file://{f}/plexmono-400-latin.woff2") format("woff2")}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1350px;background:#002B49;overflow:hidden}}
.c{{position:relative;width:1080px;height:1350px;background:#002B49;font-family:Archivo,Arial,sans-serif;color:#fff;padding:96px 88px}}
.marca{{position:absolute;right:-230px;bottom:-190px;width:900px;height:900px;opacity:.5}}
.barra{{width:72px;height:7px;background:{acento};margin-bottom:30px}}
.et{{font-family:Mono,monospace;font-size:27px;letter-spacing:.2em;text-transform:uppercase;color:{acento}}}
.cuerpo{{position:absolute;left:88px;right:88px;top:250px;bottom:230px;display:flex;flex-direction:column;justify-content:{just}}}
h1{{font-weight:700;font-size:{tam}px;line-height:1.04;letter-spacing:-.02em}}
.sub{{margin-top:40px;font-size:48px;line-height:1.3;color:#8FB4C9}}
.num{{font-weight:700;font-size:230px;line-height:.9;letter-spacing:-.03em;color:{acento};margin-bottom:30px}}
.tx{{margin-top:44px;font-size:50px;line-height:1.26;color:#fff;max-width:880px}}
.div{{margin-top:48px;font-family:Mono,monospace;font-size:32px;letter-spacing:.14em;color:#8FB4C9}}
.div b{{font-family:Archivo,Arial,sans-serif;font-weight:700;color:#fff;letter-spacing:.06em}}
.div span{{color:{acento};letter-spacing:.06em;font-weight:600;font-family:Archivo,Arial,sans-serif}}
.cta{{display:inline-block;margin-top:56px;background:#00C9B7;color:#00221C;font-weight:700;font-size:40px;padding:30px 44px}}
.cta2{{margin-top:26px;font-family:Mono,monospace;font-size:26px;letter-spacing:.12em;color:#8FB4C9;text-transform:uppercase}}
.desliza{{margin-top:60px;font-family:Mono,monospace;font-size:28px;letter-spacing:.18em;color:{acento};text-transform:uppercase}}
.pie{{position:absolute;left:88px;right:88px;bottom:80px;display:flex;align-items:center;justify-content:space-between}}
.pie .l{{display:flex;align-items:center;gap:18px}}
.pie svg{{width:60px;height:60px}}
.pie .l span{{font-weight:700;font-size:36px;letter-spacing:.12em}}
.pie .p{{font-family:Mono,monospace;font-size:27px;letter-spacing:.14em;color:#8FB4C9}}
.pie .u{{font-family:Mono,monospace;font-size:27px;letter-spacing:.1em;color:#8FB4C9}}
</style></head><body><div class="c">
<svg class="marca" viewBox="0 0 100 100">{grande}</svg>
<div class="barra"></div><div class="et">{etiqueta}</div>
<div class="cuerpo">{cuerpo}</div>
<div class="pie"><div class="l"><svg viewBox="0 0 100 100">{chico}</svg><span>SYNKA</span></div>{derecha}</div>
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

def esc(t):
    return html.escape(t)

def diapositivas(c):
    """Devuelve [(acento, tam, justify, cuerpo_html, es_ultima)] en orden."""
    out = []
    t, s, ac = c['portada']
    out.append((ac, 120 if len(t) < 45 else 96, 'center',
                f'<h1>{esc(t)}</h1><p class="sub">{esc(s)}</p><p class="desliza">Desliza →</p>'))
    for i, (titulo, texto, div, col) in enumerate(c['items'], 1):
        corto = len(titulo) < 34
        out.append((col, 88 if corto else 76, 'center',
                    f'<div class="num">{i:02d}</div><h1>{esc(titulo)}</h1><p class="tx">{esc(texto)}</p>'
                    f'<p class="div"><b>SYNKA</b> <span>{esc(div)}</span></p>'))
    t, s, boton, nota = c['cierre']
    out.append((TEAL, 96, 'center',
                f'<h1>{esc(t)}</h1><p class="tx">{esc(s)}</p>'
                f'<div><span class="cta">{esc(boton)}</span></div><p class="cta2">{esc(nota)}<br>Enlace en la bio</p>'))
    return out

def render(nombre, c, nav):
    carpeta = os.path.join(SALIDA, nombre)
    os.makedirs(carpeta, exist_ok=True)
    for viejo in glob.glob(os.path.join(carpeta, '*.png')):
        os.remove(viejo)
    laminas = diapositivas(c)
    total = len(laminas)
    for n, (acento, tam, just, cuerpo) in enumerate(laminas, 1):
        ultima = n == total
        derecha = '<div class="u">synka.mx</div>' if ultima else f'<div class="p">{n:02d} / {total:02d}</div>'
        pagina = PLANTILLA.format(f=FUENTES, acento=acento, tam=tam, just=just, etiqueta=esc(c['etiqueta']),
                                  cuerpo=cuerpo, derecha=derecha,
                                  grande=isotipo('rgba(255,255,255,.05)', 'rgba(0,201,183,.12)'),
                                  chico=isotipo('#FFFFFF', '#00C9B7'))
        with tempfile.TemporaryDirectory() as tmp:
            ruta = os.path.join(tmp, 'c.html'); png = os.path.join(tmp, 'c.png')
            open(ruta, 'w', encoding='utf-8').write(pagina)
            subprocess.run([nav, '--headless', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                            '--force-device-scale-factor=1', '--window-size=1080,1350',
                            f'--screenshot={png}', 'file://' + ruta],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            Image.open(png).convert('RGB').crop((0, 0, 1080, 1350)).save(
                os.path.join(carpeta, f'{n:02d}.png'), optimize=True)
    print(nombre, total, 'láminas')

def main():
    nav = chrome()
    pedidos = sys.argv[1:] or list(CARRUSELES)
    for nombre in pedidos:
        render(nombre, CARRUSELES[nombre], nav)

if __name__ == '__main__':
    main()
