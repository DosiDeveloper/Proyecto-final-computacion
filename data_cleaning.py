import numpy as np
import pandas as pd


df = pd.read_csv("11. Amazon Sales.csv")
# No hay datos duplicados, pero se eliminan por si acaso
df = df.drop_duplicates()

# Eliminación de las columnas img_link y product_link dado que existen actualmente en el server de Amazon
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


df["category"] = df["category"].str.split(r"[|,]", regex=True)


# eliminando outliers
q1_actual_price = df["actual_price"].quantile(.25)
q3_actual_price = df["actual_price"].quantile(.75)
iqr_actual_price = q3_actual_price - q1_actual_price
lim_inf_actual_price = q1_actual_price - 1.5 * iqr_actual_price
lim_sup_actual_price = q3_actual_price + 1.5 * iqr_actual_price
df = df.query(
    "actual_price >= @lim_inf_actual_price and actual_price <= @lim_sup_actual_price")

list_category = set()
df["category"].apply(lambda x: list_category.update(x))

# Recalculo de los descuentos
df["discounted_price"] = df["actual_price"] - \
    (df["actual_price"] * (df["discount_percentage"]/100))

# segmentación de rating y descuento
percentage_level = ["Sin descuento", "1-20%",
                    "21-40%", "41-60%", "61-80%", "81-100%"]

rating_label = ["Malo", "Regular", "Bueno"]

df["discount_percentage_group"] = pd.cut(
    df["discount_percentage"], bins=[-1, 0, 20, 40, 60, 80, np.inf], labels=percentage_level)
df["rating_group"] = pd.cut(
    df["rating"], [1, 3, 4, 5], labels=rating_label)


if __name__ == "__main__":
    df.to_csv("Cleaned Amazon Sales.csv", index=False)
    print(df.head())
    print(df.info())
