import requests

from modules.auth_manager import AuthManager


class OneDriveManager:
    def __init__(self):
        self.auth_manager = AuthManager()
        self.access_token = self.auth_manager.get_access_token_default_scopes()

    def upload_file_to_onedrive(self, file_path, upload_url):
        if upload_url is None:
            upload_url = self.auth_manager.get_endpoint() + "drive/items/root:/Holland/sklad.xlsx:/content"
        access_token = self.access_token
        headers_octet_stream = {
            'Authorization': access_token,
            'Content-Type': 'application/octet-stream',
        }

        with open(file_path, 'rb') as upload:
            media_content = upload.read()

        response = requests.put(url=upload_url, headers=headers_octet_stream, data=media_content)

        if response.status_code == 200:
            print("Файл успішно завантажено на OneDrive!")
        else:
            print(f"Сталася помилка при завантаженні файлу. {response.text}")
        return response

    def get_root_folder_json(self, one_drive_url, headers):
        result = requests.get(url=one_drive_url, headers=headers)
        return result.json()
