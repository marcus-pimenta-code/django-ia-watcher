import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Observatório de IA | Educação Profissional",
  description: "Observatório de Inteligência Artificial com foco em novidades, tendências e casos de uso em educação profissional",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body className={inter.className}>
        <header className="bg-white dark:bg-slate-900 shadow-md">
          <div className="container mx-auto py-4">
            <div className="flex justify-between items-center">
              <div className="flex items-center">
                <h1 className="text-xl font-bold text-blue-700 dark:text-blue-400 m-0">
                  Observatório de IA
                </h1>
                <span className="ml-2 text-sm bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-2 py-0.5 rounded">
                  Educação Profissional
                </span>
              </div>
              <nav>
                <ul className="flex space-x-1">
                  <li><a href="/" className="nav-link">Início</a></li>
                  <li><a href="/estrutura" className="nav-link">Estrutura</a></li>
                  <li><a href="/fontes" className="nav-link">Fontes</a></li>
                  <li><a href="/workflow" className="nav-link">Workflow</a></li>
                  <li><a href="/implementacao" className="nav-link">Implementação</a></li>
                </ul>
              </nav>
            </div>
          </div>
        </header>
        <main className="container mx-auto py-8 px-4">
          {children}
        </main>
        <footer className="bg-gray-100 dark:bg-slate-800 py-6">
          <div className="container mx-auto px-4">
            <div className="flex flex-col md:flex-row justify-between items-center">
              <div className="mb-4 md:mb-0">
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  © {new Date().getFullYear()} Observatório de IA | Educação Profissional
                </p>
              </div>
              <div>
                <ul className="flex space-x-4">
                  <li><a href="/sobre" className="text-sm text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400">Sobre</a></li>
                  <li><a href="/contato" className="text-sm text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400">Contato</a></li>
                </ul>
              </div>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
