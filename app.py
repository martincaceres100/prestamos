import streamlit as st
from datetime import datetime, timedelta
import urllib.parse

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Gestión de Préstamos", page_icon="💰", layout="wide")

# 2. ESTILOS
st.markdown("""
    <style>
        .stApp label { font-size: 1.2rem !important; font-weight: bold !important; }
        .stMetric label { font-size: 1.1rem !important; }
        .stMetric [data-testid="stMetricValue"] { font-size: 2rem !important; }
        .stButton button { height: 3.5rem !important; font-size: 1.2rem !important; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# 3. FUNCIONES
def formato_moneda(valor):
    return f"$ {valor:,.0f}".replace(",", ".")

# 4. NAVEGACIÓN
seccion = st.selectbox("📍 Ir a:", ["🚀 Nuevo Préstamo (Simulador)", "📅 Agenda de Cobros", "👤 Clientes y Préstamos"])
st.markdown("---")

if seccion == "🚀 Nuevo Préstamo (Simulador)":
    st.header("Simulador de Préstamo")
    
    # DATOS DE ENTRADA
    nombre = st.text_input("Nombre del Cliente", "Juan Pérez")
    
    # Usamos el parámetro 'key' para que Streamlit guarde el valor en tiempo real
    telefono_raw = st.text_input("Celular (Ej: 549351234567)", value="549351", key="tel_manual")
    
    c1, c2 = st.columns(2)
    with c1:
        monto = st.number_input("Monto a entregar ($)", min_value=0, value=1000000, step=50000)
    with c2:
        tasa = st.number_input("Tasa Mensual (%)", min_value=0.0, value=10.0, step=0.5)
    
    c3, c4 = st.columns(2)
    with c3:
        cuotas = st.number_input("Cuotas", min_value=1, value=6, step=1)
    with c4:
        fecha_prestamo = st.date_input("Fecha del préstamo", datetime.now(), format="DD/MM/YYYY")

    # CÁLCULOS
    interes_total = monto * (tasa / 100) * cuotas
    monto_total = monto + interes_total
    valor_cuota = monto_total / cuotas
    fecha_ultima_cuota = fecha_prestamo + timedelta(days=int(cuotas) * 30)

    st.markdown("---")
    st.subheader(f"📊 Resultados para {nombre}")
    
    col_a, col_b = st.columns(2)
    col_a.metric("Monto Entregado", formato_moneda(monto))
    col_b.metric("Cuotas Totales", f"{int(cuotas)} cuotas")
    
    col_c, col_d = st.columns(2)
    col_c.metric("Cuota Mensual", formato_moneda(valor_cuota))
    col_d.metric("Última cuota", fecha_ultima_cuota.strftime('%d/%m/%Y'))

    st.markdown("---")
    
    # --- PROCESO CRÍTICO DE LIMPIEZA ---
    # Capturamos el valor actual del input de forma forzada
    numero_final = "".join(filter(str.isdigit, st.session_state.tel_manual))
    
    texto_prop = (
        f"Hola *{nombre}*, esta es la propuesta de tu préstamo:\n\n"
        f"💰 *Monto:* {formato_moneda(monto)}\n"
        f"🗓️ *Plan:* {int(cuotas)} cuotas de {formato_moneda(valor_cuota)}\n"
        f"🏁 *Última cuota:* {fecha_ultima_cuota.strftime('%d/%m/%Y')}\n\n"
        "¿Te interesa para que lo demos de alta?"
    )
    
    # Construimos el link final asegurándonos de que numero_final sea lo último que escribió el usuario
    url_p = f"https://wa.me/{numero_final}?text={urllib.parse.quote(texto_prop)}"

    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        # El st.link_button SIEMPRE va a usar el numero_final procesado arriba
        st.link_button("📤 Enviar Propuesta", url_p)

    with col_btn2:
        if st.button("✅ Confirmar y Registrar"):
            st.success(f"Préstamo registrado para {nombre}")
            texto_conf = f"✅ *¡Préstamo Confirmado!*\n\nHola *{nombre}*, ya dimos de alta tu préstamo."
            url_c = f"https://wa.me/{numero_final}?text={urllib.parse.quote(texto_conf)}"
            st.link_button("📱 Avisar Confirmación", url_c)






