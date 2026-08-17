#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera los bancos de preguntas de los dos diagnósticos.

    python3 tools/gen-datos-diagnostico.py

Las preguntas, ayudas, opciones y puntajes se conservan **literales** de las
herramientas originales (Radar Empresarial y Diagnóstico Comercial™). Lo único
que cambia es la etiqueta de salida: donde antes había 5 dimensiones genéricas,
ahora cada pregunta apunta a una de las seis divisiones SYNKA, para que el
resultado hable el idioma de lo que se vende.

Origen de los datos:
  radar     → diagnostico.html                    (21 preguntas, Likert 0-4)
  comercial → diagnostico-comercial-vestra.html   (10 preguntas, puntos 0-5)

Ningún dato de autoridad (número de empresas, años, porcentajes de mercado)
se traslada: quedó pendiente de verificación.
"""

import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUENTE = os.path.join(RAIZ, "_source", "preguntas")

# ── Re-corte del Radar: de 5 dimensiones genéricas a las 6 divisiones ────────
#
#  Dimensión original      Preguntas   Se reparte en
#  ──────────────────────────────────────────────────────────────────────
#  Finanzas                1-4         CONTROL
#  Estrategia              5-8         ESTRUCTURA (5,6) + CONTROL (7,8)
#  Ventas                  9-13        COMERCIAL
#  Talento                 14-17       ESTRUCTURA (14) + OPERACIÓN (15) + PERSONAS (16,17)
#  Operaciones             18-21       PROCESOS (18,20) + OPERACIÓN (19,21)
#
# "Finanzas" no tiene división propia en SYNKA: se pliega dentro de CONTROL.
# Es una decisión consciente, no un descuido.

MAPA_RADAR = [
    "control", "control", "control", "control",          # 1-4   Finanzas
    "estructura", "estructura", "control", "control",     # 5-8   Estrategia
    "comercial", "comercial", "comercial",                # 9-11  Ventas
    "comercial", "comercial",                             # 12-13 Ventas
    "estructura", "operacion", "personas", "personas",    # 14-17 Talento
    "procesos", "operacion", "procesos", "operacion",     # 18-21 Operaciones
]

DIVISIONES = {
    "estructura": "ESTRUCTURA",
    "comercial": "COMERCIAL",
    "procesos": "PROCESOS",
    "operacion": "OPERACIÓN",
    "personas": "PERSONAS",
    "control": "CONTROL",
}


def cabecera(nombre):
    return (
        "/* ============================================================================\n"
        "   SYNKA — Banco de preguntas: {}\n"
        "   Generado por tools/gen-datos-diagnostico.py. No editar a mano:\n"
        "   editar el script y volver a ejecutarlo.\n"
        "   ========================================================================== */\n\n"
    ).format(nombre)


def emitir_radar():
    with open(os.path.join(FUENTE, "radar.json"), encoding="utf-8") as f:
        crudo = json.load(f)

    if len(crudo) != len(MAPA_RADAR):
        raise SystemExit(
            "El banco trae {} preguntas y el mapa cubre {}. "
            "Revisa MAPA_RADAR antes de continuar.".format(len(crudo), len(MAPA_RADAR))
        )

    preguntas = []
    for q, division in zip(crudo, MAPA_RADAR):
        preguntas.append({
            "division": division,
            "texto": q["text"],
            "ayuda": q["help"],
            # Escala Likert de 5 posiciones: 0 a 4 puntos por orden de aparición.
            "opciones": [{"t": o, "p": i} for i, o in enumerate(q["options"])],
        })

    reparto = {}
    for p in preguntas:
        reparto[p["division"]] = reparto.get(p["division"], 0) + 1

    datos = {
        "id": "radar",
        "nombre": "RADAR SYNKA",
        "escala": "porcentaje",
        "preguntas": preguntas,
        "reparto": reparto,
    }
    ruta = os.path.join(RAIZ, "js", "datos-radar.js")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(cabecera("RADAR SYNKA"))
        f.write("window.SYNKA_RADAR = ")
        f.write(json.dumps(datos, ensure_ascii=False, indent=2))
        f.write(";\n")
    print("escrito  js/datos-radar.js  ({} preguntas)".format(len(preguntas)))
    for k in DIVISIONES:
        print("           {:11} {} preguntas".format(DIVISIONES[k], reparto.get(k, 0)))


def emitir_comercial():
    with open(os.path.join(FUENTE, "comercial.json"), encoding="utf-8") as f:
        crudo = json.load(f)

    preguntas = [{
        "area": q["area"],
        "texto": q["text"],
        "ayuda": q["hint"],
        "opciones": [{"t": o["t"], "p": o["p"]} for o in q["opts"]],
    } for q in crudo]

    # El máximo se calcula, no se declara: la pregunta 6 tope en 4 y no en 5,
    # así que el máximo real es 49 aunque la herramienta original dijera 50.
    maximo = sum(max(o["p"] for o in q["opciones"]) for q in preguntas)

    datos = {
        "id": "comercial",
        "nombre": "Diagnóstico Comercial",
        "division": "comercial",
        "escala": "puntos",
        "maximo": maximo,
        "areas": ["Prospección", "Independencia", "Métricas",
                  "Predictibilidad", "Seguimiento", "Cierre"],
        "preguntas": preguntas,
    }
    ruta = os.path.join(RAIZ, "js", "datos-comercial.js")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(cabecera("Diagnóstico Comercial · SYNKA COMERCIAL"))
        f.write("window.SYNKA_COMERCIAL = ")
        f.write(json.dumps(datos, ensure_ascii=False, indent=2))
        f.write(";\n")
    print("escrito  js/datos-comercial.js  ({} preguntas, máximo real {})"
          .format(len(preguntas), maximo))


if __name__ == "__main__":
    emitir_radar()
    emitir_comercial()
