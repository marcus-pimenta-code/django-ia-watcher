
import { useEffect, useState } from 'react';

export default function RecomendacoesPage() {
  const [docs, setDocs] = useState([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/recomendacoes/`, { credentials: 'include' })
      .then(res => res.json()).then(setDocs);
  }, []);

  return (
    <div className="max-w-4xl mx-auto mt-10 space-y-6">
      <h1 className="text-2xl font-bold">Recomendações Personalizadas</h1>
      {docs.length === 0 ? (
        <p className="text-gray-500">Nenhuma sugestão no momento. Favoritar ou anotar documentos ajuda a melhorar as recomendações.</p>
      ) : (
        <div className="space-y-4">
          {docs.map((doc: any) => (
            <div key={doc.id} className="border rounded p-4 bg-white shadow-sm">
              <h2 className="text-lg font-semibold">{doc.titulo}</h2>
              <p className="text-sm text-gray-500">{doc.fonte} • {new Date(doc.data).toLocaleDateString()}</p>
              <p className="text-sm text-gray-700 mt-2">{doc.resumo}...</p>
              <p className="text-xs text-blue-600 mt-2">Temas: {doc.temas.join(', ')}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
