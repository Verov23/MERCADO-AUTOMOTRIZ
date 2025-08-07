import streamlit as st
import pandas as pd
import plotly.express as px

# =======================
# CONFIGURACIÓN DE PÁGINA
# =======================
st.set_page_config(page_title="Vehículos más vendidos en EE.UU.",
                   page_icon="🚗",
                   layout="wide")

# =======================
# CARGA DE DATOS
# =======================
@st.cache_data
def load_data():
    df = pd.read_csv("vehicles_us.csv")
    df.drop_duplicates(inplace=True)
    df = df.dropna(subset=["price", "model_year", "odometer", "transmission", "model"])
    df = df[(df["price"] > 100) & (df["price"] < 200000)]
    df = df[(df["model_year"] >= 1980) & (df["model_year"] <= 2025)]
    return df

df = load_data()

# =======================
# TÍTULO PRINCIPAL
# =======================
st.title("🚗 Vehículos más vendidos en Estados Unidos a través de los años")
st.markdown("""
Explora las tendencias del mercado automotriz en Estados Unidos con datos interactivos.
Puedes filtrar por año, transmisión y rango de precios.
""")

# =======================
# FILTROS LATERALES
# =======================
st.sidebar.header("Filtros")
year_range = st.sidebar.slider("Año del modelo", int(df["model_year"].min()), int(df["model_year"].max()), 
                                (2000, 2020))
price_range = st.sidebar.slider("Rango de precios", int(df["price"].min()), int(df["price"].max()), 
                                 (5000, 50000))
transmission_filter = st.sidebar.multiselect("Tipo de transmisión", options=df["transmission"].unique(),
                                              default=df["transmission"].unique())

# Aplicar filtros
df_filtered = df[
    (df["model_year"].between(year_range[0], year_range[1])) &
    (df["price"].between(price_range[0], price_range[1])) &
    (df["transmission"].isin(transmission_filter))
]

# =======================
# GRÁFICOS
# =======================
col1, col2 = st.columns(2)

with col1:
    fig_hist = px.histogram(df_filtered, x="price", nbins=50, 
                            title="Distribución de precios",
                            color_discrete_sequence=["skyblue"])
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    top_models = df_filtered["model"].value_counts().head(10)
    fig_bar = px.bar(top_models, x=top_models.index, y=top_models.values,
                     labels={'x': 'Modelo', 'y': 'Cantidad de anuncios'},
                     title="Top 10 modelos más vendidos",
                     color=top_models.index,
                     color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig_bar, use_container_width=True)

# Gráfico de dispersión
fig_scatter = px.scatter(df_filtered, x="model_year", y="price",
                         color="transmission",
                         title="Precio vs Año del Modelo",
                         labels={"model_year": "Año del Modelo", "price": "Precio"},
                         hover_data=["model"])
st.plotly_chart(fig_scatter, use_container_width=True)

# =======================
# BOTÓN DE DESCARGA
# =======================
st.download_button("📥 Descargar datos filtrados", df_filtered.to_csv(index=False), "datos_filtrados.csv")


