-- Run in Supabase SQL Editor. Demo sources contain fictional, non-sensitive data.
create extension if not exists pgcrypto;

create table if not exists research_sessions (
  id uuid primary key default gen_random_uuid(),
  question text not null check (char_length(trim(question)) >= 8),
  status text not null default 'draft' check (status in ('draft', 'analysed', 'needs_review')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists research_briefs (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null references research_sessions(id) on delete cascade,
  conclusion text not null,
  confidence text not null check (confidence in ('high', 'medium', 'low', 'insufficient')),
  review_status text not null check (review_status in ('needs_human_review', 'reviewed')),
  missing_data jsonb not null default '[]'::jsonb,
  warnings jsonb not null default '[]'::jsonb,
  next_steps jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists evidence_items (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  excerpt text not null,
  source_name text not null,
  source_url text not null,
  source_type text not null check (source_type in ('report', 'store_review', 'survey', 'telemetry', 'community')),
  published_at date not null,
  market text,
  game_version text,
  audience_scope text,
  metric_definition text,
  claim_key text not null,
  stance text not null check (stance in ('positive', 'negative', 'neutral')),
  reliability_score numeric(3,2) not null check (reliability_score >= 0 and reliability_score <= 1),
  retrieval_tags text[] not null default '{}',
  created_at timestamptz not null default now()
);

create table if not exists brief_evidence (
  brief_id uuid not null references research_briefs(id) on delete cascade,
  evidence_id uuid not null references evidence_items(id) on delete restrict,
  role text not null check (role in ('supporting', 'contradicting', 'context')),
  primary key (brief_id, evidence_id)
);

create index if not exists evidence_items_claim_key_idx on evidence_items(claim_key);
create index if not exists evidence_items_tags_idx on evidence_items using gin(retrieval_tags);

alter table research_sessions enable row level security;
alter table research_briefs enable row level security;
alter table evidence_items enable row level security;
alter table brief_evidence enable row level security;
-- MVP policy: FastAPI uses service-role credentials; browser clients never access these tables directly.
