import json
from contextlib import asynccontextmanager
import pandas as pd
from fastapi import FastAPI
from src.hard_skills import config as config_hard_skills
from src.soft_skills import config as config_soft_skills
from src.soft_skills import modelo_aux_soft

class AppState:
    pass

state = AppState()

@asynccontextmanager
async def lifespan(app: FastAPI):
    with open(config_hard_skills.REGLAS_EXPERTAS_PATH, encoding='utf-8') as f:
        reglas_expertas = json.load(f)['reglas']
    state.reglas_soft_proyecto = [r for r in reglas_expertas if r['tipo'] == 'soft_parcial']

    state.df_candidatos_hard = pd.read_csv(config_hard_skills.MATRIZ_TRANSACCIONAL_PATH, index_col='CandidateId').fillna(0).astype(int)
    state.df_candidatos_soft = pd.read_csv(config_soft_skills.MATRIZ_TRANSACCIONAL_PATH, index_col='CandidateId').fillna(0).astype(int)

    paises_mapa = pd.read_csv(config_hard_skills.PAISES_MAPA_PATH, sep=';')
    state.paises_mapa = paises_mapa

    df_geo_hard = pd.read_csv(config_hard_skills.PROCESSED_EDA_PATH, index_col='CandidateId', usecols=['CandidateId', 'Country', 'Continente'])
    state.df_geo_hard = df_geo_hard.reset_index().merge(paises_mapa[['Pais_Original', 'Idiomas_Oficiales']], left_on='Country', right_on='Pais_Original', how='left').set_index('CandidateId')

    reglas_limpias_hard = pd.read_csv(config_hard_skills.REGLAS_LIMPIAS_PATH)
    reglas_limpias_hard['items_totales'] = reglas_limpias_hard.apply(lambda row: set(str(row['antecedents']).split(' | ')) | set(str(row['consequents']).split(' | ')), axis=1)
    state.reglas_limpias_hard = reglas_limpias_hard

    reglas_limpias_soft = pd.read_csv(config_soft_skills.REGLAS_LIMPIAS_PATH)
    reglas_limpias_soft['items_totales'] = reglas_limpias_soft.apply(lambda row: set(str(row['antecedents']).split(' | ')) | set(str(row['consequents']).split(' | ')), axis=1)
    state.reglas_limpias_soft = reglas_limpias_soft

    state.evidencia_reglas_soft = {
        regla['id']: {
            'riesgo': regla['riesgo'],
            **modelo_aux_soft.obtener_evidencias_reglas_soft(regla, reglas_limpias_soft, state.df_candidatos_soft),
        }
        for regla in state.reglas_soft_proyecto
    }

    yield
    state.__dict__.clear()      