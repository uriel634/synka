#!/usr/bin/env python3
"""Une el calendario del mes de lanzamiento con las semanas nuevas en un solo CSV.

Uso:  python3 tools/gen-calendario-completo.py
Lee:
  marketing/calendario/calendario-publicaciones.csv         (semanas 1 a 4, generado por gen-calendario.py)
  marketing/calendario/precalentamiento-dos-voces.md        (26 oct a 6 nov)
  marketing/banco-de-publicaciones.md                       (semanas 5 a 12)
Escribe:
  marketing/calendario/calendario-completo.csv              (para importar en Metricool, Buffer, etc.)

Los textos se toman de los .md, que son la fuente de verdad: se edita ahí y se vuelve a correr.
Mismas columnas que calendario-publicaciones.csv.
"""
import csv, datetime as dt, os, re, unicodedata
from urllib.parse import urlencode

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAL = os.path.join(RAIZ, 'marketing', 'calendario')
BANCO = os.path.join(RAIZ, 'marketing', 'banco-de-publicaciones.md')
PRECAL = os.path.join(CAL, 'precalentamiento-dos-voces.md')
EXISTENTE = os.path.join(CAL, 'calendario-publicaciones.csv')
SALIDA = os.path.join(CAL, 'calendario-completo.csv')
VISUALES = os.path.join(RAIZ, 'marketing', 'visuales')

SITIO = 'https://synka.mx'
LI, IGS, IGU, GBP = 'LinkedIn (Uriel)', 'Instagram SYNKA', 'Instagram Uriel', 'Perfil de Empresa en Google'
MESES = {'ene': (2027, 1), 'oct': (2026, 10), 'nov': (2026, 11), 'dic': (2026, 12)}
HASH_IG = '#PyMEsMéxico #DueñosDeNegocio #Empresarios #ProcesosEmpresariales #LiderazgoEmpresarial'

# Carrusel de SYNKA → carpeta de imágenes
CARPETA = {'S-01': 'tablero', 'S-02': 'puesto', 'S-03': 'cierre-anio', 'S-04': 'area-debil', 'S-05': 'evaluar',
           'S-06': 'informe-vs-instalacion', 'S-07': 'estandar'}

# Artículos del blog a los que apuntan algunas piezas (slug previsto)
ARTICULO = {'U-01': 'numeros-que-un-dueno-debe-ver-sin-preguntar',
            'U-05': 'como-delegar-en-mi-empresa',
            'U-13': 'perfil-de-puesto-y-evaluacion-en-una-pyme',   # por escribir (11 ene)
            'U-19': 'estandares-de-servicio-sin-supervision'}      # por escribir (25 ene)
PENDIENTE_ARTICULO = {'U-13', 'U-19'}
CONDICIONAL = {'U-16': 'Solo si hay ≥ 30 Radar completados y el aviso de privacidad cubre el uso. Si no, publicar U-17.',
               'U-20': 'Elegir versión A (caso autorizado) o B (sin caso todavía).'}
CAMPANA_FIJA = {'U-13': 'metodo-ene27', 'U-19': 'metodo-ene27', 'R15': 'oferta-ene27', 'S-07': 'oferta-ene27',
                'U-20': 'oferta-ene27', 'U-21': 'oferta-ene27'}


def campana(f):
    for ini, fin, c in (('2026-10-26', '2026-11-08', 'precalentamiento-oct26'), ('2026-12-07', '2026-12-20', 'metodo-dic26'),
                        ('2026-12-21', '2027-01-03', 'cierre-dic26'), ('2027-01-04', '2027-01-10', 'arranque-ene27'),
                        ('2027-01-11', '2027-01-17', 'metodo-ene27'), ('2027-01-18', '2027-01-31', 'oferta-ene27')):
        if ini <= f <= fin:
            return c
    return 'arranque-ene27'


def utm(base, fuente, medio, camp, contenido):
    return base + '?' + urlencode({'utm_source': fuente, 'utm_medium': medio, 'utm_campaign': camp, 'utm_content': contenido})


def semana(f):
    d = dt.date.fromisoformat(f)
    lunes = d - dt.timedelta(days=d.weekday())
    etiqueta = {'2026-10-26': 'A', '2026-11-02': 'B'}.get(lunes.isoformat())
    if etiqueta:
        return etiqueta
    return (lunes - dt.date(2026, 11, 9)).days // 7 + 1


def fecha(dia, mes):
    a, m = MESES[mes]
    return dt.date(a, m, int(dia)).isoformat()


