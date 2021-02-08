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
    "Alachua": 1,
    "Baker": 2,
    "Bay": 3,
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


def format_data(data: dict[str, list[str]]) -> pd.DataFrame:
    return pd.DataFrame.from_dict(data)


def export_data(df: pd.DataFrame, year: int, county_name: str) -> None:
    if not os.path.exists(f"data/{year}"):
        os.mkdir(f"data/{year}")
    df.to_csv(f"data/{year}/{county_name}.csv", index=False)
