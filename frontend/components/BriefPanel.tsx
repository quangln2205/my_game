import type { ResearchResult } from '../lib/types';

const confidenceLabel = { high: 'Tin cậy cao', medium: 'Cần kiểm tra thêm', low: 'Độ chắc chắn thấp', insufficient: 'Chưa thể kết luận' };

export function BriefPanel({ result }: { result: ResearchResult | null }) {
  if (!result) return <section className="rounded-xl border border-dashed border-slate-700 bg-slate-900/40 p-6 text-slate-400">Nhập câu hỏi để tạo brief. Thử: “Người chơi mới có gặp trở ngại ở tutorial không?”</section>;
  const { brief } = result;
  return <section className="space-y-5 rounded-xl border border-slate-700 bg-slate-900/70 p-6">
    <div className="flex flex-wrap items-center justify-between gap-3"><h2 className="text-lg font-semibold">Bản nhận định</h2><span className="rounded-full border border-lime-400/40 bg-lime-400/10 px-3 py-1 text-sm text-lime-200">{confidenceLabel[brief.confidence]}</span></div>
    <p className="text-lg leading-8 text-slate-100">{brief.conclusion}</p>
    <p className="text-sm text-amber-200">Trạng thái: cần người nghiên cứu duyệt trước khi ra quyết định.</p>
    {brief.warnings.length > 0 && <div><h3 className="font-medium">Cảnh báo</h3><ul className="mt-2 space-y-2 text-sm text-amber-100">{brief.warnings.map((warning, index) => <li key={`${warning.code}-${index}`} className="rounded bg-amber-300/10 p-3">{warning.message}</li>)}</ul></div>}
    {brief.missing_data.length > 0 && <div><h3 className="font-medium">Phần còn thiếu</h3><ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-300">{brief.missing_data.map((item) => <li key={item}>{item}</li>)}</ul></div>}
    <div><h3 className="font-medium">Bước xác minh tiếp theo</h3><ol className="mt-2 list-decimal space-y-1 pl-5 text-sm text-slate-300">{brief.next_steps.map((item) => <li key={item}>{item}</li>)}</ol></div>
  </section>;
}
