import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DATA_PATH_2025 = os.path.join(BASE_DIR, 'data','raw', 'results_2025.csv')
PROCESSED_EDA_PATH = os.path.join(BASE_DIR, 'data', 'processed/hard_skills', 'survey_cleaned_eda_hard.csv')
MODEL_MATRIX_PATH = os.path.join(BASE_DIR, 'data', 'processed/hard_skills', 'matriz_autoencoder.csv')
PROYECTOS_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'proyectos_prueba.json')
PAISES_MAPA_PATH = os.path.join(BASE_DIR, 'data', 'processed/hard_skills', 'maestro_paises_mapa.csv')
MATRIZ_TRANSACCIONAL_PATH = os.path.join(BASE_DIR, 'data', 'processed/hard_skills', 'matriz_transaccional_hard.csv')
REGLAS_APRIORI_PATH = os.path.join(BASE_DIR, 'data', 'processed/hard_skills', 'reglas_apriori_hard.csv')
REGLAS_LIMPIAS_PATH = os.path.join(BASE_DIR, 'data', 'processed/hard_skills', 'reglas_limpias_hard.csv')
REGLAS_EXPERTAS_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'reglas_expertas_riesgo.json')

NUM_COLS = ['WorkExp', 'YearsCode', 'ToolCountWork', 'JobSat']
CAT_COLS_TEXT = ['ICorPM', 'Country', 'Employment']
CAT_COLS_MAPPED = ['EdLevel', 'RemoteWork', 'OrgSize', 'Industry']
TECH_COLS = [
    'LanguageHaveWorkedWith', 'DatabaseHaveWorkedWith', 
    'PlatformHaveWorkedWith', 'WebframeHaveWorkedWith', 
    'DevEnvsHaveWorkedWith', 'CommPlatformHaveWorkedWith', 
    'OfficeStackAsyncHaveWorkedWith', 'OpSysProfessional use', 
    'AIModelsHaveWorkedWith'
]

INDUSTRY_CODE_DETALLE_MAPPING = {
    1: 'Industry_Software Development',
    2: 'Industry_Internet, Telecomm or Information Services',
    3: 'Industry_Banking/Financial Services',
    4: 'Industry_Healthcare',
    5: 'Industry_Manufacturing',
    6: 'Industry_Government',
    7: 'Industry_Retail and Consumer Services',
    8: 'Industry_Higher Education',
    9: 'Industry_Energy',
    10: 'Industry_Transportation, or Supply Chain',
    11: 'Industry_Media & Advertising Services',
}

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
    'Turkey': 'Türkiye',
    'Libyan Arab Jamahiriya': 'Libya',
    'Congo, Republic of the...': 'Congo',
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

MAPEO_TECNOLOGIAS = {
    'Python': 'LanguageHaveWorkedWith_Python', 'SQL': 'LanguageHaveWorkedWith_SQL',
    'JavaScript': 'LanguageHaveWorkedWith_JavaScript', 'TypeScript': 'LanguageHaveWorkedWith_TypeScript',
    'Java': 'LanguageHaveWorkedWith_Java', 'C++': 'LanguageHaveWorkedWith_C++',
    'C': 'LanguageHaveWorkedWith_C', 'C#': 'LanguageHaveWorkedWith_C#',
    'Go': 'LanguageHaveWorkedWith_Go', 'Rust': 'LanguageHaveWorkedWith_Rust',
    'PHP': 'LanguageHaveWorkedWith_PHP', 'Ruby': 'LanguageHaveWorkedWith_Ruby',
    'Swift': 'LanguageHaveWorkedWith_Swift', 'Kotlin': 'LanguageHaveWorkedWith_Kotlin',
    'CSS': 'LanguageHaveWorkedWith_HTML/CSS',
    'React': 'WebframeHaveWorkedWith_React', 'Node.js': 'WebframeHaveWorkedWith_Node.js',
    'Angular': 'WebframeHaveWorkedWith_Angular', 'Vue.js': 'WebframeHaveWorkedWith_Vue.js',
    'Django': 'WebframeHaveWorkedWith_Django', 'Flask': 'WebframeHaveWorkedWith_Flask',
    'FastAPI': 'WebframeHaveWorkedWith_FastAPI', 'Spring Boot': 'WebframeHaveWorkedWith_Spring Boot',
    'Laravel': 'WebframeHaveWorkedWith_Laravel', 'Express': 'WebframeHaveWorkedWith_Express',
    'PostgreSQL': 'DatabaseHaveWorkedWith_PostgreSQL', 'MySQL': 'DatabaseHaveWorkedWith_MySQL',
    'MongoDB': 'DatabaseHaveWorkedWith_MongoDB', 'Redis': 'DatabaseHaveWorkedWith_Redis',
    'SQLite': 'DatabaseHaveWorkedWith_SQLite', 'MariaDB': 'DatabaseHaveWorkedWith_MariaDB',
    'Oracle': 'DatabaseHaveWorkedWith_Oracle',
    'Docker': 'PlatformHaveWorkedWith_Docker', 'Kubernetes': 'PlatformHaveWorkedWith_Kubernetes',
    'AWS': 'PlatformHaveWorkedWith_Amazon Web Services (AWS)',
    'Azure': 'PlatformHaveWorkedWith_Microsoft Azure', 'Google Cloud': 'PlatformHaveWorkedWith_Google Cloud',
    'Terraform': 'PlatformHaveWorkedWith_Terraform',
    'Linux': 'OpSysProfessional use_Linux (non-WSL)',
    'TensorFlow': None, 'PyTorch': None, 'Unreal Engine': None, 'MATLAB': None, 'Spark': None,
}

