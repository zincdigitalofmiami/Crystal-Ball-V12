import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Crystal Ball - Soybean Oil Futures Intelligence',
  description: 'Advanced forecasting system for soybean oil procurement optimization',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
