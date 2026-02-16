import streamlit as st
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(page_title="Gestión de Préstamos", page_icon="💰", layout="wide")

# --- ESTILOS CSS PARA MEJORAR LA VISTA EN CELULAR ---
st.markdown("""
    <style>
        /* Agrandar textos y etiquetas */
        .stApp label { font-size: 1.2rem !important; font-weight: bold !important; }
        .stMetric label { font-size: 1.1rem !important; }
        .stMetric [data-testid="stMetricValue"] { font-size: 2rem !important; }
        /* Botones más grandes para el pulgar */
        .stButton button { height: 3.5rem !important; font-size: 1.2rem !important; width: 100%; }
        /* Ajuste de títulos */
        h1 { font-size: 2.2rem !important; }
        h2 { font-size: 1.8rem !important; }
    </style>
""", unsafe_allow_html=True)

# --- FUNCIONES DE FORMATO ---
def formato_moneda(valor):
    return f"$ {valor:,.0f}".replace(",", ".")

# --- MENÚ DE NAVEGACIÓN ---
# Usamos un selectbox en la parte superior para que sea fácil cambiar de sección
seccion = st.selectbox("📍 Ir a:", ["🚀 Nuevo Préstamo (Simulador)", "📅 Agenda de Cobros", "👤 Clientes y Préstamos"])

st.markdown("---")

# ==========================================
# SECCIÓN 1: SIMULADOR
# ==========================================
if seccion == "🚀 Nuevo Préstamo (Simulador)":
    st.header("Simulador de Préstamo")
    
    with st.container():
        nombre = st.text_input("Nombre del Cliente", "Juan Pérez")
        telefono = st.text_input("Celular (ej: 54911...)", "549")
        
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
            fecha_prestamo = st.date_input("Fecha del préstamo", datetime.now())

    # CÁLCULOS
    interes_total = monto * (tasa / 100) * cuotas
    monto_total = monto + interes_total
    valor_cuota = monto_total / cuotas

    st.markdown("---")
    st.subheader(f"📊 Resultados para {nombre}")
    
    # Métricas visibles para el cliente
    col_a, col_b = st.columns(2)
    col_a.metric("Monto Entregado", formato_moneda(monto))
    col_b.metric("Cuotas Totales", f"{int(cuotas)} cuotas")
    
    st.metric("Cuota Mensual", formato_moneda(valor_cuota))

    # Interruptor discreto para ver ganancias
    vista_cliente = st.toggle("Vista simplificada", value=True)
    
    if not vista_cliente:
        st.markdown("#### 🔒 Solo Prestamista")
        c_p1, c_p2 = st.columns(2)
        c_p1.metric("Total a Devolver", formato_moneda(monto_total))
        c_p2.metric("Rendimiento Final", formato_moneda(interes_total), delta=f"{tasa}% mensual")

    st.markdown("---")
    
    # CRONOGRAMA
    st.subheader("📅 Cronograma")
    calendario = []
    for i in range(int(cuotas)):
        fecha_cuota = fecha_prestamo + timedelta(days=(i + 1) * 30)
        calendario.append({
            "N°": i + 1,
            "Vencimiento": fecha_cuota.strftime("%d/%m/%Y"),
            "Monto": formato_moneda(valor_cuota)
        })
    st.table(calendario)

    # ACCIONES
    if st.button("💾 Registrar Préstamo y avisar por WhatsApp"):
        st.warning("⚠️ Aquí se disparará la conexión a Supabase pronto.")
        mensaje_wsp = f"Hola {nombre}, tu préstamo de {formato_moneda(monto)} en {int(cuotas)} cuotas de {formato_moneda(valor_cuota)} ha sido registrado."
        st.success(f"Link de WhatsApp preparado para: {telefono}")

# ==========================================
# SECCIÓN 2: AGENDA DE COBROS
# ==========================================
elif seccion == "📅 Agenda de Cobros":
    st.header("Próximos Cobros")
    st.info("Aquí aparecerán las cuotas que vencen hoy y en los próximos días.")
    
    # Filtros de búsqueda rápidos para el celu
    filtro = st.radio("Ver cuotas:", ["Vencen Hoy", "Próximos 7 días", "Atrasadas (Mora)"], horizontal=True)
    
    # Ejemplo de cómo se vería la mora calculada
    st.markdown("---")
    st.error("🚨 EJEMPLO DE MORA: Cliente Juan Pérez - Cuota 2 (Vencida hace 3 días)")
    st.write("Monto Original: $183.333")
    st.write("Interés por Mora (0.5% diario): $2.750")
    st.subheader("Total a cobrar hoy: $186.083")

# ==========================================
# SECCIÓN 3: CLIENTES Y PRÉSTAMOS
# ==========================================
elif seccion == "👤 Clientes y Préstamos":
    st.header("Historial de Clientes")
    
    buscar_cliente = st.text_input("🔍 Buscar cliente por nombre...")
    
    # Simulación de lista de préstamos
    st.markdown("---")
    with st.expander(f"📂 Ver Préstamos de {buscar_cliente if buscar_cliente else 'Juan Pérez'}"):
        st.write("**Préstamo ID #1024**")
        st.write("Estado: 🟢 ACTIVO")
        st.write("Monto: $1.000.000")
        st.progress(0.33, text="Progreso de pago: 2 de 6 cuotas")
        if st.button("Refinanciar este préstamo"):
            st.info("Iniciando proceso de refinanciación...")














