# 05 · Nurture después del Radar

Quien deja sus datos al ver su resultado ya mostró interés. El objetivo de la secuencia es **agendar la sesión de diagnóstico**, no vender.
Mientras no haya automatización, se envía **manual desde el correo y WhatsApp de Uriel**, usando las variables del lead de Formspree (`nombre`, `empresa`, `resultado`, `mas_debil`).

**Regla:** el primer mensaje sale en menos de 1 hora hábil. Si respondió, se detiene la secuencia y se conversa.

## Mensaje 0 · Mismo día (WhatsApp, personal, 3 líneas)

> Hola {nombre}, soy Uriel de SYNKA. Vi que hiciste el Radar: tu resultado fue {nivel} y {mas_debil} es el punto más débil. ¿Te explico qué significa y por dónde se atiende primero? Son 15 minutos, por llamada o por aquí.

## Día 0 · Correo (resultado + siguiente paso)

**Asunto:** Tu resultado del Radar SYNKA, {nombre}
**Cuerpo:**
> Hola {nombre},
>
> Gracias por hacer el Radar. Tu resultado: **{resultado}**. La división donde más se concentra la dependencia en {empresa} es **{mas_debil}**.
>
> {Párrafo por división, ver abajo}
>
> Esto es una señal, no un dictamen: el diagnóstico completo se hace con el dueño y las áreas clave, sobre la operación real, y termina con el mapa de dependencia y el orden en que se resuelve.
>
> Si quieres, agendamos una sesión. Responde este correo o escríbeme por WhatsApp al {whatsapp de Uriel}.
>
> Uriel Vargas
> Dirección · SYNKA

### Párrafo por división (usar el que corresponda a `mas_debil`)

- **ESTRUCTURA:** Cuando Estructura es el punto más débil, suele haber roles que se traslapan o que nadie ha definido, y decisiones que regresan al dueño porque no hay niveles claros. Lo primero es un organigrama real y quién decide qué.
- **COMERCIAL:** Si Comercial es el punto débil, las ventas dependen de quien las cierra, normalmente el dueño. Se trabaja con proceso de venta documentado, pipeline visible y cuotas por persona.
- **PROCESOS:** Si Procesos es el punto débil, cada quien hace lo mismo a su manera y el conocimiento vive en la memoria de personas concretas. Se empieza por los procesos que más fallan o que solo una persona domina.
- **OPERACIÓN:** Si Operación es el punto débil, la calidad del servicio depende de supervisión constante. Se definen estándares de servicio que se sostienen sin que alguien vigile.
- **PERSONAS:** Si Personas es el punto débil, faltan perfiles de puesto, evaluación y un proceso para que quien entra sepa qué hacer. Se estructuran responsabilidades y desempeño.
- **CONTROL:** Si Control es el punto débil, para saber cómo va la empresa hay que preguntar. Se construyen indicadores y un tablero para decidir sin pedir reportes.

## Día 2 · Correo (un artículo útil)

**Asunto:** Lo que suele pasar cuando {mas_debil} es el punto débil
**Cuerpo:** una frase de contexto + enlace al artículo que corresponda + una pregunta abierta.

| División | Artículo recomendado |
|---|---|
| ESTRUCTURA, PERSONAS | `/blog/como-delegar-en-mi-empresa` |
| COMERCIAL | `/blog/ventas-sin-depender-del-dueno` |
| PROCESOS, OPERACIÓN | `/blog/documentar-procesos-sin-burocracia` |
| CONTROL, general | `/blog/empresa-que-depende-del-dueno` |

> {nombre}, de los temas que más preguntan sobre {mas_debil}, este artículo resume lo esencial: {enlace con `utm_source=correo&utm_medium=email&utm_campaign=nurture-radar&utm_content=dia-2`}. ¿Qué parte te resuena más en {empresa}?

## Día 5 · WhatsApp (corto, sin presión)

> {nombre}, ¿pudiste ver lo que te mandé? Si quieres que revisemos tu resultado juntos, tengo espacio esta semana el {día} o el {día}.

## Día 8 · Correo (invitación directa + salida amable)

**Asunto:** ¿Revisamos tu diagnóstico, {nombre}?
> {nombre}, última nota por mi parte. El diagnóstico SYNKA es una sesión de trabajo con el dueño y las áreas clave; al terminar sabes qué depende de ti, por qué, y en qué orden se resuelve.
>
> Si es buen momento, aquí está mi agenda: {enlace a agenda}. Si no, no hay problema: tu resultado queda contigo y la puerta abierta.

*(Si no hay herramienta de agenda, ofrecer dos horarios concretos en lugar de un enlace.)*

---

## Cuando se automatice

Opciones sin código desde Formspree: Zapier/Make hacia Gmail o una hoja de cálculo. El correo del día 0 es el mejor candidato para automatizar primero (variables `nombre`, `resultado`, `mas_debil`, `empresa`, y el párrafo por división).
Antes de enviar correos automáticos, confirmar que el aviso de privacidad cubra el uso del dato para estos mensajes y que cada correo incluya una forma de dejar de recibirlos.
