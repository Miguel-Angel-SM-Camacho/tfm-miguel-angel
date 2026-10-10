from fastapi import FastAPI, HTTPException
from app.state import lifespan, state
from app.routers import hard_skills, soft_skills
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="Sistema de recomenación de personal",
    description="Motor de emparejamiento candidato-proyecto explicable: hard skills (distancia/similitud) y soft skills (riesgo + compromiso).",
    lifespan=lifespan,
)

Instrumentator().instrument(app).expose(app)

app.include_router(hard_skills.router,tags=["hard_skills"])
app.include_router(soft_skills.router,tags=["soft_skills"])

@app.get("/health", tags=["health"])
def health():
    datos_cargados = hasattr(state, "df_candidatos_hard") and hasattr(state, "df_candidatos_soft")
    if not datos_cargados:
        raise HTTPException(status_code=503, detail="Datos aún no cargados")
    return {
        "status": "ok",
        "candidatos_hard_skills": len(state.df_candidatos_hard),
        "candidatos_soft_skills": len(state.df_candidatos_soft),
    }