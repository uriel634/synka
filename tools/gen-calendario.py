#!/usr/bin/env python3
"""Genera el calendario de publicaciones del mes de lanzamiento.

Uso:  python3 tools/gen-calendario.py
Salida:
  marketing/calendario/calendario-publicaciones.csv   (para importar en Metricool, Buffer, etc.)
  marketing/calendario/semana-1.md ... semana-4.md    (texto listo para copiar y pegar)

Una sola fuente de verdad: se edita PUBLICACIONES y se vuelve a correr.
Los guiones de los reels están en marketing/guiones-reels.md (se citan como R1, R2...).
"""
import csv, os, datetime as dt
from urllib.parse import urlencode

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, 'marketing', 'calendario')

SITIO = 'https://synka.mx'
ART = SITIO + '/blog/senales-empresa-depende-del-dueno'
RADAR = SITIO + '/diagnostico/radar'
COMERCIAL = SITIO + '/diagnostico/comercial'

def utm(base, fuente, medio, campana, contenido):
    return base + '?' + urlencode({'utm_source': fuente, 'utm_medium': medio,
                                   'utm_campaign': campana, 'utm_content': contenido})

LI, IGS, IGU, GBP, WEB = 'LinkedIn (Uriel)', 'Instagram SYNKA', 'Instagram Uriel', 'Perfil de Empresa en Google', 'Sitio'
HASH_IG = '#PyMEsMéxico #DueñosDeNegocio #Empresarios #ProcesosEmpresariales #LiderazgoEmpresarial'
HASH_LI = '#PyMEs #Empresarios #Liderazgo'

V = 'marketing/visuales/'
def lam(carrusel, n):
    return [f'{V}{carrusel}/{i:02d}.png' for i in range(1, n + 1)]

# ---------------------------------------------------------------------------
# fecha, hora (CDMX), cuenta, formato, título, texto, archivos, enlace, dónde va el enlace, nota
# ---------------------------------------------------------------------------
P = []
def add(fecha, hora, cuenta, formato, titulo, texto='', archivos=None, enlace='', donde='', nota=''):
    P.append(dict(fecha=fecha, hora=hora, cuenta=cuenta, formato=formato, titulo=titulo, texto=texto.strip(),
                  archivos=archivos or [], enlace=enlace, donde=donde, nota=nota))

# ============================ SEMANA 1 · lanzamiento del artículo ============================
add('2026-11-09', '09:00', WEB, 'Tarea', 'Biografías de Instagram + comprobar indexación',
    nota='El artículo ya está publicado desde el 25 de octubre. En Search Console, comprobar que figura como indexado '
         '(si no, pedir indexación). Cambiar el enlace de la biografía de Instagram (SYNKA y Uriel) al artículo.')

add('2026-11-10', '08:30', LI, 'Carrusel (PDF o imágenes)', '7 señales de que tu empresa depende de ti',
    f'''Si en tu empresa pasa alguna de estas 7 cosas, tu empresa depende de ti.

Una o dos son normales: así crecen muchas PyMEs.
Tres o más indican que la dependencia ya frena el crecimiento.

Desliza y cuenta cuántas reconoces. Cada una apunta a una de las seis áreas de la empresa, así que sabrás también dónde empezar.

¿Cuántas fueron? Cuéntame en comentarios.

{HASH_LI}''',
    lam('senales', 9), utm(ART, 'linkedin', 'social', 'senales-nov26', 'articulo-7-senales'), 'primer comentario',
    'Comentario: «Artículo completo, con el primer paso para cada señal: {enlace}». Subir las 9 imágenes como documento PDF o como imágenes múltiples.')

add('2026-11-10', '12:00', IGS, 'Carrusel', '7 señales de que tu empresa depende de ti',
    f'''7 señales de que tu empresa depende de ti.

Una o dos son normales. Tres o más indican que la dependencia ya frena el crecimiento.

Guarda este carrusel, cuenta cuántas reconoces y compártelo con otro dueño de negocio.

Artículo completo con el primer paso para cada señal: enlace en la bio.

{HASH_IG}''',
    lam('senales', 9), utm(ART, 'instagram-synka', 'bio', 'senales-nov26', 'articulo-7-senales'), 'biografía',
    'Instagram no permite enlaces en el pie de foto: la biografía ya debe apuntar al artículo (ver tarea del lunes).')

