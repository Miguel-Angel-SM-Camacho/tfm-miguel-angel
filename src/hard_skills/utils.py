import pandas as pd
import numpy as np
import requests
from src.hard_skills import config 
import pytz


def limpieza_datos(df):
    """
    Realiza la limpieza técnica implementando 'Missing Indicators' para numéricas,
    tratamiento especial para salario y mapeo de categóricas.
    """
    df_clean = df.copy()

    for col in config.NUM_COLS:
        if col in df_clean.columns:
            df_clean[f'{col}_is_missing'] = df_clean[col].isna().astype(int)
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

    if 'ConvertedCompYearly' in df_clean.columns:
        df_clean['ConvertedCompYearly_is_missing'] = df_clean['ConvertedCompYearly'].isna().astype(int)
        df_clean['ConvertedCompYearly'] = pd.to_numeric(df_clean['ConvertedCompYearly'], errors='coerce')
        mediana_salarial = df_clean[df_clean['ConvertedCompYearly'] > 0]['ConvertedCompYearly'].median()
        df_clean['ConvertedCompYearly'] = df_clean['ConvertedCompYearly'].replace(0, np.nan)
        df_clean['ConvertedCompYearly'] = df_clean['ConvertedCompYearly'].fillna(mediana_salarial)
        df_clean['ConvertedCompYearly'] = df_clean['ConvertedCompYearly'].clip(lower=10000, upper=300000)

    if 'YearsCode' in df_clean.columns:
        df_clean = df_clean[df_clean['YearsCode'].isna() | (df_clean['YearsCode'] <= 65)]
    if 'WorkExp' in df_clean.columns:
        df_clean = df_clean[df_clean['WorkExp'].isna() | (df_clean['WorkExp'] <= 65)]

    for col, mapeo in [
        ('EdLevel', config.ED_LEVEL_MAPPING),
        ('RemoteWork', config.MAPEO_MODALIDADES),
        ('OrgSize', config.ORG_SIZE_MAPPING),
        ('Industry', config.INDUSTRY_MAPPING),
    ]:
        if col in df_clean.columns:
            df_clean[f'{col}_is_missing'] = df_clean[col].isna().astype(int)
            df_clean[col] = df_clean[col].map(mapeo).astype('Int64')  # Int64 (nullable) admite NaN

    all_text_cols = config.TECH_COLS + config.CAT_COLS_TEXT
    for col in all_text_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna('None')
            
    return df_clean

def codificar_multilabel(df, col, top_n=20, sep=';'):
    """
    Convierte una columna de elementos separados por `sep` en múltiples columnas binarias.
    Solo mantiene las 'top_n' categorías más frecuentes para evitar ruido/explosión dimensional.
    """
    df = df.copy()
    listas = df[col].fillna('').apply(
        lambda x: [v.strip() for v in x.split(sep) if v.strip() and v.strip().lower() != 'none']
    )
    top_valores = listas.explode().value_counts().head(top_n).index.tolist()
    for valor in top_valores:
        df[f"{col}_{valor}"] = listas.apply(lambda lst: int(valor in lst))
    return df.drop(columns=[col])

def datos_geografia(paises_serie):
    """
    Se conecta a una API externa para mapear países a continentes, idiomas y zonas horarias 
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

        cca2 = c.get('cca2', '')
        zonas_pais = pytz.country_timezones.get(cca2, [])

        info = {
            'Idiomas_Oficiales': ", ".join(c.get('languages', {}).values()),
            'Zonas_Horarias': ", ".join(zonas_pais) if zonas_pais else 'UTC',
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
        maestro_list.append({'Pais_Original': pais, **info_pais})

    df_maestro = pd.DataFrame(maestro_list)
    df_maestro.to_csv(config.PAISES_MAPA_PATH, index=False, sep=';', encoding='utf-8-sig')
    
    print(f"CSV de países guardado en: {config.PAISES_MAPA_PATH}")
    return df_maestro