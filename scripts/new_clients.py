import pandas as pd
import numpy as np

adr = pd.read_csv('../static/csv/addresses_count_per_postal_aggr.csv')
df_feb = pd.read_csv('../static/csv/data/fev-20.csv', usecols=['BUILDING_ID', 'BOX_ID'])
df_mar = pd.read_csv('../static/csv/data/mar-20.csv', parse_dates=['DELIVERY_DATE'])
df_apr = pd.read_csv('../static/csv/data/avr-20.csv', parse_dates=['DELIVERY_DATE'])
df_mai = pd.read_csv('../static/csv/data/mai-20.csv', parse_dates=['DELIVERY_DATE'])
df_jun = pd.read_csv("../static/csv/data/juin-20.csv", parse_dates=['DELIVERY_DATE'])
df_jul = pd.read_csv("../static/csv/data/juil-20.csv", parse_dates=['DELIVERY_DATE'])
df_aug = pd.read_csv("../static/csv/data/aout-20.csv", parse_dates=['DELIVERY_DATE'])
df_sep = pd.read_csv("../static/csv/data/sept-20.csv", parse_dates=['DELIVERY_DATE'])

df_conf = pd.concat([df_mar, df_apr, df_mai, df_jun, df_jul, df_aug, df_sep])

df_conf['LOCATION'] = df_conf.BUILDING_ID.map(str) + '-' + df_conf.BOX_ID.map(str)
df_conf['WEEK'] = df_conf.DELIVERY_DATE.dt.weekofyear
conf_weeks = df_conf.WEEK.unique()
conf_weeks.sort()
old_clients_list = pd.Series((df_feb.BUILDING_ID.map(str) + '-' + df_feb.BOX_ID.map(str)).unique())

# count du nombre de old et new adresses chaque semaine
num_week_new_clients = []
num_week_old_clients = []

# count du nombre de visite des old et des new chaque semaine
num_visits_week_new_clients = []
num_visits_week_old_clients = []

# cumulative sum du nombre de old et de new rencontrés au fil des semaines
cum_week_new_clients = []
cum_week_old_clients = []

# count du nombre de old et new de chaque semaine exclusif
num_week_new_ex_clients = []
num_week_old_ex_clients = []

# variables necessaires au calcul
cum_new = pd.Series([])
cum_old = pd.Series([])

for week in conf_weeks:
    week_data = df_conf[df_conf.WEEK == week]
    week_clients = week_data['LOCATION'].drop_duplicates()

    # nouveaux par rapport à février
    week_new_clients = week_clients[~week_clients.isin(old_clients_list)]
    num_week_new_clients.append(week_new_clients.size)
    # old de février
    week_old_clients = week_clients[week_clients.isin(old_clients_list)]
    num_week_old_clients.append(week_clients.size - week_new_clients.size)
    print("week:", week)
    print("new size:", week_new_clients.size)
    print("old size:", week_old_clients.size)

    # new encore jamais vus et exclusif de cette semaine
    new_new = week_new_clients[~week_new_clients.isin(cum_new)]
    num_week_new_ex_clients.append(new_new.size)
    # new encore jamais vus et exclusif de cette semaine
    old_new = week_old_clients[~week_old_clients.isin(cum_old)]
    num_week_old_ex_clients.append(old_new.size)
    print("new ex size:", new_new.size)
    print("old ex size:", old_new.size)

    if len(cum_week_new_clients) > 0:
        cum_week_new_clients.append(cum_new.size + new_new.size)
        print("cum new size:", cum_new.size + new_new.size)
    else:
        cum_week_new_clients.append(new_new.size)
        print("cum new size:", new_new.size)
    cum_new = cum_new.append(new_new)
    if len(cum_week_old_clients) > 0:
        cum_week_old_clients.append(cum_old.size + old_new.size)
        print("cum old size:", cum_old.size + old_new.size)
    else:
        cum_week_old_clients.append(old_new.size)
        print("cum old size:", old_new.size)
    cum_old = cum_old.append(old_new)

    # count du nombre de visites
    nc_visits = len((week_data[(week_data.LOCATION.isin(week_new_clients))]).index)
    num_visits_week_new_clients.append(nc_visits)
    num_visits_week_old_clients.append(len(week_data.index) - nc_visits)

