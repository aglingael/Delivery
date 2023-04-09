import pandas as pd
import numpy as np

df_feb = pd.read_csv('../static/csv/data/fev-20.csv', parse_dates=['DELIVERY_DATE'])
df_apr = pd.read_csv('../static/csv/data/avr-20.csv', parse_dates=['DELIVERY_DATE'])
df_feb['LOCATION'] = df_feb.BUILDING_ID.map(str) + '-' + df_feb.BOX_ID.map(str)
df_apr['LOCATION'] = df_apr.BUILDING_ID.map(str) + '-' + df_apr.BOX_ID.map(str)
feb_num_per_adr = df_feb.groupby('LOCATION')['CLASS'].count().reset_index(drop=True)
apr_num_per_adr = df_apr.groupby('LOCATION')['CLASS'].count().reset_index(drop=True)

# Number of addresses per group
counts_feb, bins_feb = np.histogram(feb_num_per_adr, bins=range(1, 302, 5))
bins_feb = (bins_feb[:-1] + bins_feb[1:]-1) / 2
counts_apr, bins_apr = np.histogram(apr_num_per_adr, bins=range(1, 302, 5))
bins_apr = (bins_apr[:-1] + bins_apr[1:]-1) / 2
counts_feb.dump("../static/npy/counts_feb.npy")
bins_feb.dump("../static/npy/bins_feb.npy")
counts_apr.dump("../static/npy/counts_apr.npy")
bins_apr.dump("../static/npy/bins_apr.npy")


# Number of visits per group
a, b = np.histogram(feb_num_per_adr, bins=range(1, 302, 1))
c, d = np.histogram(apr_num_per_adr, bins=range(1, 302, 1))
feb_tok = a * b[:-1]
apr_tok = c * d[:-1]
feb_bins_count_parcels = []
apr_bins_count_parcels = []
for i in range(0, 300, 5):
    feb_bins_count_parcels.append(feb_tok[i:i+5].sum())
    apr_bins_count_parcels.append(apr_tok[i:i+5].sum())

feb_bins_count_parcels = np.asarray(feb_bins_count_parcels)
feb_bins_ratio = feb_bins_count_parcels / feb_num_per_adr.sum() * 100  # percent of feb groups parcels over feb parcels
apr_bins_count_parcels = np.asarray(apr_bins_count_parcels)
apr_bins_ratio = apr_bins_count_parcels / apr_num_per_adr.sum() * 100  # percent of apr groups parcels over apr parcels
# ratio_parcels_apr_feb = apr_bins_count_parcels / feb_bins_count_parcels

feb_bins_count_parcels.dump("../static/npy/feb_bins_count_parcels.npy")
feb_bins_ratio.dump("../static/npy/feb_bins_ratio.npy")
apr_bins_count_parcels.dump("../static/npy/apr_bins_count_parcels.npy")
apr_bins_ratio.dump("../static/npy/apr_bins_ratio.npy")
# ratio_parcels_apr_feb.dump("../static/npy/ratio_parcels_apr_feb.npy")
