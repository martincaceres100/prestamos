import streamlit as st
from datetime import datetime, timedelta

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Sistema de Gestión de Préstamos",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ESTILOS CSS PARA CELULAR (Botones grandes, textos legibles)
st.markdown("""
    <style>
        /* Agrandar textos de etiquetas y entradas */
        .stApp label { font-size: 1.2rem !important; font-weight: bold !important; color: #333; }
        .stMetric label { font-size: 1.1rem !important; }
        .stMetric [data-testid="stMetricValue"] { font-size: 2.2rem !important; color: #1f77b4; }
        
        /* Botones táctiles de alto impacto */
        .stButton button { 
            height: 3.8rem !important; 
            font-size: 1.3rem !important; 
            font-weight: bold !important;
            border-radius: 12px !important;
            background-color: #008CBA !important;
            color: white !important;
            width: 100%; 
            margin-top: 10px;
        }
        
        /* Estilo del menú de navegación */
        .stSelectbox div[data-baseweb="select"] {
            font-size: 1.3rem !important;
            font-weight: bold !important;
        }
        
        /* Ajustar espaciado en móviles */
        @media (max-width: 640px) {
            .stMetric [data-testid="stMetricValue"] { font-size: 1.8rem !important; }
            h1 { font-size: 1.8rem !important; }
        }
    </style>
""", unsafe_allow_html=True)

# 3. FUNCIONES DE AYUDA
def formato_moneda(valor):
    return f"$ {valor:,.0f}".replace(",", ".")

# 4. MENÚ DE NAVEGACIÓN SUPERIOR
# Ideal para celulares porque evita abrir el sidebar constantemente
st.title("🏦 Finanzas Pro")
seccion = st.selectbox(
    "Seleccione una operación:", 
    ["🚀 Nuevo Préstamo (Simulador)", "📅 Agenda de Cobros", "👤 Clientes y Historial"]
)
st.markdown("---")

# ==========================================
# SECCIÓN 1: SIMULADOR (NUEVO PRÉSTAMO)
# ==========================================
if seccion == "🚀 Nuevo Préstamo (Simulador)":
    st.header("📝 Cargar Nuevo Préstamo")
    
    # Bloque de datos del cliente
    with st.expander("👤 Datos del Cliente", expanded=True):
        nombre = st.text_input("Nombre Completo", "Juan Pérez")
        telefono = st.text_input("Número de WhatsApp (con código de país)", "549")
        st.caption("Ejemplo: 5491165432121")

    # Bloque financiero
    with st.container():
        st.subheader("💰 Condiciones Financieras")
        col1, col2 = st.columns(2)
        with col1:
            monto = st.number_input("Monto a entregar ($)", min_value=0, value=1000000, step=10000)
            st.info(f"Entregas: **{formato_moneda(monto)}**")













