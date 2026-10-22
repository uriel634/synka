-- SYNKA · Sistema Comercial 30 Días · esquema Postgres (Supabase)
-- Un workspace por cliente. Roles: owner (dueño) y seller (vendedor).
-- Seguridad por fila: el vendedor solo ve y edita lo suyo; el dueño ve todo.
-- Si el workspace no está activo (prueba vencida o sin pago) queda en solo lectura.

create extension if not exists pgcrypto;

-- ───────── núcleo ─────────
create table workspaces (
  id          uuid primary key default gen_random_uuid(),
  nombre      text not null,
  moneda      text not null default 'MXN' check (moneda in ('MXN','USD')),
  inicio_plan date not null default current_date,
  dia_rev     smallint not null default 0 check (dia_rev between 0 and 4), -- 0 = lunes
  hora_rev    time not null default '09:00',
  t_cierre    numeric not null default 25 check (t_cierre between 1 and 100),
  t_prop      numeric not null default 30 check (t_prop between 1 and 100),
  ticket      numeric not null default 0,
  estado      text not null default 'trial' check (estado in ('trial','active','readonly')),
  vence       date,
  creado      timestamptz not null default now()
);

create table members (
  id        uuid primary key default gen_random_uuid(),
  ws_id     uuid not null references workspaces on delete cascade,
  user_id   uuid references auth.users on delete set null,  -- null hasta que acepta la invitación
  email     text not null,
  nombre    text not null,
  rol       text not null check (rol in ('owner','seller')),
  activo    boolean not null default true,
  unique (ws_id, email)
);
create index on members (user_id);

-- ───────── proceso ─────────
create table stages (
  id     uuid primary key default gen_random_uuid(),
  ws_id  uuid not null references workspaces on delete cascade,
  orden  smallint not null,
  nombre text not null,
  prob   numeric not null check (prob between 0 and 100),
  dias   smallint not null default 7,
  resp   text not null default '',
  unique (ws_id, orden) deferrable initially deferred
);

create table criteria (
  id       uuid primary key default gen_random_uuid(),
  stage_id uuid not null references stages on delete cascade,
  orden    smallint not null,
  texto    text not null
);

-- ───────── pipeline ─────────
create table opportunities (
  id          uuid primary key default gen_random_uuid(),
  ws_id       uuid not null references workspaces on delete cascade,
  member_id   uuid references members on delete set null,   -- vendedor responsable
  empresa     text not null,
  contacto    text not null default '',
  valor       numeric not null default 0 check (valor >= 0),
  stage_id    uuid references stages on delete restrict,    -- no se puede borrar una etapa en uso
  stage_desde date not null default current_date,
  f_cierre    date,
  prox        text not null default '',
  f_prox      date,
  estado      text not null default 'abierta' check (estado in ('abierta','ganada','perdida')),
  f_real      date,
  motivo      text not null default '',
  creado      timestamptz not null default now()
);
create index on opportunities (ws_id, estado);
create index on opportunities (member_id, estado);

create table opportunity_criteria (   -- criterios marcados en la etapa actual
  opp_id      uuid not null references opportunities on delete cascade,
  criterion_id uuid not null references criteria on delete cascade,
  primary key (opp_id, criterion_id)
);

-- Historial: permite medir conversión y tiempo real por etapa.
create table opportunity_events (
  id        bigint generated always as identity primary key,
  opp_id    uuid not null references opportunities on delete cascade,
  ws_id     uuid not null references workspaces on delete cascade,
  member_id uuid references members on delete set null,     -- quién lo hizo
  tipo      text not null check (tipo in ('creada','avance','retroceso','ganada','perdida','reabierta')),
  de_stage  uuid references stages on delete set null,
  a_stage   uuid references stages on delete set null,
  valor     numeric,
  cuando    timestamptz not null default now()
);
create index on opportunity_events (ws_id, cuando);

-- ───────── control ─────────
create table daily_activity (         -- registro diario; la semana se suma
  ws_id      uuid not null references workspaces on delete cascade,
  member_id  uuid not null references members on delete cascade,
  dia        date not null,
  contactos  int not null default 0 check (contactos >= 0),
  propuestas int not null default 0 check (propuestas >= 0),
  ausente    boolean not null default false,   -- descuenta el día del ritmo esperado
  primary key (member_id, dia)
);

create table monthly_quotas (         -- una fila por mes: el pasado no se reescribe
  member_id uuid not null references members on delete cascade,
  mes       date not null check (mes = date_trunc('month', mes)::date),
  cuota     numeric not null default 0 check (cuota >= 0),
  ws_id     uuid not null references workspaces on delete cascade,
  primary key (member_id, mes)
);

