import json
import requests
import math

from modules.Images.images_api import ImagesApi
from modules.auth_manager import AuthManager


class OtomotoApi:
    def __init__(self):
        self.auth_manager = AuthManager()
        self.access_token = None
        self.base_url = "https://www.otomoto.pl/api/open/"
        self.images_api = ImagesApi()


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

            response = requests.post(otomoto_url, data=start_data, headers=headers, auth=(otomoto_client_id, otomoto_client_secret))
            if response.status_code == 200:
                self.access_token = response.json().get("access_token")
                print("New access token was acquired from OtoMoto")
                print(self.access_token)
                return self.access_token
            else:
                print("Error:", response.status_code, response.text)
        return self.access_token

        # otomoto api виведення в консоль даних про оголошення

    def _get_basic_headers(self, access_token):
        user_email = "andrewb200590@gmail.com"
        headers = {
            "User-Agent": user_email,
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    def _get_basic_url(self):
        url = "https://www.otomoto.pl/api/open/account/adverts"
        return url

    def print_adverts_list(self, access_token):
        url = self._get_basic_url()
        limit = 10
        page = 1

        headers = self._get_basic_headers(access_token)

        params = {
            "limit": limit,
            "page": page
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            adverts_data = response.json()
            # Process the adverts_data as needed
            print("Adverts data:", adverts_data)
        else:
            print("Error:", response.status_code, response.text)



    # створення колекції з фото (код не тестований, вже як матимемо фото варто спробувати + дописати рядок до data "image_collection_id": 821165355"
    # def create_image_collection(user_email, access_token, image_urls):
    #     url = "https://www.otomoto.pl/api/open/imageCollections"
    #
    #     headers = {
    #         "User-Agent": user_email,
    #         "Content-Type": "application/json",
    #         "Authorization": f"Bearer {access_token}"
    #     }
    #
    #     data = image_urls
    #
    #     response = requests.post(url, json=data, headers=headers)
    #
    #     if response.status_code == 200:
    #         collection_id = response.json().get("id")
    #         print(f"Image collection successfully created with ID: {collection_id}")
    #         return collection_id
    #     else:
    #         print("Error:", response.status_code, response.text)
    #         return None
    #
    # # Replace these with your actual values
    # user_email = "your_user_email"
    # access_token = "your_access_token"
    #
    # image_urls = {
    #     "1": "http://lorempixel.com/800/600/transport/",
    #     "2": "http://lorempixel.com/800/600/transport/",
    #     "3": "http://lorempixel.com/800/600/transport/"
    # }

    # створення нового оголошення otomoto

        # Зчитуєм данні з таблиці
        # Зберігаєм данні в словнику
        # Передаєм словник генератору дати
        # В даті розпаковуєм і створюєм

    # треба поміняти тут код на змінні які будемо отримувати з таблиці
    custom_otomoto_data = {
        "status": "unpaid",
        'title': 'Poprzeczki Belki bagaznik Thule Aerobar 3',
        'description': 'Poprzeczki Thule Aerobar\n108cm-200zł\n120cm-230zł\n127 cm-270zł\n135cm-300zł\n150cm- 350zł\nDostępność proszę sprawdz.\nWystawiam Fakturę VAT marża.\nWysyłka kurierem za pobraniem.',
        'category_id': 173,
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

    def _exel_info_dict_creator(self, product_id, title, description, price, new_used, manufacturer, photos_collection_id):
        if photos_collection_id is None:
            photos_collection_id = "12" # do not add image
        if manufacturer is None or math.isnan(manufacturer):
            manufacturer = "oryginalny"
        exel_info_dict = {
            "id": product_id,
            "title": title,
            "description": description,
            "price": price,
            "new_used": new_used,
            "manufacturer": manufacturer,
            "photos_collection_id" : photos_collection_id
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
        headers = self._get_basic_headers(access_token)
        collection_id = None
        # Відправка POST-запиту
        response = requests.post(url, headers=headers, data=json.dumps(image_data))

        # Перевірка статусу відповіді
        if response.status_code == 201:
            response_data = response.json()
            print("Колекцію зображень успішно створено.", "ID колекції:", response_data.get("id"))
            collection_id = response_data.get("id")
            # print("Посилання на зображення:")
            # for image_id, urls in response_data.get("images").items():
            #     print(f"Зображення {image_id}:")
            #     for i, url in enumerate(urls):
            #         print(f"    {i}: {url}")
        else:
            print("Помилка при створенні колекції зображень. Код статусу:", response.status_code)
            print("Текст помилки:", response.text)
        return collection_id


    def create_otomoto_advert(self, product_id, title, description, price, new_used, manufacturer) -> str:
        if manufacturer is None:
            manufacturer = "default manufacturer" # manufacture by default
        # if description:
        #     # description must be 30+ char
        #     pass
        photos_url_list = self.images_api.upload_image_to_imgur(storage_name=product_id)
        if photos_url_list is None:
            return f"Error: can't find folder {product_id}"
        # advert_id = None
        photos_collection_id = self.create_otomoto_images_collection(photos_url_list=photos_url_list)
        exel_info_dict = self._exel_info_dict_creator(product_id=product_id,
                                                      title=title,
                                                      description=description,
                                                      price=price,
                                                      new_used=new_used,
                                                      manufacturer=manufacturer,
                                                      photos_collection_id=photos_collection_id)
        otomoto_data = self._data_creator(exel_info_dict=exel_info_dict)
        url = self._get_basic_url()
        access_token = self.get_token()
        headers = self._get_basic_headers(access_token=access_token)
        print("otomoto_data:", otomoto_data)
        response = requests.post(url, json=otomoto_data, headers=headers)

        if response.status_code == 201:
            advert_id = response.json().get("id")
            print(f"Advert successfully posted with ID: {advert_id}")
            return str(advert_id)
        else:
            error = ("Error:", response.status_code, response.text)
            return str(error)



    def api_test(self):
        my_30_char_description = "qwertyuio qwertyuio qwertyuio zaoza"
        first_item = self.exel_info_dict_creator(title="Title 1", description=my_30_char_description, price=101, new_used="used",
                                            manufacturer="Manufacturer 1")
        first_item_dict = self.data_creator(first_item)
        advert_id = self.create_otomoto_advert(first_item_dict)

        # collection_id = create_image_collection(user_email, access_token, image_urls)

        # цей кусок має активувати оголошення але чомусь цього не робить тому оголошення додається до вкладки "активуйте оголошення"
        # звідки його вручну можна активувати

        # if advert_id is not None:
        #     activate_advert(advert_id, user_email, access_token)

        # #видалення оголошення
        #
        # def deactivate_advert(advert_id, user_email, access_token):
        #     url = f"https://www.otomoto.pl/api/open/account/adverts/{advert_id}/deactivate"
        #
        #     headers = {
        #         "User-Agent": user_email,
        #         "Content-Type": "application/json",
        #         "Authorization": f"Bearer {access_token}"
        #     }
        #
        #     data = {
        #         "reason": {
        #             "id": "1",
        #             "description": "Reason to deactivate the Ad"
        #         }
        #     }
        #
        #     response = requests.post(url, json=data, headers=headers)
        #
        #     if response.status_code == 200:
        #         print(f"Advert with ID {advert_id} successfully deactivated.")
        #     else:
        #         print("Error:", response.status_code, response.text)
        #
        # advert_id = "6113956279"
        #
        # deactivate_advert(advert_id, user_email, access_token)
