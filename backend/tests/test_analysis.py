from app.analysis import build_brief
from app.seed import DEMO_EVIDENCE


def test_empty_evidence_is_not_a_conclusion():
    brief = build_brief([])
    assert brief.confidence == 'insufficient'
    assert 'Chưa thể kết luận' in brief.conclusion


def test_scope_difference_is_explained():
    brief = build_brief([DEMO_EVIDENCE[1], DEMO_EVIDENCE[2]])
    assert brief.confidence == 'low'
    assert any(w.code == 'scope_mismatch' for w in brief.warnings)


def test_low_reliability_source_is_flagged():
    brief = build_brief([DEMO_EVIDENCE[3]])
    assert any(w.code == 'low_reliability' for w in brief.warnings)


def test_consistent_market_signal_is_actionable_but_not_causal():
    brief = build_brief([DEMO_EVIDENCE[0], DEMO_EVIDENCE[0]])
    assert brief.confidence == 'medium'
    assert 'không phải kết luận nhân quả' in brief.conclusion


def test_same_scope_opposing_evidence_is_insufficient():
    positive = DEMO_EVIDENCE[2].model_copy(update={'stance': 'positive'})
    negative = DEMO_EVIDENCE[2].model_copy(update={'id': 'contradiction', 'stance': 'negative'})
    brief = build_brief([positive, negative])
    assert brief.confidence == 'insufficient'
    assert any(w.code == 'direct_conflict' for w in brief.warnings)
