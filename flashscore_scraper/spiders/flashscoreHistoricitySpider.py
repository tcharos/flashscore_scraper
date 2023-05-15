import scrapy


class FlashscorehistoricityspiderSpider(scrapy.Spider):
    name = "flashscoreHistoricitySpider"
    allowed_domains = ["www.flashscore.com"]
    start_urls = ["https://www.flashscore.com/"]

    def start_requests(self):
        url = "https://www.flashscore.com/"
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "el-GR,el;q=0.9,en;q=0.8",
            "Referer": "https://www.flashscore.com/",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "X-Requested-With": "Fetch",
        }
        yield scrapy.Request(url, meta={'playwright':True})

    def parse(self, response):
        # get Country links e.g. /football/albania/
        for i in response.xpath('//div[@class = "left_menu_categories_seo"]'):
            countries_paths_list = i.xpath('a/@href').extract()
            #print(countries_paths_list)
            countries_links_final = ["https://www.flashscore.com" + ls for ls in countries_paths_list]
            print(countries_links_final)

        # get league

        # https://www.flashscore.com/football/albania/superliga/archive/
        
