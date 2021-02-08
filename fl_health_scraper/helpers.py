from typing import Union
from bs4 import BeautifulSoup
import requests
import pandas as pd

import re
import pprint
import os


"""Base url for requests."""
URL = "http://www.flhealthcharts.com/ChartsReports/rdPage.aspx?rdReport=ChartsProfiles.OpioidUseDashboard"

"""Years to query for."""
YEARS = [2015, 2016, 2017, 2018, 2019, 2020]

"""A dict of county names and their form values."""
COUNTIES = {
    # "Florida": 69,  # ommited because is aggregated on site
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


def visit_site(url: str, county_id: int, year: int) -> bytes:
    """Visit a specified site using post-request and return response content.

    Args:
        url: base url to visit
        county_id: numeric id of county to query from form data
        year: year to query in form data

    Returns:
        bytes: response content
    """
    response = requests.post(url, data={"islCounty": county_id, "islYears": year})
    return response.content


def scrape_site(content: bytes) -> dict[str, list[str]]:
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find(id="dtOpioidProfile")

    data: dict[str, list[str]] = {
        "Indicator": [],
        "Measure": [],
        "Year": [],
        "Jan-Mar": [],
        "Apr-June": [],
        "July-Sep": [],
        "Oct-Dec": [],
        "Year-to-Date": [],
        "Case Definition": [],
    }

    # get table data directly using regex compiled 'id' attribute
    # must do for each title
    regex_columns: list[str] = [
        "colIndTitle_Row",
        "colMeasure_Row",
        "colYear_Row",
        "colQuarter1_Row",
        "colQuarter2_Row",
        "colQuarter3_Row",
        "colQuarter4_Row",
        "colAnnual_Row",
        "colCaseDefinition_Row",
    ]

    # here we add '_Row' to the cols to make sure we are only accessing the ones inside the table rows
    # and not in the header

    # these loops can be improved (readability, refactored into funcs etc.)
    for field, col in zip(data.keys(), regex_columns):
        data[field] = [r.text.strip() for r in table.find_all(id=re.compile(f"{col}"))]

    return data


def format_data(data: dict[str, list[str]], year: int, county: str) -> pd.DataFrame:
    df = pd.DataFrame.from_dict(data)
    df["Year"] = year
    df["County"] = county
    return df


def export_data(df: pd.DataFrame, year: int, county_name: str) -> None:
    if not os.path.exists(f"data/{year}"):
        os.mkdir(f"data/{year}")
    df.to_csv(f"data/{year}/{county_name}.csv", index=False)


def generate_file_names() -> list[str]:
    file_names = []
    for year in YEARS:
        for name, id in COUNTIES.items():
            file_names.append(f"data/{year}/{name}.csv")
    return file_names


def combine_files():
    return pd.concat((pd.read_csv(f) for f in generate_file_names()))


def export_single_file():
    df = combine_files()
    df.to_csv("data/composite.csv", index=False)