import scrapy


class OpioidDashboardSpider(scrapy.Spider):
    name = 'opioid_dashboard'
    allowed_domains = ['https://flhealthcarts.gov']
    start_urls = ['http://https://flhealthcarts.gov/']

    def parse(self, response):
        pass
