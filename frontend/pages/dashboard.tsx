
import { useEffect, useState } from 'react';
import { Bar, Line, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  PointElement,
  LineElement,
  Tooltip,
  LineElement,
  Legend
);

export default function DashboardPage() {
  const [stats, setStats] = useState<any>(null);
  const [detalhes, setDetalhes] = useState<any>(null);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/dashboard/`)
      .then(res => res.json())
      .then(data => setStats(data));
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/dashboard/detalhes/`)
      .then(res => res.json())
      .then(data => setDetalhes(data));
  }, []);

  return (
    <div className="max-w-6xl mx-auto mt-10 space-y-10">
      <h1 className="text-2xl font-bold">Painel do Observatório</h1>

      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
          {Object.entries(stats).map(([label, value]) => (
            <div key={label} className="bg-white shadow-sm rounded p-4 text-center border">
              <p className="text-sm text-gray-500">{label}</p>
              <p className="text-2xl font-bold text-blue-600">{value}</p>
            </div>
          ))}
        </div>
      )}

      {detalhes && (
        <div className="space-y-10">
          <div>
            <h2 className="text-xl font-semibold mb-2">Documentos por Dia</h2>
            <Line data={{
              labels: detalhes.por_data.map((d: any) => d.data),
              datasets: [{
                label: 'Documentos',
                data: detalhes.por_data.map((d: any) => d.qtd),
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59,130,246,0.2)',
                tension: 0.3
              }]
            }} />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
            <div>
              <h2 className="text-xl font-semibold mb-2">Fontes mais ativas</h2>
              <Bar data={{
                labels: detalhes.fontes.map((f: any) => f.nome),
                datasets: [{
                  label: 'Qtd',
                  data: detalhes.fontes.map((f: any) => f.qtd),
                  backgroundColor: '#10b981'
                }]
              }} />
            </div>

            <div>
              <h2 className="text-xl font-semibold mb-2">Temas mais frequentes</h2>
              <Pie data={{
                labels: detalhes.temas.map((t: any) => t.nome),
                datasets: [{
                  data: detalhes.temas.map((t: any) => t.qtd),
                  backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#6366f1', '#8b5cf6', '#ec4899']
                }]
              }} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
