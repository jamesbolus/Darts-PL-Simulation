# Darts-PL-Simulation
Files and codes for a simulation task based on Darts Premier League 2025. This code is only really posted as proof of my projects. It is very inefficient, using lots of loops etc. as I wanted to make it readable and easy for me to edit later.

## Betfair Starting Price Extractor
### betfair-sp-extractor
Code that shows how to extract starting prices from Betfair historical data .Tar files. tar_extractor.py shows how .tar files are extracted to .json format; sp_extractor.py shows how starting prices are obtained from the .json data. This is specific to the Darts Premier League 2025 but small changes could be made to apply it elsewhere.

## Feature Extraction
### feature-extractor
Code that shows how some of my metrics were extracted from JSON match data.

## Simulations
###  simple_sim
Code that shows the basic monte carlo simulation that is used to simulate a certain match. This relies on treble and double hit

### normal_backtesting
Code that shows how the simulation can be used in conjunction with normal distribution sampling to generate probailities for each player winning a certain match.
