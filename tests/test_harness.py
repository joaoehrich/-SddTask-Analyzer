import pytest
from src.task_analyzer import TaskValidationError, analisar_tarefas


def test_cenario_1_sucesso_metricas():
    tarefas = [
        {
            "id_tarefa": 1,
            "data_criacao": "2026-03-01T10:00:00Z",
            "data_inicio": "2026-03-01T10:00:00Z",
            "data_conclusao": "2026-03-01T11:00:00Z",  # 60 minutos
            "prazo": "2026-03-01T12:00:00Z",
            "prioridade": "alta",
            "status": "concluida",
        },
        {
            "id_tarefa": 2,
            "data_criacao": "2026-03-01T10:00:00Z",
            "data_inicio": "2026-03-01T10:00:00Z",
            "data_conclusao": "2026-03-01T12:00:00Z",  # 120 minutos
            "prazo": "2026-03-01T11:00:00Z",            # Atrasada
            "prioridade": "alta",
            "status": "concluida",
        },
    ]

    res = analisar_tarefas(tarefas)
    assert res["quantidade_tarefas"] == 2
    assert res["tempo_medio_conclusao_min"] == 90.00
    assert res["taxa_atraso_percentual"] == 50.00


def test_cenario_2_excecao_status_invalido():
    tarefa = [
        {
            "id_tarefa": 1,
            "data_criacao": "2026-03-01T10:00:00Z",
            "prazo": "2026-03-01T12:00:00Z",
            "prioridade": "alta",
            "status": "invalid_status",
        }
    ]
    with pytest.raises(TaskValidationError):
        analisar_tarefas(tarefa)


def test_cenario_3_divisao_por_zero_prevention():
    res = analisar_tarefas([])
    assert res["tempo_medio_conclusao_min"] == 0.00
    assert res["taxa_atraso_percentual"] == 0.00