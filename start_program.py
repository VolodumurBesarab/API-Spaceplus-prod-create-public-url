import json

import requests

from modules.auth_manager import AuthManager
from modules.excel_handler import ExcelHandler
from modules.onedrive_manager import OneDriveManager


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

        response = requests.get(url=endpoint + "drive/items/01GK3VGRXOWQGPB72LHVB2WIIN642U4NKK/children",
                                headers=headers)
        photo_id_list = []
        if response.status_code == 200:
            nl_folder_contents = response.json()
            searched_folder_id = None

            # Знайти папку 'CP06C' у списку вмісту папки 'root/NL'
            for item in nl_folder_contents['value']:
                if item['name'] == 'CP06C' and item['folder']:
                    searched_folder_id = item['id']
                    break

            if searched_folder_id:
                # Отримати вміст папки 'CP06C'
                response_cp06c = requests.get(
                    f"https://graph.microsoft.com/v1.0/users/andrzej.besarab@spacelpus.onmicrosoft.com/drive/items/{searched_folder_id}/children",
                    headers=headers
                )
                # https://graph.microsoft.com/v1.0/sites/{site-id}/drives/{drive-id}/items/{item-id}/invite
                if response_cp06c.status_code == 200:
                    cp06c_folder_contents = response_cp06c.json()
                    for item in cp06c_folder_contents['value']:
                        if item['file']:
                            photo_id_list.append(item['id'])
                else:
                    print(f"Сталася помилка при отриманні вмісту папки CP06C: {response_cp06c.text}")
            else:
                print("Папка CP06C не знайдена у папці root/NL")
        else:
            print(f"Сталася помилка при отриманні вмісту папки root/NL: {response.text}")
        print(photo_id_list)

        item_id_zal = "01GK3VGRQXMBTZ5QJPXRA3EVRMXIKZCKZG"

        create_link_payload = {
            "type": "view",
            "scope": "anonymous",
            "retainInheritedPermissions": False
        }
        post_headers = {
            'Authorization': access_token,
            'Content-Type': 'application/json'
        }

        create_link_url = endpoint + f"drive/items/{photo_id_list[0]}/createLink"
        create_link_response = requests.post(url=create_link_url, headers=post_headers, json=create_link_payload)

        if create_link_response.status_code == 200:
            create_link_response_json = create_link_response.json()
            created_link = create_link_response_json["link"]["webUrl"]
            test = requests.get(created_link).content
            print(test)

        for item_id in photo_id_list:
            create_link_url = endpoint + f"drive/items/{item_id}/createLink"

            create_link_response = requests.post(url=create_link_url, headers=post_headers, json=create_link_payload)

            if create_link_response.status_code == 200:
                create_link_response_json = create_link_response.json()
                created_link = create_link_response_json["link"]["webUrl"]
                # print(created_link.content)
                print(create_link_response.json())

                # image_data = {
                #     "file": ("image.jpg", requests.get(created_link).content, "image/jpeg")
                # }
                #
                # print(image_data)




