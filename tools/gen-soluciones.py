#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera las seis landings de división y el sitemap.

Las seis páginas comparten la misma estructura y solo cambian en contenido y
color de rama. Se generan desde aquí para que no puedan divergir entre sí:
editar los datos de abajo y volver a ejecutar.

    python3 tools/gen-soluciones.py

Los colores y descriptores salen del Manual de Identidad SYNKA, cap. 09.
No se declara ningún resultado, cifra ni cliente.
"""

import os
import datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITIO = "https://synka.mx"

# El isotipo de división: geometría literal del SVG oficial. El brazo superior
# es blanco y el inferior toma el color de la rama vía currentColor.
SIGNO = """<svg viewBox="0 0 100 100" style="color:var(--rama)" aria-hidden="true" focusable="false">
        <g><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="currentColor"/></g>
        <g transform="rotate(90 50 50)"><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="currentColor"/></g>
        <g transform="rotate(180 50 50)"><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="currentColor"/></g>
        <g transform="rotate(270 50 50)"><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="currentColor"/></g>
      </svg>"""

LOGO_HEADER = """<svg viewBox="0 0 100 100" aria-hidden="true" focusable="false">
        <g><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="#00C9B7"/></g>
        <g transform="rotate(90 50 50)"><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="#00C9B7"/></g>
        <g transform="rotate(180 50 50)"><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="#00C9B7"/></g>
        <g transform="rotate(270 50 50)"><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="#00C9B7"/></g>
      </svg>"""

FLECHA = ('<svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true">'
          '<path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.6"/></svg>')

DIVISIONES = [
    {
        "slug": "estructura",
        "nombre": "ESTRUCTURA",
        "descriptor": "Organización, roles y responsabilidades",
        "titulo_seo": "SYNKA Estructura · Organigrama, roles y niveles de decisión",
        "meta": "Definimos el organigrama real de tu empresa, los roles, las responsabilidades y los niveles de decisión para que las decisiones dejen de regresar al dueño.",
        "h1": "Que las decisiones dejen de regresar a ti",
        "entrada": "Una empresa sin estructura no es una empresa desordenada: es una empresa donde nadie sabe hasta dónde puede decidir. Por eso todo sube.",
        "sintomas": [
            "Tu equipo te consulta decisiones que ya deberían resolverse sin ti.",
            "Hay funciones que nadie tiene formalmente asignadas.",
            "El organigrama que existe en papel no es el que opera en la realidad.",
            "Dos personas creen que la misma tarea es responsabilidad de la otra.",
        ],
        "instalamos": [
            ("Organigrama real", "El que refleja cómo opera hoy la empresa, no el que se dibujó cuando eran cinco personas."),
            ("Roles y responsabilidades", "Qué hace cada puesto, de qué responde y qué entrega, por escrito."),
            ("Niveles de decisión", "Qué se decide en cada nivel y con qué monto o criterio, para que la excepción deje de subir."),
            ("Matriz de responsabilidad", "Quién ejecuta, quién aprueba y a quién se informa en cada proceso clave."),
        ],
    },
    {
        "slug": "comercial",
        "nombre": "COMERCIAL",
        "descriptor": "Sistema y control de ventas",
        "titulo_seo": "SYNKA Comercial · Procesos comerciales, pipeline y cuotas",
        "meta": "Instalamos el proceso comercial, el pipeline, las cuotas y el control de ventas para que la operación comercial no dependa del dueño vendiendo.",
        "h1": "Que las ventas no dependan de que tú vendas",
        "entrada": "Cuando el mejor vendedor de la empresa es el dueño, no hay área comercial: hay una persona con agenda llena y un equipo esperando instrucciones.",
        "sintomas": [
            "Los cierres importantes solo se dan si tú entras a la reunión.",
            "Cada vendedor sigue su propio método y sus propios argumentos.",
            "No sabes cuánto hay realmente en el pipeline ni en qué etapa está.",
            "El pronóstico de ventas es una intuición, no un cálculo.",
        ],
        "instalamos": [
            ("Proceso comercial documentado", "Etapas, criterios de avance y qué tiene que ser cierto para pasar de una a la siguiente."),
            ("Pipeline y pronóstico", "Registro único de oportunidades con etapas definidas y probabilidad asignada por criterio, no por optimismo."),
            ("Cuotas y metas", "Objetivos por vendedor y por periodo, con la actividad mínima que los sostiene."),
            ("Control comercial", "Rutina de seguimiento con indicadores de actividad y de resultado."),
        ],
    },
    {
        "slug": "procesos",
        "nombre": "PROCESOS",
        "descriptor": "Estandarización y documentación",
        "titulo_seo": "SYNKA Procesos · Estandarización y documentación de procesos",
        "meta": "Mapeamos flujos y documentamos procedimientos (SOP y POE) para que cualquier persona del equipo pueda ejecutar el proceso igual, sin depender de quién lo hace.",
        "h1": "Que el proceso no viva en la cabeza de una persona",
        "entrada": "Un proceso que solo una persona conoce no es un proceso: es un riesgo con nombre y apellido.",
        "sintomas": [
            "Si esa persona se va o se enferma, el proceso se va con ella.",
            "Cada colaborador ejecuta la misma tarea de manera distinta.",
            "Entrenar a alguien nuevo depende de que otro se siente a explicarle.",
            "Los errores se repiten porque nunca quedó escrito cómo evitarlos.",
        ],
        "instalamos": [
            ("Mapeo de flujos", "Cómo corre el trabajo hoy de principio a fin, con sus tiempos, entregas y puntos de bloqueo."),
            ("Procedimientos documentados", "SOP y POE con responsable, frecuencia e indicador, en el formato de la casa."),
            ("Estándares de ejecución", "Qué se considera bien hecho, para que la calidad no dependa de quién ejecutó."),
            ("Documentación operativa", "El acervo ordenado y accesible, no una carpeta que nadie abre."),
        ],
    },
    {
        "slug": "operacion",
        "nombre": "OPERACIÓN",
        "descriptor": "Funcionamiento y ejecución diaria",
        "titulo_seo": "SYNKA Operación · Ejecución diaria y estándares de servicio",
        "meta": "Ordenamos la ejecución diaria de la empresa y los estándares de servicio para que la operación se sostenga sin supervisión permanente del dueño.",
        "h1": "Que la operación aguante cuando no estás",
        "entrada": "La prueba de una operación no es cómo se ve cuando todos están atentos. Es qué pasa la semana que el dueño no aparece.",
        "sintomas": [
            "Si te ausentas unos días, algo se cae o se atrasa.",
            "La operación se sostiene por supervisión, no por método.",
            "Las urgencias desplazan al plan casi todos los días.",
            "Las áreas se enteran tarde de lo que decidió la otra.",
        ],
        "instalamos": [
            ("Ritmo operativo", "Qué se revisa cada día, cada semana y cada mes, con quién y para decidir qué."),
            ("Estándares de servicio", "Tiempos de respuesta y niveles de cumplimiento comprometidos y medibles."),
            ("Coordinación entre áreas", "Los puntos de entrega entre ventas, operación y administración, definidos como contratos internos."),
            ("Escalamiento", "Qué se resuelve en el piso, qué sube y en cuánto tiempo."),
        ],
    },
    {
        "slug": "personas",
        "nombre": "PERSONAS",
        "descriptor": "Responsabilidades, desempeño y equipo",
        "titulo_seo": "SYNKA Personas · Perfiles de puesto, evaluación y desarrollo",
        "meta": "Definimos perfiles de puesto, criterios de evaluación y planes de desarrollo para que el equipo pueda sostener el sistema que se instala.",
        "h1": "Que el equipo pueda sostener el sistema",
        "entrada": "Ningún proceso se sostiene solo. Se sostiene porque alguien tiene el perfil, el criterio y la responsabilidad para ejecutarlo.",
        "sintomas": [
            "Contratas por urgencia y descubres el perfil sobre la marcha.",
            "No hay una conversación de desempeño más allá de la corrección puntual.",
            "El buen desempeño y el malo reciben la misma respuesta: ninguna.",
            "Nadie sabe qué tiene que lograr para crecer dentro de la empresa.",
        ],
        "instalamos": [
            ("Perfiles de puesto", "Qué tiene que saber hacer, qué tiene que entregar y con qué se mide cada posición."),
            ("Evaluación de desempeño", "Criterios objetivos y una rutina de conversación que no dependa del ánimo del mes."),
            ("Plan de desarrollo", "Qué necesita aprender cada persona para sostener su parte del sistema."),
            ("Incorporación", "Cómo entra alguien nuevo y en cuánto tiempo debe estar operando solo."),
        ],
    },
    {
        "slug": "control",
        "nombre": "CONTROL",
        "descriptor": "Indicadores y toma de decisiones",
        "titulo_seo": "SYNKA Control · Indicadores, tablero y auditoría empresarial",
        "meta": "Construimos el sistema de indicadores, el tablero de control y la rutina de auditoría para saber cómo va la empresa sin tener que preguntar.",
        "h1": "Que sepas cómo va la empresa sin preguntar",
        "entrada": "Sin indicadores, dirigir es opinar. La información llega tarde, por comentario, y casi siempre cuando ya no hay margen de maniobra.",
        "sintomas": [
            "Te enteras de los problemas cuando ya son problemas.",
            "Cada área reporta con sus propios números y no cuadran entre sí.",
            "Revisas resultados al cierre de mes y ya no hay nada que corregir.",
            "Las decisiones importantes se toman con percepción, no con dato.",
        ],
        "instalamos": [
            ("Sistema de indicadores", "Los pocos números que de verdad explican cómo va la empresa, con su definición y su fuente."),
            ("Tablero de control", "Un solo lugar donde se ve el estado real, actualizado con una frecuencia que permita corregir."),
            ("Rutina de seguimiento", "La reunión de dirección con agenda fija y decisiones que quedan registradas."),
            ("Auditoría interna", "Verificación periódica de que el proceso documentado es el que se está ejecutando."),
        ],
    },
]

PLANTILLA = """<!DOCTYPE html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>{titulo_seo}</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="{sitio}/soluciones/{slug}.html">
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
<meta property="og:title" content="SYNKA {nombre} · {descriptor}">
<meta property="og:description" content="{meta}">
<meta property="og:url" content="{sitio}/soluciones/{slug}.html">
<meta property="og:image" content="{sitio}/assets/img/og-synka.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="SYNKA {nombre} · {descriptor}">
<meta name="twitter:description" content="{meta}">
<meta name="twitter:image" content="{sitio}/assets/img/og-synka.png">

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "Service",
      "name": "SYNKA {nombre}",
      "serviceType": "{descriptor}",
      "description": "{meta}",
      "url": "{sitio}/soluciones/{slug}.html",
      "provider": {{
        "@type": "Organization",
        "name": "SYNKA",
        "url": "{sitio}/"
      }},
      "areaServed": {{ "@type": "Country", "name": "México" }}
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Inicio", "item": "{sitio}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Soluciones", "item": "{sitio}/#soluciones" }},
        {{ "@type": "ListItem", "position": 3, "name": "SYNKA {nombre}", "item": "{sitio}/soluciones/{slug}.html" }}
      ]
    }}
  ]
}}
</script>

