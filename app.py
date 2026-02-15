import streamlit as st
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(page_title="Sistema de Préstamos", page_icon="💰", layout="wide")

# --- FUNCIONES DE FORMATO ---
def formato_moneda(valor):
    # Formato con puntos de miles para que sea legible
    return f"$ {valor:,.0f}".replace(",", ".")

# Título principal
st.title("💰 Simulador de Préstamos Profesional")
st.markdown("---")

# --- BARRA LATERAL (Entradas de datos) ---
with st.sidebar:
    st.header("📋 Datos del Préstamo")
    nombre = st.text_input("Nombre del Cliente", "Juan Pérez")
    
    # Nuevo: Campo para el teléfono de WhatsApp
    telefono = st.text_input("Celular del Cliente (ej: 54911...)", "549")
    
    monto = st.number_input("Monto a entregar ($)", min_value=0, value=1000000, step=50000)
    # AYUDA VISUAL DE PUNTOS DE MILES
    st.write(f"Monto ingresado: **{formato_moneda(monto)}**")
    
    tasa = st.number_input("Tasa de Interés Mensual (%)", min_value=0.0, value=10.0, step=0.5)
    cuotas = st.number_input("Cantidad de Cuotas (Meses)", min_value=1, value=6, step=1)
    
    # La fecha_inicio ahora se toma como el día del préstamo (Hoy)
    # para que las cuotas se calculen a partir del mes que viene.
    fecha_prestamo = st.date_input("Fecha del préstamo (Hoy)", datetime.now(), format="DD/MM/YYYY")

# --- CÁLCULOS ---
interes_total = monto * (tasa / 100) * cuotas
monto_total = monto + interes_total
valor_cuota = monto_total / cuotas

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
    # LÓGICA: La primera cuota (i=0) será en 30 días
    dias_a_sumar = (i + 1) * 30
    fecha_cuota = fecha_prestamo + timedelta(days=dias_a_sumar)
    
    calendario.append({
        "N° Cuota": i + 1,
        "Fecha de Vencimiento": fecha_cuota.strftime("%d/%m/%Y"),
        "Monto de Cuota": formato_moneda(valor_cuota),
        "Estado": "⏳ Pendiente"
    })

# Mostrar la tabla
st.table(calendario)

# --- BOTÓN DE WHATSAPP REAL ---
st.markdown("---")
# Creamos el mensaje para el link de WhatsApp
mensaje_url = f"Hola {nombre}, te envío el cronograma de tu préstamo de {formato_moneda(monto)}. Las cuotas mensuales son de {formato_moneda(valor_cuota)}."
# Reemplazamos espacios para que el link funcione
link_wsp = f"https://wa.me/{telefono}?text={mensaje_url.replace(' ', '%20')}"

st.info("💡 Próximo paso: Conectar con Base de Datos para guardar estos registros.")

# Creamos dos columnas para el botón
col_btn, _ = st.columns([1, 2])
with col_btn:
    if st.link_button("📱 Enviar Plan por WhatsApp", link_wsp):
        st.write("Abriendo WhatsApp...")



