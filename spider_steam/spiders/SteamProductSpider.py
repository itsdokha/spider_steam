import scrapy
from spider_steam.items import SpiderSteamItem
import requests
from bs4 import BeautifulSoup


def do_start_urls():
    start_urls = []
    queries = ['indie', 'strategy', 'minecraft']
    for query in queries:
        for i in range(1, 3):
            url = ('https://store.steampowered.com/search/?sort_by=&sort_order=0&term=' + str(query) +
                   '&supportedlang=english&page=' + str(i))

            start_urls.append(url)
    return start_urls


class SteamProductSpider(scrapy.Spider):
    name = "SteamProductSpider"
    allowed_domains = ["store.steampowered.com"]
    start_urls = do_start_urls()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_for_page)

    def parse_for_page(self, response):
        games = response.css('a[class = "search_result_row ds_collapse_flag "]::attr(href)').extract()
        for link in games:
            if 'agecheck' not in link:
                yield scrapy.Request(link, callback=self.parse_for_game)

    def parse_for_game(self, response):
        items = SpiderSteamItem()
        product_name = response.xpath('//span[@itemprop="name"]/text()').extract()
        product_category = response.xpath('//span[@data-panel]/a/text()').extract()
        product_reviews_num = response.xpath('//span[@class = "responsive_reviewdesc_short"]/text()').extract()
        product_release_date = response.xpath('//div[@class="date"]/text()').extract()
        product_developer = response.xpath('//div[@id="developers_list"]/a/text()').extract()
        product_tags = response.xpath('//a[@class="app_tag"]/text()').extract()
        product_price = response.xpath('//div[@class="discount_final_price"]/text()').extract()
        if len(product_price) == 0:
            product_price = response.xpath('//div[@class="game_purchase_price price"]/text()').extract()
        product_platforms = response.css('div').xpath('@data-os')

        if len(product_name) != 0 and product_release_date[-1] > '2000':
            items['product_name'] = ''.join(product_name).strip().replace('™', '')
            items['product_category'] = ', '.join(product_category).strip()
            items['product_reviews_num'] = ', '.join(x.strip() for x in product_reviews_num).strip().replace('(',
                                                                                                             '').replace(
                ')', '')
            items['product_release_date'] = ''.join(product_release_date).strip()
            items['product_developer'] = ', '.join(x.strip() for x in product_developer).strip()
            items['product_tags'] = ', '.join(x.strip() for x in product_tags).strip()
            items['product_price'] = ''.join(product_price).strip().replace('уб', '')
            items['product_platforms'] = ' '.join(x.get().strip() for x in product_platforms)
            yield items
