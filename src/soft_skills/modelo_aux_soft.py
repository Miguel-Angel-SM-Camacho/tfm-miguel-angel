import pandas as pd
import numpy as np
from src.soft_skills import config as config_soft_skills


# ---------------------------------------------------------------------------
#  Evidencia de minería para las reglas expertas soft_parcial
# ---------------------------------------------------------------------------

def busqueda_evidencias(items_esperados, df_reglas, top_n=5):
    "Busca en las reglas de minería aquellas cuyos items_totales contengan (como"
    "superconjunto) los items_esperados y devuelve las top_n con mayor lift."
    items_esperados=set(items_esperados)
    masc = df_reglas['items_totales'].apply(lambda s: items_esperados.issubset(s))
    resultado = df_reglas[masc].sort_values('lift', ascending=False)
    return resultado.head(top_n)

def calculo_metricas(a,b,df_matriz):
    "Recalcula support, confianza y lift sovre la matriz cuando un ítem no supera"
    "el min_support fijado en la fase de minería y por tanto nunca aparece en reglas_limpias_soft"
    resultado = None
    n=len(df_matriz)
    support_a = df_matriz[a].sum()/n
    support_b = df_matriz[b].sum()/n
    support_ab = (df_matriz[a] & df_matriz[b]).sum() / n
    if support_a != 0 and support_b != 0:
        resultado = support_ab/(support_a*support_b)
    return resultado

def obtener_evidencias_reglas_soft(regla, df_reglas, df_matriz):
    "Determina la evidancia, primero intenta encontrarla en las reglas minadas,"
    "si no la encuentra y la regla combina 2 ítems se recalcula. En caso de ser un solo ítem"
    "sin evidencia no puede calcular lift"
    res = {'lift': None, 'fuente': 'sin_evidencia_estadistica'}
    items = set(regla['items_soft'])
    evidencia = busqueda_evidencias(items, df_reglas)
    if not evidencia.empty:
        res = {'lift': evidencia['lift'].max(), 'fuente': 'apriori'}
    elif len(items) == 2:
        a, b = sorted(items)
        lift = calculo_metricas(a, b, df_matriz)
        if lift is not None:
            res = {'lift': lift, 'fuente': 'calculo_manual'}
            
    return res

def pesos_reglas_soft(idRegla,evidencia,config_soft_skills):
    "Es el peso de una regla activa cuyo lift si tiene evidencia, o si la regla tiene un solo"
    "item sin evidencia como las reglas 11 y 22"
    lift= evidencia[idRegla]['lift']
    return lift if lift is not None else config_soft_skills.PESO_BASE_SIN_EVIDENCIA


# ---------------------------------------------------------------------------
# Evaluación de riesgo 
# ---------------------------------------------------------------------------

def activar_reglas_soft(ent, reglas, evidencia, config_soft_skills):
    "Comprueba por candidato que reglas activa y devuelve el detalle de cda una,"
    "su riesgo asociado, la mitigación sugerida y el peso de la evidencia"
    riesgos_activos = []
    for regla in reglas:
        items = regla['items_soft']
        if all(ent.get(item, 0) == 1 for item in items):
            riesgos_activos.append({
                'id_regla': regla['id'],
                'riesgo': regla['riesgo'],
                'items_activados': items,
                'mitigacion': regla['mitigacion'],
                'peso_evidencia': pesos_reglas_soft(regla['id'], evidencia, config_soft_skills),
            })
    return riesgos_activos

def evaluar_riesgo_poblacion(df_matriz, reglas, evidencia, config_soft_skills):
    "Aplica activar reglas soft a todos los candidatos y agrega un score por cada uno de ellos"
    "junto con el detalle de cada una y el número de riesgos distintos que tiene"
    res = df_matriz.apply(lambda fila: activar_reglas_soft(fila, reglas, evidencia,config_soft_skills), axis=1
    )
    df_riesgo = pd.DataFrame({
        'riesgos_activados': res,
        'n_riesgos': res.apply(len),
        'riesgos_nombres': res.apply(lambda rs: sorted({r['riesgo'] for r in rs})),
        'score_riesgo': res.apply(lambda rs: sum(r['peso_evidencia'] for r in rs)),
    }, index=df_matriz.index)
    df_riesgo['n_riesgos_unicos'] = df_riesgo['riesgos_nombres'].apply(len)
    return df_riesgo


def ranking_riesgos(df_riesgo,ascendente=True,top_n=10):
    "Ordena los candidatos por score de riesgo de forma ascendente, candidatos más seguros primero"
    return df_riesgo.sort_values(['score_riesgo', 'n_riesgos_unicos', 'n_riesgos'],ascending=ascendente).head(top_n)


# ---------------------------------------------------------------------------
# Condición de proyecto por regla que no depende del candidato sino de los atributos del proyecto
# ---------------------------------------------------------------------------

def reglas_activas_proyecto(proyecto,reglas, config_soft_skills):
    "Filtra las reglas soft_parcial que activa un proyecto concreto según sus propios atributos"
    return [r for r in reglas if config_soft_skills.CONDICIONES_PROYECTO_SOFT[r['id']](proyecto)]


def evaluacion_riesgos_proyecto(proyecto, df_matriz, reglas, evidencia, config_soft_skills):
    """Evalúa el riesgo de toda la población de candidatos, pero solo con las
    reglas soft_parcial que este proyecto concreto activa"""
    reglas_activas = reglas_activas_proyecto(proyecto, reglas, config_soft_skills)
    df_riesgo = evaluar_riesgo_poblacion(df_matriz, reglas_activas, evidencia, config_soft_skills)
    return df_riesgo, reglas_activas

