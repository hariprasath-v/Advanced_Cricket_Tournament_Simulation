
import pandas as pd
from IPython.display import display, HTML, Markdown

class Commentator:
    """
    The class is used to give commentary at the start and at the end.
    """
    def __init__(self):
        ...
    def match_info(self,date,season,team1,team2,toss_win,toss_dec,team1_sqaud,team2_sqaud):
        """
        Give match information
        """
        print(f"--"*100)
        print(f"Match Info")
        print(f"--"*100)
        print(f"Date:{date}\nseason:{season}\nTeam1:{team1}\nTeam2:{team2}\nToss Win:Toss Win by {toss_win} & opt to {toss_dec}\nTeam1 Squad:{team1_sqaud}\nTeam2 Squad:{team2_sqaud}")
        print(f"--"*100)
    def over_comm(self,over):
        """
        Over information
        """
        print(f"Over {over}")
    def player_out(self,player_name):
        """
        Wicket information
        """
        print(f"{player_name} Out!")
    def next_palyer(self,player_name):
        """
        Next player information
        """
        print(f"Next player {player_name}")
    def four_info(self,run):
        """
        Boundary information
        """
        print(f"That was {run}!")
    def six_info(self,run):
        """
        Six information
        """
        print(f"That was {run}!")
    def run_(self,run):
        """
        Run information
        """
        print(f"Got {run}")
    def over_summary(self, over_run):
        """
        Per over run information
        """
        print(f"This over so far {over_run}")
    def remain_wicket(self,wicket):
        """
        Remaining wicket information
        """
        print(f"Remaining Wicket:{wicket}")
    def run_summary(self,runs):
        """
        Run information
        """
        print(f"Runs:{runs}")
        print(f"=="*100)
    def total_runs(self, runs,over):
        """
        Total run information
        """
        print(f"{runs} Runs From {over} Overs")
    def match_summary(self,res_df):
        """
        Post match information
        """
        print(f"--"*100)
        print("Match Summary")
        print(f"--"*100)
        #display(res_df)
        #display(Markdown(res_df.to_markdown()))
        print(res_df.to_string(index=False))
        print(f"--"*100)
    def innings_summary(self,team_bat,innings_no,batter_summary_df,bowler_summary_df):
        """
        Post innings information
        """
        print(f"--"*100)
        print(f"{team_bat.capitalize()} Innings Summary")
        print(f"--"*100)
        print(f"^"*100)
        print("Scorecard")
        print(f"^"*100)
        print("Batter\n")
        print(batter_summary_df.to_string(index=False))
        print(f"^"*100)
        print("Bowler\n")
        print(bowler_summary_df.to_string(index=False))
        print(f"^"*100)
        print(f"--"*100)
