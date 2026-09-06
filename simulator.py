import numpy as np

def simular_partido(tiros_df, num_simulaciones=10000):
    equipos = tiros_df['team'].unique()
    resultados = {}
    
    for equipo in equipos:
        xg_equipo = tiros_df[tiros_df['team'] == equipo]['xg'].values
        # Matriz de números aleatorios (tiros x simulaciones)
        aleatorios = np.random.random((len(xg_equipo), num_simulaciones))
        # Sumar goles si el número aleatorio es menor al xG
        goles = (aleatorios < xg_equipo[:, None]).sum(axis=0)
        resultados[equipo] = goles
        
    return resultados, equipos