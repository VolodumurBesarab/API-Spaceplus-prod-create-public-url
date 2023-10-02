# from modules.one_drive_photo_manager import OneDrivePhotoManager
import builtins
import sys

from modules.Images.images_api import ImagesApi
from modules.Otomoto.otomoto_api import OtomotoApi
from modules.log_creator import LogCreator
from start_program import StartProgram
from modules.Otomoto.otomoto_manager import OtomotoManager

# otomoto_manager = OtomotoManager()

start_program = StartProgram()
# imagesapi = ImagesApi()
# imagesapi.get_list_photos()



start_program.otomoto_test()






# one_drive_photo_manager
# start_program.otomoto_test()
# images_api = ImagesApi()
# folder_path, image_files = images_api.create_list_of_img(storage_id="14848")
# image_urls = images_api.upload_image_to_imgur(folder_path=folder_path ,image_files=image_files)
# print(image_urls)

# otomoto_api = OtomotoApi()
# otomoto_api.create_otomoto_images_collection()
