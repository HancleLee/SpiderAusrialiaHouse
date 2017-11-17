# 澳洲房产公寓详情

# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import FormRequest
import re

from AustialiaHouse.config.env import IS_DEV
from AustialiaHouse.config.useragent import get_user_agent
from AustialiaHouse.items import ArticleApartment, AuProjectDetail, AuApartmentDetail
from AustialiaHouse.spiders.AuApartmentList import kDomain


class ProjectDetail(scrapy.Spider):
    name = 'apdetail'

    allowed_domains = ["realestate.com.au"]
    start_urls = [
    ]

    def start_requests(self):
        rst = ['https://www.realestate.com.au/property-house-qld-clayfield-126887590']
        # rst = ['https://www.realestate.com.au/property-apartment-qld-hamilton-125653546']
        ua = get_user_agent()
        for r in rst:
            url = str(r)
            yield FormRequest(url, callback=self.get_detail, meta={} , headers={'User-Agent': ua})

            if IS_DEV:
                return

    def get_detail(self, response):
        ap_detail = AuApartmentDetail()

        scripts = response.xpath('.//script[contains(@type, "text/javascript")]').extract()
        pics = []
        for script in scripts:
            script = script.replace(" ", "")

            # 利用正则把所有图片资源提取出来
            pattern = re.compile(r'LMI.Data.listings=(.*?);', re.M)
            match = pattern.findall(script)
            for item in match:
                # print("item  ",item)
                # print(type(item), type(match))
                item = item.replace(" ", "")
                photos_pattern = re.compile(r'photos:\[(.*?)\],', re.M)
                photos_match = photos_pattern.findall(item)
                for photos_i in photos_match:
                    photos = photos_i.split('{src:"')
                    phs = []
                    for ph in photos:
                        if ph:
                            photo = str(ph).split('",title')[0].replace(" ", "")
                            if len(photo) > 0:
                                phs.append(kDomain + photo)
                    if len(phs)>0:
                        pics = phs
        # print(pics)
        ap_detail["pics"] = pics

        base_info = response.xpath('.//div[contains(@class, "base-info")]')
        listing_address = base_info.xpath('.//div[contains(@id, "listing_address")]//span/text()').extract()
        address = ""
        for item_listing_addr in listing_address:
            address = address + item_listing_addr + " "
        # print(address)
        ap_detail["address"] = address

        listing_info = base_info.xpath('.//div[contains(@id, "listing_info")]/ul[@class="info"]')
        features = listing_info.xpath('.//li[contains(@class, "property_info")]/dl/dd/text()').extract()
        for item_features in features:
            bed = features[0]
            bath = features[1]
            car = features[2]
            if len(bed) > 0:
                ap_detail["bed"] = bed
            if len(bath) > 0:
                ap_detail["bath"] = bath
            if len(car) > 0:
                ap_detail["car"] = car

        property_type = listing_info.xpath('.//li[contains(@class, "property_info")]/span/text()').extract_first()
        price = listing_info.xpath('.//li[contains(@class, "price")]/p/text()').extract_first()
        # print(property_type,price)
        if len(property_type) > 0:
            ap_detail["property_type"] = property_type
        if len(price) > 0:
            ap_detail["price"] = price

        details_cont = response.xpath('.//div[contains(@id, "detailsCont")]/div[@id="primaryContent"]')
        description = details_cont.xpath('.//div[contains(@id, "description")]')
        desc_address = description.xpath('.//h3[contains(@class, "address")]/text()').extract_first()
        desc_title = description.xpath('.//p[contains(@class, "title")]/text()').extract_first()
        desc_bodys = description.xpath('.//p[contains(@class, "body")]/text()').extract()
        desc_body = ""
        for item_desc_bodys in desc_bodys:
            desc_body = desc_body + item_desc_bodys + "\n"
        # print(desc_address, desc_title, desc_body)
        if len(desc_address) > 0:
            ap_detail["f_desc_address"] = desc_address
        if len(desc_title) > 0:
            ap_detail["f_desc_title"] = desc_title
        if len(desc_body) > 0:
            ap_detail["f_desc_body"] = desc_body

        detail_features = details_cont.xpath('.//div[contains(@id, "features")]/div[@class="featureListWrapper"]/div[@class="featureList"]/ul')
        print('detail_features :',detail_features)
        f_indoor = ""
        f_outdoor = ""
        f_type = ""
        f_bed = ""
        f_bath = ""
        f_car = ""
        f_land_size = ""
        for item_detail_features in detail_features:
            feature_header = item_detail_features.xpath('.//li[contains(@class, "header")]/text()').extract_first()
            print(feature_header)

            detail_feature_list = item_detail_features.xpath('.//li[not(@class)]')
            # print('item_detail_features',detail_feature_list.extract())

            if "indoor" in feature_header.lower() or "outdoor" in feature_header.lower():
                feature_detail_str = ""
                for item_d_f_list in detail_feature_list:
                    feature_detail = item_d_f_list.xpath('.//text()').extract()
                    for item_feature_detail in feature_detail:
                        print(item_feature_detail)
                        feature_detail_str = feature_detail_str + item_feature_detail
                    feature_detail_str = feature_detail_str + ","
                if "indoor" in feature_header.lower():
                    f_indoor = feature_detail_str.strip(",")
                elif "outdoor" in feature_header.lower():
                    f_outdoor = feature_detail_str.strip(",")

            elif "general features" in feature_header.lower():
                for item_d_f_list in detail_feature_list:
                    feature_detail = item_d_f_list.xpath('.//text()').extract()
                    if len(feature_detail) == 2:
                        feature_detail0 = feature_detail[0]
                        feature_detail1 = feature_detail[1]
                        if "property type" in feature_detail0.lower():
                            f_type = feature_detail1
                        if "bedroom" in feature_detail0.lower():
                            f_bed = feature_detail1
                        if "bathroom" in feature_detail0.lower():
                            f_bath = feature_detail1
                        if "size" in feature_detail0.lower():
                            f_land_size = feature_detail1
                        if "car" in feature_detail0.lower():
                            f_car = feature_detail1

        href_floorplan = ""
        href_floorplans = details_cont.xpath('.//div[contains(@id, "floorplans")]/ul/li[@class="floorplan"]/a/@href').extract_first()
        if href_floorplans:
            href_floorplan = kDomain +href_floorplans
        # print("feartures : ",f_indoor, f_outdoor,f_type, f_bed, f_bath, f_land_size, f_car, href_floorplan)

        school_info = details_cont.xpath('.//div[contains(@id, "schoolInfo")]/div[@class="rui-school-information"]')
        school_lon = school_info.xpath('./@data-longitude').extract_first()
        school_lat = school_info.xpath('./@data-latitude').extract_first()
        href_school = "https://school-service.realestate.com.au/closest_by_type/?lat=" + school_lat+"&lon=" + school_lon

        if len(f_indoor) > 0:
            ap_detail["f_indoor"] = f_indoor
        if len(f_outdoor) > 0:
            ap_detail["f_outdoor"] = f_outdoor
        if len(f_type) > 0:
            ap_detail["f_type"] = f_type
        if len(f_bed) > 0:
            ap_detail["f_bed"] = f_bed
        if len(f_bath) > 0:
            ap_detail["f_bath"] = f_bath
        if len(f_car) > 0:
            ap_detail["f_car"] = f_car
        if len(f_land_size) > 0:
            ap_detail["f_land_size"] = f_land_size
        if len(href_floorplan) > 0:
            ap_detail["href_floorplan"] = href_floorplan
        if len(href_school) > 0:
            ap_detail["href_school"] = href_school

        # print('school_info_selected ',school_lon, school_lat, school_info.extract_first())

        yield ap_detail



