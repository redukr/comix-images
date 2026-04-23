import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "JOJ Comic Generator",
  description: "Генератор коміксів про кар'єрний ріст в ЗСУ",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="uk">
      <body className="antialiased bg-gray-50">
        <header className="bg-joj-blue text-white p-4 shadow-lg">
          <div className="container mx-auto flex items-center justify-between">
            <h1 className="text-2xl font-bold">JOJ Comic Generator</h1>
            <nav className="flex gap-4">
              <a href="/" className="hover:text-joj-yellow transition">Головна</a>
              <a href="/generator" className="hover:text-joj-yellow transition">Генератор</a>
              <a href="/gallery" className="hover:text-joj-yellow transition">Галерея</a>
            </nav>
          </div>
        </header>
        <main className="container mx-auto py-8 px-4">
          {children}
        </main>
        <footer className="bg-joj-blue text-white p-4 mt-8">
          <div className="container mx-auto text-center">
            <p>JOJ Comic Generator © 2024</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
