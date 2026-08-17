#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera las páginas de los dos instrumentos de diagnóstico.

    python3 tools/gen-diagnosticos.py

Comparten cabecera, pie y armazón del cuestionario: se generan juntas para que
no puedan divergir. El banco de preguntas lo produce gen-datos-diagnostico.py.

No se declara ninguna cifra de autoridad (empresas atendidas, años, porcentajes
de mercado): quedaron pendientes de verificación.
"""

import os
import datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITIO = "https://synka.mx"

LOGO = """<svg viewBox="0 0 100 100" aria-hidden="true" focusable="false">
        <g><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="#00C9B7"/></g>
        <g transform="rotate(90 50 50)"><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="#00C9B7"/></g>
        <g transform="rotate(180 50 50)"><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="#00C9B7"/></g>
        <g transform="rotate(270 50 50)"><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="#00C9B7"/></g>
      </svg>"""

SIGNO_GRANDE = """<svg class="signo signo--anima" data-signo viewBox="0 0 100 100" role="img" aria-label="Isotipo SYNKA">
        <g class="signo__brazo"><g><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="#00C9B7"/></g></g>
        <g class="signo__brazo"><g transform="rotate(90 50 50)"><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="#00C9B7"/></g></g>
        <g class="signo__brazo"><g transform="rotate(180 50 50)"><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="#00C9B7"/></g></g>
        <g class="signo__brazo"><g transform="rotate(270 50 50)"><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="#00C9B7"/></g></g>
      </svg>"""

INSTRUMENTOS = [
    {
        "slug": "radar",
        "quiz": "radar",
        "datos": "datos-radar.js",
        "marca_700": "RADAR",
        "marca_300": "SYNKA",
        "titulo_seo": "Radar SYNKA · Diagnóstico de control empresarial para PyMEs",
        "meta": "Autoevaluación de 21 preguntas que mide el control de tu empresa en las seis divisiones SYNKA y señala dónde se concentra la dependencia del dueño.",
        "eyebrow": "Nivel 1 · Mapa completo · 21 preguntas · unos 5 minutos",
        "h1": "¿En cuál parte de tu empresa se concentra la dependencia?",
        "entrada": "Veintiuna preguntas sobre cómo opera tu empresa hoy. Al terminar obtienes "
                   "un perfil por cada una de las seis divisiones y sabes cuál sostiene el "
                   "mayor riesgo. No cómo quisieras que operara: cómo opera hoy.",
        "que_mide_titulo": "Las seis divisiones, medidas una por una",
        "que_mide_lead": "Cada pregunta apunta a una división. El resultado no te da una nota "
                         "general vaga: te dice qué parte del sistema está sosteniendo el peso.",
        "ejes": [
            ("estructura", "ESTRUCTURA", "Si el equipo conoce los objetivos, si hay plan documentado y si los roles y niveles de decisión están definidos."),
            ("comercial", "COMERCIAL", "Si el proceso de ventas está documentado, si conoces tu conversión y si puedes predecir los ingresos del mes."),
            ("procesos", "PROCESOS", "Si los procesos principales están documentados y cuánto trabajo repetitivo sigue haciéndose a mano."),
            ("operacion", "OPERACIÓN", "Si la empresa opera sin ti dos semanas, si mides la eficiencia y si podrías duplicar volumen sin contratar."),
            ("personas", "PERSONAS", "Si hay evaluación de desempeño formal y si existe un proceso de incorporación para quien entra."),
            ("control", "CONTROL", "Si revisas resultados, si conoces tu margen, si tienes presupuesto con seguimiento y si decides con datos."),
        ],
        "cierre": "Termina el radar y llévalo a una conversación",
        "cierre_lead": "El radar te dice dónde mirar. El diagnóstico SYNKA se hace con el dueño "
                       "y las áreas clave, sobre tu operación real, y termina con el orden en "
                       "que se resuelve.",
        "cruzada": ("Ya sabes que el problema es comercial",
                    "Si el radar señala COMERCIAL, el siguiente paso es el diagnóstico de esa división: seis áreas, diez preguntas.",
                    "comercial", "Ir al Diagnóstico Comercial"),
    },
    {
        "slug": "comercial",
        "quiz": "comercial",
        "datos": "datos-comercial.js",
        "marca_700": "COMERCIAL",
        "marca_300": "DIAGNÓSTICO",
        "titulo_seo": "Diagnóstico Comercial · Sistema de ventas y procesos",
        "meta": "Autoevaluación de 10 preguntas que mide tu sistema de ventas en seis áreas: prospección, independencia, métricas, predictibilidad, seguimiento y cierre.",
        "eyebrow": "Nivel 2 · SYNKA COMERCIAL · 10 preguntas · unos 3 minutos",
        "h1": "¿Dónde se te van las ventas cada mes?",
        "entrada": "Diez preguntas directas sobre cómo vende tu empresa hoy. Al terminar sabes "
                   "en cuál de las seis áreas del sistema comercial está la fuga, con un "
                   "semáforo por área y tus tres puntos más débiles.",
        "que_mide_titulo": "Las seis áreas del sistema comercial",
        "que_mide_lead": "Estas seis áreas son la anatomía de una sola división: SYNKA COMERCIAL. "
                         "Medirlas por separado es lo que permite saber dónde intervenir primero.",
        "ejes": [
            ("comercial", "PROSPECCIÓN", "De dónde vienen tus clientes nuevos y si llegan por método o por coincidencia."),
            ("comercial", "INDEPENDENCIA", "Si alguien más puede ejecutar el proceso de ventas cuando tú no estás."),
            ("comercial", "MÉTRICAS", "Si sabes cuántos prospectos entran al mes y cuál es tu tasa de conversión."),
            ("comercial", "PREDICTIBILIDAD", "Si puedes proyectar hoy cuánto va a entrar el mes que viene."),
            ("comercial", "SEGUIMIENTO", "Qué pasa con los prospectos que piden precio y no compran de inmediato."),
            ("comercial", "CIERRE", "Si hay un proceso claro de propuesta, precio y cierre, o se improvisa cada vez."),
        ],
        "cierre": "Sabes dónde está la fuga. Falta cerrarla",
        "cierre_lead": "El diagnóstico te muestra el área. SYNKA COMERCIAL instala el proceso, "
                       "el pipeline y el control que hacen que las ventas dejen de depender de "
                       "que tú vendas.",
        "cruzada": ("¿Y el resto de la empresa?",
                    "Si quieres el mapa completo de las seis divisiones, empieza por el radar.",
                    "radar", "Ir al Radar SYNKA"),
    },
]

PLANTILLA = """<!DOCTYPE html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>{titulo_seo}</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="{sitio}/diagnostico/{slug}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#002B49">

