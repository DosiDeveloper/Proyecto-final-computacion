from threading import local

from matplotlib import legend
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

amazon_palette = ['#00A8E1', '#ff9900',
                  '#f3ece1', '#12130F', '#232f3e', '#f2f2f2']


@st.fragment
def resume_tab(filtered_df: pd.DataFrame, df: pd.DataFrame, rating_filter):
    with st.container():
        col1, col2, col3, col4 = st.columns(4, vertical_alignment="center")
        col1.metric("Precio con descuento promedio",
                    f"₹ {filtered_df["discounted_price"].mean():,.2f}",
                    border=True, format="localized", delta=filtered_df["discounted_price"].mean() - df["discounted_price"].mean(), delta_description="Comparado con el promedio general")
        col2.metric("Rating promedio",
                    filtered_df["rating"].mean(),
                    border=True, format="localized", delta=round(filtered_df["rating"].mean() - df["rating"].mean(), 2), delta_description="Comparado con el promedio general")
        col3.metric("Conteo de rating promedio",
                    filtered_df["rating_count"].mean(),
                    border=True, format="localized", delta=round(filtered_df["rating_count"].mean() - df["rating_count"].mean(), 2), delta_description="Comparado con el promedio general")

        col4.metric("Conteo de productos", len(filtered_df),
                    border=True, format="localized", delta=len(filtered_df) - len(df), delta_description="Comparado con el conteo general")

        col_g1, col_g2 = st.columns(2, vertical_alignment="center")
        with col_g1:
            if rating_filter != []:
                only_cat_selected = filtered_df.loc[filtered_df["rating_group"].isin(
                    filtered_df["rating_group"].cat.remove_unused_categories())].groupby("rating_group", observed=True)["rating_group"].value_counts()
                fig1 = px.pie(names=rating_filter, values=only_cat_selected,
                              title="Conteo de productos por grupo de rating", color_discrete_sequence=amazon_palette)
            else:
                fig1 = px.pie(names=list(filtered_df["rating_group"].cat.categories), values=filtered_df["rating_group"].value_counts(
                    ascending=True), title="Conteo de productos por grupo de rating", color_discrete_sequence=amazon_palette)

            fig1.update_traces(textposition="inside",
                               textinfo="percent+label")
            st.plotly_chart(fig1)

        with col_g2:
            fig2 = px.histogram(x=filtered_df["discount_percentage"],
                                title="Conteo de productos por rango de descuento", color_discrete_sequence=amazon_palette)
            fig2.update_layout(
                bargap=0.2, xaxis_title="Porcentaje de descuento", yaxis_title="Conteo de productos")
            st.plotly_chart(fig2)

        col1, col2 = st.columns(2, vertical_alignment="center")
        with col1:
            st.markdown(
                "Top 10 categorias con mayor porcentaje de descuento :small_red_triangle:")
            top_discounted_per_category = filtered_df.explode("category").groupby(
                "category")["discount_percentage"].mean().sort_values(ascending=False).head(10)
            st.dataframe(top_discounted_per_category.rename("Porcentaje de descuento promedio").reset_index().rename(columns={
                "category": "Categoria"}))
        with col2:
            st.markdown(
                "Top 10 productos con mejor rating :small_red_triangle:")
            top_rated = filtered_df.sort_values(
                "rating", ascending=False).head(10)
            st.dataframe(top_rated[["product_name", "rating"]].rename(columns={
                "product_name": "Nombre del producto",
                "rating": "Rating"
            }))


@st.fragment
def graph_tab(filtered_df: pd.DataFrame):
    with st.container():
        local_df = filtered_df.rename(columns={
            "product_name": "Nombre del producto",
            "category": "Categorias",
            "discounted_price": "Precio con descuento (INR)",
            "discount_percentage": "Porcentaje de descuento",
            "actual_price": "Precio real (INR)",
            "rating": "Rating",
            "rating_count": "Conteo de rating",
            "about_product": "Descripcion del producto",
        })
        select_dist_item = st.multiselect("Selecciona dos variables para graficar", [
            "Porcentaje de descuento", "Rating", "Precio real (INR)", "Precio con descuento (INR)", "Conteo de rating"], default=["Porcentaje de descuento", "Rating"], placeholder="Selecciona dos variables", max_selections=2)
        if len(select_dist_item) == 0:
            st.warning(
                "Selecciona al menos una variable para mostrar su distribución, dispersion y correlación")
            return
        if len(select_dist_item) == 1:
            fig1 = px.histogram(
                local_df[select_dist_item[0]], title=f"Distribución de {select_dist_item[0]}", color_discrete_sequence=amazon_palette)
            st.plotly_chart(fig1)
            return
        fig1 = make_subplots(rows=1, cols=2, subplot_titles=[
            f"Distribución de {select_dist_item[0]}", f"Distribución de {select_dist_item[1]}"])
        fig1.add_trace(go.Histogram(
            x=local_df[select_dist_item[0]], name=select_dist_item[0], marker_color=amazon_palette[0]), row=1, col=1)
        fig1.add_trace(go.Histogram(
            x=local_df[select_dist_item[1]], name=select_dist_item[1], marker_color=amazon_palette[1]), row=1, col=2)
        fig1.update_layout(bargap=0.2)
        fig1.update_layout(
            title_text=f"Distribucion de {select_dist_item[0]} y {select_dist_item[1]}", showlegend=False)

        st.plotly_chart(fig1)

        st.plotly_chart(px.scatter(x=local_df[select_dist_item[0]], y=local_df[select_dist_item[1]], title=f"Relacion entre {select_dist_item[0]} y {select_dist_item[1]}",
                        color_discrete_sequence=amazon_palette, trendline_color_override="#ff9900", trendline="ols").update_layout(xaxis_title=select_dist_item[0], yaxis_title=select_dist_item[1]))
        with st.expander(label=f"Mas informacion sobre el grafico", icon=":material/thumb_up:"):
            st.markdown(
                f"#### En el grafico se muestra la correlacion entre el rating y el porcentaje de descuento")
            corr_rating_percentage = local_df[[select_dist_item[0], select_dist_item[1]]].corr()[
                select_dist_item[0]].iloc[1]
            if not (np.isnan(corr_rating_percentage)):
                if corr_rating_percentage >= 0:
                    st.write(
                        f"Directamente proporcional con un: {corr_rating_percentage:.2%}")
                else:
                    st.write(
                        f"Inversamente proporcional con un: {corr_rating_percentage:.2%}")
                return
            st.write("No es posible calcular el coeficiente de correlacion")


@st.fragment
def df_tab(filtered_df: pd.DataFrame):
    st.header("Tabla")
    st.dataframe(filtered_df[["product_name", "category", "discounted_price", "discount_percentage", "actual_price", "rating", "rating_count", "about_product"]].rename(columns={
        "product_name": "Nombre del producto",
        "category": "Categorias",
        "discounted_price": "Precio con descuento (INR)",
        "discount_percentage": "Porcentaje de descuento",
        "actual_price": "Precio real (INR)",
        "rating": "Rating",
        "rating_count": "Conteo de rating",
        "about_product": "Descripcion del producto",
    }))
