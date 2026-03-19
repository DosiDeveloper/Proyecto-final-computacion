import os
import streamlit as st
import pandas as pd

from fragments import df_tab, graph_tab, resume_tab

# config
st.set_page_config(layout="wide", page_title="Analisis de Ventas Amazon",)


# cargar en cache el dataset


@st.cache_data
def load_dataset():
    try:
        load_df = pd.read_csv(os.path.abspath("11. Amazon Sales.csv"))
        return load_df
    except FileNotFoundError as e:
        st.error("El dataset no se ha encontrado", icon=":material/error")


raw_df = load_dataset()

# No hay datos duplicados, pero se eliminan por si acaso
df = raw_df.drop_duplicates()

# Eliminacion de las columnas img_link y product_link dado que existen actualmente en el server de Amazon
df = df.drop(columns=["img_link", "product_link", "review_id",
             "user_name", "user_id", "review_title", "review_content"])

# Parse de los precios
df["discounted_price"] = (df["discounted_price"].str.replace(
    "₹", "")).str.replace(",", "").astype(float)
df["actual_price"] = (df["actual_price"].str.replace(
    "₹", "")).str.replace(",", "").astype(float)

# Parse de los porcentajes de descuento
df["discount_percentage"] = df["discount_percentage"].str.replace(
    "%", "").astype(int)

# Parse de rating
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["rating"] = df["rating"].fillna(df["rating"].dropna().median())

df["rating_count"] = df["rating_count"].str.replace(",", "").fillna(
    df["rating_count"].dropna().str.replace(",", "").astype(int).median()).astype(int)

# Recalculo de los descuentos
df["discounted_price"] = df["actual_price"] - \
    (df["actual_price"] * (df["discount_percentage"]/100))

df["category"] = df["category"].str.split(r"[|,]", regex=True)

# eliminando outlier
q1_actual_price = df["actual_price"].quantile(.25)
q3_actual_price = df["actual_price"].quantile(.75)
iqr_actual_price = q3_actual_price - q1_actual_price
lim_inf_actual_price = q1_actual_price - 1.5 * iqr_actual_price
lim_sup_actual_price = q3_actual_price + 1.5 * iqr_actual_price
df = df.query(
    "actual_price >= @lim_inf_actual_price and actual_price <= @lim_sup_actual_price")

list_category = set()
df["category"].apply(lambda x: list_category.update(x))

filtered_df = df.copy()

# UI

col1, col2 = st.columns([1, 5], vertical_alignment="center")
if st.context.theme.type == "light":
    st.logo("./static/Amazon_logo_black.png", size="large",
            icon_image="./static/Amazon_icon_black.png")
    col1.container(horizontal_alignment="center").image(
        "./static/Amazon_logo_black.png", width=300)
else:
    st.logo("./static/Amazon_logo_white.png", size="large",
            icon_image="./static/Amazon_icon_white.png")
    col1.container(horizontal_alignment="center").image(
        "./static/Amazon_logo_white.png", width=300)
col2.title("Analisis de Amazon Sales", text_alignment="center")
st.space("small")


with st.sidebar:
    st.subheader("Filtros")
    filtered_category = st.multiselect(
        "Categorias", sorted(list_category), placeholder="Selecciones una categoria")
    if filtered_category != []:
        filtered_df = filtered_df[filtered_df["category"].apply(
            lambda x: not set(x).isdisjoint(filtered_category))]
    if not len(filtered_df["category"]) > 2:
        st.write("Muy pocas filas para filtrar")
    else:
        filtered_rating_start, filtered_rating_end = st.slider(
            "Eliga el rating", filtered_df["rating"].min(), filtered_df["rating"].max(), value=(filtered_df["rating"].min(), filtered_df["rating"].max()))
        filtered_df = filtered_df.query(
            "@filtered_rating_start <= rating and @filtered_rating_end >= rating")

        filtered_rating_count_start, filtered_rating_count_end = st.slider(
            "Eliga la cantidad de reviews", filtered_df["rating_count"].min(), filtered_df["rating_count"].max(), value=(filtered_df["rating_count"].min(), filtered_df["rating_count"].max()))
        filtered_df = filtered_df.query(
            "@filtered_rating_count_start <= rating_count and @filtered_rating_count_end >= rating_count")


tab_resume, tab_graph, tab_df = st.tabs(
    [":globe_with_meridians: Resumen", ":chart_with_upwards_trend: Grafico", ":blue_book: Ver tabla"])

with tab_resume:
    resume_tab(filtered_df)


with tab_graph:
    graph_tab(filtered_df)

with tab_df:
    df_tab(filtered_df)
