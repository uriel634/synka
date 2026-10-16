#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el blog: /blog/index.html y un HTML por artículo.

El contenido vive en tools/blog_articulos.py (markdown mínimo). Las páginas
heredan header, footer y CSS del sitio. Editar los datos y volver a ejecutar:

    python3 tools/gen-blog.py
    python3 tools/gen-soluciones.py   # solo si cambia la lista de URLs (sitemap)
"""

import html
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_articulos import ARTICULOS  # noqa: E402

SITIO = "https://synka.mx"
OG = SITIO + "/assets/img/og-synka.png"

LOGO = """<svg viewBox="0 0 100 100" aria-hidden="true" focusable="false">
        <g><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="#00C9B7"/></g>
        <g transform="rotate(90 50 50)"><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="#00C9B7"/></g>
        <g transform="rotate(180 50 50)"><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="#00C9B7"/></g>
        <g transform="rotate(270 50 50)"><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="#00C9B7"/></g>
      </svg>"""

FLECHA = '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.6"/></svg>'

MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def esc(s):
    return html.escape(s, quote=True)


def fecha_corta(iso):
    y, m, d = iso.split("-")
    return "{} {} {}".format(int(d), MESES[int(m) - 1].upper(), y)


def local(url):
    return url[len(SITIO):] if url.startswith(SITIO + "/") else url


# --- markdown mínimo -> HTML ------------------------------------------------

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: '<a href="{}">{}</a>'.format(local(m.group(2)), m.group(1)), t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return t


def cuerpo_html(md):
    out = []
    for bloque in re.split(r"\n\s*\n", md.strip()):
        lineas = [l.rstrip() for l in bloque.split("\n") if l.strip()]
        if not lineas:
            continue
        if lineas[0].startswith("### "):
            out.append("<h2>{}</h2>".format(inline(lineas[0][4:])))
        elif all(re.fullmatch(r"\*\*\[.+?\]\(.+?\)\*\*", l) for l in lineas):
            btns = []
            for i, l in enumerate(lineas):
                m = re.fullmatch(r"\*\*\[(.+?)\]\((.+?)\)\*\*", l)
                clase = "btn btn--primario" if i == 0 else "btn btn--fantasma"
                btns.append('<a class="{}" href="{}" data-cta="instrumento" data-seccion="articulo_blog">{}</a>'
                            .format(clase, local(m.group(2)), html.escape(m.group(1), quote=False)))
            out.append('<div class="grupo-cta articulo__cta">\n  {}\n</div>'.format("\n  ".join(btns)))
        elif all(l.startswith("- ") for l in lineas):
            out.append("<ul>\n" + "\n".join("  <li>{}</li>".format(inline(l[2:])) for l in lineas) + "\n</ul>")
        elif all(re.match(r"\d+\. ", l) for l in lineas):
            out.append("<ol>\n" + "\n".join("  <li>{}</li>".format(inline(re.sub(r"^\d+\. ", "", l))) for l in lineas) + "\n</ol>")
        else:
            out.append("<p>{}</p>".format("<br>\n".join(inline(l) for l in lineas)))
    return "\n\n".join(out)


# --- piezas comunes ---------------------------------------------------------

def cabecera(titulo, descripcion, canonical, jsonld, og_tipo):
    return """<!DOCTYPE html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>{titulo}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#002B49">

<link rel="preload" href="../assets/fonts/archivo-var-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../assets/fonts/plexmono-400-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../css/synka.css">

<link rel="icon" href="../assets/logo/favicon-32.svg" type="image/svg+xml">
<link rel="icon" href="../assets/img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="../assets/img/avatar-1024.png">
<link rel="manifest" href="../site.webmanifest">

<meta property="og:type" content="{og_tipo}">
<meta property="og:locale" content="es_MX">
<meta property="og:site_name" content="SYNKA">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="SYNKA · Sistemas que hacen funcionar tu empresa">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{titulo}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og}">
<meta name="twitter:image:alt" content="SYNKA · Sistemas que hacen funcionar tu empresa">

<script type="application/ld+json">
{jsonld}
</script>

<script src="../js/config.js"></script>
</head>

<body>
<a class="salta-al-contenido" href="#contenido">Saltar al contenido</a>

