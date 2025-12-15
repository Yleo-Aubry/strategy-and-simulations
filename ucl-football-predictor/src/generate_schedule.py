import pandas as pd
import os

# 1. CONFIGURATION DES ÉQUIPES (Saison 2025-2026)
TEAM_CONFIG = {
    "Arsenal": "ARS", "Bayern": "BAY", "Paris SG": "PSG", "Man City": "MCI",
    "Atalanta": "ATA", "Inter": "INT", "Real Madrid": "RMA", "Atletico": "ATM",
    "Liverpool": "LIV", "Dortmund": "DOR", "Tottenham": "TOT", "Newcastle": "NEW",
    "Chelsea": "CHE", "Sporting": "SPO", "Barcelona": "BAR", "Marseille": "OM",
    "Juventus": "JUV", "Galatasaray": "GAL", "Monaco": "ASM", "Leverkusen": "LEV",
    "PSV": "PSV", "Qarabag": "QAR", "Napoli": "NAP", "Copenhagen": "COP",
    "Benfica": "BEN", "Pafos": "PAF", "Union SG": "USG", "Athletic Club": "BIL",
    "Olympiacos": "OLY", "Frankfurt": "SGE", "Club Brugge": "BRU", "Bodo/Glimt": "BOD",
    "Slavia Prague": "SLA", "Ajax": "AJA", "Villarreal": "VIL", "Kairat Almaty": "KAI"
}

