import pandas as pd 
import numpy as np 
import lightgbm as lgb

data=pd.read_csv("data/data.csv")
for col in ['first_name', 'second_name', 'position','id_x','team','is_home', 'opposition_team',]:
    data[col] = data[col].astype('category')
teams=data.sort_values('team')['team'].unique()
data['first_name']=data['first_name'].apply(lambda x: x.split(" ")[0])
data['second_name']=data['second_name'].apply(lambda x: x.split(" ")[-1])

current_gw=max(set(data['event']))
past_df=data[data['event']<current_gw]
current_df=data[data['event']==current_gw]

train=past_df
test=current_df
X_train=train.drop(['event','total_points','first_name','second_name','code','av_value','av(2)_value'],axis=1)
y_train=train['total_points']
X_test=test.drop(['event','total_points','first_name','second_name','code','av_value','av(2)_value'],axis=1)
y_test=test['total_points']

reg=lgb.LGBMRegressor(n_estimators=50)
reg.fit(X_train,y_train)
preds=reg.predict(X_test)

predictions=test.copy()[['event','first_name', 'second_name', 'team', 'position','opposition_team','code']]
predictions['predicted_points']=np.round(preds).astype(int)
# Players with highest predicted points
predictions=predictions.sort_values('predicted_points',ascending=False)
predictions.to_csv('data/predictions.csv',index=False)
