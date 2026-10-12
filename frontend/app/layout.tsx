import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = { title: 'Research Brief', description: 'Evidence-aware game market research MVP' };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="vi"><body>{children}</body></html>;
}
