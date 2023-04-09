import pandas as pd
import numpy as np
import sys

# parser for datetime columns
# dateparse = lambda x: pd.datetime.strptime(x, "%d/%m/%y %H:%M:%S,%f")

# Read whole belgium addresses known by delivery
adr = pd.read_csv("../static/csv/data/addresses.csv")

# get id of houses
houses = adr[adr.BOX_ID == 0]["BUILDING_ID"].tolist()

# Read the month delivery data
month_whole = pd.read_csv("../static/dsv/" + sys.argv[1] + ".dsv", sep='|')  # nrow is added for test

# Preprocess data
month = month_whole[['ADDRESSEE_PDP_ID', 'ADDRESSEE_PDP_SUFFIX', 'EVT_CREATETIME', 'HANDLING_INSTRUCTIONS',
                     'WEIGHT_IN_GRAMS_MEASURED', 'HEIGHT_IN_MM', 'LENGTH_IN_MM', 'WIDTH_IN_MM', 'ITM_CREATED_ON',
                     'EVENT_SUB_CODE', 'ITEM_CODE']]

# select parcels from month delivery data
month = month[month.HANDLING_INSTRUCTIONS.str.contains("PARCEL", na=False)]
parcel_size_before = len(month.index)
print("number of parcels in the month:", parcel_size_before)

if len(sys.argv) > 2:
    out_file = open("../static/csv/data/stats.csv", "a+")

# remove the no more useful column
del month['HANDLING_INSTRUCTIONS']

# rename columns
month = month.rename(columns={"ITM_CREATED_ON": "FIRST_CONTACT_DATE",
                              "ITEM_CODE": "PARCEL_CODE",
                              "EVT_CREATETIME": "DELIVERY_DATE",
                              "EVENT_SUB_CODE": "DELIVERY_STATUS_CODE",
                              "ADDRESSEE_PDP_ID": "BUILDING_ID",
                              "ADDRESSEE_PDP_SUFFIX": "BOX_ID",
                              "WEIGHT_IN_GRAMS_MEASURED": "WEIGHT",
                              "HEIGHT_IN_MM": "HEIGHT",
                              "LENGTH_IN_MM": "LENGTH",
                              "WIDTH_IN_MM": "WIDTH"})

# convert date string columns to datetime objects
month.FIRST_CONTACT_DATE = pd.to_datetime(month.FIRST_CONTACT_DATE, format="%d/%m/%y %H:%M:%S,%f")
# month.DELIVERY_DATE = pd.to_datetime(month.DELIVERY_DATE, format="%d/%m/%y %H:%M:%S,%f")
month.DELIVERY_DATE = pd.to_datetime(month.DELIVERY_DATE, format="%Y-%m-%d %H:%M:%S.%f")

# get not bussable parcels i.e parcels which cannot fit in the mailbox and require presence
# this is calculated based on the weight, length, width and height of the parcels
month = month[(month.WEIGHT > 2000) | (month.HEIGHT > 30) | (month.LENGTH > 350) | (month.WIDTH > 230)]
# we miss some parcels for which we do not have measures but which could be not bussable
# the column 'FITS_IN_MAILBOX_ACTUAL' is the decision of the mailman when he saw the parcel but
# unfortunately this information is not trustable since the mailmen put false information to make
# the round by car :-(

# remove the no more useful columns
del month['WEIGHT']
del month['HEIGHT']
del month['LENGTH']
del month['WIDTH']

# remove non coherent parcels
# the delivery date cannot be before the first contact date
month.drop(month[month.DELIVERY_DATE < month.FIRST_CONTACT_DATE].index)

# remove the no more useful column
del month['FIRST_CONTACT_DATE']

pos_delivery_status_code = [1, 7, 8, 28, 31, 32, 33]  # delivered status codes
neg_delivery_status_code = [3, 22]  # not delivered status codes

# set the delivery status based on the delivery status code
month['CLASS'] = np.nan
month.loc[month.DELIVERY_STATUS_CODE.isin(pos_delivery_status_code), "CLASS"] = 1
month.loc[month.DELIVERY_STATUS_CODE.isin(neg_delivery_status_code), "CLASS"] = 0
# particular case
month.loc[(month.DELIVERY_STATUS_CODE == 13) & ((month.DELIVERY_DATE.dt.weekday == 5)  # saturday
                                                | (month.PARCEL_CODE.str.endswith("112"))
                                                | (month.PARCEL_CODE.str.endswith("126"))),
          "CLASS"] = 1

# remove the no more useful columns
del month['DELIVERY_STATUS_CODE']
del month['PARCEL_CODE']

# remove the rows for which we could not set a delivery status
month.drop(month[month.CLASS.isna()].index, inplace=True)

# add box-id for houses since it is equal to 0
month.loc[(month.BUILDING_ID.isin(houses)) & (month.BOX_ID.isna()), "BOX_ID"] = 0

# remove rows without building or box information
month.drop(month[(month.BUILDING_ID.isna()) | (month.BOX_ID.isna())].index, inplace=True)

# cast columns to int after removing NA values
month.CLASS = month.CLASS.astype(int)
month.BUILDING_ID = month.BUILDING_ID.astype(int)
month.BOX_ID = month.BOX_ID.astype(int)

# get information about postal code and municipality. It removes btw rows for which we do not have those information
month = pd.merge(month, adr, on=["BUILDING_ID", "BOX_ID"], sort=False)

parcel_size_after = len(month.index)
print("number of parcels remained for study:", parcel_size_after)

if len(sys.argv) > 2:
    out_file.write(",".join([sys.argv[1], str(parcel_size_before), str(parcel_size_after)]) + "\n")
    out_file.flush()
    out_file.close()

# export the final dataset of the month
month.to_csv("../static/csv/data/" + sys.argv[1] + ".csv", index=False)
