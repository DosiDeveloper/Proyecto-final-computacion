import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats

amazon_palette = ['#00A8E1', '#ff9900', '#232f3e']


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
                only_cat_selected = filtered_df.query(
                    "rating_group in @rating_filter")["rating_group"].cat.remove_unused_categories()
                print(only_cat_selected.cat.reorder_categories(rating_filter).value_counts(ascending=True)[
                    :len(rating_filter)])
                fig1 = px.funnel(y=rating_filter,
                                 x=only_cat_selected.cat.reorder_categories(rating_filter).value_counts(ascending=True)[
                                     :len(rating_filter)],
                                 title="Conteo de productos por grupo de rating seleccionados", color_discrete_sequence=amazon_palette)
            else:
                fig1 = px.funnel(y=filtered_df["rating_group"].cat.categories.tolist(), x=filtered_df["rating_group"].value_counts(
                    ascending=True), title="Conteo de productos por grupo de rating", color_discrete_sequence=amazon_palette)

            fig1.update_traces(textposition="outside",
                               textinfo="percent total+value")
            fig1.update_layout(yaxis_title="Grupo de rating")
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
                "Top 10 categorías con mayor porcentaje de descuento :small_red_triangle:")
            top_discounted_per_category = filtered_df.explode("category").groupby(
                "category")["discount_percentage"].mean().sort_values(ascending=False).head(10)
            st.dataframe(top_discounted_per_category.rename("Porcentaje de descuento promedio").reset_index().rename(columns={
                "category": "Categoría"}))
        with col2:
            st.markdown(
                "Top 10 productos con mejor rating :small_red_triangle:")
            top_rated = filtered_df.sort_values(
                "rating", ascending=False).head(10)
            st.dataframe(top_rated[["product_name", "rating"]].rename(columns={
                "product_name": "Nombre del producto",
                "rating": "Rating"
            }))
        st.link_button("Descargar el informe del proyecto",
                   "https://github.com/DosiDeveloper/Proyecto-final-computacion/blob/master/informe.pdf", icon=":material/info:")

@st.fragment
def graph_tab(filtered_df: pd.DataFrame):
    with st.container():
        local_df = filtered_df.rename(columns={
            "product_name": "Nombre del producto",
            "category": "Categorías",
            "discounted_price": "Precio con descuento (INR)",
            "discount_percentage": "Porcentaje de descuento",
            "actual_price": "Precio real (INR)",
            "rating": "Rating",
            "rating_count": "Conteo de rating",
            "about_product": "Descripción del producto",
            "discount_percentage_group": "Grupo de porcentaje de descuento",
            "rating_group": "Grupo de rating"
        })

        select_dist_item = st.selectbox("Selecciona dos variables para mostrar su distribución, dispersión y correlación", [
                                        "Porcentaje de descuento y Rating", "Precio real (INR) y Rating", "Conteo de rating y Rating", "Precio con descuento (INR) y Rating"], placeholder="Selecciona pares de variables")
        select_segment_item = None
        if st.checkbox("Mostrar segmentos en el gráfico de dispersión"):
            select_segment_item = st.selectbox("Selecciona una segmentacion para mostrar", [
                "Grupo de porcentaje de descuento",
                "Grupo de rating"
            ], placeholder="Selecciona una variable")
        select_dist_item = select_dist_item.split(
            " y ") if select_dist_item else []
        for item in select_dist_item:
            fig1 = go.Figure(go.Histogram(
                x=local_df[item], name=item, marker_color=amazon_palette[0], histnorm="probability density"))
            x_curve = np.linspace(local_df[item].min(
            ), local_df[item].max(), 100)
            y_curve = stats.norm.pdf(x_curve, np.mean(
                local_df[item]), np.std(local_df[item]))
            fig1.add_trace(go.Scatter(x=x_curve, y=y_curve,
                                      mode='lines', name='Normal Curve', line=dict(color=amazon_palette[1])))
            fig1.update_yaxes(showticklabels=False)
            fig1.update_layout(
                title_text=f"Distribución de {item}", xaxis_title_text=item, showlegend=False)
            fig1_box = px.box(
                x=local_df[item], title=f"Boxplot de {item}", color=local_df[select_segment_item] if select_segment_item else None, color_discrete_sequence=px.colors.qualitative.Plotly if select_segment_item else amazon_palette)
            fig1_box.update_layout(
                title_text=f"Boxplot de {item}", xaxis_title_text=item)
            st.plotly_chart(fig1)
            st.plotly_chart(fig1_box)

        fig_scatter = px.scatter(x=local_df[select_dist_item[1]], y=local_df[select_dist_item[0]], title=f"Relación entre {select_dist_item[1]} y {select_dist_item[0]}",
                                 trendline_color_override="#ff9900", trendline=None if select_segment_item else "ols", color=local_df[select_segment_item] if select_segment_item else None, color_discrete_sequence=px.colors.qualitative.Plotly if select_segment_item else amazon_palette)
        fig_scatter.update_layout(
            xaxis_title=select_dist_item[1], yaxis_title=select_dist_item[0])
        st.plotly_chart(fig_scatter)

        with st.expander(label=f"Más información sobre el gráfico", icon=":material/thumb_up:"):
            st.markdown(
                f"#### En el gráfico se muestra la correlación entre el rating y el porcentaje de descuento")
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
            st.write("No es posible calcular el coeficiente de correlación")


