import pathlib

import fpl_points_predictor


PACKAGE_ROOT = pathlib.Path(fpl_points_predictor.__file__).resolve().parent
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"
DATASET_DIR = PACKAGE_ROOT / "datasets"

API_URL_PLAYERS = 'https://fantasy.premierleague.com/api/bootstrap-static/'
API_URL_FIXTURES = 'https://fantasy.premierleague.com/api/fixtures/'
API_URL_PLAYER_GW = 'https://fantasy.premierleague.com/api/element-summary/'

NUM_PLAYERS = 574

CURRENT_GW = 18

DATASET_NAME='fpl_data.csv'
TRAINED_MODEL_NAME=f'model.pkl'

CATEGORICAL_COLS=['first_name', 'second_name', 'position','id_x','team','is_home', 'opposition_team']
DROP_COLS=['event','total_points','first_name','second_name','code','av_value','av(3)_value']