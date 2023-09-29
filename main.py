# from modules.one_drive_photo_manager import OneDrivePhotoManager
from modules.Images.images_api import ImagesApi
from start_program import StartProgram
from modules.Otomoto.otomoto_manager import OtomotoManager

# otomoto_manager = OtomotoManager()
start_program = StartProgram()


# one_drive_photo_manager
# start_program.otomoto_test()
images_api = ImagesApi()
images_api.create_list_of_img(storage_id="14848")
