import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
df = df.drop(columns=["img_link", "product_link"])

# Parse de los precios
df["discounted_price"] = (df["discounted_price"].str.replace(
    "₹", "")).str.replace(",", "").astype(float)
df["actual_price"] = (df["actual_price"].str.replace(
    "₹", "")).str.replace(",", "").astype(float)

# Parse de los porcentajes de descuento
df["discount_percentage"] = df["discount_percentage"].str.replace("%", "").astype(int)

# Parse de rating
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["rating"] = df["rating"].fillna(df["rating"].dropna().median())

df["rating_count"] = df["rating_count"].str.replace(",", "").fillna(
    df["rating_count"].dropna().str.replace(",", "").astype(int).median()).astype(int)

# Recalculo de los descuentos
df["discounted_price"] = df["actual_price"] - (df["actual_price"] * (df["discount_percentage"]/100))

df["category"] = df["category"].str.split(r"[|,]", regex=True)

# eliminando outlier
q1_actual_price = df["actual_price"].quantile(.25)
q3_actual_price = df["actual_price"].quantile(.75)
iqr_actual_price = q3_actual_price - q1_actual_price
lim_inf_actual_price = q1_actual_price - 1.5 * iqr_actual_price
lim_sup_actual_price = q3_actual_price + 1.5 * iqr_actual_price
df = df.query("actual_price >= @lim_inf_actual_price and actual_price <= @lim_sup_actual_price")

list_category = set()
df["category"].apply(lambda x: list_category.update(x))

