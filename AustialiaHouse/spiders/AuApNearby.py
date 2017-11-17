# 获取公寓-附近学校

import json

import scrapy
from scrapy import FormRequest

from AustialiaHouse.config.env import IS_DEV
from AustialiaHouse.config.useragent import get_user_agent
from AustialiaHouse.items import AuApartmentNearby


class AuApartmentNearby(scrapy.Spider):
    name = 'apnearby'

    allowed_domains = ["realestate.com.au"]
    start_urls = [
    ]

    def start_requests(self):
        rst = ['https://school-service.realestate.com.au/closest_by_type/?lat=-27.418712615966797&lon=153.05557250976562']
        # rst = ['https://www.realestate.com.au/property-apartment-qld-hamilton-125653546']
        ua = get_user_agent()
        for r in rst:
            url = str(r)
            yield FormRequest(url, callback=self.get_nearby_school, meta={}, headers={'User-Agent': ua})

            if IS_DEV:
                return

    def get_nearby_school(self, response):
        res_nearby = json.loads(response.body)
        nearby = AuApartmentNearby()
        schools = res_nearby["all"]
        # print(type(schools))
        if schools and len(schools)>0:
            nearby['nearby_schools'] = schools
        yield nearby
