# Especificação Técnica - TaskAnalyzer (SDD)

## Contrato de Interface
- **Função Principal:** `analisar_tarefas(tarefas: list[dict]) -> dict`
- **Exceção Customizada:** `TaskValidationError`

## Entradas (Inputs por tarefa)
- `id_tarefa` (int, obrigatório, > 0)
- `data_criacao` (datetime, obrigatório)
- `data_inicio` (datetime, opcional)
- `data_conclusao` (datetime, opcional)
- `prazo` (datetime, obrigatório)
- `prioridade` (str: 'baixa', 'media', 'alta')
- `status` (str: 'concluida', 'pendente', 'cancelada')

## Saídas (Outputs)
- `tempo_medio_conclusao_min` (float)
- `taxa_atraso_percentual` (float)
- `quantidade_tarefas` (int)
- `indicadores_por_prioridade` (dict contendo métricas por prioridade)