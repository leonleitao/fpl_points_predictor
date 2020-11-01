from flask import Flask,render_template,url_for,request,redirect
from flask_wtf import FlaskForm
from wtforms import SelectField
import os
import pandas as pd

all_players=pd.read_csv('data/predictions.csv').to_dict('records')
current_gw=all_players[0]['event']

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict/',methods=['GET','POST'])
def predict():
    player_id=None
    if request.method=='POST':
        player_id=request.form.get('code')
        player_selected=next(player for player in all_players if player["code"] == int(player_id))
        return render_template('predict.html',title='Points predictor',players=all_players,cgw=int(current_gw),player_id=player_id,player_selected=player_selected)
    return render_template('predict.html',title='Points predictor',players=all_players,cgw=int(current_gw),player_id=player_id)

if __name__=='__main__':
    app.run(debug=True)