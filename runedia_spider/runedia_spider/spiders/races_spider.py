import scrapy
import arrow


class RunediaSpider(scrapy.Spider):
    name = "races_spider"

    def get_urls(self, first_year=2019, last_year=None):
        actual_year = last_year
        if not last_year:
            actual_year = arrow.utcnow().year
        base_url = "https://runedia.mundodeportivo.com/en/races-calendar/spain/comunidad/provincia/mountain-races/distancia/{year}-{month}/0/0/"
        urls_list = []
        for year in range(first_year, actual_year + 1):
            for month in range(1, 13):
                urls_list.append(base_url.format(year=year, month=month))
        return urls_list

    def start_requests(self):
        for url in self.get_urls():
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        curses = response.css("div.item-cursa")
        year = response.request.url.split("/")[10].split("-")[0]
        for cursa in curses:
            print(cursa.css("span::text").getall())
            # Parse the distance
            distance = "Unknown"
            all_spans = cursa.css("span::text").getall()
            for span in all_spans:
                # Distances end with m from meters
                if span.endswith("m"):
                    distance_int = span[:len(span) - 1].strip()
                    if distance_int.isdigit():
                        distance = span
                        break
                else:
                    distance_int = span.strip()
                    if distance_int.isdigit():
                        distance = span
                        break
            location = cursa.css("span.lloc::text").get()
            delimiter = None
            if ',' in location:
                delimiter = ','
            yield {
                "day": cursa.css("span.dia::text").get(),
                "month": cursa.css("span.mes::text").get(),
                "province": location.split(delimiter)[0],
                "town": location.split(delimiter)[1],
                "title": cursa.css("a::attr(title)").get(),
                "distance": distance,
                "status": cursa.css("img.icono::attr(title)").get(),
                "year": year
            }
