import streamlit as st
import pandas as pd
import os

# Configuration de la page
st.set_page_config(page_title="Projet Scraping - CoinAfrique", layout="wide")
st.title("📊 Projet de Data Collection")

# Menu principal
menu = ["Accueil", "Scraping", "Nettoyage", "Dashboard"]
choice = st.sidebar.selectbox("Menu", menu)

# Dossiers de données
RAW_DATA = "data_clean"
CLEAN_DATA = "data1"

# Page Accueil
if choice == "Accueil":
    st.header("Bienvenue sur mon projet de scraping")
    st.markdown("""
    Cette application permet de :
    - Scraper les données de CoinAfrique
    - Nettoyer les données collectées
    - Visualiser les résultats
    """)

# Page Scraping
elif choice == "Scraping":
    st.header("Scraping des données")
    
    # Simulation de scraping (à remplacer par votre vrai code)
    if st.button("Lancer le scraping"):
        # Ici vous devriez appeler votre fonction de scraping
        # Pour l'exemple, on crée des données fictives
        sample_data = {
            'type': ['habits', 'chaussures'],
            'titre': ['T-shirt', 'Baskets'],
            'prix': [10000, 25000],
            'adresse': ['Dakar', 'Thiès']
        }
        df = pd.DataFrame(sample_data)
        
        # Sauvegarde des données brutes
        os.makedirs(RAW_DATA, exist_ok=True)
        df.to_csv(f"{RAW_DATA}/donnees_brutes.csv", index=False)
        st.success("Scraping terminé avec succès!")
        st.dataframe(df)

# Page Nettoyage
elif choice == "Nettoyage":
    st.header("Nettoyage des données")
    
    # Simulation de nettoyage
    if st.button("Nettoyer les données"):
        try:
            # Lecture des données brutes
            df = pd.read_csv(f"{RAW_DATA}/donnees_brutes.csv")
            
            # Nettoyage simple (à adapter)
            df['prix'] = pd.to_numeric(df['prix'], errors='coerce')
            df = df.dropna()
            
            # Sauvegarde des données nettoyées
            os.makedirs(CLEAN_DATA, exist_ok=True)
            df.to_csv(f"{CLEAN_DATA}/donnees_nettoyees.csv", index=False)
            st.success("Données nettoyées avec succès!")
            st.dataframe(df)
        except:
            st.warning("Veuillez d'abord scraper des données")

# Page Dashboard
elif choice == "Dashboard":
    st.header("Visualisation des données")
    
    try:
        # Chargement des données nettoyées
        df = pd.read_csv(f"{CLEAN_DATA}/donnees_nettoyees.csv")
        
        # Affichage simple
        st.subheader("Aperçu des données")
        st.dataframe(df)
        
        # Statistiques basiques
        st.subheader("Statistiques")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Nombre d'articles", len(df))
        with col2:
            st.metric("Prix moyen", f"{df['prix'].mean():.0f} FCFA")
        
        # Graphique simple
        st.bar_chart(df['type'].value_counts())
    except:
        st.warning("Veuillez d'abord nettoyer les données")