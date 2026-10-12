'use client';

import { useState } from 'react';
import type { Evidence } from '../lib/types';

const stanceLabel = { positive: 'Ủng hộ', negative: 'Phản biện', neutral: 'Bối cảnh' };

export function EvidenceDrawer({ evidence }: { evidence: Evidence[] }) {
  const [open, setOpen] = useState(true);
  return <aside className="rounded-xl border border-slate-700 bg-slate-900/70">
    <button onClick={() => setOpen(!open)} className="flex w-full items-center justify-between px-5 py-4 text-left font-semibold">
      <span>Sources & Evidence <span className="ml-2 rounded-full bg-slate-800 px-2 py-0.5 text-xs text-slate-300">{evidence.length}</span></span><span aria-hidden>{open ? '−' : '+'}</span>
    </button>
    {open && <div className="space-y-3 border-t border-slate-800 p-4">
      {evidence.length === 0 && <p className="text-sm text-slate-400">Chưa có nguồn khớp trực tiếp. Hãy thu hẹp hoặc làm rõ câu hỏi.</p>}
      {evidence.map((item) => <article key={item.id} className="rounded-lg border border-slate-700 bg-slate-950 p-4">
        <div className="mb-2 flex flex-wrap gap-2 text-xs"><span className="rounded bg-slate-800 px-2 py-1">{stanceLabel[item.stance]}</span><span className="rounded bg-slate-800 px-2 py-1">Độ tin cậy {Math.round(item.reliability_score * 100)}%</span></div>
        <h3 className="font-medium">{item.title}</h3><p className="mt-2 text-sm leading-6 text-slate-300">“{item.excerpt}”</p>
        <p className="mt-3 text-xs text-slate-400">{item.source_name} · {item.metadata.published_at} · {item.metadata.market ?? 'Chưa rõ thị trường'} · v{item.metadata.game_version ?? 'chưa rõ'}</p>
        <a className="mt-3 inline-block text-sm text-lime-300 underline" href={item.source_url} target="_blank" rel="noreferrer">Mở nguồn gốc</a>
      </article>)}
    </div>}
  </aside>;
}
