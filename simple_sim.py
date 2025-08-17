# Runs a monte-carlo simulation for a Premier League format match, given 2 players treble and double hitting success rates.

import numpy as np
import random


# Create dictionaries to define what the player is to aim at.

# First, define 
target3 = {} # The target with 3 darts in hand
# Initially make all above 60 a treble 20, and all doubles the current score.
for i in range(61, 502):
    target3[i] = (20, "T")

for i in range(41, 61):
    target3[i] = (int(i-40), "S")

for i in range(2, 41, 2):
    target3[i] = (int(i/2), "D")

for i in range(3, 49, 2):
    target3[i] = (1, "S")


# Manually define the ideal numbers to be left on (left is most ideal, right is least)
ideals = [32, 40, 16, 24, 20, 36, 8, 28, 12, 30, 4, 38, 18, 14, 10, 34, 22, 2, 26, 6]
ideals.reverse()

# Reach a target number with a single if possible, then a treble if single is not possible.
for score in target3:
    for aim in ideals:
        if score not in ideals: # Check if we are on a double
            for i in range(1, 21):
                if score-i == aim:
                    target3[score] = (i, 'S')
                elif score-(3*i) == aim:
                    target3[score] = (i, 'T')

# Set scores greater than 171 to just "score" (e.g. either t20 or t19)
for i in range(171, 502):
    target3[i] = ("score", "T")

# Define dictonaries for 1 and 2 darts in hand
target2 = target3
target1 = target3

# Update 2 darts in hand logic to account for bullseye checkouts
bull_check = [110, 107, 104, 101]
for score in target2:
    for i in range(18, 21):
        if score-i in bull_check:
            target2[score] = (i, 'T')



# Define function that simulates a player's throw

def throw(score, inhand, player):
    checkout = 0
    original_score = score
    while inhand > 0 and checkout == 0:
        if inhand == 3:
            target_number, target_type = target3.get(score, (20, 'T'))
        elif inhand == 2:
            target_number, target_type = target2.get(score, (20, 'T'))
        elif inhand == 1:
            target_number, target_type = target1.get(score, (20, 'T'))
        elif inhand == 0:
            return(score, inhand, checkout)
        else:
            print("Error, inhand is not in range")
    
        r = random.random()
        p_switch = 0.25
        if target_type == 'T':
            if target_number == "score":
                r2 = random.random()
                if r2 < p_switch:
                    target_number = 19
                else:
                    target_number = 20
            if r < player['trebs'][target_number]:
                score -= target_number*3
            else:
                score -= target_number
            inhand -= 1
                
        elif target_type == 'D':
            if r < player['dbls'][target_number]:
                score -= target_number*2
                if score == 0:
                    checkout = 1
            else:
                r2 = random.random()
                change = target_number if r2 > 0.5 else 0
                score -= change
                if score == 1:
                    score = 2
            inhand -= 1
    
        elif target_type == 'S':
            score -= target_number
            inhand -= 1
            
        if score < 0 or score == 1:
            return (original_score, 0, 0)
            
    return(score, inhand, checkout)

# Function that simulates a leg between two players

def leg(start_throw, home_player, away_player):
    turn = start_throw
    home_score = 501
    away_score = 501
    home_totals = [home_score]
    away_totals = [away_score]
    checkout = 0
    winner = None
    home_darts = 0
    home_t_score = 0
    away_darts = 0
    away_t_score = 0
    while checkout == 0:
        if turn == 0:
            home_score, inhand, checkout = throw(home_score, 3, home_player)
            home_totals.append(home_score)
            home_darts += 3-inhand
            home_t_score += home_totals[-2] - home_totals[-1]            
            turn = 1
            if checkout == 1:
                winner = 0
        elif turn == 1:
            away_score, inhand, checkout = throw(away_score, 3, away_player)
            away_totals.append(away_score)
            away_darts += 3-inhand
            away_t_score += away_totals[-2] - away_totals[-1]            
            turn = 0
            if checkout == 1:
                winner = 1
    return(home_totals, away_totals, winner, home_darts, home_t_score, away_darts, away_t_score)

# Function that simulates a full match of a set number of legs

def match(best_of, home_player, away_player, start_throw):
    next_throw = start_throw
    win_score = round(best_of/2)
    legs_played = 0
    home_legs = 0
    away_legs = 0
    match_winner = None
    home_total_darts = 0
    home_total_score = 0
    away_total_darts = 0
    away_total_score = 0
    while max(home_legs, away_legs) < win_score:
        home_leg, away_leg, winner, home_darts, home_t_score, away_darts, away_t_score = leg(next_throw, home_player, away_player)
        home_total_darts += home_darts
        home_total_score += home_t_score
        away_total_darts += away_darts
        away_total_score += away_t_score
        next_throw = 1 if next_throw == 0 else 0
        legs_played += 1
        if winner == 0:
            home_legs += 1
        elif winner == 1:
            away_legs += 1
    score = [home_legs, away_legs]
    if score[0] > score[1]:
        match_winner = 0
    elif score[1] > score[0]:
        match_winner = 1

    home_match_avg = 3*home_total_score/home_total_darts
    away_match_avg = 3*away_total_score/away_total_darts
    return(score, match_winner, home_match_avg, away_match_avg)

# Function for monte carlo simulation of a PL game length

def pl_monte_carlo(home_player, away_player, original_throw, n):
    best_of = 11
    win_score = round(best_of/2)
    score_frequency = {}
    original_throw = 0
    for i in range(win_score):
        score_frequency[f"{win_score}-{i}"] = 0
    for i in range(win_score-1, -1, -1):
        score_frequency[f"{i}-{win_score}"] = 0
    
    n_original = n
    home_wins = 0
    away_wins = 0
    home_t_avg = []
    away_t_avg = []
    while n > 0:
        score, match_winner, home_avg, away_avg = match(best_of, home_player, away_player, original_throw)
        home_t_avg.append(home_avg)
        away_t_avg.append(away_avg)
        if match_winner == 0:
            home_wins += 1
        elif match_winner == 1:
            away_wins += 1
        h_legs = score[0]
        a_legs = score[1]
        score_frequency[f"{h_legs}-{a_legs}"] += 1
        n -= 1
    
    return(score_frequency, home_wins, away_wins, home_t_avg, away_t_avg)
