import streamlit as st
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(page_title="Gestión de Préstamos", page_icon="💰", layout="wide")

# --- ESTILOS CSS PARA MEJORAR LA VISTA EN CELULAR ---
st.markdown("""
    <style>
        .stApp label { font-size: 1.2rem !important; font-weight: bold !important; }
        .stMetric label { font-size: 1.1rem !important; }
        .stMetric [data-testid="stMetricValue"] { font-size: 2rem !important; }
        .stButton button { height: 3.5rem !important; font-size: 1.2rem !important; width: 100%; }
        h1 { font-size: 2.2rem !important; }
        h2 { font-size: 1.8rem !important; }
    </style>
""", unsafe_allow_html=True)

# --- FUNCIONES DE APOYO ---
def formato_moneda(valor):
    return f"$ {valor:,.0f}".replace(",", ".")

def limpiar_telefono(num):
    return "".join(filter(str.isdigit, num))

# --- MENÚ DE NAVEGACIÓN ---
seccion = st.selectbox("📍 Ir a:", ["🚀 Nuevo Préstamo (Simulador)", "📅 Agenda de Cobros", "👤 Clientes y Préstamos"])
st.markdown("---")

# ==========================================
# SECCIÓN 1: SIMULADOR
# ==========================================
if seccion == "🚀 Nuevo Préstamo (Simulador)":
    st.header("Simulador de Préstamo")
    
    with st.container():
        nombre = st.text_input("Nombre del Cliente", "Juan Pérez")
        telefono_raw = st.text_input("Celular (prefijo automático)", "+54 9 351 ")
        
        c1, c2 = st.columns(2)
        with c1:
            monto = st.number_input("Monto a entregar ($)", min_value=0, value=1000000, step=50000)
            st.write(f"Monto: **{formato_moneda(monto)}**")
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
    
    # Bloque de Cuota Mensual y Fecha Final integrados
    st.metric("Cuota Mensual", formato_moneda(valor_cuota))
    st.markdown(f"🗓️ **Última cuota:** {fecha_ultima_cuota.strftime('%d/%m/%Y')}")

    st.markdown("---")

    # --- LÓGICA DEL INTERRUPTOR ---
    vista_simplificada = st.toggle("Vista simplificada (Ocultar datos de cierre)", value=False)
    
    if not vista_simplificada:
        st.markdown("#### 🔒 Datos de Cierre (Solo Prestamista)")
        c_p1, c_p2 = st.columns(2)
        c_p1.metric("Total a Devolver", formato_moneda(monto_total))
        c_p2.metric("Rendimiento Final", formato_moneda(interes_total), delta=f"{tasa}% mensual")

    st.markdown("---")
    
    # ACCIONES DE WHATSAPP
    tel_destino = limpiar_telefono(telefono_raw)
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        mensaje_propuesta = (
            f"Hola {nombre}, esta es la propuesta de tu préstamo:\n\n"
            f"💰 *Monto:* {formato_moneda(monto)}\n"
            f"🗓️ *Plan:* {int(cuotas)} cuotas de {formato_moneda(valor_cuota)}\n"
            f"🏁 *Última cuota:* {fecha_ultima_cuota.strftime('%d/%m/%Y')}\n\n"
            "¿Te interesa para que lo demos de alta?"
        )
        url_propuesta = f"https://wa.me/{tel_destino}?text={mensaje_propuesta.replace(' ', '%20').replace('\n', '%0A')}"
        st.link_button("📤 Enviar Propuesta", url_propuesta)

    with col_btn2:
        if st.button("✅ Confirmar y Registrar"):
            st.success(f"Préstamo de {nombre} registrado exitosamente.")
            mensaje_confirmacion = f"✅ *¡Préstamo Confirmado!*\n\nHola {nombre}, ya dimos de alta tu préstamo de {formato_moneda(monto)}."
            url_confirmar = f"https://wa.me/{tel_destino}?text={mensaje_confirmacion.replace(' ', '%20').replace('\n', '%0A')}"
            st.link_button("📱 Avisar Confirmación", url_confirmar)

# Las demás secciones permanecen igual...