<script src="../js/config.js"></script>
</head>

<body style="--rama: var(--div-{slug}-neg)">
<a class="salta-al-contenido" href="#contenido">Saltar al contenido</a>

<header class="header">
  <div class="wrap header__barra">
    <a class="logotipo" href="../index.html" aria-label="SYNKA · Inicio">
      {logo}
      <span class="logotipo__palabra">SYNKA</span>
    </a>

    <nav class="nav" aria-label="Principal">
      <ul class="nav__lista">
        <li><a class="nav__enlace" href="../index.html#problema">El problema</a></li>
        <li><a class="nav__enlace" href="../index.html#metodo">Método SYNKA</a></li>
        <li><a class="nav__enlace" href="../index.html#soluciones">Soluciones</a></li>
        <li><a class="nav__enlace" href="../index.html#resultados">Resultados</a></li>
        <li><a class="nav__enlace" href="../index.html#nosotros">Nosotros</a></li>
        <li><a class="nav__enlace" href="../index.html#diagnostico">Diagnóstico</a></li>
      </ul>
      <a class="btn btn--primario" href="#solicitar" data-cta="solicitar_diagnostico" data-seccion="header">Solicitar diagnóstico</a>
    </nav>

    <button class="menu-btn" type="button" data-menu-btn aria-expanded="false" aria-controls="menu-movil" aria-label="Abrir menú">
      <span></span><span></span><span></span>
    </button>
    <span class="progreso" data-progreso aria-hidden="true"></span>
  </div>

  <div class="wrap menu-movil" id="menu-movil" data-menu data-abierto="false">
    <nav aria-label="Principal, versión móvil">
      <ul>
        <li><a href="../index.html#problema">El problema</a></li>
        <li><a href="../index.html#metodo">Método SYNKA</a></li>
        <li><a href="../index.html#soluciones">Soluciones</a></li>
        <li><a href="../index.html#resultados">Resultados</a></li>
        <li><a href="../index.html#nosotros">Nosotros</a></li>
        <li><a href="../index.html#diagnostico">Diagnóstico</a></li>
      </ul>
      <a class="btn btn--primario btn--bloque" href="#solicitar" data-cta="solicitar_diagnostico" data-seccion="menu_movil">Solicitar diagnóstico</a>
    </nav>
  </div>
