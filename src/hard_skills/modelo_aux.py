import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
#  Funciones auxiliares mapeo de requisitos del proyecto
# ---------------------------------------------------------------------------

def mapeo_proyecto(tech_stack_req, mapeo):
    "Tiene como bojetivo traducir el stack tecnológico que requiere el proyecto"
    "a columnas de la matriz de candidatos"
    col_mendibles = [mapeo[t] for t in tech_stack_req if mapeo.get(t)]
    no_medibles = [t for t in tech_stack_req if not mapeo.get(t)]
    return col_mendibles, no_medibles

def calculo_score_ponderado(df,pesos):
    "Combina un conjunto de columnas binarias y sus pesos en una única puntuación o score"
    col = list(pesos.keys())
    valores = np.array(list(pesos.values()))
    return df[col].values @  valores

def detalle_industria(proyecto, config_hard_skills):
    "Obtiene el detalle de la industria a partir del proyecto y el mapeo en el config.py de las hard skills"
    key_encuesta = proyecto.get('industry_survey_key')
    resultado = None
    if key_encuesta:
        codigo_industria = config_hard_skills.INDUSTRY_MAPPING.get(key_encuesta)
        if codigo_industria:
            resultado = config_hard_skills.INDUSTRY_CODE_DETALLE_MAPPING.get(codigo_industria)
    return resultado

def obtener_roles(proyecto):
    "Obtiene los roles de los desarrolladores a partir del proyecto"
    keys_roles = proyecto.get('role_devtype_keys')
    resultado = None
    if keys_roles:
        resultado = [f'DevType_{key}' for key in keys_roles]
    return resultado

def detalle_manager(proyecto):
    "Obtiene el detalle del nivel de gestión a partir del proyecto"
    val = proyecto.get('management_level_required')
    return f'ICorPM_{val}' if val else None

def detalle_educacion(proyecto, config_hard_skills):
    "Obtiene el detalle de la educación requerida a partir del proyecto y el mapeo en el config.py de las hard skills"
    key = proyecto.get('education_required')
    resultado = None
    if key:
        sufijo = config_hard_skills.EDLEVEL_MAPPING_PROYECTO.get(key)
        if sufijo:
            resultado = f'EdLevel_{sufijo}'
    return resultado

def detalle_ssoo(proyecto, config_hard_skills):
    "Obtiene el detalle del ssoo requerido a partir del proyecto y el mapeo del config.py hard skills"
    key_ssoo = proyecto.get('os_required')
    resultado = None
    if key_ssoo:
        key_final = config_hard_skills.OS_MAPPING.get(key_ssoo, key_ssoo)
        resultado = f'OpSysProfessional use_{key_final}'
    return resultado

def detalle_empleo(proyecto, config_hard_skills):
    key_empleo = proyecto.get('employment_type_required')
    resultado = None
    if key_empleo:
        key_final = config_hard_skills.EMPLOYMENT_MAPPING_PROYECTO.get(key_empleo, key_empleo)
        resultado = f'Employment_{key_final}'
    return resultado

def mapeo_herramientas_conocidas(tools_used, medibles, mapeo):
    "Realiza el mapeo de las herramientas conocidas por el candidato a las columnas de la matriz de candidatos"
    col_medibles = [f'OfficeStackAsyncHaveWorkedWith_{mapeo.get(t, t)}' for t in tools_used if t in medibles]
    col_nomedibles = [t for t in tools_used if t not in medibles]
    return col_medibles, col_nomedibles

def detalle_ide(proyecto):
    "Obtiene el detalle del IDE preferido a partir del proyecto"
    val = proyecto.get('ide_preferred')
    return f'DevEnvsHaveWorkedWith_{val}' if val else None


def obtener_ai_tools(proyecto):
    "Obtiene el detalle de las herramientas de IA preferidas a partir del proyecto"
    values = proyecto.get('ai_tools_preferred')
    resultado = None
    if values:
        resultado = [f'AIModelsHaveWorkedWith_{v}' for v in values]
    return resultado

