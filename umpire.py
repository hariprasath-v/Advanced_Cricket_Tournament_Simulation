

import random

class Umpire:
    """
    Class to predict the outcome of the ball
    """
    def predict_ball_outcome(self,batter_stats,bowler_stats):
        """
        :param batter_stats: batter information
        :param bowler_stats: bowler information
        """
        if batter_stats>bowler_stats: #if Batter stats are greater than bowler stats then the possibility of outcome changes
            return random.choices([0,1],[0.2,0.8])[0] #80 percentage chance for legal delivery and 20 percentage chance for out(bowled)
        else: #if Batter stats are not greater than bowler stats then the possibility of outcome changes
            return random.choices([0,1],[0.6,0.4])[0] #60 percentage chance for out(bowled) and 40 percentage chance for legal delivery
