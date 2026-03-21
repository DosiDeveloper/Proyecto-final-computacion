import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.fragment
def resume_tab(filtered_df: pd.DataFrame):
    with st.container():
        col1, col2, col3, col4 = st.columns(4, vertical_alignment="center")
        col1.metric("Precio con descuento promedio",
                    f"₹ {filtered_df["discounted_price"].mean():.2f}", border=True)
        col2.metric("Rating promedio",
                    round(filtered_df["rating"].mean(), 2), border=True)
        col3.metric("Conteo de rating promedio",
                    round(filtered_df["rating_count"].mean(), 2), border=True)
        
        col4.metric("Conteo de productos", len(filtered_df), border=True)
        st.write("Grafico importante aqui xd")
        col1, col2 = st.columns(2, vertical_alignment="center")
        with col1:
            st.markdown("Top 10 categorias con mayor porcentaje de descuento :small_red_triangle:")
            top_discounted_per_category = filtered_df.explode("category").groupby("category")["discount_percentage"].mean().sort_values(ascending=False).head(10)
            st.dataframe(top_discounted_per_category.rename("Porcentaje de descuento promedio").reset_index().rename(columns={
                "category": "Categoria"}))
        with col2:
            st.markdown("Top 10 productos con mejor rating :small_red_triangle:")
            top_rated = filtered_df.sort_values("rating", ascending=False).head(10)
            st.dataframe(top_rated[["product_name", "rating"]].rename(columns={
                "product_name": "Nombre del producto",
                "rating": "Rating"
            }))
        
    
@st.fragment
def graph_tab(filtered_df: pd.DataFrame, filtered_category):
    with st.container():
        fig = px.histogram(filtered_df, x="discount_percentage",
                           title="Distribución del porcentaje de descuento")
        fig.update_layout(xaxis_title="Porcentaje de descuento (%)",
                          yaxis_title="Cantidad de productos")
        st.plotly_chart(fig)
        fig2 = px.histogram(filtered_df, x="rating",
                            title="Distribución de los ratings") 
        fig2.update_layout(xaxis_title="Rating",
                          yaxis_title="Cantidad de productos")   
        st.plotly_chart(fig2)
        fig1 = px.scatter(filtered_df, x="actual_price", y="rating", 
                         title="Relación entre precio real y el rating", trendline="ols", trendline_color_override="red")
        fig1.update_layout(xaxis_title="precio real (INR)", yaxis_title="Rating")
        st.plotly_chart(fig1)
        with st.expander(label=f"Mas informacion sobre el grafico", icon=":material/thumb_up:"):
            st.markdown(f"#### En el grafico se muestra la correlacion entre el rating y el precio actual en {"las categorias seleccionadas" if len(filtered_category) > 0 else "todas las categorias o en la categoria seleccionada"}")
            corr_rating_percentage = filtered_df[["rating", "actual_price"]].corr()["actual_price"][0]
            if not (np.isnan(corr_rating_percentage)):
                if corr_rating_percentage >= 0:
                    st.write(f"Directamente proporcional con un: {corr_rating_percentage:.2%}")
                else:
                    st.write(f"Inversamente proporcional con un: {corr_rating_percentage:.2%}")
            else:
                st.write("No es posible calcular el coeficiente de correlacion")

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
