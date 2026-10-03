from typing import List, Optional
from pydantic import BaseModel, Field

class ProyectoInput(BaseModel):
    # Datos obligatorios de las hard skills
    project_id: str
    role_title: str
    industry: str
    tech_stack_required: List[str]
    seniority_threshold: float = Field(..., ge=0, le=1)
    remote_work_pct: float = Field(..., ge=0, le=100)

    # Datos opcionales de las hard skills
    company_name: Optional[str] = None
    seniority_required: Optional[str] = None
    industry_survey_key: Optional[str] = None
    role_devtype_keys: Optional[List[str]] = None
    common_project_language: Optional[str] = None
    countries_involved: Optional[List[str]] = None
    management_level_required: Optional[str] = None
    education_required: Optional[str] = None
    os_required: Optional[str] = None
    employment_type_required: Optional[str] = None
    tools_used: Optional[List[str]] = None
    ide_preferred: Optional[str] = None
    ai_tools_preferred: Optional[List[str]] = None
    salary_budget_usd: Optional[float] = None
    company_size_category: Optional[str] = None

    # Datos opcionales de las soft skills
    concurrent_projects_per_member: Optional[int] = None
    timezone_overlap_hours: Optional[float] = None
    has_annual_inperson_meeting: Optional[bool] = None
    has_prior_team_experience: Optional[bool] = None
    has_team_building_activities: Optional[bool] = None
    multiple_teams_involved: Optional[bool] = None
    disconnection_policy: Optional[bool] = None
    project_complexity: Optional[str] = None
    meetings_per_week: Optional[int] = None
    deadline_tightness: Optional[str] = None

class CandidatoHardOut(BaseModel):
    candidate_id: int
    nivel_match_pct: float
    distancia_manhattan: float
    similitud_coseno_pct: float
    ubicacion: str
    idiomas: str
    cumple: List[str]
    no_cumple: List[str]
    lift_evidencia_mineria: Optional[float] = None
    n_items_evaluados_evidencia: Optional[int] = None

class RankingHardSkillsOut(BaseModel):
    project_id: str
    dimensiones_evaluadas: List[str]
    no_medibles: List[str]
    candidatos: List[CandidatoHardOut]

class RiesgoActivoOut(BaseModel):
    id_regla: int
    riesgo: str
    items_activados: List[str]
    mitigacion: str
    peso_evidencia: float

class CandidatoSoftOut(BaseModel):
    candidate_id: int
    score_riesgo: float
    n_riesgos_unicos: int
    n_riesgos_activados: int
    indice_compromiso: float
    riesgos_activados: List[RiesgoActivoOut]

class ReglaActivaOut(BaseModel):
    id: int
    riesgo: str
    condicion_texto: str

class RankingSoftSkillsOut(BaseModel):
    project_id: Optional[str] = None
    reglas_activas: List[ReglaActivaOut]
    total_reglas_soft: int
    candidatos_con_riesgo_aceptable: int
    candidatos: List[CandidatoSoftOut]