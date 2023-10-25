import os

import boto3


s3_bucket_name = "Photos"


class S3LinkGenerator:
    def _get_files_in_folder(self, folder_path):
        file_list = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_list.append(os.path.join(root, file))
        return file_list

    def _upload_photos(self, path_to_save_photos: str):
        # s3_object_key = None
        file_list = self._get_files_in_folder(path_to_save_photos)
        for file_path in file_list:
            with open(file_path, "rb") as file:
                s3_object_key = os.path.basename(file_path)
                # Завантаження файлу на Amazon S3
                s3 = boto3.client("s3")
                s3.upload_fileobj(file, s3_bucket_name, s3_object_key)
        return f"Завантажено {len(file_list)} файлів на S3."

    def _del_photos(self):
        pass

    def generate_link(self, folder_name: str):
        pass
