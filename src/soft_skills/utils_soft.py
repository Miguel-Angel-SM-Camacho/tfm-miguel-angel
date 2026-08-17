import pandas as pd
import numpy as np
import requests
from src.soft_skills import config 

def limpieza_soft_skills_2019(df):

    """Realiza la limpieza técnica y el tratamiento de outliers para el dataset del año 2019.
    Un cambio importante es que la deduplicación real ya se realiza antes de este punto, sobre el dataset completo
    para evitar falsos positivos por coincidencia de NaNs."""

    df_clean = df.copy() 
    
    # 1. Tratamiento de variables numéricas y creación de flags de nulos
    num_cols = ['WorkWeekHrs', 'CodeRevHrs']
    for col in num_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
            df_clean[f'{col}_is_missing'] = df_clean[col].isna().astype(int)
            
    # Clipping de outliers
    if 'WorkWeekHrs' in df_clean.columns:
        df_clean['WorkWeekHrs'] = df_clean['WorkWeekHrs'].clip(lower=0, upper=80)
    if 'CodeRevHrs' in df_clean.columns:
        df_clean['CodeRevHrs'] = df_clean['CodeRevHrs'].clip(lower=0, upper=24)

    # Columnas que dependen de tener un empleo
    labor_cols = [
        'CareerSat', 'JobSat', 'MgrIdiot', 'MgrWant', 'WorkPlan', 
        'WorkChallenge', 'WorkRemote', 'WorkLoc', 'CodeRev', 
        'PurchaseHow', 'PurchaseWhat', 'ImpSyn', 'JobFactors'
    ]
    
    # Columnas de personalidad
    personal_cols = [
        'Hobbyist', 'OpenSourcer', 'Employment', 'JobSeek', 
        'LastHireDate', 'ResumeUpdate', 'BetterLife', 'SocialMedia', 
        'Extraversion', 'SOVisitTo', 'SOPartFreq', 'WelcomeChange'
    ]
    
    for col in labor_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna('Not Applicable')
            
    for col in personal_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna('Not Provided')

    for col in df_clean.select_dtypes(include=['object']).columns:
        df_clean[col] = df_clean[col].astype('category')  
    return df_clean

def clasificar_trabajo_en_remoto(df):
    """Crea WorkRemote_Pct (numérica, para distancias) y WorkRemote_Bucket, la cual
    es categórica y se alinea a los umbrales del documento de reglas de Aurora)."""
    
    df = df.copy()
    df['WorkRemote_Pct'] = df['WorkRemote'].map(config.MAPEO_REMOTE_PCT)

    def bucket(row):
        texto = row['WorkRemote']
        if texto == 'Not Applicable':
            return 'Desconocido (Sin datos)'
        elif texto == "It's complicated":
            return 'Variable / Sin patrón fijo'
        pct = row['WorkRemote_Pct']
        if pd.isna(pct):
            return 'Desconocido (Sin datos)'
        elif pct >= 70:
            return 'Remoto Alto (>70%)'
        elif pct >= 30:
            return 'Rem. Parcial (30-70%)'
        else:
            return 'Presencial / Bajo remoto (<30%)'

    df['WorkRemote_Bucket'] = df.apply(bucket, axis=1)
    return df

def _normalizar_workweek(horas):
    """Normalizamos WorkWeekHrs a escala 0-1 entre 35h (0.0) y 80h (1.0)."""
    if pd.isna(horas):
        return np.nan
    return np.clip((horas - 35) / (80 - 35), 0, 1)

def _normalizar_opensourcer(valor):
    """Normalizamos OPENSOURCER_MAPPING (escala 1-4) a 0-1."""
    val = config.OPENSOURCER_MAPPING.get(valor, np.nan)
    if pd.isna(val):
        return np.nan
    return (val - 1) / 3

def calcular_proxies_bigfive(df):
    """Calcula scores continuos (0-1) y buckets categóricos (cortes fijos, calibrados
    por variable según su distribución observada) para Neuroticismo, Amabilidad y Apertura,
    como proxies conductuales de Big Five."""

    df = df.copy()

    # --- Neuroticismo ---
    s_imp = df['ImpSyn'].map(config.IMPSYN_SCORE)
    s_jobsat = df['JobSat'].map(config.SATISFACCION_SCORE)
    s_careersat = df['CareerSat'].map(config.SATISFACCION_SCORE)
    s_horas = df['WorkWeekHrs'].apply(_normalizar_workweek)
    df['Neuroticismo_Score'] = pd.concat([s_imp, s_jobsat, s_careersat, s_horas], axis=1).mean(axis=1, skipna=True)

    # --- Amabilidad ---
    s_welcome = df['WelcomeChange'].map(config.WELCOME_SCORE)
    s_coderev = df['CodeRev'].map(config.CODEREV_SCORE)
    s_mgr = df['MgrIdiot'].map(config.MGRIDIOT_SCORE)
    df['Amabilidad_Score'] = pd.concat([s_welcome, s_coderev, s_mgr], axis=1).mean(axis=1, skipna=True)

    # --- Apertura a la experiencia ---
    s_hobby = df['Hobbyist'].map(config.HOBBYIST_SCORE)
    s_opensource = df['OpenSourcer'].apply(_normalizar_opensourcer)
    s_betterlife = df['BetterLife'].map(config.BETTERLIFE_SCORE)
    df['Apertura_Score'] = pd.concat([s_hobby, s_opensource, s_betterlife], axis=1).mean(axis=1, skipna=True)

    # --- Buckets categóricos con cortes fijos, calibrados por rasgo ---
    for rasgo in ['Neuroticismo', 'Amabilidad', 'Apertura']:
        col_score = f'{rasgo}_Score'
        col_bucket = f'{rasgo}_Nivel'
        cortes = config.CORTES_BIGFIVE[rasgo]
        df[col_bucket] = df[col_score].apply(lambda x, c=cortes: _bucket_fijo(x, c))

    return df


def _bucket_fijo(score, cortes):
    """Clasifica un score 0-1 en Bajo/Medio/Alto usando cortes semánticos fijos."""
    if pd.isna(score):
        return 'Desconocido'
    elif score < cortes['bajo']:
        return 'Bajo'
    elif score <= cortes['alto']:
        return 'Medio'
    else:
        return 'Alto'

def codificar_multilabel(df, col, top_n=20, sep=';'):
    """Parsea una columna de texto multi-valor (separado por `sep`) y crea columnas 
    binarias [0,1] para las top_n categorías más frecuentes. Elimina la columna original."""
    df = df.copy()
    listas = df[col].fillna('').apply(lambda x: [v.strip() for v in x.split(sep) if v.strip()])
    top_valores = listas.explode().value_counts().head(top_n).index.tolist()
    for valor in top_valores:
        df[f"{col}_{valor}"] = listas.apply(lambda lst: int(valor in lst))
    return df.drop(columns=[col])

