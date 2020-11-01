# FPL Points Predictor
## What is FPL?
Fantasy Premier League (FPL) is a game that casts you in the role of a Fantasy manager. You are given the task to pick a squad of real-life players who score points for your team based on their performances in their own matches.<br>
For more information visit the <a href="https://fantasy.premierleague.com/">official website</a>.

## Objective
The goal of this project is to use machine learning to predict the points that each player will get in the next gameweek. The predictions are primarily based on player performances in the past gameweeks. The predictions can then be used to inform transfer strategy, i.e buy/sell certain players.<br>

## Dataset
All the data used has been taken from the fantasy premier league api
Three api urls were used
<li>Player data: 'https://fantasy.premierleague.com/api/bootstrap-static/'
<li>Fixtures: 'https://fantasy.premierleague.com/api/fixtures/'
<li>Gameweek data: 'https://fantasy.premierleague.com/api/element-summary/[player_id]/'
<br>
<br>

## Tools used

<li>Python with Numpy and Pandas
<li>Flask
<li>Heroku
