/* ============================================================================
   SYNKA — Comportamiento del sitio
   Sin dependencias. Todo el contenido crítico existe en el HTML: este archivo
   solo mejora la experiencia. Si no se ejecuta, el sitio sigue siendo legible
   y contactable.
   ========================================================================== */

(function () {
  'use strict';

  var CFG = window.SYNKA_CONFIG || {};
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* --- 1 · Analítica ----------------------------------------------------
     Capa única. Si no hay GTM ni GA4 configurados, los eventos se acumulan
     en dataLayer y no se pierde el contrato de medición.                    */

  window.dataLayer = window.dataLayer || [];

  function evento(nombre, datos) {
    var carga = { event: nombre };
    for (var k in datos) { if (Object.prototype.hasOwnProperty.call(datos, k)) carga[k] = datos[k]; }
    window.dataLayer.push(carga);
    if (typeof window.gtag === 'function') window.gtag('event', nombre, datos || {});
  }
  window.synkaEvento = evento;

  function cargarAnalitica() {
    if (CFG.gtmId) {
      window.dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' });
      var g = document.createElement('script');
      g.async = true;
      g.src = 'https://www.googletagmanager.com/gtm.js?id=' + encodeURIComponent(CFG.gtmId);
      document.head.appendChild(g);
    }
    if (CFG.ga4Id) {
      var s = document.createElement('script');
      s.async = true;
      s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(CFG.ga4Id);
      document.head.appendChild(s);
      window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
      window.gtag('js', new Date());
      window.gtag('config', CFG.ga4Id);
    }
  }
  cargarAnalitica();

  /* Clic en cualquier CTA marcada */
  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-cta]');
    if (!el) return;
    evento('cta_clic', {
      cta_nombre: el.getAttribute('data-cta'),
      cta_seccion: el.getAttribute('data-seccion') || '',
      cta_texto: (el.textContent || '').trim().slice(0, 60)
    });
  });

  /* Clic en WhatsApp */
  document.addEventListener('click', function (e) {
    var el = e.target.closest('a[href*="wa.me"]');
    if (el) evento('whatsapp_clic', { destino: el.getAttribute('href') });
  });

  /* Profundidad de scroll: 25 / 50 / 75 / 100 */
  (function () {
    var hitos = [25, 50, 75, 100], vistos = {}, pendiente = false;
    function medir() {
      pendiente = false;
      var alto = document.documentElement.scrollHeight - window.innerHeight;
      if (alto <= 0) return;
      var pct = Math.min(100, Math.round((window.scrollY / alto) * 100));
      for (var i = 0; i < hitos.length; i++) {
        if (pct >= hitos[i] && !vistos[hitos[i]]) {
          vistos[hitos[i]] = true;
          evento('scroll_profundidad', { porcentaje: hitos[i] });
        }
      }
    }
    window.addEventListener('scroll', function () {
      if (!pendiente) { pendiente = true; window.requestAnimationFrame(medir); }
    }, { passive: true });
  })();

  /* --- 2 · Contacto configurable ---------------------------------------- */

  (function () {
    document.querySelectorAll('[data-correo]').forEach(function (a) {
      if (!CFG.correo) return;
      a.href = 'mailto:' + CFG.correo;
      if (a.hasAttribute('data-rellena')) a.textContent = CFG.correo;
    });
    document.querySelectorAll('[data-telefono]').forEach(function (a) {
      if (!CFG.telefono) { var c = a.closest('[data-oculta-si-vacio]'); if (c) c.hidden = true; return; }
      a.href = 'tel:' + CFG.telefono;
      if (a.hasAttribute('data-rellena')) a.textContent = CFG.telefono;
    });
    document.querySelectorAll('[data-linkedin]').forEach(function (a) {
      if (!CFG.linkedin) { var c = a.closest('[data-oculta-si-vacio]'); if (c) c.hidden = true; return; }
      a.href = CFG.linkedin;
    });
    document.querySelectorAll('[data-whatsapp]').forEach(function (a) {
      if (!CFG.whatsapp) { a.hidden = true; return; }
      a.href = 'https://wa.me/' + CFG.whatsapp;
      a.hidden = false;
    });
  })();

  /* --- 3 · Navegación ---------------------------------------------------- */

  (function () {
    var btn = document.querySelector('[data-menu-btn]');
    var panel = document.querySelector('[data-menu]');
    if (!btn || !panel) return;

    function cerrar() {
      btn.setAttribute('aria-expanded', 'false');
      panel.setAttribute('data-abierto', 'false');
    }
    btn.addEventListener('click', function () {
      var abierto = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!abierto));
      panel.setAttribute('data-abierto', String(!abierto));
    });
    panel.addEventListener('click', function (e) { if (e.target.closest('a')) cerrar(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') cerrar(); });
    window.addEventListener('resize', function () { if (window.innerWidth >= 1000) cerrar(); });
  })();

  /* Sección activa en la navegación + barra de progreso */
  (function () {
    var barra = document.querySelector('[data-progreso]');
    var enlaces = Array.prototype.slice.call(document.querySelectorAll('.nav__enlace[href^="#"]'));
    var secciones = enlaces
      .map(function (a) { return document.querySelector(a.getAttribute('href')); })
      .filter(Boolean);
    var pendiente = false;

    function pintar() {
      pendiente = false;
      if (barra) {
        var alto = document.documentElement.scrollHeight - window.innerHeight;
        barra.style.transform = 'scaleX(' + (alto > 0 ? Math.min(1, window.scrollY / alto) : 0) + ')';
      }
      if (!secciones.length) return;
      var y = window.scrollY + window.innerHeight * 0.32;
      var activa = null;
      for (var i = 0; i < secciones.length; i++) {
        if (secciones[i].offsetTop <= y) activa = secciones[i];
      }
      enlaces.forEach(function (a) {
        var on = activa && a.getAttribute('href') === '#' + activa.id;
        if (on) a.setAttribute('aria-current', 'true');
        else a.removeAttribute('aria-current');
      });
    }
    window.addEventListener('scroll', function () {
      if (!pendiente) { pendiente = true; window.requestAnimationFrame(pintar); }
    }, { passive: true });
    pintar();
  })();

  /* --- 4 · Movimiento ----------------------------------------------------
     Dos únicos efectos, ambos explican el concepto de la marca:
     los cuatro brazos convergiendo, y las partes de un sistema entrando en
     secuencia. Nada decorativo.                                             */

  (function () {
    if (reduce || !('IntersectionObserver' in window)) {
      document.querySelectorAll('[data-signo]').forEach(function (s) { s.setAttribute('data-sync', 'true'); });
      document.querySelectorAll('.aparece').forEach(function (s) { s.setAttribute('data-visto', 'true'); });
      return;
    }
    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        if (el.hasAttribute('data-signo')) el.setAttribute('data-sync', 'true');
        else el.setAttribute('data-visto', 'true');
        obs.unobserve(el);
      });
    }, { threshold: 0.25, rootMargin: '0px 0px -8% 0px' });

    document.querySelectorAll('[data-signo], .aparece').forEach(function (el) { obs.observe(el); });
  })();

  /* --- 5 · Diagnóstico ---------------------------------------------------
     Ocho preguntas. Cuatro están redactadas en positivo: en ellas un "Sí"
     resta dependencia. Eso lo resuelve el campo `invierte`.                 */

  var PREGUNTAS = [
    { t: '¿Tu equipo necesita preguntarte antes de tomar decisiones?', rama: 'estructura', invierte: false },
    { t: '¿Si te ausentas, la operación se complica?',                 rama: 'operacion',  invierte: false },
    { t: '¿Existen procesos que solamente una persona conoce?',        rama: 'procesos',   invierte: false },
    { t: '¿Cada colaborador trabaja de manera diferente?',             rama: 'personas',   invierte: false },
    { t: '¿Tus ventas tienen un proceso definido?',                    rama: 'comercial',  invierte: true },
    { t: '¿Tienes indicadores claros?',                                rama: 'control',    invierte: true },
    { t: '¿Tu operación está documentada?',                            rama: 'procesos',   invierte: true },
    { t: '¿Sabes exactamente quién es responsable de cada proceso?',   rama: 'estructura', invierte: true }
  ];

  /* Los valores negativos del manual: el panel de foco va sobre navy. */
  var RAMAS = {
    estructura: { n: 'ESTRUCTURA', color: 'var(--div-estructura-neg)', d: 'Organigrama, roles y niveles de decisión que no regresan a ti.', url: '/soluciones/estructura' },
    comercial:  { n: 'COMERCIAL',  color: 'var(--div-comercial-neg)',  d: 'Estructura de ventas, pipeline y cuotas que no dependen del dueño vendiendo.', url: '/soluciones/comercial' },
    procesos:   { n: 'PROCESOS',   color: 'var(--div-procesos-neg)',   d: 'SOP, POE y mapeo de flujos que cualquiera puede ejecutar.', url: '/soluciones/procesos' },
    operacion:  { n: 'OPERACIÓN',  color: 'var(--div-operacion-neg)',  d: 'Ejecución diaria y estándares de servicio que se sostienen sin supervisión.', url: '/soluciones/operacion' },
    personas:   { n: 'PERSONAS',   color: 'var(--div-personas-neg)',   d: 'Perfiles de puesto, evaluación y desarrollo del equipo.', url: '/soluciones/personas' },
    control:    { n: 'CONTROL',    color: 'var(--div-control-neg)',    d: 'Indicadores, tablero y auditoría para saber cómo va la empresa sin preguntar.', url: '/soluciones/control' }
  };

  var NIVELES = {
    alto: {
      etiqueta: 'ALTO',
      texto: 'Tu empresa tiene operación, pero una parte importante del sistema todavía depende de ti. Las decisiones, las excepciones y el criterio siguen pasando por una sola persona.'
    },
    medio: {
      etiqueta: 'MEDIO',
      texto: 'Tu empresa ya tiene partes que funcionan solas y partes que no. Lo que falta no es esfuerzo: es que lo que hoy vive en tu cabeza quede escrito, asignado y medido.'
    },
    bajo: {
      etiqueta: 'BAJO',
      texto: 'Tu empresa opera con un grado alto de autonomía. El siguiente paso no es soltar más, es sostener lo construido con indicadores y control para que no se degrade.'
    }
  };

  (function () {
    var raiz = document.querySelector('[data-diagnostico]');
    if (!raiz) return;

    var vistaPregunta = raiz.querySelector('[data-vista-pregunta]');
    var vistaResultado = raiz.querySelector('[data-vista-resultado]');
    var elLegend = raiz.querySelector('[data-legend]');
    var elOpciones = raiz.querySelector('[data-opciones]');
    var elPaso = raiz.querySelector('[data-paso]');
    var elAvance = raiz.querySelector('[data-avance]');
    var btnAtras = raiz.querySelector('[data-atras]');
    var btnReiniciar = raiz.querySelector('[data-reiniciar]');
    var elVeredicto = raiz.querySelector('[data-veredicto]');
    var elTextoNivel = raiz.querySelector('[data-texto-nivel]');
    var elMedidor = raiz.querySelector('[data-medidor]');
    var elFoco = raiz.querySelector('[data-foco]');

    var i = 0;
    var respuestas = new Array(PREGUNTAS.length).fill(null);
    var iniciado = false;

    var OPCIONES = [
      { et: 'Sí', v: 2 },
      { et: 'A veces', v: 1 },
      { et: 'No', v: 0 }
    ];

    function pintar() {
      var p = PREGUNTAS[i];
      elPaso.textContent = String(i + 1).padStart(2, '0') + ' / ' + String(PREGUNTAS.length).padStart(2, '0');
      elAvance.style.width = (i / PREGUNTAS.length) * 100 + '%';
      elLegend.textContent = p.t;
      btnAtras.hidden = i === 0;

      elOpciones.textContent = '';
      OPCIONES.forEach(function (o) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'diag__opcion';
        b.textContent = o.et;
        var puntos = p.invierte ? (2 - o.v) : o.v;
        b.setAttribute('aria-pressed', String(respuestas[i] === puntos));
        b.addEventListener('click', function () { responder(puntos); });
        elOpciones.appendChild(b);
      });
    }

    function responder(puntos) {
      if (!iniciado) {
        iniciado = true;
        evento('diagnostico_iniciado', { total_preguntas: PREGUNTAS.length });
      }
      respuestas[i] = puntos;
      evento('diagnostico_pregunta', { pregunta: i + 1, puntos: puntos });
      if (i < PREGUNTAS.length - 1) { i++; pintar(); }
      else resultado();
    }

    function resultado() {
      var total = respuestas.reduce(function (a, b) { return a + (b || 0); }, 0);
      var max = PREGUNTAS.length * 2;

      var nivel = total >= (CFG.umbralAlto || 11) ? 'alto'
                : total >= (CFG.umbralMedio || 5) ? 'medio' : 'bajo';

      /* Rama con más dependencia acumulada */
      var porRama = {};
      PREGUNTAS.forEach(function (p, idx) {
        porRama[p.rama] = (porRama[p.rama] || 0) + (respuestas[idx] || 0);
      });
      var focoClave = Object.keys(porRama).sort(function (a, b) {
        return porRama[b] - porRama[a];
      })[0];
      var foco = RAMAS[focoClave];

      /* Si ninguna rama acumuló dependencia, no hay "mayor punto de dependencia"
         que señalar. Afirmarlo sería inventar un hallazgo. */
      var hayFoco = porRama[focoClave] > 0;
      elFoco.hidden = !hayFoco;

      elVeredicto.textContent = 'NIVEL DE DEPENDENCIA: ' + NIVELES[nivel].etiqueta;
      elTextoNivel.textContent = NIVELES[nivel].texto;

      elMedidor.textContent = '';
      for (var k = 0; k < max; k++) {
        var s = document.createElement('span');
        if (k < total) s.setAttribute('data-on', 'true');
        elMedidor.appendChild(s);
      }
      elMedidor.setAttribute('aria-label', 'Puntuación de dependencia: ' + total + ' de ' + max);

      elFoco.style.setProperty('--foco', foco.color);
      elFoco.querySelector('[data-foco-nombre]').textContent = foco.n;
      elFoco.querySelector('[data-foco-desc]').textContent = foco.d;
      var enlaceFoco = elFoco.querySelector('[data-foco-url]');
      if (enlaceFoco) enlaceFoco.href = foco.url;

      vistaPregunta.hidden = true;
      vistaResultado.setAttribute('data-visible', 'true');
      elAvance.style.width = '100%';
      elPaso.textContent = 'RESULTADO';

      evento('diagnostico_terminado', {
        puntuacion: total,
        puntuacion_maxima: max,
        nivel: NIVELES[nivel].etiqueta,
        foco: hayFoco ? foco.n : 'ninguno'
      });

      /* El resultado se anuncia a lectores de pantalla por aria-live */
      vistaResultado.focus({ preventScroll: true });
      vistaResultado.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
    }

    btnAtras.addEventListener('click', function () { if (i > 0) { i--; pintar(); } });
    btnReiniciar.addEventListener('click', function () {
      i = 0;
      respuestas = new Array(PREGUNTAS.length).fill(null);
      iniciado = false;
      vistaResultado.removeAttribute('data-visible');
      vistaPregunta.hidden = false;
      pintar();
      raiz.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    });

    raiz.querySelector('[data-sin-js]').hidden = true;
    vistaPregunta.hidden = false;
    pintar();
  })();

  /* --- 6 · Formulario ---------------------------------------------------- */

  (function () {
    var form = document.querySelector('[data-form-diagnostico]');
    if (!form) return;

    var error = form.querySelector('[data-form-error]');
    var enviar = form.querySelector('[type="submit"]');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      error.hidden = true;

      /* Trampa anti-bots: si viene llena, se descarta en silencio */
      if (form.querySelector('[name="empresa_web"]').value) return;

      if (!form.checkValidity()) {
        form.reportValidity();
        error.textContent = 'Revisa los campos marcados: falta información obligatoria.';
        error.hidden = false;
        evento('formulario_error', { motivo: 'validacion' });
        return;
      }

      var datos = {};
      new FormData(form).forEach(function (v, k) { if (k !== 'empresa_web') datos[k] = v; });
      datos.origen = window.location.pathname;
      datos.enviado_en = new Date().toISOString();

      evento('formulario_enviado', {
        colaboradores: datos.colaboradores || '',
        depende_de: datos.depende_de || ''
      });

      var textoOriginal = enviar.textContent;
      enviar.disabled = true;
      enviar.textContent = 'Enviando…';

      function exito() {
        form.innerHTML =
          '<div class="diag__nivel">SOLICITUD RECIBIDA</div>' +
          '<p class="t-h3" style="max-width:26ch;margin-bottom:1rem">Gracias. Te contactamos para agendar el diagnóstico.</p>' +
          '<p>Revisa tu correo: ahí llega la confirmación con los siguientes pasos.</p>';
        evento('formulario_exito', {});
      }

      function fallo(motivo) {
        enviar.disabled = false;
        enviar.textContent = textoOriginal;
        error.innerHTML = 'No pudimos enviar la solicitud. Escríbenos directo a ' +
          '<a href="mailto:' + (CFG.correo || '') + '">' + (CFG.correo || '') + '</a>.';
        error.hidden = false;
        evento('formulario_error', { motivo: motivo });
      }

      if (CFG.endpointFormulario) {
        /* Formspree: `Accept: application/json` es lo que evita que responda
           con su página de gracias y devuelva JSON. `_subject` define el asunto
           del correo que llega. */
        datos._subject = 'Solicitud de diagnóstico — ' + (datos.empresa || datos.nombre || '');
        fetch(CFG.endpointFormulario, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify(datos)
        }).then(function (r) { r.ok ? exito() : fallo('http_' + r.status); })
          .catch(function () { fallo('red'); });
      } else {
        /* Sin endpoint configurado: se compone un correo con los datos.
           El sitio nunca se queda sin vía de conversión.                   */
        var cuerpo = Object.keys(datos).map(function (k) {
          return k.replace(/_/g, ' ').toUpperCase() + ': ' + datos[k];
        }).join('\n');
        window.location.href = 'mailto:' + (CFG.correo || '') +
          '?subject=' + encodeURIComponent('Solicitud de diagnóstico — ' + (datos.empresa || '')) +
          '&body=' + encodeURIComponent(cuerpo);
        setTimeout(exito, 600);
      }
    });
  })();

})();
