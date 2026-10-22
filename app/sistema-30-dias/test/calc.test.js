'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const C = require('../js/calc.js');

const near = (a, b, e = 1e-9) => assert.ok(Math.abs(a - b) < e, a + ' ≠ ' + b);

test('octubre 2026 tiene 22 días hábiles; ausencias y festivos se descuentan', () => {
  assert.equal(C.diasHabiles('2026-10').length, 22);
  assert.equal(C.diasHabiles('2026-10', ['2026-10-06', '2026-10-07']).length, 20);
  assert.equal(C.diasHabiles('2026-10', ['2026-10-10']).length, 22, 'un sábado no resta');
});

test('las fracciones de las semanas que tocan el mes suman 1 (no mes ÷ 4)', () => {
  const lunes = ['2026-09-28', '2026-10-05', '2026-10-12', '2026-10-19', '2026-10-26'];
  near(C.fraccionSemana('2026-09-28', '2026-10'), 2 / 22);
  near(C.fraccionSemana('2026-10-05', '2026-10'), 5 / 22);
  near(C.fraccionSemana('2026-10-26', '2026-10'), 5 / 22);
  near(lunes.reduce((s, l) => s + C.fraccionSemana(l, '2026-10'), 0), 1);
});

test('una semana con ausencia pide menos; el resto del mes pide más', () => {
  const aus = ['2026-10-12', '2026-10-13', '2026-10-14', '2026-10-15', '2026-10-16'];
  assert.equal(C.fraccionSemana('2026-10-12', '2026-10', aus), 0);
  near(C.fraccionSemana('2026-10-05', '2026-10', aus), 5 / 17);
});

test('actividad mínima: cuota ÷ ticket ÷ tasa de cierre ÷ tasa de propuesta', () => {
  const m = C.minimosMes(66000, 22000, 25, 30);
  near(m.ventas, 3); near(m.prop, 12); near(m.cont, 40);
  const s = C.minimosSemana(66000, 22000, 25, 30, '2026-10-05', '2026-10');
  near(s.cont, 40 * 5 / 22); near(s.cuota, 66000 * 5 / 22);
});

test('sin ticket no hay mínimo calculable y no se rompe', () => {
  const m = C.minimosMes(50000, 0, 25, 30);
  assert.deepEqual([m.ventas, m.prop, m.cont], [0, 0, 0]);
  const z = C.minimosMes(50000, 1000, 0, 0);   // tasas en 0 no dividen entre cero
  assert.ok(Number.isFinite(z.cont));
});

test('avance esperado cuenta días hábiles transcurridos de esa semana', () => {
  near(C.avanceEsperado('2026-10-05', '2026-10-07', '2026-10'), 3 / 5);
  near(C.avanceEsperado('2026-10-05', '2026-10-07', '2026-10', ['2026-10-06']), 2 / 4);
  near(C.avanceEsperado('2026-10-05', '2026-10-31', '2026-10'), 1);
  assert.equal(C.avanceEsperado('2026-10-12', '2026-10-07', '2026-10'), 0);
});

test('semáforo', () => {
  assert.equal(C.semaforo(0.95, true), 'g');
  assert.equal(C.semaforo(0.9, true), 'g');
  assert.equal(C.semaforo(0.75, true), 'y');
  assert.equal(C.semaforo(0.2, true), 'r');
  assert.equal(C.semaforo(1, false), 'n');
});

test('pronóstico: solo cuentan las abiertas con cierre en el mes', () => {
  const E = { a: 20, b: 60, c: 90 };
  const opps = [
    { estado: 'ganada', fReal: '2026-10-03', valor: 1000 },
    { estado: 'ganada', fReal: '2026-09-30', valor: 5000 },           // otro mes
    { estado: 'perdida', fReal: '2026-10-04', valor: 9999 },
    { estado: '', etapa: 'a', valor: 1000, fcierre: '2026-10-20' },
    { estado: '', etapa: 'b', valor: 2000, fcierre: '2026-10-25' },
    { estado: '', etapa: 'c', valor: 3000, fcierre: '2026-11-02' },   // fuera del mes
    { estado: '', etapa: 'c', valor: 4000, fcierre: '' },             // sin fecha
    { estado: '', etapa: 'a', valor: 500, fcierre: '2020-01-01' }     // vencida
  ];
  const p = C.pronostico(opps, E, '2026-10', '2026-10-22');
  assert.equal(p.cerrado, 1000);
  near(p.esperado, 1000 + 1000 * .2 + 2000 * .6);
  near(p.conservador, 1000 + 2000 * .6);
  assert.equal(p.optimista, 1000 + 1000 + 2000);
  assert.equal(p.sinFecha, 1);
  assert.equal(p.cierreVencido, 2, 'la del 20 de oct y la de 2020 ya vencieron al 22');
});

