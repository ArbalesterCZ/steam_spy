import json
import requests
import re

from email_service import Email
from report_database import ReportDatabase


def extract_item(item):
    result = {'success': False}
    props = item['items'][0]
    if 'url' in props:
        result['url'] = props['url']
        search_number = re.search(r'\d+', result['url'])
        if search_number:
            result['id'] = str(search_number.group())
            url_extend = 'https://store.steampowered.com/api/appdetails?appids=' + result['id']

            result['success'] = json.loads(requests.get(url_extend + '&filters=success').text)[result['id']]['success']
            if result['success']:
                item_price_overview = json.loads(requests.get(url_extend + '&filters=price_overview').text)
                price_overview = item_price_overview[result['id']]['data']['price_overview']
                result['discount'] = price_overview['discount_percent']
                result['price_old'] = price_overview['initial_formatted']
                result['price_new'] = price_overview['final_formatted']

                item_platforms = json.loads(requests.get(url_extend + '&filters=platforms').text)
                platforms = item_platforms[result['id']]['data']['platforms']
                result['win'] = platforms['windows']
                result['mac'] = platforms['mac']
                result['linux'] = platforms['linux']

    return result


def extract_item_special(item):
    result = {'success': True, 'id': str(item['id']), 'name': item['name'], 'preview': item['header_image']}

    if 'apps' in result['preview']:
        result['url'] = 'https://store.steampowered.com/app/' + result['id']
    else:
        result['url'] = 'https://store.steampowered.com/bundle/' + result['id']

    result['win'] = item['windows_available']
    result['mac'] = item['mac_available']
    result['linux'] = item['linux_available']
    result['discount'] = item['discount_percent']
    result['price_old'] = set_value_or_zero_if_not_integer(item['original_price'])
    result['price_new'] = set_value_or_zero_if_not_integer(item['final_price'])

    return result


def set_value_or_zero_if_not_integer(value):
    return value if type(value) is int else 0


class SteamService:
    def __init__(self, min_discount, report_lifespan, report_filepath, sender_email, sender_password):
        self.__data = json.loads(requests.get('https://store.steampowered.com/api/featuredcategories').text)
        self.__email = Email(sender_email, sender_password)
        self.__min_discount = min_discount
        self.__report_database = ReportDatabase(report_filepath)
        self.__report_database.remove_invalid(report_lifespan)

    def proces_message(self, receivers):
        for main_key in self.__data:
            if main_key.isnumeric():
                self.__proces(extract_item, self.__data[main_key])
            elif type(self.__data[main_key]) is dict and 'items' in self.__data[main_key]:
                for item_special in self.__data[main_key]['items']:
                    self.__proces(extract_item_special, item_special)

        if self.__email.send(receivers):
            self.__report_database.save()

    def __proces(self, extract_function, item):
        data = extract_function(item)
        if data['success'] and data['discount'] >= self.__min_discount and not self.__report_database.exist(data['id']):
            self.__email.add_body(data)
            self.__report_database.add(data['id'])
