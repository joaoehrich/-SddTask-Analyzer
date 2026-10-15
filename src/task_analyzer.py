from datetime import datetime, timezone
import logging
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskValidationError(Exception):
    """Exceção customizada lançada para erros de contrato ou dados inválidos."""
    pass


def _parse_datetime(dt_val: Any, field_name: str, task_id: Any) -> datetime:
    """Valida e converte entradas de data garantindo timezone UTC."""
    if dt_val is None:
        raise TaskValidationError(f"Campo obrigatório '{field_name}' ausente na tarefa {task_id}.")
    
    if isinstance(dt_val, datetime):
        dt = dt_val
    elif isinstance(dt_val, str):
        try:
            dt = datetime.fromisoformat(dt_val.replace("Z", "+00:00"))
        except ValueError as e:
            raise TaskValidationError(f"Formato de data inválido para '{field_name}' na tarefa {task_id}: {e}")
    else:
        raise TaskValidationError(f"Tipo inválido para '{field_name}' na tarefa {task_id}.")

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
        
    return dt


def analisar_tarefas(tarefas: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analisa a coleção de tarefas e calcula os indicadores do contrato SDD.
    """
    STATUS_PERMITIDOS = {"concluida", "pendente", "cancelada"}
    PRIORIDADES_PERMITIDAS = {"baixa", "media", "alta"}

    resultado = {
        "tempo_medio_conclusao_min": 0.00,
        "taxa_atraso_percentual": 0.00,
        "quantidade_tarefas": len(tarefas),
        "indicadores_por_prioridade": {
            "baixa": {"quantidade": 0, "tempo_medio_min": 0.00, "taxa_atraso_percentual": 0.00},
            "media": {"quantidade": 0, "tempo_medio_min": 0.00, "taxa_atraso_percentual": 0.00},
            "alta": {"quantidade": 0, "tempo_medio_min": 0.00, "taxa_atraso_percentual": 0.00},
        },
    }

    if not tarefas:
        return resultado

    tempos_conclusao_geral: List[float] = []
    concluidas_avaliaveis_geral = 0
    atrasadas_geral = 0

    por_prioridade: Dict[str, Dict[str, Any]] = {
        p: {"tempos": [], "avaliaveis": 0, "atrasadas": 0, "total": 0}
        for p in PRIORIDADES_PERMITIDAS
    }

    for t in tarefas:
        task_id = t.get("id_tarefa")
        if task_id is None or not isinstance(task_id, int) or task_id <= 0:
            raise TaskValidationError(f"id_tarefa inválido ou ausente: {task_id}")

        status = str(t.get("status", "")).lower()
        prioridade = str(t.get("prioridade", "")).lower()

        if status not in STATUS_PERMITIDOS:
            raise TaskValidationError(f"Status inválido '{status}' na tarefa {task_id}.")
        if prioridade not in PRIORIDADES_PERMITIDAS:
            raise TaskValidationError(f"Prioridade inválida '{prioridade}' na tarefa {task_id}.")

        por_prioridade[prioridade]["total"] += 1

        if status != "concluida":
            continue

        _parse_datetime(t.get("data_criacao"), "data_criacao", task_id)
        prazo = _parse_datetime(t.get("prazo"), "prazo", task_id)

        data_inicio = None
        if t.get("data_inicio") is not None:
            data_inicio = _parse_datetime(t.get("data_inicio"), "data_inicio", task_id)

        data_conclusao = None
        if t.get("data_conclusao") is not None:
            data_conclusao = _parse_datetime(t.get("data_conclusao"), "data_conclusao", task_id)

        # Regra de data inconsistente (RN05)
        data_inconsistente = False
        if data_conclusao and data_inicio and data_conclusao < data_inicio:
            logger.warning(f"Tarefa {task_id} ignorada nos cálculos de tempo: data_conclusao < data_inicio")
            data_inconsistente = True

        if data_conclusao and data_inicio and not data_inconsistente:
            duracao_min = (data_conclusao - data_inicio).total_seconds() / 60.0
            tempos_conclusao_geral.append(duracao_min)
            por_prioridade[prioridade]["tempos"].append(duracao_min)

        if data_conclusao:
            concluidas_avaliaveis_geral += 1
            por_prioridade[prioridade]["avaliaveis"] += 1

            if data_conclusao > prazo:
                atrasadas_geral += 1
                por_prioridade[prioridade]["atrasadas"] += 1

    if tempos_conclusao_geral:
        resultado["tempo_medio_conclusao_min"] = round(
            sum(tempos_conclusao_geral) / len(tempos_conclusao_geral), 2
        )

    if concluidas_avaliaveis_geral > 0:
        resultado["taxa_atraso_percentual"] = round(
            (atrasadas_geral / concluidas_avaliaveis_geral) * 100.0, 2
        )

    for prio, dados in por_prioridade.items():
        media_prio = 0.00
        taxa_atraso_prio = 0.00

        if dados["tempos"]:
            media_prio = round(sum(dados["tempos"]) / len(dados["tempos"]), 2)

        if dados["avaliaveis"] > 0:
            taxa_atraso_prio = round((dados["atrasadas"] / dados["avaliaveis"]) * 100.0, 2)

        resultado["indicadores_por_prioridade"][prio] = {
            "quantidade": dados["total"],
            "tempo_medio_min": media_prio,
            "taxa_atraso_percentual": taxa_atraso_prio,
        }

    return resultado