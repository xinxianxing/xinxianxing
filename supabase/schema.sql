-- 信先行 operational data schema.
-- Run this once in Supabase SQL Editor. All application writes use the
-- server-side service role key from GitHub Actions or local .env only.

create table if not exists public.pipeline_runs (
  run_date date not null,
  language text not null,
  generated_at timestamptz not null,
  status text not null,
  fetched_count integer not null default 0,
  unique_count integer not null default 0,
  analyzed_count integer not null default 0,
  selected_count integer not null default 0,
  score_threshold numeric,
  source_counts jsonb not null default '{}'::jsonb,
  signal_counts jsonb not null default '{}'::jsonb,
  group_counts jsonb not null default '{}'::jsonb,
  cards jsonb not null default '[]'::jsonb,
  primary key (run_date, language)
);

create table if not exists public.action_cards (
  run_date date not null,
  language text not null,
  card_id text not null,
  signal_type text,
  score numeric,
  source_id text,
  card jsonb not null,
  created_at timestamptz not null default now(),
  primary key (run_date, language, card_id)
);

create table if not exists public.channel_deliveries (
  run_date date not null,
  language text not null,
  channel_id text not null,
  destination_type text not null,
  channel_name text not null,
  item_count integer not null,
  status text not null check (status in ('success', 'failed')),
  error text,
  delivered_at timestamptz not null,
  primary key (run_date, language, channel_id, destination_type)
);

create index if not exists action_cards_run_date_idx
  on public.action_cards (run_date desc, language);
create index if not exists channel_deliveries_status_idx
  on public.channel_deliveries (run_date desc, status);

alter table public.pipeline_runs enable row level security;
alter table public.action_cards enable row level security;
alter table public.channel_deliveries enable row level security;

-- No public policies are created intentionally. Use the service role key only
-- from trusted automation; never embed it in the static site or browser code.