<header class="header">
  <div class="wrap header__barra">
    <a class="logotipo" href="../index" aria-label="SYNKA · Inicio">
      {logo}
      <span class="logotipo__palabra">SYNKA</span>
    </a>

    <nav class="nav" aria-label="Principal">
      <ul class="nav__lista">
        <li><a class="nav__enlace" href="/#problema">El problema</a></li>
        <li><a class="nav__enlace" href="/#metodo">Método SYNKA</a></li>
        <li><a class="nav__enlace" href="/#soluciones">Soluciones</a></li>
        <li><a class="nav__enlace" href="/#nosotros">Nosotros</a></li>
        <li><a class="nav__enlace" href="/#diagnostico">Diagnóstico</a></li>
      </ul>
      <a class="btn btn--primario" href="/#solicitar" data-cta="solicitar_diagnostico" data-seccion="header">Solicitar diagnóstico</a>
    </nav>

    <button class="menu-btn" type="button" data-menu-btn aria-expanded="false" aria-controls="menu-movil" aria-label="Abrir menú">
      <span></span><span></span><span></span>
    </button>
    <span class="progreso" data-progreso aria-hidden="true"></span>
  </div>

  <div class="wrap menu-movil" id="menu-movil" data-menu data-abierto="false">
    <nav aria-label="Principal, versión móvil">
      <ul>
        <li><a href="/#problema">El problema</a></li>
        <li><a href="/#metodo">Método SYNKA</a></li>
        <li><a href="/#soluciones">Soluciones</a></li>
        <li><a href="/#nosotros">Nosotros</a></li>
        <li><a href="/#diagnostico">Diagnóstico</a></li>
      </ul>
      <a class="btn btn--primario btn--bloque" href="/#solicitar" data-cta="solicitar_diagnostico" data-seccion="menu_movil">Solicitar diagnóstico</a>
    </nav>
  </div>
</header>

<main id="contenido">
""".format(titulo=esc(titulo), desc=esc(descripcion), canonical=canonical, jsonld=jsonld,
           og_tipo=og_tipo, og=OG, logo=LOGO)


PIE = """
</main>

<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <a class="logotipo" href="../index" aria-label="SYNKA · Inicio">
          {logo}
          <span class="logotipo__palabra">SYNKA</span>
        </a>
        <p class="footer__descriptor">Sistemas que hacen funcionar tu empresa</p>
      </div>
      <div>
        <h4>Soluciones</h4>
        <ul>
          <li><a href="../soluciones/estructura">SYNKA Estructura</a></li>
          <li><a href="../soluciones/comercial">SYNKA Comercial</a></li>
          <li><a href="../soluciones/procesos">SYNKA Procesos</a></li>
          <li><a href="../soluciones/operacion">SYNKA Operación</a></li>
          <li><a href="../soluciones/personas">SYNKA Personas</a></li>
          <li><a href="../soluciones/control">SYNKA Control</a></li>
        </ul>
      </div>
      <div>
        <h4>Navegación</h4>
        <ul>
          <li><a href="/#problema">El problema</a></li>
          <li><a href="/#metodo">Método SYNKA</a></li>
          <li><a href="/#nosotros">Nosotros</a></li>
          <li><a href="../blog/">Blog</a></li>
          <li><a href="../diagnostico/radar">Radar SYNKA</a></li>
          <li><a href="../diagnostico/comercial">Diagnóstico Comercial</a></li>
          <li><a href="mailto:hola@synka.mx" data-correo data-rellena>hola@synka.mx</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__base">
      <span>&copy; <span id="anio">2026</span> SYNKA</span>
      <span>Todo funcionando como uno</span>
    </div>
  </div>
</footer>

<script>document.getElementById('anio').textContent = new Date().getFullYear();</script>
<script src="../js/synka.js" defer></script>
</body>
</html>
""".format(logo=LOGO)


def tarjeta(a):
    return """      <a class="blog-card aparece" href="{slug}" data-cta="articulo_blog" data-seccion="blog">
        <span class="dato blog-card__fecha">{fecha}</span>
        <h3>{h1}</h3>
        <p>{desc}</p>
        <span class="division__ir">Leer artículo {flecha}</span>
      </a>""".format(slug=a["slug"], fecha=fecha_corta(a["fecha"]), h1=esc(a["h1"]),
                     desc=esc(a["description"]), flecha=FLECHA.replace("<svg ", '<svg class="" '))


def construir_articulo(a):
    url = "{}/blog/{}".format(SITIO, a["slug"])
    jsonld = """{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "BlogPosting",
      "headline": "{h1}",
      "description": "{desc}",
      "keywords": "{kw}",
      "inLanguage": "es-MX",
      "datePublished": "{fecha}",
      "dateModified": "{fecha}",
      "mainEntityOfPage": "{url}",
      "image": "{og}",
      "author": {{ "@type": "Organization", "name": "SYNKA", "url": "{sitio}/" }},
      "publisher": {{ "@type": "Organization", "name": "SYNKA", "url": "{sitio}/", "logo": {{ "@type": "ImageObject", "url": "{sitio}/assets/img/isotipo-bicolor-512.png" }} }}
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Inicio", "item": "{sitio}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Blog", "item": "{sitio}/blog" }},
        {{ "@type": "ListItem", "position": 3, "name": "{h1}", "item": "{url}" }}
      ]
    }}
  ]
}}""".format(h1=a["h1"].replace('"', '\\"'), desc=a["description"].replace('"', '\\"'), kw=a["keyword"],
             fecha=a["fecha"], url=url, og=OG, sitio=SITIO)

    otros = [x for x in ARTICULOS if x["slug"] != a["slug"]]
    cuerpo = """
