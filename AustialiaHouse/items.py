# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AustialiahouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 邮编对象（城市-大区域-城区-区域-街道）
class Postcode(scrapy.Item):
    street = scrapy.Field()     # 街道名称
    postcode = scrapy.Field()   # 区域邮编
    href = scrapy.Field()       # 区域下面的街道链接，可能为空
    city = scrapy.Field()       # 城市
    bigArea = scrapy.Field()    # 大区域
    area = scrapy.Field()       # 城区
    streets = scrapy.Field()    # 文档里区域对应的街道，蒋b划分的


# 列表中的公寓信息
class ArticleApartment(scrapy.Item):
    url = scrapy.Field()    # 公寓详情URL
    pics = scrapy.Field()   # 图片，以'；'隔开
    price = scrapy.Field()  # 价格
    desc = scrapy.Field()   # 描述（有些包含地址信息）
    bed = scrapy.Field()    # 卧室
    bath = scrapy.Field()   # 浴室
    car = scrapy.Field()    # 车库

# 列表中的项目信息
class ArticleProject(scrapy.Item):
    pro_url = scrapy.Field()        # 项目详情URL
    pro_title = scrapy.Field()      # 项目标题
    pro_address = scrapy.Field()    # 项目地址
    pro_pics = scrapy.Field()       # 项目图片，以'；'隔开
    pro_apartments = scrapy.Field(serializer=list)  # 项目下面的公寓信息

# 澳洲房产列表（项目or公寓，每个article只存在一个）
class Article(scrapy.Item):
    project = scrapy.Field(serializer=ArticleProject)     # 项目信息
    apartment = scrapy.Field(serializer=ArticleApartment) # 公寓信息


class AuProjectDetail(scrapy.Item):
    project_name = scrapy.Field()           # 项目名称
    project_address = scrapy.Field()        # 项目地址
    project_title = scrapy.Field()          # 项目标题
    project_price_range = scrapy.Field()    # 项目价格区间
    pics = scrapy.Field()                   # 项目图片，以"；"分割
    project_location = scrapy.Field()       # 项目详细地址
    display_location = scrapy.Field()       # 展示厅位置
    total_size = scrapy.Field()             # 房源套数
    completion_date = scrapy.Field()        # 竣工时间
    project_info_desc = scrapy.Field()      # 项目介绍
    project_info_feature = scrapy.Field()   # 项目特性
    pro_apartments = scrapy.Field(serializer=list)  # 项目下面的公寓信息


class AuApartmentDetail(scrapy.Item):
    pics = scrapy.Field()           # 图片
    address = scrapy.Field()        # 地址
    bed = scrapy.Field()            # 卧室
    bath = scrapy.Field()           # 浴室
    car = scrapy.Field()            # 车库
    property_type = scrapy.Field()  # 房屋类型
    price = scrapy.Field()          # 价格
    f_desc_address = scrapy.Field() # 特性-详细地址
    f_desc_title = scrapy.Field()   # 特性-房产介绍标题
    f_desc_body = scrapy.Field()    # 特性-房产介绍内容
    f_indoor = scrapy.Field()       # 特性-室内功能
    f_outdoor = scrapy.Field()      # 特性-室外功能
    f_type = scrapy.Field()         # 特性-房产类型
    f_bed = scrapy.Field()          # 特性-卧室
    f_bath = scrapy.Field()         # 特性-浴室
    f_car = scrapy.Field()          # 特性-车库
    f_land_size = scrapy.Field()    # 特性-建筑面积
    href_floorplan = scrapy.Field() # 户型平面图的数据链接
    href_school = scrapy.Field()    # 周边学校的数据链接

class AuApartmentNearby(scrapy.Item):
    nearby_schools = scrapy.Field(serializer=list)  # 公寓-附近的学校

class AuApartmentFloorplan(scrapy.Item):
    floorplan = scrapy.Field(serializer=list)  # 公寓-平面图

class AuApInvest(scrapy.Item):
    investor_metrics = scrapy.Field(serializer=list)  # 地区投资数据
    investor_suggestion = scrapy.Field()              # 地区投资数据的说明

class AuApartmentPopulation(scrapy.Item):
    population = scrapy.Field(serializer=list)  # 公寓-地区人口组成