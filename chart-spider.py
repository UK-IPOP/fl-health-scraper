import scrapy
from scrapy.http.request.form import FormRequest

DASHBOARD_URL = "https://www.flhealthcharts.gov/ChartsDashboards/rdPage.aspx?rdReport=SubstanceUse.Report&irbSelection=1"


class CombosSpider(scrapy.Spider):
    name = "combos"
    start_urls = [DASHBOARD_URL]

    def parse(self, response):
        county_values: list[str] = response.css(
            "#islCounty option::attr(value)"
        ).getall()
        county_names: list[str] = response.css("#islCounty option::text").getall()
        year_values: list[str] = response.css("#islYearsC option::attr(value)").getall()
        for county_code, county_name, year_code in zip(
            county_values, county_names, year_values
        ):
            request = FormRequest(
                url=DASHBOARD_URL,
                callback=self.parse_data_page,
                method="POST",
                formdata={
                    "cslCounty": str(county_code),
                    "cslYearsC": str(year_code),
                },
            )
            request.cb_kwargs["county"] = county_name
            request.cb_kwargs["year"] = year_code
            yield request

    def parse_data_page(self, response, county, year):
        headers: list[str] = response.css("table thead tr th::text").getall()
        for row in response.css("tr[row]"):
            # gets only for the row so length varies (1-10ish)
            row_cells: list[str] = row.css("td span[id^=lbl]::text").getall()
            # remove the hover description
            row_cells.pop(1)
            # zip cells to headers
            row_data: dict[str, str] = {x[0]: x[1] for x in zip(headers, row_cells)}
            row_data["scraped_county"] = county
            row_data["scraped_year"] = year
            yield row_data
