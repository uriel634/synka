/* ============================================================================
   SYNKA — Configuración del sitio
   Único archivo que se edita para poner el sitio en producción.
   No contiene credenciales reales: todos los identificadores están vacíos
   y el sitio funciona sin ellos.
   ========================================================================== */

window.SYNKA_CONFIG = {

  /* --- Dominio ---------------------------------------------------------- */
  sitio: 'https://synka.mx',

  /* --- Contacto --------------------------------------------------------
     Los valores de abajo son los placeholder del manual de marca.
     Sustituir por los reales antes de publicar.                            */
  correo: 'hola@synka.mx',
  telefono: '',            // formato E.164, p. ej. '+525512345678'
  whatsapp: '',            // solo dígitos, p. ej. '525512345678'
                           // vacío => no se muestra el botón de WhatsApp
  linkedin: '',            // p. ej. 'https://www.linkedin.com/company/synka'

  /* --- Analítica -------------------------------------------------------
     Dejar vacío desactiva la carga. No se inyecta ningún script si no hay ID. */
  gtmId: '',               // 'GTM-XXXXXXX'
  ga4Id: '',               // 'G-XXXXXXXXXX'

  /* --- Formulario ------------------------------------------------------
     Endpoint que recibe el POST en JSON. Vacío => el formulario compone un
     correo con los datos y lo abre en el cliente del usuario.
     Para conectar un CRM, apuntar aquí a la función/webhook intermedia.      */
  endpointFormulario: '',

  /* --- Diagnóstico ------------------------------------------------------ */
  umbralMedio: 5,          // puntuación a partir de la cual el nivel es MEDIO
  umbralAlto: 11           // puntuación a partir de la cual el nivel es ALTO
};