</header>

<main id="contenido">

<section class="hero seccion--navy">
  <div class="wrap hero__grid">
    <div>
      <nav class="eyebrow" aria-label="Ruta de navegación" style="margin-bottom:1.75rem">
        <a href="../index.html#soluciones" style="color:inherit">Soluciones</a>
      </nav>

      <p class="marca-division" style="font-size:clamp(1.4rem,4vw,1.9rem); margin-bottom:1.5rem; color:var(--blanco)">
        <b>SYNKA</b> <span style="color:var(--rama)">{nombre}</span><sup aria-hidden="true">&trade;</sup>
      </p>

      <h1>{h1}</h1>

      <p class="lead" style="margin-top:1.5rem">{entrada}</p>

      <div class="grupo-cta" style="margin-top:clamp(2rem,5vw,2.75rem)">
        <a class="btn btn--primario" href="#solicitar" data-cta="solicitar_diagnostico" data-seccion="hero_{slug}">Solicita tu diagnóstico</a>
        <a class="enlace-linea" href="../index.html#metodo" data-cta="conoce_metodo" data-seccion="hero_{slug}">Conoce el Método SYNKA {flecha}</a>
      </div>
    </div>

    <div class="hero__signo">
      {signo}
    </div>
  </div>
</section>

<section class="seccion seccion--arena">
  <div class="wrap">
    <div class="encabezado-seccion">
      <p class="eyebrow">Esto es para ti si</p>
      <h2>Señales de que {nombre_min} es tu punto de dependencia</h2>
    </div>
    <ul class="sintomas">
{sintomas}
    </ul>
  </div>
