import numpy as np
from scipy.stats import poisson



# 1. Avantage Domicile 
HOME_ADVANTAGE = 74.0   

# 2. Facteur de Hiérarchie (Le "Divider")

DIVIDER = 320.0 

# 3. Moyenne de buts

AVG_GOALS = 1.42 

# 4. Correction Dixon-Coles (Matches nuls)
RHO = -0.13 

def elo_to_expected_goals(elo_attack, elo_defense):
    """
    Calcule l'espérance de buts (Lambda) en accentuant les écarts de niveau.
    """
    diff = elo_attack - elo_defense
    
    # Formule Sigmoïde
    expected_score = 1 / (1 + 10 ** (-diff / DIVIDER))
    
    # Projection sur les buts
    mu = AVG_GOALS * (expected_score / 0.5) 
    return mu

def dixon_coles_adjustment(prob, home_goals, away_goals, mu_home, mu_away, rho):
    """
    Corrige les probabilités des scores faibles (0-0, 1-0, 0-1, 1-1).
    """
    if home_goals == 0 and away_goals == 0:
        return prob * (1.0 - (mu_home * mu_away * rho))
    elif home_goals == 0 and away_goals == 1:
        return prob * (1.0 + (mu_home * rho))
    elif home_goals == 1 and away_goals == 0:
        return prob * (1.0 + (mu_away * rho))
    elif home_goals == 1 and away_goals == 1:
        return prob * (1.0 - rho)
    else:
        return prob

def simulate_match(home_elo, away_elo, max_goals=8):
    """
    Simule un score.
    """
    # 1. Calcul des xG (Espérance)
    mu_home = elo_to_expected_goals(home_elo + HOME_ADVANTAGE, away_elo)
    mu_away = elo_to_expected_goals(away_elo, home_elo + HOME_ADVANTAGE)
    
    # 2. Matrice de probabilités
    score_probs = []
    scores = []
    
    for h in range(max_goals + 1):
        for a in range(max_goals + 1):
            prob_h = poisson.pmf(h, mu_home)
            prob_a = poisson.pmf(a, mu_away)
            base_prob = prob_h * prob_a
            
            # Ajustement
            adj_prob = dixon_coles_adjustment(base_prob, h, a, mu_home, mu_away, RHO)
            
            score_probs.append(max(0, adj_prob)) # Sécurité contre proba négative
            scores.append((h, a))
            
    # 3. Normalisation & Tirage
    score_probs = np.array(score_probs)
    if score_probs.sum() == 0: 
        score_probs = np.ones(len(score_probs)) # Fallback impossible normalement
        
    score_probs /= score_probs.sum()
    
    index = np.random.choice(len(scores), p=score_probs)
    final_score = scores[index]
    
    return final_score[0], final_score[1], mu_home, mu_away
