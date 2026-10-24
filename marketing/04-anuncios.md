# 04 · Anuncios (Meta y Google)

**Destino único:** `https://synka.mx/diagnostico/radar` con UTM. El objetivo del anuncio es que **hagan el Radar**, no que llenen el formulario largo.
El lead se captura en la pantalla de resultado.

> No lanzar hasta tener: GA4 activo, `generate_lead` como evento clave, aviso de privacidad publicado y el flujo probado en móvil (ver `01`).
> El 80–90 % del tráfico pago será móvil: probar el Radar completo en un teléfono antes de gastar.

## Presupuesto de prueba (semanas 3–6)

| Plataforma | Mensual | Diario |
|---|---|---|
| Meta Ads | 9,000 MXN | ≈ 300 |
| Google Ads | 6,000 MXN | ≈ 200 |

Primeras 2 semanas: **gastar 50 %** de lo anterior para validar creativos y seguimiento; subir solo si el costo por Radar completado se acerca a la meta.

---

## Meta Ads (Instagram + Facebook)

**Campaña:** Conversiones o Clientes potenciales → optimizar a evento `generate_lead` (cuando haya ≥ 10 eventos; antes, optimizar a `diagnostico_terminado`).
**Ubicaciones:** automáticas al inicio; revisar y quitar las que den tráfico sin Radar completado.

### Públicos

| Conjunto | Definición |
|---|---|
| A · Dueños | México, 30–60 años, intereses: "Propietario de pequeña empresa", "Emprendimiento", "Administración de empresas"; comportamiento: administradores de páginas de negocio |
| B · Cargos | Cargo: Director General, Propietario, Fundador, CEO; empresas de 11–200 empleados |
| C · Retargeting | Visitantes de synka.mx (30 días) y quienes iniciaron el Radar sin terminarlo |

Presupuesto: 40 % A · 40 % B · 20 % C (cuando C tenga volumen).
Excluir a quienes ya enviaron el formulario (audiencia de `generate_lead`).

### Creativos

Estilo visual: navy `#002B49`, teal `#00C9B7` solo sobre navy, tipografía Archivo, sin fotos de stock, sin sombras, mucho aire. Isotipo oficial sin modificar.

**Anuncio 1 · "Dolor"** (imagen estática 1080×1350)
- Texto en imagen: *Si te ausentas dos semanas, ¿qué se detiene?*
- Texto principal: *Cuando todo pasa por ti, tu empresa crece hasta donde tú alcanzas. El Radar SYNKA mide en 5 minutos en qué parte de tu empresa se concentra esa dependencia. Gratis.*
- Título: *Mide cuánto depende de ti tu empresa*
- Descripción: *21 preguntas · 5 minutos · gratis*
- CTA: Más información
- UTM: `utm_source=meta&utm_medium=paid&utm_campaign=radar-nov26&utm_content=anuncio-dolor`

**Anuncio 2 · "Las frases"** (carrusel 5 láminas)
- Láminas: "Pregúntale al dueño." · "Eso siempre lo ha hecho Juan." · "Sin mí esto no funciona." · "No tenemos un proceso." · *¿Te suena? Haz el Radar.*
- Texto principal: *Estas frases no son ejemplos: se escuchan todos los días en empresas que ya venden y ya tienen equipo. Descubre qué parte de la tuya depende de ti.*
- Título: *El Radar SYNKA te lo muestra*
- UTM: `utm_content=anuncio-frases`

**Anuncio 3 · "Resultado"** (video 15–20 s, vertical 9:16)
- Guion: grabación de pantalla del Radar (pregunta → hexágono con las seis divisiones → "dónde se concentra la dependencia"). Voz de Uriel: *"Casi todas las PyMEs que crecieron dependen de su dueño. El Radar te dice en cuál de seis áreas. Cinco minutos, gratis."*
- Texto principal: *Un mapa de las seis áreas de tu empresa y cuál sostiene el mayor riesgo.*
- UTM: `utm_content=anuncio-resultado`

**Anuncio 4 · Retargeting** (a quienes iniciaron y no terminaron)
- Texto: *Te quedaste a mitad del Radar. Te faltan unas preguntas para ver el mapa completo de tu empresa.*
- Título: *Termina tu Radar*
- UTM: `utm_content=retarget-radar`

**Políticas:** ninguna promesa de resultados ("duplica tus ventas", "gana más"). Hablar del diagnóstico, no de garantías.

