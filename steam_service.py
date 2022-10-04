import json
import requests

from email_service import Email
from report_database import ReportDatabase


def extract_item(item):
    item_url = ''
    price_discount = -1
    price_original = -1
    price_final = -1
    props = item['items'][0]

    if 'url' in props:
        item_url = props['url']
        item_id = item_url.replace('https://store.steampowered.com/app/', '')

        if item_id.isnumeric():
            details_url = 'https://store.steampowered.com/api/appdetails?appids=' + item_id + '&filters=price_overview'
            overview = json.loads(requests.get(details_url).text)
            price_overview = overview[item_id]['data']['price_overview']
            price_discount = price_overview['discount_percent']
            price_original = price_overview['initial_formatted']
            price_final = price_overview['final_formatted']

    return props['name'], props['header_image'], item_url, price_discount, price_original, price_final


def extract_item_special(item):
    app_url = 'https://store.steampowered.com/app/' + str(item['id'])
    price_original = str(item['original_price'] / 100.0) + '€'
    price_final = str(item['final_price'] / 100.0) + '€'

    return item['name'], item['header_image'], app_url, item['discount_percent'], price_original, price_final


class SteamService:
    def __init__(self, min_discount, report_lifespan, report_filepath, sender_email, sender_pass, receivers):
        self.__data = json.loads(requests.get('https://store.steampowered.com/api/featuredcategories').text)
        self.__email = Email(sender_email, sender_pass, receivers)
        self.__min_discount = min_discount
        self.__report_database = ReportDatabase(report_filepath)
        self.__report_database.clear_old(report_lifespan)

    def proces_message(self):
        i = 0
        while str(i) in self.__data:
            self.__proces(extract_item, self.__data[str(i)])
            i += 1

        for special_item in self.__data['specials']['items']:
            self.__proces(extract_item_special, special_item)

        self.__email.send()

    def __proces(self, extract_function, item):
        title, image, url, discount, original_price, final_price = extract_function(item)
        app_id = url.replace('https://store.steampowered.com/app/', '')
        if discount >= self.__min_discount and not self.__report_database.exist(app_id):
            self.__email.add_body(title, image, url, discount, original_price, final_price)
            self.__report_database.add(app_id)
