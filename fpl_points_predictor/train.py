import pandas as pd
import lightgbm as lgb
import joblib

from fpl_points_predictor.config import config
from fpl_points_predictor.processing import processing as pr

def run_training():
    """Trains a lightbgm model on the data and saves it as a pickle file"""
    data=pd.read_csv(config.DATASET_DIR/config.DATASET_NAME)

    data=data[data['event']<config.CURRENT_GW]
    data=pr.convert_to_categorical(data,config.CATEGORICAL_COLS)
    features=data.drop(config.DROP_COLS,axis=1)
    target=data['total_points']
    
    model=lgb.LGBMRegressor(n_estimators=50)
    model.fit(features,target)
    joblib.dump(model,config.TRAINED_MODEL_DIR/config.TRAINED_MODEL_NAME)

if __name__=='__main__':
    run_training()

