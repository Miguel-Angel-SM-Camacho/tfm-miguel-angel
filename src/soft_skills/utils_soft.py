import pandas as pd
import numpy as np
import requests
from src.soft_skills import config 

def limpieza_soft_skills_2019(df):

    """Realiza la limpieza técnica y el tratamiento de outliers para el dataset del año 2019."""

    df_clean = df.copy()
    df_clean = df_clean.drop_duplicates(keep='first')
    
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
        'PurchaseHow', 'PurchaseWhat'
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