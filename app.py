import streamlit as st
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(page_title="Sistema de Préstamos", page_icon="💰", layout="wide")

# Título principal
st.title("💰 Simulador de Préstamos Profesional")
st.markdown("---")

# --- BARRA LATERAL (Entradas de datos) ---
with st.sidebar:
    st.header("📋 Datos del Préstamo")
    nombre = st.text_input("Nombre del Cliente", "Juan Pérez")
    monto = st.number_input("Monto a entregar ($)", min_value=0, value=1000000, step=50000)
    tasa = st.number_input("Tasa de Interés Mensual (%)", min_value=0.0, value=10.0, step=0.5)
    cuotas = st.number_input("Cantidad de Cuotas (Meses)", min_value=1, value=6, step=1)
    fecha_inicio = st.date_input("Fecha del primer pago", datetime.now())

# --- CÁLCULOS ---
# Usamos Interés Fijo (Simple) que es el estándar para préstamos rápidos
interes_total = monto * (tasa / 100) * cuotas
monto_total = monto + interes_total
valor_cuota = monto_total / cuotas

# --- FUNCIONES DE FORMATO ---
def formato_moneda(valor):
    # Formato con puntos de miles para que sea legible
    return f"$ {valor:,.0f}".replace(",", ".")

# --- RESULTADOS PRINCIPALES ---
st.subheader(f"👤 Cliente: {nombre}")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Cuota Mensual", formato_moneda(valor_cuota))
with col2:
    st.metric("Total a Devolver", formato_moneda(monto_total))
with col3:
    st.metric("Tu Ganancia", formato_moneda(interes_total), delta=f"{tasa}% mensual")

st.markdown("---")

# --- TABLA DE PAGOS (CALENDARIO) ---
st.subheader("📅 Cronograma de Pagos")

calendario = []
for i in range(int(cuotas)):
    # Calculamos la fecha de cada cuota (sumando 30 días aprox. por mes)
    fecha_cuota = fecha_inicio + timedelta(days=i*30)
    
    calendario.append({
        "N° Cuota": i + 1,
        "Fecha de Vencimiento": fecha_cuota.strftime("%d/%m/%Y"),
        "Monto de Cuota": formato_moneda(valor_cuota),
        "Estado": "⏳ Pendiente"
    })

# Mostrar la tabla
st.table(calendario)

# --- BOTÓN DE WHATSAPP (SIMULADO) ---
# Esto genera un link que podrías usar para avisar al cliente
st.markdown("---")
mensaje_wsp = f"Hola {nombre}, tu plan de préstamo de {formato_moneda(monto)} ha sido generado. Cuotas de {formato_moneda(valor_cuota)}."
st.info("💡 Próximo paso: Conectar con Base de Datos para guardar estos registros.")

if st.button("📱 Simular Aviso por WhatsApp"):
    st.success(f"Mensaje preparado para {nombre}: '{mensaje_wsp}'")