# 2. LISTE DES MATCHS COMPLETE
raw_matches = [
    # --- JOURNÉE 1 (16-18 Septembre 2025) ---
    {"round": 1, "home": "Athletic Club", "away": "Arsenal", "score_home": 0, "score_away": 2, "played": True},
    {"round": 1, "home": "PSV", "away": "Union SG", "score_home": 1, "score_away": 3, "played": True},
    {"round": 1, "home": "Tottenham", "away": "Villarreal", "score_home": 1, "score_away": 0, "played": True},
    {"round": 1, "home": "Benfica", "away": "Qarabag", "score_home": 2, "score_away": 3, "played": True},
    {"round": 1, "home": "Juventus", "away": "Dortmund", "score_home": 4, "score_away": 4, "played": True},
    {"round": 1, "home": "Real Madrid", "away": "Marseille", "score_home": 2, "score_away": 1, "played": True},
    {"round": 1, "home": "Slavia Prague", "away": "Bodo/Glimt", "score_home": 2, "score_away": 2, "played": True},
    {"round": 1, "home": "Olympiacos", "away": "Pafos", "score_home": 0, "score_away": 0, "played": True},
    {"round": 1, "home": "Ajax", "away": "Inter", "score_home": 0, "score_away": 2, "played": True},
    {"round": 1, "home": "Paris SG", "away": "Atalanta", "score_home": 4, "score_away": 0, "played": True},
    {"round": 1, "home": "Liverpool", "away": "Atletico", "score_home": 3, "score_away": 2, "played": True},
    {"round": 1, "home": "Bayern", "away": "Chelsea", "score_home": 3, "score_away": 1, "played": True},
    {"round": 1, "home": "Copenhagen", "away": "Leverkusen", "score_home": 2, "score_away": 2, "played": True},
    {"round": 1, "home": "Club Brugge", "away": "Monaco", "score_home": 4, "score_away": 1, "played": True},
    {"round": 1, "home": "Frankfurt", "away": "Galatasaray", "score_home": 5, "score_away": 1, "played": True},
    {"round": 1, "home": "Sporting", "away": "Kairat Almaty", "score_home": 4, "score_away": 1, "played": True},
    {"round": 1, "home": "Man City", "away": "Napoli", "score_home": 2, "score_away": 0, "played": True},
    {"round": 1, "home": "Newcastle", "away": "Barcelona", "score_home": 1, "score_away": 2, "played": True},

    # --- JOURNÉE 2 (30 Septembre - 1 Octobre 2025) ---
    {"round": 2, "home": "Atalanta", "away": "Club Brugge", "score_home": 2, "score_away": 1, "played": True},
    {"round": 2, "home": "Pafos", "away": "Bayern", "score_home": 1, "score_away": 5, "played": True},
    {"round": 2, "home": "Bodo/Glimt", "away": "Tottenham", "score_home": 2, "score_away": 2, "played": True},
    {"round": 2, "home": "Galatasaray", "away": "Liverpool", "score_home": 1, "score_away": 0, "played": True},
    {"round": 2, "home": "Chelsea", "away": "Benfica", "score_home": 1, "score_away": 0, "played": True},
    {"round": 2, "home": "Kairat Almaty", "away": "Real Madrid", "score_home": 0, "score_away": 5, "played": True},
    {"round": 2, "home": "Marseille", "away": "Ajax", "score_home": 4, "score_away": 0, "played": True},
    {"round": 2, "home": "Atletico", "away": "Frankfurt", "score_home": 5, "score_away": 1, "played": True},
    {"round": 2, "home": "Inter", "away": "Slavia Prague", "score_home": 3, "score_away": 0, "played": True},
    {"round": 2, "home": "Union SG", "away": "Newcastle", "score_home": 0, "score_away": 4, "played": True},
    {"round": 2, "home": "Napoli", "away": "Sporting", "score_home": 2, "score_away": 1, "played": True},
    {"round": 2, "home": "Arsenal", "away": "Olympiacos", "score_home": 2, "score_away": 0, "played": True},
    {"round": 2, "home": "Leverkusen", "away": "PSV", "score_home": 1, "score_away": 1, "played": True},
    {"round": 2, "home": "Monaco", "away": "Man City", "score_home": 2, "score_away": 2, "played": True},
    {"round": 2, "home": "Qarabag", "away": "Copenhagen", "score_home": 2, "score_away": 0, "played": True},
    {"round": 2, "home": "Dortmund", "away": "Athletic Club", "score_home": 4, "score_away": 1, "played": True},
    {"round": 2, "home": "Villarreal", "away": "Juventus", "score_home": 2, "score_away": 2, "played": True},
    {"round": 2, "home": "Barcelona", "away": "Paris SG", "score_home": 1, "score_away": 2, "played": True},
    
    # --- JOURNÉE 3 (21-22 Octobre 2025) ---
    {"round": 3, "home": "Barcelona", "away": "Olympiacos", "score_home": 6, "score_away": 1, "played": True},
    {"round": 3, "home": "Union SG", "away": "Inter", "score_home": 0, "score_away": 4, "played": True},
    {"round": 3, "home": "Copenhagen", "away": "Dortmund", "score_home": 2, "score_away": 4, "played": True},
    {"round": 3, "home": "PSV", "away": "Napoli", "score_home": 6, "score_away": 2, "played": True},
    {"round": 3, "home": "Newcastle", "away": "Benfica", "score_home": 3, "score_away": 0, "played": True},
    {"round": 3, "home": "Kairat Almaty", "away": "Pafos", "score_home": 0, "score_away": 0, "played": True},
    {"round": 3, "home": "Villarreal", "away": "Man City", "score_home": 0, "score_away": 2, "played": True},
    {"round": 3, "home": "Arsenal", "away": "Atletico", "score_home": 4, "score_away": 0, "played": True},
    {"round": 3, "home": "Leverkusen", "away": "Paris SG", "score_home": 2, "score_away": 7, "played": True},
    {"round": 3, "home": "Galatasaray", "away": "Bodo/Glimt", "score_home": 3, "score_away": 1, "played": True},
    {"round": 3, "home": "Chelsea", "away": "Ajax", "score_home": 5, "score_away": 1, "played": True},
    {"round": 3, "home": "Sporting", "away": "Marseille", "score_home": 2, "score_away": 1, "played": True},
    {"round": 3, "home": "Frankfurt", "away": "Liverpool", "score_home": 1, "score_away": 5, "played": True},
    {"round": 3, "home": "Monaco", "away": "Tottenham", "score_home": 0, "score_away": 0, "played": True},
    {"round": 3, "home": "Athletic Club", "away": "Qarabag", "score_home": 3, "score_away": 1, "played": True},
    {"round": 3, "home": "Real Madrid", "away": "Juventus", "score_home": 1, "score_away": 0, "played": True},
    {"round": 3, "home": "Atalanta", "away": "Slavia Prague", "score_home": 0, "score_away": 0, "played": True},
    {"round": 3, "home": "Bayern", "away": "Club Brugge", "score_home": 4, "score_away": 0, "played": True},

    # --- JOURNÉE 4 (4-5 Novembre 2025) ---
    {"round": 4, "home": "Slavia Prague", "away": "Arsenal", "score_home": 0, "score_away": 3, "played": True},
    {"round": 4, "home": "Napoli", "away": "Frankfurt", "score_home": 0, "score_away": 0, "played": True},
    {"round": 4, "home": "Paris SG", "away": "Bayern", "score_home": 1, "score_away": 2, "played": True},
    {"round": 4, "home": "Atletico", "away": "Union SG", "score_home": 3, "score_away": 1, "played": True},
    {"round": 4, "home": "Juventus", "away": "Sporting", "score_home": 1, "score_away": 1, "played": True},
    {"round": 4, "home": "Liverpool", "away": "Real Madrid", "score_home": 1, "score_away": 0, "played": True},
    {"round": 4, "home": "Bodo/Glimt", "away": "Monaco", "score_home": 0, "score_away": 1, "played": True},
    {"round": 4, "home": "Tottenham", "away": "Copenhagen", "score_home": 4, "score_away": 0, "played": True},
    {"round": 4, "home": "Olympiacos", "away": "PSV", "score_home": 1, "score_away": 1, "played": True},
    {"round": 4, "home": "Qarabag", "away": "Chelsea", "score_home": 2, "score_away": 2, "played": True},
    {"round": 4, "home": "Pafos", "away": "Villarreal", "score_home": 1, "score_away": 0, "played": True},
    {"round": 4, "home": "Ajax", "away": "Galatasaray", "score_home": 0, "score_away": 3, "played": True},
    {"round": 4, "home": "Man City", "away": "Dortmund", "score_home": 4, "score_away": 1, "played": True},
    {"round": 4, "home": "Marseille", "away": "Atalanta", "score_home": 0, "score_away": 1, "played": True},
    {"round": 4, "home": "Benfica", "away": "Leverkusen", "score_home": 0, "score_away": 1, "played": True},
    {"round": 4, "home": "Inter", "away": "Kairat Almaty", "score_home": 2, "score_away": 1, "played": True},
    {"round": 4, "home": "Newcastle", "away": "Athletic Club", "score_home": 2, "score_away": 0, "played": True},
    {"round": 4, "home": "Club Brugge", "away": "Barcelona", "score_home": 3, "score_away": 3, "played": True},

    # --- JOURNÉE 5 (25-26 Novembre 2025) ---
    {"round": 5, "home": "Ajax", "away": "Benfica", "score_home": 0, "score_away": 2, "played": True},
    {"round": 5, "home": "Galatasaray", "away": "Union SG", "score_home": 0, "score_away": 1, "played": True},
    {"round": 5, "home": "Marseille", "away": "Newcastle", "score_home": 2, "score_away": 1, "played": True},
    {"round": 5, "home": "Dortmund", "away": "Villarreal", "score_home": 4, "score_away": 0, "played": True},
    {"round": 5, "home": "Man City", "away": "Leverkusen", "score_home": 0, "score_away": 2, "played": True},
    {"round": 5, "home": "Slavia Prague", "away": "Athletic Club", "score_home": 0, "score_away": 0, "played": True},
    {"round": 5, "home": "Napoli", "away": "Qarabag", "score_home": 2, "score_away": 0, "played": True},
    {"round": 5, "home": "Bodo/Glimt", "away": "Juventus", "score_home": 2, "score_away": 3, "played": True},
    {"round": 5, "home": "Chelsea", "away": "Barcelona", "score_home": 3, "score_away": 0, "played": True},
    {"round": 5, "home": "Copenhagen", "away": "Kairat Almaty", "score_home": 3, "score_away": 2, "played": True},
    {"round": 5, "home": "Pafos", "away": "Monaco", "score_home": 2, "score_away": 2, "played": True},
    {"round": 5, "home": "Frankfurt", "away": "Atalanta", "score_home": 0, "score_away": 3, "played": True},
    {"round": 5, "home": "Olympiacos", "away": "Real Madrid", "score_home": 3, "score_away": 4, "played": True},
    {"round": 5, "home": "Arsenal", "away": "Bayern", "score_home": 3, "score_away": 1, "played": True},
    {"round": 5, "home": "Paris SG", "away": "Tottenham", "score_home": 5, "score_away": 3, "played": True},
    {"round": 5, "home": "Liverpool", "away": "PSV", "score_home": 1, "score_away": 4, "played": True},
    {"round": 5, "home": "Atletico", "away": "Inter", "score_home": 2, "score_away": 1, "played": True},
    {"round": 5, "home": "Sporting", "away": "Club Brugge", "score_home": 3, "score_away": 0, "played": True},

    # --- JOURNÉE 6 (9-10 Décembre 2025) ---
    {"round": 6, "home": "Kairat Almaty", "away": "Olympiacos", "score_home": 0, "score_away": 1, "played": True},
    {"round": 6, "home": "Bayern", "away": "Sporting", "score_home": 3, "score_away": 1, "played": True},
    {"round": 6, "home": "Inter", "away": "Liverpool", "score_home": 0, "score_away": 1, "played": True},
    {"round": 6, "home": "Barcelona", "away": "Frankfurt", "score_home": 2, "score_away": 1, "played": True},
    {"round": 6, "home": "Tottenham", "away": "Slavia Prague", "score_home": 3, "score_away": 0, "played": True},
    {"round": 6, "home": "Union SG", "away": "Marseille", "score_home": 2, "score_away": 3, "played": True},
    {"round": 6, "home": "PSV", "away": "Atletico", "score_home": 2, "score_away": 3, "played": True},
    {"round": 6, "home": "Atalanta", "away": "Chelsea", "score_home": 2, "score_away": 1, "played": True},
    {"round": 6, "home": "Monaco", "away": "Galatasaray", "score_home": 1, "score_away": 0, "played": True},
    {"round": 6, "home": "Villarreal", "away": "Copenhagen", "score_home": 2, "score_away": 3, "played": True},
    {"round": 6, "home": "Qarabag", "away": "Ajax", "score_home": 2, "score_away": 4, "played": True},
    {"round": 6, "home": "Athletic Club", "away": "Paris SG", "score_home": 0, "score_away": 0, "played": True},
    {"round": 6, "home": "Real Madrid", "away": "Man City", "score_home": 1, "score_away": 2, "played": True},
    {"round": 6, "home": "Benfica", "away": "Napoli", "score_home": 2, "score_away": 0, "played": True},
    {"round": 6, "home": "Leverkusen", "away": "Newcastle", "score_home": 2, "score_away": 2, "played": True},
    {"round": 6, "home": "Dortmund", "away": "Bodo/Glimt", "score_home": 2, "score_away": 2, "played": True},
    {"round": 6, "home": "Juventus", "away": "Pafos", "score_home": 2, "score_away": 0, "played": True},
    {"round": 6, "home": "Club Brugge", "away": "Arsenal", "score_home": 0, "score_away": 3, "played": True},

    # --- JOURNÉE 7 (20-21 Janvier 2026 - A Venir) ---
    {"round": 7, "home": "Kairat Almaty", "away": "Club Brugge", "score_home": None, "score_away": None, "played": False},
    {"round": 7, "home": "Bodo/Glimt", "away": "Man City", "score_home": None, "score_away": None, "played": False},
    {"round": 7, "home": "Inter", "away": "Arsenal", "score_home": None, "score_away": None, "played": False},
    {"round": 7, "home": "Sporting", "away": "Paris SG", "score_home": None, "score_away": None, "played": False},
    {"round": 7, "home": "Real Madrid", "away": "Monaco", "score_home": None, "score_away": None, "played": False},
    {"round": 7, "home": "Olympiacos", "away": "Leverkusen", "score_home": None, "score_away": None, "played": False},
    {"round": 7, "home": "Tottenham", "away": "Dortmund", "score_home": None, "score_away": None, "played": False},
    {"round": 7, "home": "Villarreal", "away": "Ajax", "score_home": None, "score_away": None, "played": False},
    {"round": 7, "home": "Copenhagen", "away": "Napoli", "score_home": None, "score_away": None, "played": False},
    {"round": 7, "home": "Qarabag", "away": "Frankfurt", "score_home": None, "score_away": None, "played": False},
    {"round": 7, "home": "Galatasaray", "away": "Atletico", "score_home": None, "score_away": None, "played": False},
    {"round": 7, "home": "Atalanta", "away": "Athletic Club", "score_home": None, "score_away": None, "played": False},
    {"round": 7, "home": "Slavia Prague", "away": "Barcelona", "score_home": None, "score_away": None, "played": False},
    {"round": 7, "home": "Marseille", "away": "Liverpool", "score_home": None, "score_away": None, "played": False},
    {"round": 7, "home": "Bayern", "away": "Union SG", "score_home": None, "score_away": None, "played": False},
    {"round": 7, "home": "Chelsea", "away": "Pafos", "score_home": None, "score_away": None, "played": False},
    {"round": 7, "home": "Juventus", "away": "Benfica", "score_home": None, "score_away": None, "played": False},
    {"round": 7, "home": "Newcastle", "away": "PSV", "score_home": None, "score_away": None, "played": False},

    # --- JOURNÉE 8 (28 Janvier 2026 - A Venir) ---
    {"round": 8, "home": "Club Brugge", "away": "Marseille", "score_home": None, "score_away": None, "played": False},
    {"round": 8, "home": "Benfica", "away": "Real Madrid", "score_home": None, "score_away": None, "played": False},
    {"round": 8, "home": "Paris SG", "away": "Newcastle", "score_home": None, "score_away": None, "played": False},
    {"round": 8, "home": "Monaco", "away": "Juventus", "score_home": None, "score_away": None, "played": False},
    {"round": 8, "home": "Man City", "away": "Galatasaray", "score_home": None, "score_away": None, "played": False},
    {"round": 8, "home": "Dortmund", "away": "Inter", "score_home": None, "score_away": None, "played": False},
    {"round": 8, "home": "Leverkusen", "away": "Villarreal", "score_home": None, "score_away": None, "played": False},
    {"round": 8, "home": "PSV", "away": "Bayern", "score_home": None, "score_away": None, "played": False},
    {"round": 8, "home": "Arsenal", "away": "Kairat Almaty", "score_home": None, "score_away": None, "played": False},
    {"round": 8, "home": "Napoli", "away": "Chelsea", "score_home": None, "score_away": None, "played": False},
    {"round": 8, "home": "Athletic Club", "away": "Sporting", "score_home": None, "score_away": None, "played": False},
    {"round": 8, "home": "Pafos", "away": "Slavia Prague", "score_home": None, "score_away": None, "played": False},
    {"round": 8, "home": "Liverpool", "away": "Qarabag", "score_home": None, "score_away": None, "played": False},
    {"round": 8, "home": "Atletico", "away": "Bodo/Glimt", "score_home": None, "score_away": None, "played": False},
    {"round": 8, "home": "Ajax", "away": "Olympiacos", "score_home": None, "score_away": None, "played": False},
    {"round": 8, "home": "Barcelona", "away": "Copenhagen", "score_home": None, "score_away": None, "played": False},
    {"round": 8, "home": "Frankfurt", "away": "Tottenham", "score_home": None, "score_away": None, "played": False},
    {"round": 8, "home": "Union SG", "away": "Atalanta", "score_home": None, "score_away": None, "played": False},
]

