import json

from modules.otomoto.otomoto_manager import OtomotoManager
from modules.src_image_url_creator import SrcImageUrlCreator


def lambda_handler(event, context):
    otomoto_manager = OtomotoManager(excel_file_name=r"otomoto.xlsx", sheet_name="otomoto")
    otomoto_manager.create_all_adverts()

    # src_image_url_creator = SrcImageUrlCreator()
    # src_image_url_creator.generate_links()

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


# lambda_handler(event=None, context=None)