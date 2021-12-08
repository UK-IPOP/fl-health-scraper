import scrapy
from . import utils
import json

urls = utils.read_urls()


class OpioidDashboardSpider(scrapy.Spider):
    name = "opioid_dashboard"
    start_urls = urls

    def parse(self, response):
        county_info = utils.extract_county_name_and_year(response.url)
        headers: list[str] = response.css("#dtSubstanceUse thead th::text").getall()
        with open(f"data/{county_info['name']}_{county_info['year']}.jsonl", "w") as f:
            for row in response.css("tr[row]"):
                # gets only for the row so length varies (1-10ish)
                row_data: list[str] = []
                for cell in row.css("td"):
                    cell_text = cell.css("span[id]::text").get(default="")
                    row_data.append(cell_text)
                # zip row data to headers
                zipped_data: dict[str, str] = {
                    x[0]: x[1] for x in zip(headers, row_data)
                }
                f.write(json.dumps(zipped_data))
                f.write("\n")
