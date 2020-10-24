import pandas as pd
import numpy as np
import get_data
from utils_feat_engineering import get_average_stats

players=get_data.get_player_data()
gws=get_data.get_gameweek_data()
fixtures=get_data.get_fixtures()

# Getting the current gameweek number
current_gw=max(set(gws['round']))+1

# Filtering player data to only required columns
players=players[['id_x','first_name','second_name','team','position']]
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
# Drop these columns as they cannot be used for new predictions
df=df.drop(cols,axis=1)

df.to_csv('data/data.csv',index=False,header=True)