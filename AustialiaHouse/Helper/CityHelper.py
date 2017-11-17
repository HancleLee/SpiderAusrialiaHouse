# 获取地区名称和链接等

import xlrd

kCityDomain = "http://www.geopostcodes.com"

def au_area_url():
    house_type_data = xlrd.open_workbook(
        '/Users/qicheng/AustialiaHouse/AustialiaHouse/Files/austrialia_house_type.xlsx')
    table = house_type_data.sheets()[0]  # 通过索引顺序获取
    nrows = table.nrows

    result = []
    big_area=""
    city = ""
    for i in range(nrows):
        postcode_item = {}
        row_val_list = table.row_values(i)
        if (i >= 1 and len(row_val_list) > 5):
            # print("row_val_list", row_val_list)
            city_name = row_val_list[0].strip()
            big_area_name = row_val_list[1].strip()
            area_name = row_val_list[2].strip()
            street_name = row_val_list[4].strip()
            # 去掉' and'，将' '替换成'-'，可拼接url，如http://www.geopostcodes.com/Greater_Dandenong
            url_name = area_name.replace(" and", "").replace(" ","_")
            url = kCityDomain + "/"+url_name
            # print(url,"\n")
            if len(city_name) > 0:
                city = city_name
            if len(big_area_name)>0:
                big_area = big_area_name
            if len(city)>0:
                postcode_item["city"] = city
            if len(big_area)>0:
                postcode_item["bigArea"] = big_area
            if len(area_name)>0:
                postcode_item["area"] = area_name
                postcode_item["area_url"] = url
            if len(street_name)>0:
                postcode_item["street"] = street_name
            if len(postcode_item)>0:
                result.append(postcode_item)

    return result

# 根据url来获取地区信息对象
def getItemWith(items, url):
    for it in items:
        it_url = it["area_url"]
        if len(it_url) > 0 and it_url == url:
            return it
    return {}

# 根据街道名来匹配大区域,返回大区域
def getBigAreaWith(items, street):
    for it in items:
        it_street = False
        it_bigarea = False
        for k, v in it.items():
            if k == "street":
                it_street = it["street"]
            if k == "bigArea":
                it_bigarea = it["bigArea"]
        if it_street and len(it_street)>0:
            streets = it_street.split(",")
            # print(street, streets)
            for st in streets:
                # 大写字母转成小写字母，并去除空格 再做比较
                st = st.lower().replace(" ","")
                street = street.lower().replace(" ","")
                if street == st:
                    return it_bigarea
    return False