# %%
import time
import requests

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

years = ["2015", "2016", "2017", "2018", "2019", "2020"]
# %%
for county_name, county_val in counties.items():
    for year in years:
        payload = {"islCounty": county_val, "islYears": year}
        res = requests.post(
            "https://www.flhealthcharts.gov/ChartsDashboards/rdPage.aspx?rdReport=SubstanceUse.Overdose",
            data=payload,
        )
        if res.status_code != 200:
            print(f"Error: {res.status_code}")
            continue
        with open(f"data/scraped/{county_name}_{year}.html", "w") as f:
            f.write(res.text)

        if county_val % 10 == 0:
            time.sleep(10)

# %%
