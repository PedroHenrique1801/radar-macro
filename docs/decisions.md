# Decisões de Arquitetura (ADR)

Registro das decisões técnicas relevantes tomadas durante o desenvolvimento, no formato Architecture Decision Record.

---

## ADR-001 — Vetor fixo na query de busca (bug corrigido)

**Status:** Resolvido

**Contexto**
A busca da API sempre retornava os mesmos 3 trechos, independente da pergunta enviada. A query SQL comparava com o vetor de um documento fixo (`WHERE id = 1`), resquício de um teste anterior usado apenas para validar a sintaxe do operador `<=>` do `pgvector` em Java.

**Decisão**
Substituir o vetor fixo pelo embedding gerado dinamicamente a partir da pergunta do usuário em tempo de requisição.

**Consequências**
A busca passou a refletir a similaridade semântica real. Expôs a necessidade de validar não só se um endpoint responde (`200 OK`), mas se a lógica de negócio por trás dele está correta.

---

## ADR-002 — Migração de embeddings de `sentence-transformers` para OpenAI

**Status:** Resolvido

**Contexto**
Os embeddings dos documentos eram gerados localmente com `sentence-transformers` (gratuito). Ao corrigir o ADR-001, seria necessário gerar o embedding da pergunta em Java — sem um caminho direto para rodar esse modelo nessa linguagem.

**Decisão**
Migrar toda a base de embeddings (documentos e perguntas) para a API da OpenAI (`text-embedding-3-small`).

**Consequências**
- Positivo: permite gerar embeddings nativamente via HTTP em Java; evita comparar vetores de modelos diferentes, que não são matematicamente compatíveis entre si.
- Trade-off aceito: custo pequeno e recorrente por chamada de API, em troca de uma arquitetura mais simples e confiável para demonstração.

---

## ADR-003 — Erro 406 na API do Banco Central

**Status:** Resolvido

**Contexto**
A ingestão de dados via API do BCB retornava `406 Client Error`, mesmo com headers de navegador simulados. Hipótese inicial de bloqueio de bot (WAF) não se sustentou em teste a partir de origem diferente.

**Decisão**
Investigar a documentação oficial da API antes de assumir causa raiz. Identificado que, desde março/2025, a API exige parâmetros de data (`dataInicial`/`dataFinal`) obrigatórios.

**Consequências**
Corrigido incluindo os parâmetros de data na requisição. Reforça a prática de validar hipóteses de erro contra a fonte oficial antes de aplicar workarounds.

---

## ADR-004 — Normalização de texto na avaliação automatizada

**Status:** Resolvido

**Contexto**
Dois casos da avaliação automatizada falhavam mesmo com o retrieval funcionando corretamente. O texto extraído dos PDFs preservava artefatos de formatação original (quebras de linha, hifenização de fim de linha), quebrando comparações de substring exata.

**Decisão**
Normalizar espaços em branco (`re.sub(r'\s+', ' ', texto)`) antes da comparação no script de avaliação.

**Consequências**
Taxa de acerto medida subiu de 80% para 100% — refletindo a real eficácia da busca semântica, que já funcionava corretamente antes do ajuste. A hifenização em si permanece uma limitação conhecida da extração de PDF, sem impacto observado na qualidade da resposta final gerada pelo LLM.