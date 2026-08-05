import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DATA_PATH_2019 = os.path.join(BASE_DIR, 'data','raw', 'results_2019.csv')
PROCESSED_EDA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'survey_cleaned_eda.csv')
MODEL_MATRIX_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'matriz_autoencoder.csv')
PAISES_MAPA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'maestro_paises_mapa.csv')

OPENSOURCER_MAPPING = {
    'Never': 1, 
    'Less than once per year': 2,
    'Less than once a month but more than once per year': 3, 
    'Once a month or more often': 4
}

SATISFACCION_MAPPING = {
    'Very satisfied': 'Satisfecho',
    'Slightly satisfied': 'Satisfecho',
    'Neither satisfied nor dissatisfied': 'Neutral',
    'Slightly dissatisfied': 'Insatisfecho',
    'Very dissatisfied': 'Insatisfecho'
}

IDIOT_MAPPING = {
    'Very confident': 'Very confident',
    'Somewhat confident': 'Somewhat confident',
    'Not at all confident': 'Not at all confident'
}

WANT_MAPPING = {
    'Yes': 'Yes',
    'Not sure': 'Not sure',
    'No': 'No'
}

INFLUENCIA_MAPPING = {
    'I have little or no influence': 'I have little or no influence',
    'I have some influence': 'I have some influence',
    'I have a great deal of influence': 'I have a great deal of influence'
}

ORDEN_HIRE = ['Less than a year ago', '1-2 years ago', '3-4 years ago', 'More than 4 years ago']

MAPEO_SEEK = {
    'I am actively looking for a job': 'Búsqueda Activa',
    'I’m not actively looking, but I am open to new opportunities': 'Pasivo (Abierto a ofertas)',
    'I am not interested in new job opportunities': 'Cerrado a ofertas'
}

MAPEO_RESUME_UPDATE = {
    'I heard about a job opportunity (from a recruiter, online job posting, etc.)': 'Contacto de Recruiter u Oferta Online',
    'I had a negative experience or interaction at work': 'Experiencia negativa en el trabajo',
    'My job status changed (promotion, new job, etc.)': 'Cambio de estatus (ascenso, nuevo rol)',
    'I was preparing for a job search': 'Preparando búsqueda de empleo'
}

MAPEO_FACTORES = {
    "Languages, frameworks, and other technologies I'd be working with": "Tecnologías y frameworks a utilizar",
    "Office environment or company culture": "Cultura de empresa y buen ambiente",
    "Flex time or a flexible schedule": "Horario flexible",
    "Opportunities for professional development": "Crecimiento profesional",
    "Remote work options": "Opciones de trabajo en remoto",
    "How widely used or impactful my work output would be": "Impacto real de mi trabajo",
    "Financial performance or funding status of the company or organization": "Solidez financiera",
    "Industry that I'd be working in": "Sector o industria",
    "Specific department or team I'd be working on": "Equipo o departamento específico",
    "Diversity of the company or organization": "Diversidad e inclusión"
}

MAPEO_PLAN = {
    'There is a schedule and/or spec (made by me or by a colleague), and I follow it very closely': 'Estricto (Sigue el plan)',
    'There is a schedule and/or spec (made by me or by a colleague), and my work somewhat aligns': 'Flexible (Alineado al plan)',
    'There is no schedule or spec; I work on what seems most important or urgent': 'Caos (Apaga fuegos)'
}

MAPEO_LOC = {
    'Office': 'Oficina',
    'Home': 'Casa',
    'Other place, such as a coworking space or cafe': 'Coworking / Café'
}

MAPEO_RETOS = {
    'Distracting work environment': 'Entorno con distracciones',
    'Meetings': 'Exceso de reuniones',
    'Being tasked with non-development work': 'Tareas no relacionadas con programación',
    'Toxic work environment': 'Entorno laboral tóxico',
    'Inadequate access to necessary tools': 'Falta de herramientas adecuadas',
    'Lack of support from management': 'Falta de apoyo de los mánagers',
    'Non-work commitments (parenting, school work, hobbies, etc.)': 'Compromisos personales'
}

MAPEO_IMP = {
    'Far above average': '1. Muy por encima de la media',
    'A little above average': '2. Ligeramente por encima',
    'Average': '3. En la media',
    'A little below average': '4. Ligeramente por debajo',
    'Far below average': '5. Muy por debajo (Impostor)'
}

MAPEO_REV = {
    'Yes, because I see value in it': 'Sí, le veo gran valor',
    'Yes, because I was told to do it': 'Sí, por pura obligación',
    'No': 'No reviso código'
}

MAPEO_EXTRA = {
    'In real life (in person)': 'Cara a cara (Presencial)',
    'Online': 'En línea (Digital)'
}

MAPEO_VIDA = {
    'Yes': 'Optimista (Sí mejora)',
    'No': 'Escéptico (No mejora)'
}

MAPEO_WELCOME = {
    'A lot more welcome now than last year': 'Me siento más integrado',
    'Somewhat more welcome now than last year': 'Me siento más integrado',
    'Just as welcome now as I felt last year': 'Igual que siempre (Estable)',
    'Somewhat less welcome now than last year': 'Me siento menos integrado',
    'A lot less welcome now than last year': 'Me siento menos integrado',
    'Not applicable - I did not use Stack Overflow last year': 'Nuevo en la comunidad'
}

MAPEO_SOPART = {
    'I have never participated in Q&A on Stack Overflow': 'Nunca participo (Solo leo)',
    'Less than once per month or monthly': 'Mensualmente',
    'A few times per month or weekly': 'Semanalmente',
    'A few times per week': 'Varias veces por semana',
    'Daily or almost daily': 'A diario (Evangelizador)'
}