def secciones(texto):
    """Divide en secciones '## ...' y devuelve (encabezado, cuerpo)."""
    partes = re.split(r'^## ', texto, flags=re.M)[1:]
    out = []
    for p in partes:
        enc, _, cuerpo = p.partition('\n')
        cuerpo = re.split(r'^(?:---|# )', cuerpo, maxsplit=1, flags=re.M)[0]
        out.append((enc.strip(), cuerpo))
    return out


def bloques(cuerpo):
    return re.findall(r'```\n(.*?)\n```', cuerpo, flags=re.S)


def despues_de(cuerpo, marca):
    """Primer bloque de código que aparece después de `marca`."""
    i = cuerpo.find(marca)
    if i < 0:
        return ''
    b = bloques(cuerpo[i:])
    return b[0].strip() if b else ''


def texto_de(cuerpo):
    m = re.search(r'\*\*Texto:\*\* `(.+?)`', cuerpo)
    if m:
        return m.group(1).strip()
    if '**Texto:**' in cuerpo:
        return despues_de(cuerpo, '**Texto:**')
    b = bloques(cuerpo)
    return b[0].strip() if b else ''


def imagenes(carpeta):
    d = os.path.join(VISUALES, carpeta)
    n = len([x for x in os.listdir(d) if x.endswith('.png')]) if os.path.isdir(d) else 0
    return [f'marketing/visuales/{carpeta}/{i:02d}.png' for i in range(1, n + 1)]


def titulo_de(cuerpo):
    m = re.search(r'^\*\*(.+?)\*\*', cuerpo, flags=re.M)
    return m.group(1).strip() if m else ''


def fila(sem, f, hora, cuenta, formato, titulo, texto, archivos, enlace, donde, nota, estado):
    return dict(semana=sem, fecha=f, hora_cdmx=hora, cuenta=cuenta, formato=formato, titulo=titulo, texto=texto,
                archivos='\n'.join(archivos), enlace_con_utm=enlace, donde_va_el_enlace=donde, nota=nota, estado=estado)


def estado_de(texto):
    return 'completar' if '[' in texto and ']' in texto else 'pendiente'


def desde_precalentamiento():
    filas = []
    for enc, cuerpo in secciones(open(PRECAL, encoding='utf-8').read()):
        m = re.match(r'(\w+) (\d+) (\w+) · (\d\d:\d\d) · (.+?) · (.+)', enc)
        if not m:
            continue
        _, dia, mes, hora, cuenta, formato = m.groups()
        f = fecha(dia, mes)
        texto = texto_de(cuerpo)
        enlace = despues_de(cuerpo, '**Enlace**')
        donde = 'primer comentario' if cuenta.startswith('LinkedIn') else 'biografía'
        archivos = []
        if 'Carrusel nuevo' in formato:
            carpeta = 'seis-areas' if f == '2026-10-28' else 'instalar'
            archivos = imagenes(carpeta)
        if not enlace:
            donde = ''
        if formato.startswith('Reel'):
            formato = 'Reel'
        filas.append(fila(semana(f), f, hora, cuenta, formato, titulo_de(cuerpo), texto, archivos, enlace, donde,
                          'Colaboración con @synkamx.' if formato == 'Reel' else '', estado_de(texto)))
    return filas


