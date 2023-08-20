# Advanced_Cricket_Tournament_Simulation

Simulate cricket matches between two teams with this command-line program.

## Overview

The Cricket Simulation Program allows you to simulate cricket matches and analyze player performances. The simulation program consists of the following classes.
- Players: This class gathers player information and presents it in a structured dataframe format.
- Teams: Utilize the Teams class to designate team captains, arrange batting orders, and establish the list of bowlers. It leverages player information to make informed decisions.
- Umpire: The Umpire class plays a pivotal role in predicting ball outcomes, enhancing the simulation's authenticity.
- Commentator: Enjoy dynamic match commentary throughout the simulation with the Commentator class, adding a lively aspect to the experience.
- Match: The Match class encapsulates the core simulation, replicating the dynamics of a cricket game.


## Features

- Simulate matches between custom-named teams.
- Set the number of overs for each match.
- Display detailed statistics for each player, including runs scored, wickets taken, and more.


## Installation
1. Clone the repository
```python
git clone https://github.com/hariprasath-v/Advanced_Cricket_Tournament_Simulation.git
```
2. Navigate to the cloned repo directory
```python
cd Advanced_Cricket_Tournament_Simulation
```
3. Install dependencies
```python
pip install -r requirements.txt
```

## Usage
run the play.py (The player's information can be changed in this file)

The simulation proceeds through the following stages:

1. Player Information Collection
2. Captain, Batter, and Bowler Selection
3. Coin Flip to Determine Play Choice
4. First Innings Simulation
5. Second Innings Simulation
6. Post-Match Summary

After the simulation, the program generates the following files within the folder named by the date of the simulation and both team names:

- Innings Scorecard (Image Format)
- Ball-by-Ball Summary (DataFrame Format)
- Match Result (DataFrame Format)
- Team's Score Comparison Chart (Image Format)

### Demo simulation

Sample Scorecard
![Alt text](https://github.com/hariprasath-v/Advanced_Cricket_Tournament_Simulation/blob/main/Country_a%20vs%20Country_b%202023-08-20/Country_a%20Scorecard.jpg)

Sample Score Comparison
![Alt text](https://github.com/hariprasath-v/Advanced_Cricket_Tournament_Simulation/blob/main/Country_a%20vs%20Country_b%202023-08-20/Team%20Score%20Comparison.jpg)


