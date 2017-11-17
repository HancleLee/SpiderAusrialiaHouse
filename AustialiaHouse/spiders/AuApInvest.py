# 获取公寓-地区情况

import json
import re

import scrapy
from scrapy import FormRequest

from AustialiaHouse.config.env import IS_DEV
from AustialiaHouse.config.useragent import get_user_agent
from AustialiaHouse.items import AuApInvest


class AuApartmentInvest(scrapy.Spider):
    name = 'apinvest'

    allowed_domains = ["realestate.com.au"]
    start_urls = [
    ]

    type = ""
    addr = ""
    state = ""
    code = ""

    def start_requests(self):
        # rst = ['/invest/4-bed-house-in-millers+point,+nsw+2000?pid=investor:source:pdp:buy']
        rst = ['/invest/2-bed-unit-in-hamilton,+qld+4007?pid=investor:source:pdp:buy', '/invest/1-bed-unit-in-the+rocks,+nsw+2000?pid=investor:source:pdp:buy']

        ua = get_user_agent()
        for r in rst:
            url = str(r)

            type_match = re.findall(r'bed-.*?-in', url, re.M | re.I)
            if type_match and len(type_match)>0:
                self.type = type_match[0].split('-')[1]
                print("matchObj.group() : ", self.type)

            else:
                print("No match!!")

            addr_match = re.findall(r'in-.*?,', url, re.M | re.I)
            if addr_match and len(addr_match) > 0:
                self.addr = addr_match[0].split('-')[1].strip(",")
                if "+" in self.addr:
                    address = self.addr.split("+")
                    self.addr = ""
                    index_addr = 0
                    while index_addr < len(address):
                        item_address = address[index_addr]
                        self.addr = self.addr + item_address
                        if index_addr < len(address) - 1:
                            self.addr = self.addr + " "
                        index_addr = index_addr + 1
                print("matchObj.group() : ", self.addr)

            else:
                print("No match!!")

            state_match = re.findall(r',\+.*?\+', url, re.M | re.I)
            if state_match and len(state_match) > 0:
                self.state = state_match[0].split('+')[1]
                print("matchObj.group() : ", self.state)

            else:
                print("No match!!")

            code_match = re.findall(r'\d+\?', url, re.M | re.I)
            if code_match and len(code_match) > 0:
                self.code = code_match[0].split('?')[0]
                print("matchObj.group() : ", self.code)

            else:
                print("No match!!")

            if len(self.type)>0 and len(self.addr)>0 and len(self.state)>0 and len(self.code)>0:
                redirect_url = 'https://investor-api.realestate.com.au/states/' + self.state.upper() + '/suburbs/' + self.addr.upper() + '/postcodes/' + self.code + '.json'
                yield FormRequest(redirect_url, callback=self.get_invest, meta={}, headers={'User-Agent': ua})

            # if IS_DEV:
            #     return

    def get_invest(self, response):
        ap_invest = AuApInvest()
        try:
            res_invest = json.loads(response.body)

            data_key = self.addr.upper() + '-' + self.code
            data_dic = res_invest[str(data_key)]
            property_types = data_dic["property_types"]
            investor_metrics_all = {}
            if "HOUSE" in self.type.upper():  # house
                houses = property_types["HOUSE"]
                bedrooms = houses["bedrooms"]
                bed_all = bedrooms["ALL"]
                investor_metrics_all = bed_all["investor_metrics"]

            else:  # unit
                units = property_types["UNIT"]
                bedrooms = units["bedrooms"]
                bed_all = bedrooms["ALL"]
                investor_metrics_all = bed_all["investor_metrics"]

            ap_invest["investor_metrics"] = investor_metrics_all
            annual_growth = investor_metrics_all["annual_growth"]
            # median_rental_price = investor_metrics_all["median_rental_price"]
            median_sold_price = investor_metrics_all["median_sold_price"]
            median_sold_price_five_years_ago = investor_metrics_all["median_sold_price_five_years_ago"]
            # rental_demand = investor_metrics_all["rental_demand"]
            rental_properties = investor_metrics_all["rental_properties"]
            rental_yield = investor_metrics_all["rental_yield"]
            sold_properties = investor_metrics_all["sold_properties"]
            # sold_properties_five_years_ago = investor_metrics_all["sold_properties_five_years_ago"]

            inscrease_rate = str('%.1f%%' % (((median_sold_price / median_sold_price_five_years_ago) - 1) * 100))
            annual_growth_rate = str('%.1f%%' % (annual_growth * 100))
            rental_yield_rate = str('%.1f%%' % (rental_yield * 100))

            # 地区情况说明
            suggestion = "The median sales price for " + self.type.lower() + "s in " \
                         + self.addr.capitalize() + ", " + self.state.upper() + " in the last year was $" + str(int(median_sold_price))\
                         + " based on " + str(sold_properties) + " home sales.Compared to the same period five years ago,the median "\
                         + self.type.lower() + " sales price for " + self.type.lower() + "s increased " + inscrease_rate \
                         + " which equates to a compound annual growth rate of " + annual_growth_rate + ". \n" \
                         + "The rental yield for " + self.type.lower() + "s in "+ self.addr.capitalize() + ", " + self.state.upper() \
                         + " was " + rental_yield_rate + " based on " + str(rental_properties) + " property rentals and "\
                         + str(sold_properties) + " property sales over the preceding 12 months."
            ap_invest["investor_suggestion"] = suggestion
            # print(suggestion)


        except (IOError, KeyError) as e:
            print(e)

        yield ap_invest