test('wa.me limpia el número y codifica el texto', () => {
  const u = C.waLink('+52 55 2899 4084', 'Hola, ¿qué tal?\nOk');
  assert.ok(u.startsWith('https://wa.me/525528994084?text='));
  assert.equal(decodeURIComponent(u.split('text=')[1]), 'Hola, ¿qué tal?\nOk');
});

test('reporte semanal incluye actividad, mínimos y compromisos', () => {
  const t = C.reporteSemanal({ negocio: 'Distribuidora', lunes: '2026-10-05', cerrado: 40000, cuota: 135000, esperado: 90000, moneda: 'MXN',
    filas: [{ nombre: 'Ana', contactos: 14, propuestas: 5, minCont: 9.09, minProp: 2.7, cerrado: 22000 }, { nombre: 'Luis', contactos: 0, propuestas: 0, minCont: 0, minProp: 0, cerrado: 0 }],
    estancadas: 2, vencidas: 1, compromisos: 'Ana: cerrar Industrias el jueves' });
  assert.match(t, /Semana del 5 oct al 11 oct/);
  assert.match(t, /Ana: 14 contactos, 5 propuestas \(mínimo 10 y 3\)/);
  assert.match(t, /Luis: 0 contactos, 0 propuestas \(sin cuota\)/);
  assert.match(t, /Alertas: 2 estancadas, 1 con acción vencida/);
  assert.match(t, /Compromisos:\nAna: cerrar Industrias/);
});

test('mensaje al vendedor dice cuánto falta o confirma que va al día', () => {
  assert.match(C.mensajeVendedor({ nombre: 'Ana', minCont: 10, minProp: 3, contactos: 7, propuestas: 3, vencidas: 0 }), /te faltan 3 contactos\./);
  assert.match(C.mensajeVendedor({ nombre: 'Ana', minCont: 10, minProp: 3, contactos: 7, propuestas: 1, vencidas: 2 }), /3 contactos y 2 propuestas.*2 acciones vencidas/);
  assert.match(C.mensajeVendedor({ nombre: 'Ana', minCont: 10, minProp: 3, contactos: 10, propuestas: 3 }), /vas al día/);
});

test('.ics: CRLF, recurrencia semanal, escape y plegado a 75 octetos sin partir UTF-8', () => {
  const largo = 'Compromisos: ' + 'acción ñandú, '.repeat(20);
  const out = C.ics([{ uid: 'rev-1', titulo: 'Revisión semanal; ventas', descripcion: largo, fecha: '2026-10-12', hora: '09:00', minutos: 20, semanal: true }]);
  assert.ok(out.startsWith('BEGIN:VCALENDAR\r\n') && out.endsWith('END:VCALENDAR\r\n'));
  assert.ok(!/[^\r]\n/.test(out), 'solo CRLF');
  assert.match(out, /RRULE:FREQ=WEEKLY/);
  assert.match(out, /DTSTART;TZID=America\/Mexico_City:20261012T090000/);
  assert.match(out, /DTEND;TZID=America\/Mexico_City:20261012T092000/);
  assert.match(out, /SUMMARY:Revisión semanal\\; ventas/);
  const lineas = out.split('\r\n');
  lineas.forEach(l => assert.ok(Buffer.byteLength(l) <= 75, 'línea larga: ' + l));
  const desplegado = out.replace(/\r\n /g, '');
  assert.ok(desplegado.includes('acción ñandú\\, acción ñandú\\,'), 'el contenido sobrevive al plegado');
  assert.ok(!desplegado.includes('�'), 'no se partió ningún carácter');
});

test('.ics: la hora de fin cruza la hora en punto', () => {
  const out = C.ics([{ uid: 'x', titulo: 't', fecha: '2026-10-12', hora: '09:50', minutos: 20 }]);
  assert.match(out, /DTEND;TZID=America\/Mexico_City:20261012T101000/);
  assert.ok(!/RRULE/.test(out));
});

test('próximo día de revisión', () => {
  assert.equal(C.proximoDia('2026-10-07', 0), '2026-10-12');
  assert.equal(C.proximoDia('2026-10-07', 2), '2026-10-07');
  assert.equal(C.proximoDia('2026-10-07', 1), '2026-10-13');
});
