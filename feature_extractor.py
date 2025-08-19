import requests
import json
import pandas as pd
import time
import os
import numpy as np

pl_games = pd.read_csv("pl_ids.csv", index_col=0)
pl_games = pl_games[pl_games["match_id"] != 57413401].reset_index(drop=True) # Bye game
ids = pl_games["match_id"]

throw_order = []

t20_attempt_home = []
t20_success_home = []
t19_attempt_home = []
t19_success_home = []
dbl_attempt_home = []

t20_attempt_away = []
t20_success_away = []
t19_attempt_away = []
t19_success_away = []
dbl_attempt_away = []

home_checkout = []
home_3da = []
home_high_check = []
home_check_100_plus = []
home_180s = []
home_140s_plus = []
away_checkout = []
away_3da = []
away_high_check = []
away_check_100_plus = []
away_180s = []
away_140s_plus = []


home_legs = []
away_legs = []

for i in range(len(ids)):
    ID = ids[i]
    filepath = os.path.join("pl25_data", f"pl_{ID}.json")
    with open(filepath, 'r') as file:
        data = json.load(file)

    timeline = data["timeline"]
    # Who has throw
    for event in timeline:
        if event["type"] == "first_throw":
            first_throw = event["competitor"]
            throw = 0 if first_throw == "home" else 1

    throw_order.append(throw)

    home_legs_won = data["sport_event_status"]["home_score"]
    away_legs_won = data["sport_event_status"]["away_score"]
    home_legs.append(home_legs_won)
    away_legs.append(away_legs_won)

    # Treble pcnt
    home_pcnt = {}
    away_pcnt = {}
    home_dbl_at = 0
    away_dbl_at = 0
    for event in timeline: 
        # Counts treble attempts and successes
        if event["type"] == "dart" and event.get("is_checkout_attempt", 0) == 0:
            if event["competitor"] == "home":
                segment = event["dart_score"]
                success = 1 if event["dart_score_multiplier"] == 3 else 0
                
                if f"{segment}" not in home_pcnt:
                    home_pcnt[f"{segment}"] = {"attempts": 0, "success": 0}
                    
                home_pcnt[f"{segment}"]["attempts"] += 1
                home_pcnt[f"{segment}"]["success"] += success
            if event["competitor"] == "away":
                segment = event["dart_score"]
                success = 1 if event["dart_score_multiplier"] == 3 else 0
                
                if f"{segment}" not in away_pcnt:
                    away_pcnt[f"{segment}"] = {"attempts": 0, "success": 0}
                    
                away_pcnt[f"{segment}"]["attempts"] += 1
                away_pcnt[f"{segment}"]["success"] += success
                
        # Counts double attempts    
        if event.get("is_checkout_attempt"):
            if event["competitor"] == "home":
                home_dbl_at += 1
            if event["competitor"] == "away":
                away_dbl_at += 1

    # Append success and attempts for trebles and doubles
    t20_attempt_home.append(home_pcnt["20"]["attempts"])
    t20_success_home.append(home_pcnt["20"]["success"])
    t19_attempt_home.append(home_pcnt["19"]["attempts"])
    t19_success_home.append(home_pcnt["19"]["success"])
    dbl_attempt_home.append(home_dbl_at)
    t20_attempt_away.append(away_pcnt["20"]["attempts"])
    t20_success_away.append(away_pcnt["20"]["success"])
    t19_attempt_away.append(away_pcnt["19"]["attempts"])
    t19_success_away.append(away_pcnt["19"]["success"])
    dbl_attempt_away.append(away_dbl_at)


    data["sport_event_status"]["home_score"]
    competitors = data["statistics"]["totals"]["competitors"]
    
    for player in competitors:
        if player["qualifier"] == "home":
            home_checkout.append(player["statistics"]["checkout_percentage"])
            #home_darts_at_dbl.append((100*home_legs_won)/player["statistics"]["checkout_percentage"])
            home_3da.append(player["statistics"]["average_3_darts"])
            home_high_check.append(player["statistics"]["highest_checkout"])
            home_check_100_plus.append(player["statistics"]["checkouts_100s_plus"])
            home_180s.append(player["statistics"]["scores_180s"])
            home_140s_plus.append(player["statistics"]["scores_140s_plus"])
        elif player["qualifier"] == "away":
            away_checkout.append(player["statistics"]["checkout_percentage"])
            #away_darts_at_dbl.append((100*away_legs_won)/player["statistics"]["checkout_percentage"])
            away_3da.append(player["statistics"]["average_3_darts"])
            away_high_check.append(player["statistics"]["highest_checkout"])
            away_check_100_plus.append(player["statistics"]["checkouts_100s_plus"])
            away_180s.append(player["statistics"]["scores_180s"])
            away_140s_plus.append(player["statistics"]["scores_140s_plus"])


pl_games["throw"] = throw_order
pl_games["t20_attempt_home"] = t20_attempt_home
pl_games["t20_success_home"] = t20_success_home
pl_games["t20_rate_home"] = pl_games["t20_success_home"]/pl_games["t20_attempt_home"]
pl_games["t19_attempt_home"] = t19_attempt_home
pl_games["t19_success_home"] = t19_success_home
pl_games["t19_rate_home"] = pl_games["t19_success_home"]/pl_games["t19_attempt_home"]
pl_games["t20_attempt_away"] = t20_attempt_away
pl_games["t20_success_away"] = t20_success_away
pl_games["t20_rate_away"] = pl_games["t20_success_away"]/pl_games["t20_attempt_away"]
pl_games["t19_attempt_away"] = t19_attempt_away
pl_games["t19_success_away"] = t19_success_away
pl_games["t19_rate_away"] = pl_games["t19_success_away"]/pl_games["t19_attempt_away"]

pl_games["home_check_pcnt"] = home_checkout
pl_games["home_3da"] = home_3da
pl_games["home_high_check"] = home_high_check
pl_games["home_check_100_plus"] = home_check_100_plus
pl_games["home_180s"] = home_180s
pl_games["home_140s_plus"] = home_140s_plus
pl_games["away_check_pcnt"] = away_checkout
pl_games["away_3da"] = away_3da
pl_games["away_high_check"] = away_high_check
pl_games["away_check_100_plus"] = away_check_100_plus
pl_games["away_180s"] = away_180s
pl_games["away_140s_plus"] = away_140s_plus

pl_games["home_darts_at_dbl"] = dbl_attempt_home
pl_games["away_darts_at_dbl"] = dbl_attempt_away
pl_games["home_legs"] = home_legs
pl_games["away_legs"] = away_legs

pl_games["winner"] = np.where(pl_games["home_legs"] > pl_games["away_legs"], 0, 1)

pl_games.to_excel("results.xlsx")