def detalle_company_size(proyecto):
    "Obtiene el detalle del tamaño de la empresa a partir del proyecto"
    val = proyecto.get('company_size_category')
    return f'OrgSize_{val}' if val else None

def aux_normalizacion_salarios(valor, config_hard_skills):
    "Normaliza el salario a partir del proyecto y el mapeo del config.py hard skills"
    resultado = None
    if valor is not None:
        if valor < 40000:
            resultado = config_hard_skills.SALARY_PESOS['ConvertedCompYearly_Bin_<40k']
        elif valor < 70000:
            resultado = config_hard_skills.SALARY_PESOS['ConvertedCompYearly_Bin_40-70k']
        elif valor < 100000:
            resultado = config_hard_skills.SALARY_PESOS['ConvertedCompYearly_Bin_70-100k']
        elif valor < 150000:
            resultado = config_hard_skills.SALARY_PESOS['ConvertedCompYearly_Bin_100-150k']
        else:
            resultado = config_hard_skills.SALARY_PESOS['ConvertedCompYearly_Bin_>150k']
    return resultado


# ---------------------------------------------------------------------------
# Funciones auxiliares de matching con respecto a la localizacion y el idioma del proyecto
# ---------------------------------------------------------------------------

def matching_candidatos_idioma(df_matriz, proyecto, df_geo_hard):
    "Obtiene un vector binario indicando si el candidato cumple con el idioma del proyecto"
    project_idioma = proyecto.get('common_project_language')
    result = None
    if project_idioma:
        idiomas_candidatos = df_geo_hard['Idiomas_Oficiales'].reindex(df_matriz.index).fillna('')
        result = idiomas_candidatos.str.contains(project_idioma, case=False, na=False).astype(int).values
    return result

def matching_candidatos_localizacion(df_matriz, proyecto, df_geo_hard, paises_mapa, score_localizacion=0.5):
    "Realiza un match de localizacion entre los candidatos y el proyecto en varios niveles, si es el país exacto"
    "el score es 1, si es la misma región geográfica el score es 0.5, si no hay match el score es 0"
    resultado = None
    paises_proyecto = proyecto.get('countries_involved', [])
    if paises_proyecto:
        paises_candidatos = df_geo_hard['Country'].reindex(df_matriz.index)
        matching = paises_candidatos.isin(paises_proyecto).astype(int)

        regiones_proyecto = set(paises_mapa.loc[paises_mapa['Pais_Original'].isin(paises_proyecto), 'Region'].dropna())

        if regiones_proyecto:
            mapa_region = paises_mapa.set_index('Pais_Original')['Region']
            regiones_candidatos = paises_candidatos.map(mapa_region)
            matching_regiones = regiones_candidatos.isin(regiones_proyecto).astype(int) * score_localizacion
        else:
            matching_regiones = pd.Series(0, index=df_matriz.index)

        resultado = np.maximum(matching.values, matching_regiones.values)
        
    return resultado



# ---------------------------------------------------------------------------
# Construcción del vector proyecto <--> candidatos
# ---------------------------------------------------------------------------

