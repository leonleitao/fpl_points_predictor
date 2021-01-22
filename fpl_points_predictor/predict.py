import pandas as pd
import numpy as np
import joblib

from fpl_points_predictor.config import config
from fpl_points_predictor.processing import processing as pr

def make_prediction()->list:
    """Make point predictions for the upcoming gameweek"""
    data=pd.read_csv(config.DATASET_DIR/config.DATASET_NAME)
    data=data[data['event']==config.CURRENT_GW]
    data=pr.convert_to_categorical(data,config.CATEGORICAL_COLS)
    data=pr.shorten_names(data)
    features=data.drop(config.DROP_COLS,axis=1)

    model=joblib.load(config.TRAINED_MODEL_DIR/config.TRAINED_MODEL_NAME)
    preds=model.predict(features)
    predictions=data.copy()[['event','first_name', 'second_name', 'team', 'position','opposition_team','code']]
    predictions['predicted_points']=np.round(preds).astype(int)
    predictions=predictions.drop_duplicates()
    predictions=predictions.to_dict('records')
    predictions=sorted(predictions, key=lambda k: k['first_name']) 
    return predictions

def top_n_players(predictions,n)->list:
    """Filter the predictions for the top n players"""
    predictions=sorted(predictions, key=lambda k: k['predicted_points'],reverse=True) 
    return (predictions[:n])



    