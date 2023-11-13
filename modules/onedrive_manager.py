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
        self.default_header = self.auth_manager.get_default_header(access_token=self.access_token)

    def upload_file_to_onedrive(self, file_path, rows_to_skip=None, rows_to_read=None, current_day=DATETIME, path_after_current_day = None):
        if rows_to_skip is None and rows_to_read is None:
            uploading_file_name = os.path.basename(file_path)
        else:
            base_name, extension = os.path.splitext(file_path)
            new_file_path = f"{base_name} {rows_to_skip + 1}-{rows_to_skip + rows_to_read}{extension}"
            uploading_file_name = os.path.basename(new_file_path)
        if path_after_current_day is None:
            upload_url = self.endpoint + f"drive/items/root:/Holland/Reports/{current_day}/{uploading_file_name}:/content"
        else:
            upload_url = self.endpoint + f"drive/items/root:/Holland/Reports/{current_day}/{path_after_current_day}/{uploading_file_name}:/content"


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

    def get_item_id(self, name, path_in_onedrive="/Holland/Reports"):
        url = self.endpoint + f"drive/root:{path_in_onedrive}:/children"
        response = requests.get(url, headers=self.default_header(access_token=self.access_token))

        data = response.json()
        for item in data["value"]:
            if item["name"] == name:
                return item["id"]

    def download_file_to_tmp(self, download_url, file_name, is_report=False):
        response = requests.get(download_url,
                                headers=self.auth_manager.get_default_header(access_token=self.access_token))

        if response.status_code == 200:
            print(response.content)
            if is_report:
                folder_path = "/tmp/text_reports"
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                with open(f"{folder_path}/{file_name}", "wb") as f:
                    f.write(response.content)
            else:
                with open(f"/tmp/{file_name}", "wb") as f:
                    f.write(response.content)
        else:
            print(f"Помилка при завантаженні файлу {file_name}: {response.status_code} - {response.text}")

    def download_reports_to_tmp(self, current_day=DATETIME):
        upload_url = self.endpoint + f"drive/items/root:/Holland/Reports/{current_day}:/children"
        response = requests.get(url=upload_url,
                                headers=self.default_header)
        if response.status_code == 200:
            files = response.json().get("value", [])
            for file in files:
                if "report" in file.get("name", "").lower():
                    file_name = file.get("name")
                    file_id = file.get("id")
                    download_url = self.endpoint + f"drive/items/{file_id}/content"
                    self.download_file_to_tmp(download_url, file_name, is_report=True)
        else:
            print(f"Error in download_reports_to_tmp {response.status_code} - {response.text}")

    def is_list_folder_created(self, current_day=DATETIME):
        upload_url = self.endpoint + f"drive/items/root:/Holland/Reports/{current_day}:/children"
        print(upload_url)
        response = requests.get(url=upload_url,
                                headers=self.default_header)
        if response.status_code == 200:
            items = response.json().get('value', [])
            return any(item['name'] == 'Lists' and item['folder'] is not None for item in items)
        else:
            return response.json()

    def is_current_day_folder_created(self, current_day=DATETIME):
        upload_url = self.endpoint + f"drive/items/root:/Holland/Reports:/children"
        response = requests.get(url=upload_url,
                                headers=self.default_header)
        if response.status_code == 200:
            items = response.json().get('value', [])
            return any(item['name'] == current_day and item['folder'] is not None for item in items)
        else:
            return response.json()

    def create_current_day_folder(self, current_day=DATETIME):
        create_url = self.endpoint + f"drive/items/root:/Holland/Reports:children"
        payload = {
            "name": current_day,
            "folder": {},
            "@microsoft.graph.conflictBehavior": "rename"
        }
        response = requests.post(url=create_url, headers=self.default_header, json=payload)
        return response.json()

    def create_lists_folder(self, current_day=DATETIME):
        create_url = self.endpoint + f"drive/items/root:/Holland/Reports/{current_day}:children"
        payload = {
            "name": "Lists",
            "folder": {},
            "@microsoft.graph.conflictBehavior": "rename"
        }
        response = requests.post(url=create_url, headers=self.default_header, json=payload)
        return response.json()

# folder_path = os.path.join(os.path.dirname(os.getcwd()), "tmp/text_reports")
# file_list = (os.listdir(folder_path))
# for file_name in file_list:
#     file_path = os.path.join(folder_path, file_name)
#     onedrivemanager.upload_file_to_onedrive(file_path=file_path, rows_to_read=1, rows_to_skip=0)