<link rel="preload" href="../assets/fonts/archivo-var-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../assets/fonts/plexmono-400-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../css/synka.css">

<link rel="icon" href="../assets/logo/favicon-32.svg" type="image/svg+xml">
<link rel="icon" href="../assets/img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="../assets/img/avatar-1024.png">
<link rel="manifest" href="../site.webmanifest">

<meta property="og:type" content="website">
<meta property="og:locale" content="es_MX">
<meta property="og:site_name" content="SYNKA">
<meta property="og:title" content="{titulo_seo}">
<meta property="og:description" content="{meta}">
<meta property="og:url" content="{sitio}/diagnostico/{slug}">
<meta property="og:image" content="{sitio}/assets/img/og-synka.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{titulo_seo}">
<meta name="twitter:description" content="{meta}">
<meta name="twitter:image" content="{sitio}/assets/img/og-synka.png">

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "WebApplication",
      "name": "{nombre_plano}",
      "applicationCategory": "BusinessApplication",
      "operatingSystem": "Web",
      "url": "{sitio}/diagnostico/{slug}",
      "description": "{meta}",
      "inLanguage": "es-MX",
      "isAccessibleForFree": true,
      "offers": {{ "@type": "Offer", "price": "0", "priceCurrency": "MXN" }},
      "publisher": {{ "@type": "Organization", "name": "SYNKA", "url": "{sitio}/" }}
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Inicio", "item": "{sitio}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Diagnóstico", "item": "{sitio}/#diagnostico" }},
        {{ "@type": "ListItem", "position": 3, "name": "{nombre_plano}", "item": "{sitio}/diagnostico/{slug}" }}
      ]
    }}
  ]
}}
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

