import pandas as pd
import numpy as np
import requests

def get_player_data():
    '''Connects to FPL api and returns a dataframe with player data'''
    # Make an api call
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
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
    url='https://fantasy.premierleague.com/api/fixtures/'
    r = requests.get(url)
    json = r.json()
    # Convert to dataframe
    fixtures=pd.DataFrame(json)
    return fixtures

def get_gameweek_data():
    '''Connects to FPL api and returns a dataframe with player data for each gameweek'''
    gws=pd.DataFrame()
    # Makes an api call for each player with their player id and concatenates the dataframes
    for player_id in range (1,574):
        url='https://fantasy.premierleague.com/api/element-summary/{}/'.format(player_id)
        r = requests.get(url)
        json = r.json()
        player_gw=pd.DataFrame(json['history'])
        gws=pd.concat([gws,player_gw])
    return gws