SENIORITY_PESOS = {
    'WorkExp_Bin_<5 (Junior)': 0.2,
    'WorkExp_Bin_5-9 (Semi-Senior o Mid)': 0.5,
    'WorkExp_Bin_10-18 (Senior)': 0.75,
    'WorkExp_Bin_>=19 (Muy Senior)': 0.95,
}

REMOTO_PESOS = {
    'RemoteWork_Fully remote': 1.0,
    'RemoteWork_Hybrid (some in-person, leans heavy to flexibility)': 0.5,
    'RemoteWork_In-person': 0.0,
}

EDLEVEL_MAPPING_PROYECTO = {
    'Bachelor': 'Bachelor’s degree (B.A., B.S., B.Eng., etc.)',
    'Master': 'Master’s degree (M.A., M.S., M.Eng., MBA, etc.)',
    'Professional': 'Professional degree (JD, MD, Ph.D, Ed.D, etc.)',
    'Associate': 'Associate degree (A.A., A.S., etc.)',
    'Secondary': 'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)',
    'SomeCollege': 'Some college/university study without earning a degree',
}

OS_MAPPING_PROYECTO = {
    'Linux': 'Linux (non-WSL)',
}

EMPLOYMENT_MAPPING_PROYECTO = {
    'Freelancer': 'Independent contractor, freelancer, or self-employed',
}

TOOLS_MEDIBLES = {'Jira', 'GitHub', 'GitLab', 'Confluence', 'Azure DevOps', 'Notion', 'Trello', 'Linear'}

TOOLS_MAPPING_PROYECTO = {
    'Azure DevOps': 'Azure Devops',
}

SALARY_PESOS = {
    'ConvertedCompYearly_Bin_<40k': 0.1,
    'ConvertedCompYearly_Bin_40-70k': 0.3,
    'ConvertedCompYearly_Bin_70-100k': 0.5,
    'ConvertedCompYearly_Bin_100-150k': 0.7,
    'ConvertedCompYearly_Bin_>150k': 0.9,
}

PESOS_DIMENSION = {
    'seniority': 2.5,
    'idioma_proyecto': 2.5,
    'role_title': 2.0,
    'localizacion_proyecto': 2.0,
    'remote_work_pct': 1.5,
    'industry': 1.0,
    'management_level': 1.0,
    'education': 1.0,
    'os': 1.0,
    'employment_type': 1.0,
    'tools_used': 1.0,
    'salary_budget': 1.0,
    'ide_preferred': 0.5,
    'ai_tools_preferred': 0.5,
    'company_size': 0.5,
}
PESO_TECH_DEFAULT = 3.0  # cualquier dimensión no listada arriba es un ítem del stack técnico exigido

ETIQUETAS_DIMENSION = {
    'seniority': 'Nivel de seniority', 'remote_work_pct': '% Teletrabajo',
    'industry': 'Industria', 'role_title': 'Rol / puesto',
    'idioma_proyecto': 'Idioma del proyecto', 'localizacion_proyecto': 'Localización',
    'management_level': 'Nivel de gestión', 'education': 'Formación',
    'os': 'Sistema operativo', 'employment_type': 'Tipo de contrato',
    'tools_used': 'Herramientas de trabajo', 'ide_preferred': 'IDE preferido',
    'ai_tools_preferred': 'Herramientas de IA', 'salary_budget': 'Presupuesto salarial',
    'company_size': 'Tamaño de empresa',
}
DIMENSIONES_UMBRAL = {'seniority', 'remote_work_pct', 'salary_budget', 'tools_used'}