conf_weeks.dump("../static/npy/conf_weeks.npy")
np.asarray(num_week_new_clients).dump("../static/npy/num_week_new_clients.npy")
np.asarray(num_week_old_clients).dump("../static/npy/num_week_old_clients.npy")
np.asarray(num_visits_week_new_clients).dump("../static/npy/num_visits_week_new_clients.npy")
np.asarray(num_visits_week_old_clients).dump("../static/npy/num_visits_week_old_clients.npy")
np.asarray(cum_week_new_clients).dump("../static/npy/cum_week_new_clients.npy")
np.asarray(cum_week_old_clients).dump("../static/npy/cum_week_old_clients.npy")
np.asarray(num_week_new_ex_clients).dump("../static/npy/num_week_new_ex_clients.npy")
np.asarray(num_week_old_ex_clients).dump("../static/npy/num_week_old_ex_clients.npy")


# For maps
df_new_agg = pd.DataFrame(columns=['POSTAL_CODE2', 'MUNICIPALITY2', 'WEEK', 'N_NEW', 'NORM_NEW',
                                   'NEW_VISITS', 'NORM_VISITS', 'PERCENT_NEW', 'PERCENT_NEW_VISITS',
                                  'PERCENT_NORM_NEW', 'PERCENT_NORM_VISITS'])
for week in conf_weeks:
    week_data = (df_conf[df_conf.WEEK == week]).copy()
    week_data["POSTAL_CODE2"] = week_data.POSTAL_CODE // 100
    week_clients = pd.Series(week_data['LOCATION'].unique())
    new_clients = week_clients[~week_clients.isin(old_clients_list)]
    new_clients = pd.merge(new_clients.rename("LOCATION"),
                           week_data[["LOCATION", "POSTAL_CODE2", "CLASS"]], on="LOCATION")
    new_clients = new_clients.groupby("POSTAL_CODE2").agg(
        {"LOCATION": 'nunique', "CLASS": "count"}).reset_index().rename(
        columns={"LOCATION": "N_NEW", "CLASS": "NEW_VISITS"})
    new_clients = pd.merge(new_clients, adr, on="POSTAL_CODE2")
    new_clients["NORM_NEW"] = new_clients["N_NEW"] / new_clients["N_ADDRESSES"]
    new_clients["NORM_VISITS"] = new_clients["NEW_VISITS"] / new_clients["N_ADDRESSES"]
    new_clients["PERCENT_NEW"] = 100 * new_clients.N_NEW / new_clients.N_NEW.sum()
    new_clients["PERCENT_NEW_VISITS"] = 100 * new_clients.NEW_VISITS / new_clients.NEW_VISITS.sum()
    new_clients["PERCENT_NORM_NEW"] = 100 * new_clients.NORM_NEW / new_clients.NORM_NEW.sum()
    new_clients["PERCENT_NORM_VISITS"] = 100 * new_clients.NORM_VISITS / new_clients.NORM_VISITS.sum()
    new_clients["WEEK"] = week
    df_new_agg = df_new_agg.append(new_clients[["POSTAL_CODE2", "MUNICIPALITY2", "WEEK", "N_NEW", "NORM_NEW",
                                                "NEW_VISITS", "NORM_VISITS", "PERCENT_NEW", "PERCENT_NEW_VISITS",
                                               "PERCENT_NORM_NEW", "PERCENT_NORM_VISITS"]])
df_new_agg.to_csv("../static/csv/new_clients_weeks_postal_aggr.csv", index=False)