create table meetings (
  ws_id      uuid not null references workspaces on delete cascade,
  semana     date not null check (extract(isodow from semana) = 1),
  items      jsonb not null default '{}',
  compromisos text not null default '',
  cerrada    boolean not null default false,
  primary key (ws_id, semana)
);

-- Tareas del plan de 30 días que no se pueden deducir de los datos.
create table plan_flags (
  ws_id uuid not null references workspaces on delete cascade,
  clave text not null,
  hecho timestamptz not null default now(),
  primary key (ws_id, clave)
);

-- ───────── helpers de seguridad ─────────
create function my_member(w uuid) returns members
language sql stable security definer set search_path = public as $$
  select * from members where ws_id = w and user_id = auth.uid() and activo limit 1
$$;

create function is_member(w uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from members where ws_id = w and user_id = auth.uid() and activo)
$$;

create function is_owner(w uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from members where ws_id = w and user_id = auth.uid() and activo and rol = 'owner')
$$;

create function ws_writable(w uuid) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from workspaces
                 where id = w and estado in ('trial','active') and (vence is null or vence >= current_date))
$$;

-- ───────── RLS ─────────
alter table workspaces          enable row level security;
alter table members             enable row level security;
alter table stages              enable row level security;
alter table criteria            enable row level security;
alter table opportunities       enable row level security;
alter table opportunity_criteria enable row level security;
alter table opportunity_events  enable row level security;
alter table daily_activity      enable row level security;
alter table monthly_quotas      enable row level security;
alter table meetings            enable row level security;
alter table plan_flags          enable row level security;

-- workspace: lo ve cualquier miembro; solo el dueño lo edita. El estado/vence solo lo cambia el
-- servidor (webhook de pago con service_role), nunca el cliente.
create policy ws_sel on workspaces for select using (is_member(id));
create policy ws_upd on workspaces for update using (is_owner(id) and ws_writable(id))
  with check (is_owner(id) and ws_writable(id));
revoke update (estado, vence) on workspaces from authenticated;

-- miembros: todos se ven entre sí (para asignar); solo el dueño gestiona.
create policy mb_sel on members for select using (is_member(ws_id));
create policy mb_all on members for all using (is_owner(ws_id) and ws_writable(ws_id))
  with check (is_owner(ws_id) and ws_writable(ws_id));

-- proceso: lo lee todo el equipo, lo edita el dueño.
create policy st_sel on stages for select using (is_member(ws_id));
create policy st_all on stages for all using (is_owner(ws_id) and ws_writable(ws_id))
  with check (is_owner(ws_id) and ws_writable(ws_id));
create policy cr_sel on criteria for select
  using (exists (select 1 from stages s where s.id = stage_id and is_member(s.ws_id)));
create policy cr_all on criteria for all
  using (exists (select 1 from stages s where s.id = stage_id and is_owner(s.ws_id) and ws_writable(s.ws_id)))
  with check (exists (select 1 from stages s where s.id = stage_id and is_owner(s.ws_id) and ws_writable(s.ws_id)));

-- oportunidades: el dueño ve todas; el vendedor solo las suyas.
create policy op_sel on opportunities for select
  using (is_owner(ws_id) or member_id = (my_member(ws_id)).id);
create policy op_ins on opportunities for insert
  with check (ws_writable(ws_id) and (is_owner(ws_id) or member_id = (my_member(ws_id)).id));
create policy op_upd on opportunities for update
  using (ws_writable(ws_id) and (is_owner(ws_id) or member_id = (my_member(ws_id)).id))
  with check (ws_writable(ws_id) and (is_owner(ws_id) or member_id = (my_member(ws_id)).id));   -- el vendedor no se las pasa a otro
create policy op_del on opportunities for delete using (is_owner(ws_id) and ws_writable(ws_id));

create policy oc_all on opportunity_criteria for all
  using (exists (select 1 from opportunities o where o.id = opp_id and ws_writable(o.ws_id)
         and (is_owner(o.ws_id) or o.member_id = (my_member(o.ws_id)).id)))
  with check (exists (select 1 from opportunities o where o.id = opp_id and ws_writable(o.ws_id)
         and (is_owner(o.ws_id) or o.member_id = (my_member(o.ws_id)).id)));

