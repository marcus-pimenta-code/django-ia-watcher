
import '../styles/globals.css'
import type { AppProps } from 'next/app'

export default function App({ Component, pageProps }: AppProps) {
  return (
    <>
      <nav className="bg-gray-900 text-white p-4 flex gap-4">
        <a href="/" className="hover:underline">Início</a>
        <a href="/query" className="hover:underline">Consulta</a>
        <a href="/historico" className="hover:underline">Histórico</a>
        <a href="/grafo" className="hover:underline">Grafo</a>
        <a href="/dashboard" className="hover:underline">Dashboard</a>
        <a href="/busca" className="hover:underline font-bold">Busca Híbrida</a>
        <a href="/meu-painel" className="hover:underline">Meu Painel</a>
  <a href="/tema-evolucao" className="hover:underline">Evolução por Tema</a>
  <a href="/recomendacoes" className="hover:underline">Recomendações</a>
  <a href="/exportar" className="hover:underline">Exportar</a>
</nav>
      <main className="p-4">
        <Component {...pageProps} />
      </main>
    </>
  );
}
