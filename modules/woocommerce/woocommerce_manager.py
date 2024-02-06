import json
import os
import re

import requests
from requests import Response

from dotenv import load_dotenv

from modules.onedrive_manager import OneDriveManager
from modules.reports.reports_generator import ReportsGenerator

load_dotenv()


class WoocommerceManager:
    def __init__(self):
        self.reports_generator = ReportsGenerator()
        self.one_drive_manager = OneDriveManager()
        try:
            self.CONSUMER_KEY_WC = os.getenv("CONSUMER_KEY_WC")
            self.CONSUMER_SECRET_WC = os.getenv("CONSUMER_SECRET_WC")
            self.WC_URL = os.getenv("WC_URL")
        except:
            self.CONSUMER_KEY_WC = os.getenv("CONSUMER_KEY_WC")
            self.CONSUMER_SECRET_WC = os.getenv("CONSUMER_SECRET_WC")
            self.WC_URL = os.getenv("WC_URL")
            print("add env to lambda")

    def get_database(self):
        woocommerce_endpoint = 'products'
        url = f'{self.WC_URL}{woocommerce_endpoint}'
        auth = (self.CONSUMER_KEY_WC, self.CONSUMER_SECRET_WC)
        woocommerce_data_base = None

        response = requests.get(url=url, auth=auth)
        if response.status_code == 200:
            woocommerce_data_base = self.create_database_in_onedrive(response=response)
        else:
            print('Підключення не вдалось. Перевірте ключі та URL.')

        return woocommerce_data_base

    def create_database_in_onedrive(self, response: Response):
        adverts_data = response.json()
        adverts = {}
        for advert in adverts_data:
            pattern = re.compile(r'\|(.+?)\|')

            description = advert["description"]
            match = pattern.search(description)

            if match:
                # print(advert["id"], match.group(1))
                adverts[match.group(1)] = advert["id"]
            else:
                message = f"{advert['id']} have not id 'номер на складі'"
                print(message)
                # self.reports_generator.create_general_report(message=message)
        return adverts

    def save_database_woocommerce_on_onedrive(self, woocommerce_data_base):
        adverts_dict_json_path = "/tmp/adverts_dict_woocommerce.json"
        with open(adverts_dict_json_path, "w", encoding="utf-8") as file:
            json.dump(woocommerce_data_base, file, ensure_ascii=False, indent=4)

        self.one_drive_manager.upload_file_to_onedrive(file_path=adverts_dict_json_path)

woocommerce_manager = WoocommerceManager()
data_base = woocommerce_manager.get_database()
woocommerce_manager.save_database_woocommerce_on_onedrive(woocommerce_data_base=data_base)
