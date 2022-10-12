import json
import requests

from email_service import Email
from report_database import ReportDatabase


def extract_item(item):
    item_url = ''
    price_discount, price_old, price_new = -1, -1, -1
    win, mac, linux = False, False, False

    props = item['items'][0]

    if 'url' in props:
        item_url = props['url']
        item_id = item_url.replace('https://store.steampowered.com/app/', '')

        if item_id.isnumeric():
            details_url = 'https://store.steampowered.com/api/appdetails?appids=' + item_id

            item_price_overview = json.loads(requests.get(details_url + '&filters=price_overview').text)
            price_overview = item_price_overview[item_id]['data']['price_overview']
            price_discount = price_overview['discount_percent']
            price_old = price_overview['initial_formatted']
            price_new = price_overview['final_formatted']

            item_platforms = json.loads(requests.get(details_url + '&filters=platforms').text)
            platforms = item_platforms[item_id]['data']['platforms']
            win = platforms['windows']
            mac = platforms['mac']
            linux = platforms['linux']

    return props['name'], props['header_image'], item_url, price_discount, price_old, price_new, win, mac, linux


def extract_item_special(item):
    item_url = 'https://store.steampowered.com/app/' + str(item['id'])
    price_old = str(item['original_price'] / 100.0) + '€'
    price_new = str(item['final_price'] / 100.0) + '€'
    win = item['windows_available']
    mac = item['mac_available']
    linux = item['linux_available']

    return item['name'], item['header_image'], item_url, item['discount_percent'], price_old, price_new, win, mac, linux


class SteamService:
    def __init__(self, min_discount, report_lifespan, report_filepath, sender_email, sender_password):
        self.__data = json.loads(requests.get('https://store.steampowered.com/api/featuredcategories').text)
        self.__email = Email(sender_email, sender_password)
        self.__min_discount = min_discount
        self.__report_database = ReportDatabase(report_filepath)
        self.__report_database.remove_invalid(report_lifespan)
        self.__new_items = []

    def proces_message(self, receivers):
        i = 0
        while str(i) in self.__data:
            self.__proces(extract_item, self.__data[str(i)])
            i += 1

        for special_item in self.__data['specials']['items']:
            self.__proces(extract_item_special, special_item)

        if not self.__email.send(receivers):
            self.__report_database.remove(self.__new_items)

    def __proces(self, extract_function, item):
        title, image, url, discount, original_price, final_price, win, mac, linux = extract_function(item)
        item_id = url.replace('https://store.steampowered.com/app/', '')
        if discount >= self.__min_discount and not self.__report_database.exist(item_id):
            self.__email.add_body(title, image, url, discount, original_price, final_price, win, mac, linux)
            self.__report_database.add([item_id])
            self.__new_items.append(item_id)
