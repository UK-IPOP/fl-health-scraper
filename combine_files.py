# %%
from pathlib import Path
import json
import pandas as pd

# %% [markdown]
# ## Loading Step

# %%
jsonlines_paths = [x for x in Path("./fl_health_charts/data").glob("*.jsonl")]
data: list[dict[str, str]] = []
for file_path in jsonlines_paths:
    county, year = file_path.name.strip(".jsonl").split("_")
    with open(file_path, "r") as f:
        for line in f:
            line_data = json.loads(line)
            line_data["County"] = county
            line_data["YearScraped"] = year
            data.append(line_data)

data[0]

# %% [markdown]
# ## Cleaning Step

# %%
# %%
df = pd.DataFrame.from_records(data)
# df.drop_duplicates(inplace=True)
# df.dropna(thresh=7, inplace=True)
# df.reset_index(drop=True, inplace=True)
print(df.shape)
df.head()

# %% [markdown]
# ## Joining Step
#
# ... joins in the URL field

# %%
counties = {
    "Florida": 69,
    "Alachua": 1,
    "Baker": 2,
    "Bay": 3,
    "Bradford": 4,
    "Brevard": 5,
    "Broward": 6,
    "Calhoun": 7,
    "Charlotte": 8,
    "Citrus": 9,
    "Clay": 10,
    "Collier": 11,
    "Columbia": 12,
    "Miami-Dade": 13,
    "DeSoto": 14,
    "Dixie": 15,
    "Duval": 16,
    "Escambia": 17,
    "Flagler": 18,
    "Fanklin": 19,
    "Gadsden": 20,
    "Gilchrist": 21,
    "Glades": 22,
    "Gulf": 23,
    "Hamilton": 24,
    "Hardee": 25,
    "Hendry": 26,
    "Hernando": 27,
    "Highlands": 28,
    "Hillsborough": 29,
    "Holmes": 30,
    "India River": 31,
    "Jackson": 32,
    "Jefferson": 33,
    "Lafayette": 34,
    "Lake": 35,
    "Lee": 36,
    "Leon": 37,
    "Levy": 38,
    "Liberty": 39,
    "Madison": 40,
    "Manatee": 41,
    "Marion": 42,
    "Martin": 43,
    "Monroe": 44,
    "Nassau": 45,
    "Okaloosa": 46,
    "Okeechobee": 47,
    "Orange": 48,
    "Osceola": 49,
    "Palm Beach": 50,
    "Pasco": 51,
    "Pinellas": 52,
    "Polk": 53,
    "Putnam": 54,
    "St. Johns": 55,
    "St. Lucie": 56,
    "Santa Rosa": 57,
    "Sarasota": 58,
    "Seminole": 59,
    "Sumter": 60,
    "Suwannee": 61,
    "Taylor": 62,
    "Union": 63,
    "Volusia": 64,
    "Wakulla": 65,
    "Walton": 66,
    "Washington": 67,
}


# %%
url_lookups = dict()
for c in counties.keys():
    for y in {2015, 2016, 2017, 2018, 2019, 2020, 2021}:
        url_lookups[
            f"{c}_{y}"
        ] = f"http://www.flhealthcharts.com/ChartsReports/rdPage.aspx?rdReport=SubstanceUseDashboard.SubstanceUseReport&ddlCounty={counties[c]}&ddlYear={y}&selTab=1"


def make_url(county, year):
    if pd.isna(county) or pd.isna(year):
        return None
    return url_lookups[f"{county}_{int(year)}"]


df["URL"] = df.apply(lambda row: make_url(row["County"], row["YearScraped"]), axis=1)
df.head()

# %% [markdown]
# ## Write step

# %%
df.to_csv("./data/results.csv", index=False)

# %%
