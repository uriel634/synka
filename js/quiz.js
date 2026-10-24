/* ============================================================================
   SYNKA — Motor de diagnóstico
   Sirve a los dos instrumentos y a los que falten por construir. Sin
   dependencias. La página declara qué banco usar con data-quiz="radar" o
   data-quiz="comercial".
   ========================================================================== */

(function () {
  'use strict';

  var raiz = document.querySelector('[data-quiz]');
  if (!raiz) return;

  var CFG = window.SYNKA_CONFIG || {};
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var evento = window.synkaEvento || function () {};

  var tipo = raiz.getAttribute('data-quiz');
  var DATOS = tipo === 'radar' ? window.SYNKA_RADAR : window.SYNKA_COMERCIAL;
  if (!DATOS) return;

  /* Metadatos de las seis divisiones. Los colores son los valores negativos
     del manual (cap. 09): el resultado se pinta sobre navy. */
  var DIVISIONES = {
    estructura: { n: 'ESTRUCTURA', c: '#4FA3F0', url: '/soluciones/estructura',
                  d: 'Organigrama, roles y niveles de decisión.' },
    comercial:  { n: 'COMERCIAL',  c: '#F0845B', url: '/soluciones/comercial',
                  d: 'Estructura de ventas, pipeline y cuotas.' },
    procesos:   { n: 'PROCESOS',   c: '#00C9B7', url: '/soluciones/procesos',
                  d: 'SOP, POE y mapeo de flujos.' },
    operacion:  { n: 'OPERACIÓN',  c: '#9C86F5', url: '/soluciones/operacion',
                  d: 'Ejecución diaria y estándares de servicio.' },
    personas:   { n: 'PERSONAS',   c: '#D9AC55', url: '/soluciones/personas',
                  d: 'Perfiles, evaluación y desarrollo.' },
    control:    { n: 'CONTROL',    c: '#39C4A6', url: '/soluciones/control',
                  d: 'Indicadores, tablero y auditoría.' }
  };

  /* Semáforo construido con la propia paleta de divisiones, no con colores
     nuevos: COMERCIAL para crítico, PERSONAS para intermedio, CONTROL para
     sólido. Los tres pasan AA sobre navy. */
  var SEMAFORO = [
    { hasta: 40, etiqueta: 'CRÍTICO',    color: '#F0845B' },
    { hasta: 70, etiqueta: 'IRREGULAR',  color: '#D9AC55' },
    { hasta: 101, etiqueta: 'SÓLIDO',    color: '#39C4A6' }
  ];
  function semaforo(pct) {
    for (var i = 0; i < SEMAFORO.length; i++) if (pct < SEMAFORO[i].hasta) return SEMAFORO[i];
    return SEMAFORO[2];
  }

  var P = DATOS.preguntas;
  var i = 0;
  var respuestas = new Array(P.length).fill(null);
  var iniciado = false;

  var elPaso = raiz.querySelector('[data-paso]');
  var elAvance = raiz.querySelector('[data-avance]');
  var vistaP = raiz.querySelector('[data-vista-pregunta]');
  var vistaR = raiz.querySelector('[data-vista-resultado]');
  var elLegend = raiz.querySelector('[data-legend]');
  var elAyuda = raiz.querySelector('[data-ayuda]');
  var elOpciones = raiz.querySelector('[data-opciones]');
  var btnAtras = raiz.querySelector('[data-atras]');
  var btnReiniciar = raiz.querySelector('[data-reiniciar]');
  var elSinJs = raiz.querySelector('[data-sin-js]');

  function eje(q) { return tipo === 'radar' ? q.division : q.area; }

  /* --- Render de pregunta ------------------------------------------------ */

  function pintar() {
    var q = P[i];
    elPaso.textContent = pad(i + 1) + ' / ' + pad(P.length);
    elAvance.style.width = (i / P.length) * 100 + '%';
    elLegend.textContent = q.texto;

    if (q.ayuda) { elAyuda.textContent = q.ayuda; elAyuda.hidden = false; }
    else { elAyuda.hidden = true; }

    btnAtras.hidden = i === 0;

    elOpciones.textContent = '';
    q.opciones.forEach(function (o) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'quiz__opcion';
      b.textContent = o.t;
      b.setAttribute('aria-pressed', String(respuestas[i] === o.p));
      b.addEventListener('click', function () { responder(o.p); });
      elOpciones.appendChild(b);
    });
  }

  function pad(n) { return String(n).padStart(2, '0'); }

  function responder(p) {
    if (!iniciado) {
      iniciado = true;
      evento('diagnostico_iniciado', { instrumento: DATOS.id, total_preguntas: P.length });
    }
    respuestas[i] = p;
    if (i < P.length - 1) { i++; pintar(); }
    else resultado();
  }

  /* --- Cálculo ----------------------------------------------------------- */

  function calcular() {
    var ejes = {};
    P.forEach(function (q, idx) {
      var k = eje(q);
      var max = Math.max.apply(null, q.opciones.map(function (o) { return o.p; }));
      if (!ejes[k]) ejes[k] = { obtenido: 0, maximo: 0, preguntas: 0 };
      ejes[k].obtenido += respuestas[idx] || 0;
      ejes[k].maximo += max;
      ejes[k].preguntas++;
    });
    var totalObt = 0, totalMax = 0;
    Object.keys(ejes).forEach(function (k) {
      ejes[k].pct = Math.round((ejes[k].obtenido / ejes[k].maximo) * 100);
      totalObt += ejes[k].obtenido;
      totalMax += ejes[k].maximo;
    });
    return { ejes: ejes, obtenido: totalObt, maximo: totalMax,
             pct: Math.round((totalObt / totalMax) * 100) };
  }

  /* --- Radar hexagonal en SVG puro --------------------------------------- */

  function radarSVG(orden, ejes) {
    var cx = 150, cy = 138, R = 82, n = orden.length;
    function punto(idx, r) {
      var a = (-90 + idx * (360 / n)) * Math.PI / 180;
      return [cx + Math.cos(a) * r, cy + Math.sin(a) * r];
    }
    function poli(r) {
      var p = [];
      for (var k = 0; k < n; k++) { var q = punto(k, r); p.push(q[0].toFixed(1) + ',' + q[1].toFixed(1)); }
      return p.join(' ');
    }
    var s = '<svg viewBox="0 0 300 290" role="img" aria-label="Perfil por división" class="radar">';
    /* Retícula: cuatro anillos, filete de 1px, sin relleno */
    [0.25, 0.5, 0.75, 1].forEach(function (f) {
      s += '<polygon points="' + poli(R * f) + '" fill="none" stroke="#123A57" stroke-width="1"/>';
    });
    for (var k = 0; k < n; k++) {
      var e = punto(k, R);
      s += '<line x1="' + cx + '" y1="' + cy + '" x2="' + e[0].toFixed(1) + '" y2="' + e[1].toFixed(1) +
           '" stroke="#123A57" stroke-width="1"/>';
    }
    /* Perfil */
    var pts = [];
    orden.forEach(function (k, idx) {
      var v = Math.max(ejes[k].pct, 3) / 100;
      var q = punto(idx, R * v);
      pts.push(q[0].toFixed(1) + ',' + q[1].toFixed(1));
    });
    s += '<polygon class="radar__area" points="' + pts.join(' ') + '" fill="#00C9B7" fill-opacity="0.16" ' +
         'stroke="#00C9B7" stroke-width="2"/>';
    /* Vértices y etiquetas */
    orden.forEach(function (k, idx) {
      var v = Math.max(ejes[k].pct, 3) / 100;
      var q = punto(idx, R * v);
      var col = DIVISIONES[k] ? DIVISIONES[k].c : '#00C9B7';
      s += '<rect x="' + (q[0] - 3.5).toFixed(1) + '" y="' + (q[1] - 3.5).toFixed(1) +
           '" width="7" height="7" fill="' + col + '" transform="rotate(45 ' +
           q[0].toFixed(1) + ' ' + q[1].toFixed(1) + ')"/>';
      var l = punto(idx, R + 30);
      var anchor = Math.abs(l[0] - cx) < 6 ? 'middle' : (l[0] > cx ? 'start' : 'end');
      var nom = DIVISIONES[k] ? DIVISIONES[k].n : k.toUpperCase();
      s += '<text x="' + l[0].toFixed(1) + '" y="' + l[1].toFixed(1) + '" text-anchor="' + anchor +
           '" fill="#8FB4C9" font-family="IBM Plex Mono, monospace" font-size="10" letter-spacing="1.4">' +
           nom + '</text>';
      s += '<text x="' + l[0].toFixed(1) + '" y="' + (l[1] + 15).toFixed(1) + '" text-anchor="' + anchor +
           '" fill="' + col + '" font-family="IBM Plex Mono, monospace" font-size="13">' +
           ejes[k].pct + '%</text>';
    });
    return s + '</svg>';
  }

  /* --- Resultado --------------------------------------------------------- */

  function resultado() {
    var r = calcular();
    var orden = tipo === 'radar'
      ? ['estructura', 'comercial', 'procesos', 'operacion', 'personas', 'control']
      : DATOS.areas;

    /* Ejes ordenados de más débil a más fuerte */
    var debiles = orden.slice().sort(function (a, b) { return r.ejes[a].pct - r.ejes[b].pct; });
    var sem = semaforo(r.pct);

    var h = '';
    h += '<p class="diag__nivel">Tu resultado</p>';
    h += '<p class="diag__veredicto">' + (tipo === 'radar'
        ? r.pct + '% de control'
        : r.obtenido + ' / ' + r.maximo + ' puntos') + '</p>';
    h += '<p class="quiz__semaforo" style="--sem:' + sem.color + '">' + sem.etiqueta + '</p>';

    /* El hexágono aplica a cualquier instrumento de seis ejes, sean las seis
       divisiones o las seis áreas de una sola división. */
    if (orden.length === 6) {
      h += '<div class="quiz__radar">' + radarSVG(orden, r.ejes) + '</div>';
    }

    /* Barras por eje */
    h += '<ul class="quiz__ejes">';
    orden.forEach(function (k) {
      var e = r.ejes[k];
      var s2 = semaforo(e.pct);
      var nom = DIVISIONES[k] ? DIVISIONES[k].n : k;
      var col = DIVISIONES[k] ? DIVISIONES[k].c : s2.color;
      h += '<li class="quiz__eje" style="--rama:' + col + '">' +
           '<span class="quiz__eje-nom">' + (DIVISIONES[k] ? '<b>SYNKA</b> ' : '') +
             '<span>' + nom + '</span></span>' +
           '<span class="quiz__barra"><span style="width:' + e.pct + '%"></span></span>' +
           '<span class="quiz__eje-pct">' + e.pct + '%</span>' +
           '<span class="quiz__eje-sem" style="--sem:' + s2.color + '">' + s2.etiqueta + '</span>' +
           '</li>';
    });
    h += '</ul>';

    /* Foco: los tres ejes más débiles.
       Si el eje más flojo ya está en verde no hay punto débil que señalar, y
       afirmarlo sería inventar un hallazgo. Se muestran solo los que no lo están. */
    var flojos = debiles.filter(function (k) { return r.ejes[k].pct < SEMAFORO[1].hasta; }).slice(0, 3);

    if (!flojos.length) {
      h += '<div class="quiz__foco"><span class="dato">SIN PUNTOS DÉBILES DETECTADOS</span>' +
           '<p class="quiz__nota">Ninguna división quedó por debajo del umbral. Con este perfil ' +
           'el trabajo no es soltar más, sino sostener lo construido para que no se degrade.</p></div>';
    } else {
    h += '<div class="quiz__foco">';
    h += '<span class="dato">' + (tipo === 'radar'
        ? 'DONDE SE CONCENTRA LA DEPENDENCIA'
        : 'TUS ÁREAS MÁS DÉBILES') + '</span>';
    h += '<ol class="quiz__lista-foco">';
    flojos.forEach(function (k) {
      var d = DIVISIONES[k];
      h += '<li style="--rama:' + (d ? d.c : '#00C9B7') + '">' +
           '<span class="quiz__eje-nom">' + (d ? '<b>SYNKA</b> ' : '') +
             '<span>' + (d ? d.n : k) + '</span></span>' +
           '<span class="quiz__foco-pct">' + r.ejes[k].pct + '%</span>' +
           (d ? '<p>' + d.d + ' <a href="' + d.url + '" data-cta="division_desde_' + DATOS.id + '">Ver división</a></p>' : '') +
           '</li>';
    });
    h += '</ol></div>';
    }

    if (tipo === 'comercial') {
      h += '<p class="quiz__nota">Las seis áreas de arriba son la anatomía de una sola división: ' +
           '<a href="../soluciones/comercial.html" data-cta="division_desde_comercial"><b>SYNKA</b> COMERCIAL</a>.</p>';
    }

    /* Captura del lead en el momento de mayor interés: justo al ver el resultado.
       Antes este punto mandaba a la portada y quien no volvía a llenar el
       formulario largo se perdía. */
    h += '<div class="quiz__lead" data-lead>' +
         '<span class="dato">RECIBE ESTE RESULTADO Y AGENDA TU DIAGNÓSTICO</span>' +
         '<p class="quiz__lead-texto">Te escribimos para revisar este perfil contigo y acordar una sesión de diagnóstico. Sin costo y sin compromiso.</p>' +
         '<form class="form" data-form-lead novalidate>' +
           '<div class="trampa" aria-hidden="true"><label for="lead_web">No llenar</label>' +
             '<input type="text" id="lead_web" name="empresa_web" tabindex="-1" autocomplete="off"></div>' +
           '<div class="form__fila form__fila--2">' +
             '<p class="campo"><label for="lead_nombre">Nombre <span aria-hidden="true">*</span></label>' +
               '<input type="text" id="lead_nombre" name="nombre" autocomplete="name" required></p>' +
             '<p class="campo"><label for="lead_empresa">Empresa <span aria-hidden="true">*</span></label>' +
               '<input type="text" id="lead_empresa" name="empresa" autocomplete="organization" required></p>' +
           '</div>' +
           '<div class="form__fila form__fila--2">' +
             '<p class="campo"><label for="lead_whatsapp">WhatsApp <span aria-hidden="true">*</span></label>' +
               '<input type="tel" id="lead_whatsapp" name="whatsapp" autocomplete="tel" inputmode="tel" required></p>' +
             '<p class="campo"><label for="lead_email">Email <span aria-hidden="true">*</span></label>' +
               '<input type="email" id="lead_email" name="email" autocomplete="email" inputmode="email" required></p>' +
           '</div>' +
           '<p class="campo"><label for="lead_colab">Número aproximado de colaboradores <span aria-hidden="true">*</span></label>' +
             '<select id="lead_colab" name="colaboradores" required>' +
               '<option value="">Selecciona</option><option value="1-4">1 a 4</option><option value="5-15">5 a 15</option>' +
               '<option value="16-50">16 a 50</option><option value="51-100">51 a 100</option><option value="100+">Más de 100</option>' +
             '</select></p>' +
           '<p class="form__error" data-lead-error role="alert" hidden></p>' +
           '<button class="btn btn--primario btn--bloque" type="submit" data-cta="enviar_formulario" data-seccion="' + DATOS.id + '_resultado">Quiero mi diagnóstico</button>' +
           '<p class="form__aviso">Usamos tus datos únicamente para contactarte sobre el diagnóstico.</p>' +
         '</form></div>';

    h += '<div class="grupo-cta">' +
         '<button type="button" class="diag__reiniciar" data-reiniciar-2>Volver a empezar</button>' +
         '</div>';

    h += '<p class="form__aviso quiz__descargo">Esta autoevaluación refleja tus propias respuestas. ' +
         'No es un dictamen: el diagnóstico SYNKA se hace con el dueño y las áreas clave, sobre tu operación real.</p>';

    vistaR.innerHTML = h;
    vistaP.hidden = true;
    vistaR.setAttribute('data-visible', 'true');
    elAvance.style.width = '100%';
    elPaso.textContent = 'RESULTADO';

    vistaR.querySelector('[data-reiniciar-2]').addEventListener('click', reiniciar);

    var carga = { instrumento: DATOS.id, puntuacion: r.obtenido, maximo: r.maximo,
                  porcentaje: r.pct, nivel: sem.etiqueta };
    orden.forEach(function (k) { carga['eje_' + k] = r.ejes[k].pct; });
    carga.mas_debil = DIVISIONES[debiles[0]] ? DIVISIONES[debiles[0]].n : debiles[0];
    evento('diagnostico_terminado', carga);

    conectarLead(carga, orden.map(function (k) { return k + ' ' + r.ejes[k].pct + '%'; }).join(' · '));

    vistaR.focus({ preventScroll: true });
    vistaR.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
  }

  /* --- Formulario de lead dentro del resultado --------------------------- */

  function conectarLead(carga, perfil) {
    var form = vistaR.querySelector('[data-form-lead]');
    if (!form) return;
    var error = form.querySelector('[data-lead-error]');
    var enviar = form.querySelector('[type="submit"]');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      error.hidden = true;
      if (form.querySelector('[name="empresa_web"]').value) return;
      if (!form.checkValidity()) {
        form.reportValidity();
        error.textContent = 'Revisa los campos marcados: falta información obligatoria.';
        error.hidden = false;
        evento('formulario_error', { motivo: 'validacion', origen: DATOS.id + '_resultado' });
        return;
      }

      var datos = {};
      new FormData(form).forEach(function (v, k) { if (k !== 'empresa_web') datos[k] = v; });
      datos.origen = window.location.pathname;
      datos.instrumento = DATOS.id;
      datos.resultado = carga.nivel + ' · ' + carga.porcentaje + '%';
      datos.mas_debil = carga.mas_debil;
      datos.perfil = perfil;
      datos.enviado_en = new Date().toISOString();
      var atr = window.synkaAtribucion ? window.synkaAtribucion() : {};
      for (var ak in atr) { if (Object.prototype.hasOwnProperty.call(atr, ak)) datos[ak] = atr[ak]; }

      evento('formulario_enviado', { origen: DATOS.id + '_resultado', colaboradores: datos.colaboradores });

      var original = enviar.textContent;
      enviar.disabled = true;
      enviar.textContent = 'Enviando…';

      function exito() {
        var wa = CFG.whatsapp
          ? '<p style="margin-top:1.25rem"><a class="btn btn--primario" target="_blank" rel="noopener" href="https://wa.me/' +
            CFG.whatsapp + '?text=' + encodeURIComponent('Hola, acabo de hacer el ' + DATOS.id +
            ' en synka.mx. Mi resultado: ' + datos.resultado + '. Mi punto más débil: ' + datos.mas_debil + '.') +
            '">Escríbenos por WhatsApp</a></p>'
          : '';
        form.outerHTML = '<div class="quiz__lead-ok" role="status"><span class="dato">RECIBIDO</span>' +
          '<p class="quiz__lead-texto">Gracias, ' + (datos.nombre || '').replace(/[<>&"]/g, '') +
          '. Te escribiremos por WhatsApp o correo para acordar el día y la hora de tu diagnóstico.</p>' + wa + '</div>';
        evento('formulario_exito', { origen: DATOS.id + '_resultado' });
        evento('generate_lead', { origen: DATOS.id + '_resultado', nivel: carga.nivel,
                                  mas_debil: carga.mas_debil,
                                  utm_source: atr.utm_source || '', utm_campaign: atr.utm_campaign || '' });
      }

      function fallo(motivo) {
        enviar.disabled = false;
        enviar.textContent = original;
        error.innerHTML = 'No pudimos enviar tus datos. Escríbenos directo a ' +
          '<a href="mailto:' + (CFG.correo || '') + '">' + (CFG.correo || '') + '</a>.';
        error.hidden = false;
        evento('formulario_error', { motivo: motivo, origen: DATOS.id + '_resultado' });
      }

      if (CFG.endpointFormulario) {
        datos._subject = 'Lead ' + DATOS.id + ' — ' + datos.empresa + ' (' + datos.resultado + ')';
        fetch(CFG.endpointFormulario, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify(datos)
        }).then(function (r) { r.ok ? exito() : fallo('http_' + r.status); })
          .catch(function () { fallo('red'); });
      } else {
        var cuerpo = Object.keys(datos).map(function (k) {
          return k.replace(/_/g, ' ').toUpperCase() + ': ' + datos[k];
        }).join('\n');
        window.location.href = 'mailto:' + (CFG.correo || '') + '?subject=' +
          encodeURIComponent('Lead ' + DATOS.id + ' — ' + datos.empresa) + '&body=' + encodeURIComponent(cuerpo);
        setTimeout(exito, 600);
      }
    });
  }

  function reiniciar() {
    i = 0;
    respuestas = new Array(P.length).fill(null);
    iniciado = false;
    vistaR.removeAttribute('data-visible');
    vistaR.innerHTML = '';
    vistaP.hidden = false;
    pintar();
    raiz.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
  }

  btnAtras.addEventListener('click', function () { if (i > 0) { i--; pintar(); } });
  if (btnReiniciar) btnReiniciar.addEventListener('click', reiniciar);

  if (elSinJs) elSinJs.hidden = true;
  vistaP.hidden = false;
  pintar();
})();
