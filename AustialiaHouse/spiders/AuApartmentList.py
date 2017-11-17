#  获取澳洲房产列表

# -*- coding: utf-8 -*-

import scrapy
from scrapy import FormRequest

from AustialiaHouse.config.env import IS_DEV
from AustialiaHouse.config.useragent import get_user_agent
from AustialiaHouse.items import Article, ArticleApartment, ArticleProject

kDomain = "https://www.realestate.com.au"

class ApartmentList(scrapy.Spider):
    name = "apartmentlist"

    allowed_domains = ["realestate.com.au"]
    start_urls = [
    ]
    data_url = "https://www.realestate.com.au/buy/property-unitblock-villa-townhouse-unit+apartment-house-in-"

    def start_requests(self):
        rst = ['4011']
        ua = get_user_agent()
        # ck = "reauid=1cf37468112700009dff035a290000001d541700; _hjIncludedInSample=1; s_nr=1510211664299; NSC_mch-fry=ffffffffaf11261945525d5f4f58455e445a4a423660; lmdstok=aWQjMmM5OWI4ODg1ZjcwZWNlNjAxNWZhNGNkMjFhNzZmMWE6MzY1Nzc4MjA3NDgxODpmZDExYzI4ZWU3ZmM3MmFlNTE2NDIyYmYxYTlhNjViYQ; utag_main=v_id:015fa4d01995001652c761631ceb04079005907100bd0$_sn:1$_ss:0$_st:1510300440427$ses_id:1510298622359%3Bexp-session$_pn:4%3Bexp-session$vapi_domain:realestate.com.au; _sp_id.2fe7=cfe58a2c-6cb4-4a8b-b022-c3e3c6ae5464.1510298624.1.1510298640.1510298624.e89b9d7a-33eb-4a68-8c3e-63a1bdc01c52; QSI_HistorySession=https%3A%2F%2Fwww.realestate.com.au%2Fbuy%2Fin-5035%2Flist-1%3Fsource%3Dlocation-search~1510542735615%7Chttps%3A%2F%2Fwww.realestate.com.au%2Fbuy%2Fproperty-unitblock-villa-townhouse-unit%2Bapartment-house-in-5035%2Flist-1%3FnewOrEstablished%3Dnew%26source%3Dlocation-search~1510543694676%7Chttps%3A%2F%2Fwww.realestate.com.au%2Fbuy%2Fproperty-unitblock-villa-townhouse-unit%2Bapartment-house-in-4011%2Flist-1%3FnewOrEstablished%3Dnew%26source%3Dlocation-search~1510623940804; JSESSIONID=FFA6AF9D6684EA671095AE07E6410233; _readc=EQX; _stc=typedBookmarked; External=%2FPUBMATIC%3D60576AD1-434E-41F9-A5C3-EEF2121C8866%2FRUBICON%3DJ2TW1ROL-Z-1I7Y%2F_EXP%3D1542161399%2F_exp%3D1542161432; VT_LANG=language%3Dzh-CN; s_cc=true; s_fid=5A31B76D4BE9324A-298908167D40BB09; s_sq=%5B%5BB%5D%5D; s_vi=[CS]v1|2D01FFD30503436F-60001188C00006B1[CE]; mid=8085025707731574106; Hint=apse2e8"
        for r in rst:
            url = self.data_url + str(r) + "/list-1?newOrEstablished=new&source=location-search"
            yield FormRequest(url, callback=self.get_list, meta={} , headers={'User-Agent': ua})

            if IS_DEV:
                return

    def get_list(self, response):
        target = response.xpath('//div[@id="DSContents"]/div[@id="results"]')
        article_list = target.xpath('./div[@id="searchResultsTbl"]/article')
        print(len(article_list), ' len')
        for ar in article_list:
            article = Article()
            article_type = ar.xpath('./@data-content-type').extract_first()

            # ----------------------------项目-------------------------------------
            if "new apartment project" in article_type: # 新公寓项目 data-content-type="new apartment project"
                project = ArticleProject()
                print("new apartment project")
                viewport = ar.xpath('.//div[contains(@class, "viewport")]/div[@class="strip"]/div')
                pics = ''
                for vp in viewport:
                    pro_href = vp.xpath('.//div[contains(@class, "media")]/a/@href').extract_first() # 项目href
                    media = vp.xpath('.//div[contains(@class, "media")]//img/@src').extract_first()
                    if type(media)==str:
                        pics = pics + media + ";"
                if type(pro_href)==str and len(pro_href)>0:
                    project["pro_url"] = kDomain + pro_href
                if type(pics)==str and len(pics)>0:
                    project["pro_pics"] = pics
                # print("picssss ", pics)

                listing_info = ar.xpath('.//div[@class="listingInfo rui-clearfix"]')
                title = listing_info.xpath('.//h3[contains(@class, "title")]/text()').extract_first()
                address = listing_info.xpath('.//div[contains(@class,"vcard")]/h2/a/text()').extract_first()
                if len(title)>0:
                    project["pro_title"] = title
                if len(address)>0:
                    project["pro_address"] = address

                apartment_list = ar.xpath('.//div[contains(@class, "project-child-listings")]/a')
                print(len(apartment_list))
                pro_apas = []
                for pro_apartment in apartment_list:
                    pro_apa = ArticleApartment()
                    apa_href = pro_apartment.xpath('./@href').extract_first()
                    if len(apa_href)>0:
                        pro_apa["url"] = kDomain + apa_href

                    apa_pic = pro_apartment.xpath('.//div[contains(@class, "propertyImage")]/img/@src').extract_first()
                    apa_price = pro_apartment.xpath('.//div[contains(@class, "priceAndPropertyTypeContainer")]/span[@class="price rui-truncate"]/text()').extract_first()
                    apa_desc = pro_apartment.xpath('.//div[contains(@class, "priceAndPropertyTypeContainer")]/span[@class="propertyType rui-truncate"]/text()').extract_first()
                    if len(apa_pic)>0:
                        pro_apa["pics"] = apa_pic
                    if len(apa_price)>0:
                        pro_apa["price"] = apa_price
                    if len(apa_desc)>0:
                        pro_apa["desc"] = apa_desc

                    apa_feature = pro_apartment.xpath('.//div[contains(@class, "features")]/*/dd/text()').extract()
                    if len(apa_feature) >= 3:
                        apa_bed = apa_feature[0]
                        apa_bath = apa_feature[1]
                        apa_car = apa_feature[2]
                        # print(apa_pic, apa_price, apa_desc,"\n",apa_bed, apa_bath, apa_car)
                        if len(apa_bed)>0:
                            pro_apa["bed"] = apa_bed
                        if len(apa_bath)>0:
                            pro_apa["bath"] = apa_bath
                        if len(apa_car)>0:
                            pro_apa["car"] = apa_car
                    if len(pro_apa)>0:
                        pro_apas.append(pro_apa)

                if len(pro_apas)>0:
                    project["pro_apartments"] = pro_apas

                if len(project) > 0:
                    article["project"] = project

            #-----------------------------公寓------------------------------------
            else :   #  data-content-type='residential' or 'house land package'
                apartment = ArticleApartment()

                print("not new apartment project")
                a_photoviewer = ar.xpath('.//div[@class="photoviewer"]/a')
                if len(a_photoviewer)>0:
                    href = ar.xpath('.//div[@class="photoviewer"]/a/@href').extract_first()
                    if href and len(href) > 0:
                        apartment["url"] = kDomain + href
                    imgs = ''
                    for a_pic in a_photoviewer:
                        imgs = a_pic.xpath('./img/@src').extract_first()
                        imgs = imgs + (";")
                    if len(imgs) > 0:
                        apartment["pics"] = imgs
                else:
                    pics_div = ar.xpath('.//div[contains(@class, "viewport")]/div[@class="strip"]/div')
                    pics = ''
                    for vp in pics_div:
                        href = vp.xpath('.//div[contains(@class, "media")]/a/@href').extract_first()  # 项目href
                        media = vp.xpath('.//div[contains(@class, "media")]//img/@src').extract_first()
                        if type(media) == str:
                            pics = pics + media + ";"
                    if type(href) == str and len(href) > 0:
                        apartment["url"] = kDomain + href
                    if type(pics) == str and len(pics) > 0:
                        apartment["pics"] = pics

                listing_info = ar.xpath('.//div[@class="listingInfo rui-clearfix"]')
                if len(listing_info) <= 0:
                    listing_info = ar.xpath('./div/div[@class="listingInfo rui-clearfix"]')
                # print(listing_info)

                price = listing_info.xpath('.//div[contains(@class,"propertyStats")]/p/text()').extract_first()
                desc = listing_info.xpath('.//h2[contains(@class,"rui-truncate")]/text()').extract_first()
                if desc == None:
                    desc = listing_info.xpath('./div/h2[contains(@class,"rui-truncate")]/a/text()').extract_first()
                if len(price) > 0:
                    apartment["price"] = price
                if len(desc) > 0:
                    apartment["desc"] = desc

                features = listing_info.xpath('.//dl[contains(@class,"rui-property-features rui-clearfix")]/dd/text()').extract()
                if len(features)>=3:
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

                if len(apartment) > 0:
                    article["apartment"] = apartment

            yield article

