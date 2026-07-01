import streamlit as st
import datetime
import plotly.graph_objects as go

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Dashboard de Ahorro", page_icon="💰", layout="wide")

st.title("🎯 Mi Dashboard Interactivo de Ahorro")
st.markdown("Ingresa tus ahorros en el menú de la izquierda para actualizar el gráfico automáticamente.")

# ==========================================
# CONSTANTES DE TU META
# ==========================================
META_TOTAL = 7355216
AHORRO_INICIAL = 135000
FECHA_INICIO = datetime.date(2026, 7, 1)
FECHA_FIN = datetime.date(2027, 5, 20)

# ==========================================
# SISTEMA DE MEMORIA (Session State)
# ==========================================
if 'fechas' not in st.session_state:
    st.session_state.fechas = [FECHA_INICIO]
    st.session_state.ahorros = [AHORRO_INICIAL]

# ==========================================
# INTERFAZ DE USUARIO (Formulario de Ingreso)
# ==========================================
with st.sidebar:
    st.header("📝 Registrar Nuevo Ahorro")
    
    fecha_input = st.date_input("Fecha del ahorro:", value=datetime.date.today())
    cantidad_input = st.number_input("Cantidad ahorrada ($):", min_value=0, step=10000)
    
    if st.button("Guardar Ahorro"):
        if cantidad_input > 0:
            nuevo_total = st.session_state.ahorros[-1] + cantidad_input
            st.session_state.fechas.append(fecha_input)
            st.session_state.ahorros.append(nuevo_total)
            st.success("¡Ahorro registrado con éxito!")
        else:
            st.warning("Por favor ingresa una cantidad mayor a 0.")

# ==========================================
# CÁLCULOS DE PROGRESO Y ESTADO
# ==========================================
ahorro_actual = st.session_state.ahorros[-1]
fecha_actual = st.session_state.fechas[-1]

dias_totales = (FECHA_FIN - FECHA_INICIO).days
dias_transcurridos = (fecha_actual - FECHA_INICIO).days
dias_restantes = (FECHA_FIN - datetime.date.today()).days

ahorro_diario_necesario = (META_TOTAL - AHORRO_INICIAL) / dias_totales
ahorro_ideal_hoy = AHORRO_INICIAL + (ahorro_diario_necesario * dias_transcurridos)

# ==========================================
# VISUALIZACIÓN: MÉTRICAS Y ALERTAS
# ==========================================
col1, col2, col3 = st.columns(3)

col1.metric("Ahorro Actual", f"${ahorro_actual:,.0f}")
col2.metric("Dinero Faltante", f"${(META_TOTAL - ahorro_actual):,.0f}")
col3.metric("Días Restantes", f"{dias_restantes} días")

if ahorro_actual >= ahorro_ideal_hoy:
    st.success(f"🟢 **¡Todo está melo!** Llevas un excelente ritmo. El ahorro ideal para hoy era ${ahorro_ideal_hoy:,.0f}.")
else:
    atraso = ahorro_ideal_hoy - ahorro_actual
    st.error(f"🔴 **Alerta:** Estás un poco atrasado. Te faltan ${atraso:,.0f} para igualar la meta proyectada de hoy.")

st.progress(min(ahorro_actual / META_TOTAL, 1.0))
st.write(f"**Progreso Total:** {(ahorro_actual / META_TOTAL) * 100:.2f}% completado")

# ==========================================
# VISUALIZACIÓN: GRÁFICO INTERACTIVO (PLOTLY)
# ==========================================
st.markdown("---")
st.subheader("📈 Proyección vs. Realidad")

fechas_proyectadas = [FECHA_INICIO + datetime.timedelta(days=i) for i in range(dias_totales + 1)]
ahorro_proyectado = [AHORRO_INICIAL + (ahorro_diario_necesario * i) for i in range(dias_totales + 1)]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=fechas_proyectadas, y=ahorro_proyectado,
    mode='lines', name='Meta Proyectada',
    line=dict(dash='dash', color='rgba(150, 150, 150, 0.8)')
))

fig.add_trace(go.Scatter(
    x=st.session_state.fechas, y=st.session_state.ahorros,
    mode='lines+markers', name='Tu Ahorro Real',
    line=dict(color='#007BFF', width=3),
    marker=dict(size=8, color='#0056b3')
))

fig.update_layout(
    xaxis_title="Fechas",
    yaxis_title="Dinero ($)",
    hovermode="x unified",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)
