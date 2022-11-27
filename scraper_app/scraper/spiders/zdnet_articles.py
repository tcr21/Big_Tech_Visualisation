import scrapy
from scraper.items import ZDNetArticlesItem


class ZDNetSpider(scrapy.Spider):
    name = "zdnet_articles"

    start_urls = [
        "https://www.zdnet.com/topic/microsoft/rss.xml",
        "https://www.zdnet.com/topic/ibm/rss.xml",
        "https://www.zdnet.com/topic/google/rss.xml",
        "https://www.zdnet.com/topic/apple/rss.xml",
    ]

    # all this does is define what you want to do with the results of each HTML scrape from
    # the links in start_urls
    def parse(self, response):
        # loop through every news item
        for article in response.css("channel item"):
            # get the link to the article
            article_link = article.css("link::text").get()
            # assuming that the link isn't dead, follow the link and scrape the article itself
            if article_link is not None:
                yield scrapy.Request(article_link, callback=self.parse_article)

    def parse_article(self, response):
        # create new item (useful for pipeline)
        item = ZDNetArticlesItem()

        # add all relevant info to the item.
        # TODO something really odd is happening with the date and link, possibly being sent back as lists?
        item["title"] = (response.xpath("//head/title/text()").get(),)
        item["date"] = (response.xpath("//time/@datetime").get(),)
        item["link"] = (
            response.xpath('//head/meta[@property="og:url"]/@content').get(),
        )
        item["text"] = (
            "\n".join(response.xpath('//div[@class="storyBody"]/p/text()').getall()),
        )
        item["short_desc"] = response.xpath(
            '//head/meta[@property="og:description"]/@content'
        ).get()
        item["publisher"] = "ZD Net"
        # hand the item back to the parse method
        yield item
