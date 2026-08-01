import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DATA_PATH_2019 = os.path.join(BASE_DIR, 'data','raw', 'results_2019.csv')
PROCESSED_EDA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'survey_cleaned_eda.csv')
MODEL_MATRIX_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'matriz_autoencoder.csv')
PAISES_MAPA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'maestro_paises_mapa.csv')

#NUM_COLS = ['WorkExp', 'YearsCode', 'ToolCountWork', 'JobSat']
#CAT_COLS_TEXT = ['ICorPM', 'Country', 'Employment', 'DevType']