# 用作测试的爬虫

import json
import re

import scrapy
from scrapy import FormRequest

from AustialiaHouse.Helper.CityHelper import au_area_url, kCityDomain, getItemWith, getBigAreaWith
from AustialiaHouse.config.env import IS_DEV
from AustialiaHouse.config.useragent import get_user_agent
from AustialiaHouse.items import Postcode


class test(scrapy.Spider):
    name = 'test'
    au_items = au_area_url()

    allowed_domains = ["realestate.com.au"]
    start_urls = [
    ]

    def start_requests(self):
        rst = ['http://www.geopostcodes.com/browse.php?t=2&n=50&id=AU050708&l=0']
        # rst = ['https://www.realestate.com.au/property-apartment-qld-hamilton-125653546']
        ua = get_user_agent()
        for r in rst:
            url = str(r)
            yield FormRequest(url, callback=self.get_nearby_school, meta={}, headers={'User-Agent': ua})

            if IS_DEV:
                return

    def get_nearby_school(self, response):
        pcItem = Postcode()

        tr_items = response.xpath('.//tr[@itemscope]')
        tr_next_list = response.xpath('.//tr[contains(@class, "nextlist")]/td/@onclick').extract_first()
        print("tr itemsss", tr_items)
        print(tr_next_list)
        r = re.compile(r'".*"')
        r_result = r.findall(tr_next_list)
        href = ""
        if r_result and len(r_result) > 0:
            try:
                href = r_result[0].strip('"')
            except (IOError, AttributeError) as e:
                print(e)

        if len(href) > 0:
            href = kCityDomain + "/browse.php?" + href

        for tr_item in tr_items:
            # print("tritem", tr_item.extract())
            tr_item_list = tr_item.xpath('./td')
            if len(tr_item_list) > 3:
                tr_item0 = tr_item_list[0].xpath('.').extract_first()
                # print("tr_item0",tr_item0)
                if str.find(tr_item0, "href=") == -1:
                    name = tr_item_list[0].xpath('./text()').extract_first()
                    href = False
                else:
                    name = tr_item_list[0].xpath('./a/text()').extract_first()
                    href = tr_item_list[0].xpath('./a/@href').extract_first()
                # print('href : ',href)
                postcode = tr_item_list[2].xpath('./text()').extract_first()
                if name:
                    pcItem["street"] = name
                if href:
                    pcItem["href"] = href
                if postcode:
                    pcItem["postcode"] = postcode
                pc_items = getItemWith(self.au_items, url=response.url)
                addedBigArea = False
                for k, v in pc_items.items():
                    if k == "city":
                        pcItem["city"] = pc_items["city"]
                    if k == "bigArea" and addedBigArea == False:
                        pcItem["bigArea"] = pc_items["bigArea"]
                    if k == "area":
                        pcItem["area"] = pc_items["area"]
                    if k == "street":
                        pcItem["streets"] = pc_items["street"]
                        # print("get big area: ",getBigAreaWith(self.au_items, name))
                        big_area = getBigAreaWith(self.au_items, name)
                        if big_area:
                            pcItem["bigArea"] = big_area
                            addedBigArea = True
            yield pcItem
