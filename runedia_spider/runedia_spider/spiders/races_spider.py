import scrapy
import arrow


class QuotesSpider(scrapy.Spider):
    name = "races_spider"

    def get_urls(first_year=1999, last_year=None):
        actual_year = last_year
        if not last_year:
            actual_year = arrow.utcnow().year
        base_url = "https://runedia.mundodeportivo.com/en/races-calendar/pais/comunidad/provincia/tipo/distancia/{year}-{month}/0/0/"
        urls_list = []
        for year in range(first_year, actual_year + 1):
            for month in range(1, 13):
                urls_list.append(base_url.format(year=year, month=month))
        return urls_list

    def start_requests(self):
        for url in self.get_urls():
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
