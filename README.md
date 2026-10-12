# Gamota Research Brief MVP

MVP ba ngày cho chuyên viên nghiên cứu thị trường game: nhập một câu hỏi, đối chiếu bằng chứng có metadata và nhận một brief nêu rõ điều đã biết, điều còn thiếu, mâu thuẫn và bước kiểm chứng tiếp theo. Công cụ hỗ trợ lập luận; con người duyệt và ra quyết định cuối cùng.

## Chạy local

Yêu cầu: Node.js 20+, Python 3.11+.

```powershell
Copy-Item .env.example .env
Copy-Item frontend\.env.local.example frontend\.env.local
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Mở một terminal khác:

```powershell
cd frontend
npm install
npm run dev
```

Truy cập http://localhost:3000. API docs: http://localhost:8000/docs.

MVP chạy với evidence seed khi chưa cấu hình Supabase. Để lưu research sessions vào Supabase, chạy `supabase/schema.sql`, sau đó điền `SUPABASE_URL` và `SUPABASE_SERVICE_ROLE_KEY` vào `.env`. Không commit `.env` hay `frontend/.env.local`.

## Cấu trúc

```text
backend/                 FastAPI: core loop, logic xung đột, persistence
frontend/                Next.js App Router + Tailwind
supabase/schema.sql      Schema và RLS cho Supabase PostgreSQL
docs/test-cases.md       05 tình huống kiểm thử theo format Mission 2
```

## Giới hạn có chủ đích

- Retrieval hiện dùng kho evidence demo có thể thay bằng Supabase/RAG adapter.
- `reliability_score` hỗ trợ ưu tiên đọc nguồn, không biến thành sự thật tuyệt đối.
- Không suy ra quan hệ nhân quả chỉ từ phản hồi hay một chỉ số.
- Brief giữ trạng thái `insufficient_evidence` hoặc `conflicted` thay vì ép ra kết luận.
