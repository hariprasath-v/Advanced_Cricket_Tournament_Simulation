

import pandas as pd


class Players():
    """
    Collect player information and return it in dataframe format.
    """
    def __init__(self):
        """
        Instance for the class Players.
        """
        #create player info dataframe
        self.data=pd.DataFrame(columns=['country','name','bowling','batting','fielding','running','experience'])
        self.data=self.data.round(2)
    def get_player_info(self,country: str, name: str, bowling: float, batting: float, fielding: float, running: float, experience: int):
        """
        :param country: country name
        :param name: player name
        :param bowling: bowling score
        :param batting: batting score
        :param fielding: fielding score
        :param running: running score
        :param experience: experience score
        """
        #Update player info dataframe
        self.data.loc[len(self.data)]=[country,name,bowling,batting,fielding,running,experience]

