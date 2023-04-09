import pandas as pd

from datetime import datetime



dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d %h:%m:%s')

df_feb = pd.read_csv("../static/csv/data/fev-20.csv",parse_dates=['DELIVERY_DATE'],sep=',')
df_mar = pd.read_csv("../static/csv/data/mar-20.csv",parse_dates=['DELIVERY_DATE'],sep=',')
df_apr = pd.read_csv("../static/csv/data/avr-20.csv",parse_dates=['DELIVERY_DATE'],sep=',')

df = pd.concat([df_feb,df_mar,df_apr])


df_postal = df.groupby(['POSTAL_CODE','MUNICIPALITY'])['BOX_ID'].count().reset_index(name="count")
df_postal.to_csv("../static/csv/postalcounts.csv",index=False)
