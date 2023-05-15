import scrapy


class FlashscorehistoricityspiderSpider(scrapy.Spider):
    name = "flashscoreHistoricitySpider"
    allowed_domains = ["www.flashscore.com"]
    start_urls = ["https://www.flashscore.com/"]
    global base_url
    base_url = "https://www.flashscore.com"

    custom_settings = {
        'FEEDS': { 'data.csv': { 'format': 'csv',}}
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
        #yield scrapy.Request(url, meta=dict(playwright = True, playwright_include_page = True, errback=self.errback))
        yield scrapy.Request(base_url, meta={'playwright':True})


    def parse(self, response):
        #page = response.meta["playwright_page"]
        #await page.close()

        # TODO 
        # click on "Show more" to load all countries
        
        # construct country links
        for i in response.xpath('//div[@class = "lmc__block "]/a'):
            # country_name --> Albania
            country_name =  i.xpath('./span[@class="lmc__elementName"]/text()').get()

            # countries_links --> https://www.flashscore.com/football/albania/
            country_final_url = base_url + i.xpath('@href').get()

            #yield scrapy.Request(url = country_final_url, callback = self.parse_country, meta={'playwright':True})
            yield scrapy.Request(url = country_final_url, 
                                 callback = self.parse_country, 
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
            
            yield scrapy.Request(url = archive_url,
                                 callback = self.parse_country_league_archived_competitions,
                                 meta = {'country': cn, 'league': league})
                

    # function to parse each league and construct archived urls
    def parse_country_league_archived_competitions(self, response):
        cn = response.meta.get('country')
        league = response.meta.get('league')

        for k in response.xpath('//div[@class = "archive__row"]'):
            #print("--------------------------")
            #print(k.xpath('div[@class="archive__season"]/a/@href').get())
            spec_archived_competition = base_url + k.xpath('div[@class="archive__season"]/a/@href').get()
            #print(spec_archived_competition)
            yield{'country': cn,
                  'league': league,
                  'hist_url': spec_archived_competition}

    # function to parse each archived competition
    def parse_archived_competition(self, response):
        # TODO
        # click on "Show more matches" link to load all matches
        pass
    
    
    #async def errback(self, failure):
    #    page = failure.request.meta["playwright_page"]
    #    await page.close()

