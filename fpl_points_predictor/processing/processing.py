import pandas as pd

def convert_to_categorical(df,cols):
    for col in cols:
        df[col] = df[col].astype('category')
    return df

def shorten_names(df):
    df['first_name']=df['first_name'].apply(lambda x: x.split(" ")[0])
    df['second_name']=df['second_name'].apply(lambda x: x.split(" ")[-1])
    return df