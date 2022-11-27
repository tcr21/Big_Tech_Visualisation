import scrapy
from scraper.items import GuardianArticlesItem


class GuardianSpider(scrapy.Spider):
    name = "guardian_articles"

    start_urls = ["https://www.theguardian.com/uk/technology/rss"]

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
        item = GuardianArticlesItem()

        # add all relevant info to the item.
        # TODO something really odd is happening with the date and link, possibly being sent back as lists?
        item["title"] = (response.xpath("//head/title/text()").get(),)
        item["date"] = (
            response.xpath(
                '//head/meta[@property="article:published_time"]/@content'
            ).get(),
        )
        item["link"] = (
            response.xpath('//head/meta[@property="og:url"]/@content').get(),
        )
        item["text"] = ("\n".join(response.css("body p::text").getall()[2:]),)
        # item['text'] = response.xpath('//body//div[@data-gu-name="body"]//div[@id="maincontent"]//p[@class="dcr-eu20cu"]')
        item["short_desc"] = response.xpath(
            '//head/meta[@property="og:description"]/@content'
        ).get()
        item["publisher"] = "Guardian"
        # hand the item back to the parse method
        yield item
