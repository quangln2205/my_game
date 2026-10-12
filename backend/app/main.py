from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .analysis import build_brief
from .repository import ResearchRepository
from .schemas import ResearchRequest, ResearchResponse

app = FastAPI(title='Gamota Research Brief API', version='0.1.0')
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:3000'], allow_credentials=False, allow_methods=['*'], allow_headers=['*'])
repository = ResearchRepository()


@app.get('/health')
def health() -> dict[str, str]:
    return {'status': 'ok'}


@app.post('/api/research', response_model=ResearchResponse)
def analyse_research_question(payload: ResearchRequest) -> ResearchResponse:
    """Core loop: record question -> retrieve evidence -> flag uncertainty -> human-review brief."""
    session_id = repository.create_session(payload.question)
    evidence = repository.retrieve(payload.question)
    brief = build_brief(evidence)
    repository.store_brief(session_id, brief, evidence)
    return ResearchResponse(session_id=session_id, question=payload.question, brief=brief, evidence=evidence, generated_at=datetime.now(timezone.utc))
