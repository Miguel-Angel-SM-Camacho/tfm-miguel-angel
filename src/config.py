import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_PATH_2019 = os.path.join(BASE_DIR, 'data', 'raw', 'results_2019.csv')
RAW_DATA_PATH_2025 = os.path.join(BASE_DIR, 'data', 'raw', 'results_2025.csv')
PROCESSED_EDA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'survey_cleaned_eda.csv')
MODEL_MATRIX_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'matriz_autoencoder.csv')
PAISES_MAPA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'maestro_paises_mapa.csv')

NUM_COLS = ['WorkExp', 'YearsCode', 'ToolCountWork', 'JobSat']
CAT_COLS_TEXT = ['ICorPM', 'Country', 'Employment', 'DevType']
CAT_COLS_MAPPED = ['EdLevel', 'RemoteWork', 'OrgSize', 'Industry']
TECH_COLS = [
    'LanguageHaveWorkedWith', 'DatabaseHaveWorkedWith', 
    'PlatformHaveWorkedWith', 'WebframeHaveWorkedWith', 
    'DevEnvsHaveWorkedWith', 'CommPlatformHaveWorkedWith', 
    'OfficeStackAsyncHaveWorkedWith', 'OpSysProfessional use', 
    'AIModelsHaveWorkedWith'
]

ED_LEVEL_MAPPING = {
    'Primary/elementary school': 1,
    'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)': 2,
    'Some college/university study without earning a degree': 3,
    'Associate degree (A.A., A.S., etc.)': 4,
    'Bachelor’s degree (B.A., B.S., B.Eng., etc.)': 5,
    'Master’s degree (M.A., M.S., M.Eng., MBA, etc.)': 6,
    'Professional degree (JD, MD, Ph.D, Ed.D, etc.)': 7,
    'Other (please specify):': 0
}

MAPEO_MODALIDADES = {
    'Full in-person': 1,
    'In-person': 1,
    'Hybrid (some in-person, leans heavy to in-person)': 2,
    'Hybrid (some in-person, leans heavy to neither)': 3,
    'Hybrid (some remote, some in-person)': 3,
    'Hybrid (some in-person, leans heavy to flexibility)': 4,
    'Remote': 5,
    'Fully remote': 5
}

TRADUCCIONES = {
    'United States of America': 'United States',
    'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom',
    'Russian Federation': 'Russia',
    'Turkey': 'Turkey', 
    'Czech Republic': 'Czechia',
    'Viet Nam': 'Vietnam',
    'Hong Kong (S.A.R.)': 'Hong Kong',
    'Republic of Korea': 'South Korea',
    'Iran, Islamic Republic of...': 'Iran',
    'Venezuela, Bolivarian Republic of...': 'Venezuela',
    'Republic of Moldova': 'Moldova',
    'Republic of North Macedonia': 'North Macedonia',
    'Taiwan': 'Taiwan'
}

ORG_SIZE_MAPPING = {
    'Just me - I am a freelancer, sole proprietor, etc.': 1,
    'Less than 20 employees': 2,
    '20 to 99 employees': 3,
    '100 to 499 employees': 4,
    '500 to 999 employees': 5,
    '1,000 to 4,999 employees': 6,
    '5,000 to 9,999 employees': 7,
    '10,000 or more employees': 8,
    'I don’t know': 0,
    'None': 0
}

INDUSTRY_MAPPING = {
    'Software Development': 1,
    'Computer Systems Design and Services': 1,
    'Internet, Telecomm or Information Services': 2,
    'Banking/Financial Services': 3,
    'Fintech': 3,
    'Insurance': 3,
    'Healthcare': 4,
    'Manufacturing': 5,
    'Government': 6,
    'Retail and Consumer Services': 7,
    'Higher Education': 8,
    'Energy': 9,
    'Transportation, or Supply Chain': 10,
    'Media & Advertising Services': 11,
    'Other:': 0,
    'None': 0
}