import pandas as pd
import numpy as np
import get_data


def get_average_stats(df,cols,n=None):
    '''Function to get the average stats of each player'''
    if n:
        colnames=['av({})_{}'.format(n,col) for col in cols]
        df[colnames]=df[cols].shift(1).rolling(n).mean().fillna(0)
        return df
    colnames=['av_{}'.format(col) for col in cols]
    df[colnames]=df[cols].shift(1).expanding().mean().fillna(0)
    return df

if __name__ == '__main__':
    players=get_data.get_player_data()
    gws=get_data.get_gameweek_data()
    fixtures=get_data.get_fixtures()

    # Getting the current gameweek number
    current_gw=max(set(gws['round']))+1
    # Create dictionary to map team number to team name
    team_dict=dict(players[['team','team_name']].values)

    # Filtering player data to only required columns
    players=players[['id_x','first_name','second_name','team','position','code']]
    # test=test[(test['id_x']==531)|(test['id_x']==390)|(test['id_x']==569)]

    # Filtering the fixtures upto the current list of fixtures
    fixtures=fixtures[['event','team_a','team_h']]
    fixtures=fixtures[fixtures['event']<= current_gw]

    # Home fixtures for each player
    home=pd.merge(players,fixtures,left_on='team',right_on='team_h')
    # Away fixxtures for each player
    away=pd.merge(players,fixtures,left_on='team',right_on='team_a')
    # Concatenating home and away fixtures to a single dataframe
    df=pd.concat([home,away]).sort_values('event').reset_index(drop=True)

    # Adding a binary feature for home fixtures
    df['is_home']=np.where(df['team']==df['team_h'],1,0)
    # Adding a feature for the opposition team team number
    df['opposition_team']=np.where(df['is_home'],df['team_a'],df['team_h'])
    df=df.drop(['team_a','team_h'],axis=1)

    # List of stats from gws dataset that would be useful
    cols=['minutes','goals_scored', 'assists', 'clean_sheets', 'goals_conceded',
        'yellow_cards','red_cards', 'saves', 'bonus', 'bps', 'influence', 'creativity',
        'threat', 'ict_index', 'value']
    target_col=['total_points',]
    # Merging the current dataframe with gws to include the above information
    df=pd.merge(df,gws[['element','round']+cols+target_col],left_on=['id_x','event'],right_on=['element','round'],how='left').drop(['element','round'],axis=1)
    # Removing NA values that result from the merge. These NA's are because of new transfers as the player did not have scores/points for previous gameweeks.
    df=df[~((df['event']!=current_gw)&(df['total_points'].isna()))]


    # Get the average stats for each player for past gameweeks as well as average for last 2 gameweeks
    df=df.groupby('id_x').apply(lambda x: get_average_stats(x,cols+target_col))
    df=df.groupby('id_x').apply(lambda x: get_average_stats(x,cols+target_col,2))
    # Change team numbers to team names
    df['team']=df['team'].apply(lambda x: team_dict[x])
    df['opposition_team']=df['opposition_team'].apply(lambda x: team_dict[x])
    # Drop these columns as they cannot be used for new predictions
    df=df.drop(cols,axis=1)

    # Save dataset as a csv file
    df.to_csv(f'data/data.csv',index=False,header=True)
