
import pandas as pd
import copy
import numpy as np
import random



class Teams():
    """
    This class used to select the team captain, batting order, and bowlers list based on the player informations.
    """
    def __init__(self,player_list_df):
        """
        Instance for the class Teams.

        :param player_list_df:list of players and player information in dataframe format.

        """
        self.player_list_df=player_list_df #Player information dataframe
        self.captain=self._select_captain() #Call the method to select the captain
        self.batting_order=self._batting_order() #Call the method to get batting order
        self.choose_bowler=self._choose_bowler() #Call the method to get top five bowlers
        self.country=self._country_name() #Call the method to get the country name
    def _select_captain(self):
        """
        Select the team captain based on batting, fileding, and experience score.
        """
        temp_df=self.player_list_df.copy(deep=True)
        temp_df['rank']=temp_df.apply(lambda x:np.mean([x.batting,x.fielding,x.experience]),axis=1)
        value=temp_df[temp_df['rank']==max(temp_df['rank'])]['name'].values[0]
        return value
        del temp_df
    def _batting_order(self):
        """
        Select the batting order based on batting, and experience score.
        """
        temp_df=self.player_list_df.copy(deep=True)
        temp_df['rank']=temp_df.apply(lambda x:np.mean([x.batting,x.experience]),axis=1)
        value=temp_df.sort_values('rank',ascending=False)['name'].values
        return value
        del temp_df
    def _choose_bowler(self):
        """
        Select top five bowlers based on bowling, and experience score.
        """
        temp_df=self.player_list_df.copy(deep=True)
        temp_df['rank']=temp_df.apply(lambda x:np.mean([x.bowling,x.experience]),axis=1)
        value=temp_df.nlargest(5,'rank')['name'].values
        return value
        del temp_df
    def _country_name(self):
        """
        Select country name from player information dataframe.
        """
        return self.player_list_df['country'].unique()[0]




