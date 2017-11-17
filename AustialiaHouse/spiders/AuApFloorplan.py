# 获取公寓-平面图

import json

import scrapy
from scrapy import FormRequest

from AustialiaHouse.config.env import IS_DEV
from AustialiaHouse.config.useragent import get_user_agent
from AustialiaHouse.items import AuApartmentFloorplan


class AuApartmentFloorplan(scrapy.Spider):
    name = 'apfloorplan'

    allowed_domains = ["realestate.com.au"]
    start_urls = [
    ]

    def start_requests(self):
        rst = ['https://www.realestate.com.au/floorplan_new.ds?id=125653546&theme=rea.buy']
        # rst = ['https://www.realestate.com.au/property-apartment-qld-hamilton-125653546']
        ua = get_user_agent()
        for r in rst:
            url = str(r)
            yield FormRequest(url, callback=self.get_floorplan, meta={}, headers={'User-Agent': ua})

            if IS_DEV:
                return

    def get_floorplan(self, response):
        ap_floor = AuApartmentFloorplan()
        media_viewer = response.xpath('.//div[contains(@class, "mediaViewer platinum")]/@data-media').extract_first()
        floorplan = json.loads(media_viewer)
        if floorplan and len(floorplan) > 0:
            ap_floor.floorplan = floorplan
        yield ap_floor
