# Sistema Comercial 30 Días — versión multiusuario

Plan de producto y arquitectura para convertir el prototipo de un solo archivo
(`localStorage`) en un producto con dueño + vendedores.

## Decisiones

| Tema | Decisión |
|---|---|
| Usuarios | Dueño y vendedores, cada uno con su sesión |
| Entrega | Producto de pago con acceso, en subdominio aparte (`app.synka.mx`) para no mezclarlo con el sitio estático |
| Backend | Supabase: Postgres, acceso por enlace al correo y seguridad por fila |
| Frontend | JS puro sin build, como el resto del repo; fuentes de `assets/fonts/` |
| Prioridad | WhatsApp y calendario |

Pendiente de decidir: pasarela de cobro (Mercado Pago o Stripe).

## Versión 1

1. Cuentas, roles e invitación de vendedores (`db/schema.sql`).
2. Sincronización con caché local para trabajar con mala señal.
3. Registro diario de contactos y propuestas por vendedor.
4. Reporte semanal y mensaje al vendedor por enlace `wa.me`.
5. Reunión semanal y próximas acciones como `.ics`.

Versión 2: cobro automático por webhook y recordatorios con la API de WhatsApp Business.

## Cambios sobre el prototipo

- Cuota semanal por días hábiles del mes y ausencias, no mes ÷ 4.
- Cuotas por mes (`monthly_quotas`): cambiar una cuota no reescribe el pasado.
- Historial de etapas (`opportunity_events`) para medir conversión y tiempo real.
- Un cierre anterior ya no se guarda en la última etapa; se registra sin etapa de embudo.
- El número de WhatsApp sale de `js/config.js` del sitio (el prototipo usaba otro).

## Seguridad

- El vendedor solo ve y edita sus oportunidades, actividad y cuota.
- El vendedor no puede reasignar una oportunidad a otro.
- `estado` y `vence` del workspace solo los cambia el servidor, nunca el cliente.
- Con la prueba vencida el workspace queda en solo lectura; no se borra nada.
- El historial de oportunidades solo admite altas.

## Probar el esquema

```bash
psql "$DATABASE_URL" -f app/sistema-30-dias/db/schema.sql
```

Requiere el esquema `auth` de Supabase (`auth.users`, `auth.uid()`).
