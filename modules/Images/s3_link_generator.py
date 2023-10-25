import boto3


s3_bucket_name = "Photos"

class S3LinkGenerator:
    def _upload_photos(self, folder_name: str):
        s3_object_key = None
        photos_pass = "/tmp/temp_file.jpg"
        s3 = boto3.client("s3")
        s3.upload_file(photos_pass, s3_bucket_name, s3_object_key)
        pass

    def _del_photos(self):
        pass

    def generate_link(self, folder_name: str):
        pass
