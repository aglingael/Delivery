import pandas as pd
import math

adr = pd.read_csv("../static/csv/data/addresses.csv")

adr["LOCATION"] = adr.BUILDING_ID.map(str) + "-" + adr.BOX_ID.map(str)
adr.drop(["BUILDING_ID", "BOX_ID"], axis=1, inplace=True)

df_addr = adr.groupby(['POSTAL_CODE','MUNICIPALITY']).agg({'LOCATION': pd.Series.nunique}).rename(columns={"LOCATION": "N_ADDRESSES"})
df_addr.to_csv("../static/csv/addresses_count_per_postal.csv")


df_addr.reset_index(inplace=True)

df_addr['POSTAL_CODE2'] = df_addr.apply(lambda x: math.floor(int(x['POSTAL_CODE'])/100), axis=1)

def find_base_municipality(x):
    pc = x.POSTAL_CODE2*100
    y = df_addr.loc[df_addr.POSTAL_CODE == pc]
    while len(y) == 0:
        pc += 10
        y = df_addr.loc[df_addr.POSTAL_CODE == pc]
    return y.iloc[0].MUNICIPALITY

df_addr['MUNICIPALITY2'] = df_addr.apply(find_base_municipality, axis=1)

df_addr = df_addr.groupby([df_addr.POSTAL_CODE2,df_addr.MUNICIPALITY2]).agg({'N_ADDRESSES': ['sum']}).reset_index()
df_addr.columns = df_addr.columns.get_level_values(0)
df_addr.to_csv("../static/csv/addresses_count_per_postal_aggr.csv",index=False)
