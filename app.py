import streamlit as st
import pandas as pd
from scraping import scrape_all_urls
from utils import clean_data, display_dashboard

st.set_page_config(page_title="Web Scraper App", layout="wide")

st.title("🕸️ Web Scraper App – CoinAfrique")

# Menu
menu = ["Accueil", "Scraper des données", "Télécharger données brutes", "Dashboard", "Évaluer l'app"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Accueil":
    st.markdown("### Bienvenue dans l'application de scraping CoinAfrique !")
    st.markdown("- Scraping de plusieurs pages")
    st.markdown("- Visualisation et nettoyage de données")
    st.markdown("- Téléchargement de données Web Scraper")
    st.markdown("- Dashboard interactif")

elif choice == "Scraper des données":
    st.subheader("🔍 Scraper les données CoinAfrique")

    if st.button("Lancer le scraping (12 pages)"):
        data = scrape_all_urls()
        df = pd.DataFrame(data)
        df_clean = clean_data(df)
        df_clean.to_csv("data/cleaned_data.csv", index=False)
        st.success("Scraping terminé et données nettoyées enregistrées !")
        st.dataframe(df_clean.head())

elif choice == "Télécharger données brutes":
    st.subheader("📥 Données brutes de Web Scraper")
    uploaded_file = st.file_uploader("Uploader un fichier CSV ou JSON exporté depuis Web Scraper", type=["csv", "json"])

    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            df_raw = pd.read_csv(uploaded_file)
        else:
            df_raw = pd.read_json(uploaded_file)
        st.write("Aperçu des données brutes :")
        st.dataframe(df_raw.head())
        st.download_button("Télécharger données brutes", df_raw.to_csv(index=False), file_name="raw_webscraper.csv")

elif choice == "Dashboard":
    st.subheader("📊 Dashboard – Données nettoyées")
    try:
        df_cleaned = pd.read_csv("data/cleaned_data.csv")
        display_dashboard(df_cleaned)
    except FileNotFoundError:
        st.warning("Aucune donnée nettoyée trouvée. Lancez le scraping d'abord.")

elif choice == "Évaluer l'app":
    st.subheader("📝 Formulaire d’évaluation")
    nom = st.text_input("Votre nom")
    note = st.slider("Note de l’application", 1, 10)
    avis = st.text_area("Donnez votre avis")

    if st.button("Soumettre"):
        with open("feedback.txt", "a", encoding="utf-8") as f:
            f.write(f"Nom: {nom}, Note: {note}, Avis: {avis}\n")
        st.success("Merci pour votre retour 🙏")

