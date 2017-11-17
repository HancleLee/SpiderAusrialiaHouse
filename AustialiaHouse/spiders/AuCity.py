# 澳洲房产-城市(邮编)
import re

import scrapy
import xlrd
from scrapy import FormRequest

from AustialiaHouse.Helper.CityHelper import au_area_url, kCityDomain, getItemWith, getBigAreaWith
from AustialiaHouse.config.env import IS_DEV
from AustialiaHouse.items import Postcode


# 初始化地区信息对象
# au_items = au_area_url()
class City(scrapy.Spider):
    name = 'postcode'

    # start_urls = [
    # ]
    start_urls = [
    ]
    allowed_domains = ["geopostcodes.com"]

    au_items = au_area_url()

    def start_requests(self):
        pc_urls = []
        for it in self.au_items:
            url = it["area_url"]
            if len(url) > 0:
                pc_urls.append(url)

                # http://www.geopostcodes.com/browse.php?t=2&n=50&id=AU050708&l=0
                # http://www.geopostcodes.com/browse.php?t=2&n=50&id=AU050701&l=0
                # http://www.geopostcodes.com/browse.php?t=2&n=100&id=AU050701&l=0

                yield FormRequest("http://www.geopostcodes.com/Brisbane", callback=self.get_list)

            if IS_DEV:
                return

    def get_list(self, response):

        pcItem = Postcode()

        target = response.xpath('//table[@id="browser"]')
        table_list = target.xpath('//table[@class="list2"]')
        tr_items = table_list.xpath('//tr[@itemscope]')
        # 获取下一页的数据
        tr_next_list = table_list.xpath('.//tr[contains(@class, "nextlist")]/td/@onclick').extract_first()
        r = re.compile(r'".*"')
        r_result = r.findall(tr_next_list)
        href = ""
        if r_result and len(r_result) > 0:
            try:
                href = r_result[0].strip('"')
            except (IOError, AttributeError) as e:
                print(e)
        if len(href)>0:
            href = kCityDomain + "/browse.php?" + href
            yield FormRequest(href, callback=self.get_next_list)

        for tr_item in tr_items:
            # print("tritem", tr_item.extract())
            tr_item_list = tr_item.xpath('./td')
            if len(tr_item_list)>3:
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
                    if k=="city":
                        pcItem["city"] = pc_items["city"]
                    if k=="bigArea" and addedBigArea==False:
                        pcItem["bigArea"] = pc_items["bigArea"]
                    if k=="area":
                        pcItem["area"] = pc_items["area"]
                    if k=="street":
                        pcItem["streets"] = pc_items["street"]
                        # print("get big area: ",getBigAreaWith(self.au_items, name))
                        big_area = getBigAreaWith(self.au_items, name)
                        if big_area:
                            pcItem["bigArea"] = big_area
                            addedBigArea = True
            yield pcItem

    def get_next_list(self, response):
        pcItem = Postcode()

        tr_items = response.xpath('.//tr[@itemscope]')
        # 获取下一页的数据
        tr_next_list = response.xpath('.//tr[contains(@class, "nextlist")]/td/@onclick').extract_first()
        if tr_next_list:
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
                yield FormRequest(href, callback=self.get_next_list)

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