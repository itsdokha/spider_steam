import scrapy
from spider_steam.items import SpiderSteamItem
import requests
from bs4 import BeautifulSoup


class SteamProductSpider(scrapy.Spider):
    name = "SteamProductSpider"
    allowed_domains = ["store.steampowered.com"]
    start_urls = [
        'https://store.steampowered.com/search/?g=n&SearchText=Sandbox&page=1',
        'https://store.steampowered.com/search/?g=n&SearchText=Sandboxpage=2',
        'https://store.steampowered.com/search/?g=n&SearchText=Simulation&page=1',
        'https://store.steampowered.com/search/?g=n&SearchText=Simulation&page=2',
        'https://store.steampowered.com/search/?g=n&SearchText=RPG&page=1',
        'https://store.steampowered.com/search/?g=n&SearchText=RPG&page=2']
        
    
    def start_requests(self):
        for url in self.start_urls:
            # yield scrapy.Request(url=get_url(url), callback=self.parse_for_page)
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
        product_price = response.xpath('//div[@class="game_purchase_price price"]/text()')[0].extract()
        product_platforms = response.css('div').xpath('@data-os')

        if product_name != '' and product_release_date[-1] > '2000':
            items['product_name'] = ''.join(product_name).strip().replace('™', '')
            items['product_category'] = ', '.join(product_category).strip()
            items['product_reviews_num'] = ', '.join(x.strip() for x in product_reviews_num).strip().replace('(', '').replace(')', '')
            items['product_release_date'] = ''.join(product_release_date).strip()
            items['product_developer'] = ', '.join(x.strip() for x in product_developer).strip()
            items['product_tags'] = ', '.join(x.strip() for x in product_tags).strip()
            items['product_price'] = ''.join(product_price).strip().replace('уб', '')
            items['product_platforms'] = ' '.join(x.get().strip() for x in product_platforms)
        yield items
