import streamlit as st
import pandas as pd
import os
import zipfile
from scraper import scrape_category
from utils import clean_data, display_dashboard

# -----------------------------
# Configuration globale
# -----------------------------
st.set_page_config(page_title="Web Scraper App - CoinAfrique", layout="wide")
st.title("📦 Application Web Scraping – CoinAfrique")

DATA_RAW = "data_clean"
DATA_CLEAN = "data1"

# -----------------------------
# Menu
# -----------------------------
menu = [
    "Accueil",
    "1️⃣ Scraper les données (data_clean)",
    "2️⃣ Nettoyer les données (→ data1)",
    "3️⃣ Télécharger les données",
    "4️⃣ Dashboard",
    "5️⃣ Formulaire Kobotools"
]
choice = st.sidebar.selectbox("Navigation", menu)

# -----------------------------
# 0. Accueil
# -----------------------------
if choice == "Accueil":
    st.header("Bienvenue 👋")
    st.markdown("Cette application permet de scraper CoinAfrique, nettoyer les données, et explorer les résultats via un dashboard.")

# -----------------------------
# 1. Scraper les données brutes
# -----------------------------
elif choice == "1️⃣ Scraper les données (data_clean)":
    st.subheader("🔍 Scraping CoinAfrique")

    categories = {
        "Chaussures Enfants": "https://sn.coinafrique.com/categorie/chaussures-enfants",
        "Chaussures Hommes": "https://sn.coinafrique.com/categorie/chaussures-homme",
        "Vêtements Enfants": "https://sn.coinafrique.com/categorie/vetements-enfants",
        "Vêtements Hommes": "https://sn.coinafrique.com/categorie/vetements-homme"
    }

    selected_category = st.radio("Choisir une catégorie", list(categories.keys()))
    page_count = st.slider("Nombre de pages à scraper", 1, 20, 5)

    if st.button("🚀 Lancer le scraping"):
        url = categories[selected_category]
        type_article = "chaussures" if "Chaussures" in selected_category else "habits"
        df = scrape_category(url, type_article, page_count)

        if not df.empty:
            st.dataframe(df.head())
            os.makedirs(DATA_RAW, exist_ok=True)
            file_name = selected_category.lower().replace(" ", "_") + ".csv"
            raw_path = f"{DATA_RAW}/{file_name}"
            df.to_csv(raw_path, index=False, encoding="utf-8-sig")
            st.success(f"✅ Fichier sauvegardé dans `{raw_path}`")
        else:
            st.warning("⚠️ Aucune donnée trouvée.")

# -----------------------------
# 2. Nettoyer les données
# -----------------------------
elif choice == "2️⃣ Nettoyer les données (→ data1)":
    st.subheader("🧹 Nettoyage des fichiers bruts")

    try:
        files = [f for f in os.listdir(DATA_RAW) if f.endswith(".csv")]
        fichier = st.selectbox("Sélectionnez un fichier à nettoyer", files)

        if st.button("🧼 Nettoyer le fichier sélectionné"):
            input_path = f"{DATA_RAW}/{fichier}"
            output_path = f"{DATA_CLEAN}/{fichier}"
            cleaned_df = clean_data(input_path, output_path)

            if not cleaned_df.empty:
                st.success(f"✅ Données nettoyées sauvegardées dans `{output_path}`")
                st.dataframe(cleaned_df.head())
            else:
                st.warning("⚠️ Fichier vide ou erreur de nettoyage.")
    except FileNotFoundError:
        st.warning(f"⚠️ Aucun fichier trouvé dans `{DATA_RAW}`.")

# -----------------------------
# 3. Télécharger les données
# -----------------------------
elif choice == "3️⃣ Télécharger les données":
    st.subheader("📥 Télécharger les fichiers nettoyés (data1)")

    try:
        files = [f for f in os.listdir(DATA_CLEAN) if f.endswith(".csv")]
        fichier = st.selectbox("Choisir un fichier à télécharger", files)

        file_path = f"{DATA_CLEAN}/{fichier}"
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            st.dataframe(df.head())
            st.download_button("📤 Télécharger ce fichier", df.to_csv(index=False), file_name=fichier)
        else:
            st.warning("⚠️ Fichier introuvable.")
        
        # ✅ Télécharger tous les fichiers en ZIP
        if st.button("📦 Télécharger tous les fichiers en ZIP"):
            zip_path = "fichiers_nettoyes.zip"
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for file in files:
                    zipf.write(os.path.join(DATA_CLEAN, file), arcname=file)
            with open(zip_path, "rb") as f:
                st.download_button("⬇️ Télécharger le ZIP", f, file_name=zip_path)
            os.remove(zip_path)
    except FileNotFoundError:
        st.warning(f"⚠️ Aucun fichier trouvé dans `{DATA_CLEAN}`.")

# -----------------------------
# 4. Dashboard
# -----------------------------
elif choice == "4️⃣ Dashboard":
    st.subheader("📊 Visualisation des données nettoyées")

    try:
        files = [f for f in os.listdir(DATA_CLEAN) if f.endswith(".csv")]
        fichier = st.selectbox("Choisir un fichier à visualiser", files)

        if fichier:
            df_clean = pd.read_csv(os.path.join(DATA_CLEAN, fichier))
            display_dashboard(df_clean)
    except FileNotFoundError:
        st.warning(f"⚠️ Aucun fichier trouvé dans `{DATA_CLEAN}`.")
    except Exception as e:
        st.error(f"❌ Une erreur est survenue : {e}")

# -----------------------------
# 5. Kobotools
# -----------------------------
elif choice == "5️⃣ Formulaire Kobotools":
    st.subheader("📝 Évaluation via Kobotools")

    st.components.v1.html(
        """
        <iframe src="https://ee.kobotoolbox.org/i/WoLHl7cc" width="50%" height="600" frameborder="0"></iframe>
        """,
        height=650,
        scrolling=True
    )