add('2026-11-10', '12:10', IGU, 'Historias (3 cuadros)', 'Aviso personal del artículo',
    '''Cuadro 1 (a cámara, 10 s): «Llevo tiempo pensando en esto y por fin lo escribí: las 7 señales de que una empresa depende de su dueño.»
Cuadro 2 (captura del carrusel): «Si tienes un negocio, cuenta cuántas reconoces.»
Cuadro 3 (texto sobre fondo navy): «Si quieres medir dónde se concentra, hay un Radar de 5 minutos. Gratis.» + sticker de enlace.''',
    lam('senales', 1), utm(ART, 'instagram-uriel', 'historia', 'senales-nov26', 'articulo-7-senales'), 'sticker de enlace (cuadro 3)',
    'Pedir de forma directa y breve: «Si lo lees, dime qué señal te tocó». Responder todos los mensajes ese día.')

add('2026-11-11', '08:30', LI, 'Texto', 'La prueba de una pregunta',
    f'''Hagamos una prueba de una pregunta.

Si te ausentas dos semanas, sin celular, ¿qué se detiene?

→ Si la respuesta es «nada», es poco común.
→ Si es «las cotizaciones», «los pagos», «las quejas de clientes» o «todo»: ahí está tu mapa.

Cada cosa que se detiene es una decisión o un proceso que vive en tu cabeza y no en la empresa.

Escribe en comentarios qué se detiene primero en la tuya. Sin juzgar: es el mejor punto de partida.

{HASH_LI}''',
    [], utm(ART, 'linkedin', 'social', 'senales-nov26', 'post-03'), 'primer comentario',
    'Comentario: «Si quieres ver las 7 señales completas: {enlace}».')

add('2026-11-12', '08:30', LI, 'Texto', 'Invitación al Radar',
    f'''Mide cuánto depende tu empresa de ti. 21 preguntas, 5 minutos, gratis.

El Radar SYNKA te da un perfil de las seis áreas de tu empresa (estructura, comercial, procesos, operación, personas y control) y te dice en cuál se concentra el riesgo.

No es un dictamen: es una señal para saber dónde mirar primero.

Si el resultado te sorprende, platicamos. Si no, ya sabes qué atender.

{HASH_LI}''',
    [], utm(RADAR, 'linkedin', 'social', 'radar-nov26', 'post-12'), 'primer comentario',
    'Comentario: «Aquí está el Radar: {enlace}».')

add('2026-11-12', '19:00', IGU, 'Reel (guion R1)', 'La prueba de las dos semanas',
    f'''Si te ausentas dos semanas, ¿qué se detiene en tu empresa?

Esa lista es tu mapa de riesgo. Escríbela y empieza por lo primero que se detiene.

Si quieres medir en qué parte se concentra tu dependencia, el Radar SYNKA son 5 minutos y es gratis. Enlace en mi bio.

{HASH_IG}''',
    ['marketing/guiones-reels.md (R1)'], utm(RADAR, 'instagram-uriel', 'bio', 'radar-nov26', 'reel-r1'), 'biografía',
    'Al programar en Meta Business Suite: invitar a @synkamx como colaborador (publicación en colaboración) para que salga en las dos cuentas.')

add('2026-11-13', '10:00', GBP, 'Publicación', 'Artículo: 7 señales',
    'Nuevo artículo: 7 señales de que tu empresa depende de ti, y el primer paso para cada una. Léelo en el sitio.',
    [V + 'senales/01.png'], utm(ART, 'google', 'organic', 'gbp', 'articulo-7-senales'), 'botón «Más información»',
    'Requiere el Perfil de Empresa verificado.')

# ============================ SEMANA 2 · las frases ============================
add('2026-11-16', '19:00', IGU, 'Reel (guion R2)', '«Sin mí esto no funciona»',
    f'''Si has dicho «sin mí esto no funciona», no es orgullo: es una alerta.

Una empresa que solo funciona contigo es un empleo que tú mismo te diste. Se arregla con estructura: quién decide qué, cómo se hace cada cosa y cómo sabes que va bien.

Mide dónde se concentra tu dependencia con el Radar SYNKA. Enlace en mi bio.

{HASH_IG}''',
    ['marketing/guiones-reels.md (R2)'], utm(RADAR, 'instagram-uriel', 'bio', 'radar-nov26', 'reel-r2'), 'biografía', 'Colaboración con @synkamx.')

