
import { useEffect, useState } from 'react';

export default function ExportarPage() {
  const [temas, setTemas] = useState([]);
  const [fontes, setFontes] = useState([]);
  const [tema, setTema] = useState('');
  const [fonte, setFonte] = useState('');
  const [dataIni, setDataIni] = useState('');
  const [dataFim, setDataFim] = useState('');

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/temas/`).then(res => res.json()).then(setTemas);
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/fontes/`).then(res => res.json()).then(setFontes);
  }, []);

  const exportar = (formato: string) => {
    const params = new URLSearchParams();
    if (tema) params.append('tema', tema);
    if (fonte) params.append('fonte', fonte);
    if (dataIni) params.append('data_ini', dataIni);
    if (dataFim) params.append('data_fim', dataFim);
    params.append('formato', formato);
    window.open(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/exportar/?` + params.toString(), '_blank');
  };

  return (
    <div className="max-w-3xl mx-auto mt-10 space-y-6">
      <h1 className="text-2xl font-bold">Exportar Documentos</h1>

      <div className="space-y-4">
        <select className="border p-2 rounded w-full" value={tema} onChange={e => setTema(e.target.value)}>
          <option value="">Todos os temas</option>
          {temas.map((t: any) => <option key={t.id} value={t.id}>{t.nome}</option>)}
        </select>

        <select className="border p-2 rounded w-full" value={fonte} onChange={e => setFonte(e.target.value)}>
          <option value="">Todas as fontes</option>
          {fontes.map((f: any) => <option key={f.id} value={f.id}>{f.nome}</option>)}
        </select>

        <div className="flex gap-4">
          <input type="date" className="border p-2 rounded w-full" value={dataIni} onChange={e => setDataIni(e.target.value)} />
          <input type="date" className="border p-2 rounded w-full" value={dataFim} onChange={e => setDataFim(e.target.value)} />
        </div>

        <div className="flex gap-4">
          <button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={() => exportar('csv')}>Exportar CSV</button>
          <button className="bg-green-600 text-white px-4 py-2 rounded" onClick={() => exportar('md')}>Exportar Markdown</button>
          <button className="bg-red-600 text-white px-4 py-2 rounded" onClick={() => exportar('pdf')}>Exportar PDF</button>
        </div>
      </div>
    </div>
  );
}
