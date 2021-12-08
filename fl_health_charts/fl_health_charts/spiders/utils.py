from rich import pretty, print

pretty.install()


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


def build_urls(county_lookup: dict[str, int] = counties) -> list[str]:
    urls = []
    for county_code in county_lookup.values():
        for year in {2015, 2016, 2017, 2018, 2019, 2020, 2021}:
            url = f"http://www.flhealthcharts.com/ChartsReports/rdPage.aspx?rdReport=SubstanceUseDashboard.SubstanceUseReport&ddlCounty={county_code}&ddlYear={year}&selTab=1"
            urls.append(url)
    return urls


def extract_county_name_and_year(
    url: str, county_lookup: dict[str, int] = counties
) -> dict[str, str]:
    parts1 = url.split("&")
    parts2 = parts1[1].split("=")
    county_code = parts2[1]
    county_name = ""
    for k, v in county_lookup.items():
        if str(v) == county_code:
            county_name = k
    parts3 = parts1[2].split("=")
    year = parts3[1]
    return {"name": county_name, "year": year}


def read_urls() -> list[str]:
    with open("data/urls.txt", "r") as f:
        lines = f.readlines()
    return [u.strip() for u in lines]


if __name__ == "__main__":
    urls = read_urls()
    print(urls[:2])
    print(extract_county_name_and_year(urls[0]))
