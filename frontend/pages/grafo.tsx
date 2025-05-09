
import { useEffect, useRef } from 'react';
import { Network } from 'vis-network/standalone/esm/vis-network';

export default function GrafoPage() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/grafo/`)
      .then(res => res.json())
      .then(data => {
        const nodes = new window.vis.DataSet(data.nodes);
        const edges = new window.vis.DataSet(data.edges);
        const container = containerRef.current;

        if (container) {
          new Network(container, { nodes, edges }, {
            nodes: { shape: 'dot', size: 16, font: { size: 14 } },
            edges: { arrows: 'to', color: '#aaa' },
            physics: { stabilization: false }
          });
        }
      });
  }, []);

  return (
    <div className="max-w-6xl mx-auto mt-10">
      <h1 className="text-2xl font-bold mb-4">Visualização do Grafo</h1>
      <div ref={containerRef} style={{ height: '600px', border: '1px solid #ccc' }} />
    </div>
  );
}
