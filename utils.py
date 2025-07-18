import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------------------------------
# 1. Fonction de nettoyage des données
# -----------------------------------------------

def clean_data(input_path, output_path=None):
    try:
        df = pd.read_csv(input_path)

        # Nettoyage de base
        df.dropna(how='all', inplace=True)  # Supprimer lignes vides
        df.drop_duplicates(inplace=True)    # Supprimer doublons

        # Nettoyer les prix s'ils existent
        if "prix" in df.columns:
            df["prix"] = df["prix"].astype(str).str.replace(r"[^\d]", "", regex=True)
            df["prix"] = pd.to_numeric(df["prix"], errors="coerce")
            df = df[df["prix"] > 0]  # On garde que les prix positifs

        # Nettoyer les noms de colonnes
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df.to_csv(output_path, index=False, encoding="utf-8-sig")

        return df

    except Exception as e:
        st.error(f"Erreur lors du nettoyage : {e}")
        return pd.DataFrame()


# -----------------------------------------------
# 2. Dashboard des données nettoyées
# -----------------------------------------------

def display_dashboard(df):
    st.markdown("## 📊 Dashboard interactif")
    
    st.markdown("### 🔍 Aperçu rapide des données")
    st.dataframe(df.head())

    st.markdown("### 📈 Statistiques sur les prix")

    try:
        # Nettoyage de la colonne 'prix'
        df_clean = df.copy()
        df_clean = df_clean[df_clean['prix'].str.contains("CFA", na=False)]
        df_clean = df_clean[~df_clean['prix'].str.contains("Prix sur demande", case=False, na=False)]

        # Supprimer les caractères inutiles et convertir en nombre
        df_clean["prix_num"] = df_clean["prix"].str.replace("CFA", "", regex=False)
        df_clean["prix_num"] = df_clean["prix_num"].str.replace(" ", "", regex=False)
        df_clean["prix_num"] = pd.to_numeric(df_clean["prix_num"], errors="coerce")

        # Supprimer les valeurs NaN
        df_clean = df_clean.dropna(subset=["prix_num"])

        # Afficher les statistiques
        st.metric("Prix moyen", f"{int(df_clean['prix_num'].mean()):,} CFA")
        st.metric("Prix minimum", f"{int(df_clean['prix_num'].min()):,} CFA")
        st.metric("Prix maximum", f"{int(df_clean['prix_num'].max()):,} CFA")

        st.bar_chart(df_clean["prix_num"])
    
    except Exception as e:
        st.error(f"❌ Une erreur est survenue : {e}")
