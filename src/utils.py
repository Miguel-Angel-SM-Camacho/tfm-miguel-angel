import pandas as pd
import numpy as np
import requests
from src import config 

def limpieza_datos(df):
    """
    Realiza la limpieza técnica implementando 'Missing Indicators' para numéricas,
    tratamiento especial para salario y mapeo de categóricas.
    """
    df_clean = df.copy()
    
    df_clean = df_clean.drop_duplicates(keep='first')

    for col in config.NUM_COLS:
        if col in df_clean.columns:
            df_clean[f'{col}_is_missing'] = df_clean[col].isna().astype(int)
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0)

    if 'ConvertedCompYearly' in df_clean.columns:
        df_clean['ConvertedCompYearly_is_missing'] = df_clean['ConvertedCompYearly'].isna().astype(int)
        df_clean['ConvertedCompYearly'] = pd.to_numeric(df_clean['ConvertedCompYearly'], errors='coerce')
        
        mediana_salarial = df_clean[df_clean['ConvertedCompYearly'] > 0]['ConvertedCompYearly'].median()
        
        df_clean['ConvertedCompYearly'] = df_clean['ConvertedCompYearly'].replace(0, np.nan)
        df_clean['ConvertedCompYearly'] = df_clean['ConvertedCompYearly'].fillna(mediana_salarial)
        df_clean['ConvertedCompYearly'] = df_clean['ConvertedCompYearly'].clip(lower=10000, upper=300000)

    if 'YearsCode' in df_clean.columns:
        df_clean = df_clean[df_clean['YearsCode'] <= 65]
    if 'WorkExp' in df_clean.columns:
        df_clean = df_clean[df_clean['WorkExp'] <= 65]
    
    if 'EdLevel' in df_clean.columns:
        df_clean['EdLevel'] = df_clean['EdLevel'].map(config.ED_LEVEL_MAPPING).fillna(0).astype(int)
    if 'RemoteWork' in df_clean.columns:
        df_clean['RemoteWork'] = df_clean['RemoteWork'].map(config.MAPEO_MODALIDADES).fillna(0).astype(int)
    if 'OrgSize' in df_clean.columns:
        df_clean['OrgSize'] = df_clean['OrgSize'].map(config.ORG_SIZE_MAPPING).fillna(0).astype(int)
    if 'Industry' in df_clean.columns:
        df_clean['Industry'] = df_clean['Industry'].map(config.INDUSTRY_MAPPING).fillna(0).astype(int)

    all_text_cols = config.TECH_COLS + config.CAT_COLS_TEXT
    for col in all_text_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna('None')
            
    return df_clean

def limpieza_soft_skills_2019(df):
    
    """Realiza la limpieza técnica y el tratamiento de outliers para el dataset del año 2019. """
   
    df_clean = df.copy()
    df_clean = df_clean.drop_duplicates(keep='first')
    
    # Variables numéricas que requieren tratamiento especial
    num_cols = ['WorkWeekHrs', 'CodeRevHrs']
    
    for col in num_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
            df_clean[f'{col}_is_missing'] = df_clean[col].isna().astype(int)
            
    if 'WorkWeekHrs' in df_clean.columns:
        df_clean['WorkWeekHrs'] = df_clean['WorkWeekHrs'].clip(lower=0, upper=80)
    if 'CodeRevHrs' in df_clean.columns:
        df_clean['CodeRevHrs'] = df_clean['CodeRevHrs'].clip(lower=0, upper=24)

    if 'ConvertedComp' in df_clean.columns:
        df_clean['ConvertedComp_is_missing'] = df_clean['ConvertedComp'].isna().astype(int)
        df_clean['ConvertedComp'] = pd.to_numeric(df_clean['ConvertedComp'], errors='coerce')
        
        mediana_salarial = df_clean[df_clean['ConvertedComp'] > 0]['ConvertedComp'].median()
        
        df_clean['ConvertedComp'] = df_clean['ConvertedComp'].replace(0, np.nan)
        df_clean['ConvertedComp'] = df_clean['ConvertedComp'].fillna(mediana_salarial)
        df_clean['ConvertedComp'] = df_clean['ConvertedComp'].clip(lower=10000, upper=300000)

    # Variables categóricas que requieren mapeo
    all_text_cols = [
        'Hobbyist', 'OpenSourcer', 'Employment', 'CareerSat', 'JobSat', 
        'MgrIdiot', 'MgrWant', 'JobSeek', 'LastHireDate', 'ResumeUpdate', 
        'WorkPlan', 'WorkChallenge', 'WorkRemote', 'WorkLoc', 'CodeRev', 
        'PurchaseHow', 'PurchaseWhat', 'BetterLife', 'SocialMedia', 
        'Extraversion', 'SOVisitTo', 'SOPartFreq', 'WelcomeChange']
    
    for col in all_text_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna('Not Provided')
            
    return df_clean

def codificar_multilabel(df, col, top_n=20):
    """
    Convierte una columna de elementos separados por ';' en múltiples columnas binarias.
    Solo mantiene las 'top_n' tecnologías más frecuentes para evitar ruido.
    """
    dummies = df[col].str.get_dummies(sep=';')
    dummies = dummies.drop(columns=['None'], errors='ignore')
    top_tech = dummies.sum().nlargest(top_n).index
    dummies = dummies[top_tech].add_prefix(f"{col}_")
    return pd.concat([df.drop(columns=[col]), dummies], axis=1)

def datos_geografia(paises_serie):
    """
    Se conecta a una API externa para mapear países a continentes y zonas horarias.
    """
    unicos = [c for c in paises_serie.unique() if pd.notna(c) and str(c) not in ('nan', 'None', '')]

    url = "https://raw.githubusercontent.com/mledoze/countries/master/countries.json"
    try:
        data = requests.get(url, timeout=10).json()
    except Exception as e:
        print(f"Error al conectar con la API: {e}")
        return pd.DataFrame()

    lookup = {}
    for c in data:
        nombres = [c.get('name', {}).get('common'), c.get('name', {}).get('official'), c.get('cca2'), c.get('cca3')]
        if 'translations' in c:
            for t in c['translations'].values():
                nombres.extend([t.get('common'), t.get('official')])

        info = {
            'Idiomas_Oficiales': ", ".join(c.get('languages', {}).values()),
            'Zonas_Horarias': ", ".join(c.get('timezones', [])) if isinstance(c.get('timezones', []), list) else str(c.get('timezones', '')),
            'Continente': c.get('region', 'Other'),
            'Region': c.get('subregion', 'Other'),
            'Coordenadas': f"{c.get('latlng', [0.0, 0.0])[0]}, {c.get('latlng', [0.0, 0.0])[1]}"
        }

        for n in filter(None, nombres):
            lookup[str(n).lower()] = info

    fallback = {
        'Idiomas_Oficiales': 'English', 'Zonas_Horarias': 'UTC',
        'Continente': 'Other', 'Region': 'Other', 'Coordenadas': '0.0, 0.0'
    }

    maestro_list = []
    for pais in unicos:
        nombre_buscar = config.TRADUCCIONES.get(pais, pais).lower()
        
        info_pais = lookup.get(nombre_buscar, fallback)
        
        maestro_list.append({
            'Pais_Original': pais,
            **info_pais
        })

    df_maestro = pd.DataFrame(maestro_list)
    df_maestro.to_csv(config.PAISES_MAPA_PATH, index=False, sep=';', encoding='utf-8-sig')
    
    print(f"CSV de países guardado en: {config.PAISES_MAPA_PATH}")
    return df_maestro