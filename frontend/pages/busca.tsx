
import { useEffect, useState } from 'react';

export default function BuscaPage() {
  const [termo, setTermo] = useState('');
  const [tema, setTema] = useState('');
  const [fonte, setFonte] = useState('');
  const [temas, setTemas] = useState([]);
  const [fontes, setFontes] = useState([]);
  const [resultados, setResultados] = useState([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/temas/`).then(res => res.json()).then(setTemas);
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/fontes/`).then(res => res.json()).then(setFontes);
  }, []);

  const buscar = async () => {
    const query = new URLSearchParams();
    if (termo) query.append("termo", termo);
    if (tema) query.append("tema", tema);
    if (fonte) query.append("fonte", fonte);
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/busca/?` + query.toString());
    const data = await res.json();
    setResultados(data);
  };

  return (
    <div className="max-w-5xl mx-auto mt-10 space-y-6">
      <h1 className="text-2xl font-bold">Busca Híbrida</h1>

      <div className="flex gap-4 flex-wrap">
        <input
          type="text"
          placeholder="Digite um termo..."
          className="border p-2 rounded w-full sm:w-1/2"
          value={termo}
          onChange={e => setTermo(e.target.value)}
        />
        <select className="border p-2 rounded" value={tema} onChange={e => setTema(e.target.value)}>
          <option value="">Todos os temas</option>
          {temas.map((t: any) => <option key={t.id} value={t.id}>{t.nome}</option>)}
        </select>
        <select className="border p-2 rounded" value={fonte} onChange={e => setFonte(e.target.value)}>
          <option value="">Todas as fontes</option>
          {fontes.map((f: any) => <option key={f.id} value={f.id}>{f.nome}</option>)}
        </select>
        <button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={buscar}>Buscar</button>
      </div>

      <div className="space-y-4">
        {resultados.map((doc: any) => (
          <div key={doc.id} className="border rounded p-4 shadow-sm bg-white">
            <h2 className="text-lg font-semibold">{doc.titulo}</h2>
            <p className="text-sm text-gray-500">{doc.fonte} • {new Date(doc.data).toLocaleDateString()}</p>
            <div className="text-sm text-gray-700 mt-2">{doc.resumo}...</div>
            <div className="text-xs text-blue-600 mt-2">Temas: {doc.temas.join(', ')}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