add('2026-11-17', '08:30', LI, 'Carrusel (PDF o imágenes)', 'Las 7 frases',
    f'''Si en tu empresa se escucha alguna de estas 7 frases, tu empresa depende de ti.

Estas frases no son ejemplos: se oyen todos los días en empresas que ya venden y ya tienen equipo.

No es falta de esfuerzo. Es que el dueño se convirtió en el sistema operativo de su empresa.

¿Cuántas escuchas tú esta semana?

{HASH_LI}''',
    lam('frases', 9), utm(RADAR, 'linkedin', 'social', 'radar-nov26', 'post-01-frases'), 'primer comentario',
    'Comentario: «Para saber en qué área se concentra, el Radar son 5 minutos y es gratis: {enlace}».')

add('2026-11-17', '12:00', IGS, 'Carrusel', 'Las 7 frases',
    f'''7 frases que escuchas cuando tu empresa depende de ti.

No son ejemplos: se oyen todos los días en empresas que ya venden y ya tienen equipo.

¿Cuántas te suenan? Escríbelo en comentarios y mide dónde se concentra con el Radar SYNKA (gratis, 5 minutos). Enlace en la bio.

{HASH_IG}''',
    lam('frases', 9), utm(RADAR, 'instagram-synka', 'bio', 'radar-nov26', 'carrusel-frases'), 'biografía',
    'Cambiar el enlace principal de la biografía al Radar.')

add('2026-11-18', '08:30', LI, 'Texto', '«Eso siempre lo ha hecho Juan»',
    f'''«Eso siempre lo ha hecho Juan.»

Cuando una frase así existe en tu empresa, tienes un riesgo con nombre y apellido.

Si Juan se enferma, renuncia o se lo lleva la competencia, esa función no se retrasa: desaparece.

La solución no es desconfiar de Juan. Es sacar lo que Juan sabe de su cabeza y ponerlo en un procedimiento que cualquiera pueda ejecutar igual.

¿Cuántos «Juan» hay en tu empresa?

{HASH_LI}''',
    [], utm(ART, 'linkedin', 'social', 'senales-nov26', 'post-06'), 'primer comentario',
    'Comentario: «Más señales como esta, con el primer paso para cada una: {enlace}».')

add('2026-11-19', '08:30', LI, 'Texto', 'El problema no es el equipo',
    f'''El problema no es que tu equipo no se esfuerce.

Cuando todo se decide en una sola cabeza, el equipo aprende a esperar. Y espera bien: te pregunta, te confirma, te avisa.

Desde fuera parece falta de iniciativa. Desde dentro es lo más racional que puede hacer: nadie le dijo dónde termina su decisión y dónde empieza la tuya.

Eso no se arregla con una charla de motivación. Se arregla con una estructura que diga quién decide qué.

¿Tu equipo sabe hoy qué puede decidir sin preguntarte?

{HASH_LI}''',
    [], utm(RADAR, 'linkedin', 'social', 'radar-nov26', 'post-02'), 'primer comentario',
    'Comentario: «Para ver en qué área se concentra la espera, el Radar SYNKA: {enlace}».')

add('2026-11-19', '19:00', IGU, 'Reel (guion R3)', 'Tu equipo no es flojo, está esperando',
    f'''Tu equipo no es flojo. Está esperando.

Cuando todas las decisiones pasan por ti, esperar es lo más racional que puede hacer. La salida no es motivación: es una estructura que diga quién decide qué.

Mide dónde se concentra con el Radar SYNKA. Enlace en mi bio.

{HASH_IG}''',
    ['marketing/guiones-reels.md (R3)'], utm(RADAR, 'instagram-uriel', 'bio', 'radar-nov26', 'reel-r3'), 'biografía', 'Colaboración con @synkamx.')

add('2026-11-20', '10:00', GBP, 'Publicación', 'Radar SYNKA',
    'Radar SYNKA: 21 preguntas, 5 minutos, gratis. Mide en cuál de las seis áreas de tu empresa se concentra la dependencia del dueño.',
    [V + 'frases/01.png'], utm(RADAR, 'google', 'organic', 'gbp', 'radar'), 'botón «Más información»')

# ============================ SEMANA 3 · ventas + arranque de anuncios ============================
add('2026-11-23', '09:00', WEB, 'Tarea', 'Artículo 2 (Estructura): pendiente de redactar',
    nota='Según el calendario editorial toca «El organigrama real». Aún no está escrito: pedirlo antes del viernes 20.')

