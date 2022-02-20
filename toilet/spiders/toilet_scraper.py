import scrapy
from scrapy.http import Request
from time import sleep
import json
import os

file_dir = r"C:\Users\luke-\Projects\Suite_Selector\Toilet Data"


class ToiletScraperSpider(scrapy.Spider):
    name = "toilet_scraper"
    allowed_domains = ["www.reece.com.au"]
    start_urls = [
        "https://www.reece.com.au/search/toilets-c469/toilet-suites-c705/?sortBy=POPULARITY&sortDirection=DESCENDING&pageNumber=1&pageSize=45&generalFacets=waterinletposition%3Abottominletreversiblerightorleft%2Cbottominlet%2Cbottominletrighthandside%2Cbackinletlefthandside"
    ]

    def parse(self, response):
        toilets = response.xpath('//div[@class="product-grid-wrapper"]/div')
        for toilet in toilets:
            toilet_url = toilet.xpath(
                './div[@class="product-tile__content"]/div[@class="product-tile__section-details"]/a/@href'
            ).extract_first()
            absolute_toilet_url = response.urljoin(toilet_url)
            yield Request(absolute_toilet_url, callback=self.toilet_parse)

    def toilet_parse(self, response):
        page_url = response.url
        toilet_image = response.xpath(".//img/@src").extract_first()
        product_name = response.xpath(
            '//h1[@class="pdp-main-block__product-name"]/text()'
        ).extract_first()
        product_name = product_name.strip()
        product_code = response.xpath(
            '//p[@class="pdp-main-block__product-code"]/span/text()'
        ).extract_first()
        table = response.xpath('//div[@class="mobile-padded"]/table')[0]
        rows = table.xpath("./tr")
        p_trap_setout = rows.xpath(
            './/th[contains(.,"P Trap Setout")]/following-sibling::td/text()'
        ).extract_first()
        if p_trap_setout is not None:
            try:
                p_trap_setout = p_trap_setout.replace(" mm", "")
            except:
                p_trap_setout = "Null"
        s_trap_min_set = rows.xpath(
            './/th[contains(.,"S Trap Min Setout")]/following-sibling::td/text()'
        ).extract_first()
        if s_trap_min_set is not None:
            try:
                s_trap_min_set = s_trap_min_set.replace(" mm", "")
            except:
                s_trap_min_set = "Null"
        s_trap_max_set = rows.xpath(
            './/th[contains(.,"S Trap Max Setout")]/following-sibling::td/text()'
        ).extract_first()
        if s_trap_max_set is not None:
            try:
                s_trap_max_set = s_trap_max_set.replace(" mm", "")
            except:
                s_trap_max_set = "Null"
        s_trap_set_out = rows.xpath(
            './/th[contains(.,"S Trap Setout")]/following-sibling::td/text()'
        ).extract_first()
        if s_trap_set_out is not None:
            try:
                s_trap_set_out = s_trap_set_out.replace(" mm", "")
            except:
                s_trap_set_out = "Null"
        spec_sheet = response.xpath(
            '//div[@class="detail-resource-block__content"][1]/a[1]/@href'
        ).extract_first()
        yield {
            "pageUrl": page_url,
            "image": toilet_image,
            "productName": product_name,
            "productCode": product_code,
            "specSheet": spec_sheet,
            "PTrapSetout": p_trap_setout,
            "STrapSetout": s_trap_set_out,
            "STrapMin": s_trap_min_set,
            "STrapMax": s_trap_max_set,
            "BottomInlet": True
        }

