import pandas as pd
import re

def load_all_time_table():
    # Cargar datos
    df = pd.read_csv("dataset/UCL_AllTime_Performance_Table.csv")
    
    # 1. Rellenar los rankings vacíos (Forward fill)
    df['#'] = df['#'].ffill().astype(int)
    
    # 2. Corregir la columna de goles arruinada por Excel
    df['Goals_For'] = df['goals'].str.split(':').str[0].astype(int)
    df['Goals_Against'] = df['Goals_For'] - df['Dif']
    df = df.drop(columns=['goals'])
    
    # 3. Recalcular los puntos correctamente (3 por victoria, 1 por empate)
    df['Pt.'] = (df['W'] * 3) + (df['D'] * 1)
    
    return df

def load_finals_history():
    # Cargar datos
    df = pd.read_csv("dataset/UCL_Finals_1955-2023.csv")
    
    # 1. Renombrar columnas duplicadas
    df = df.rename(columns={
        'Country': 'Winner_Country', 
        'Country.1': 'RunnerUp_Country'
    })
    
    # 2. Limpiar caracteres extraños en los nombres de las columnas (ej. Attend\xadance)
    df.columns = [re.sub(r'[^\x00-\x7F]+', '', col) for col in df.columns]
    
    # 3. Limpiar Asistencia para que sea un número (la final de 2020 tiene 0 por el Covid)
    df['Attendance'] = df['Attendance'].astype(str).str.replace(',', '').replace('nan', '0')
    df['Attendance'] = pd.to_numeric(df['Attendance'], errors='coerce').astype('Int64')
    
    # 4. Dividir el marcador en goles del ganador y del perdedor
    df['Score_Clean'] = df['Score'].str.replace('–', '-')
    df[['Winner_Goals', 'RunnerUp_Goals']] = df['Score_Clean'].str.split('-', expand=True).astype(int)
    
    return df