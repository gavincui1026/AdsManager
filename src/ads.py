import random
import time

import requests

from src.proxy import Proxy


class AdsPower:
    def __init__(self,proxies,token):
        for region,city in proxies.items():
            print(region, city)
            proxy_host, proxy_port, proxy_user, proxy_password = self.get_proxy(region, city,token)
            ads = {
                "proxy_soft": "other",
                "proxy_type": "http",
                "proxy_host": proxy_host,
                "proxy_port": proxy_port,
                "proxy_username": proxy_user,
                "proxy_password": proxy_password
            }
            user_id = self.create_broswer(ads)


            self.start(user_id)

    def create_broswer(self, ads):
        url = "http://local.adspower.com:50325/api/v1/user/create"
        payload = {
                "group_id": "0",
                "user_proxy_config": {
                    "proxy_soft": 'other',
                    "proxy_type": 'socks5',
                    "proxy_host": ads["proxy_host"],
                    "proxy_port": ads["proxy_port"],
                    "proxy_user": ads["proxy_username"],
                    "proxy_password": ads["proxy_password"],

                },
                "fingerprint_config": {
                    "automatic_timezone": "1",
                    "webrtc": "forward",
                    "location_switch":"1",
                    "language_switch":"1",
                    "page_language_switch":"1",
                    "screen_resolution":"random",
                    "fonts":self.generate_random_fonts(),
                    "canvas":"1",
                    "webgl_image":"1",
                    "webgl":"3",
                    "do_not_track":"true",
                    "mac_address_config":{"model":"1","address": ""},
                },
            }
        response = requests.post(url, json=payload)
        print(response.json())
        if response.json()["code"] == 0:
            return response.json()["data"]["id"]
        else:
            return None

    def generate_random_fonts(self):
        fonts = [
            "Arial",
            "Arial Black",
            "Arial Narrow",
            "Arial Rounded MT Bold",
            "Book Antiqua",
            "Bookman Old Style",
            "Bradley Hand ITC",
            "Calibri",
            "Cambria",
            "Cambria Math",
            "Century",
            "Century Gothic",
            "Comic Sans MS",
            "Consolas",
            "Constantia",
            "Cooper Black",
            "Corbel",
            "Courier",
            "Courier New",
            "Garamond",
            "Georgia",
            "Impact",
            "Lucida Console",
            "Lucida Sans Unicode",
            "Palatino",
            "Palatino Linotype",
            "Segoe Print",
            "Segoe Script",
            "Segoe UI",
            "Segoe UI Light",
            "Segoe UI Semibold",
            "Segoe UI Symbol",
            "Tahoma",
            "Times",
            "Times New Roman",
            "Trebuchet MS",
            "Verdana",
            "Webdings",
            "Wingdings",
            "Wingdings 2",
            "Wingdings 3",
        ]
        random_fonts = random.sample(fonts, 3)
        return random_fonts
    def start(self, user_id):
        url="http://local.adspower.com:50325/api/v1/browser/start"

        params = {
            "user_id": user_id
        }
        response = requests.get(url, params=params)
    def get_proxy(self, region, city,token):
        print('到这了')
        proxy = Proxy()
        res = proxy.yuliproxy(1, region, city, token)
        print(res)
        addy = res["lists"]
        parts = addy[0].split(":")
        print(parts)
        proxy_host = parts[0]
        proxy_port = parts[1]
        proxy_user = parts[2]
        proxy_password = parts[3]
        return proxy_host, proxy_port, proxy_user, proxy_password

if __name__ == '__main__':
    proxies = {
        "quebec": "montreal",
        "ontario": "toronto",
        # "british columbia": "vancouver",
        # "alberta": "calgary",
        # "manitoba": "winnipeg",
        # "saskatchewan": "saskatoon",
        # "nova scotia": "halifax",
        # "new brunswick": "moncton",
        # "newfoundland and labrador": "st. john's",
        # "prince edward island": "charlottetown",
        # "northwest territories": "yellowknife",
        # "yukon": "whitehorse",
        # "nunavut": "iqaluit"
    }
    ads_power = AdsPower(proxies)



