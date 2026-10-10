import time
from fastapi import APIRouter
from app.schemas import ProyectoInput, RankingHardSkillsOut
from app.state import state
from app.metrics import PREDICTIONS, PREDICTIONS_FAILED, LATENCY
from src.hard_skills import config as config_hard_skills, modelo_aux

router = APIRouter()

@router.post("/ranking/hard_skills", response_model=RankingHardSkillsOut)
def ranking_hard_skills(proyecto: ProyectoInput, top_n: int = 5):
    PREDICTIONS.labels("hard").inc()
    t0 = time.perf_counter()
    try:
        proyecto_sel = proyecto.model_dump(exclude_none=True)
        res = modelo_aux.asignacion_proyecto_candidatos_hard(proyecto_sel, state.df_candidatos_hard, state.df_geo_hard, state.paises_mapa, config_hard_skills, top_n=top_n)
        res = modelo_aux.add_evidencia(res, proyecto_sel, state.df_candidatos_hard, state.reglas_limpias_hard, config_hard_skills)
        return modelo_aux.construir_ranking_json(proyecto_sel, res, state.df_candidatos_hard, state.df_geo_hard, state.paises_mapa, config_hard_skills, top_n=top_n)
    except Exception:
        PREDICTIONS_FAILED.labels("hard").inc()
        raise
    finally:
        LATENCY.labels("hard").observe(time.perf_counter() - t0)