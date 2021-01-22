from flask import Flask,render_template,url_for,request,redirect
import pandas as pd
from fpl_points_predictor.predict import make_prediction,top_n_players
from fpl_points_predictor.config import config


predictions = make_prediction()
top6=top_n_players(predictions,6)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict/',methods=['GET','POST'])
def predict():
    player_id=None
    if request.method=='POST':
        player_id=request.form.get('code')
        player_selected=next(player for player in predictions if player["code"] == int(player_id))
        return render_template('predict.html',title='Points predictor',players=predictions,cgw=int(config.CURRENT_GW),top6=top6,player_id=player_id,player_selected=player_selected)
    return render_template('predict.html',title='Points predictor',players=predictions,cgw=int(config.CURRENT_GW),top6=top6,player_id=player_id)

if __name__=='__main__':
    app.run()