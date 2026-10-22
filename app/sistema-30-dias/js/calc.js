/* SYNKA · Sistema 30 Días — lógica de cálculo (sin DOM, sin red).
   Fechas como 'AAAA-MM-DD'. Funciona en el navegador (window.SynkaCalc) y en Node. */
(function (root) {
  'use strict';

  var pad = function (n) { return String(n).padStart(2, '0'); };
  var iso = function (d) { return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); };
  var fromIso = function (s) { var a = s.split('-').map(Number); return new Date(a[0], a[1] - 1, a[2]); };
  var addDays = function (s, n) { var d = fromIso(s); d.setDate(d.getDate() + n); return iso(d); };
  var isWeekday = function (s) { var g = fromIso(s).getDay(); return g >= 1 && g <= 5; };
  var mondayOf = function (s) { var d = fromIso(s); d.setDate(d.getDate() - ((d.getDay() + 6) % 7)); return iso(d); };

  /* Días hábiles (lun-vie) de un mes, sin los que el vendedor marcó ausente o festivo.
     mes = 'AAAA-MM'; descontar = array de fechas. */
  function diasHabiles(mes, descontar) {
    var skip = {}; (descontar || []).forEach(function (f) { skip[f] = 1; });
    var y = +mes.slice(0, 4), m = +mes.slice(5, 7) - 1, n = new Date(y, m + 1, 0).getDate(), out = [];
    for (var d = 1; d <= n; d++) {
      var f = y + '-' + pad(m + 1) + '-' + pad(d);
      if (isWeekday(f) && !skip[f]) out.push(f);
    }
    return out;
  }

  /* Qué parte del mes (0..1) cae en la semana que empieza en `lunes`.
     Reparte la cuota por días hábiles reales, no mes ÷ 4. Una semana a caballo entre dos
     meses cuenta solo los días del mes pedido. */
  function fraccionSemana(lunes, mes, descontar) {
    var mesDias = diasHabiles(mes, descontar);
    if (!mesDias.length) return 0;
    var fin = addDays(lunes, 6);
    var enSemana = mesDias.filter(function (f) { return f >= lunes && f <= fin; });
    return enSemana.length / mesDias.length;
  }

  /* Cuánta actividad exige una cuota mensual. Si el ticket es 0 no se puede calcular. */
  function minimosMes(cuota, ticket, tCierrePct, tPropPct) {
    var tc = Math.max((tCierrePct || 0) / 100, 0.01), tp = Math.max((tPropPct || 0) / 100, 0.01);
    var ventas = ticket > 0 ? cuota / ticket : 0, prop = ventas / tc, cont = prop / tp;
    return { ventas: ventas, prop: prop, cont: cont };
  }

  /* Mínimo de una semana concreta: el del mes por la fracción de días hábiles de esa semana. */
  function minimosSemana(cuota, ticket, tCierrePct, tPropPct, lunes, mes, descontar) {
    var f = fraccionSemana(lunes, mes, descontar), m = minimosMes(cuota, ticket, tCierrePct, tPropPct);
    return { ventas: m.ventas * f, prop: m.prop * f, cont: m.cont * f, cuota: cuota * f, fraccion: f };
  }

  /* Cuánto del mínimo debería llevar hecho hoy dentro de una semana.
     Cuenta los días hábiles transcurridos (incluido hoy) sobre los de esa semana en el mes. */
  function avanceEsperado(lunes, hoy, mes, descontar) {
    var dias = diasHabiles(mes, descontar).filter(function (f) { return f >= lunes && f <= addDays(lunes, 6); });
    if (!dias.length) return 0;
    if (hoy < lunes) return 0;
    var pasados = dias.filter(function (f) { return f <= hoy; }).length;
    return pasados / dias.length;
  }

  /* Semáforo: verde ≥ 90 %, amarillo ≥ 70 %, rojo debajo. 'n' si no hay base de comparación. */
  function semaforo(ratio, hayDato) {
    if (!hayDato) return 'n';
    return ratio >= 0.9 ? 'g' : ratio >= 0.7 ? 'y' : 'r';
  }

  /* Pronóstico de cierre: lo ya cerrado, más cada oportunidad abierta con cierre en el mes por la
     probabilidad de su etapa. `etapas` = {id: prob%}. */
  function pronostico(opps, etapas, mes, hoy) {
    hoy = hoy || iso(new Date());
    var cerrado = 0, esperado = 0, conservador = 0, optimista = 0, sinFecha = 0, vencidas = 0;
    opps.forEach(function (o) {
      if (o.estado === 'ganada') { if ((o.fReal || '').slice(0, 7) === mes) cerrado += o.valor; return; }
      if (o.estado === 'perdida') return;
      if (!o.fcierre) { sinFecha++; return; }
      if (o.fcierre < hoy) vencidas++;
      if (o.fcierre.slice(0, 7) !== mes) return;
      var p = (etapas[o.etapa] || 0) / 100;
      esperado += o.valor * p; optimista += o.valor;
      if (p >= 0.5) conservador += o.valor * p;
    });
    return { cerrado: cerrado, esperado: cerrado + esperado, conservador: cerrado + conservador,
             optimista: cerrado + optimista, sinFecha: sinFecha, cierreVencido: vencidas };
  }

  /* ───────── WhatsApp ───────── */
  function waLink(numero, texto) {
    var n = String(numero || '').replace(/\D/g, '');
    return 'https://wa.me/' + n + '?text=' + encodeURIComponent(texto);
  }

  var dinero = function (v, moneda) {
    try { return new Intl.NumberFormat('es-MX', { style: 'currency', currency: moneda || 'MXN', maximumFractionDigits: 0 }).format(v || 0); }
    catch (e) { return '$' + Math.round(v || 0); }
  };
  var corta = function (s) {
    var m = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'], d = fromIso(s);
    return d.getDate() + ' ' + m[d.getMonth()];
  };

  /* Reporte semanal del dueño. filas = [{nombre, contactos, propuestas, minCont, minProp, cerrado}] */
  function reporteSemanal(o) {
    var t = 'Control comercial · ' + (o.negocio || 'Mi negocio') + '\n' +
      'Semana del ' + corta(o.lunes) + ' al ' + corta(addDays(o.lunes, 6)) + '\n' +
      'Mes: cerrado ' + dinero(o.cerrado, o.moneda) + (o.cuota > 0 ? ' de ' + dinero(o.cuota, o.moneda) : '') +
      ' · pronóstico esperado ' + dinero(o.esperado, o.moneda) + '\n';
    o.filas.forEach(function (r) {
      t += '• ' + r.nombre + ': ' + r.contactos + ' contactos, ' + r.propuestas + ' propuestas' +
        (r.minCont > 0 ? ' (mínimo ' + Math.ceil(r.minCont - 1e-9) + ' y ' + Math.ceil(r.minProp - 1e-9) + ')' : ' (sin cuota)') +
        ' · cerró ' + dinero(r.cerrado, o.moneda) + '\n';
    });
    if (o.estancadas || o.vencidas) t += '\nAlertas: ' + (o.estancadas || 0) + ' estancadas, ' + (o.vencidas || 0) + ' con acción vencida';
    if (o.compromisos) t += '\n\nCompromisos:\n' + o.compromisos;
    return t;
  }

  /* Mensaje del dueño a un vendedor con lo que le falta hoy. */
  function mensajeVendedor(o) {
    var fc = Math.max(0, Math.ceil(o.minCont - o.contactos - 1e-9)), fp = Math.max(0, Math.ceil(o.minProp - o.propuestas - 1e-9));
    var t = 'Hola ' + o.nombre + ', ';
    if (fc === 0 && fp === 0) return t + 'vas al día con tu actividad de la semana. Gracias.';
    t += 'para llegar al mínimo de la semana te faltan ';
    var p = []; if (fc) p.push(fc + ' contacto' + (fc > 1 ? 's' : '')); if (fp) p.push(fp + ' propuesta' + (fp > 1 ? 's' : ''));
    t += p.join(' y ') + '.';
    if (o.vencidas) t += ' Además tienes ' + o.vencidas + (o.vencidas > 1 ? ' acciones vencidas' : ' acción vencida') + ' en tu pipeline.';
    return t;
  }

  /* ───────── Calendario (.ics) ───────── */
  var escIcs = function (s) { return String(s == null ? '' : s).replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\r?\n/g, '\\n'); };
  function fold(line) {            // RFC 5545: líneas de hasta 75 octetos; la continuación empieza con un espacio
    var enc = new TextEncoder(), dec = new TextDecoder(), bytes = enc.encode(line);
    if (bytes.length <= 75) return line;
    var out = [], i = 0, lim = 75;
    while (i < bytes.length) {
      var end = Math.min(i + lim, bytes.length);
      while (end < bytes.length && (bytes[end] & 0xC0) === 0x80) end--;   // no cortar un carácter UTF-8 a la mitad
      out.push(dec.decode(bytes.slice(i, end))); i = end; lim = 74;
    }
    return out.join('\r\n ');
  }
  var ymdhm = function (f, hora) { return f.replace(/-/g, '') + 'T' + hora.replace(':', '') + '00'; };

  /* evs = [{uid, titulo, descripcion, fecha, hora, minutos, semanal}]; hora local de `tz`, sin VTIMEZONE:
     los clientes de calendario la interpretan en su zona (suficiente para México sin horario de verano). */
  function ics(evs, tz) {
    var L = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//SYNKA//Sistema 30 Dias//ES', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH'];
    evs.forEach(function (e) {
      var fin = (function (m) { var p = e.hora.split(':').map(Number), t = p[0] * 60 + p[1] + (m || 20); return pad(Math.floor(t / 60) % 24) + ':' + pad(t % 60); })(e.minutos);
      L.push('BEGIN:VEVENT', 'UID:' + e.uid + '@synka.mx', 'DTSTAMP:' + (e.stamp || '20260101T000000Z'),
        'DTSTART;TZID=' + (tz || 'America/Mexico_City') + ':' + ymdhm(e.fecha, e.hora),
        'DTEND;TZID=' + (tz || 'America/Mexico_City') + ':' + ymdhm(e.fecha, fin),
        'SUMMARY:' + escIcs(e.titulo));
      if (e.descripcion) L.push('DESCRIPTION:' + escIcs(e.descripcion));
      if (e.semanal) L.push('RRULE:FREQ=WEEKLY');
      L.push('BEGIN:VALARM', 'ACTION:DISPLAY', 'DESCRIPTION:' + escIcs(e.titulo), 'TRIGGER:-PT15M', 'END:VALARM', 'END:VEVENT');
    });
    L.push('END:VCALENDAR');
    return L.map(fold).join('\r\n') + '\r\n';
  }

  /* Próxima fecha, desde `desde` (inclusive), que cae en el día de la semana 0 = lunes … 4 = viernes. */
  function proximoDia(desde, dow) {
    var f = desde; for (var i = 0; i < 7; i++) { if ((fromIso(f).getDay() + 6) % 7 === dow) return f; f = addDays(f, 1); }
    return desde;
  }

  var api = { diasHabiles: diasHabiles, fraccionSemana: fraccionSemana, minimosMes: minimosMes, minimosSemana: minimosSemana,
    avanceEsperado: avanceEsperado, semaforo: semaforo, pronostico: pronostico, waLink: waLink, reporteSemanal: reporteSemanal,
    mensajeVendedor: mensajeVendedor, ics: ics, proximoDia: proximoDia, mondayOf: mondayOf, addDays: addDays };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.SynkaCalc = api;
})(typeof window !== 'undefined' ? window : this);