<section class="hero seccion--navy">
  <div class="wrap hero__grid">
    <div>
      <p class="eyebrow">{eyebrow}</p>
      <p class="marca-division" style="font-size:clamp(1.4rem,4vw,1.9rem); margin-bottom:1.5rem; color:var(--blanco)">
        <span>{marca_300}</span> <b>{marca_700}</b><sup aria-hidden="true">&trade;</sup>
      </p>
      <h1>{h1}</h1>
      <p class="lead" style="margin-top:1.5rem">{entrada}</p>
      <div class="grupo-cta" style="margin-top:clamp(2rem,5vw,2.75rem)">
        <a class="btn btn--primario" href="#instrumento" data-cta="empezar_{slug}" data-seccion="hero">Empezar</a>
        <a class="enlace-linea" href="#que-mide" data-cta="que_mide" data-seccion="hero">Ver qué mide {flecha}</a>
      </div>
    </div>
    <div class="hero__signo">
      {signo}
    </div>
  </div>
</section>

<section class="seccion seccion--arena" id="instrumento">
  <div class="wrap">
    <div class="diag quiz" data-quiz="{quiz}">
      <div class="diag__barra">
        <span data-paso>01 / {total}</span>
        <span class="diag__pista" aria-hidden="true"><span class="diag__avance" data-avance></span></span>
      </div>

      <div class="diag__sin-js" data-sin-js>
        <h2 style="margin-bottom:1rem">Autoevaluación</h2>
        <p style="margin-bottom:1.5rem">Este instrumento necesita JavaScript. Puedes responder
          estas mismas preguntas con nosotros durante el diagnóstico.</p>
        <a class="btn btn--primario" href="/#solicitar" data-cta="solicitar_diagnostico" data-seccion="{slug}_sin_js">Solicitar diagnóstico</a>
      </div>

      <div class="diag__cuerpo" data-vista-pregunta hidden>
        <fieldset class="diag__pregunta">
          <legend data-legend></legend>
          <p class="quiz__ayuda" data-ayuda hidden></p>
          <div class="quiz__opciones" data-opciones role="group" aria-label="Opciones de respuesta"></div>
        </fieldset>
        <div class="diag__pie">
          <button type="button" class="diag__atras" data-atras hidden>&larr; Anterior</button>
        </div>
      </div>

      <div class="diag__cuerpo diag__resultado" data-vista-resultado tabindex="-1" role="status" aria-live="polite"></div>
    </div>
  </div>
</section>

<section class="seccion seccion--navy seccion--linea" id="que-mide">
  <div class="wrap">
    <div class="encabezado-seccion">
      <p class="eyebrow">Qué mide</p>
      <h2>{que_mide_titulo}</h2>
      <p class="lead">{que_mide_lead}</p>
    </div>
    <div class="reticula reticula--3">
{ejes}
    </div>
  </div>
</section>

<section class="seccion seccion--blanco">
  <div class="wrap">
    <div class="encabezado-seccion">
      <p class="eyebrow">Siguiente instrumento</p>
      <h2>{cruz_titulo}</h2>
      <p class="lead">{cruz_texto}</p>
    </div>
    <a class="btn btn--fantasma" href="{cruz_url}" data-cta="instrumento_cruzado" data-seccion="{slug}">{cruz_cta}</a>
  </div>
</section>