# ---------------------------------------------------------------------------
# Índice de compromiso/disponibilidad
# ---------------------------------------------------------------------------

def calculo_compromiso(df_matriz, pesos=config_soft_skills.PESOS_INDICE_COMPROMISO, n=len(config_soft_skills.VARIABLES_INDICE_COMPROMISO)):
    """Índice [0,1]: media, entre las 9 variables, del peso de la categoría que
    tiene cada candidato. Valida antes que todas las columnas de `pesos` existen
    en la matriz, para no fallar en silencio si algún nombre no coincide."""
    col = list(pesos.keys())
    faltantes = [c for c in col if c not in df_matriz.columns]
    if faltantes:
        raise KeyError(f"Columnas del índice de compromiso faltantes en la matriz: {faltantes}")
    val = np.array(list(pesos.values()))
    return (df_matriz[col].values @ val) / n


# ---------------------------------------------------------------------------
# Selección en dos fases: filtra por riesgo, ordena por compromiso
# ---------------------------------------------------------------------------

def mejores_candidatos(proyecto, df_matriz, reglas, evidencia, config_soft_skills, top_n=10, umbral_riesgo_max=0.0):
    "En la primera fase descarta a candidatos que superan el umbral máximo y en la segunda fase, los que quedan se ordenan"
    "por índice de compromiso descendiente"
    df_riesgo, reglas= evaluacion_riesgos_proyecto(proyecto, df_matriz,reglas, evidencia, config_soft_skills)
    df_riesgo['indice_compromiso'] = calculo_compromiso(df_matriz)
    candidatos_elegidos = df_riesgo[df_riesgo['score_riesgo'] <= umbral_riesgo_max]
    ranking = candidatos_elegidos.sort_values('indice_compromiso', ascending=False).head(top_n)
    return ranking, reglas, len(candidatos_elegidos)

# ---------------------------------------------------------------------------
# Visualización del riesgo por candidato / proyecto
# ---------------------------------------------------------------------------

def riesgo_candidatos(idCandidato, df_riesgo):
    "Muestra el score de riesgo de un candidato y si tiene el detalle de las reglas activas"
    "además de su causa y posible mitigación"
    ent = df_riesgo.loc[idCandidato]
    print(f"CANDIDATO {idCandidato} | Score de riesgo: {ent['score_riesgo']:.2f} "
          f"({ent['n_riesgos_unicos']} riesgos únicos, {ent['n_riesgos']} reglas activadas)")
    
    if not ent['riesgos_activados']:
        print("  Sin riesgos activados.")
    else:
        for r in ent['riesgos_activados']:
            items_txt = ', '.join(r['items_activados'])
            print(f"  - [{r['riesgo']}] activado por: {items_txt} (peso evidencia: {r['peso_evidencia']:.2f})")
            print(f"      Mitigación sugerida: {r['mitigacion']}")


def mostrar_riesgo_proyecto(proyecto, df_riesgos_top, reglas, total_reglas_soft, titulo_bloque="candidatos más destacados", top_n=5):
    "Muestra el proyecto y los candidatos más relevantes en el mismo"
    print("=" * 72)
    print(f" PROYECTO: {proyecto.get('project_id', 'N/D')} | {proyecto.get('company_name', 'N/D')} busca {proyecto.get('role_title', 'N/D')}")
    print(f" CONDICIONES DE RIESGO QUE ACTIVA ESTE PROYECTO ({len(reglas)}/{total_reglas_soft} reglas soft_parcial):")
    if reglas:
        for r in reglas:
            print(f"   - [{r['id']}] {r['riesgo']}: {r['condicion_texto']}")
    else:
        print("   Ninguna — las condiciones de este proyecto no activan ningún riesgo de soft skills conocido.")
    print("=" * 72)

    print(f"\nTOP {min(top_n, len(df_riesgos_top))} {titulo_bloque.upper()} PARA ESTE PROYECTO:\n")
    for i, cid in enumerate(df_riesgos_top.index, start=1):
        print(f"RANKING #{i}")
        riesgo_candidatos(cid, df_riesgos_top)
        print("-" * 72)


# ---------------------------------------------------------------------------
# Despliegue de la API para el ranking de candidatos según hard skills Docker
# ---------------------------------------------------------------------------

def construir_respuesta_json(proyecto, df_ranking, reglas_activas, n_candidatos_finales, total_reglas_soft):
    "Construye la respuesta JSON para la API del ranking de candidatos en base a las soft skills"
    candidatos = []
    for cid, f in df_ranking.iterrows():
        candidatos.append({
            'candidate_id': int(cid),
            'score_riesgo': round(float(f['score_riesgo']), 4),
            'n_riesgos_unicos': int(f['n_riesgos_unicos']),
            'n_riesgos_activados': int(f['n_riesgos']),
            'indice_compromiso': round(float(f['indice_compromiso']), 4),
            'riesgos_activados': [
                {
                    'id_regla': r['id_regla'],
                    'riesgo': r['riesgo'],
                    'items_activados': r['items_activados'],
                    'mitigacion': r['mitigacion'],
                    'peso_evidencia': round(float(r['peso_evidencia']), 4),
                }
                for r in f['riesgos_activados']
            ],
        })
    return {
        'project_id': proyecto.get('project_id'),
        'reglas_activas': [{'id': r['id'], 'riesgo': r['riesgo'], 'condicion_texto': r['condicion_texto']} for r in reglas_activas],
        'total_reglas_soft': total_reglas_soft,
        'candidatos_con_riesgo_aceptable': n_candidatos_finales,
        'candidatos': candidatos,
    }        