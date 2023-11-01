import os

import requests

from modules.auth_manager import AuthManager


class OneDriveManager:
    def __init__(self):
        self.auth_manager = AuthManager()
        self.access_token = self.auth_manager.get_access_token_default_scopes()

    def upload_file_to_onedrive(self, file_path, rows_to_skip, rows_to_read):
        if rows_to_skip is None and rows_to_read is None:
            file_name = os.path.basename(file_path)
        else:
            file_name = f"{os.path.basename(file_path)} {rows_to_skip}-{rows_to_read} "
        upload_url = self.auth_manager.get_endpoint() + f"drive/items/root:/Holland/{file_name}:/content"
        access_token = self.access_token
        headers_octet_stream = {
            'Authorization': access_token,
            'Content-Type': 'application/octet-stream',
        }

        with open(file_path, 'rb') as upload:
            media_content = upload.read()

        response = requests.put(url=upload_url, headers=headers_octet_stream, data=media_content)
        if response.status_code == 201 or response.status_code == 200:
            print("Файл успішно завантажено на OneDrive!")
        else:
            print(f"Сталася помилка при завантаженні файлу на OneDrive!. {response.text}")
        return response

    def get_root_folder_json(self, one_drive_url, headers):
        result = requests.get(url=one_drive_url, headers=headers)
        return result.json()
