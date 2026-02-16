import streamlit as st
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(page_title="Sistema de Préstamos", page_icon="💰", layout="wide")

# --- FUNCIONES DE FORMATO ---
def formato_moneda(valor):
    return f"$ {valor:,.0f}".replace(",", ".")

# Título principal
st.title("💰 Simulador de Préstamos Profesional")
st.markdown("---")

# --- BARRA LATERAL (Entradas de datos) ---
with st.sidebar:
    st.header("📋 Datos del Préstamo")
    nombre = st.text_input("Nombre del Cliente", "Juan Pérez")
    telefono = st.text_input("Celular del Cliente (ej: 54911...)", "549")
    monto = st.number_input("Monto a entregar ($)", min_value=0, value=1000000, step=50000)
    st.write(f"Monto ingresado: **{formato_moneda(monto)}**")
    tasa = st.number_input("Tasa de Interés Mensual (%)", min_value=0.0, value=10.0, step=0.5)
    cuotas = st.number_input("Cantidad de Cuotas (Meses)", min_value=1, value=6, step=1)
    fecha_prestamo = st.date_input("Fecha del préstamo (Hoy)", datetime.now(), format="DD/MM/YYYY")

# --- CÁLCULOS ---
interes_total = monto * (tasa / 100) * cuotas
monto_total = monto + interes_total
valor_cuota = monto_total / cuotas

# --- RESULTADOS PRINCIPALES (Organizados en bloques para evitar cortes) ---
st.subheader(f"👤 Resumen para: {nombre}")

# BLOQUE 1: Datos de entrega y plazos
st.markdown("#### 📥 Detalles de Entrega")
col_a, col_b = st.columns(2)
with col_a:
    st.metric("Monto Entregado", formato_moneda(monto))
with col_b:
    st.metric("Cuotas Totales", f"{int(cuotas)} meses")

# BLOQUE 2: Datos de cobro y ganancia
st.markdown("#### 📤 Detalles de Cobro")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Cuota Mensual", formato_moneda(valor_cuota))
with col2:
    st.metric("Total a Devolver", formato_moneda(monto_total))
with col3:
    st.metric("Tu Ganancia", formato_moneda(interes_total), delta=f"{tasa}% mensual")

st.markdown("---")

# --- TABLA DE PAGOS ---
st.subheader("📅 Cronograma de Pagos")

calendario = []
for i in range(int(cuotas)):
    dias_a_sumar = (i + 1) * 30
    fecha_cuota = fecha_prestamo + timedelta(days=dias_a_sumar)
    
    calendario.append({
        "N°": i + 1,
        "Vencimiento": fecha_cuota.strftime("%d/%m/%Y"),
        "Monto Cuota": formato_moneda(valor_cuota)
    })

# Usamos st.table para que se vea estático y profesional
st.table(calendario)

# --- BOTÓN DE WHATSAPP ---
st.markdown("---")
mensaje_url = f"Hola {nombre}, te envío el cronograma de tu préstamo de {formato_moneda(monto)} en {int(cuotas)} cuotas de {formato_moneda(valor_cuota)}."
link_wsp = f"https://wa.me/{telefono}?text={mensaje_url.replace(' ', '%20')}"

st.link_button("📱 Enviar Plan por WhatsApp", link_wsp, use_container_width=True)







