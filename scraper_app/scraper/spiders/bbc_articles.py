import scrapy
from scraper.items import BBCArticlesItem


class BBCSpider(scrapy.Spider):
    name = "bbc_articles"

    start_urls = ["http://feeds.bbci.co.uk/news/technology/rss.xml"]

    # all this does is define what you want to do with the results of each HTML scrape from
    # the links in start_urls

    def parse(self, response):
        # loop through every news item
        for article in response.css("channel item"):
            # get the link to the article
            article_link = article.css("guid::text").get()
            # assuming that the link isn't dead, follow the link and scrape the article itself
            if article_link is not None:
                yield scrapy.Request(article_link, callback=self.parse_article)

    def parse_article(self, response):
        # create new item (useful for pipeline)
        item = BBCArticlesItem()

        # add all relevant info to the item.
        # TODO something really odd is happening with the date and link, possibly being sent back as lists?
        item["title"] = (response.xpath("//head/title/text()").get(),)
        item["date"] = (response.xpath("//time/@datetime").get(),)
        item["link"] = (response.xpath('//head/link[@rel="canonical"]/@href').get(),)
        item["text"] = (
            "\n".join(
                response.xpath(
                    '//article//p[@class="ssrcss-1q0x1qg-Paragraph eq5iqo00"]/text()'
                ).getall()
            ),
        )
        item["short_desc"] = response.xpath(
            '//head/meta[@property="og:description"]/@content'
        ).get()
        item["publisher"] = "BBC"
        # hand the item back to the parse method
        yield item
