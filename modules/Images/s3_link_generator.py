import os

import boto3


s3_bucket_name = "prod-spaceplus-automation"


class S3LinkGenerator:
    def _get_files_in_folder(self, folder_path):
        file_list = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_list.append(os.path.join(root, file))
        return file_list

    def _get_list_and_upload_photos(self, path_to_save_photos: str):
        # s3_object_key = None
        file_list = self._get_files_in_folder(path_to_save_photos)
        for file_path in file_list:
            with open(file_path, "rb") as file:
                s3_object_key = os.path.basename(file_path)
                # Завантаження файлу на Amazon S3
                s3 = boto3.client("s3")
                s3.upload_fileobj(file, s3_bucket_name, s3_object_key)
        return file_list

    def _del_photos(self):
        pass

    def generate_public_urls(self, path_to_save_photos: str):
        file_list = self._get_list_and_upload_photos(path_to_save_photos=path_to_save_photos)
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
