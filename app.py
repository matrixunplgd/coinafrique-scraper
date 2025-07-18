import streamlit as st
import pandas as pd
from scraper import scrape_category
from utils import clean_data, display_dashboard

st.set_page_config(page_title="Exam - Web Scraper App", layout="wide")

st.title("📦 Application Web Scraping – CoinAfrique")

menu = [
    "Accueil",
    "1️⃣ Scraper avec BeautifulSoup",
    "2️⃣ Télécharger des données Web Scraper",
    "3️⃣ Dashboard (Nettoyé)",
    "4️⃣ Évaluation via Kobotools"
]

choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Accueil":
    st.markdown("### Bienvenue dans l'application CoinAfrique Scraper")
    st.markdown("Vous pouvez :")
    st.markdown("- Scraper les données avec BeautifulSoup")
    st.markdown("- Télécharger les données Web Scraper")
    st.markdown("- Visualiser un dashboard")
    st.markdown("- Remplir un formulaire d’évaluation")

# Option 1 – Scraping
elif choice == "1️⃣ Scraper avec BeautifulSoup":
    st.subheader("🔍 Scraper les données")
    st.markdown("Choisissez une catégorie et le nombre de pages à scraper")

    categories = {
        "Chaussures Enfants": "https://sn.coinafrique.com/categorie/chaussures-enfants",
        "Chaussures Hommes": "https://sn.coinafrique.com/categorie/chaussures-homme",
        "Vêtements Enfants": "https://sn.coinafrique.com/categorie/vetements-enfants",
        "Vêtements Hommes": "https://sn.coinafrique.com/categorie/vetements-homme"
    }

    selected_category = st.radio("Choisissez une catégorie", list(categories.keys()))
    page_count = st.number_input("Nombre de pages à scraper", min_value=1, max_value=20, value=5)

    if st.button("Lancer le scraping"):
        url = categories[selected_category]
        type_article = "chaussures" if "Chaussures" in selected_category else "habits"
        data = scrape_category(url, type_article, page_count)
        df = pd.DataFrame(data)
        st.dataframe(df.head())
        filename = f"data_clean/{selected_category.lower().replace(' ', '_')}.csv"
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        st.success(f"Scraping terminé. Données enregistrées dans : `{filename}`")

# Option 2 – Télécharger fichier Web Scraper
elif choice == "2️⃣ Télécharger des données Web Scraper":
    st.subheader("📥 Données Web Scraper")
    fichier = st.selectbox("Choisir un fichier brut à télécharger", [
        "chaussures_enfants.csv",
        "vetements_enfants.csv",
        "chaussures_hommes.csv",
        "vetements_hommes.csv"
    ])

    try:
        df = pd.read_csv(f"data1/{fichier}")
        st.dataframe(df.head())
        st.download_button("📤 Télécharger le fichier", df.to_csv(index=False), file_name=fichier)
    except:
        st.warning("Fichier introuvable.")

# Option 3 – Dashboard
elif choice == "3️⃣ Dashboard (Nettoyé)":
    st.subheader("📊 Dashboard des données nettoyées")
    try:
        df_clean = pd.read_csv("data_clean/cleaned_data.csv")
        display_dashboard(df_clean)
    except:
        st.warning("Aucune donnée nettoyée trouvée.")

# Option 4 – Kobotools
elif choice == "4️⃣ Évaluation via Kobotools":
    st.subheader("📝 Formulaire d’évaluation")
    kobotools_url ="https://ee.kobotoolbox.org/i/WoLHl7cc"  
    st.markdown(f"[Cliquez ici pour remplir le formulaire]({kobotools_url})")
