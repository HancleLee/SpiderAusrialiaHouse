# 澳洲房产项目详情

# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
import re

from AustialiaHouse.config.env import IS_DEV
from AustialiaHouse.config.useragent import get_user_agent
from AustialiaHouse.items import ArticleApartment, AuProjectDetail
from AustialiaHouse.spiders.AuApartmentList import kDomain


class ProjectDetail(scrapy.Spider):
    name = 'prdetail'

    allowed_domains = ["realestate.com.au"]
    start_urls = [
    ]

    def start_requests(self):
        rst = ['https://www.realestate.com.au/project/ascot-green-600009922?propertyTypes=apartments%2Funits,houses&activeSort=child-order']
        ua = get_user_agent()
        for r in rst:
            url = str(r)
            yield FormRequest(url, callback=self.get_detail, meta={} , headers={'User-Agent': ua})

            if IS_DEV:
                return

    def get_detail(self, response):
        auDetail = AuProjectDetail()

        project_media_viewer = response.xpath('.//div[contains(@id, "mediaViewerWrapper")]/div[@class="mediaViewer"]/@data-media').extract_first()

        # 利用正则把所有图片资源提取出来
        pattern = re.compile(r'(https://|http://)(.*?)(.jpg|.png|.jpeg)', re.M)
        match = pattern.findall(project_media_viewer)
        url_media_viewer = ""
        for item in match:
            item_url = ""
            if type(item) == tuple:
                for i in item:
                    item_url = item_url + i.strip()
            if len(item_url) > 0:
                url_media_viewer = url_media_viewer + item_url + ";"
        print("url_media_viewer : ",url_media_viewer)
        urls_list = url_media_viewer.split(";")
        print(len(urls_list))


        project_info = response.xpath('.//div[contains(@class,"project-overview-info")]')

        project_name = project_info.xpath('.//h1[contains(@class, "project-name")]/text()').extract_first()
        project_address = project_info.xpath('.//h2[contains(@class, "project-address")]/text()').extract_first()
        project_title = project_info.xpath('.//div[contains(@class, "project-title")]/text()').extract_first()
        project_price_range = project_info.xpath('.//div[contains(@class, "project-price-range")]/text()').extract_first()
        if project_name and len(project_name):
            auDetail["project_name"] = project_name
        if project_address and len(project_address):
            auDetail["project_address"] = project_address
        if project_title and len(project_title):
            auDetail["project_title"] = project_title
        if project_price_range and len(project_price_range):
            auDetail["project_price_range"] = project_price_range

        project_key_info = response.xpath('.//ul[contains(@class, "project-key-info-list")]/li')
        index_key_info = 0
        for item_key_info in project_key_info:
            pro_key_details = item_key_info.xpath('.//div[contains(@class, "project-key-detail")]/text()').extract()
            pro_key_detail = ""
            for item_pro_key_details in pro_key_details:
                pro_key_detail = pro_key_detail + item_pro_key_details
                if pro_key_detail:
                    if index_key_info == 0:
                        project_location = pro_key_detail  # 项目详细地址
                        auDetail["project_location"] = project_location

                    elif index_key_info == 1:
                        display_location = pro_key_detail  # 展示厅地址
                        auDetail["display_location"] = display_location

                    elif index_key_info == 2:
                        total_size = pro_key_detail  # 房源套数
                        auDetail["total_size"] = total_size

                    elif index_key_info == 3:
                        completion_date = pro_key_detail  # 竣工时间
                        auDetail["completion_date"] = completion_date

            index_key_info += 1
            # print("pro_key_detail : ",pro_key_detail)

        print("project info : \n",project_name, project_address, project_title, project_price_range)

        project_info_descs = response.xpath('.//div[contains(@id, "projectInfo")]/div[@id = "description"]/p[@class = "body"]/span[not(@class= "less")]/text()').extract()
        project_info_desc = ""
        for item_info_descs in project_info_descs:
            project_info_desc = project_info_desc + "\n" + item_info_descs
        print("project_info_desc :", project_info_desc)
        if project_info_desc and len(project_info_desc):
            auDetail["project_info_desc"] = project_info_desc

        project_info_features = response.xpath('.//div[contains(@id, "features")]/ul[@class = "features"]/li/text()').extract()
        project_info_feature = ""
        for item_info_features in project_info_features:
            project_info_feature = project_info_feature + "\n" + item_info_features
        print("project_info_feature :", project_info_feature)
        if project_info_feature and len(project_info_feature):
            auDetail["project_info_feature"] = project_info_feature

        # 房产户型
        pro_apartments = []
        article_matched = response.xpath('.//div[contains(@id, "propertyOptionsForMatchedListing")]/article')
        for item_article in article_matched:
            apartment = ArticleApartment()

            a_photoviewer = item_article.xpath('.//div[@class="photoviewer"]/div/a')
            if len(a_photoviewer) > 0:
                href = item_article.xpath('.//div[@class="photoviewer"]/a/@href').extract_first()
                if href and len(href) > 0:
                    apartment["url"] = kDomain + href
                imgs = ''
                for a_pic in a_photoviewer:
                    imgs = a_pic.xpath('./img/@src').extract_first()
                    imgs = imgs + (";")
                if len(imgs) > 0:
                    apartment["pics"] = imgs
            else:
                pics_div = item_article.xpath('.//div[contains(@class, "viewport")]/div[@class="strip"]/div')
                pics = ''
                href = ""
                for vp in pics_div:
                    href = vp.xpath('.//div[contains(@class, "media")]/a/@href').extract_first()  # 项目href
                    media = vp.xpath('.//div[contains(@class, "media")]//img/@src').extract_first()
                    if type(media) == str:
                        pics = pics + media + ";"
                if type(href) == str and len(href) > 0:
                    apartment["url"] = kDomain + href
                if type(pics) == str and len(pics) > 0:
                    apartment["pics"] = pics

            listing_info = item_article.xpath('.//div[@class="listingInfo"]')
            if listing_info and len(listing_info) <= 0:
                listing_info = item_article.xpath('./div/div[@class="listingInfo"]')
            print(listing_info)

            price = listing_info.xpath('.//div[contains(@class,"propertyStats")]/p/span/text()').extract_first()
            print("price   ", price)
            desc_title = listing_info.xpath('.//a[contains(@class,"title")]/text()').extract_first()
            desc_subtitle = listing_info.xpath('.//p[contains(@class,"description")]/text()').extract_first()
            desc = ""
            if desc_title:
                desc = desc_title
            if desc_subtitle:
                desc = desc + "\n" + desc_subtitle
            if price and len(price) > 0:
                apartment["price"] = price
            if desc and len(desc) > 0:
                apartment["desc"] = desc

            features = listing_info.xpath(
                './/dl[contains(@class,"rui-property-features rui-clearfix")]/dd/text()').extract()
            if features and len(features) >= 3:
                bed = features[0]
                bath = features[1]
                car = features[2]
                if len(bed) > 0:
                    apartment["bed"] = bed
                if len(bath) > 0:
                    apartment["bath"] = bath
                if len(car) > 0:
                    apartment["car"] = car
                    # print(bed, bath, car)

            if apartment:
                pro_apartments.append(apartment)

            print("item_articless  ",apartment)
        if pro_apartments:
            auDetail["pro_apartments"] = pro_apartments

        yield auDetail