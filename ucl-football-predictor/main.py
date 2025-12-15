import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from tqdm import tqdm
from collections import Counter 
from src.simulation_engine import simulate_match

# =============================================================================
# 🛠️ ZONE DE CONFIGURATION
# =============================================================================

# 1. PERFORMANCE
N_SIMULATIONS = 10000     

# 2. VOYAGE DANS LE TEMPS
SCENARIO_MODE = "SEASON_START"  # "SEASON_START", "CURRENT", "AFTER_ROUND"
TARGET_ROUND  = 3

# 3. AFFICHAGE & VISUALISATION
SHOW_SINGLE_SCENARIO = True   # Affiche le scénario le plus fréquent
CLUB_FOCUS = "Paris SG"       # Pour les graphiques (ou None)
OPEN_CHARTS = True            # Ouvrir les fenêtres graphiques ?

# =============================================================================

DATA_PATH_MATCHES = "data/raw/matches.csv"
DATA_PATH_RATINGS = "data/raw/ratings.csv"

def load_data():
    if not os.path.exists(DATA_PATH_MATCHES):
        print("❌ Erreur : 'data/raw/matches.csv' introuvable.")
        sys.exit()
    df_matches = pd.read_csv(DATA_PATH_MATCHES, sep=';', encoding='utf-8-sig')
    df_ratings = pd.read_csv(DATA_PATH_RATINGS, sep=';', encoding='utf-8-sig')
    elo_dict = pd.Series(df_ratings.elo.values, index=df_ratings.team_name).to_dict()
    all_teams = set(df_matches['home_team']).union(set(df_matches['away_team']))
    for team in all_teams:
        if team not in elo_dict: elo_dict[team] = 1500
    return df_matches, elo_dict

def apply_scenario(df):
    df_scenario = df.copy()
    if SCENARIO_MODE == "SEASON_START":
        df_scenario['is_played'] = 0
        df_scenario['home_score'] = None
        df_scenario['away_score'] = None
    elif SCENARIO_MODE == "AFTER_ROUND":
        mask_future = df_scenario['round'] > TARGET_ROUND
        df_scenario.loc[mask_future, 'is_played'] = 0
        df_scenario.loc[mask_future, 'home_score'] = None
        df_scenario.loc[mask_future, 'away_score'] = None
    return df_scenario

def run_simulation():
    # --- CHARGEMENT ---
    df_original, elo_dict = load_data()
    df_matches = apply_scenario(df_original)
    
    matches_to_sim = df_matches[df_matches['is_played'] == 0].copy()
    matches_played = df_matches[df_matches['is_played'] == 1].copy()
    
    # Base de points acquis
    matches_played['h_pts'] = np.where(matches_played['home_score'] > matches_played['away_score'], 3, 
                              np.where(matches_played['home_score'] == matches_played['away_score'], 1, 0))
    matches_played['a_pts'] = np.where(matches_played['away_score'] > matches_played['home_score'], 3, 
                              np.where(matches_played['away_score'] == matches_played['home_score'], 1, 0))
    
    base_home = matches_played.groupby('home_team')[['h_pts', 'home_score', 'away_score']].sum()
    base_away = matches_played.groupby('away_team')[['a_pts', 'away_score', 'home_score']].sum()
    
    teams = list(elo_dict.keys())
    raw_ranks = {team: [] for team in teams if team in set(df_matches['home_team'])}

    # Dictionnaire pour compter les scores de chaque match
    # Clé = Index du match dans le DataFrame, Valeur = Counter objects
    # ex: { 12: Counter({(1,0): 50, (2,1): 12...}) }
    score_tracker = {idx: Counter() for idx in matches_to_sim.index}

    # --- MONTE CARLO ---
    print(f"\n🚀 Simulation ({N_SIMULATIONS} itérations)...")
    
    for _ in tqdm(range(N_SIMULATIONS), disable=(N_SIMULATIONS < 10)):
        sim_scores = matches_to_sim.copy()
        
        # Moteur Dixon-Coles
        h_scores = []
        a_scores = []
        
        # On itère sur les matchs à simuler
        for idx, row in sim_scores.iterrows():
            h_elo = elo_dict.get(row['home_team'], 1500)
            a_elo = elo_dict.get(row['away_team'], 1500)
            h, a, _, _ = simulate_match(h_elo, a_elo)
            
            h_scores.append(h)
            a_scores.append(a)
            
            
            # On stocke le tuple (h, a) dans le compteur de ce match
            score_tracker[idx].update([(h, a)])
            
        sim_scores['home_score'] = h_scores
        sim_scores['away_score'] = a_scores
        
        # Calcul du classement pour cette itération
        sim_scores['h_pts'] = np.where(sim_scores['home_score'] > sim_scores['away_score'], 3, 
                              np.where(sim_scores['home_score'] == sim_scores['away_score'], 1, 0))
        sim_scores['a_pts'] = np.where(sim_scores['away_score'] > sim_scores['home_score'], 3, 
                              np.where(sim_scores['away_score'] == sim_scores['home_score'], 1, 0))

        sim_home = sim_scores.groupby('home_team')[['h_pts', 'home_score', 'away_score']].sum()
        sim_away = sim_scores.groupby('away_team')[['a_pts', 'away_score', 'home_score']].sum()
        
        total_home = base_home.add(sim_home, fill_value=0)
        total_away = base_away.add(sim_away, fill_value=0)
        
        final_table = pd.DataFrame(index=total_home.index.union(total_away.index))
        final_table['Pts'] = total_home['h_pts'].add(total_away['a_pts'], fill_value=0)
        final_table['GF'] = total_home['home_score'].add(total_away['away_score'], fill_value=0)
        final_table['GA'] = total_home['away_score'].add(total_away['home_score'], fill_value=0)
        final_table['GD'] = final_table['GF'] - final_table['GA']
        
        final_table = final_table.sort_values(by=['Pts', 'GD', 'GF'], ascending=False)
        
        for rank, team in enumerate(final_table.index, 1):
            if team in raw_ranks:
                raw_ranks[team].append(rank)

    # --- CONSTRUCTION DU SCÉNARIO LE PLUS FRÉQUENT ---
    if SHOW_SINGLE_SCENARIO:
        most_frequent_scenario = matches_to_sim.copy()
        for idx in most_frequent_scenario.index:
            # most_common(1) renvoie [( (score_h, score_a), count )]
            # Si égalité, Counter renvoie le premier rencontré
            best_score_tuple = score_tracker[idx].most_common(1)[0][0]
            most_frequent_scenario.at[idx, 'home_score'] = best_score_tuple[0]
            most_frequent_scenario.at[idx, 'away_score'] = best_score_tuple[1]
            
        print_most_frequent_scenario(most_frequent_scenario)

    # --- VISUALISATION ---
    if OPEN_CHARTS:
        plot_leaderboard(raw_ranks)
        if CLUB_FOCUS:
            plot_club_distribution(CLUB_FOCUS, raw_ranks)
        
        print("\n🖼️  Les graphiques sont ouverts.")
        plt.show()

