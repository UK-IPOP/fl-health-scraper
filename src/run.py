import helpers

def run():
    for year in helpers.YEARS:
        for name, id in helpers.COUNTIES.items():
            site_content = helpers.visit_site(helpers.URL, id, year)
            site_data = helpers.scrape_site(site_content)
            dataframe = helpers.format_data(site_data)
            helpers.export_data(df=dataframe, year=year, county_name=name)

run()