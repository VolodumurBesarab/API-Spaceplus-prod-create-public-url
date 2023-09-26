from imgurpython import ImgurClient


class ImagesApi:
# Ваші дані з облікового запису Imgur
        client_id = 'f82bcb68847441a'
        client_secret = 'd3870caebcf64e7cc4ab0d180204d25b292dc3b6'

        # Шлях до фото на вашому локальному комп'ютері
        image_path = 'C:\\Users\\vladi\\OneDrive\\Desktop\\IMG-8277.jpg'

        # Функція для завантаження фото на Imgur і отримання URL
        def upload_image_to_imgur(client_id, client_secret, image_path):
            client = ImgurClient(client_id, client_secret)

            # Завантаження фото
            uploaded_image = client.upload_from_path(image_path, anon=True)

            # Отримання URL завантаженого фото
            image_url = uploaded_image['link']

            return image_url

        # Завантаження фото і отримання URL
        imgur_image_url = upload_image_to_imgur(client_id, client_secret, image_path)

        # Виведення URL
        print("URL фото на Imgur:", imgur_image_url)