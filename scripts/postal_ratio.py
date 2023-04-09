import pandas as pd
from datetime import datetime
import numpy as np

df_feb = pd.read_csv("../static/csv/postal_count/fev.csv")
df_mar = pd.read_csv("../static/csv/postal_count/mar.csv")
df_apr = pd.read_csv("../static/csv/postal_count/avr.csv")

df_feb = df_feb.rename(columns={"COUNT": "COUNT_FEB"})
df_mar = df_mar.rename(columns={"COUNT": "COUNT_MAR"})
df_apr = df_apr.rename(columns={"COUNT": "COUNT_APR"})

df_ratio = pd.merge(df_feb, df_apr, how='outer')

#### DIVIDE BY # BUSINESS DAYS ####

df = pd.read_csv("../static/csv/dailycounts.csv",parse_dates=['DELIVERY_DATE'],sep=',')
df = df.groupby(['DELIVERY_DATE'])['TOT_VISITS'].sum().reset_index()
df['BUSINESS_DAY'] = df['TOT_VISITS'].apply(lambda c: 1 if c > 100000 else 0)
df = df.groupby(df['DELIVERY_DATE'].dt.to_period("M"))['BUSINESS_DAY'].sum().reset_index()

df_ratio["COUNT_FEB"] = df_ratio["COUNT_FEB"] / df['BUSINESS_DAY'][0]
df_ratio["COUNT_APR"] = df_ratio["COUNT_APR"] / df['BUSINESS_DAY'][2]

###################################

df_ratio["COUNT_APR"] = df_ratio["COUNT_APR"] / df_ratio["COUNT_FEB"]
df_ratio = df_ratio.rename(columns={"COUNT_APR": "RATIO"}).drop(["COUNT_FEB"], axis=1)
df_ratio.to_csv("../static/csv/postalratio_avr_fev.csv",index=False)

df_feb = pd.read_csv("../static/csv/postal_count_aggr/fev.csv")
df_mar = pd.read_csv("../static/csv/postal_count_aggr/mar.csv")
df_apr = pd.read_csv("../static/csv/postal_count_aggr/avr.csv")

df_feb = df_feb.rename(columns={"COUNT": "COUNT_FEB"})
df_mar = df_mar.rename(columns={"COUNT": "COUNT_MAR"})
df_apr = df_apr.rename(columns={"COUNT": "COUNT_APR"})

df_ratio = pd.merge(df_feb, df_apr, how='outer')

#### SAME FOR AGGREGATED VIEW ####

df_ratio["COUNT_FEB"] = df_ratio["COUNT_FEB"] / df['BUSINESS_DAY'][0]
df_ratio["COUNT_APR"] = df_ratio["COUNT_APR"] / df['BUSINESS_DAY'][2]

##################################

df_ratio["COUNT_APR"] = df_ratio["COUNT_APR"] / df_ratio["COUNT_FEB"]
df_ratio = df_ratio.rename(columns={"COUNT_APR": "RATIO"}).drop(["COUNT_FEB"], axis=1)
df_ratio.to_csv("../static/csv/postalratio_aggr_avr_fev.csv",index=False)
