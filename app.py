import streamlit as st
import datetime
import numpy as np
import pandas as pd
from historical_data import load_all_time_table, load_finals_history

# Configuración inicial
st.set_page_config(page_title="UCL Deserve-to-Win", layout="wide")

# CSS Minimalista y adaptado a Modo Oscuro
st.markdown("""
<style>
.horizontal-scroll {
    display: flex;
    overflow-x: auto;
    gap: 20px;
    padding-bottom: 20px;
}
.game-card {
    min-width: 280px;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 16px;
    background-color: #1e293b; /* Fondo oscuro y limpio */
    color: #f8fafc; /* Texto claro */
    flex: 0 0 auto;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.tag-lucky {
    background-color: #f3e8ff;
    color: #7e22ce;
    font-size: 0.7rem;
    font-weight: bold;
    padding: 4px 8px;
    border-radius: 12px;
    float: right;
}
.tag-close {
    background-color: #fef3c7;
    color: #b45309;
    font-size: 0.7rem;
    font-weight: bold;
    padding: 4px 8px;
    border-radius: 12px;
    float: right;
}
</style>
""", unsafe_allow_html=True)

# 1. Navegación Superior y Header
st.title("⚽ UCL Deserve-to-Win")
st.markdown("<p style='color: #94a3b8; font-size: 1.1rem; margin-top: -10px;'>Who deserved to win: every UCL game re-simulated from shot quality (xG), not the final score.</p>", unsafe_allow_html=True)
st.text_input("Search", placeholder="Search players & teams...", label_visibility="collapsed")

# 2. Menú de Navegación
tab_selection = st.radio(
    "Navigation",
    ["Latest Games", "All-Time Standings", "Finals History"],
    horizontal=True,
    label_visibility="collapsed"
)
st.divider()

# Cargar los datos limpios
df_standings = load_all_time_table()
df_finals = load_finals_history()

# 3. Lógica de Pestañas
if tab_selection == "Latest Games":
    
    # Fechas
    ultima_fecha = datetime.date(2023, 6, 10)
    hace_un_mes = ultima_fecha - datetime.timedelta(days=30)

    col1, col2 = st.columns([4, 1])
    with col1:
        st.subheader("Latest games")
    with col2:
        st.date_input("Select date range", value=(hace_un_mes, ultima_fecha), label_visibility="collapsed")
        
    # Generación Dinámica de Tarjetas (Últimas 4 finales)
    ultimos_juegos = df_finals.tail(4).iloc[::-1]
    colores_borde = ["#f59e0b", "#3b82f6", "#8b5cf6", "#ef4444"]
    
    cards_html = '<div class="horizontal-scroll">\n'
    for idx, (_, row) in enumerate(ultimos_juegos.iterrows()):
        color = colores_borde[idx % len(colores_borde)]
        cards_html += f"""<div class="game-card" style="border-left: 4px solid {color};">
<div style="color: #94a3b8; font-size: 0.8rem; margin-bottom: 15px;">
Season {row['Season']} <span class="tag-lucky" style="background-color: #fef08a; color: #b45309;">FINAL</span>
</div>
<div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 8px; font-size: 1.1rem;">
<span>{row['Winners']}</span><span>{row['Winner_Goals']}</span>
</div>
<div style="display: flex; justify-content: space-between; color: #cbd5e1; font-size: 1.1rem;">
<span>{row['Runners-up']}</span><span>{row['RunnerUp_Goals']}</span>
</div>
</div>
"""
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)
    
    # Simulación Monte Carlo
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.subheader("🎲 Simulaciones Monte Carlo (Proyección 2025-2026)")
    st.markdown("<span style='color: #94a3b8;'>Proyección estadística basada en el rendimiento histórico absoluto y modelo de Poisson.</span>", unsafe_allow_html=True)
    
    equipos_historicos = sorted(df_standings['Team'].tolist())
    # Definir valores por defecto inteligentemente si existen
    idx_eq1 = equipos_historicos.index("Real Madrid") if "Real Madrid" in equipos_historicos else 0
    idx_eq2 = equipos_historicos.index("Bayern Munich") if "Bayern Munich" in equipos_historicos else 1

    c1, c2 = st.columns(2)
    with c1:
        equipo1 = st.selectbox("Equipo Local", equipos_historicos, index=idx_eq1)
    with c2:
        equipo2 = st.selectbox("Equipo Visitante", equipos_historicos, index=idx_eq2)
        
    if equipo1 and equipo2 and equipo1 != equipo2:
        stats1 = df_standings[df_standings['Team'] == equipo1].iloc[0]
        stats2 = df_standings[df_standings['Team'] == equipo2].iloc[0]
        
        # Salvaguardia matemática para evitar división por 0
        partidos1 = max(1, stats1['M.'])
        partidos2 = max(1, stats2['M.'])
        
        xg1 = (stats1['Goals_For'] / partidos1 + stats2['Goals_Against'] / partidos2) / 2
        xg2 = (stats2['Goals_For'] / partidos2 + stats1['Goals_Against'] / partidos1) / 2
        
        num_sims = 10000
        sims_eq1 = np.random.poisson(xg1, num_sims)
        sims_eq2 = np.random.poisson(xg2, num_sims)
        
        vic_1 = (sims_eq1 > sims_eq2).mean() * 100
        vic_2 = (sims_eq2 > sims_eq1).mean() * 100
        empate = (sims_eq1 == sims_eq2).mean() * 100
        
        st.markdown(f"**xG Proyectado:** {equipo1} **{xg1:.2f}** - **{xg2:.2f}** {equipo2}")
        
        m1, m2, m3 = st.columns(3)
        m1.metric(f"Victoria {equipo1}", f"{vic_1:.1f}%")
        m2.metric("Empate", f"{empate:.1f}%")
        m3.metric(f"Victoria {equipo2}", f"{vic_2:.1f}%")
        
        # Gráfico Minimalista de Streamlit (Sustituye a Matplotlib)
        max_goles = max(sims_eq1.max(), sims_eq2.max())
        
        # Extraer las frecuencias en un DataFrame para st.bar_chart
        frecuencias_eq1 = np.bincount(sims_eq1, minlength=max_goles+1) / num_sims
        frecuencias_eq2 = np.bincount(sims_eq2, minlength=max_goles+1) / num_sims
        
        df_grafico = pd.DataFrame({
            equipo1: frecuencias_eq1,
            equipo2: frecuencias_eq2
        })
        
        st.bar_chart(df_grafico, color=["#3b82f6", "#ef4444"])

elif tab_selection == "All-Time Standings":
    st.subheader("🏆 All-Time Champions League Performance")
    st.dataframe(
        df_standings[['#', 'Team', 'M.', 'W', 'D', 'L', 'Goals_For', 'Goals_Against', 'Dif', 'Pt.']],
        hide_index=True,
        width="stretch"  # Solución a la advertencia de depreciación
    )

elif tab_selection == "Finals History":
    st.subheader("📖 UCL Finals History (1955-2023)")
    
    c_a, c_b = st.columns(2)
    c_a.metric("Total Finals Played", len(df_finals))
    c_b.metric("Avg. Attendance", f"{df_finals['Attendance'].mean():,.0f}")

    st.dataframe(
        df_finals[['Season', 'Winners', 'Winner_Goals', 'RunnerUp_Goals', 'Runners-up', 'Venue', 'Attendance']],
        hide_index=True,
        width="stretch"  # Solución a la advertencia de depreciación
    )