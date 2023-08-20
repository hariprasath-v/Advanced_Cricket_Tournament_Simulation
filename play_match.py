

import pandas as pd
import copy
import numpy as np
import random
import os
from IPython.display import display, HTML, Markdown
import seaborn as sns
from matplotlib import  pyplot as plt

from commentator import Commentator
from umpire import  Umpire

class Match:
    """
    Simulate Cricket Match.

    The Class providing methods for perform a coin flip, play first innings, play second innings.
    """
    def __init__(self,over: int,team1_player_obj: object,team2_player_obj: object):
        """
        Initialize Match Instance.

        :param over: Number of over to play innings
        :param team1_player_obj: First innings team
        :param team2_player_obj: Second innings team
        """
        self.over=over #Number of over
        self.team1_player_obj=team1_player_obj #Team1 object that conatins batting order, bowlers list, captain name, country.
        self.team2_player_obj=team2_player_obj #Team2 object that conatins batting order, bowlers list, captain name, country.
        self.toss_win_team=None #Store the toss winning team name
        self.play_choice=None #Store the choice of play
        self.bat_team=None #Store the batting team object
        self.bowl_team=None #Store the bowling team object
        #Create a dataframe to store the ball by ball summary
        self.df=pd.DataFrame(columns=['innings','over','ball','striker','bowler','non-striker','wicket','run','four','six','total_run'])
        self.team1_total_run=0 #Store first innings team runs
        self.team2_total_run=0 #Store second innings team run
        #Create a  dataframe to store match summary
        self.match_result=pd.DataFrame(columns=['Date','Season','Team1','Team2','Toss_Win','Toss_Decision','Team1_Run','Team2_Run','Winning_Team','Margin'])
        self.status=None
        self.temp_df=None
        self.path=""

        #Store the country name and the respective team's captain name in a dictionary
        self.country_captain_dict={f"{self.team1_player_obj.player_list_df['country'].unique()[0]}":f"{self.team1_player_obj.captain}",
                                f"{self.team2_player_obj.player_list_df['country'].unique()[0]}":f"{self.team2_player_obj.captain}"}

        #Store the country name and the respective team's object in a dictionaryy
        self.country_obj={f"{team1_player_obj.player_list_df['country'].unique()[0]}":self.team1_player_obj,
                                f"{team2_player_obj.player_list_df['country'].unique()[0]}":self.team2_player_obj}


    def toss(self):
        """
        Flip a Coin to Decide the Choice of Play, Batting Team, and Bowling Team.

        Choose a random captain from the captain list and the choice of coin side (H, T).
        Flip a coin. If the flipped coin side matches the chosen coin side, then select the choice of play ("Batting", "Bowling").
        Based on the choice of play, assign a batting team and a bowling team.
        """
        choice_captain=random.choice([self.team1_player_obj.captain,self.team2_player_obj.captain]) #Select random captain from two teams to determine a play
        coin_choice=random.choice(['H','T'])  #Random choice of coin sides
        toss_coin=random.choice(['H','T']) #Flip a coin
        if coin_choice==toss_coin: #Check whether choosen side is equal to outcome of coin flip
            self.play_choice=random.choice(['Bat','Bowl']) #Choose Random Choice Between Batting and Bowling
            self.toss_win_team=[key for key,val in self.country_captain_dict.items() if val==choice_captain][0] #Select Toss Winning Team Based on Team Captain Name
            print(f"{self.toss_win_team} Won the Toss and opt to {self.play_choice} First") #Print Toss Won Team And Choice of Play
            if self.play_choice=='Bat': #If Play Choice is Batting
                self.bat_team=[val for key,val in self.country_obj.items() if key==self.toss_win_team][0] #Select Batting Team
                self.bowl_team=[val for key,val in self.country_obj.items() if key!=self.toss_win_team][0] #Select Bowling Team
            elif self.play_choice=='Bowl': #If Play Choice is Bowling
                self.bowl_team=[val for key,val in self.country_obj.items() if key==self.toss_win_team][0] #Select Bowling Team
                self.bat_team=[val for key,val in self.country_obj.items() if key!=self.toss_win_team][0] #Select Batting Team
        else: #Choosen side is not equal to outcome of coin flip
            self.play_choice=random.choice(['Bat','Bowl'])  #Choose Random Choice Between Batting and Bowling
            self.toss_win_team=[key for key,val in self.country_captain_dict.items() if val!=choice_captain][0]  #Select Toss Winning Team Based on Team Captain Name
            print(f"{self.toss_win_team} Won the Toss and opt to {self.play_choice} First") #Print Toss Won Team And Choice of Play
            if self.play_choice=='Bat': #If Play Choice is Batting
                self.bat_team=[val for key,val in self.country_obj.items() if key==self.toss_win_team][0]  #Select Batting Team
                self.bowl_team=[val for key,val in self.country_obj.items() if key!=self.toss_win_team][0]  #Select Bowling Team
            elif self.play_choice=='Bowl':
                self.bowl_team=[val for key,val in self.country_obj.items() if key==self.toss_win_team][0]  #Select Bowling Team
                self.bat_team=[val for key,val in self.country_obj.items() if key!=self.toss_win_team][0]  #Select Batting Team

    def start_match(self):
        """
        Method to call other methods.

        1.Call match_info method from Commentator class and provide match information
        2.start the first innings
        3.start the second innings
        3.call the result function to store the match summary
        4.Print the match summary using match_summary method from Commentator class
        5.Print the first innings summary using innings_summary method from Commentator class
        6.Print the second innings summary using innings_summary method from Commentator class
        """
        #Match info at start
        Commentator().match_info(pd.Timestamp.today().date(),
                                pd.Timestamp.today().date().year,
                                self.bat_team.country,
                                self.bowl_team.country,
                                self.toss_win_team,
                                self.play_choice,
                                self.bat_team.player_list_df['name'].values,
                                self.bowl_team.player_list_df['name'].values)
        #Play first innings
        self.play_innings_1(over=self.over,team1_bat=self.bat_team.batting_order,team2_bowl=self.bowl_team.choose_bowler)

        #Play second innings
        self.play_innings_2(over=self.over,team1_bat=self.bowl_team.batting_order,team2_bowl=self.bat_team.choose_bowler)
        self.result() #Match result
        Commentator().match_summary(self.match_result) #Match summary at the end
        Commentator().innings_summary(self.bat_team.country,1,self.batter_summary(1),self.bowler_summary(1)) #First innings Summary
        Commentator().innings_summary(self.bowl_team.country,2,self.batter_summary(2),self.bowler_summary(2)) #Second innings Summary
        self.create_dir() #Create directory with team names and match date
        #Save first innings scorecard
        self.innings_scorecard_plot(self.batter_summary(1),self.bowler_summary(1) ,team_name=self.bat_team.country,path=self.path)
        #Save second innings scorecard
        self.innings_scorecard_plot(self.batter_summary(2),self.bowler_summary(2) ,team_name=self.bowl_team.country,path=self.path)
        self.score_comparison_plot(path=self.path) #Save score comparison chart
        self.df.to_csv(f"{self.path}/Ball_by_Ball Summary.csv",index=False) #Save Ball_by_Ball summary in csv format
        self.match_result.to_csv(f"{self.path}/Match Result Summary.csv",index=False) #Save match result summary in csv format

    def batter_summary(self,innings_no):
        return self.df[self.df['innings']==innings_no].groupby('striker').agg({'run':'sum','ball':'count','four':'sum','six':'sum'}).\
                reset_index().assign(strike_rate=lambda x:round((x.run/x.ball)*100,2))

    def bowler_summary(self,innings_no):
        return self.df[self.df['innings']==innings_no].groupby('bowler').\
                agg({'ball':'count','run':'sum','wicket':'sum'}).\
                reset_index().assign(over=lambda x: round(x.ball/6,1),\
                     economy_rate=lambda x: round(x.run/x.over,1).replace(np.inf, np.nan).fillna(0),
                     bowling_strike_rate=lambda x: round(x.ball/x.wicket,1).replace(np.inf, np.nan).fillna(0),
                     bowling_average=lambda x: round(x.run/x.wicket,1).replace(np.inf, np.nan).fillna(0))


    def update_run(self):
        self.run_info={'country':[f"{self.bat_team.country}", f"{self.bowl_team.country}"],
                       'score':[self.team1_total_run,self.team2_total_run]}

    def check_result(self):
        """
        Check final result after two innings.
        """
        if self.team1_total_run>self.team2_total_run: #Check whether the first batting team runs greater than second batting team run
            self.status=f"{self.bat_team.country}"
            return self.status
        elif self.team1_total_run==self.team2_total_run: #If first batting team runs equal to second batting team run then return match is draw.
            self.status="Match_tie"
            return self.status
        else: #If condition not satisfies return the second batting team won the match
            self.status=f"{self.bowl_team.country}"
            return self.status


    def result(self):
        """
        Prepare match summary after two innings.
        """
        self.match_result.loc[len(self.match_result)]=[pd.Timestamp.today().date(), #Generate Today Date
                                                       pd.Timestamp.today().date().year, #Extract Year From Generated Date
                                                       self.bat_team.country, #Batting Team Name
                                                       self.bowl_team.country, #Bowling Team name
                                                       self.toss_win_team, #Toss Won Team
                                                       self.play_choice, #Play choice of Toss Won Team
                                                       self.team1_total_run, #First Innings Team Total Runs
                                                       self.team2_total_run, #SecondInnings Team Total Runs
                                                       str(self.check_result()), #Function for Select the Winning Team
                                                       np.abs(self.team1_total_run-self.team2_total_run) #Winning Margin
                                                       ]



    def play_innings_1(self,over: int, team1_bat: list, team2_bowl: list):
        """
        Play first Innings.

        :param over: Number of over to play innings
        :param team1_bat: Batting team player list
        :param team2_bowl: Bowling team player list
        """
        print("*"*100)
        print("1st Innings")
        print("*"*100)
        team1_bat1=list(team1_bat) #Convert array of values to list
        striker=0 #Initial striker postion index for the batting team player list
        non_striker=1 #Non-striker postion index for the batting team player list
        wicket=0 #Wicket count
        balls=0 #Ball count
        for ovr in range(1,over+1): #Iterate over the range of over
            bowler=random.choices(team2_bowl,[0.2,0.2,0.2,0.2,0.2])[0] #choose random bowler from bowling player list
            if striker > len(team1_bat1)-1: #If striker position is greater than length of player list then break the loop and end it
                break #Break and end the loop
            Commentator().over_comm(ovr) #Over commentry
            over_runs=[] #List to store per over runs
            for ball_dlivery in range(1,7): #Iterate over range of 7
                balls+=1 #Increase the ball count by 1
                #Get the mean of batter batting, running, and total experience value
                batter_stats=self.bat_team.player_list_df[self.bat_team.player_list_df['name']==team1_bat1[striker]]\
                                                    [['batting', 'running', 'experience']].mean(axis=1).values[0]

                #Get the mean of bowler bwoling, fielding, and total experience value
                bowler_stats=self.bowl_team.player_list_df[self.bowl_team.player_list_df['name']==bowler]\
                                                            [['bowling', 'fielding', 'experience']].mean(axis=1).values[0]
                ball=Umpire().predict_ball_outcome(batter_stats,bowler_stats) #Predict the ball outcome by using batter and bowler stats
                #The iteration only run when folowing statment is true otherwise iteration will be ended
                if striker is not None and non_striker is not None and striker < len(team1_bat1):
                    if ball==0: #If predicted ball outcome is zero
                        wicket+=1 #Update the wicket by 1
                        over_runs.append('0w') #Append 0w to the list over_runs
                        self.team1_total_run+=0 #add team1_total_run value by 0
                        #Update the ball by by summary dataframe
                        self.df.loc[len(self.df)]=[1,ovr,ball_dlivery,team1_bat1[striker],bowler,team1_bat1[non_striker],1,0,0,0,self.team1_total_run]
                        Commentator().player_out(team1_bat1[striker]) #Commentary to show current wicket name
                        if striker>non_striker: #if striker index value greater than non striker index
                            striker+=1 #update striker index by 1
                            if striker > len(team1_bat1)-1:  #if striker index value greater than length batting player list
                                Commentator().over_summary(over_runs) #Commentary to show over summary
                                Commentator().run_summary(self.team1_total_run)  #Commentary to show run summary
                                break #Break and end the loop
                            Commentator().next_palyer(team1_bat1[striker]) #Commentary to show next player name batting player list based on the striker value
                            Commentator().remain_wicket(9-wicket)  #Commentary to show remaining wicket count
                            striker,non_striker=non_striker,striker #Swap the striker and non-striker
                        else:#if striker index value not greater than non striker index
                            striker=non_striker+1 #Increase the non-striker index by 1 and assign to striker
                            if striker > len(team1_bat1)-1: #if striker index value greater than length batting player list
                                Commentator().over_summary(over_runs) #Commentary to show over summary
                                Commentator().run_summary(self.team1_total_run) #Commentary to show run summary
                                break #Break and end the loop
                            Commentator().next_palyer(team1_bat1[striker]) #Commentary to show next player name batting player list based on the striker value
                            Commentator().remain_wicket(9-wicket) #Commentary to show remaining wicket count
                            striker,non_striker=non_striker,striker #Swap the striker and non-striker
                    else: #If predicted ball outcome is not zero
                        if striker > len(team1_bat1)-1: #if striker index value greater than length batting player list
                            Commentator().over_summary(over_runs) #Commentary to show over summary
                            Commentator().run_summary(self.team1_total_run) #Commentary to show run summary
                            break #Break and end the loop
                        #Random choices among the numbers [0,1,2,3,4,6].If delivery is legal one, then striker would hit the ball and possibly get runs like [0,1,2,3,4,6]
                        #run=random.choices([0,1,2,3,4,6],[0.1,0.2,0.2,0.1,0.3,0.1])[0]
                        run=random.choice([0,1,2,3,4,6])
                        if run==4: #If random choice of number is 4
                            over_runs.append(run) #Append the run to over_runs list
                            Commentator().four_info(run)  #Commentary to show run info
                            self.team1_total_run+=run #increase team1_total_run value by 4
                            #Update the ball by by summary dataframe
                            self.df.loc[len(self.df)]=[1,ovr,ball_dlivery,team1_bat1[striker],bowler,team1_bat1[non_striker],0,run,1,0,self.team1_total_run]
                        elif run==6:  #If random choice of number is 4
                            over_runs.append(run) #Append the run to over_runs list
                            Commentator().six_info(run) #Commentary to show run info
                            self.team1_total_run+=run #increase team1_total_run value by 6
                            #Update the ball by by summary dataframe
                            self.df.loc[len(self.df)]=[1,ovr,ball_dlivery,team1_bat1[striker],bowler,team1_bat1[non_striker],0,run,0,1,self.team1_total_run]
                        else:  #If the random choice of number is neither 4 nor 6
                            over_runs.append(run) #Append the run to over_runs list
                            Commentator().run_(run) #Commentary to show run info
                            self.team1_total_run+=run #increase team1_total_run value random choice number
                            #Update the ball by by summary dataframe
                            self.df.loc[len(self.df)]=[1,ovr,ball_dlivery,team1_bat1[striker],bowler,team1_bat1[non_striker],0,run,0,0,self.team1_total_run]
                        #print([ovr,ball_dlivery,striker,bowler,non_striker,0,run])
                        if run in [1,3]: #If striker get run 1 or 3 , the striker and non-striker positions should be swapped
                            striker,non_striker=non_striker,striker #Swap the striker and non-striker
                    if ball_dlivery==6: #If ball number is 6
                        Commentator().over_summary(over_runs)  #Commentary to show over summary
                        Commentator().run_summary(self.team1_total_run)  #Commentary to show run summary
                        striker,non_striker=non_striker,striker #Swap the striker and non-striker


                else:
                    break
        Commentator().total_runs(self.team1_total_run,round(balls/6,1))
        print("*"*100)
        print("1st Innings Over")
        print("*"*100)


    def play_innings_2(self,over,team1_bat,team2_bowl):
        """
        Play second Innings. In second innings, the team will play to chase the first innings team total run.

        :param over: Number of over to play innings
        :param team1_bat: Batting team player list
        :param team2_bowl: Bowling team player list
        """
        print("*"*100)
        print("2nd Innings")
        print("*"*100)
        team1_bat1=list(team1_bat)  #Convert array of values to list
        striker=0  #Initial striker postion index for the batting team player list
        non_striker=1  #Non-striker postion index for the batting team player list
        wicket=0 #Wicket count
        balls=0 #Ball count
        for ovr in range(1,over+1):  #Iterate over the range of over
            bowler=random.choices(team2_bowl,[0.2,0.2,0.2,0.2,0.2])[0] #choose random bowler from bowling player list
            if self.team2_total_run>self.team1_total_run: #If second innings team total runs greater than first innings team total runs
                break #Break and end the loop
            if striker > len(team1_bat1)-1: #If striker position is greater than length of player list then break the loop and end it
                break #Break and end the loop
            Commentator().over_comm(ovr)  #Over commentry
            over_runs=[] #List to store per over runs
            for ball_dlivery in range(1,7):  #Iterate over the range of over
                balls+=1 #Increase the ball count by 1
                if self.team2_total_run>self.team1_total_run:  #If second innings team total runs greater than first innings team total runs
                    Commentator().over_summary(over_runs)  #Commentary to show over summary
                    Commentator().run_summary(self.team2_total_run)  #Commentary to show run summary
                    break #Break and end the loop
                #Get the mean of batter batting, running, and total experience value
                batter_stats=self.bowl_team.player_list_df[self.bowl_team.player_list_df['name']==team1_bat1[striker]]\
                                                    [['batting', 'running', 'experience']].mean(axis=1).values[0]
                #Get the mean of batter bowling, fielding, and total experience value
                bowler_stats=self.bat_team.player_list_df[self.bat_team.player_list_df['name']==bowler]\
                                                            [['bowling', 'fielding', 'experience']].mean(axis=1).values[0]
                ball=Umpire().predict_ball_outcome(batter_stats,bowler_stats) #Predict the ball outcome by using batter and bowler statse
                #Iteration only run when folowing statment is true otherwise iteration will be ended
                if striker is not None and non_striker is not None and striker < len(team1_bat1):
                    if ball==0: #If predicted ball outcome is zero
                        wicket+=1 #Update the wicket by 1
                        over_runs.append('0w') #append 0w to over_runs list
                        self.team2_total_run+=0 #Add 0 to team2_total_run
                        #Update the ball by by summary dataframe
                        self.df.loc[len(self.df)]=[2,ovr,ball_dlivery,team1_bat1[striker],bowler,team1_bat1[non_striker],1,0,0,0,self.team2_total_run]
                        Commentator().player_out(team1_bat1[striker])#Commentary to show current wicket name

                        if striker>non_striker:  #if striker index value greater than non striker index
                            striker+=1 #Update the striker index by 1
                            if striker > len(team1_bat1)-1:  #If striker position is greater than length of player list then break the loop and end it
                                Commentator().over_summary(over_runs) #Commentary to show over summary
                                Commentator().run_summary(self.team2_total_run) #Commentary to show run summary
                                break #Break and end the loop
                            Commentator().next_palyer(team1_bat1[striker])  #Commentary to show next player name batting player list based on the striker value
                            Commentator().remain_wicket(9-wicket)  #Commentary to show remaining wicket count
                            striker,non_striker=non_striker,striker #Swap stiker and non-striker position
                        else:  #if striker index value not greater than non striker index
                            striker=non_striker+1 #Increase the non-striker index by 1 and assign to striker
                            if striker > len(team1_bat1)-1:  #If striker position is greater than length of player list then break the loop and end it
                                Commentator().over_summary(over_runs)  #Commentary to show over summary
                                Commentator().run_summary(self.team2_total_run)  #Commentary to show run summary
                                break #Break and end the loop
                            Commentator().next_palyer(team1_bat1[striker])  #Commentary to show next player name batting player list based on the striker value
                            Commentator().remain_wicket(9-wicket)  #Commentary to show remaining wicket count
                            striker,non_striker=non_striker,striker  #Swap stiker and non-striker position
                    else:#If predicted ball outcome is not zero
                        if striker > len(team1_bat1)-1: #If striker position is greater than length of player list then break the loop and end it
                            Commentator().over_summary(over_runs)  #Commentary to show over summary
                            break  #Break and end the loop
                         #Random choices among the numbers [0,1,2,3,4,6].If delivery is legal one, then striker would hit the ball and possibly get runs like [0,1,2,3,4,6]
                        #run=random.choices([0,1,2,3,4,6],[0.1,0.2,0.2,0.1,0.3,0.1])[0]
                        run=random.choice([0,1,2,3,4,6])
                        if run==4: #if run is 4
                            over_runs.append(run)  #append 4 to over_runs list
                            Commentator().four_info(run) #Commentary to four summary
                            self.team2_total_run+=run #Increase team2_total_run by 4
                            #Update the ball by by summary dataframe
                            self.df.loc[len(self.df)]=[2,ovr,ball_dlivery,team1_bat1[striker],bowler,team1_bat1[non_striker],0,run,1,0,self.team2_total_run]
                        elif run==6: #if run is 6
                            over_runs.append(run) #append 6 to over_runs list
                            Commentator().six_info(run) #Commentary to six summary
                            self.team2_total_run+=run  #Increase team2_total_run by 6
                            #Update the ball by by summary dataframe
                            self.df.loc[len(self.df)]=[2,ovr,ball_dlivery,team1_bat1[striker],bowler,team1_bat1[non_striker],0,run,0,1,self.team2_total_run]
                        else: #If the random choice of number is neither 4 nor 6
                            over_runs.append(run)  #Append random choice over_runs list
                            Commentator().run_(run)  #Commentary to show run info
                            self.team2_total_run+=run  #Increase team2_total_run by random choice
                            #Update the ball by by summary dataframe
                            self.df.loc[len(self.df)]=[2,ovr,ball_dlivery,team1_bat1[striker],bowler,team1_bat1[non_striker],0,run,0,0,self.team2_total_run]
                        if run in [1,3]:  #If striker get run 1 or 3 , the striker and non-striker positions should be swapped
                            striker,non_striker=non_striker,striker  #Swap stiker and non-striker position
                    if ball_dlivery==6: #If ball number is six
                        Commentator().over_summary(over_runs)  #Commentary to show over run summary
                        Commentator().run_summary(self.team2_total_run) #Commentary to show run summary
                        striker,non_striker=non_striker,striker #Swap stiker and non-striker position
                    if self.team2_total_run>self.team1_total_run: #If second innings team total runs greater than first innings team total runs
                        Commentator().over_summary(over_runs)  #Commentary to show over run summary
                        Commentator().run_summary(self.team2_total_run)  #Commentary to show run summary
                        break  #Break and end the loop
                else:
                    break

        Commentator().total_runs(self.team2_total_run,round(balls/6,1))
        print("*"*100)
        print("2nd Innings Over")
        print("*"*100)

    def innings_scorecard_plot(self,batter_df,bowler_df ,team_name="",path=''):
        """
        Create innings scorecard and save it in jpg format.
        """
        plt.rcParams.update({'text.color': "white"})
        fig,(ax1, ax2) = plt.subplots(nrows=2,figsize=(12,6))
        tbl1=ax1.table(cellText = batter_df.values,colLabels=[col.capitalize() for col in batter_df.columns],
                       loc='upper center',rowLoc='center',colLoc="right",edges ="horizontal",)
        ax1.axis('off')
        tbl1.auto_set_font_size(False)
        tbl1.set_fontsize(10)
        ax1.set_title("\n\nBatter")
        tbl2=ax2.table(cellText = bowler_df.values,colLabels=[col.capitalize() for col in bowler_df.columns],
                       loc='upper center',rowLoc='center',colLoc="right",edges ="horizontal",)
        ax2.axis('off')
        tbl2.auto_set_font_size(False)
        tbl2.set_fontsize(10)
        ax2.set_title("\nBowler")
        fig.tight_layout()
        fig.set_facecolor('#3c4142')
        #open', 'closed', 'horizontal', 'vertical'
        plt.suptitle(f"{team_name.capitalize()} Innings Scorecard")
        fig.savefig(f"{path}/{team_name.capitalize()} Scorecard.jpg",dpi=600)
        plt.close()

    def score_comparison_plot(self,path=''):
        """
        Team's score comparison using line chart and save it in jpg format.
        """
        self.temp_df=pd.concat([self.bat_team.player_list_df,self.bowl_team.player_list_df],axis=0)[['name','country']]
        self.temp_df=pd.merge(self.df,self.temp_df,how='left',left_on='striker',right_on='name')
        plt.rcParams.update({'text.color': "black"})
        fig,ax= plt.subplots(nrows=1,figsize=(6,4))
        ax=sns.pointplot(self.temp_df,x='over',y='total_run',hue='country',errorbar=None,)
        ax.set_xlabel("Overs")
        ax.set_ylabel("Runs")
        ax.set_title(f"{self.winning_info()}")
        fig.suptitle("Team Score Comparsion",fontsize=18)
        fig.tight_layout()
        legend = plt.legend()
        legend.set_title('')
        fig.savefig(f"{path}/Team Score Comparison.jpg",dpi=600)
        plt.close()

    def winning_info(self):
        """
        Post match information
        """
        if self.match_result['Margin'].values[0]==0:
            return "Match Tie"
        else:
            res1=f"{self.match_result['Winning_Team'].values[0].capitalize()} Won by {self.match_result['Margin'].values[0]}"
            res2=f"{' Run' if self.match_result['Margin'].values[0]==1 else ' Runs'}"
            return  res1+res2

    def create_dir(self):
        """
        Create directory with team names and match date.
        """
        self.path=f"{self.match_result['Team1'].values[0].capitalize()} vs {self.match_result['Team2'].values[0].capitalize()} {self.match_result['Date'].values[0]}"
        os.makedirs(self.path,exist_ok=True)






