import os

import boto3


s3_bucket_name = "prod-spaceplus-automation"


class S3LinkGenerator:
    def _get_files_in_folder(self, folder_path):
        file_list = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_list.append(os.path.join(root, file))
        file_names = [os.path.basename(file_path) for file_path in file_list]

        return file_list, file_names

    def _get_list_and_upload_photos(self, path_to_save_photos: str, file_name: str):
        # s3_object_key = None
        file_list, file_names = self._get_files_in_folder(path_to_save_photos)
        s3 = boto3.client("s3")

        for file_path, file_name in zip(file_list, file_names):
            s3.upload_file(file_path, s3_bucket_name, file_name)
            try:
                s3.head_object(Bucket=s3_bucket_name, Key=file_name)
                print(f"Файл {file_name} успішно завантажено на S3.")
            except Exception as e:
                print(f"Помилка: {e}. Файл {file_name} не був знайдений на S3.")

        return file_list

    def _del_photos(self):
        pass

    def generate_public_urls(self, path_to_save_photos: str, file_name):
        file_list = self._get_list_and_upload_photos(path_to_save_photos=path_to_save_photos, file_name=file_name)
        s3 = boto3.client("s3")

        public_urls = []

        for file_path in file_list:
            s3_object_key = os.path.basename(file_path)
            url = s3.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": s3_bucket_name, "Key": s3_object_key},
                ExpiresIn=3600  # Тут ви можете вказати термін дії посилання в секундах (наприклад, 1 година)
            )
            public_urls.append(url)
        if public_urls:
            return public_urls
        else:
            return None
