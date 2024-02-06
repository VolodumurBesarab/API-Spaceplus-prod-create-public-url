import os
import re

import requests
from requests import Response

from dotenv import load_dotenv

from modules.reports.reports_generator import ReportsGenerator

load_dotenv()


class WoocommerceManager:
    def __init__(self):
        self.reports_generator = ReportsGenerator()
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

        response = requests.get(
            url=f'{self.WC_URL}{woocommerce_endpoint}',
            auth=(self.CONSUMER_KEY_WC, self.CONSUMER_SECRET_WC)
        )
        if response.status_code == 200:
            self.create_database_in_onedrive(response=response)
        else:
            print('Підключення не вдалось. Перевірте ключі та URL.')
        pass

    def create_database_in_onedrive(self, response: Response):
        adverts_data = response.json()
        adverts = {}
        for advert in adverts_data:
            pattern = re.compile(r'\|(.+?)\|')

            description = advert["description"]
            match = pattern.search(description)

            if match:
                # print(advert["id"], match.group(1))
                adverts[advert["id"]] = match.group(1)
            else:
                message = f"{advert['id']} have not id 'номер на складі'"
                print(message)
                # self.reports_generator.create_general_report(message=message)
        print(adverts)
        pass


woocommerce_manager = WoocommerceManager()
woocommerce_manager.get_database()
