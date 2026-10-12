'use client';

import { FormEvent, useState } from 'react';
import { BriefPanel } from '../components/BriefPanel';
import { EvidenceDrawer } from '../components/EvidenceDrawer';
import type { ResearchResult } from '../lib/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000';

export default function Home() {
  const [question, setQuestion] = useState('Người chơi mới có gặp trở ngại ở tutorial không?');
  const [result, setResult] = useState<ResearchResult | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault(); setLoading(true); setError('');
    try {
      const response = await fetch(`${API_BASE_URL}/api/research`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ question }) });
      if (!response.ok) throw new Error('API chưa trả về brief hợp lệ. Kiểm tra FastAPI đang chạy tại cổng 8000.');
      setResult(await response.json());
    } catch (caught) { setError(caught instanceof Error ? caught.message : 'Không thể chạy phân tích.'); }
    finally { setLoading(false); }
  }

  return <main className="mx-auto max-w-6xl px-5 py-10 md:px-8"><header className="mb-10"><p className="text-sm font-semibold tracking-widest text-lime-300">GAMOTA · RESEARCH BRIEF MVP</p><h1 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">Kết luận chỉ có giá trị khi kiểm chứng được.</h1><p className="mt-3 max-w-3xl text-slate-400">Một core loop nhỏ cho chuyên viên nghiên cứu: câu hỏi → bằng chứng có bối cảnh → brief có giới hạn → con người quyết định.</p></header>
    <form onSubmit={submit} className="mb-8 rounded-xl border border-slate-700 bg-slate-900/70 p-5"><label htmlFor="question" className="font-medium">Câu hỏi nghiên cứu</label><textarea id="question" value={question} onChange={(event) => setQuestion(event.target.value)} minLength={8} className="mt-3 min-h-28 w-full rounded-lg border border-slate-600 bg-slate-950 p-3 text-slate-100" /><div className="mt-3 flex items-center justify-between gap-3"><p className="text-xs text-slate-400">Nguồn demo. Mở Sources & Evidence để tự kiểm tra bối cảnh.</p><button disabled={loading} className="rounded-lg bg-lime-300 px-4 py-2 font-semibold text-slate-950 hover:bg-lime-200 disabled:opacity-50">{loading ? 'Đang phân tích…' : 'Tạo brief'}</button></div>{error && <p role="alert" className="mt-3 text-sm text-red-300">{error}</p>}</form>
    <div className="grid gap-6 lg:grid-cols-[minmax(0,1.3fr)_minmax(320px,0.9fr)]"><BriefPanel result={result} /><EvidenceDrawer evidence={result?.evidence ?? []} /></div>
  </main>;
}
