


import random

from player import *
from team import *

from play_match import *


player_set1=Players()
player_set2=Players()

for i in range(11):
    player_set1.get_player_info(country='country_a',
                                name=f"a_{i}",
                                bowling=random.uniform(0.2, 0.8),
                                batting=random.uniform(0.2, 0.8),
                                fielding=random.uniform(0.2, 0.8),
                                running=random.uniform(0.2, 0.8),
                                experience=random.uniform(0.2, 0.9))
    player_set2.get_player_info(country='country_b',
                                name=f"b_{i}",
                                bowling=random.uniform(0.2, 0.8),
                                batting=random.uniform(0.2, 0.8),
                                fielding=random.uniform(0.2, 0.8),
                                running=random.uniform(0.2, 0.8),
                                experience=random.uniform(0.2, 0.9))

team1=Teams(player_set1.data)
team2=Teams(player_set2.data)
crick_match=Match(10,team1,team2)
crick_match.toss()
crick_match.start_match()



