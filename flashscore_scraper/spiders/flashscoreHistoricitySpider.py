import scrapy
from scrapy.selector import Selector


class FlashscorehistoricityspiderSpider(scrapy.Spider):
    name = "flashscoreHistoricitySpider"
    allowed_domains = ["www.flashscore.com"]
    start_urls = ["https://www.flashscore.com/"]

    global base_url
    base_url = "https://www.flashscore.com"

    custom_settings = {
        'FEEDS': {'data.csv': {'format': 'csv', }}
    }

    def start_requests(self):
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
        # yield scrapy.Request(url, meta=dict(playwright = True, playwright_include_page = True, errback=self.errback))
        yield scrapy.Request(base_url, callback=self.parse,
                             meta=dict(playwright=True, playwright_include_page=True))

    def parse(self, response):
        # page = response.meta["playwright_page"]
        # page.set_default_timeout(1000)

       # construct country links
        for i in response.xpath('//div[@class = "left_menu_categories_seo"]/a'):
            # country_name --> Albania
            country_name = i.xpath(
                './span[@class="lmc__elementName"]/text()').get()

            # countries_links --> https://www.flashscore.com/football/albania/
            country_final_url = base_url + i.xpath('@href').get()

            # yield scrapy.Request(url = country_final_url, callback = self.parse_country, meta={'playwright':True})
            yield scrapy.Request(url=country_final_url,
                                 callback=self.parse_country,
                                 meta={'country_name': country_name})
            break

    # function to parse each country to get the leagues it has

    def parse_country(self, response):
        cn = response.meta.get('country_name')
        for j in response.xpath('//div[@class = "leftMenu__item leftMenu__item--width "]'):
            # league url --> https://www.flashscore.com/football/albania/
            league = j.xpath('a/text()').get()
            league_url = base_url + j.xpath('a/@href').get()

            # archive url --> https://www.flashscore.com/football/albania/superliga/archive/
            archive_url = league_url + "archive/"

            yield scrapy.Request(url=archive_url,
                                 callback=self.parse_country_league_archived_competitions,
                                 meta={'country': cn, 'league': league})

    # function to parse each league and construct archive/results urls

    def parse_country_league_archived_competitions(self, response):
        cn = response.meta.get('country')
        league = response.meta.get('league')

        for k in response.xpath('//div[@class = "archive__row"]'):
            if any(map((k.xpath('div[@class="archive__season"]/a/@href').get()).__contains__,
                       ('2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023'))):
                spec_archived_competition = base_url + k.xpath('div[@class="archive__season"]/a/@href').get() + "results/"
                # print(spec_archived_competition)
                yield scrapy.Request(url=spec_archived_competition,
                                     callback=self.parse_archived_competition,
                                     meta=dict(counrty=cn,
                                               league=league,
                                               url=spec_archived_competition,
                                               playwright=True,
                                               playwright_include_page=True))

    # function to parse each archived competition

    async def parse_archived_competition(self, response):
        print('--------------------------------')
        print('entering parse_archived_competition function')
        print('--------------------------------')

        page = response.meta['playwright_page']
        #page.set_default_timeout(0)
        #print(page)

        #hist_url = response.meta.get('hist_url')
        cn = response.meta.get('country')
        league = response.meta.get('league')
        url = response.meta.get('url')

        # TODO - click on "Show more matches" link to load all matches (e.g. https://www.flashscore.com/football/albania/superliga-2019-2020/results/)
        # try:
        #    while button := page.locator("//a[contains(@class,'event__more--static')]"):
        #        await button.scroll_into_view_if_needed()
        #        await button.click()
        #        print('------- button clicked ??? -------')
        # except:
        #    pass

        # content = await page.content()
        # sel = Selector(text=content)

        show_more_exists_tmp = response.xpath("//a[contains(@class,'event__more--static')]")

        if (show_more_exists_tmp == []):
            print("------------------ Show more matches url NOT found ------------------")
            # print(response.xpath('//a[@class="event__more.event__more--static"]'))
            # yield scrapy.Request(url = self.parse_archived_competition,callback = self.parse_archived_competition,meta = {'country': cn,'league': league})
        else:
            print("------------------ Show more matches url found ------------------")
            try:
                while button := page.locator("//a[contains(@class,'event__more--static')]"):
                    await button.scroll_into_view_if_needed()
                    await button.click()
                    print('------- button clicked ??? -------')
            except:
                pass
            # print(response.xpath('//a[@class="event__more event__more--static"]/@href').get())

        # TODO - correct url is spec_archived_competition + results/

        # TODO - callback for each match
        pass

    # function to parse each match

    def parse_match(self, response):
        pass

    # async def errback(self, failure):
    #    page = failure.request.meta["playwright_page"]
    #    await page.close()
