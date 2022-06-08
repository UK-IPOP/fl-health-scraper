# %%
from os import sep
from bs4 import BeautifulSoup
from pathlib import Path

# %%
web_files = Path("data/scraped").glob("*.html")

for file in web_files:
    with open(file, "r") as input_file:
        soup = BeautifulSoup(input_file.read(), "html.parser")

    with open(f"data/datafiles/{file.stem}.csv", "w") as output_file:
        table = soup.find("table", id="dtOverdose")
        for row in table.find_all("tr"):
            data = [
                d.text.strip().replace(",", "")
                for d in row.find_all("td", recursive=False)
            ]
            if data and len(data) > 1:
                data[0] = data[0].split("\xa0")[0]
                output_file.write(",".join(data) + "\n")

# %%

data_files = Path("data/datafiles").glob("*.csv")
with open("data/output.csv", "w") as output_file:
    # header
    output_file.write(
        "County,Year,Indicator,Measure,Year,Jan-Mar,Apr-Jun,Jul-Sep,Oct-Dec,Annual\n"
    )
    for file in data_files:
        county, year = file.stem.split("_")
        with open(file, "r") as input_file:
            for line in input_file:
                output_file.write(f"{county.title()},{year},{line}")

# %%
