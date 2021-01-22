import pandas as pd
import numpy as np

def add_home_flag(players,fixtures) -> pd.DataFrame:
    """Adds a new column to denote if the match is home/away"""
    # Home fixtures for each player
    home=pd.merge(players,fixtures,left_on='team',right_on='team_h')
    # Away fixxtures for each player
    away=pd.merge(players,fixtures,left_on='team',right_on='team_a')
    # Concatenating home and away fixtures to a single dataframe
    df=pd.concat([home,away]).sort_values('event').reset_index(drop=True)

    # Adding a binary feature for home fixtures
    df['is_home']=np.where(df['team']==df['team_h'],1,0)
    return df

def add_opposition_team(df) -> pd.DataFrame:
    """Adds a new columns to denote the opposition team for a fixture"""
    # Adding a feature for the opposition team team number
    df['opposition_team']=np.where(df['is_home'],df['team_a'],df['team_h'])
    df=df.drop(['team_a','team_h'],axis=1)
    return df

def get_average_stats(df,cols,n=None) -> pd.DataFrame:
    '''Function to get the average stats of each player given a list of columns'''
    if n:
        colnames=['av({})_{}'.format(n,col) for col in cols]
        df[colnames]=df[cols].shift(1).rolling(n).mean().fillna(0)
        return df
    colnames=['av_{}'.format(col) for col in cols]
    df[colnames]=df[cols].shift(1).expanding().mean().fillna(0)
    return df

def change_team_number_to_name(df,team_dict) -> pd.DataFrame:
    """Changes a numeric team number to the team name"""
    df['team']=df['team'].apply(lambda x: team_dict[x])
    df['opposition_team']=df['opposition_team'].apply(lambda x: team_dict[x])
    return df