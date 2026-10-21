# 🚀 SDD TaskAnalyzer

[![TaskAnalyzer CI Pipeline](https://github.com/joaoehrich/-SddTask-Analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/joaoehrich/-SddTask-Analyzer/actions)

O **TaskAnalyzer** é um módulo de alta performance desenvolvido para análise, agregação e validação de métricas de tarefas. O projeto foi construído utilizando a metodologia **Spec-Driven Development (SDD)**, com uma governança rigorosa focada no modelo **Critical-in-the-Loop**, containerização via Docker e automação CI/CD com GitHub Actions[cite: 1, 3, 4].

---

## 📐 Arquitetura do Repositório

```text
sdd-task-analyzer/
├── .github/
│   └── workflows/
│       └── ci.yml                 # Motor de CI/CD (GitHub Actions)
├── specs/
│   ├── system_design_document.pdf # Especificação do sistema (SDD)
│   └── task_analyzer_spec.md      # Contrato executável e cenários de aceite
├── src/
│   ├── __init__.py
│   └── task_analyzer.py           # Código homologado e otimizado
├── tests/
│   └── test_harness.py            # Suíte automatizada de testes com pytest
├── CONTEXT_RULES.md               # Regras de contexto e restrições para IA
├── Dockerfile                     # Empacotamento leve (python:3.11-slim)
├── docker-compose.yml             # Orquestração isolada para testes locais
├── requirements.txt               # Dependências do projeto (pytest)
└── README.md                      # Documentação principal