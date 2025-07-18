import pandas as pd
import os

def clean_data(input_file, output_file):
    """Nettoie les données et les sauvegarde dans data1/"""
    try:
        df = pd.read_csv(input_file)

        # Exemple : enlever les doublons et les lignes vides
        df.drop_duplicates(inplace=True)
        df.dropna(subset=['titre', 'prix'], inplace=True)

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        return df
    except Exception as e:
        print(f"Erreur nettoyage : {e}")
        return pd.DataFrame()