-- historial: se lee con la misma regla; se agrega pero no se edita ni se borra.
create policy ev_sel on opportunity_events for select
  using (is_owner(ws_id) or exists (select 1 from opportunities o where o.id = opp_id
         and o.member_id = (my_member(o.ws_id)).id));
create policy ev_ins on opportunity_events for insert
  with check (ws_writable(ws_id) and member_id = (my_member(ws_id)).id);

-- actividad: cada quien captura la suya; el dueño ve y corrige todas.
create policy ac_sel on daily_activity for select
  using (is_owner(ws_id) or member_id = (my_member(ws_id)).id);
create policy ac_all on daily_activity for all
  using (ws_writable(ws_id) and (is_owner(ws_id) or member_id = (my_member(ws_id)).id))
  with check (ws_writable(ws_id) and (is_owner(ws_id) or member_id = (my_member(ws_id)).id));

-- cuotas: las fija el dueño; el vendedor lee la suya.
create policy qt_sel on monthly_quotas for select
  using (is_owner(ws_id) or member_id = (my_member(ws_id)).id);
create policy qt_all on monthly_quotas for all
  using (is_owner(ws_id) and ws_writable(ws_id)) with check (is_owner(ws_id) and ws_writable(ws_id));

-- reuniones y tareas del plan: equipo lee, dueño escribe.
create policy mt_sel on meetings for select using (is_member(ws_id));
create policy mt_all on meetings for all using (is_owner(ws_id) and ws_writable(ws_id))
  with check (is_owner(ws_id) and ws_writable(ws_id));
create policy pf_sel on plan_flags for select using (is_member(ws_id));
create policy pf_all on plan_flags for all using (is_owner(ws_id) and ws_writable(ws_id))
  with check (is_owner(ws_id) and ws_writable(ws_id));

-- ───────── alta de cliente ─────────
-- Crea workspace + dueño + etapas de la plantilla en una sola llamada (rpc).
create function crear_workspace(p_nombre text, p_nombre_dueno text, p_plantilla text)
returns uuid language plpgsql security definer set search_path = public as $$
declare w uuid; s uuid; e jsonb; c text; i int := 0; j int;
  tpl jsonb := case p_plantilla
   when 'serv' then '[["Contacto inicial",10,5,["Sé quién decide y quién paga","Tengo su contacto directo"]],["Diagnóstico realizado",25,7,["Entendí el problema y su impacto","Tengo claro el alcance aproximado"]],["Propuesta enviada",45,7,["Envié alcance, tiempo y precio por escrito","El decisor la revisó"]],["Negociación",70,10,["Resolví dudas y objeciones","Acordamos forma de pago"]],["Cierre por firmar",90,5,["Envié el contrato o la aceptación","Quedó definida la fecha de arranque"]]]'
   else '[["Prospecto identificado",10,5,["Sé quién decide la compra","Tengo su contacto directo"]],["Contactado",20,7,["El cliente respondió","Quedó agendada una conversación"]],["Necesidad confirmada",40,10,["Conozco qué necesita y en qué volumen","Sé su rango de presupuesto","Sé cuándo necesita resolverlo"]],["Propuesta enviada",60,7,["Envié precio y condiciones por escrito","El decisor la recibió","Acordamos fecha de seguimiento"]],["Negociación",80,10,["Se resolvieron las objeciones","Acordamos condiciones de pago"]]]' end::jsonb;
begin
  if auth.uid() is null then raise exception 'no autenticado'; end if;
  insert into workspaces (nombre, vence) values (p_nombre, current_date + 14) returning id into w;
  insert into members (ws_id, user_id, email, nombre, rol)
    values (w, auth.uid(), (select email from auth.users where id = auth.uid()), p_nombre_dueno, 'owner');
  for e in select * from jsonb_array_elements(tpl) loop
    i := i + 1;
    insert into stages (ws_id, orden, nombre, prob, dias, resp)
      values (w, i, e->>0, (e->>1)::numeric, (e->>2)::smallint, p_nombre_dueno) returning id into s;
    j := 0;
    for c in select jsonb_array_elements_text(e->3) loop
      j := j + 1; insert into criteria (stage_id, orden, texto) values (s, j, c);
    end loop;
  end loop;
  return w;
end $$;

-- Un vendedor invitado entra al registrarse con el mismo correo.
create function aceptar_invitaciones() returns int
language sql security definer set search_path = public as $$
  with u as (update members set user_id = auth.uid()
             where user_id is null and lower(email) = lower((select email from auth.users where id = auth.uid()))
             returning 1) select count(*)::int from u
$$;