---

## Google Ads (Búsqueda)

**Campaña:** Búsqueda, solo red de búsqueda (sin Display), México, español. Puja: maximizar clics con tope en las primeras 2 semanas → pasar a maximizar conversiones cuando haya ≥ 15 conversiones.
**Conversión:** `generate_lead` (principal) y `diagnostico_terminado` (secundaria, sin valor).

### Grupos y palabras clave (concordancia de frase y exacta)

| Grupo | Palabras clave de ejemplo |
|---|---|
| Dependencia del dueño | "mi empresa depende de mí", "empresa depende del dueño", "dependencia del dueño empresa", "como dejar de depender de mi empresa" |
| Delegar | "como delegar en mi empresa", "como delegar en una pyme", "delegar responsabilidades empresa" |
| Procesos | "estandarizar procesos pyme", "documentar procesos empresa", "consultoría de procesos para pymes", "consultor de procesos empresariales" |
| Diagnóstico | "diagnóstico empresarial pyme", "diagnóstico de empresa gratis", "evaluación de madurez empresa", "test empresa depende de mi" |
| Estructura | "organigrama pyme", "estructura organizacional pyme", "profesionalizar empresa familiar" |

**Negativas iniciales:** gratis curso, curso, pdf, plantilla, trabajo, empleo, vacante, universidad, tesis, ejemplo, software, app, excel, word, sap, erp, crm. *(Quitar "gratis" solo si la oferta gratuita es lo que se quiere anunciar; aquí el Radar es gratis, así que revisar términos tras 2 semanas y no bloquear "diagnóstico gratis".)*

### Anuncios responsivos de búsqueda

**Títulos (≤ 30 caracteres):**
1. Tu empresa depende de ti
2. Radar SYNKA · 5 minutos
3. Mide la dependencia del dueño
4. Diagnóstico gratis para PyMEs
5. Empresa que funciona sin ti
6. Estructura, procesos y control
7. Consultoría para PyMEs en MX
8. Haz el Radar SYNKA
9. 21 preguntas, 6 áreas
10. Sistemas que hacen funcionar

**Descripciones (≤ 90 caracteres):**
1. Descubre en qué parte de tu empresa se concentra la dependencia. Gratis y en 5 minutos.
2. Recibe un mapa de las seis áreas de tu PyME y cuál sostiene el mayor riesgo.
3. Instalamos estructura, procesos y control para que tu operación no dependa del dueño.
4. Empieza por el Radar SYNKA: sin costo y sin compromiso.

**URL final:** `https://synka.mx/diagnostico/radar?utm_source=google&utm_medium=cpc&utm_campaign=radar-nov26&utm_content={adgroupid}`
**Ruta visible:** `synka.mx/radar-empresarial` (no existe: es solo visual; puede ser cualquier texto).

### Extensiones

- Sitelinks: Radar SYNKA · Diagnóstico Comercial · Método SYNKA · Blog.
- Fragmentos: Servicios → Estructura, Comercial, Procesos, Operación, Personas, Control.
- Llamada y ubicación: agregar solo cuando exista el Perfil de Empresa verificado.

---

## Reglas de operación (para decidir sin discutir)

| Situación | Acción |
|---|---|
| Anuncio con ≥ 2,000 impresiones y CTR < 0.6 % (Meta) | Apagar y reemplazar el gancho |
| Anuncio con ≥ 40 clics y 0 Radares iniciados | Revisar landing y seguimiento, no el anuncio |
| Costo por Radar completado > 2× la meta tras 2 semanas | Pausar el conjunto/grupo |
| Inicio → fin del Radar < 40 % | El problema es el Radar, no el tráfico: parar gasto y revisar |
| Lead calificado (según hoja) | Duplicar presupuesto del conjunto que lo trajo, de 20 % en 20 % cada 3 días |
| Fatiga (frecuencia > 3 en Meta) | Rotar creativo |

Revisión: lunes (resultado semanal) y jueves (ajustes). **Documentar cada cambio en la hoja** para saber qué lo causó.

## Pruebas A/B sugeridas (una variable a la vez)

1. Gancho "Dolor" vs. "Las frases".
2. Título "Mide cuánto depende de ti tu empresa" vs. "Haz el Radar SYNKA".
3. Imagen navy tipográfica vs. foto del retrato de dirección (tratamiento de marca).
