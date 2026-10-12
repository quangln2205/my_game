from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class ResearchRequest(BaseModel):
    question: str = Field(min_length=8, max_length=500)


class EvidenceMetadata(BaseModel):
    published_at: date
    market: str | None = None
    game_version: str | None = None
    audience_scope: str | None = None
    metric_definition: str | None = None


class Evidence(BaseModel):
    id: str
    title: str
    excerpt: str
    source_name: str
    source_url: HttpUrl
    source_type: Literal['report', 'store_review', 'survey', 'telemetry', 'community']
    metadata: EvidenceMetadata
    claim_key: str
    stance: Literal['positive', 'negative', 'neutral']
    reliability_score: float = Field(ge=0, le=1)


class WarningItem(BaseModel):
    code: Literal['scope_mismatch', 'direct_conflict', 'insufficient_evidence', 'low_reliability']
    message: str
    evidence_ids: list[str] = []


class Brief(BaseModel):
    conclusion: str
    confidence: Literal['high', 'medium', 'low', 'insufficient']
    review_status: Literal['needs_human_review', 'reviewed'] = 'needs_human_review'
    missing_data: list[str]
    warnings: list[WarningItem]
    next_steps: list[str]


class ResearchResponse(BaseModel):
    session_id: UUID | str
    question: str
    brief: Brief
    evidence: list[Evidence]
    generated_at: datetime
