import os

from imgurpython import ImgurClient

CLIENT_ID = 'f82bcb68847441a'
CLIENT_SECRET = 'd3870caebcf64e7cc4ab0d180204d25b292dc3b6'

# client_id = 'f82bcb68847441a'
# client_secret = 'd3870caebcf64e7cc4ab0d180204d25b292dc3b6'

class ImagesApi:
    # Шлях до фото на вашому локальному комп'ютері
    image_path = 'C:\\Users\\vladi\\OneDrive\\Desktop\\IMG-8277.jpg'

    # Функція для завантаження фото на Imgur і отримання URL
    def create_list_of_img(self, storage_id) -> list[str]:
        folder_path = os.path.join('Data', 'Images', storage_id)
        image_files = os.listdir(folder_path)
        print(image_files)
        return image_files

    def upload_image_to_imgur(self, image_files: list[str]):
        # base_path = os.path.join('Data', 'Images', folder_name, image_name)
        # image_files = os.listdir(base_path)
        # print("bla-bla aaaaaaaaaa", image_files)
        #
        # folder_path = os.path.join('Data', 'Images', folder_name)
        #
        # # Отримуємо список усіх файлів у папці folder_path
        # image_files = os.listdir(folder_path)

        client = ImgurClient(CLIENT_ID, CLIENT_SECRET)


        # image_urls = []
        #
        # # Проходимося по кожному файлу у папці та завантажуємо його на Imgur
        # for image_name in image_files:
        #     image_url = upload_image_to_imgur(folder_name, image_name)
        #     image_urls.append(image_url)
        #
        # client = ImgurClient(CLIENT_ID, CLIENT_SECRET)

        # Завантаження фото
        for folder_name in image_files:
            uploaded_image = client.upload_from_path(folder_name, anon=True)

            # Отримання URL завантаженого фото
            image_url = uploaded_image['link']
            print(image_url)
        # return image_url

    # # Завантаження фото і отримання URL
    # imgur_image_url = upload_image_to_imgur(image_path)
    #
    # # Виведення URL
    # print("URL фото на Imgur:", imgur_image_url)