# Florida Health Scraper

<!-- [![Go Reference](https://pkg.go.dev/badge/github.com/UK-IPOP/fl-health-scraper.svg)](https://pkg.go.dev/github.com/UK-IPOP/fl-health-scraper) -->

This is the Florida Health Charts Substance Use Dashboard Web Scraper.

It will scrape the FL Health Charts Substance Use Dashboard for 68 counties plus the entire state of Florida from 2015-2021 and output the results into the `results.csv` file.

## Usage

To use:

```bash
git clone https://github.com/UK-IPOP/fl-health-scraper
cd fl-health-scraper/fl_health_charts
scrapy crawl opioid_dashboard
```

Then you can see the output in `fl-health-scraper/data/results.csv`
