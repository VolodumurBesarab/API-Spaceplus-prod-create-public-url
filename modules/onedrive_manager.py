import requests


class OneDriveManager:
    def upload_excel_to_onedrive(self, access_token, file_path, upload_url):
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
