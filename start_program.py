import json

import requests

from modules.auth_manager import AuthManager
from modules.excel_handler import ExcelHandler
from modules.one_drive_photo_manager import OneDrivePhotoManager
from modules.onedrive_manager import OneDriveManager

CLIENT_ID = "e3608d4cee384d3b9adc39b2e5f2f92f"  # wprowadź Client_ID aplikacji
CLIENT_SECRET = "xoDO0ODIDd0yaH0y5H3Gn0fVMCpfzujZ6rfrsXBYIMPKnh24Dwm08NTB3OusLky4"  # wprowadź Client_Secret aplikacji
TOKEN_URL = "https://allegro.pl/auth/oauth/token"
API_BASE_URL = "https://allegro.pl"


class StartProgram:
    def __init__(self):
        self.auth_manager = AuthManager()
        self.excel_handler = ExcelHandler()
        self.onedrive_manager = OneDriveManager()

    def start(self):
        endpoint = self.auth_manager.get_endpoint()
        access_token = self.auth_manager.get_access_token_default_scopes()
        one_drive_url = self.auth_manager.get_endpoint() + "drive/root/children"
        headers = self.auth_manager.get_default_header(access_token=access_token)
        excel_file_name = "sklad.xlsx"

        self.one_drive_photo_manager = OneDrivePhotoManager(endpoint=endpoint,headers=headers, access_token=access_token)

        root_folder_onedrive = self.onedrive_manager.get_root_folder_json(one_drive_url=one_drive_url, headers=headers)

        file_content = self.excel_handler.get_exel_file(root_folder_onedrive=root_folder_onedrive, name=excel_file_name)

        # Робота з Excel-файлами
        df1 = self.excel_handler.read_excel(file_content, sheet_name='Sheet1')
        print(df1)
        df2 = self.excel_handler.read_excel(file_content, sheet_name='Sheet2')
        print(df2)
        df2 = self.excel_handler.fill_missing_values(df2, 'write here', '400$')
        print(df2)

        self.excel_handler.save_excel(df1, df2, output_excel_filename=excel_file_name)

        upload_url = endpoint + "drive/items/root:/sklad.xlsx:/content"
        excel_file_path = 'sklad.xlsx'
        self.onedrive_manager.upload_excel_to_onedrive(access_token=access_token,
                                                       file_path=excel_file_path,
                                                       upload_url=upload_url)


        """
        Ця частина працює, а може не, хто знає
        """

        self.one_drive_photo_manager.get_photos("CP06C")



    # #підключення до allegro api
    # def get_access_token():
    #     try:
    #         data = {'grant_type': 'client_credentials'}
    #         access_token_response = requests.post(TOKEN_URL, data=data, verify=False,
    #                                               allow_redirects=False, auth=(CLIENT_ID, CLIENT_SECRET))
    #         print(access_token_response.text)  # Додайте цей рядок для виводу вмісту відповіді сервера
    #         tokens = json.loads(access_token_response.text)
    #         access_token = tokens['access_token']
    #         return access_token
    #     except requests.exceptions.HTTPError as err:
    #         raise SystemExit(err)
    #
    # access_token = get_access_token()
    # print("access token = " + access_token)
    #
    #
    # #запит на отримання даних про оголошення по ід
    # # Приклад виклику API для отримання інформації про продукт за ID
    # try:
    #     headers = {
    #         "Authorization": f"Bearer {access_token}"
    #     }
    #
    #     product_id = "13067041315"
    #     endpoint = f"https://allegro.pl/sale/products/13067041315"
    #
    #     response = requests.get(endpoint, headers=headers)
    #     if response.status_code == 200:
    #         product_info = response.json()
    #         print(product_info)
    #     else:
    #         print(f"API request failed: {response.text}")
    # except Exception as e:
    #     print(f"Error: {e}")


    #otomoto api connection

    url = "https://www.otomoto.pl/api/open/oauth/token"
    client_id = "1399"
    client_secret = "62ef409424513c656da791bcb052ee67"
    username = "andrewb200590@gmail.com"
    password = "6925Papa@"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "password",
        "username": username,
        "password": password
    }

    response = requests.post(url, data=data, headers=headers, auth=(client_id, client_secret))

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print("Access Token:", access_token)
    else:
        print("Error:", response.status_code, response.text)

    #otomoto api виведення в консоль даних про оголошення

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

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        adverts_data = response.json()
        # Process the adverts_data as needed
        print("Adverts data:", adverts_data)
    else:
        print("Error:", response.status_code, response.text)


    #створення колекції з фото (код не тестований, вже як матимемо фото варто спробувати + дописати рядок до data "image_collection_id": 821165355"
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

    #створення нового оголошення otomoto

    def activate_advert(advert_id, user_email, access_token):
        url = f"https://www.otomoto.pl/api/open/account/adverts/{advert_id}/activate"

        headers = {
            "User-Agent": user_email,
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            print(f"Advert with ID {advert_id} successfully activated!")
        else:
            print("Error:", response.status_code, response.text)

    def post_advert(user_email, access_token):
        url = "https://www.otomoto.pl/api/open/account/adverts"

        headers = {
            "User-Agent": user_email,
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        #треба поміняти тут код на змінні які будемо отримувати з таблиці
        data = {
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

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 201:
            advert_id = response.json().get("id")
            print(f"Advert successfully posted with ID: {advert_id}")
            return advert_id
        else:
            print("Error:", response.status_code, response.text)
            return None

    # Replace these with your actual values
    user_email = "andrewb200590@gmail.com"

    advert_id = post_advert(user_email, access_token)

    #collection_id = create_image_collection(user_email, access_token, image_urls)


    #цей кусок має активувати оголошення але чомусь цього не робить тому оголошення додається до вкладки "активуйте оголошення"
    #звідки його вручну можна активувати

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


