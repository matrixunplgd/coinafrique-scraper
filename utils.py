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

    # Aperçu des données
    st.write("### Aperçu rapide des données")
    st.dataframe(df.head())

    # Statistiques descriptives
    st.write("### Statistiques sur les prix")
    if "prix" in df.columns:
        col1, col2, col3 = st.columns(3)
        col1.metric("Prix Moyen", f"{df['prix'].mean():,.0f} FCFA")
        col2.metric("Min", f"{df['prix'].min():,.0f} FCFA")
        col3.metric("Max", f"{df['prix'].max():,.0f} FCFA")

        # Histogramme des prix
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(df["prix"], bins=30, kde=True, ax=ax, color="skyblue")
        ax.set_title("Distribution des prix")
        ax.set_xlabel("Prix (FCFA)")
        st.pyplot(fig)
    else:
        st.warning("La colonne `prix` est absente dans le fichier.")

    # Catégories si présentes
    for col in ["ville", "titre", "categorie", "nom"]:
        if col in df.columns:
            st.write(f"### Top valeurs dans : `{col}`")
            st.dataframe(df[col].value_counts().head(10))

