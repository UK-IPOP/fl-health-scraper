"""This module is the core functionality of the scraper."""

import os
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

from .constants import COUNTIES, URL, YEARS


def visit_site(url: str, county_id: int, year: int) -> requests.Response:
    """Visit a specified site using post-request and return response content.

    Args:
        url: base url to visit
        county_id: numeric id of county to query from form data
        year: year to query in form data

    Returns:
        bytes: response content

    """
    response = requests.post(url, data={"islCounty": county_id, "islYears": year})
    return response


def scrape_site(web_response: requests.Response) -> dict[str, list[str]]:
    """Scrapes webpage content from web response context.

    Args:
        content: website content from response object

    Returns:
        dict[str, list[str]]: dictionary of column names and data scraped from the web-table

    """
    content = web_response.content
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

    # these loops can be improved (readability, refactored into funcs etc.)
    for field, col in zip(data.keys(), regex_columns):
        data.update(
            {field: [r.text.strip() for r in table.find_all(id=re.compile(f"{col}"))]}
        )
    return data


def export_data(
    data: dict[str, list[str]],
    county_name: str,
    year: int,
) -> pd.DataFrame:
    """Exports data to a file.

    Args:
        data: data scraped from website
        year: year of dataset
        county_name: county name of dataset

    """
    df = pd.DataFrame.from_dict(data)
    df["Year"] = year
    df["County"] = county_name
    directory = os.path.join("data", str(year))
    if not os.path.exists(directory):
        os.mkdir(directory)
    df.to_csv(os.path.join(directory, f"{county_name}.csv"), index=False)
    return df


def generate_file_names() -> list[str]:
    """Generates filenames for export using YEARS and COUNTIES globals.

    Returns:
        list[str]: list of filepaths/filenames.

    """
    file_names = []
    for year in YEARS:
        for name, _ in COUNTIES.items():
            file_names.append(os.path.join("data", str(year), f"{name}.csv"))
    return file_names


def remove_files() -> bool:
    """Removes files and dirs created during scraping process."""
    year_dirs = [os.path.join("data", str(y)) for y in YEARS]
    years_dirs_exist = all(os.path.exists(d) for d in year_dirs)
    if not os.path.exists("data") or not years_dirs_exist:
        return False
    else:
        filenames = generate_file_names()
        for f in filenames:
            if os.path.exists(f):
                os.remove(f)
        if years_dirs_exist:
            for d in year_dirs:
                os.rmdir(d)
        return True


def combine_files() -> pd.DataFrame:
    """Combines all of the individual files into one composite file."""
    large_df = pd.concat((pd.read_csv(f) for f in generate_file_names()))
    new_col_order = [
        "Year",
        "County",
        "Indicator",
        "Measure",
        "Jan-Mar",
        "Apr-June",
        "July-Sep",
        "Oct-Dec",
        "Year-to-Date",
        "Case Definition",
    ]
    reordered_df = large_df[new_col_order]
    reordered_df.to_csv(os.path.join("data", "composite.csv"), index=False)
    return reordered_df


def gather_data() -> pd.DataFrame:
    """Runs entire pipeline of visiting site, scraping data, and exporting data."""
    for i, year in enumerate(YEARS):
        print(f"Getting data for {year} -- {i + 1}/{len(YEARS)}")
        for name, id in COUNTIES.items():
            site_content = visit_site(URL, id, year)
            site_data = scrape_site(site_content)
            export_data(data=site_data, year=year, county_name=name)
    df = combine_files()
    remove_files()
    return df