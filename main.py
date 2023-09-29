# from modules.one_drive_photo_manager import OneDrivePhotoManager
from modules.Images.images_api import ImagesApi
from start_program import StartProgram
from modules.Otomoto.otomoto_manager import OtomotoManager

# otomoto_manager = OtomotoManager()
start_program = StartProgram()


# one_drive_photo_manager
# start_program.otomoto_test()
images_api = ImagesApi()
folder_path, image_files = images_api.create_list_of_img(storage_id="14848")
images_api.upload_image_to_imgur(folder_path=folder_path ,image_files=image_files)
