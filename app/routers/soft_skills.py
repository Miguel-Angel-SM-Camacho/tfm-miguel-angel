import time
from fastapi import APIRouter
from app.schemas import ProyectoInput, RankingSoftSkillsOut
from app.state import state
from app.metrics import PREDICTIONS, PREDICTIONS_FAILED, LATENCY
from src.soft_skills import config as config_soft_skills, modelo_aux_soft

router = APIRouter()

@router.post("/ranking/soft_skills", response_model=RankingSoftSkillsOut)
def ranking_soft_skills(proyecto: ProyectoInput, top_n: int = 5, umbral_riesgo_max: float = 0.0):
    PREDICTIONS.labels("soft").inc()
    t0 = time.perf_counter()
    try:
        proyecto_sel = proyecto.model_dump(exclude_none=True)
        ranking, reglas_activas, n_elegidos = modelo_aux_soft.mejores_candidatos(
            proyecto_sel, state.df_candidatos_soft, state.reglas_soft_proyecto,
            state.evidencia_reglas_soft, config_soft_skills,
            top_n=top_n, umbral_riesgo_max=umbral_riesgo_max)
        return modelo_aux_soft.construir_respuesta_json(
            proyecto_sel, ranking, reglas_activas, n_elegidos,
            total_reglas_soft=len(state.reglas_soft_proyecto))
    except Exception:
        PREDICTIONS_FAILED.labels("soft").inc()
        raise
    finally:
        LATENCY.labels("soft").observe(time.perf_counter() - t0)