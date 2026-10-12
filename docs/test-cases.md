# Bộ kiểm thử Mission 2

Chạy automated checks:

```powershell
cd backend
pytest
```

| # | Tình huống | Kỳ vọng | Kết quả thực tế | Đạt/Chưa đạt | Điều học được |
|---|---|---|---|---|---|
| 1 | Câu hỏi về tiềm năng Strategy RPG tại Việt Nam | Brief dẫn về nguồn báo cáo, nêu độ tin cậy và bước kiểm tra thêm. | Nguồn market report được tìm thấy; brief chỉ là nhận định cần đối chiếu. | Đạt | Luồng câu hỏi → evidence → brief hoạt động với câu hỏi có tín hiệu rõ. |
| 2 | Tutorial có telemetry hoàn thành cao nhưng khảo sát phản ánh bối rối | Không ép một kết luận; giải thích hai nguồn có khác định nghĩa chỉ số. | Có cảnh báo `scope_mismatch`, confidence thấp và bước chuẩn hoá phạm vi. | Đạt | Hoàn thành tutorial không đồng nghĩa người chơi hiểu trải nghiệm. |
| 3 | Câu hỏi không có evidence khớp | Ghi rõ “chưa thể kết luận”, không bịa nguồn. | Trả về `insufficient_evidence` và yêu cầu làm rõ phạm vi. | Đạt | Cần mở rộng kho nguồn trước khi dùng cho câu hỏi ngoài dữ liệu demo. |
| 4 | Community post sau bản 1.4.1 báo lỗi nhận thưởng | Gắn cờ độ tin cậy thấp và phiên bản thay vì khẳng định lỗi thiết kế. | Nguồn được đánh dấu low reliability; brief yêu cầu kiểm tra dữ liệu gốc. | Đạt | Phản hồi cộng đồng phù hợp để tạo giả thuyết, không đủ để kết luận. |
| 5 | Hai bằng chứng cùng phạm vi nhưng stance đối nghịch | Hệ thống giữ cả hai và trả về “chưa thể kết luận”. | Automated test `test_same_scope_opposing_evidence_is_insufficient` pass. | Đạt | MVP đã xử lý đúng xung đột trực tiếp; bước sau là thêm nguồn thứ ba và UI so sánh chi tiết hơn. |

## Giới hạn hiện tại và ưu tiên tiếp theo

Trường hợp MVP xử lý chưa tốt là retrieval ngây thơ dựa trên từ khoá: câu hỏi dùng đồng nghĩa hoặc tên game mới có thể không lấy được evidence liên quan. Trong ba ngày, đây là đánh đổi chấp nhận được để kiểm chứng core loop. Nếu có thêm thời gian, ưu tiên kế tiếp là embedding retrieval có filter bắt buộc theo market/version/date, đánh giá retrieval bằng tập câu hỏi thật và liên kết session/brief vào Supabase thật.
