# FL Health Scraper
FL Health Charts Opioid Use Dashboard Web Scraper

More documentation can be found [here](https://UK-IPOP.github.io/fl-health-scraper/).

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

# collects data from all sites and cleans dirs after finished
df = scraper.gather_data()  # takes some time,, maybe go refresh your coffee
df.head()  # see results

```

## Run tests
To run the test suite: `poetry run pytest --cov`

## Future plans:
1. Build API functionality into gather_data() to specify select years/counties for smaller queries.
2. Build asynchronous functionality to increase gather_data() speed.
3. Add long-form functionality from notebook analysis to API.