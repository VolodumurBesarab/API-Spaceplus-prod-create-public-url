import os

from imgurpython import ImgurClient

CLIENT_ID = 'f82bcb68847441a'
CLIENT_SECRET = 'd3870caebcf64e7cc4ab0d180204d25b292dc3b6'

# client_id = 'f82bcb68847441a'
# client_secret = 'd3870caebcf64e7cc4ab0d180204d25b292dc3b6'

class ImagesApi:
    # Шлях до фото на вашому локальному комп'ютері
    # image_path = 'C:\\Users\\vladi\\OneDrive\\Desktop\\IMG-8277.jpg'

    # Функція для завантаження фото на Imgur і отримання URL
    def _create_list_of_img(self, storage_name) -> tuple[str, list[str]]:
        try:
            folder_path = os.path.join('Data', 'Images', str(storage_name))
            image_files = os.listdir(folder_path)
            return folder_path, image_files
        except:
            print(f"Folder with photos {storage_name} not found")
            return None

    def upload_image_to_imgur(self, storage_name) -> list[str]:
        if self._create_list_of_img(storage_name=storage_name) is None:
            return None
        folder_path, image_files = self._create_list_of_img(storage_name=storage_name)

        # base_path = os.path.join('Data', 'Images', folder_name, image_name)
        # image_files = os.listdir(base_path)
        # print("bla-bla aaaaaaaaaa", image_files)
        #
        # folder_path = os.path.join('Data', 'Images', folder_name)
        #
        # # Отримуємо список усіх файлів у папці folder_path
        # image_files = os.listdir(folder_path)

        # client = ImgurClient(CLIENT_ID, CLIENT_SECRET)


        # image_urls = []
        #
        # # Проходимося по кожному файлу у папці та завантажуємо його на Imgur
        # for image_name in image_files:
        #     image_url = upload_image_to_imgur(folder_name, image_name)
        #     image_urls.append(image_url)
        #
        client = ImgurClient(CLIENT_ID, CLIENT_SECRET)
        image_urls = []
        # Завантаження фото
        for image_name in image_files:
            final_path = os.path.join(folder_path, image_name)
            print("Download:", final_path)
            try:
                uploaded_image = client.upload_from_path(final_path, anon=True)
                image_url = uploaded_image['link']
                image_urls.append(image_url)
                print("Success")
            except Exception as e:
                print(f"Помилка при завантаженні файлу {final_path}: {str(e)}")
        return image_urls

    def get_list_photos(self):
        client = ImgurClient(CLIENT_ID, CLIENT_SECRET)
        # client.get_account_images(username="spaceplus69", page=1)
        authorization_url = client.get_auth_url("code")
        print(authorization_url)
        authorization_code = input("Введіть код авторизації: ")
        # credentials = client.authorize(authorization_code, 'code')
        # print("Отримано токен доступу:", credentials['access_token'])
        client.get_account_images(username="spaceplus69")