@st.fragment
def df_tab(filtered_df: pd.DataFrame, df: pd.DataFrame):
    st.header("Tabla")
    st.dataframe(filtered_df[["product_name", "category", "discounted_price", "discount_percentage", "actual_price", "rating", "rating_count", "about_product"]].rename(columns={
        "product_name": "Nombre del producto",
        "category": "Categorías",
        "discounted_price": "Precio con descuento (INR)",
        "discount_percentage": "Porcentaje de descuento",
        "actual_price": "Precio real (INR)",
        "rating": "Rating",
        "rating_count": "Conteo de rating",
        "about_product": "Descripción del producto",
    }))

    with st.expander(label="¿Cómo se hizo la limpieza de datos?", icon=":material/info:"):
        st.markdown(
            """
            - Se eliminaron las columnas img_link, product_link, review_id, user_name, user_id, review_title y review_content dado que no aportaban información relevante para el análisis y actualmente no existen en el server de Amazon
            - Se parsearon los precios eliminando el símbolo de rupia y las comas para convertirlos a tipo float
            - Se parsearon los porcentajes de descuento eliminando el símbolo de porcentaje para convertirlos a tipo int
            - Se parsearon los ratings convirtiendo los valores no numéricos a NaN y luego rellenando esos NaN con la mediana de los ratings
            - Se parsearon los conteos de rating eliminando las comas, convirtiendo los valores no numéricos a NaN y luego rellenando esos NaN con la mediana de los conteos de rating
            - Se parsearon las categorías dividiendo las cadenas por los caracteres '|' o ',' para convertirlas a listas
            - Se eliminaron los outliers del precio real utilizando el método del rango intercuartílico (IQR)
            - Se recalcularon los precios con descuento a partir de los precios sin outliers""")

        st.link_button("Descargar el dataset sin limpiar",
                       "https://github.com/DosiDeveloper/Proyecto-final-computacion/blob/master/11.%20Amazon%20Sales.pdf", icon=":material/release_alert:")
        st.download_button("Descargar el dataset limpio",
                           df.to_csv().encode("utf-8"), icon=":material/info:", mime="text/csv", file_name="Cleaned Amazon Sales.csv")
        st.download_button("Descargar el dataset segun los filtros aplicados", icon=":material/download:", data=filtered_df.to_csv(
            index=False), file_name="Cleaned and Filtered Amazon Sales.csv", mime="text/csv")
