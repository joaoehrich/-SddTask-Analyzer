Regras de governança para o agente de IA e mantenedores.
```markdown
# Regras de Governança e Contexto de IA (CONTEXT_RULES)

## Arquitetura e Tecnologia
- Linguagem: Python 3.11+
- Tipagem: Type hints obrigatórios em 100% das funções.
- Estilo: PEP 8 e Google Style Docstrings.
- Fuso Horário: Sempre tratar datas em padrão UTC.

## Restrições de Negócio
- Não persistir dados em banco ou arquivos.
- Prevenir divisão por zero retornando 0.00 para conjuntos sem tarefas concluídas.
- Não alterar as assinaturas das funções especificadas no contrato.
- Utilizar tratamento de exceções específico com a exceção customizada `TaskValidationError`.