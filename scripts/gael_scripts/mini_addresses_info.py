import pandas as pd

# read whole belgium addresses known by delivery
addresses = pd.read_csv("../static/dsv/addresses.dsv", sep='|')

# select relevant columns
adr_dice = addresses[["PDP_ID", "SUFFIX", "POSTAL_CODE", "MUNICIPALITY"]]  # we could add "STREET_NAME", "STREET_NUMBER"

# rename columns
adr_dice = adr_dice.rename(columns={"PDP_ID": "BUILDING_ID", "SUFFIX": "BOX_ID"})

# fix incorrect postal code
adr_dice.loc[adr_dice.POSTAL_CODE == 1040, "MUNICIPALITY"] = "ETTERBEEK"
adr_dice.loc[adr_dice.POSTAL_CODE == 6540, "MUNICIPALITY"] = "LOBBES"

# export new addresses data in csv
adr_dice.to_csv("../static/csv/data/addresses.csv", index=False)
