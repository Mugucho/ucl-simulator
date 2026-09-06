import streamlit as st

# Configuración inicial
st.set_page_config(page_title="UCL Deserve-to-Win", layout="wide")

# CSS Corregido (Forzando color de texto oscuro para compatibilidad)
st.markdown("""
<style>
.horizontal-scroll {
    display: flex;
    overflow-x: auto;
    gap: 15px;
    padding-bottom: 15px;
}
.game-card {
    min-width: 260px;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 15px;
    background-color: white;
    color: #111827; /* Forzamos texto oscuro */
    flex: 0 0 auto;
}
.tag-lucky {
    background-color: #f3e8ff;
    color: #7e22ce;
    font-size: 0.7rem;
    font-weight: bold;
    padding: 3px 8px;
    border-radius: 12px;
    float: right;
}
.tag-close {
    background-color: #fef3c7;
    color: #b45309;
    font-size: 0.7rem;
    font-weight: bold;
    padding: 3px 8px;
    border-radius: 12px;
    float: right;
}
.pills {
    display: flex;
    gap: 10px;
    margin: 20px 0;
    align-items: center;
}
.pill {
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 0.9rem;
    color: #4b5563;
    background-color: white;
}
.pill.active {
    background-color: #1f2937;
    color: white;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# 1. Navegación Superior
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown("### ⚽ UCL Deserve-to-Win")
with col2:
    st.markdown("<div style='text-align: right; padding-top: 10px; color: #4b5563;'><b>Home</b> &nbsp;&nbsp; Games &nbsp;&nbsp; Standings &nbsp;&nbsp; League &nbsp;&nbsp; Teams &nbsp;&nbsp; Tools &nbsp;&nbsp; Analysis</div>", unsafe_allow_html=True)

# 2. Buscador y Texto Principal
st.text_input("Search", placeholder="Search players & teams...", label_visibility="collapsed")
st.markdown("<p style='color: #6b7280; font-size: 1.1rem; margin-top: 15px;'>Who deserved to win: every UCL game re-simulated from shot quality (xG), not the final score.</p>", unsafe_allow_html=True)

# 3. Navegación de Página
st.markdown("""
<div class="pills">
<span style="font-size: 0.8rem; font-weight: bold; color: #6b7280; letter-spacing: 1px;">ON THIS PAGE</span>
<div class="pill active">Latest</div>
<div class="pill">Upcoming games</div>
<div class="pill">This season</div>
<div class="pill">Analysis</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# 4. Sección de Partidos
col3, col4 = st.columns([4, 1])
with col3:
    st.markdown("## Latest games")
with col4:
    st.date_input("Date", label_visibility="collapsed")

# 5. Tarjetas de Partidos (Sin indentación extra para evitar bloques de código Markdown)
st.markdown("""
<div class="horizontal-scroll">
<div class="game-card" style="border-left: 4px solid #10b981;">
<div style="color: #6b7280; font-size: 0.8rem; margin-bottom: 15px;">SEP 5, 2026</div>
<div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 8px;"><span>Real Madrid</span><span>3</span></div>
<div style="display: flex; justify-content: space-between; color: #4b5563;"><span>Liverpool</span><span>1</span></div>
</div>
<div class="game-card" style="border-left: 4px solid #3b82f6;">
<div style="color: #6b7280; font-size: 0.8rem; margin-bottom: 15px;">SEP 5, 2026 <span class="tag-close">CLOSE</span></div>
<div style="display: flex; justify-content: space-between; color: #4b5563; margin-bottom: 8px;"><span>Bayern Munich</span><span>1</span></div>
<div style="display: flex; justify-content: space-between; font-weight: bold;"><span>Man City</span><span>2</span></div>
</div>
<div class="game-card" style="border-left: 4px solid #8b5cf6;">
<div style="color: #6b7280; font-size: 0.8rem; margin-bottom: 15px;">SEP 5, 2026 <span class="tag-lucky">LUCKY</span></div>
<div style="display: flex; justify-content: space-between; color: #4b5563; margin-bottom: 8px;"><span>Juventus</span><span>1</span></div>
<div style="display: flex; justify-content: space-between; font-weight: bold;"><span>PSG</span><span>2</span></div>
</div>
<div class="game-card" style="border-left: 4px solid #ef4444;">
<div style="color: #6b7280; font-size: 0.8rem; margin-bottom: 15px;">SEP 5, 2026 <span class="tag-close">CLOSE</span></div>
<div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 8px;"><span>Barcelona</span><span>2</span></div>
<div style="display: flex; justify-content: space-between; color: #4b5563;"><span>Inter Milan</span><span>1</span></div>
</div>
</div>
""", unsafe_allow_html=True)