def vector_candidato_proyecto(proyecto, df_matriz, df_geo_hard, paises_mapa, config_hard_skills):
    "Construye dimensión por dimension la matriz de candidatos y el vector ideal del proyecto"
    "sobre las mismas columnas, para así poder calcular después la distancia entre ambos"
    
    columnas_tech, no_medibles_tech = mapeo_proyecto(proyecto['tech_stack_required'], config_hard_skills.MAPEO_TECNOLOGIAS)
    bloq_candidato = [df_matriz[columnas_tech].values]
    bloq_ideal = [np.ones(len(columnas_tech))]
    dimensiones = list(columnas_tech)
    no_medibles = list(no_medibles_tech)

    nivel_senior = calculo_score_ponderado(df_matriz, config_hard_skills.SENIORITY_PESOS)
    bloq_candidato.append(nivel_senior.reshape(-1, 1))
    bloq_ideal.append(np.array([proyecto['seniority_threshold']]))
    dimensiones.append('seniority')

    score_teletrabajo = calculo_score_ponderado(df_matriz, config_hard_skills.REMOTO_PESOS)
    bloq_candidato.append(score_teletrabajo.reshape(-1, 1))
    bloq_ideal.append(np.array([proyecto['remote_work_pct'] / 100]))
    dimensiones.append('remote_work_pct')

    col_industria = detalle_industria(proyecto, config_hard_skills)
    if col_industria:
        bloq_candidato.append(df_matriz[[col_industria]].values)
        bloq_ideal.append(np.array([1.0]))
        dimensiones.append('industry')
    else:
        no_medibles.append(f"industry:{proyecto['industry']}")

    col_roles = obtener_roles(proyecto)
    if col_roles:
        match_roles = df_matriz[col_roles].max(axis=1).values.reshape(-1, 1)
        bloq_candidato.append(match_roles)
        bloq_ideal.append(np.array([1.0]))
        dimensiones.append('role_title')
    else:
        no_medibles.append(f"role_title:{proyecto['role_title']}")

    match_idioma = matching_candidatos_idioma(df_matriz, proyecto, df_geo_hard)
    if match_idioma is not None:
        bloq_candidato.append(match_idioma.reshape(-1, 1))
        bloq_ideal.append(np.array([1.0]))
        dimensiones.append('idioma_proyecto')
    else:
        no_medibles.append(f"idioma:{proyecto.get('common_project_language')}")

    match_ubicacion = matching_candidatos_localizacion(df_matriz, proyecto, df_geo_hard, paises_mapa)
    if match_ubicacion is not None:
        bloq_candidato.append(match_ubicacion.reshape(-1, 1))
        bloq_ideal.append(np.array([1.0]))
        dimensiones.append('localizacion_proyecto')
    else:
        no_medibles.append(f"localizacion: {proyecto.get('countries_involved')}")

    col_management = detalle_manager(proyecto)
    if col_management:
        bloq_candidato.append(df_matriz[[col_management]].values)
        bloq_ideal.append(np.array([1.0]))
        dimensiones.append('management_level')
    else:
        no_medibles.append("management_level: no especificado")

    col_educacion = detalle_educacion(proyecto, config_hard_skills)
    if col_educacion:
        bloq_candidato.append(df_matriz[[col_educacion]].values)
        bloq_ideal.append(np.array([1.0]))
        dimensiones.append('education')
    else:
        no_medibles.append("education: no especificado")

    col_ssoo = detalle_ssoo(proyecto, config_hard_skills)
    if col_ssoo:
        bloq_candidato.append(df_matriz[[col_ssoo]].values)
        bloq_ideal.append(np.array([1.0]))
        dimensiones.append('os')
    else:
        no_medibles.append("os: no especificado")

    col_employment = detalle_empleo(proyecto, config_hard_skills)
    if col_employment:
        bloq_candidato.append(df_matriz[[col_employment]].values)
        bloq_ideal.append(np.array([1.0]))
        dimensiones.append('employment_type')
    else:
        no_medibles.append("employment_type: no especificado")

    columnas_tools, no_medibles_tools = mapeo_herramientas_conocidas(
        proyecto.get('tools_used', []), config_hard_skills.TOOLS_MEDIBLES, config_hard_skills.TOOLS_MAPPING_PROYECTO
    )
    if columnas_tools:
        cobertura_tools = df_matriz[columnas_tools].mean(axis=1).values
        bloq_candidato.append(cobertura_tools.reshape(-1, 1))
        bloq_ideal.append(np.array([1.0]))
        dimensiones.append('tools_used')
    no_medibles.extend([f"tools_used:{t}" for t in no_medibles_tools])

    col_ide = detalle_ide(proyecto)
    if col_ide:
        bloq_candidato.append(df_matriz[[col_ide]].values)
        bloq_ideal.append(np.array([1.0]))
        dimensiones.append('ide_preferred')
    else:
        no_medibles.append("ide_preferred: no especificado")

    col_ai = obtener_ai_tools(proyecto)
    if col_ai:
        match_ai = df_matriz[col_ai].max(axis=1).values.reshape(-1, 1)
        bloq_candidato.append(match_ai)
        bloq_ideal.append(np.array([1.0]))
        dimensiones.append('ai_tools_preferred')
    else:
        no_medibles.append("ai_tools_preferred: no especificado")

    salario_ideal = aux_normalizacion_salarios(proyecto.get('salary_budget_usd'), config_hard_skills)
    if salario_ideal is not None:
        score_salario = calculo_score_ponderado(df_matriz, config_hard_skills.SALARY_PESOS)
        bloq_candidato.append(score_salario.reshape(-1, 1))
        bloq_ideal.append(np.array([salario_ideal]))
        dimensiones.append('salary_budget')
    else:
        no_medibles.append("salary_budget: no especificado")

    col_company_size = detalle_company_size(proyecto)
    if col_company_size:
        bloq_candidato.append(df_matriz[[col_company_size]].values)
        bloq_ideal.append(np.array([1.0]))
        dimensiones.append('company_size')
    else:
        no_medibles.append("company_size: no especificado")

    matriz_candidatos = np.hstack(bloq_candidato)
    vector_ideal = np.concatenate(bloq_ideal)
    return matriz_candidatos, vector_ideal, dimensiones, no_medibles

