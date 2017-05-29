import scrapy
from scrapy.http import Request
from creeper_imdb.items import ImdbItem
import re
import subprocess as subp
import os
import math
import codecs

class ImdbSpider(scrapy.Spider):
    global movie_id
    name = "imdb"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["http://www.imdb.com/search/title?title_type=feature&primary_language=cmn&country_of_origin=cn&sort=moviemeter,asc&page=1&ref_=adv_nxt"
    ]
    def parse(self, response):
        # filename = response.url.split("/")[-2]
        # with open('index', 'wb') as f:
        #     f.write(response.body)
        index_raw = response.xpath('//span[@class="lister-current-last-item"]/..').extract()
        temp_index = re.findall('[0-9,]*(?= titles)',index_raw[0])[0]
        total_index = int(math.floor(int(re.sub(',','',temp_index))/50))
        for search_pages in range(1,total_index):
            temp_url = 'http://www.imdb.com/search/title?title_type=feature&primary_language=cmn&country_of_origin=cn&page='+str(search_pages)+'&sort=user_rating,desc&ref_=adv_nxt' 
            yield Request(temp_url,callback=self.index_parse)


    def index_parse(self, response):
        imdb_entry = response.xpath('//div/@data-tconst').extract()
        for item in imdb_entry:
            temp_url = 'http://www.imdb.com/title/' + item
            yield Request(temp_url,callback=self.moive_parse)

    def moive_parse(self, response):
        item = ImdbItem() # for sel in response.xpath('//ul/li'):
        # temp_id = response.xpath('//div[@ratings_wrapper]').extract()

        # item['identifier'] = re.findall('tt[0-9]*',temp_id)[0] 
        movie_id = response.url.split("/")[-2]
        item['identifier'] = response.url.split("/")[-2]
        item['title'] = response.xpath('//title/text()').extract()
        item['publish_date'] = response.xpath('//a/meta[@itemprop="datePublished"]/@content').extract()
        item['director'] = response.xpath('//div[@class="credit_summary_item"]/span[@itemprop="director"]/..//span[@itemprop="name"]/text()').extract()
        item['creator']  = response.xpath('//div[@class="credit_summary_item"]/span[@itemprop="creator"]/..//span[@itemprop="name"]/text()').extract()
        item['cast'] = response.xpath('//div[@class="credit_summary_item"]/span[@itemprop="actors"]/..//span[@itemprop="name"]/text()').extract()
        item['country'] = response.xpath('//h4[@class="inline" and text()="Country:"]/../a/text()').extract()
        item['language'] = response.xpath('//h4[@class="inline" and text()="Language:"]/../a/text()').extract()
        item['review_info'] = response.xpath('//div/span[@itemprop="reviewCount"]/text()').extract()
        temp_pageinfo=item['review_info'][0]
        temp_page = re.findall('[0-9,]*(?= user)',temp_pageinfo)[0]
        total_pages = int(math.floor(int(re.sub(',','',temp_page))/10))
        print(total_pages)
        if not os.path.exists(movie_id + '/'):
            os.makedirs(movie_id+ '/')
        # subp.call('scrapy crawl imdb_review', shell=True)
        if total_pages == 1:
            temp_url = 'http://www.imdb.com/title/' + movie_id + '/reviews?start=0' 
            yield Request(temp_url,callback=self.imdb_review)
        else:
            for counts in range(0,total_pages+1):
                temp_url = 'http://www.imdb.com/title/' + movie_id + '/reviews?start=' + str(counts*10)
                yield Request(temp_url,callback=self.imdb_review)
        # review_pages = 
    # country = scrapy.Field()
    # language = scrapy.Field()
    # review  = scrapy.Field()
        filename = response.url.split("/")[-2]
        with open(movie_id+'/'+ filename, 'wb') as f:
            for entry in item:
                f.write(entry +  ':' )
                f.write(str(item[entry]))
                f.write('\n')

        # return item

    def imdb_review(self,response):
        movie_id= response.url.split("/")[-2]
        temp_detail = response.xpath('//div/small/..').extract()
        temp_text = response.xpath('//div/small/../../p').extract()
        if not os.path.exists(movie_id):
            os.makedirs(movie_id)
        temp_pages = response.xpath('//table/tr/td//font/text()').extract()
        temp_current_pages = re.findall('[0-9,]*(?= of)',temp_pages[0])[0]
        current_pages = int(re.sub(',','',temp_current_pages))
        for index,entry in enumerate(temp_detail):
            # print(index,temp_detail)
            review_num= (current_pages-1) *10 +index
            with open(movie_id+ '/review_' + str(review_num), 'w') as f:
                f.write(temp_detail[index].encode('utf8'))
                f.write(temp_text[index].encode('utf8'))


# class ImdbSpider_review(scrapy.Spider):
#     # def __init__(self,ImdbSpider):
#     #     self.total_pages = ImdbSpider.total_pages
#     #     self.movie_id = ImdbSpider.movie_id
#     # movie_id = ImdbSpider.movie_id
#     # global movie_id,total_pages
#     # total_pages = ImdbSpider.total_pages
#     # movie_id = ImdbSpider.movie_id
#     name = "imdb_review"
#     allowed_domains = ["www.imdb.com"]
#     ini_url = "http://www.imdb.com/title/" + movie_id + "/reviews?start=0"
#     start_urls =[ini_url] 
    
#     # review_pages = int(re.findall('(?<=of )[0-9]*(?=:)',temp_pages[0])[0])


#     # start_urls = ["http://www.imdb.com/title/tt0068646/reviews?start=0"
    

#     def parse(self, response):
#         # item = ImdbItem() # for sel in response.xpath('//ul/li'):
#         temp_detail = response.xpath('//div/small/..').extract()
#         temp_text = response.xpath('//div/small/../../p').extract()
#         if not os.path.exists(movie_id):
#             os.makedirs(movie_id)
#         temp_pages = response.xpath('//table/tr/td//font/text()').extract()
#         current_pages = num(re.findall('[0-9]*(?= of)',temp_pages[0])[0])
#         for index,entry in enumerate(temp_detail):
#             with open(movie_id/'review_' + current_pages, 'wb') as f:
#                 f.write(temp_detail[index])
#                 f.write(temp_text[index])


#         return item





