#!/usr/bin/env python3
import pandas as pd
import numpy as np
from datetime import datetime
import datetime
import sys
import csv
import statsmodels.api as sm

with open(sys.argv[1],'r') as my_file:
     df = pd.read_csv(my_file,sep=',',header=0)
     df['ts'] = pd.to_datetime(df['ts'], errors='coerce')
     df.ts = pd.to_datetime(df.ts)
     df['day_of_week'] =df['ts'].dt.weekday_name
     df['date'] = df.ts.dt.floor('d')
     df['Busi_days'] = df['ts'].dt.dayofweek < 5
     df['Busi_hours'] = df['ts'].dt.time.between(datetime.time(9), datetime.time(18))
     df['date'] = df.ts.dt.floor('d')
     
## Defining function for the features     
def Features(df):
    df.ts = pd.to_datetime(df.ts)

    df['date'] = df.ts.dt.floor('d')

    u = df.uuid.unique()
    a = df.groupby(['uuid', 'date']).size().reset_index(level=1, drop=True)
    a = a[a>5]
    target_df = (a[~a.index.duplicated()]
                    .astype(bool).reindex(u, fill_value=False).to_frame(name='Highly_Active'))

    a = df.groupby('uuid')['ts'].nunique()
    target_df['Multiple_days'] = a[a>5].astype(bool).reindex(u, fill_value=False)

    a = df.loc[(df.Busi_days==True)&(df.Busi_hours==True)].uuid.unique()
    target_df['Busi_weekday'] = target_df.index.isin(a)
    target_df.reset_index(inplace=True)	
    return target_df   

New=Features(df)
#print(New.head())

# Fourth Feature using Logistic Regression based on Highly active users
Counts       = df.groupby(by='uuid')['ts'].apply(lambda x: x.nunique())
Counts       = pd.DataFrame(Counts).reset_index()
Counts_annon = pd.merge(df,Counts,on='uuid')
#print(Counts.head())
Counts_annon=Counts_annon.sort_values(by='ts_x')
Count_ann_new=pd.merge(New,Counts_annon[["ts_y","uuid"]],on='uuid')

# The column with counts based on grouped by on the Timeseries for each users ts_y
# fit the model
logit       = sm.Logit(Count_ann_new['Highly_Active'], Count_ann_new['ts_y'])
result      = logit.fit(disp=False)
Count_ann_new['My_feature'] = result.predict()
Count_ann_new['My_feature'] = result.predict()
Count_ann_new.reset_index(inplace=True)
## Print the output to the log file
print(Count_ann_new[["uuid","Highly_Active","Multiple_days","Busi_weekday","My_feature"]])