</section>

<section class="seccion seccion--blanco">
  <div class="wrap">
    <div class="encabezado-seccion">
      <p class="eyebrow">Qué instalamos</p>
      <h2>{descriptor}</h2>
      <p class="lead">El entregable no es un documento: es una forma de operar que se
        ejecuta distinto la semana siguiente, con responsables e indicadores asignados.</p>
    </div>
    <div class="pasos pasos--2">
{instalamos}
    </div>
  </div>
</section>

<section class="seccion seccion--navy seccion--linea">
  <div class="wrap">
    <div class="encabezado-seccion">
      <p class="eyebrow">Dónde encaja</p>
      <h2>Una división no se vende sola</h2>
      <p class="lead">SYNKA {nombre_min} entra donde el diagnóstico la señala, sola o junto
        con otras divisiones. Arreglar un área aislada normalmente solo mueve el cuello de
        botella de lugar.</p>
    </div>
    <div class="divisiones">
{otras}
    </div>
  </div>
</section>

<section class="seccion seccion--hundida" id="solicitar">
  <div class="wrap centrado" style="max-width:760px">
    <p class="eyebrow" style="justify-content:center">El siguiente paso</p>
    <h2>¿Cuánto de tu empresa todavía depende de ti?</h2>
    <p class="lead" style="margin-top:1.25rem">Empieza por el diagnóstico. Es una sesión de
      trabajo con el dueño y las áreas clave, sobre tu operación real.</p>
    <div class="grupo-cta" style="justify-content:center; margin-top:2.25rem">
      <a class="btn btn--primario" href="../index.html#solicitar" data-cta="solicitar_diagnostico" data-seccion="cta_final_{slug}">Solicita tu diagnóstico</a>
      <a class="enlace-linea" href="{instrumento_url}" data-cta="instrumento" data-seccion="cta_final_{slug}">{instrumento_texto} {flecha}</a>
    </div>
  </div>
</section>

</main>

