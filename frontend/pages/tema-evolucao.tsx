
import { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Tooltip, Legend);

export default function TemaEvolucaoPage() {
  const [temas, setTemas] = useState([]);
  const [temaId, setTemaId] = useState('');
  const [dados, setDados] = useState([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/temas/`)
      .then(res => res.json()).then(setTemas);
  }, []);

  useEffect(() => {
    if (temaId) {
      fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/tema/evolucao/${temaId}/?dias=60`)
        .then(res => res.json()).then(setDados);
    }
  }, [temaId]);

  return (
    <div className="max-w-4xl mx-auto mt-10 space-y-6">
      <h1 className="text-2xl font-bold">Evolução Temporal por Tema</h1>
      <select
        className="border p-2 rounded"
        value={temaId}
        onChange={(e) => setTemaId(e.target.value)}
      >
        <option value="">Selecione um tema</option>
        {temas.map((t: any) => (
          <option key={t.id} value={t.id}>{t.nome}</option>
        ))}
      </select>

      {dados.length > 0 && (
        <div className="bg-white p-4 rounded shadow">
          <Line
            data={{
              labels: dados.map((d: any) => d.data),
              datasets: [{
                label: 'Documentos',
                data: dados.map((d: any) => d.qtd),
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59,130,246,0.2)',
                tension: 0.3
              }]
            }}
          />
        </div>
      )}
    </div>
  );
}
