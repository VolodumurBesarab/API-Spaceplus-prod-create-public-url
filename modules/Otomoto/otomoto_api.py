import json
import requests
from modules.auth_manager import AuthManager

class OtomotoApi:

    def __init__(self):
        self.auth_manager = AuthManager()

    def start(self):
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
        access_token = None
        if response.status_code == 200:
            access_token = response.json().get("access_token")
            # remove
            print("Access Token:", access_token)
        else:
            print("Error:", response.status_code, response.text)

        # otomoto api виведення в консоль даних про оголошення

        url = "https://www.otomoto.pl/api/open/account/adverts"
        user_email = "andrewb200590@gmail.com"
        limit = 10
        page = 1

        headers = {
            "User-Agent": user_email,
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        params = {
            "limit": limit,
            "page": page
        }

        def print_adverts_list():
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                adverts_data = response.json()
                # Process the adverts_data as needed
                print("Adverts data:", adverts_data)
            else:
                print("Error:", response.status_code, response.text)

        print_adverts_list()

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

        def activate_advert(advert_id, user_email, access_token):
            url = f"https://www.otomoto.pl/api/open/account/adverts/{advert_id}/activate"

            response = requests.post(url, headers=headers)

            if response.status_code == 200:
                print(f"Advert with ID {advert_id} successfully activated!")
            else:
                print("Error:", response.status_code, response.text)

            # def post_advert(user_email, access_token):
            #     url = "https://www.otomoto.pl/api/open/account/adverts"
            #
            #     headers = {
            #         "User-Agent": user_email,
            #         "Content-Type": "application/json",
            #         "Authorization": f"Bearer {access_token}"
            #     }

            # Винести статичні данні і поміняти
            CITY = "Lublin"

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

        def exel_info_dict_creator(title, description, price, new_used, manufacturer):
            exel_info_dict = {
                "title": title,
                "description": description,
                "price": price,
                "new_used": new_used,
                "manufacturer": manufacturer,
            }
            return exel_info_dict

        def data_creator(exel_info_dict) -> json:
            if dict == None or dict == {}:
                print("Dictionaty is empty")
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
                    'title_parts': exel_info_dict["title"],
                    'manufacturer': exel_info_dict["manufacturer"],
                    "price": {
                        '0': 'price',
                        '1': exel_info_dict["price"],
                        'currency': 'PLN',
                        'gross_net': 'gross'
                    },
                },
                'new_used': exel_info_dict["new_used"],
                'visible_in_profile': '1',
            }
            return otomoto_data

        def create_otomoto_advert(otomoto_data):
            response = requests.post(url, json=otomoto_data, headers=headers)

            if response.status_code == 201:
                advert_id = response.json().get("id")
                print(f"Advert successfully posted with ID: {advert_id}")
                return advert_id
            else:
                print("Error:", response.status_code, response.text)
                return None

        # Replace these with your actual values
        # user_email = "andrewb200590@gmail.com"
        #
        # advert_id = post_advert(user_email, access_token)
        my_30_char_description = "qwertyuio qwertyuio qwertyuio zaoza"
        first_item = exel_info_dict_creator(title="Title 1", description=my_30_char_description, price=101, new_used="used",
                                            manufacturer="Manufacturer 1")
        first_item_dict = data_creator(first_item)
        advert_id = create_otomoto_advert(first_item_dict)

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
