-- Session Intelligence for Teams waitlist (teams.amvo.store). Run once in the IronTrack Supabase project's SQL editor.
-- Written by api/waitlist.js with the secret (service role) key; browsers have no access.

create table if not exists public.teams_waitlist (
  id          uuid primary key default gen_random_uuid(),
  email       text not null unique check (char_length(email) <= 254),
  name        text check (char_length(name) <= 120),
  company     text check (char_length(company) <= 120),
  team_size   text not null check (team_size in ('1', '2–5', '6–15', '16–50', '50+')),
  os          text[] not null default '{}',
  agents      text[] not null default '{}',
  wanted      text[] not null default '{}',  -- "Which of these would make you pay?"
  pain        text check (char_length(pain) <= 500),
  consent     boolean not null check (consent),
  source      text check (char_length(source) <= 300),
  user_agent  text check (char_length(user_agent) <= 300),
  created_at  timestamptz not null default now()
);

-- If the table was created before the wanted column existed:
alter table public.teams_waitlist add column if not exists wanted text[] not null default '{}';

-- RLS on with no policies: the anon and authenticated roles can't read or write.
-- The service role (used only by the Vercel function) bypasses RLS.
alter table public.teams_waitlist enable row level security;
revoke all on public.teams_waitlist from anon, authenticated;

comment on table public.teams_waitlist is 'Session Intelligence for Teams waitlist (teams.amvo.store). Not IronTrack data.';