<section class="hero hero--articulo seccion--navy">
  <div class="wrap">
    <nav class="eyebrow" aria-label="Ruta de navegación" style="margin-bottom:1.75rem">
      <a href="./" style="color:inherit">Blog</a>
    </nav>
    <p class="dato articulo__fecha"><time datetime="{fecha}">{fecha_c}</time></p>
    <h1>{h1}</h1>
  </div>
</section>

<section class="seccion seccion--blanco">
  <div class="wrap">
    <article class="articulo">
{contenido}
    </article>
    <p class="articulo__volver"><a class="enlace-linea" href="./">Ver todos los artículos {flecha}</a></p>
  </div>
</section>

<section class="seccion seccion--arena">
  <div class="wrap">
    <div class="encabezado-seccion">
      <p class="eyebrow">Sigue leyendo</p>
      <h2>Más artículos</h2>
    </div>
    <div class="blog-grid">
{tarjetas}
    </div>
  </div>
</section>
""".format(fecha=a["fecha"], fecha_c=fecha_corta(a["fecha"]), h1=esc(a["h1"]),
           contenido=indentar(cuerpo_html(a["cuerpo"]), 6), flecha=FLECHA,
           tarjetas="\n".join(tarjeta(x) for x in otros))
    return cabecera(a["title"], a["description"], url, jsonld, "article") + cuerpo + PIE


def construir_indice():
    titulo = "Blog SYNKA · Estructura, procesos y control para tu PyME"
    desc = ("Artículos para dueños de PyME que quieren una empresa que funcione sin depender de ellos: "
            "delegación, organigrama, procesos, ventas, indicadores y diagnóstico.")
    url = SITIO + "/blog"
    items = ",\n".join(
        '        {{ "@type": "ListItem", "position": {}, "url": "{}/blog/{}", "name": "{}" }}'.format(
            i, SITIO, a["slug"], a["h1"].replace('"', '\\"'))
        for i, a in enumerate(ARTICULOS, 1))
    jsonld = """{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "CollectionPage",
      "name": "Blog SYNKA",
      "description": "{desc}",
      "url": "{url}",
      "inLanguage": "es-MX",
      "isPartOf": {{ "@type": "WebSite", "name": "SYNKA", "url": "{sitio}/" }},
      "mainEntity": {{
        "@type": "ItemList",
        "itemListElement": [
{items}
        ]
      }}
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Inicio", "item": "{sitio}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Blog", "item": "{url}" }}
      ]
    }}
  ]
}}""".format(desc=desc, url=url, sitio=SITIO, items=items.replace("        {", "          {"))
    cuerpo = """
<section class="hero hero--articulo seccion--navy">
  <div class="wrap">
    <nav class="eyebrow" aria-label="Ruta de navegación" style="margin-bottom:1.75rem">
      <a href="../index" style="color:inherit">Inicio</a>
    </nav>
    <h1>Blog SYNKA</h1>
    <p class="lead" style="margin-top:1.5rem">Cómo dejar de ser el centro de tu empresa: estructura, delegación, procesos, ventas e indicadores para dueños de PyME.</p>
  </div>
</section>

<section class="seccion seccion--arena">
  <div class="wrap">
    <div class="blog-grid">
{tarjetas}
    </div>
  </div>
</section>

<section class="seccion seccion--hundida" id="solicitar">
  <div class="wrap centrado" style="max-width:760px">
    <p class="eyebrow" style="justify-content:center">El siguiente paso</p>
    <h2>¿Cuánto de tu empresa todavía depende de ti?</h2>
    <p class="lead" style="margin-top:1.25rem">Empieza por el diagnóstico. Son 21 preguntas, sin costo.</p>
    <div class="grupo-cta" style="justify-content:center; margin-top:2.25rem">
      <a class="btn btn--primario" href="/diagnostico/radar" data-cta="instrumento" data-seccion="cta_final_blog">Haz el Radar SYNKA</a>
      <a class="enlace-linea" href="/diagnostico/comercial" data-cta="instrumento" data-seccion="cta_final_blog">Diagnóstico Comercial {flecha}</a>
    </div>
  </div>
</section>
""".format(tarjetas="\n".join(tarjeta(a) for a in ARTICULOS), flecha=FLECHA)
    return cabecera(titulo, desc, url, jsonld, "website") + cuerpo + PIE


def indentar(txt, n):
    p = " " * n
    return "\n".join(p + l if l else l for l in txt.split("\n"))


def main():
    destino = os.path.join(RAIZ, "blog")
    os.makedirs(destino, exist_ok=True)
    with open(os.path.join(destino, "index.html"), "w", encoding="utf-8") as f:
        f.write(construir_indice())
    print("escrito  blog/index.html")
    for a in ARTICULOS:
        with open(os.path.join(destino, a["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(construir_articulo(a))
        print("escrito  blog/{}.html".format(a["slug"]))


if __name__ == "__main__":
    main()
