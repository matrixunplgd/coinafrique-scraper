import pandas as pd
import streamlit as st

def clean_data(df):
    df = df.drop_duplicates()
    df["prix"] = df["prix"].str.replace("FCFA", "").str.replace(" ", "").str.replace("\u202f", "")
    df["prix"] = pd.to_numeric(df["prix"], errors='coerce')
    return df

def display_dashboard(df):
    st.metric("Nombre total d'annonces", len(df))
    st.bar_chart(df["type"].value_counts())

    if "prix" in df.columns:
        st.line_chart(df.groupby("type")["prix"].mean())

    if "adresse" in df.columns:
        st.map(df.dropna(subset=["adresse"]))
