# Cargar librerías necesarias
library(tidyverse)
library(knitr)
library(kableExtra)
library(scales)
library(janitor)

#Limpieza del dataframe
df <- read.csv("Data/Raw/11. Amazon Sales.csv", encoding = "UTF-8")
df_limpio <- df %>%
  janitor::clean_names() %>%
  
  #Seleccion de variables a utilizar para el estudio
  select(product_id, product_name, category, discounted_price, 
         actual_price, discount_percentage, rating, rating_count, review_title)%>%
  
  # Limpieza de simbolos y comas
  mutate(discounted_price = as.numeric(gsub("[^0-9.]", "", discounted_price)),
         actual_price = as.numeric(gsub("[^0-9.]", "", actual_price)),
         rating = as.numeric(rating), 
         rating_count = as.numeric(gsub(",", "",  rating_count)),
         # Convercion de porcentaje (ej. 50%) a decimal (0.50)
         discount_percentage = as.numeric(gsub("%", "", discount_percentage))/100
  ) 
# Recalculo de porcentajes
df_limpio <- df_limpio %>%
  mutate(discounted_price = actual_price - (actual_price*discount_percentage),
         discounted_price = round(discounted_price, 0))

#Verificacion e imputacion de NA's

df_limpio <- df_limpio %>%
  mutate(rating = replace_na(rating, mean(rating, na.rm = TRUE)), 
         rating_count = replace_na(rating_count, mean(rating_count, na.rm = TRUE))) 


#Elimimacion de Outliers
# Calculo  de límites para 'actual_price' usando IQR
Q1 <- quantile(df_limpio$actual_price, 0.25, na.rm = TRUE)
Q3 <- quantile(df_limpio$actual_price, 0.75, na.rm = TRUE)
IQR_val <- Q3 - Q1

# Definicion de límites
limite_inferior <- Q1 - 1.5 * IQR_val
limite_superior <- Q3 + 1.5 * IQR_val

# Filtracion de datos
df_sin_atipicos <- df_limpio %>%
  filter(actual_price >= limite_inferior & actual_price <= limite_superior)
#Se exporta el dataset limpio
write.csv(df_sin_atipicos, "Data/Clean/data_limpia.csv", row.names = FALSE)