
import { useEffect, useState } from 'react';

export default function MeuPainelPage() {
  const [favoritos, setFavoritos] = useState([]);
  const [anotacoes, setAnotacoes] = useState([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/meus-favoritos/`, { credentials: 'include' })
      .then(res => res.json()).then(setFavoritos);
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/minhas-anotacoes/`, { credentials: 'include' })
      .then(res => res.json()).then(setAnotacoes);
  }, []);

  return (
    <div className="max-w-5xl mx-auto mt-10 space-y-8">
      <h1 className="text-2xl font-bold">Meu Painel</h1>

      <section>
        <h2 className="text-xl font-semibold mb-2">⭐ Favoritos</h2>
        {favoritos.length === 0 ? <p className="text-gray-500">Nenhum documento favoritado.</p> : (
          <div className="space-y-3">
            {favoritos.map((f: any) => (
              <div key={f.id} className="border p-3 rounded bg-white shadow-sm">
                <div className="text-lg font-semibold">{f.titulo}</div>
                <div className="text-sm text-gray-500">{f.fonte} • {new Date(f.data).toLocaleDateString()}</div>
                <div className="text-sm text-gray-700 mt-1">{f.resumo}...</div>
                <div className="text-xs text-blue-600 mt-1">Temas: {f.temas.join(', ')}</div>
              </div>
            ))}
          </div>
        )}
      </section>

      <section>
        <h2 className="text-xl font-semibold mb-2">📝 Minhas Anotações</h2>
        {anotacoes.length === 0 ? <p className="text-gray-500">Nenhuma anotação registrada.</p> : (
          <div className="space-y-3">
            {anotacoes.map((a: any, i: number) => (
              <div key={i} className="border p-3 rounded bg-white shadow-sm">
                <div className="text-md font-semibold">{a.titulo}</div>
                <div className="text-sm text-gray-700 mt-1">{a.texto}</div>
                <div className="text-xs text-gray-500 mt-1">{new Date(a.criado_em).toLocaleString()}</div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