<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <a class="logotipo" href="../index.html" aria-label="SYNKA · Inicio">
          {logo}
          <span class="logotipo__palabra">SYNKA</span>
        </a>
        <p class="footer__descriptor">Sistemas que hacen funcionar tu empresa</p>
      </div>
      <div>
        <h4>Soluciones</h4>
        <ul>
{pie_soluciones}
        </ul>
      </div>
      <div>
        <h4>Navegación</h4>
        <ul>
          <li><a href="../index.html#problema">El problema</a></li>
          <li><a href="../index.html#metodo">Método SYNKA</a></li>
          <li><a href="../index.html#resultados">Resultados</a></li>
          <li><a href="../index.html#nosotros">Nosotros</a></li>
          <li><a href="../diagnostico/radar.html">Radar SYNKA</a></li>
          <li><a href="../diagnostico/comercial.html">Diagnóstico Comercial</a></li>
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
</body>
</html>
"""


def escapar(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def construir(d, todas):
    sintomas = "\n".join(
        '      <li class="sintoma aparece"><span class="sintoma__n">{:02d}</span>'
        '<span class="sintoma__frase">{}</span></li>'.format(i + 1, escapar(s))
        for i, s in enumerate(d["sintomas"])
    )

    instalamos = "\n".join(
        '      <article class="paso aparece">\n'
        '        <span class="paso__n">{:02d}</span>\n'
        '        <h3>{}</h3>\n'
        '        <p>{}</p>\n'
        '      </article>'.format(i + 1, escapar(t), escapar(p))
        for i, (t, p) in enumerate(d["instalamos"])
    )

    otras = "\n".join(
        '      <a class="division aparece" data-rama="{s}" href="{s}.html" data-cta="division" data-seccion="cruzada">\n'
        '        <svg class="division__signo" viewBox="0 0 100 100" style="color:var(--rama)" aria-hidden="true" focusable="false">\n'
        '          <g><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="currentColor"/></g>\n'
        '          <g transform="rotate(90 50 50)"><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="currentColor"/></g>\n'
        '          <g transform="rotate(180 50 50)"><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="currentColor"/></g>\n'
        '          <g transform="rotate(270 50 50)"><polygon points="36,50 8,22 8,39 19,50" fill="#FFFFFF"/><polygon points="36,50 8,78 8,61 19,50" fill="currentColor"/></g>\n'
        '        </svg>\n'
        '        <h3 class="marca-division division__nombre"><b>SYNKA</b> <span>{n}</span><sup aria-hidden="true">&trade;</sup></h3>\n'
        '        <p>{desc}.</p>\n'
        '        <span class="division__ir">Ver división <svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
        '<path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.8"/></svg></span>\n'
        '      </a>'.format(s=o["slug"], n=o["nombre"], desc=escapar(o["descriptor"]))
        for o in todas if o["slug"] != d["slug"]
    )

    pie = "\n".join(
        '          <li><a href="{}.html">SYNKA {}</a></li>'.format(o["slug"], o["nombre"].capitalize())
        for o in todas
    )

    # La única división con instrumento propio hoy es COMERCIAL. El resto
    # manda al radar, que es el que mide las seis a la vez.
    if d["slug"] == "comercial":
        inst_url, inst_txt = "../diagnostico/comercial.html", "Hacer el Diagnóstico Comercial"
    else:
        inst_url, inst_txt = "../diagnostico/radar.html", "Medir esta división en el Radar SYNKA"

    return PLANTILLA.format(
        instrumento_url=inst_url,
        instrumento_texto=inst_txt,
        sitio=SITIO,
        slug=d["slug"],
        nombre=d["nombre"],
        nombre_min=d["nombre"].capitalize(),
        descriptor=escapar(d["descriptor"]),
        titulo_seo=escapar(d["titulo_seo"]),
        meta=escapar(d["meta"]),
        h1=escapar(d["h1"]),
        entrada=escapar(d["entrada"]),
        sintomas=sintomas,
        instalamos=instalamos,
        otras=otras,
        pie_soluciones=pie,
        logo=LOGO_HEADER,
        signo=SIGNO,
        flecha=FLECHA,
        anio=datetime.date.today().year,
    )


def sitemap():
    hoy = datetime.date.today().isoformat()
    urls = [(SITIO + "/", "1.0")]
    urls += [("{}/soluciones/{}.html".format(SITIO, d["slug"]), "0.8") for d in DIVISIONES]
    urls += [("{}/diagnostico/radar.html".format(SITIO), "0.9"),
             ("{}/diagnostico/comercial.html".format(SITIO), "0.9")]
    filas = "\n".join(
        "  <url>\n    <loc>{}</loc>\n    <lastmod>{}</lastmod>\n"
        "    <changefreq>monthly</changefreq>\n    <priority>{}</priority>\n  </url>".format(u, hoy, p)
        for u, p in urls
    )
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + filas + "\n</urlset>\n")


def main():
    destino = os.path.join(RAIZ, "soluciones")
    os.makedirs(destino, exist_ok=True)
    for d in DIVISIONES:
        ruta = os.path.join(destino, d["slug"] + ".html")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(construir(d, DIVISIONES))
        print("escrito  soluciones/{}.html".format(d["slug"]))

    with open(os.path.join(RAIZ, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap())
    print("escrito  sitemap.xml")


if __name__ == "__main__":
    main()
