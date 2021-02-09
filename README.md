# FL Health Scraper
FL Health Charts Opioid Use Dashboard Web Scraper

## Installation
Get the code from GitHub:

`gh repo clone UK-IPOP/fl-health-scraper`

Install dependencies:

`poetry install`

OR, install production only dependencies:

`poetry install --dev-only`


Then: `poetry shell` to activate the virtual environment.

## Utilize API
```python
import fl_health_scraper as scraper

# collects data from all sites and creates data directory with year sub-directories
scraper.gather_data()  # can take some time

# combine all of the files into one csv for analysis
# file -> composite.csv in data directory
scraper.combine_files() 
```

## Run tests
To run the test suite: `poetry run pytest --cov`

## Future plans:
1. Build API functionality into gather_data() to specify select years/counties for smaller queries.
2. Build asynchronous functionality to increase gather_data() speed.
