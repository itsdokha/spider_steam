# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderSteamItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = scrapy.Field()
    product_category = scrapy.Field()
    product_reviews_num = scrapy.Field()
    product_release_date = scrapy.Field()
    product_developer = scrapy.Field()
    product_tags = scrapy.Field()
    product_price = scrapy.Field()
    product_platforms = scrapy.Field()

