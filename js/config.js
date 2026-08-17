/* ============================================================================
   SYNKA — Configuración del sitio
   Único archivo que se edita para poner el sitio en producción.
   ========================================================================== */

window.SYNKA_CONFIG = {

  /* --- Dominio ---------------------------------------------------------- */
  sitio: 'https://synka.mx',

  /* --- Contacto --------------------------------------------------------- */
  correo: 'contacto@synka.mx',

  // Formato E.164 para marcar. En México el "1" no se usa al llamar.
  telefono: '+525520654337',

  // Solo dígitos, para wa.me. Se conserva el "1" después del 52 porque es el
  // formato que ya venía funcionando en el sitio anterior de VESTRA.
  // Si el enlace fallara, quitar el 1: 525520654337.
  whatsapp: '5215520654337',

  linkedin: '',            // p. ej. 'https://www.linkedin.com/company/synka'

  /* --- Analítica -------------------------------------------------------
     Dejar vacío desactiva la carga: no se inyecta ningún script y el sitio
     funciona igual. Los eventos se siguen acumulando en dataLayer, así que
     al pegar el ID más adelante empieza a medir sin tocar nada más.         */
  gtmId: '',               // 'GTM-XXXXXXX'
  ga4Id: '',               // 'G-XXXXXXXXXX'

  /* --- Formulario ------------------------------------------------------
     Formspree. Crear el formulario en formspree.io, copiar el ID que aparece
     en el endpoint (https://formspree.io/f/ESTE_ID) y pegarlo abajo.
     Mientras esté vacío, el formulario compone un correo a `correo` y el
     sitio nunca se queda sin vía de contacto.                               */
  formspreeId: '',         // p. ej. 'xdorwkyz'

  /* --- Diagnóstico ------------------------------------------------------ */
  umbralMedio: 5,          // puntuación a partir de la cual el nivel es MEDIO
  umbralAlto: 11           // puntuación a partir de la cual el nivel es ALTO
};

/* El endpoint se arma solo a partir del ID. */
window.SYNKA_CONFIG.endpointFormulario = window.SYNKA_CONFIG.formspreeId
  ? 'https://formspree.io/f/' + window.SYNKA_CONFIG.formspreeId
  : '';
