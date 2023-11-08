import os
from datetime import datetime

import requests

from modules.auth_manager import AuthManager

DATETIME = datetime.now().strftime("%d-%m-%Y")


class OneDriveManager:
    def __init__(self):
        self.auth_manager = AuthManager()
        self.access_token = self.auth_manager.get_access_token_default_scopes()
        self.endpoint = self.auth_manager.get_endpoint()

    def upload_file_to_onedrive(self, file_path, rows_to_skip, rows_to_read, current_day=DATETIME):
        if rows_to_skip is None and rows_to_read is None:
            uploading_file_name = os.path.basename(file_path)
        else:
            base_name, extension = os.path.splitext(file_path)
            new_file_path = f"{base_name} {rows_to_skip + 1}-{rows_to_skip + rows_to_read}{extension}"
            uploading_file_name = os.path.basename(new_file_path)

        upload_url = self.endpoint + f"drive/items/root:/Holland/Reports/{current_day}/{uploading_file_name}:/content"
        access_token = self.access_token
        headers_octet_stream = {
            'Authorization': access_token,
            'Content-Type': 'application/octet-stream',
        }

        with open(file_path, 'rb') as upload:
            media_content = upload.read()

        response = requests.put(url=upload_url, headers=headers_octet_stream, data=media_content)
        if response.status_code == 201 or response.status_code == 200:
            print(f"File {uploading_file_name} download to OneDrive!")
        else:
            print(f"Сталася помилка при завантаженні файлу на OneDrive!. {response.text}")
        return response

    def get_root_folder_json(self, one_drive_url, headers):
        result = requests.get(url=one_drive_url, headers=headers)
        return result.json()

    def download_file_to_tmp(self, download_url, file_name):
        response = requests.get(download_url,
                                headers=self.auth_manager.get_default_header(access_token=self.access_token))

        if response.status_code == 200:
            with open(f"/tmp/text_reports/{file_name}", "wb") as f:
                f.write(response.content)
        else:
            print(f"Помилка при завантаженні файлу {file_name}: {response.status_code} - {response.text}")

    def download_reports_to_tmp(self, current_day=DATETIME):
        upload_url = self.endpoint + f"drive/items/root:/Holland/Reports/{current_day}:/children"
        print(upload_url)
        response = requests.get(url=upload_url,
                                headers=self.auth_manager.get_default_header(access_token=self.access_token))
        if response.status_code == 200:
            files = response.json().get("value", [])
            for file in files:
                if "report" in file.get("name", "").lower():
                    file_name = file.get("name")
                    file_id = file.get("id")
                    download_url = self.endpoint + f"drive/items/{file_id}/content"
                    self.download_file_to_tmp(download_url, file_name)
        else:
            print(f"Error in download_reports_to_tmp {response.status_code} - {response.text}")

onedrivemanager = OneDriveManager()

onedrivemanager.download_reports_to_tmp()



# folder_path = os.path.join(os.path.dirname(os.getcwd()), "tmp/text_reports")
# file_list = (os.listdir(folder_path))
# for file_name in file_list:
#     file_path = os.path.join(folder_path, file_name)
#     onedrivemanager.upload_file_to_onedrive(file_path=file_path, rows_to_read=1, rows_to_skip=0)



