create table if not exists public.card_feedback (
  id bigint generated always as identity primary key,
  card_id text not null check (char_length(trim(card_id)) between 1 and 300),
  button_type text not null check (button_type in ('useful', 'favorite', 'ignore')),
  clicked_at timestamptz not null default now(),
  origin text not null default 'website' check (origin = 'website')
);

create index if not exists card_feedback_card_id_idx
  on public.card_feedback (card_id, clicked_at desc);

alter table public.card_feedback enable row level security;

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
