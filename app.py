import streamlit as st
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(page_title="Sistema de Préstamos", page_icon="💰")

# --- FUNCIONES DE FORMATO ---
def formato_moneda(valor):
    return f"$ {valor:,.0f}".replace(",", ".")

# Título principal
st.title("💰 Simulador de Préstamos")

# --- SECCIÓN DE ENTRADA (Directo en la pantalla principal para celular) ---
st.subheader("📋 Cargar Datos")

nombre = st.text_input("Nombre del Cliente", "Juan Pérez")
telefono = st.text_input("Celular del Cliente (ej: 54911...)", "549")

# Usamos columnas para que en PC se vea a la par, pero en celular se apilan solo
c1, c2 = st.columns(2)
with c1:
    monto = st.number_input("Monto a entregar ($)", min_value=0, value=1000000, step=50000)
    st.write(f"Monto: **{formato_moneda(monto)}**")
with c2:
    tasa = st.number_input("Tasa Interés Mensual (%)", min_value=0.0, value=10.0, step=0.5)

c3, c4 = st.columns(2)
with c3:
    cuotas = st.number_input("Cuotas (Meses)", min_value=1, value=6, step=1)
with c4:
    fecha_prestamo = st.date_input("Fecha del préstamo", datetime.now(), format="DD/MM/YYYY")

st.markdown("---")

# --- CÁLCULOS ---
interes_total = monto * (tasa / 100) * cuotas
monto_total = monto + interes_total
valor_cuota = monto_total / cuotas

# --- RESULTADOS PRINCIPALES (Tarjetas grandes) ---
st.subheader(f"👤 Resumen: {nombre}")

# En celular, estas 4 métricas se verán una debajo de otra, bien grandes
st.metric("Monto Entregado", formato_moneda(monto))
st.metric("Cuota Mensual", formato_moneda(valor_cuota))
st.metric("Total a Devolver", formato_moneda(monto_total))
st.metric("Tu Ganancia", formato_moneda(interes_total), delta=f"{tasa}% mensual")

st.markdown("---")

# --- TABLA DE PAGOS ---
st.subheader("📅 Cronograma")
calendario = []
for i in range(int(cuotas)):
    dias_a_sumar = (i + 1) * 30
    fecha_cuota = fecha_prestamo + timedelta(days=dias_a_sumar)
    
    calendario.append({
        "N°": i + 1,
        "Vencimiento": fecha_cuota.strftime("%d/%m/%Y"),
        "Cuota": formato_moneda(valor_cuota)
    })

st.table(calendario)

# --- BOTÓN DE WHATSAPP ---
mensaje_url = f"Hola {nombre}, te envío el cronograma de tu préstamo de {formato_moneda(monto)}. Las cuotas mensuales son de {formato_moneda(valor_cuota)}."
link_wsp = f"https://wa.me/{telefono}?text={mensaje_url.replace(' ', '%20')}"

# Botón ancho completo para que sea fácil de tocar con el pulgar
st.link_button("📱 Enviar por WhatsApp", link_wsp, use_container_width=True)





