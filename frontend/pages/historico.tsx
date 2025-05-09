
import { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';

type LogItem = {
  pergunta: string;
  resposta: string;
  contexto: string;
  criado_em: string;
};

export default function HistoricoPage() {
  const [logs, setLogs] = useState<LogItem[]>([]);
  const [favoritos, setFavoritos] = useState<Record<number, boolean>>({});
  const [novaAnotacao, setNovaAnotacao] = useState<Record<number, string>>({});

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/historico/`)
      .then(res => res.json())
      .then(data => setLogs(data));
  }, []);

  const alternarFavorito = async (index: number) => {
    const docId = index;
    const url = `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/favorito/${docId}/`;
    const metodo = favoritos[docId] ? 'DELETE' : 'POST';

    await fetch(url, { method: metodo, credentials: 'include' });
    setFavoritos({ ...favoritos, [docId]: !favoritos[docId] });
  };

  const salvarAnotacao = async (index: number) => {
    const texto = novaAnotacao[index];
    await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/anotacao/${index}/`, {
      method: 'POST',
      body: new URLSearchParams({ texto }),
      credentials: 'include'
    });
    alert("Anotação salva!");
    setNovaAnotacao({ ...novaAnotacao, [index]: '' });
  };

  return (
    <div className="max-w-4xl mx-auto mt-10 space-y-6">
      <h1 className="text-2xl font-bold">Histórico de Consultas</h1>
      {logs.length === 0 && <p className="text-gray-500">Nenhum registro disponível.</p>}
      {logs.map((log, index) => (
        <div key={index} className="p-4 border rounded bg-white shadow-sm space-y-2">
          <div className="flex justify-between text-sm text-gray-500 items-center">
            <span><strong>Pergunta:</strong> {log.pergunta}</span>
            <button onClick={() => alternarFavorito(index)} className="text-yellow-500 text-lg">
              {favoritos[index] ? '★' : '☆'}
            </button>
          </div>
          <div className="prose max-w-none bg-gray-50 p-3 rounded">
            <ReactMarkdown>{log.resposta}</ReactMarkdown>
          </div>
          <details className="text-sm text-gray-600 mt-2">
            <summary className="cursor-pointer">Ver contexto usado</summary>
            <pre className="bg-gray-100 mt-2 p-2 rounded text-xs whitespace-pre-wrap">{log.contexto}</pre>
          </details>
          <details className="mt-2">
            <summary className="text-sm text-blue-600 cursor-pointer">+ Anotar</summary>
            <textarea
              rows={2}
              placeholder="Digite sua anotação..."
              className="w-full mt-1 border rounded p-1 text-sm"
              value={novaAnotacao[index] || ''}
              onChange={(e) => setNovaAnotacao({ ...novaAnotacao, [index]: e.target.value })}
            />
            <button
              onClick={() => salvarAnotacao(index)}
              className="mt-1 text-sm bg-blue-600 text-white px-2 py-1 rounded"
            >
              Salvar Anotação
            </button>
          </details>
        </div>
      ))}
    </div>
  );
}
