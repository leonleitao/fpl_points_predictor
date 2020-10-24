import numpy as np
import pandas as pd

def get_average_stats(df,cols,n=None):
    if n:
        colnames=['av({})_{}'.format(n,col) for col in cols]
        df[colnames]=df[cols].shift(1).rolling(n).mean().fillna(0)
        return df
    colnames=['av_{}'.format(col) for col in cols]
    df[colnames]=df[cols].shift(1).expanding().mean().fillna(0)
    return df