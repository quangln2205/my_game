import os
from pathlib import Path
from uuid import UUID, uuid4

from dotenv import load_dotenv

from .schemas import Evidence
from .seed import DEMO_EVIDENCE


class ResearchRepository:
    """Evidence/RAG adapter with a safe in-memory fallback for local demos."""

    def __init__(self) -> None:
        load_dotenv(Path(__file__).resolve().parents[2] / '.env')
        self._sessions: dict[str, str] = {}
        self.client = None
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        if url and key:
            try:
                from supabase import create_client
                self.client = create_client(url, key)
            except ImportError as error:
                raise RuntimeError('SUPABASE_URL is set but the supabase package is not installed.') from error

    def create_session(self, question: str) -> str:
        session_id = str(uuid4())
        if self.client:
            response = self.client.table('research_sessions').insert({'question': question, 'status': 'analysed'}).execute()
            return response.data[0]['id']
        self._sessions[session_id] = question
        return session_id

    def retrieve(self, question: str, limit: int = 6) -> list[Evidence]:
        pool = self._supabase_evidence() if self.client else DEMO_EVIDENCE
        tokens = {word.strip('?,.!').lower() for word in question.split() if len(word) > 2}
        scored: list[tuple[int, Evidence]] = []
        for item in pool:
            haystack = ' '.join([item.title, item.excerpt, item.claim_key, item.metadata.market or '', item.metadata.game_version or '', item.metadata.metric_definition or '']).lower()
            score = sum(1 for token in tokens if token in haystack)
            if score:
                scored.append((score, item))
        return [item for _, item in sorted(scored, key=lambda pair: (-pair[0], -pair[1].reliability_score))[:limit]]

    def store_brief(self, session_id: str, brief, evidence: list[Evidence]) -> None:
        """Persist only when the session is a real Supabase UUID; local MVP remains zero-config."""
        if not self.client:
            return
        brief_id = self.client.table('research_briefs').insert({
            'session_id': session_id,
            'conclusion': brief.conclusion,
            'confidence': brief.confidence,
            'review_status': brief.review_status,
            'missing_data': brief.missing_data,
            'warnings': [warning.model_dump() for warning in brief.warnings],
            'next_steps': brief.next_steps,
        }).execute().data[0]['id']
        links = []
        for item in evidence:
            try:
                UUID(item.id)
            except ValueError:
                continue
            role = 'supporting' if item.stance == 'positive' else 'contradicting' if item.stance == 'negative' else 'context'
            links.append({'brief_id': brief_id, 'evidence_id': item.id, 'role': role})
        if links:
            self.client.table('brief_evidence').insert(links).execute()

    def _supabase_evidence(self) -> list[Evidence]:
        rows = self.client.table('evidence_items').select('*').limit(100).execute().data
        return [Evidence(
            id=row['id'], title=row['title'], excerpt=row['excerpt'], source_name=row['source_name'],
            source_url=row['source_url'], source_type=row['source_type'], claim_key=row['claim_key'],
            stance=row['stance'], reliability_score=float(row['reliability_score']),
            metadata={'published_at': row['published_at'], 'market': row.get('market'), 'game_version': row.get('game_version'),
                      'audience_scope': row.get('audience_scope'), 'metric_definition': row.get('metric_definition')},
        ) for row in rows]
