import pandas as pd
import numpy as np
import requests

from fpl_points_predictor.config import config
from fpl_points_predictor.processing import feature_engineering as fe

def get_player_data():
    '''Connects to FPL api and returns a dataframe with player data'''
    # Make an api call
    url = config.API_URL_PLAYERS
    r = requests.get(url)
    json = r.json()
    # Convert to dataframe
    players = pd.DataFrame(json['elements'])
    teams = pd.DataFrame(json['teams'])
    # Merge dataframes to get team names
    players=pd.merge(players,teams[['id','short_name']],left_on='team',right_on='id')
    # Add position names for each player
    positions={1:'GKP',2:'DEF',3:'MID',4:'FWD'}
    players['position']=players.apply(lambda x: positions[x['element_type']],axis=1)
    # Rename columns
    players=players.rename(columns={'short_name':'team_name'})
    return players

def get_fixtures():
    '''Connects to FPL api and returns a dataframe with game fixtures '''
    # Make an api call
    url=config.API_URL_FIXTURES
    r = requests.get(url)
    json = r.json()
    # Convert to dataframe
    fixtures=pd.DataFrame(json)
    return fixtures

def get_gameweek_data():
    '''Connects to FPL api and returns a dataframe with player data for each gameweek'''
    gws=pd.DataFrame()
    # Makes an api call for each player with their player id and concatenates the dataframes
    for player_id in range (1,config.NUM_PLAYERS):
        url=config.API_URL_PLAYER_GW  + f'{player_id}/'
        r = requests.get(url)
        json = r.json()
        player_gw=pd.DataFrame(json['history'])
        gws=pd.concat([gws,player_gw])
    return gws

def download_and_clean_data():
    players = get_player_data()
    # Create dictionary to map team number to team name
    team_dict=dict(players[['team','team_name']].values)
    # Filtering player data to only required columns
    players = players[['id_x','first_name','second_name','team','position','code']]

    fixtures=get_fixtures()
    # Filtering the fixtures upto the current list of fixtures
    fixtures = fixtures[['event','team_a','team_h']]
    fixtures = fixtures[fixtures['event']<= config.CURRENT_GW]

    gws=get_gameweek_data()
    # Fmportant columns from the gws dataframe
    cols=['element','round','minutes','goals_scored', 'assists', 'clean_sheets', 'goals_conceded',
        'yellow_cards','red_cards', 'saves', 'bonus', 'bps', 'influence', 'creativity',
        'threat', 'ict_index', 'value','total_points']
    # Filter the gameweek data to only important columns
    gws=gws[cols]

    return (players,fixtures,gws,team_dict)

def add_features(players,fixtures,gws,team_dict):
    df = fe.add_home_flag(players,fixtures)
    df = fe.add_opposition_team(df)

    # List of stats from gws dataset that would be useful
    cols=['minutes','goals_scored', 'assists', 'clean_sheets', 'goals_conceded',
        'yellow_cards','red_cards', 'saves', 'bonus', 'bps', 'influence', 'creativity',
        'threat', 'ict_index', 'value']
    target_col=['total_points']
    # Merging the current dataframe with gws to include the above information
    df=pd.merge(df,gws,left_on=['id_x','event'],right_on=['element','round'],how='left').drop(['element','round'],axis=1)
    # Removing NA values that result from the merge. These NA's are because of new transfers as the player did not have scores/points for previous gameweeks.
    df=df[~((df['event']!=config.CURRENT_GW)&(df['total_points'].isna()))]

    # Get the average stats for each player for past gameweeks as well as average for last 3 gameweeks
    df=df.groupby('id_x').apply(lambda x: fe.get_average_stats(x,cols+target_col))
    df=df.groupby('id_x').apply(lambda x: fe.get_average_stats(x,cols+target_col,3))

    
    # Change team numbers to team names
    df=fe.change_team_number_to_name(df,team_dict)

    # Drop these columns as they cannot be used for new predictions
    df=df.drop(cols,axis=1)
    return df

def save_data(df):
    filedir=config.DATASET_DIR / config.DATASET_NAME
    df.to_csv(filedir,index=False,header=True)
    return None

if __name__=='__main__':
    players,fixtures,gws,team_dict=download_and_clean_data()
    df=add_features(players,fixtures,gws,team_dict)
    save_data(df)