#  UCL Football Predictor 2026

A probabilistic simulation engine designed to forecast the outcome of the UEFA Champions League.

This project moves beyond simple "coin-flip" predictions by implementing advanced statistical modeling (**Dixon-Coles adjustment**) and large-scale simulations (**Monte Carlo method**) to determine qualification probabilities for each team.

---

##  Key Features

* **Advanced Match Engine:** Uses specific Elo ratings and the **Dixon-Coles model** to correct the underestimation of draws common in standard Poisson distributions.
* **Monte Carlo Simulation:** Runs **10,000+ iterations** of the remaining schedule to generate statistically robust probabilities (Top 8, Playoffs, Elimination).
* **"Time Travel" Scenarios:** Capable of simulating from the start of the season or predicting the end of the season based on current real-world results.
* **Data Visualization:** Interactive CLI and **Matplotlib** charts to visualize team ranking distributions.
* **Modern Calibrations:** Adjusted for the new UCL "League Phase" format using optimized parameters (Home Advantage +80, Elo Divider 320).

##  The Mathematics Behind It

This engine is built on three statistical pillars:

### 1. Elo Ratings & Expected Goals (xG)
Team strength is derived from dynamic Elo ratings. I calculate the expected goals ($\lambda$) for a match between Team A and Team B using a logistic function adapted for modern football:
$$\lambda_{Home} = \text{AvgGoals} \times 10^{\frac{(Elo_{Home} + \text{HomeAdv}) - Elo_{Away}}{320}}$$

### 2. Dixon-Coles Adjustment
A standard Poisson distribution assumes goal independence. However, in low-scoring sports like football, scores like 0-0 or 1-1 happen more often than Poisson predicts.
I implement the **Dixon-Coles (1997)** adjustment factor ($\rho = -0.13$) to correct probabilities for low scores, significantly increasing the model's realism regarding draws.

### 3. Monte Carlo Method
Since the new UCL format involves complex tie-breakers (Goal Difference, Goals For), analytical calculation is impossible. I use Monte Carlo simulations to "play" the tournament thousands of times, aggregating the results to derive the probability of specific outcomes (e.g., *What is the % chance of PSG finishing in the Top 8?*).

## 🛠️ Project Structure
```text
ucl-football-predictor/
├── data/
│   └── raw/            # CSV files containing Match Schedule and Team Ratings
├── src/
│   ├── simulation_engine.py  # The core logic (Maths & Probability models)
│   └── fetch_ratings.py      # Scripts to fetch/update data
├── main.py             # Entry point: CLI Menu & Visualization orchestration
└── requirements.txt    # Python dependencies
