from collections import defaultdict

from .schemas import Brief, Evidence, WarningItem


def _scope(evidence: Evidence) -> tuple[str | None, str | None, str | None]:
    return (evidence.metadata.market, evidence.metadata.game_version, evidence.metadata.metric_definition)


def build_brief(evidence: list[Evidence]) -> Brief:
    if not evidence:
        return Brief(
            conclusion='Chưa thể kết luận: kho bằng chứng hiện chưa có nguồn phù hợp trực tiếp với câu hỏi.',
            confidence='insufficient',
            missing_data=['Ít nhất hai nguồn độc lập cùng phạm vi đo', 'Thị trường, kỳ đo và định nghĩa chỉ số của câu hỏi'],
            warnings=[WarningItem(code='insufficient_evidence', message='Không truy xuất được bằng chứng liên quan; không nên suy diễn từ dữ liệu hiện có.')],
            next_steps=['Làm rõ thị trường, game/phiên bản và chỉ số cần quyết định.', 'Bổ sung nguồn có quyền sử dụng rồi chạy lại phân tích.'],
        )

    warnings: list[WarningItem] = []
    missing: list[str] = []
    grouped: dict[str, list[Evidence]] = defaultdict(list)
    for item in evidence:
        grouped[item.claim_key].append(item)
        if item.reliability_score < 0.5:
            warnings.append(WarningItem(code='low_reliability', message=f'Nguồn {item.source_name} có độ tin cậy thấp; chỉ dùng để nêu giả thuyết.', evidence_ids=[item.id]))

    conflict = False
    scope_mismatch = False
    for items in grouped.values():
        stances = {item.stance for item in items if item.stance != 'neutral'}
        if len(stances) > 1:
            ids = [item.id for item in items]
            if len({_scope(item) for item in items}) > 1:
                scope_mismatch = True
                warnings.append(WarningItem(code='scope_mismatch', message='Các nguồn trái chiều không đo cùng thị trường, phiên bản hoặc định nghĩa chỉ số; đây chưa phải mâu thuẫn trực tiếp.', evidence_ids=ids))
            else:
                conflict = True
                warnings.append(WarningItem(code='direct_conflict', message='Các nguồn cùng phạm vi nhưng đưa tín hiệu trái chiều; chưa thể kết luận.', evidence_ids=ids))

    if len(evidence) < 2:
        missing.append('Nguồn độc lập thứ hai để đối chiếu nhận định chính')
        warnings.append(WarningItem(code='insufficient_evidence', message='Chỉ có một nguồn phù hợp; không đủ để khẳng định nhận định.', evidence_ids=[evidence[0].id]))
    if any(item.metadata.game_version is None for item in evidence):
        missing.append('Phiên bản game cho các bằng chứng liên quan')

    if conflict:
        return Brief(conclusion='Chưa thể kết luận vì các nguồn cùng phạm vi cho tín hiệu trái chiều. Brief giữ cả hai thay vì chọn kết luận thuận ý.', confidence='insufficient', missing_data=missing or ['Nguồn thứ ba hoặc kiểm tra dữ liệu gốc'], warnings=warnings, next_steps=['Kiểm tra dữ liệu gốc và phương pháp thu thập của từng nguồn.', 'Bổ sung nguồn thứ ba cùng phạm vi đo.'])
    if scope_mismatch:
        return Brief(conclusion='Có tín hiệu khác nhau, nhưng các nguồn đang đo các phạm vi khác nhau; không nên so sánh trực tiếp hay gộp thành một kết luận.', confidence='low', missing_data=missing or ['Một chỉ số chung cùng thị trường, phiên bản và kỳ đo'], warnings=warnings, next_steps=['Chuẩn hoá phạm vi: thị trường, phiên bản, nhóm người dùng và định nghĩa chỉ số.', 'Quan sát người chơi hoặc truy vấn telemetry cho đúng phạm vi.'])

    strongest = max(evidence, key=lambda item: item.reliability_score)
    confidence = 'medium' if len(evidence) >= 2 else 'low'
    return Brief(conclusion=f'Bằng chứng hiện nghiêng về: {strongest.excerpt} Đây là nhận định để người nghiên cứu kiểm tra, không phải kết luận nhân quả.', confidence=confidence, missing_data=missing, warnings=warnings, next_steps=['Mở từng nguồn để kiểm tra bối cảnh và mẫu số.', 'Xác nhận nhận định với một nguồn độc lập cùng phạm vi trước khi ra quyết định.'])
