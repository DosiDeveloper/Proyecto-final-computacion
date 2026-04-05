import logging
import os
import streamlit as st
import pandas as pd

from fragments import df_tab, graph_tab, resume_tab

# config
st.set_page_config(layout="wide", page_title="Analisis de Ventas Amazon",)
st.column_config.NumberColumn(format="localized")

# cargar en cache el dataset


@st.cache_data
def load_dataset():
    try:
        load_df = pd.read_csv(os.path.abspath("Cleaned Amazon Sales.csv"))
        return load_df
    except FileNotFoundError as e:
        st.error("El dataset no se ha encontrado", icon=":material/error")


df = load_dataset()

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
percentage_level = ["0-20%", "20-40%", "40-60%", "60-80%", "80-100%"]
rating_label = ["malisimo", "malo", "regular", "bueno", "muy bueno"]


with st.sidebar:
    st.subheader("Filtros")
    filtered_category = st.multiselect(
        "Categorias", sorted(list_category), placeholder="Selecciones una categoria")
    # filtros basicos
    filtered_df["discount_percentage_group"] = pd.cut(filtered_df["discount_percentage"], bins=[-1, 20, 40, 60, 80, 100], labels=percentage_level)
    filtered_discount_qcut = st.multiselect("Filtro de porcentaje de descuento por level", percentage_level)
    filtered_df = filtered_df[filtered_df["discount_percentage_group"].isin(filtered_discount_qcut)] if len(filtered_discount_qcut) > 0 else filtered_df
    
    filtered_df["rating_group"] = pd.qcut(filtered_df["rating"], 5, labels = rating_label)    
    filtered_rating_qcut = st.multiselect("Filtro de rating por level", rating_label )
    filtered_df = filtered_df[filtered_df["rating_group"].isin(filtered_rating_qcut)] if len(filtered_rating_qcut) > 0 else filtered_df
    # filtros "avanzados"
    if filtered_category != []:
            filtered_df = filtered_df[filtered_df["category"].apply(
                lambda x: not set(filtered_category).isdisjoint(x))]
    if not len(filtered_df["category"]) > 2:
            st.warning("Muy pocas filas para filtrar")
    elif st.checkbox("Filtros avanzados"):
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
    resume_tab(filtered_df, df, rating_filter=filtered_rating_qcut)
    st.link_button("Informe del proyecto", "https://github.com/DosiDeveloper/Proyecto-final-computacion/blob/master/informe.pdf", icon=":material/info:")


with tab_graph:
    graph_tab(filtered_df, filtered_category)

with tab_df:
    df_tab(filtered_df)

