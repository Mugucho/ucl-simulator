from statsbombpy import sb

def obtener_tiros_champions(match_id):
    eventos = sb.events(match_id=match_id)
    tiros = eventos[eventos['type'] == 'Shot'].copy()
    
    # Extraer coordenadas (location se mantiene como una lista [x, y])
    tiros['x'] = tiros['location'].apply(lambda loc: loc[0] if isinstance(loc, list) else None)
    tiros['y'] = tiros['location'].apply(lambda loc: loc[1] if isinstance(loc, list) else None)
    
    # StatsBomb ya extrajo el xG en su propia columna
    if 'shot_statsbomb_xg' in tiros.columns:
        tiros['xg'] = tiros['shot_statsbomb_xg'].fillna(0)
    else:
        tiros['xg'] = 0
        
    return tiros[['team', 'player', 'x', 'y', 'xg']]