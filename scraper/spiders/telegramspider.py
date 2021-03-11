import scrapy

class TelegramSpider(scrapy.Spider):
    name = 'telegram'

    seed = pd.read_csv('groups.csv')
    seed = seed.loc[(seed['consp'] == 1.0) & (seed['eng'] != 1.0)]
    seed = seed.drop(columns = ['consp', 'eng'])
    seed.reset_index(inplace=True)
    seed = seed['ch_name'].tolist()
    
    start_urls = ['https://web.telegram.org/#/im?p=@' + x for x in seed]

    #TODO Get the messages using html tags.

    def parse(self, response):
        for title in response.css(''):
            yield {'title': title.css('::text').get()}

        for next_page in response.css('a.next'):
            yield response.follow(next_page, self.parse)

