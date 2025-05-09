import Link from 'next/link';

export default function ImplementacaoPagina() {
  return (
    <div className="space-y-8">
      <section>
        <h1 className="text-3xl font-bold mb-6">Guia de Implementação</h1>
        <p className="mb-4">
          Este guia fornece instruções passo a passo para implementar e operar seu próprio Observatório de IA 
          com foco em educação profissional. A estrutura é flexível e adaptável às suas necessidades específicas.
        </p>
      </section>

      <section className="card">
        <h2>Passo a Passo para Implementação</h2>
        
        <div className="mb-8">
          <h3 className="mb-3">Fase 1: Configuração Inicial (1-2 dias)</h3>
          
          <div className="bg-gray-50 dark:bg-slate-700 p-4 rounded-lg mb-4">
            <h4 className="font-semibold mb-2">1. Escolha da Plataforma</h4>
            <ul className="list-disc pl-6">
              <li>Decidir entre Obsidian ou Notion com base nas suas preferências</li>
              <li>Instalar a aplicação escolhida ou criar conta (Notion)</li>
            </ul>
          </div>
          
          <div className="bg-gray-50 dark:bg-slate-700 p-4 rounded-lg mb-4">
            <h4 className="font-semibold mb-2">2. Criação da Estrutura Básica</h4>
            <ul className="list-disc pl-6">
              <li>Configurar a estrutura de pastas conforme definido</li>
              <li>Criar os templates de notas</li>
              <li>Configurar o sistema inicial de tags</li>
            </ul>
          </div>
          
          <div className="bg-gray-50 dark:bg-slate-700 p-4 rounded-lg">
            <h4 className="font-semibold mb-2">3. Configuração de Ferramentas de Captura</h4>
            <ul className="list-disc pl-6">
              <li>Instalar extensões de navegador para clipping</li>
              <li>Configurar agregador de RSS (Feedly/Inoreader)</li>
              <li>Configurar alertas do Google para termos-chave</li>
            </ul>
          </div>
        </div>
        
        <div className="mb-8">
          <h3 className="mb-3">Fase 2: Implementação do Workflow (3-5 dias)</h3>
          
          <div className="bg-gray-50 dark:bg-slate-700 p-4 rounded-lg mb-4">
            <h4 className="font-semibold mb-2">1. Teste Inicial</h4>
            <ul className="list-disc pl-6">
              <li>Capturar e processar 5-10 itens manualmente</li>
              <li>Ajustar templates e fluxo conforme necessário</li>
            </ul>
          </div>
          
          <div className="bg-gray-50 dark:bg-slate-700 p-4 rounded-lg mb-4">
            <h4 className="font-semibold mb-2">2. Configuração de Automações</h4>
            <ul className="list-disc pl-6">
              <li>Configurar regras IFTTT/Zapier para automação</li>
              <li>Testar e refinar as automações</li>
            </ul>
          </div>
          
          <div className="bg-gray-50 dark:bg-slate-700 p-4 rounded-lg">
            <h4 className="font-semibold mb-2">3. Desenvolvimento de Rotina</h4>
            <ul className="list-disc pl-6">
              <li>Implementar a rotina diária recomendada</li>
              <li>Ajustar tempos e processos conforme necessário</li>
            </ul>
          </div>
        </div>
        
        <div>
          <h3 className="mb-3">Fase 3: Expansão e Refinamento (Contínuo)</h3>
          
          <div className="bg-gray-50 dark:bg-slate-700 p-4 rounded-lg mb-4">
            <h4 className="font-semibold mb-2">1. Expansão de Fontes</h4>
            <ul className="list-disc pl-6">
              <li>Adicionar gradualmente mais fontes de informação</li>
              <li>Refinar a priorização de fontes com base na relevância</li>
            </ul>
          </div>
          
          <div className="bg-gray-50 dark:bg-slate-700 p-4 rounded-lg mb-4">
            <h4 className="font-semibold mb-2">2. Refinamento de Taxonomia</h4>
            <ul className="list-disc pl-6">
              <li>Ajustar o sistema de tags conforme necessário</li>
              <li>Desenvolver MOCs mais detalhados</li>
            </ul>
          </div>
          
          <div className="bg-gray-50 dark:bg-slate-700 p-4 rounded-lg">
            <h4 className="font-semibold mb-2">3. Otimização de Processos</h4>
            <ul className="list-disc pl-6">
              <li>Identificar gargalos no workflow e otimizar</li>
              <li>Aumentar gradualmente o nível de automação</li>
            </ul>
          </div>
        </div>
      </section>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <section className="card">
          <h2>Dicas para Implementação em Obsidian</h2>
          
          <div className="mb-6">
            <h3 className="mb-2">Plugins Recomendados</h3>
            <ul className="list-disc pl-6">
              <li><strong>Dataview:</strong> Para criar painéis e visualizações dinâmicas</li>
              <li><strong>Tag Wrangler:</strong> Para gerenciamento eficiente de tags</li>
              <li><strong>Templater:</strong> Para templates avançados</li>
              <li><strong>Calendar:</strong> Para visualização e navegação temporal</li>
              <li><strong>Obsidian Git:</strong> Para backup e sincronização</li>
            </ul>
          </div>
          
          <div>
            <h3 className="mb-2">Configurações Recomendadas</h3>
            <ul className="list-disc pl-6">
              <li>Ativar "Strict line breaks" para melhor compatibilidade</li>
              <li>Configurar "Default location for new notes" para organização automática</li>
              <li>Personalizar hotkeys para operações frequentes</li>
            </ul>
          </div>
        </section>

        <section className="card">
          <h2>Dicas para Implementação em Notion</h2>
          
          <div className="mb-6">
            <h3 className="mb-2">Configurações de Banco de Dados</h3>
            <ul className="list-disc pl-6">
              <li>Criar um banco de dados principal para todas as notas</li>
              <li>Configurar propriedades para metadados (fonte, data, tags, etc.)</li>
              <li>Criar views filtradas para diferentes categorias e tags</li>
            </ul>
          </div>
          
          <div>
            <h3 className="mb-2">Integrações Recomendadas</h3>
            <ul className="list-disc pl-6">
              <li>Configurar integração com e-mail para captura direta</li>
              <li>Utilizar API do Notion (ou ferramentas como Make) para automações avançadas</li>
              <li>Configurar templates de página para padronização</li>
            </ul>
          </div>
        </section>
      </div>

      <section className="card">
        <h2>Manutenção e Evolução</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div>
            <h3 className="mb-2">Manutenção Diária</h3>
            <ul className="list-disc pl-6">
              <li>Backup automático da base de conhecimento</li>
              <li>Verificação de links quebrados</li>
              <li>Atualização de índices e MOCs</li>
            </ul>
          </div>
          
          <div>
            <h3 className="mb-2">Manutenção Mensal</h3>
            <ul className="list-disc pl-6">
              <li>Revisar e refinar taxonomia de tags</li>
              <li>Avaliar eficácia das fontes de informação</li>
              <li>Ajustar automações conforme necessário</li>
            </ul>
          </div>
          
          <div>
            <h3 className="mb-2">Manutenção Trimestral</h3>
            <ul className="list-disc pl-6">
              <li>Revisar estrutura geral da base de conhecimento</li>
              <li>Atualizar lista de fontes de informação</li>
              <li>Avaliar e otimizar o workflow</li>
            </ul>
          </div>
        </div>
        
        <h3 className="mb-3">Métricas de Avaliação</h3>
        <p className="mb-4">Para avaliar a eficácia do workflow, considere monitorar:</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-gray-50 dark:bg-slate-700 p-4 rounded-lg">
            <h4 className="font-semibold mb-2">Volume de Processamento</h4>
            <ul className="list-disc pl-6">
              <li>Número de itens capturados diariamente</li>
              <li>Número de notas criadas semanalmente</li>
            </ul>
          </div>
          
          <div className="bg-gray-50 dark:bg-slate-700 p-4 rounded-lg">
            <h4 className="font-semibold mb-2">Qualidade do Conteúdo</h4>
            <ul className="list-disc pl-6">
              <li>Relevância das informações capturadas</li>
              <li>Profundidade e utilidade das notas</li>
            </ul>
          </div>
          
          <div className="bg-gray-50 dark:bg-slate-700 p-4 rounded-lg">
            <h4 className="font-semibold mb-2">Eficiência do Processo</h4>
            <ul className="list-disc pl-6">
              <li>Tempo gasto em cada etapa do workflow</li>
              <li>Nível de automação alcançado</li>
            </ul>
          </div>
          
          <div className="bg-gray-50 dark:bg-slate-700 p-4 rounded-lg">
            <h4 className="font-semibold mb-2">Impacto</h4>
            <ul className="list-disc pl-6">
              <li>Feedback dos usuários da base de conhecimento</li>
              <li>Aplicações práticas derivadas das informações coletadas</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6">
        <h2 className="text-2xl font-bold mb-4">Considerações Finais</h2>
        <p className="mb-4">
          Este workflow foi projetado para ser flexível e adaptável às suas necessidades específicas. 
          Comece com as etapas essenciais e gradualmente incorpore mais automação e sofisticação conforme 
          se familiariza com o processo.
        </p>
        <p>
          Lembre-se que a consistência é mais importante que a perfeição - é melhor ter um processo simples 
          que você execute diariamente do que um complexo que raramente é seguido.
        </p>
      </section>

      <div className="flex justify-between mt-8">
        <Link href="/workflow" className="btn-secondary">
          ← Workflow de Atualização
        </Link>
        <Link href="/" className="btn-primary">
          Voltar para Início
        </Link>
      </div>
    </div>
  );
}
