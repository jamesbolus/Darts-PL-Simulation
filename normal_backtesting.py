import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from simple_sim import match

full_df = pd.read_excel("../full_df.xlsx")

pl_players = ['Littler, Luke', 'Humphries, Luke', 'Cross, Rob', 'Bunting, Stephen', 'Price, Gerwyn', 'Dobey, Chris', 
              'van Gerwen, Michael', 'Aspinall, Nathan']

period = 20
t20_mean_home = []
t20_sd_home = []
dbl_mean_home = []
dbl_sd_home = []
t20_mean_away = []
t20_sd_away = []
dbl_mean_away = []
dbl_sd_away = []

for index, row in full_df.iterrows():
    if row['Event'] == 'Premier League':
        home_player = row['Home']
        away_player = row['Away']
        home_t20s = []
        away_t20s = []
        home_dbls = []
        away_dbls = []
        rel_df = full_df.iloc[:index, :]
        for index2, row2 in rel_df.iterrows():
            if row2['Home'] == home_player:
                home_t20s.append(row2['t20_rate_home'])
                home_dbls.append(row2['home_check_pcnt']/100)
            elif row2['Away'] == home_player:
                home_t20s.append(row2['t20_rate_away'])
                home_dbls.append(row2['away_check_pcnt']/100)
            elif row2['Home'] == away_player:
                away_t20s.append(row2['t20_rate_home'])
                away_dbls.append(row2['home_check_pcnt']/100)
            elif row2['Away'] == home_player:
                away_t20s.append(row2['t20_rate_away'])
                away_dbls.append(row2['away_check_pcnt']/100)
                
        t20_mean_home.append(np.mean(home_t20s[-period:]))
        t20_sd_home.append(np.std(home_t20s[-period:]))
        dbl_mean_home.append(np.mean(home_dbls[-period:]))
        dbl_sd_home.append(np.std(home_dbls[-period:]))
        
        t20_mean_away.append(np.mean(away_t20s[-period:]))
        t20_sd_away.append(np.std(away_t20s[-period:]))
        dbl_mean_away.append(np.mean(away_dbls[-period:]))
        dbl_sd_away.append(np.std(away_dbls[-period:]))


pl_df = pd.read_excel("../results.xlsx")

pl_df["t20_mean_home"] = t20_mean_home
pl_df["t20_std_home"] = t20_sd_home
pl_df["dbl_mean_home"] = dbl_mean_home
pl_df["dbl_std_home"] = dbl_sd_home

pl_df["t20_mean_away"] = t20_mean_away
pl_df["t20_std_away"] = t20_sd_away
pl_df["dbl_mean_away"] = dbl_mean_away
pl_df["dbl_std_away"] = dbl_sd_away


n_sims = 2000
best_of = 11
home_probs = []
away_probs = []
for index, row in pl_df.iterrows():
    #print(f"{row['home']} vs {row['away']}")
    start_throw = row['throw']
    home_wins = 0
    away_wins = 0
    x = 0
    for a in range(n_sims):
        home_treb_rate = np.clip(np.random.normal(row['t20_mean_home'], row['t20_std_home']), 0.05, 0.9)
        home_dbl_rate = np.clip(np.random.normal(row['dbl_mean_home'], row['dbl_std_home']), 0.05, 0.9)
        home_stats = {'p_treble': home_treb_rate, 'p_double': home_dbl_rate}
        away_treb_rate = np.clip(np.random.normal(row['t20_mean_away'], row['t20_std_away']), 0.05, 0.9)
        away_dbl_rate = np.clip(np.random.normal(row['dbl_mean_away'], row['dbl_std_away']), 0.05, 0.9)
        away_stats = {'p_treble': away_treb_rate, 'p_double': away_dbl_rate}
        score, match_winner, home_match_avg, away_match_avg = match(best_of, home_stats, away_stats, start_throw)
        if match_winner == 0:
            home_wins += 1
        elif match_winner == 1:
            away_wins += 1

    home_probs.append(home_wins/n_sims)
    away_probs.append(away_wins/n_sims)

pl_df['home_prob'] = home_probs
pl_df['away_prob'] = away_probs

pl_sp = pd.read_excel("../BFD/weekly/results_sp.xlsx")

pl_df["home_sp"] = pl_sp['home_sp']
pl_df["away_sp"] = pl_sp['away_sp']
pl_df = pl_df.iloc[:111, :]

test = pl_df[['home', 'away', 'home_prob', 'home_sp', 'away_prob', 'away_sp', 'winner']]
test['home_sp'] = 1 / test['home_sp']
test['away_sp'] = 1 / test['away_sp']

def kelly(odds, prob_win):
    return(((odds-1)*prob_win+prob_win-1)/odds)

bankroll = 1000
bankroll_history = []
stakes = []
home = []
away= []
bets = []
winners = []
odds = []
probs = []
for index, row in pl_df.iterrows():
    home_price = row["home_sp"]
    home_prob = row["home_prob"]
    away_price = row["away_sp"]
    away_prob = row["away_prob"]

    home_edge = home_prob - 1/home_price
    away_edge = away_prob - 1/away_price

    if home_edge == away_edge:
        continue

    if home_edge > away_edge:
        kc = kelly(home_price, home_prob)
        stake = 0.5*bankroll*kc
        bets.append(0)
        odds.append(1/home_price)
        probs.append(home_prob)
        if row['winner'] == 0:
            bankroll += stake*(home_price-1)
        else:
            bankroll -= stake
    elif home_edge < away_edge:
        kc = kelly(away_price, away_prob)
        stake = 0.5*bankroll*kc
        bets.append(1)
        odds.append(1/away_price)
        probs.append(away_prob)
        if row['winner'] == 1:
            bankroll += stake*(away_price-1)
        else:
            bankroll -= stake
            
    stakes.append(stake)
    home.append(row["home"])
    away.append(row["away"])
    winners.append(row["winner"])
    bankroll_history.append(bankroll)


bet_results = pd.DataFrame({
    'Home': home,
    'Away': away,
    'Bet': bets,
    'Winner': winners,
    'Implied prob': odds,
    'Prob' : probs,
    'Stake': stakes,
    'Bankroll': bankroll_history
})


plt.figure(figsize=(10, 6),dpi=600)
plt.plot(bankroll_history)
plt.xlabel("Time")
plt.ylabel("Bankroll (£)")
plt.title("Bankroll Over Time")
plt.grid(True)
plt.show()
