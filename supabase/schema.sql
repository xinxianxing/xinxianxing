-- 信先行 operational data schema.
-- Run this once in Supabase SQL Editor. All application writes use the
-- server-side service role key from GitHub Actions or local .env only. The
-- only browser-facing exception is card_feedback, which permits anonymous
-- inserts through a tightly scoped RLS policy.

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

create table if not exists public.card_feedback (
  id bigint generated always as identity primary key,
  card_id text not null check (char_length(trim(card_id)) between 1 and 300),
  button_type text not null check (button_type in ('useful', 'favorite', 'ignore')),
  clicked_at timestamptz not null default now(),
  origin text not null default 'website' check (origin = 'website')
);

create index if not exists action_cards_run_date_idx
  on public.action_cards (run_date desc, language);
create index if not exists channel_deliveries_status_idx
  on public.channel_deliveries (run_date desc, status);
create index if not exists card_feedback_card_id_idx
  on public.card_feedback (card_id, clicked_at desc);

alter table public.pipeline_runs enable row level security;
alter table public.action_cards enable row level security;
alter table public.channel_deliveries enable row level security;
alter table public.card_feedback enable row level security;

-- Pipeline, card, and delivery tables have no public policies. The public site
-- may only submit one of the three feedback actions below; it cannot SELECT,
-- UPDATE, or DELETE any table. Use the service role key only from trusted
-- automation, never in the static site or browser code.
do $$
begin
  if not exists (
    select 1
    from pg_policies
    where schemaname = 'public'
      and tablename = 'card_feedback'
      and policyname = 'Website visitors can submit card feedback'
  ) then
    create policy "Website visitors can submit card feedback"
      on public.card_feedback
      for insert
      to anon
      with check (
        button_type in ('useful', 'favorite', 'ignore')
        and char_length(trim(card_id)) between 1 and 300
        and origin = 'website'
      );
  end if;
end $$;
