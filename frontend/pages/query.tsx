
import { useState } from 'react';

export default function QueryPage() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const formData = new FormData();
      formData.append('query', query);

      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/query/`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        throw new Error('Erro ao consultar a API');
      }

      const html = await res.text();
      setResponse(html);
    } catch (err) {
      setError('Erro ao processar sua consulta.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto mt-10 space-y-6">
      <h1 className="text-2xl font-bold">Consultar Base de Conhecimento</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <textarea
          className="w-full p-2 border rounded"
          rows={4}
          placeholder="Digite sua pergunta..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          required
        />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
          Enviar Consulta
        </button>
      </form>

      {loading && <p>Consultando...</p>}
      {error && <p className="text-red-600">{error}</p>}
      {response && (
        <div className="p-4 border rounded bg-gray-100">
          <h2 className="font-semibold mb-2">Resposta:</h2>
          <div dangerouslySetInnerHTML={{ __html: response }} />
        </div>
      )}
    </div>
  );
}