<section class="seccion seccion--hundida">
  <div class="wrap centrado" style="max-width:760px">
    <p class="eyebrow" style="justify-content:center">El siguiente paso</p>
    <h2>{cierre}</h2>
    <p class="lead" style="margin-top:1.25rem">{cierre_lead}</p>
    <div class="grupo-cta" style="justify-content:center; margin-top:2.25rem">
      <a class="btn btn--primario" href="/#solicitar" data-cta="solicitar_diagnostico" data-seccion="cta_final_{slug}">Solicita tu diagnóstico</a>
      <a class="enlace-linea" href="/#soluciones" data-cta="ver_soluciones" data-seccion="cta_final_{slug}">Ver las seis divisiones {flecha}</a>
    </div>
  </div>
</section>

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
        <h4>Diagnóstico</h4>
        <ul>
          <li><a href="/#diagnostico">Autoevaluación de dependencia</a></li>
          <li><a href="radar">Radar SYNKA</a></li>
          <li><a href="comercial">Diagnóstico Comercial</a></li>
        </ul>
      </div>
      <div>
        <h4>Navegación</h4>
        <ul>
          <li><a href="/#metodo">Método SYNKA</a></li>
          <li><a href="/#soluciones">Soluciones</a></li>
          <li><a href="/#nosotros">Nosotros</a></li>
          <li><a href="mailto:hola@synka.mx" data-correo data-rellena>hola@synka.mx</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__base">
      <span>&copy; <span id="anio">{anio}</span> SYNKA</span>
      <span>Todo funcionando como uno</span>
    </div>
  </div>
</footer>

<script>document.getElementById('anio').textContent = new Date().getFullYear();</script>
<script src="../js/synka.js" defer></script>
<script src="../js/{datos}" defer></script>
<script src="../js/quiz.js" defer></script>
</body>
</html>
"""

FLECHA = ('<svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true">'
          '<path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.6"/></svg>')


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def total_preguntas(slug):
    import json
    f = "radar.json" if slug == "radar" else "comercial.json"
    with open(os.path.join(RAIZ, "_source", "preguntas", f), encoding="utf-8") as fh:
        return len(json.load(fh))


def construir(ins):
    ejes = "\n".join(
        '      <article class="tarjeta aparece" style="--rama:var(--div-{rama}-neg)">\n'
        '        <h3 class="marca-division" style="color:var(--blanco); margin-bottom:.85rem">'
        '<span style="color:var(--rama)">{nom}</span></h3>\n'
        '        <p>{desc}</p>\n'
        '      </article>'.format(rama=rama, nom=nom, desc=esc(desc))
        for rama, nom, desc in ins["ejes"]
    )
    ct, cx, cu, cc = ins["cruzada"]
    return PLANTILLA.format(
        sitio=SITIO,
        slug=ins["slug"],
        quiz=ins["quiz"],
        datos=ins["datos"],
        total="{:02d}".format(total_preguntas(ins["slug"])),
        nombre_plano="{} {}".format(ins["marca_300"].title(), ins["marca_700"].title()),
        titulo_seo=esc(ins["titulo_seo"]),
        meta=esc(ins["meta"]),
        eyebrow=esc(ins["eyebrow"]),
        marca_300=ins["marca_300"],
        marca_700=ins["marca_700"],
        h1=esc(ins["h1"]),
        entrada=esc(ins["entrada"]),
        que_mide_titulo=esc(ins["que_mide_titulo"]),
        que_mide_lead=esc(ins["que_mide_lead"]),
        ejes=ejes,
        cruz_titulo=esc(ct), cruz_texto=esc(cx), cruz_url=cu, cruz_cta=esc(cc),
        cierre=esc(ins["cierre"]),
        cierre_lead=esc(ins["cierre_lead"]),
        logo=LOGO, signo=SIGNO_GRANDE, flecha=FLECHA,
        anio=datetime.date.today().year,
    )


def main():
    destino = os.path.join(RAIZ, "diagnostico")
    os.makedirs(destino, exist_ok=True)
    for ins in INSTRUMENTOS:
        ruta = os.path.join(destino, ins["slug"] + ".html")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(construir(ins))
        print("escrito  diagnostico/{}.html".format(ins["slug"]))


if __name__ == "__main__":
    main()
