#!/usr/bin/env python3
"""Crea o actualiza las carpetas privadas de cliente en app/c/<clave>/.

  python3 tools/nuevo-cliente.py nuevo [--solo sistema|panel]
      Crea una carpeta con clave aleatoria e imprime la URL para el cliente.
      La clave NO se guarda en el repositorio: anótala junto al cliente en
      tu propio registro (el nombre del cliente nunca se escribe aquí).

  python3 tools/nuevo-cliente.py actualizar
      Vuelve a copiar las plantillas de _source/app/ a todas las carpetas
      existentes en app/c/. Se usa después de cambiar una plantilla.

Cada carpeta lleva su clave dentro del identificador de almacenamiento, así
los datos de un cliente nunca se mezclan con los de otro aunque se abran en
el mismo navegador (por ejemplo, al probar).
"""
import re, secrets, sys, pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PLANTILLAS = RAIZ / "_source" / "app"
CLIENTES = RAIZ / "app" / "c"
BASE = "https://synka.mx/app/c/"
PRODUCTOS = {
    "sistema": ("sistema-30-dias.html", "Sistema Comercial 30 Días",
                "Tu plan de 4 semanas: proceso de venta, pipeline, cuotas y control semanal."),
    "panel": ("panel-comercial.html", "Panel Comercial",
              "Tus ventas del día, tu meta del mes y tu semáforo semanal."),
}
CLAVES_ALMACEN = {
    "sistema-30-dias.html": "synka-sistema30-v1",
    "panel-comercial.html": "synka-panel-comercial-v1",
}


def escribir_producto(carpeta, clave, archivo):
    h = (PLANTILLAS / archivo).read_text(encoding="utf-8")
    viejo = f"const KEY='{CLAVES_ALMACEN[archivo]}';"
    assert h.count(viejo) == 1, f"no se encontró {viejo} en {archivo}"
    h = h.replace(viejo, f"const KEY='{CLAVES_ALMACEN[archivo]}:{clave}';")
    (carpeta / archivo).write_text(h, encoding="utf-8")


def escribir_indice(carpeta, presentes):
    tarjetas = "".join(
        f'<a class="t" href="{PRODUCTOS[p][0]}"><b>{PRODUCTOS[p][1]}</b><span>{PRODUCTOS[p][2]}</span></a>'
        for p in ("sistema", "panel") if p in presentes)
    (carpeta / "index.html").write_text(f"""<!doctype html><html lang="es-MX"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Tus herramientas · SYNKA</title>
<meta name="robots" content="noindex, nofollow"><meta name="referrer" content="no-referrer"><meta name="theme-color" content="#002B49">
<link rel="icon" href="/assets/logo/favicon-32.svg" type="image/svg+xml">
<style>
@font-face{{font-family:'Archivo';font-weight:300 700;font-display:swap;src:url('/assets/fonts/archivo-var-latin.woff2') format('woff2')}}
:root{{color-scheme:light dark;--bg:#EEF1F4;--s:#fff;--fg:#002B49;--m:#4A6B84;--l:#DCE2E8;--a:#00C9B7}}
@media(prefers-color-scheme:dark){{:root{{--bg:#01213A;--s:#002B49;--fg:#fff;--m:#8FB4C9;--l:#123A57}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 'Archivo',Arial,sans-serif}}
main{{max-width:560px;margin:0 auto;padding:32px 16px}}h1{{font-size:26px;letter-spacing:-.02em;line-height:1.15;margin:0 0 8px}}
p{{color:var(--m);margin:0 0 24px}}.t{{display:grid;gap:4px;background:var(--s);border:1px solid var(--l);border-left:4px solid var(--a);padding:16px;margin-bottom:12px;color:inherit;text-decoration:none;min-height:44px}}
.t span{{color:var(--m);font-size:14px}}.t:focus-visible{{outline:3px solid #0F6FD1;outline-offset:2px}}.n{{font-size:13px;color:var(--m);margin-top:24px}}
</style></head><body><main><h1>Tus herramientas SYNKA</h1>
<p>Guarda esta página en tu pantalla de inicio. Es tu enlace personal: no lo compartas.</p>
{tarjetas}
<p class="n">Tus datos se guardan en este dispositivo. Descarga tu respaldo desde la herramienta cada semana.</p></main></body></html>
""", encoding="utf-8")


def nuevo(solo):
    prods = [solo] if solo else ["sistema", "panel"]
    clave = secrets.token_hex(10)
    carpeta = CLIENTES / clave
    carpeta.mkdir(parents=True)
    for p in prods:
        escribir_producto(carpeta, clave, PRODUCTOS[p][0])
    escribir_indice(carpeta, prods)
    print("Carpeta creada: app/c/" + clave)
    print("URL del cliente:", BASE + clave + "/")
    for p in prods:
        print("  ", PRODUCTOS[p][1] + ":", BASE + clave + "/" + PRODUCTOS[p][0].replace(".html", ""))


def actualizar():
    if not CLIENTES.exists():
        sys.exit("No hay carpetas de cliente todavía.")
    n = 0
    for carpeta in sorted(p for p in CLIENTES.iterdir() if p.is_dir()):
        clave = carpeta.name
        presentes = [p for p, (a, *_) in PRODUCTOS.items() if (carpeta / a).exists()]
        for p in presentes:
            escribir_producto(carpeta, clave, PRODUCTOS[p][0])
        escribir_indice(carpeta, presentes)
        n += 1
    print(f"Actualizadas {n} carpeta(s).")


def main():
    a = sys.argv[1:]
    if a and a[0] == "nuevo":
        solo = None
        if "--solo" in a:
            solo = a[a.index("--solo") + 1]
            if solo not in PRODUCTOS:
                sys.exit("--solo admite: sistema o panel")
        nuevo(solo)
    elif a and a[0] == "actualizar":
        actualizar()
    else:
        sys.exit(__doc__)


main()
