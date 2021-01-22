import pandas as pd

def convert_to_categorical(df,cols) -> pd.DataFrame:
    """Converts the given list of columns to categorical type"""
    for col in cols:
        df[col] = df[col].astype('category')
    return df

def shorten_names(df) -> pd.DataFrame:
    """Shortens names of players to display on the web application"""
    df['first_name']=df['first_name'].apply(lambda x: x.split(" ")[0])
    df['second_name']=df['second_name'].apply(lambda x: x.split(" ")[-1])
    return df