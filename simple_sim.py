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

# Define dictonaries for 1 and 2 darts in hand
target2 = target3
target1 = target3

# Update 2 darts in hand logic to account for bullseye checkouts
bull_check = [110, 107, 104, 101]
for score in target2:
    for i in range(18, 21):
        if score-i in bull_check:
            target2[score] = (i, 'T')


