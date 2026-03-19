import streamlit as st
import seaborn as sns
import pandas as pd

@st.fragment
def resume_tab(filtered_df: pd.DataFrame):
    resume_container = st.container()
    with resume_container:
        col1, col2, col3, col4 = st.columns(4, vertical_alignment="center")
        col1.metric("Precio con descuento promedio",
                    f"₹ {filtered_df["discounted_price"].mean():.2f}", border=True)
        col2.metric("Rating promedio",
                    round(filtered_df["rating"].mean(), 2), border=True)
        col3.metric("Conteo de rating promedio",
                    round(filtered_df["rating_count"].mean(), 2), border=True)
        col4.metric("Conteo de productos", len(filtered_df), border=True)
        st.write("graph")

@st.fragment
def graph_tab(filtered_df: pd.DataFrame):
    graph_container = st.container()
    with graph_container:
        st.write("graph")


@st.fragment
def df_tab(filtered_df: pd.DataFrame):
    st.header("Tabla")
    st.dataframe(filtered_df.rename(columns={
        "product_name": "Nombre del producto",
        "category": "Categorias",
        "discounted_price": "Precio con descuento (INR)",
        "discount_percentage": "Porcentaje de descuento",
        "actual_price": "Precio real (INR)",
        "rating": "Rating",
        "rating_count": "Conteo de rating",
        "about_product": "Descripcion del producto",
    }))