add('2026-11-23', '19:00', IGU, 'Reel (guion R4)', '«Eso siempre lo ha hecho Juan»',
    f'''«Eso siempre lo ha hecho Juan.»

Esa frase es un riesgo con nombre y apellido. Si Juan se va, la función no se retrasa: desaparece.

No se arregla desconfiando de Juan, sino sacando lo que sabe de su cabeza y poniéndolo en un procedimiento que cualquiera pueda ejecutar. Enlace en mi bio para medir dónde tienes más «Juanes».

{HASH_IG}''',
    ['marketing/guiones-reels.md (R4)'], utm(RADAR, 'instagram-uriel', 'bio', 'radar-nov26', 'reel-r4'), 'biografía', 'Colaboración con @synkamx.')

add('2026-11-24', '08:30', LI, 'Carrusel (PDF o imágenes)', '¿Tus ventas dependen de ti?',
    f'''Si todas las ventas pasan por ti, tu empresa vende lo que tú alcances a cerrar.

5 señales de que tus ventas dependen de ti:
→ Todas las cotizaciones pasan por ti.
→ Tus mejores clientes solo hablan contigo.
→ No conoces tu conversión por etapa.
→ Si tú no estás, nadie cierra.
→ No puedes predecir los ingresos del mes.

Si te suenan, el Diagnóstico Comercial SYNKA son 10 preguntas y 3 minutos.

{HASH_LI}''',
    lam('ventas', 7), utm(COMERCIAL, 'linkedin', 'social', 'comercial-nov26', 'post-07-ventas'), 'primer comentario',
    'Comentario: «Diagnóstico Comercial (gratis, 3 minutos): {enlace}».')

add('2026-11-24', '12:00', IGS, 'Carrusel', '¿Tus ventas dependen de ti?',
    f'''¿Tus ventas dependen de ti?

5 señales para saberlo. Si reconoces varias, mide tu sistema comercial con el Diagnóstico Comercial SYNKA: 10 preguntas, 3 minutos, gratis.

Enlace en la bio.

{HASH_IG}''',
    lam('ventas', 7), utm(COMERCIAL, 'instagram-synka', 'bio', 'comercial-nov26', 'carrusel-ventas'), 'biografía',
    'Cambiar el enlace principal de la biografía al Diagnóstico Comercial durante esta semana.')

add('2026-11-25', '08:30', LI, 'Texto', 'Delegar no es soltar',
    f'''Delegar no es soltar. Es decidir qué se suelta primero.

Un dueño que delega todo de golpe termina recogiendo todo de golpe. Un orden que funciona:

1. Lo repetitivo y documentable (procesos).
2. Lo que tiene criterio claro (reglas de decisión por monto, por cliente, por tipo).
3. Lo que requiere juicio (se queda contigo hasta que formes a alguien).

Antes de delegar una tarea, pregúntate: ¿puedo explicar cómo se hace bien en 10 líneas? Si no, no es delegación: es abandono con buena intención.

{HASH_LI}''',
    [], utm(SITIO + '/blog/como-delegar-en-mi-empresa', 'linkedin', 'social', 'senales-nov26', 'post-05'), 'primer comentario',
    'Comentario: «Seis pasos para empezar a delegar sin que todo se caiga: {enlace}».')

add('2026-11-26', '08:30', LI, 'Texto', 'El organigrama real',
    f'''El organigrama de la pared y el organigrama real casi nunca coinciden.

El de la pared dice quién reporta a quién. El real dice a quién le preguntan de verdad.

Si el real tiene tu nombre en el centro de todo, hay un cuello de botella con forma de persona.

Diseñar estructura no es dibujar cajas: es definir quién decide qué y qué ya no regresa a ti.

{HASH_LI}''',
    [], utm(RADAR, 'linkedin', 'social', 'radar-nov26', 'post-09'), 'primer comentario',
    'Comentario: «Para ver si tu estructura es el punto débil, el Radar SYNKA: {enlace}». Enlazar el artículo 2 cuando exista.')

