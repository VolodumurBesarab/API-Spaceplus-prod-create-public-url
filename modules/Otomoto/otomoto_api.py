import json
import os
import re

import requests
import math

from requests import Response

from modules.Images.images_api import ImagesApi
from modules.Images.s3_link_generator import S3LinkGenerator
from modules.auth_manager import AuthManager
from modules.one_drive_photo_manager import OneDrivePhotoManager


class OtomotoApi:
    def __init__(self):
        self.auth_manager = AuthManager()
        self.access_token = None
        self.base_url = "https://www.otomoto.pl/api/open/"
        self.images_api = ImagesApi()
        self.one_drive_photo_manager = OneDrivePhotoManager()

    def get_token(self):
        if not self.access_token:
            otomoto_url = self.auth_manager.get_otomoto_url()
            otomoto_client_id = self.auth_manager.get_otomoto_client_id()
            otomoto_client_secret = self.auth_manager.get_otomoto_client_secret()
            otomoto_username = self.auth_manager.get_otomoto_username()
            otomoto_password = self.auth_manager.get_otomoto_password()

            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }

            start_data = {
                "grant_type": "password",
                "username": otomoto_username,
                "password": otomoto_password
            }

            response = requests.post(otomoto_url, data=start_data, headers=headers,
                                     auth=(otomoto_client_id, otomoto_client_secret))
            if response.status_code == 200:
                self.access_token = response.json().get("access_token")
                print("New access token was acquired from OtoMoto")
                return self.access_token
            else:
                print("Error:", response.status_code, response.text)
        return self.access_token

    def get_basic_headers(self, access_token):
        user_email = "andrewb200590@gmail.com"
        headers = {
            "User-Agent": user_email,
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    def get_basic_url(self):
        url = "https://www.otomoto.pl/api/open/account/adverts"
        return url

    def get_database(self, access_token):
        url = self.get_basic_url()
        limit = 1250
        page = 1

        headers = self.get_basic_headers(access_token)

        params = {
            "limit": limit,
            "page": page
        }
        database = {}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            adverts_data = response.json()

            for result in adverts_data["results"]:
                pattern = re.compile(r'\|(.+?)\|')

                description = result["description"]
                match = pattern.search(description)

                if match:
                    additional_text = match.group(1)
                    description_with_additional_text = description + additional_text

                    # Перевірка чи існує ключ у базі даних
                    if description_with_additional_text in database:
                        print(f"Помилка: Ключ '{description_with_additional_text}' вже існує в базі даних.")
                    else:
                        in_storage_id = match.group(1)
                        database[in_storage_id] = result["id"]

            with open("/tmp/adverts_dict.json", "w", encoding="utf-8") as file:
                json.dump(database, file, ensure_ascii=False, indent=2)
        else:
            print("Error:", response.status_code, response.text)
        return database

    def get_adverts_body(self, otomoto_id) -> Response:
        url = self.get_basic_url() + f"/{otomoto_id}"
        access_token = self.get_token()
        headers = self.get_basic_headers(access_token=access_token)
        response = requests.get(url=url, headers=headers)
        print(response.json())
        return response

    custom_otomoto_data = {
        "status": "unpaid",
        'title': 'Poprzeczki Belki bagaznik Thule Aerobar 3',
        'description': 'Poprzeczki Thule Aerobar\n108cm-200zł\n120cm-230zł\n127 cm-270zł\n135cm-300zł\n150cm- 350zł\nDostępność proszę sprawdz.\nWystawiam Fakturę VAT marża.\nWysyłka kurierem za pobraniem.',
        'category_id': 163,
        'region_id': 8,
        'city_id': 10119,
        'municipality': 'Lublin',
        'city': {
            'pl': 'Lublin',
            'en': 'Lublin'
        },
        'coordinates': {
            'latitude': 51.23955,
            'longitude': 22.55257,
            'radius': 0,
            'zoom_level': 13
        },
        'advertiser_type': 'business',
        'contact': {
            'person': 'Andrzej Besarab',
            'phone_numbers': [
                '+48660086570'
            ]
        },
        "params": {
            'tire-brand': 'others',
            "parts-category": "roof-boxes",
            'delivery': '1',
            'title_parts': 'Poprzeczki Belki bagaznik Thule Aerobar delux',
            'manufacturer': 'Thule',
            "price": {
                '0': 'price',
                '1': 200,
                'currency': 'PLN',
                'gross_net': 'gross'
            },
        },
        'new_used': 'used',
        'visible_in_profile': '1',
    }

    def _exel_info_dict_creator(self, product_id, title, description, price, new_used, manufacturer,
                                photos_collection_id):
        if photos_collection_id is None:
            photos_collection_id = "12"  # do not add image
        if manufacturer is None or math.isnan(manufacturer):
            manufacturer = "oryginalny"
        exel_info_dict = {
            "id": product_id,
            "title": title,
            "description": description,
            "price": price,
            "new_used": new_used,
            "manufacturer": manufacturer,
            "photos_collection_id": photos_collection_id
        }
        return exel_info_dict

    def _data_creator(self, exel_info_dict) -> json:
        if exel_info_dict is None or exel_info_dict == {}:
            print("Dictionary is empty")
        otomoto_data = {
            "status": "unpaid",
            'title': exel_info_dict["title"],
            'description': exel_info_dict["description"],
            'category_id': 173,
            'region_id': 8,
            'city_id': 10119,
            'municipality': 'Lublin',
            'city': {
                'pl': 'Lublin',
                'en': 'Lublin'
            },
            'coordinates': {
                'latitude': 51.271275,
                'longitude': 22.569633,
                'radius': 0,
                'zoom_level': 13
            },
            'advertiser_type': 'business',
            'contact': {
                'person': 'Andrzej Besarab',
                'phone_numbers': [
                    '+48660086570'
                ]
            },
            "params": {
                'tire-brand': 'others',
                'delivery': '1',
                'title_parts': exel_info_dict["title"],
                'manufacturer': exel_info_dict["manufacturer"],
                "price": {
                    '0': 'price',
                    '1': exel_info_dict["price"],
                    'currency': 'PLN',
                    'gross_net': 'gross'
                },
            },
            "image_collection_id": exel_info_dict["photos_collection_id"],
            'new_used': exel_info_dict["new_used"],
            'visible_in_profile': '1',
        }
        return otomoto_data

    def create_otomoto_images_collection(self, photos_url_list: list[str]):
        url = self.base_url + "imageCollections"  # Замініть на правильний URL

        # example creation image data
        # image_data = {
        #     "1": "https://i.imgur.com/x9c4rhA.jpeg",
        #     "2": "https://i.imgur.com/pbUDT54.jpeg",
        #     "3": "https://i.imgur.com/WVXzjrn.jpeg"
        # }

        image_data = {}
        counter = 1
        for photo_url in photos_url_list:
            image_data.update({str(counter): photo_url})
            counter += 1

        access_token = self.get_token()
        headers = self.get_basic_headers(access_token)
        collection_id = None
        # Відправка POST-запиту
        response = requests.post(url, headers=headers, data=json.dumps(image_data))

        # Перевірка статусу відповіді
        if response.status_code == 201:
            response_data = response.json()
            print("Колекцію зображень успішно створено.", "ID колекції:", response_data.get("id"))
            collection_id = response_data.get("id")
        else:
            print("Помилка при створенні колекції зображень. Код статусу:", response.status_code)
            print("Текст помилки:", response.text)
        return collection_id

    def delete_and_save_in_json(self, json_file_path, key_to_delete):
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        if key_to_delete in data:
            del data[key_to_delete]
            print(f'Об\'єкт з ключем "{key_to_delete}" видалено.')

            with open(json_file_path, 'w') as file:
                json.dump(data, file, indent=4)
                print('Зміни успішно збережено у файлі.')
        else:
            print(f'Ключ "{key_to_delete}" не знайдено в файлі.')

    def delete_advert(self, in_stock_id, otomoto_id) -> Response:
        url = self.base_url + f"adverts/{otomoto_id}"
        print(url)
        response = requests.delete(url=url, headers=self.get_basic_headers(self.get_token()))
        if response.status_code == 204:
            json_file_path = "/tmp/adverts_dict.json"
            self.delete_and_save_in_json(json_file_path=json_file_path, key_to_delete=in_stock_id)
        return response

    def create_otomoto_advert(self, product_id, title, description: str, price, new_used, manufacturer) -> str:
        if len(str(description)) < 30:
            return f"Error: {product_id}'s description must be more then 30 symbol"
        if product_id == 0 or product_id == 2 or product_id is None:
            return f"Error: can't create ads with ID {product_id}"
        parent_folder_id = self.one_drive_photo_manager.get_stock_photos_folder_id()
        folder_id = self.one_drive_photo_manager.find_folder_by_name(parent_folder_id=parent_folder_id,
                                                                     folder_name=str(product_id))

        path_to_save_photos = self.one_drive_photo_manager.download_files_from_folder(folder_id=folder_id,
                                                                                      folder_name=str(product_id))

        print(path_to_save_photos)
        s3_link_generator = S3LinkGenerator()
        photos_url_list = s3_link_generator.generate_public_urls(path_to_save_photos=path_to_save_photos)

        if photos_url_list is None or photos_url_list == []:
            return f"Error: can't find folder {product_id}, or folder is empty"

        photos_collection_id = self.create_otomoto_images_collection(photos_url_list=photos_url_list)
        exel_info_dict = self._exel_info_dict_creator(product_id=product_id,
                                                      title=title,
                                                      description=description,
                                                      price=price,
                                                      new_used=new_used,
                                                      manufacturer=manufacturer,
                                                      photos_collection_id=photos_collection_id)

        otomoto_data = self._data_creator(exel_info_dict=exel_info_dict)
        url = self.get_basic_url()
        access_token = self.get_token()
        headers = self.get_basic_headers(access_token=access_token)
        response = requests.post(url, json=otomoto_data, headers=headers)

        if response.status_code == 201:
            advert_id = response.json().get("id")
            return str(advert_id)
        else:
            error = ("Error:", response.status_code, response.text)
            return str(error)
