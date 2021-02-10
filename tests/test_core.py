import time
from collections import namedtuple
from random import choice

import pandas as pd

import fl_health_scraper.core as scraper
from fl_health_scraper.constants import COUNTIES, URL, YEARS

Choices = namedtuple("Choice", ["county", "year"])


def randomly_choose():
    return Choices(choice(list(COUNTIES.values())), choice(YEARS))


def test_visit_random_site():
    """Test accessing website and response code.

    Uses random choices from the COUNTIES and YEARS globals so note when failures occur where they happen.
    """
    r = randomly_choose()
    assert scraper.visit_site(URL, r.county, r.year).status_code == 200


def test_visit_all_sites():
    """Test accessing website and response code.

    Runs against all COUNTIES and YEARS.
    Useful for seeing if a page goes down.
    """
    for year in YEARS:
        for county in COUNTIES.values():
            res = scraper.visit_site(URL, county, year)
            assert res.status_code == 200
            time.sleep(3)  # delay so no timeout


def test_scrape_site():
    """Relies on functioning visit_site() to test scraping ability."""
    r = randomly_choose()
    response = scraper.visit_site(URL, r.county, r.year)
    scraped = scraper.scrape_site(response)
    column_names: list[str] = [
        "Indicator",
        "Measure",
        "Year",
        "Jan-Mar",
        "Apr-June",
        "July-Sep",
        "Oct-Dec",
        "Year-to-Date",
        "Case Definition",
    ]
    assert type(scraped) == dict
    assert list(scraped.keys()) == column_names
    assert type(list(scraped.values())[0]) == list


def test_export_data():
    """Tests export functionality using simulated data."""
    data = {"nick": [12, 15, 19], "kingsley": [2.0, 15.0, 10.0]}
    r = randomly_choose()
    new_data = scraper.export_data(data, r.county, 9999)
    assert type(new_data) == pd.DataFrame
    assert "Year" in new_data.columns
    assert "County" in new_data.columns


def test_generate_file_names():
    """Tests successful creation of file paths for export."""
    files = scraper.generate_file_names()
    assert type(files) == list
    assert type(files[0]) == str
    assert all(".csv" in f for f in files)
    assert all("data" in f for f in files)


def test_combine_files():
    columns = [
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
    df = scraper.combine_files()
    assert type(df) == pd.DataFrame
    assert df.columns == columns
    ...
