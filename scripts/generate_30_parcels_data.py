import pandas as pd

df_feb = pd.read_csv("../static/csv/data/fev-20.csv", parse_dates=['DELIVERY_DATE'])
df_feb['LOCATION'] = df_feb.BUILDING_ID.map(str) + '-' + df_feb.BOX_ID.map(str)
feb_particulars = (df_feb.BUILDING_ID.map(str) + '-' + df_feb.BOX_ID.map(str))
feb_particulars = feb_particulars.groupby(feb_particulars).count()
feb_particulars = feb_particulars[feb_particulars <= 30]
df_feb = df_feb[df_feb.LOCATION.isin(feb_particulars.index.tolist())]
df_feb.to_csv("../static/csv/data/30_parcels_feb.csv", index=False)
print("feb")

df_mar = pd.read_csv("../static/csv/data/mar-20.csv", parse_dates=['DELIVERY_DATE'])
df_mar['LOCATION'] = df_mar.BUILDING_ID.map(str) + '-' + df_mar.BOX_ID.map(str)
mar_particulars = (df_mar.BUILDING_ID.map(str) + '-' + df_mar.BOX_ID.map(str))
mar_particulars = mar_particulars.groupby(mar_particulars).count()
mar_particulars = mar_particulars[mar_particulars <= 30]
df_mar = df_mar[df_mar.LOCATION.isin(mar_particulars.index.tolist())]
df_mar.to_csv("../static/csv/data/30_parcels_mar.csv", index=False)
print("mar")

df_apr = pd.read_csv("../static/csv/data/avr-20.csv", parse_dates=['DELIVERY_DATE'])
df_apr['LOCATION'] = df_apr.BUILDING_ID.map(str) + '-' + df_apr.BOX_ID.map(str)
apr_particulars = (df_apr.BUILDING_ID.map(str) + '-' + df_apr.BOX_ID.map(str))
apr_particulars = apr_particulars.groupby(apr_particulars).count()
apr_particulars = apr_particulars[apr_particulars <= 30]
df_apr = df_apr[df_apr.LOCATION.isin(apr_particulars.index.tolist())]
df_apr.to_csv("../static/csv/data/30_parcels_apr.csv", index=False)
print("apr")

df_may = pd.read_csv("../static/csv/data/mai-20.csv", parse_dates=['DELIVERY_DATE'])
df_may['LOCATION'] = df_may.BUILDING_ID.map(str) + '-' + df_may.BOX_ID.map(str)
may_particulars = (df_may.BUILDING_ID.map(str) + '-' + df_may.BOX_ID.map(str))
may_particulars = may_particulars.groupby(may_particulars).count()
may_particulars = may_particulars[may_particulars <= 30]
df_may = df_may[df_may.LOCATION.isin(may_particulars.index.tolist())]
df_may.to_csv("../static/csv/data/30_parcels_may.csv", index=False)
print("mai")

df_jun = pd.read_csv("../static/csv/data/juin-20.csv", parse_dates=['DELIVERY_DATE'])
df_jun['LOCATION'] = df_jun.BUILDING_ID.map(str) + '-' + df_jun.BOX_ID.map(str)
jun_particulars = (df_jun.BUILDING_ID.map(str) + '-' + df_jun.BOX_ID.map(str))
jun_particulars = jun_particulars.groupby(jun_particulars).count()
jun_particulars = jun_particulars[jun_particulars <= 30]
df_jun = df_jun[df_jun.LOCATION.isin(jun_particulars.index.tolist())]
df_jun.to_csv("../static/csv/data/30_parcels_jun.csv", index=False)
print("june")

df_jul = pd.read_csv("../static/csv/data/juil-20.csv", parse_dates=['DELIVERY_DATE'])
df_jul['LOCATION'] = df_jul.BUILDING_ID.map(str) + '-' + df_jul.BOX_ID.map(str)
jul_particulars = (df_jul.BUILDING_ID.map(str) + '-' + df_jul.BOX_ID.map(str))
jul_particulars = jul_particulars.groupby(jul_particulars).count()
jul_particulars = jul_particulars[jul_particulars <= 30]
df_jul = df_jul[df_jul.LOCATION.isin(jul_particulars.index.tolist())]
df_jul.to_csv("../static/csv/data/30_parcels_jul.csv", index=False)
print("july")

df_aug = pd.read_csv("../static/csv/data/aout-20.csv", parse_dates=['DELIVERY_DATE'])
df_aug['LOCATION'] = df_aug.BUILDING_ID.map(str) + '-' + df_aug.BOX_ID.map(str)
aug_particulars = (df_aug.BUILDING_ID.map(str) + '-' + df_aug.BOX_ID.map(str))
aug_particulars = aug_particulars.groupby(aug_particulars).count()
aug_particulars = aug_particulars[aug_particulars <= 30]
df_aug = df_aug[df_aug.LOCATION.isin(aug_particulars.index.tolist())]
df_aug.to_csv("../static/csv/data/30_parcels_aug.csv", index=False)
print("august")

df_sep = pd.read_csv("../static/csv/data/sept-20.csv", parse_dates=['DELIVERY_DATE'])
df_sep['LOCATION'] = df_sep.BUILDING_ID.map(str) + '-' + df_sep.BOX_ID.map(str)
sep_particulars = (df_sep.BUILDING_ID.map(str) + '-' + df_sep.BOX_ID.map(str))
sep_particulars = sep_particulars.groupby(sep_particulars).count()
sep_particulars = sep_particulars[sep_particulars <= 30]
df_sep = df_sep[df_sep.LOCATION.isin(sep_particulars.index.tolist())]
df_sep.to_csv("../static/csv/data/30_parcels_sep.csv", index=False)
print("september")
