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