# ---------------------------------------------------------------------------
# Pesos por dimensión
# ---------------------------------------------------------------------------


def obtener_pesos(dimensiones,config_hard_skills):
    return np.array([config_hard_skills.PESOS_DIMENSION.get(d, config_hard_skills.PESO_TECH_DEFAULT) 
                     for d in dimensiones])

# ---------------------------------------------------------------------------
# Evidencias obtenidas de la minería de reglas
# ---------------------------------------------------------------------------

def obtener_perfil_tech_candidato(idCandidato, proyecto, df_matriz, config_hard_skills, max_items=4):
    "Subconjunto de tecnologías del stack que el candidato debe dominar. El motivo de limitarlo a 4 items"
    "es porque las reglas de minerías se generaron con max_len bajo: comparar el perfil completo nunca llegaría"
    "a encontrar coincidencias"
    ent = df_matriz.loc[idCandidato]
    columnas_hard, _ = mapeo_proyecto(proyecto['tech_stack_required'], config_hard_skills.MAPEO_TECNOLOGIAS)
    perfil_tech = sorted(c for c in columnas_hard if c in ent.index and ent[c] == 1)
    return set(perfil_tech[:max_items])

def busqueda_evidencias(items_esperados, df_reglas, top_n=5):
    "Busca en las reglas de minería aquellas cuyos items_totales contengan (como superconjunto) "
    "los items_esperados y devuelve las top_n con mayor lift"
    items_esperados=set(items_esperados)
    masc = df_reglas['items_totales'].apply(lambda s: items_esperados.issubset(s))
    resultado = df_reglas[masc].sort_values('lift', ascending=False)
    return resultado.head(top_n)