def desde_banco():
    filas = []
    texto_banco = open(BANCO, encoding='utf-8').read()
    for enc, cuerpo in secciones(texto_banco):
        m = re.match(r'(U-\d+|R\d+|S-\d+) · (\w+) (\d+) (\w+) · (.+)', enc)
        if m:
            pid, _, dia, mes, resto = m.groups()
            f = fecha(dia, mes)
            camp = CAMPANA_FIJA.get(pid, campana(f))
            texto = texto_de(cuerpo)
            if pid.startswith('U-'):
                cuenta, hora, formato = LI, '08:30', 'Texto'
                enlace, donde = '', ''
                if '**Enlace**' in cuerpo:
                    base = SITIO + ('/blog/' + ARTICULO[pid] if pid in ARTICULO else '/diagnostico/radar')
                    enlace = utm(base, 'linkedin', 'social', camp, pid.lower())
                    donde = 'primer comentario'
                nota = CONDICIONAL.get(pid, '')
                if pid in PENDIENTE_ARTICULO:
                    nota = (nota + ' ' if nota else '') + 'Requiere el artículo publicado el lunes anterior.'
                if pid == 'U-01':
                    nota = 'Requiere el artículo de Control publicado el 7 dic.'
                estado = 'condicional' if pid in CONDICIONAL else estado_de(texto)
                filas.append(fila(semana(f), f, hora, cuenta, formato, titulo_de(cuerpo), texto, [], enlace, donde, nota, estado))
            elif pid.startswith('R'):
                texto = texto if len(texto) > 40 else texto + ' Radar SYNKA, gratis: enlace en mi bio.\n\n' + HASH_IG
                if HASH_IG not in texto:
                    texto += '\n\n' + HASH_IG
                enlace = utm(SITIO + '/diagnostico/radar', 'instagram-uriel', 'bio', camp, 'reel-' + pid.lower())
                filas.append(fila(semana(f), f, '19:00', IGU, 'Reel', titulo_de(cuerpo), texto, [], enlace, 'biografía',
                                  'Colaboración con @synkamx. Guion en el banco (' + pid + ').', 'pendiente'))
            else:
                carpeta = CARPETA[pid]
                enlace = utm(SITIO + '/diagnostico/radar', 'instagram-synka', 'bio', camp, 'carrusel-' + pid.lower().replace('-', ''))
                if HASH_IG not in texto:
                    texto += '\n\n' + HASH_IG
                filas.append(fila(semana(f), f, '12:00', IGS, 'Carrusel', titulo_de(cuerpo), texto, imagenes(carpeta), enlace,
                                  'biografía', '', 'pendiente'))
            continue
    # Publicaciones de Google (tabla de viernes)
    gbp_ini = texto_banco.find('## Perfil de Empresa en Google')
    gbp = texto_banco[gbp_ini:].split('\n\n')[1] if gbp_ini >= 0 else ''
    for linea in gbp.splitlines():
        m = re.match(r'\| (\d+) (\w+) \| (.+?) \|$', linea)
        if m:
            dia, mes, tema = m.groups()
            f = fecha(dia, mes)
            slug = re.sub(r'[^a-z0-9]+', '-', unicodedata.normalize('NFKD', tema.lower().split('(')[0]).encode('ascii', 'ignore').decode()).strip('-')
            filas.append(fila(semana(f), f, '10:00', GBP, 'Publicación', tema.split('(')[0].strip(),
                              f'{tema.split("(")[0].strip()}. Radar SYNKA: 21 preguntas, 5 minutos, gratis.', [],
                              utm(SITIO + '/diagnostico/radar', 'google', 'organic', 'gbp', slug[:40]),
                              'botón «Más información»', 'Requiere el Perfil de Empresa verificado.', 'pendiente'))
    return filas


LI_SYNKA = 'LinkedIn (SYNKA)'


def linkedin_de_synka(filas):
    """Cada carrusel de Instagram de SYNKA se publica también en la página de empresa de LinkedIn (misma hora +
    una hora; el enlace va en el primer comentario, con su propio UTM)."""
    out = []
    for r in filas:
        if r['cuenta'] != IGS or 'Carrusel' not in r['formato']:
            continue
        texto = r['texto'].replace(HASH_IG, '').rstrip()
        texto = re.sub(r'[Ee]nlace en la bio\.?', 'Enlace en el primer comentario.', texto)
        texto += '\n\n#PyMEs #Empresarios #Liderazgo'
        enlace = (r['enlace_con_utm'].replace('utm_source=instagram-synka', 'utm_source=linkedin')
                  .replace('utm_medium=bio', 'utm_medium=social'))
        enlace = re.sub(r'(utm_content=[^&]+)', r'\1-pagina', enlace)
        out.append(dict(r, cuenta=LI_SYNKA, hora_cdmx='10:00', formato='Carrusel (PDF o imágenes)', texto=texto,
                        enlace_con_utm=enlace, donde_va_el_enlace='primer comentario',
                        nota='Publicar desde la página de empresa SYNKA, no desde el perfil personal. Subir las imágenes en orden '
                             '(documento PDF o imágenes múltiples). Mismo carrusel que Instagram de SYNKA de ese día.'))
    return out


def main():
    with open(EXISTENTE, encoding='utf-8-sig', newline='') as fh:
        previas = list(csv.DictReader(fh))
    columnas = list(previas[0].keys())
    nuevas = desde_precalentamiento() + desde_banco()
    nuevas += linkedin_de_synka(previas + nuevas)
    todas = previas + nuevas
    todas.sort(key=lambda r: (r['fecha'], r['hora_cdmx']))
    with open(SALIDA, 'w', encoding='utf-8-sig', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=columnas, extrasaction='ignore')
        w.writeheader()
        w.writerows(todas)
    print(f'{len(previas)} existentes + {len(nuevas)} nuevas = {len(todas)} filas → {os.path.relpath(SALIDA, RAIZ)}')


if __name__ == '__main__':
    main()