def generate_csv():
    processed_data = []

    print(f"Traitement de {len(raw_matches)} matchs...")

    for match in raw_matches:
        home_name = match["home"]
        away_name = match["away"]

        if home_name not in TEAM_CONFIG:
            raise ValueError(f"ERREUR: L'équipe '{home_name}' (J{match['round']}) n'est pas dans TEAM_CONFIG.")
        if away_name not in TEAM_CONFIG:
            raise ValueError(f"ERREUR: L'équipe '{away_name}' (J{match['round']}) n'est pas dans TEAM_CONFIG.")

        home_code = TEAM_CONFIG[home_name]
        away_code = TEAM_CONFIG[away_name]
        match_id = f"{match['round']:02d}-{home_code}-{away_code}"

        if match["played"] and (match["score_home"] is None or match["score_away"] is None):
             raise ValueError(f"ERREUR: Le match {home_name}-{away_name} est marqué 'played' mais n'a pas de score.")

        processed_data.append({
            "match_id": match_id,
            "round": match["round"],
            "home_team": home_name,
            "away_team": away_name,
            "is_played": 1 if match["played"] else 0,
            "home_score": match["score_home"],
            "away_score": match["score_away"]
        })

    df = pd.DataFrame(processed_data)
    
    os.makedirs("data/raw", exist_ok=True)
    
    output_path = "data/raw/matches.csv"
    #  Ajout du séparateur point-virgule pour Excel Français
    df.to_csv(output_path, index=False, sep=';', encoding='utf-8-sig')
    
    print(f"✅ Fichier généré avec succès : {output_path}")
    print(f"ℹ️  Nombre de matchs configurés : {len(df)}")
    if len(df) < 144:
        print(f"⚠️  Attention : Il manque {144 - len(df)} matchs pour avoir le calendrier complet (8 journées).")

if __name__ == "__main__":
    generate_csv()
