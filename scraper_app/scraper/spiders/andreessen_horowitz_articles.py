import scrapy
from scraper.items import AndreessenHorowitzArticlesItem


class AndreessenHorowitzSpider(scrapy.Spider):
    name = "andreessen_horowitz_articles"

    start_urls = ["https://a16z.com/articles/feed/"]

    # all this does is define what you want to do with the results of each HTML scrape from
    # the links in start_urls

    def parse(self, response):
        # loop through every news item
        for article in response.css("item"):
            # get the link to the article
            article_link = article.css("link::text").get()
            # assuming that the link isn't dead, follow the link and scrape the article itself
            if article_link is not None:
                yield scrapy.Request(article_link, callback=self.parse_article)

    def parse_article(self, response):
        # create new item (useful for pipeline)
        item = AndreessenHorowitzArticlesItem()

        # add all relevant info to the item.
        item["title"] = (response.xpath("//head/title/text()").get(),)
        item["date"] = (
            response.xpath(
                '//head/meta[@property="article:published_time"]/@content'
            ).get(),
        )
        item["link"] = (
            response.xpath('//head/meta[@property="og:url"]/@content').get(),
        )
        # TODO Some stories have inconsistent text formatting which skips the p tags, unsure how to resolve. Occurs roughly 1/10 stories
        item["text"] = ("\n".join(response.css("p::text").getall()[1:-3]),)
        item["short_desc"] = response.xpath(
            '//head/meta[@property="og:description"]/@content'
        ).get()
        item["publisher"] = "Andreessen Horowitz"

        # hand the item back to the parse method
        yield item