add('2026-11-26', '19:00', IGU, 'Reel (guion R5)', '¿Tus ventas dependen de ti?',
    f'''Si te vas, ¿quién cierra?

Tres preguntas: ¿quién cotiza?, ¿conoces tu conversión por etapa?, ¿puedes predecir los ingresos del mes? Si no sabes responderlas, tus ventas dependen de ti.

El Diagnóstico Comercial SYNKA son 10 preguntas y 3 minutos. Enlace en mi bio.

{HASH_IG}''',
    ['marketing/guiones-reels.md (R5)'], utm(COMERCIAL, 'instagram-uriel', 'bio', 'comercial-nov26', 'reel-r5'), 'biografía',
    'Es el tema que mejor respondió en tu cuenta personal. Colaboración con @synkamx.')

add('2026-11-27', '10:00', GBP, 'Publicación', 'Diagnóstico Comercial',
    'Diagnóstico Comercial SYNKA: 10 preguntas y 3 minutos para medir qué tanto dependen tus ventas de ti, con semáforo por área.',
    [V + 'ventas/01.png'], utm(COMERCIAL, 'google', 'organic', 'gbp', 'diagnostico-comercial'), 'botón «Más información»')

# ============================ SEMANA 4 · consolidar y medir ============================
add('2026-11-30', '19:00', IGU, 'Reel (guion R6)', 'Delegar no es soltar',
    f'''Delegar no es soltar: es decidir qué se suelta primero.

Primero lo repetitivo, después lo que tiene criterio claro, al final lo que requiere juicio. Si no puedes explicar cómo se hace bien en 10 líneas, no es delegación: es abandono con buena intención.

Mide dónde tienes más dependencia con el Radar SYNKA. Enlace en mi bio.

{HASH_IG}''',
    ['marketing/guiones-reels.md (R6)'], utm(RADAR, 'instagram-uriel', 'bio', 'radar-nov26', 'reel-r6'), 'biografía', 'Colaboración con @synkamx.')

add('2026-12-01', '08:30', LI, 'Texto', 'Documentar sin burocracia',
    f'''Documentar procesos no tiene por qué volver burocrática tu empresa.

La burocracia aparece cuando se documenta todo. El sistema aparece cuando se documenta lo que se repite, lo que se equivoca y lo que depende de una sola persona.

Empieza por tres:
1. El proceso que más errores genera.
2. El que solo una persona sabe hacer.
3. El que te interrumpe más veces al día.

Una página por proceso: pasos, responsable y cómo se sabe que salió bien.

{HASH_LI}''',
    [], utm(SITIO + '/blog/documentar-procesos-sin-burocracia', 'linkedin', 'social', 'senales-nov26', 'post-08'), 'primer comentario',
    'Comentario: «Guía completa para hacerlo sin burocracia: {enlace}».')

add('2026-12-02', '08:30', LI, 'Texto', 'Lo que hacemos distinto',
    f'''No decimos cómo administrar tu empresa.

SYNKA no llega a opinar sobre tu negocio. Llega a construir el sistema que hace que funcione mejor sin ti en el centro.

Tres cosas que hacemos distinto:
→ Instalamos, no entregamos documentos. El entregable es una operación que se ejecuta distinto el lunes siguiente.
→ Trabajamos la empresa completa, no un área aislada. Arreglar una sola mueve el cuello de botella de lugar.
→ El sistema queda con la empresa. El objetivo no es que nos necesites.

{HASH_LI}''',
    [], utm(RADAR, 'linkedin', 'social', 'radar-nov26', 'post-11'), 'primer comentario',
    'Comentario: «El primer paso es medir dónde está tu dependencia: {enlace}».')

add('2026-12-03', '08:30', LI, 'Texto', 'Dependencia contra sistema',
    f'''Dos empresas que venden lo mismo pueden funcionar de forma muy distinta.

Empresa que depende del dueño: caos, improvisación, procesos informales, falta de control.
Empresa que funciona como sistema: estructura, procesos, responsabilidades, indicadores, control y autonomía.

La diferencia no es el tamaño ni el esfuerzo. Es que lo que hoy vive en tu cabeza esté escrito, asignado y medido.

¿De qué lado está la tuya?

{HASH_LI}''',
    [], utm(ART, 'linkedin', 'social', 'senales-nov26', 'post-04'), 'primer comentario',
    'Comentario: «Siete señales para saber de qué lado estás: {enlace}».')