def obtener_perfil_completo_candidato(idCandidato, proyecto, df_matriz, config_hard_skills):
    "Perfil completo del candidato con todas las dimensiones evaluables, su objetivo es informar"
    "el tamaño n_items_perfil_completo) en el ranking."
    ent = df_matriz.loc[idCandidato]
    col_candidatas =[]

    col_tech, _ = mapeo_proyecto(proyecto['tech_stack_required'], config_hard_skills.MAPEO_TECNOLOGIAS)
    col_candidatas.extend(col_tech)
    col_candidatas.extend(col_tech)
    col_candidatas.extend(config_hard_skills.SENIORITY_PESOS.keys())
    col_candidatas.extend(config_hard_skills.REMOTO_PESOS.keys())

    col_industria = detalle_industria(proyecto, config_hard_skills)
    if col_industria:col_candidatas.append(col_industria)

    col_roles = obtener_roles(proyecto)
    if col_roles:col_candidatas.extend(col_roles)

    col_management = detalle_manager(proyecto)
    if col_management:col_candidatas.append(col_management)

    col_educacion = detalle_educacion(proyecto, config_hard_skills)
    if col_educacion:col_candidatas.append(col_educacion)

    col_ssoo = detalle_ssoo(proyecto, config_hard_skills)
    if col_ssoo:col_candidatas.append(col_ssoo)

    col_employment = detalle_empleo(proyecto, config_hard_skills)
    if col_employment:col_candidatas.append(col_employment)

    columnas_tools, _ = mapeo_herramientas_conocidas(proyecto.get('tools_used', []), config_hard_skills.TOOLS_MEDIBLES, 
        config_hard_skills.TOOLS_MAPPING_PROYECTO)
    col_candidatas.extend(columnas_tools)

    col_ide = detalle_ide(proyecto)
    if col_ide:col_candidatas.append(col_ide)

    col_ai = obtener_ai_tools(proyecto)
    if col_ai: col_candidatas.extend(col_ai)
    
    col_candidatas.extend(config_hard_skills.SALARY_PESOS.keys())

    col_company_size = detalle_company_size(proyecto)
    if col_company_size: col_candidatas.append(col_company_size)

    perfil = {c for c in col_candidatas if c in ent.index and ent[c] == 1}
    return perfil

def add_evidencia(res_ranking, proyecto, df_matriz, df_reglas, 
                  config_hard_skills, top_n_evidencia=4,max_items_evidencia=4):
    "Añade al ranking, para cada candidato, el lift máximo de evidencia minada "
    "sobre su perfil tech (limitado a max_items_evidencia) y el tamaño de su perfil completo/evaluado"
    lifts =[]
    n_items_perfil =[]
    n_items_testeados = []
    for idCandidato in res_ranking['ranking'].index:
        perfil_completo = obtener_perfil_completo_candidato(idCandidato, proyecto, df_matriz, config_hard_skills)
        perfil_solo_tech = obtener_perfil_tech_candidato(idCandidato, proyecto, df_matriz, config_hard_skills,
                                                         max_items=max_items_evidencia)
        if perfil_solo_tech:
            evidencia = busqueda_evidencias(perfil_solo_tech,df_reglas, top_n=top_n_evidencia)
            lift_max = evidencia['lift'].max() if not evidencia.empty else None
        else:
            lift_max = None
        lifts.append(lift_max)
        n_items_perfil.append(len(perfil_completo))
        n_items_testeados.append(len(perfil_solo_tech))
                                 
    ranking = res_ranking['ranking'].copy()
    ranking['lift_evidencia_mineria'] = lifts
    ranking['n_items_perfil_completo'] = n_items_perfil
    ranking['n_items_evaluados'] = n_items_testeados
    res_ranking['ranking'] = ranking
    return res_ranking



# ---------------------------------------------------------------------------
# Visualización del ranking final para las hard skills
# ---------------------------------------------------------------------------

def ubicacion_candidatos(idCandidato, df_geo_hard):
    "Obtiene la ubicación y el idioma del candidato a partir de su id y del dataframe de geolocalización"
    pais = 'N/A'
    idioma = 'N/A'
    if df_geo_hard is not None and idCandidato in df_geo_hard.index:
        dato_geo = df_geo_hard.loc[idCandidato]
        pais = dato_geo.at['Country']
        idioma = dato_geo.at['Idiomas_Oficiales']
        if pd.isna(pais):
            pais = 'N/A'
        if pd.isna(idioma):
            idioma = 'N/A'
    return pais, idioma

def cumple_dimension(nombre, val_candidato, val_proyecto, config_hard_skills, err=1e-6):
    "Comprueba que se cumplen las dimensiones calificadas como umbral o claves"
    if nombre in config_hard_skills.DIMENSIONES_UMBRAL:
        cumple = val_candidato >= (val_proyecto - err)
    else:
        cumple = abs(val_candidato - val_proyecto) <= err
    return cumple

def etiqueta_dimension(nombre, config_hard_skills):
    "Comprueba que la dimension a evaluar se encuentre en el mapeo"
    if nombre in config_hard_skills.ETIQUETAS_DIMENSION:
        resultado = config_hard_skills.ETIQUETAS_DIMENSION[nombre]
    else:
        resultado = nombre.split('_', 1)[-1] if '_' in nombre else nombre
    return resultado

