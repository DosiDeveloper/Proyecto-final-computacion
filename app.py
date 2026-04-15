import os
from pathlib import Path
import streamlit as st
from streamlit_theme import st_theme
import pandas as pd
import plotly.io as pio

from fragments import df_tab, graph_tab, resume_tab
from scripts.data_cleaning import list_category, percentage_level, rating_label

# config
st.set_page_config(layout="wide", page_title="Análisis de Ventas Amazon",)
st.column_config.NumberColumn(format="localized")

# cargar en cache el dataset


@st.cache_data
def load_dataset():
    try:
        load_df_clean = pd.read_csv(
            Path("Data").resolve() / "Clean" / "Cleaned Amazon Sales.csv")
        load_df_clean["category"] = load_df_clean["category"].map(
            lambda x: eval(x) if isinstance(x, str) else x)
        load_df_clean["discount_percentage_group"] = load_df_clean["discount_percentage_group"].astype(
            "category").cat.set_categories(percentage_level, ordered=True)
        load_df_clean["rating_group"] = load_df_clean["rating_group"].astype(
            "category").cat.set_categories(rating_label, ordered=True)
        load_df_clean["discount_percentage_group"] = load_df_clean["discount_percentage_group"].astype(
            "category")
        return load_df_clean
    except FileNotFoundError:
        st.error("El dataset no se ha encontrado", icon=":material/error")


df = load_dataset()

filtered_df = df.copy()

col1, col2 = st.columns([1, 5], vertical_alignment="center")

actual_theme = st_theme()


if actual_theme is not None and actual_theme.get("base") == "light":
    st.logo("./static/Amazon_logo_black.png", size="large",
            icon_image="./static/Amazon_icon_black.png")
    col1.container(horizontal_alignment="center").image(
        "./static/Amazon_logo_black.png", width=300)
    pio.templates.default = "plotly_white"

else:
    st.logo("./static/Amazon_logo_white.png", size="large",
            icon_image="./static/Amazon_icon_white.png")
    col1.container(horizontal_alignment="center").image(
        "./static/Amazon_logo_white.png", width=300)
    pio.templates.default = "plotly_dark"

col2.title("Análisis de Amazon Sales", text_alignment="center")
st.space("small")


with st.sidebar:
    st.subheader("Filtros")
    filtered_category = st.multiselect(
        "Categorías", sorted(list_category), placeholder="Seleccione una categoría")
    # filtros básicos

    filtered_discount_qcut = st.multiselect(
        "Filtro de porcentaje de descuento por intervalo", percentage_level,  placeholder="Seleccione un intervalo de descuento")
    filtered_df = filtered_df.query("discount_percentage_group in @filtered_discount_qcut") if len(
        filtered_discount_qcut) > 0 else filtered_df

    filtered_rating_qcut = st.multiselect(
        "Filtro de rating por nivel", rating_label,  placeholder="Seleccione un nivel de rating")
    filtered_df = filtered_df[filtered_df["rating_group"].isin(
        filtered_rating_qcut)] if len(filtered_rating_qcut) > 0 else filtered_df
    # filtros "avanzados"
    if filtered_category != []:
        filtered_df = filtered_df[filtered_df["category"].apply(
            lambda x: not set(filtered_category).isdisjoint(x))]
    if not len(filtered_df["category"]) > 2:
        st.warning("Muy pocas filas para filtrar")
    elif st.checkbox("Filtros avanzados"):
        filtered_rating_start, filtered_rating_end = st.slider(
            "Elija el rating", df["rating"].min(), df["rating"].max(), value=(filtered_df["rating"].min(), filtered_df["rating"].max()))
        filtered_df = filtered_df.query(
            "@filtered_rating_start <= rating and @filtered_rating_end >= rating")

        filtered_rating_count_start, filtered_rating_count_end = st.slider(
            "Elija la cantidad de reviews", df["rating_count"].min(), df["rating_count"].max(), value=(filtered_df["rating_count"].min(), filtered_df["rating_count"].max()))
        filtered_df = filtered_df.query(
            "@filtered_rating_count_start <= rating_count and @filtered_rating_count_end >= rating_count")

        filtered_actual_price_start, filtered_actual_price_end = st.slider(
            "Elija el precio real (INR)", df["actual_price"].min(), df["actual_price"].max(), value=(filtered_df["actual_price"].min(), filtered_df["actual_price"].max()))
        filtered_df = filtered_df.query(
            "@filtered_actual_price_start <= actual_price and @filtered_actual_price_end >= actual_price")

        filtered_discounted_price_start, filtered_discounted_price_end = st.slider(
            "Elija el precio con descuento (INR)", df["discounted_price"].min(), df["discounted_price"].max(), value=(filtered_df["discounted_price"].min(), filtered_df["discounted_price"].max()))
        filtered_df = filtered_df.query(
            "@filtered_discounted_price_start <= discounted_price and @filtered_discounted_price_end >= discounted_price")


tab_resume, tab_graph, tab_df = st.tabs(
    [":globe_with_meridians: Resumen", ":chart_with_upwards_trend: Gráfico", ":blue_book: Ver tabla"])

with tab_resume:
    resume_tab(filtered_df, df, rating_filter=filtered_rating_qcut)
with tab_graph:
    graph_tab(filtered_df)

with tab_df:
    df_tab(filtered_df, df)
