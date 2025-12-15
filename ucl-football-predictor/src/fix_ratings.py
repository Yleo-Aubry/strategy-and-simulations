import pandas as pd
import os


FILE_PATH = "data/raw/ratings.csv"


CORRECTIONS = {
    "Slavia Praha": "Slavia Prague",
    "Kobenhavn": "Copenhagen",
    "Athletic": "Athletic Club",
    "Kairat": "Kairat Almaty",
    "Bodo Glimt": "Bodo/Glimt",
    "Olympiakos": "Olympiacos",  
    "Frankfurt": "Frankfurt"     
}

def fix_csv():
    if not os.path.exists(FILE_PATH):
        print(f"❌ Erreur : Le fichier {FILE_PATH} est introuvable.")
        return

    # Lecture du CSV (avec le bon séparateur)
    df = pd.read_csv(FILE_PATH, sep=';')
    
    print("📋 Avant correction :")
    print(df[df['team_name'].isin(CORRECTIONS.keys())])

    # Application des corrections
    # On remplace les valeurs dans la colonne 'team_name'
    df['team_name'] = df['team_name'].replace(CORRECTIONS)
    
    # Sauvegarde en écrasant l'ancien fichier
    df.to_csv(FILE_PATH, index=False, sep=';', encoding='utf-8-sig')
    
    print("\n✅ Fichier corrigé et sauvegardé !")
    print("📋 Après correction (Vérification) :")
    # On vérifie que les nouveaux noms sont bien là
    check_names = list(CORRECTIONS.values())
    print(df[df['team_name'].isin(check_names)])

if __name__ == "__main__":
    fix_csv()
