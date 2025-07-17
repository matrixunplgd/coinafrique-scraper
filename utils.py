import pandas as pd
import streamlit as st

def clean_data(df):
    df = df.drop_duplicates()
    df["prix"] = df["prix"].str.replace("FCFA", "").str.replace(" ", "").str.replace("\u202f", "")
    df["prix"] = pd.to_numeric(df["prix"], errors='coerce')
    return df

def display_dashboard(df):
    st.write("### Nombre total d’annonces :", len(df))
    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(df["type"].value_counts())
    with col2:
        st.line_chart(df.groupby("type")["prix"].mean())
    st.map(df.dropna(subset=["adresse"]))
