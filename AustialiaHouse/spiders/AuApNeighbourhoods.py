# 公寓详情->地区人口组成

import scrapy
from scrapy import FormRequest

from AustialiaHouse.config.env import IS_DEV
from AustialiaHouse.config.useragent import get_user_agent
from AustialiaHouse.items import AuApartmentPopulation


class AuApartmentNeighbourhoods(scrapy.Spider):
    name = 'apneighbourhood'

    allowed_domains = ["realestate.com.au"]
    start_urls = [
    ]

    def start_requests(self):
        rst = ['https://www.realestate.com.au/neighbourhoods/hamilton-4007-qld']
        # rst = ['https://www.realestate.com.au/property-apartment-qld-hamilton-125653546']
        ua = get_user_agent()
        for r in rst:
            url = str(r)
            yield FormRequest(url, callback=self.get_neighbourhoods, meta={}, headers={'User-Agent': ua})

            if IS_DEV:
                return

    def get_neighbourhoods(self, response):
        ap_population = AuApartmentPopulation()

        life_stage = response.xpath('.//div[contains(@id, "life-stage")]/div/div[@class="slide-content"]')
        populations = life_stage.xpath('.//div[contains(@class, "details-container desktop")]/div[@class="row"]')
        population = []
        for item_population in populations:
            p_dic = {}
            p_percentage = item_population.xpath('.//div[contains(@class, "percentage")]/text()').extract_first()
            p_label = item_population.xpath('.//div[contains(@class, "label")]/text()').extract_first()
            # print(p_percentage, p_label)
            if p_percentage and p_label and  len(p_percentage)>0 and len(p_label)>0:
                p_dic["percentage"] = p_percentage
                p_dic["label"] = p_label
            if len(p_dic) > 0:
                population.append(p_dic)

        if len(population)>0:
            ap_population["population"] = population

        yield ap_population
