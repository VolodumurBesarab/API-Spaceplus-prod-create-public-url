import requests as requests
import os
import requests

NL_FOLDER_ID = "01GK3VGRXOWQGPB72LHVB2WIIN642U4NKK"

class OneDriveHelper:
    def __init__(self, endpoint, headers, access_token):
        self.endpoint = endpoint
        self.headers = headers
        self.access_token = access_token

    def find_folder_by_name(self, folder_name):
        response = requests.get(f"{self.endpoint}/root/children", headers=self.headers)
        response.raise_for_status()
        items = response.json().get('value', [])
        for item in items:
            if item.get('folder', {}).get('name') == folder_name:
                return item['id']
        return None

    def download_files_from_folder(self, folder_id, destination_folder):
        response = requests.get(f"{self.endpoint}/items/{folder_id}/children", headers=self.headers)
        response.raise_for_status()
        items = response.json().get('value', [])
        for item in items:
            if 'file' in item:
                file_id = item['id']
                file_name = item['name']
                download_url = f"{self.endpoint}/items/{file_id}/content"
                file_path = os.path.join(destination_folder, file_name)

                # Завантаження файлу
                response = requests.get(download_url, headers=self.headers)
                if response.status_code == 200:
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f"Завантажено: {file_name}")
                else:
                    print(f"Не вдалося завантажити: {file_name}")





class OneDrivePhotoManager:
    def __init__(self, endpoint: str, headers, access_token):
        self.endpoint = endpoint
        self.headers = headers
        self.access_token = access_token

    def get_photos(self, folder_name: str):
        response = requests.get(url=self.endpoint + f"drive/items/{NL_FOLDER_ID}/children",
                                headers=self.headers)
        photo_id_list = []
        if response.status_code == 200:
            nl_folder_contents = response.json()
            searched_folder_id = None

            # Знайти папку 'CP06C' у списку вмісту папки 'root/NL'
            for item in nl_folder_contents['value']:
                if item['name'] == folder_name and item['folder']:
                    searched_folder_id = item['id']
                    break

            if searched_folder_id:
                # Отримати вміст папки 'CP06C'
                response_cp06c = requests.get(
                    self.endpoint + f"drive/items/{searched_folder_id}/children",
                    headers=self.headers
                )
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

        create_link_payload = {
            "type": "view",
            "scope": "anonymous",
            "retainInheritedPermissions": False
        }
        post_headers = {
            'Authorization': self.access_token,
            'Content-Type': 'application/json'
        }

        create_link_url = self.endpoint + f"drive/items/{photo_id_list[0]}/createLink"
        create_link_response = requests.post(url=create_link_url, headers=post_headers, json=create_link_payload)

        if create_link_response.status_code == 200:
            create_link_response_json = create_link_response.json()
            created_link = create_link_response_json["link"]["webUrl"]
            # test = requests.get(created_link).content
            # print(test)

        for item_id in photo_id_list:
            create_link_url = self.endpoint + f"drive/items/{item_id}/createLink"

            create_link_response = requests.post(url=create_link_url, headers=post_headers, json=create_link_payload)

            if create_link_response.status_code == 200:
                create_link_response_json = create_link_response.json()
                created_link = create_link_response_json["link"]["webUrl"]
                print(created_link)
                # print(create_link_response_json)

                # image_data = {
                #     "file": ("image.jpg", requests.get(created_link).content, "image/jpeg")
                # }
                #
                # print(image_data)