add('2026-12-03', '19:00', IGU, 'Reel (guion R7)', '3 números que un dueño debería ver sin preguntar',
    f'''3 números que todo dueño debería ver sin tener que preguntar: lo que vendió el equipo, lo que está por cobrar y cuántas entregas salieron a tiempo.

Si para saberlo tienes que pedirlo, esperar y dudar del número, tu empresa depende de ti.

Mide tu nivel de control con el Radar SYNKA. Enlace en mi bio.

{HASH_IG}''',
    ['marketing/guiones-reels.md (R7)'], utm(RADAR, 'instagram-uriel', 'bio', 'radar-nov26', 'reel-r7'), 'biografía', 'Colaboración con @synkamx.')

add('2026-12-04', '10:00', GBP, 'Publicación', 'Método SYNKA',
    'El Método SYNKA: tres fases (diagnóstico, diseño e implementación) y seis movimientos para que tu empresa opere sin ti en el centro.',
    [V + 'senales/01.png'], utm(SITIO + '/#metodo', 'google', 'organic', 'gbp', 'metodo'), 'botón «Más información»')

add('2026-12-04', '16:00', WEB, 'Tarea', 'Revisión de las 4 semanas',
    nota='Abrir la hoja de leads, GA4 (embudo artículo → Radar → generate_lead) y Search Console. Decidir: qué carrusel y qué reel '
         'funcionaron mejor, qué canal trajo leads calificados, y qué se repite el mes siguiente.')

# ---------------------------------------------------------------------------
DIAS = ['lun', 'mar', 'mié', 'jue', 'vie', 'sáb', 'dom']
MESES = ['', 'ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']

def etiqueta(f):
    d = dt.date.fromisoformat(f)
    return f'{DIAS[d.weekday()]} {d.day} {MESES[d.month]}'

def semana(f):
    base = dt.date(2026, 11, 9)
    return (dt.date.fromisoformat(f) - base).days // 7 + 1

def main():
    os.makedirs(SALIDA, exist_ok=True)
    P.sort(key=lambda p: (p['fecha'], p['hora']))

    with open(os.path.join(SALIDA, 'calendario-publicaciones.csv'), 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.writer(fh)
        w.writerow(['semana', 'fecha', 'hora_cdmx', 'cuenta', 'formato', 'titulo', 'texto', 'archivos',
                    'enlace_con_utm', 'donde_va_el_enlace', 'nota', 'estado'])
        for p in P:
            w.writerow([semana(p['fecha']), p['fecha'], p['hora'], p['cuenta'], p['formato'], p['titulo'], p['texto'],
                        ' | '.join(p['archivos']), p['enlace'], p['donde'], p['nota'], 'pendiente'])

    for n in range(1, 5):
        filas = [p for p in P if semana(p['fecha']) == n]
        ini, fin = filas[0]['fecha'], filas[-1]['fecha']
        t = [f'# Semana {n} · {etiqueta(ini)} a {etiqueta(fin)}\n',
             'Todo lo de esta página está listo para copiar y pegar. Las imágenes están en `marketing/visuales/`.\n',
             'Resumen de la semana:\n']
        for p in filas:
            t.append(f'- {etiqueta(p["fecha"])} {p["hora"]} · {p["cuenta"]} · {p["formato"]} · {p["titulo"]}')
        t.append('')
        for p in filas:
            t.append(f'## {etiqueta(p["fecha"])} · {p["hora"]} · {p["cuenta"]} · {p["formato"]}\n')
            t.append(f'**{p["titulo"]}**\n')
            if p['archivos']:
                t.append('**Archivos:** ' + ', '.join(f'`{a}`' for a in p['archivos'][:1]) +
                         (f' … `{p["archivos"][-1]}` ({len(p["archivos"])} imágenes, en orden)' if len(p['archivos']) > 1 else '') + '\n')
            if p['texto']:
                t.append('**Texto:**\n\n```\n' + p['texto'] + '\n```\n')
            if p['enlace']:
                t.append(f'**Enlace** ({p["donde"]}):\n\n```\n{p["enlace"]}\n```\n')
            if p['nota']:
                t.append(f'**Nota:** {p["nota"].replace("{enlace}", p["enlace"])}\n')
        open(os.path.join(SALIDA, f'semana-{n}.md'), 'w', encoding='utf-8').write('\n'.join(t))
    print(len(P), 'publicaciones y tareas ·', len({p["fecha"] for p in P}), 'días')

if __name__ == '__main__':
    main()