def print_most_frequent_scenario(df_scenario):
    """Affiche le score le plus fréquent (Mode) pour chaque match."""
    print("\n🎲 RÉSULTATS LES PLUS FRÉQUENTS (Mode Statistique)")
    print("-" * 50)
    print(f"{'Journée':<8} | {'Domicile':>15} {'Score':^7} {'Extérieur':<15}")
    print("-" * 50)
    
    df = df_scenario.sort_values(by='round')
    current_round = 0
    
    for _, row in df.iterrows():
        if row['round'] != current_round:
            current_round = row['round']
            print(f"\n--- JOURNÉE {current_round} ---")
        
        h = int(row['home_score'])
        a = int(row['away_score'])
        print(f"{'':<8} | {row['home_team']:>15}  {h}-{a}  {row['away_team']:<15}")
    print("-" * 50)

def plot_leaderboard(raw_ranks):
    teams = []
    top8_probs = []
    playoff_probs = []
    out_probs = []
    avg_ranks = []

    for team, ranks in raw_ranks.items():
        if not ranks: continue
        r = np.array(ranks)
        teams.append(team)
        top8_probs.append(np.mean(r <= 8) * 100)
        playoff_probs.append(np.mean((r > 8) & (r <= 24)) * 100)
        out_probs.append(np.mean(r > 24) * 100)
        avg_ranks.append(np.mean(r))

    df_plot = pd.DataFrame({
        'Team': teams, 'Top8': top8_probs, 'Playoff': playoff_probs, 'Out': out_probs, 'Avg': avg_ranks
    })
    df_plot = df_plot.sort_values('Avg', ascending=True).iloc[::-1]

    fig, ax = plt.subplots(figsize=(12, 10))
    y_pos = np.arange(len(df_plot))
    
    ax.barh(y_pos, df_plot['Top8'], label='Top 8', color='#4CAF50', alpha=0.8)
    ax.barh(y_pos, df_plot['Playoff'], left=df_plot['Top8'], label='Barrage', color='#FFC107', alpha=0.8)
    ax.barh(y_pos, df_plot['Out'], left=df_plot['Top8'] + df_plot['Playoff'], label='Out', color='#F44336', alpha=0.8)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(df_plot['Team'])
    ax.set_xlabel('Probabilité (%)')
    ax.set_title(f'Prédictions LDC 2026 - Classement Moyen ({N_SIMULATIONS} sims)')
    ax.legend(loc='lower right')
    
    for i, (idx, row) in enumerate(df_plot.iterrows()):
        ax.text(101, i, f"Moy: {row['Avg']:.1f}", va='center', fontsize=8, color='black')
    plt.tight_layout()

def plot_club_distribution(team_name, raw_ranks):
    found = [t for t in raw_ranks.keys() if team_name.lower() in t.lower()]
    if not found:
        print(f"❌ Club '{team_name}' introuvable.")
        return
    real_name = found[0]
    ranks = np.array(raw_ranks[real_name])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    counts, bins, patches = ax.hist(ranks, bins=np.arange(0.5, 37.5, 1), edgecolor='black', alpha=0.7)
    
    for i in range(len(patches)):
        if (i+1) <= 8: patches[i].set_facecolor('#4CAF50')
        elif (i+1) <= 24: patches[i].set_facecolor('#FFC107')
        else: patches[i].set_facecolor('#F44336')
            
    ax.set_xticks(range(1, 37, 2))
    ax.set_title(f'Distribution : {real_name.upper()}')
    plt.tight_layout()

if __name__ == "__main__":
    run_simulation()