def mostrar_ranking_proyecto(proyecto, res_ranking, df_matriz, df_geo, paises_mapa, config_hard_skills, top_n=5):
    matriz_candidatos_finales, vector_ideales, dimensiones, no_medibles = vector_candidato_proyecto(
        proyecto, df_matriz, df_geo, paises_mapa, config_hard_skills
    )
    posiciones = {cid: i for i, cid in enumerate(df_matriz.index)}

    pesos = obtener_pesos(dimensiones, config_hard_skills)
    distancia_maxima = pesos.sum()

    print("=" * 72)
    print(f" OFERTA: {proyecto.get('company_name', 'N/D')} busca {proyecto.get('role_title', 'N/D')}")
    print(f" PROYECTO: {proyecto.get('project_id', 'N/D')} | Industria: {proyecto.get('industry', 'N/D')}")
    stack = ', '.join(proyecto.get('tech_stack_required', [])) or 'N/D'
    print(f" REQUISITOS TÉCNICOS: {stack}")
    print(f" SENIORITY: {proyecto.get('seniority_required', 'N/D')} (umbral >= {proyecto.get('seniority_threshold', 'N/D')})")
    print(f" TELETRABAJO: {proyecto.get('remote_work_pct', 'N/D')}% | IDIOMA: {proyecto.get('common_project_language', 'N/D')}")
    print(f" PAÍSES DEL PROYECTO: {', '.join(proyecto.get('countries_involved', [])) or 'N/D'}")
    if proyecto.get('tools_used'):
        print(f" HERRAMIENTAS: {', '.join(proyecto['tools_used'])}")
    if no_medibles:
        print(f" (No evaluables por falta de mapeo/dato: {'; '.join(no_medibles)})")
    print("=" * 72)

    ranking = res_ranking['ranking'].head(top_n)
    print(f"\nTOP {len(ranking)} CANDIDATOS:\n")

    for i, (candidato_id, fila) in enumerate(ranking.iterrows(), start=1):
        pos = posiciones[candidato_id]
        vector_candidato = matriz_candidatos_finales[pos]
        cumple_mask = [cumple_dimension(n, vc, vi, config_hard_skills) for n, vc, vi in zip(dimensiones, vector_candidato, vector_ideales)]
        dims_ok = [etiqueta_dimension(d, config_hard_skills) for d, ok in zip(dimensiones, cumple_mask) if ok]
        dims_ko = [etiqueta_dimension(d, config_hard_skills) for d, ok in zip(dimensiones, cumple_mask) if not ok]
        pais_candidato, idiomas_candidato = ubicacion_candidatos(candidato_id, df_geo)

        distancia = fila['distancia_manhattan']
        nivel_match = max(0.0, 100 * (1 - distancia / distancia_maxima)) if distancia_maxima > 0 else 0.0

        print(f" RANKING #{i} | Candidato {candidato_id} | Nivel de Match: {nivel_match:.2f}% "
              f"(distancia Manhattan: {distancia:.2f} | similitud coseno: {fila['similitud_coseno'] * 100:.2f}%)")
        print(f"    * Ubicación: {pais_candidato} | Idiomas: {idiomas_candidato}")
        print(f"    * Cumple ({len(dims_ok)}/{len(dimensiones)}): {', '.join(dims_ok) if dims_ok else '—'}")
        if dims_ko:
            print(f"    * No cumple: {', '.join(dims_ko)}")
        if 'lift_evidencia_mineria' in fila.index:
            lift = fila['lift_evidencia_mineria']
            n_ev = fila.get('n_items_evaluados')
            n_ev = int(n_ev) if pd.notna(n_ev) else n_ev
            lift_txt = f"{lift:.2f}" if pd.notna(lift) else "sin evidencia minada"
            print(f"    * Evidencia de minería (lift, sobre {n_ev} ítems tech): {lift_txt}")
        print("-" * 72)