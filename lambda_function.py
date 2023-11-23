import json

from modules.Otomoto.otomoto_manager import OtomotoManager
from modules.excel_handler import ExcelHandler
from modules.onedrive_manager import OneDriveManager


def lambda_handler(event, context):
    otomoto_manager = OtomotoManager(excel_file_name=r"Volodumurs_tested_file.xlsx", sheet_name="OtoMoto")
    otomoto_manager.create_next_twenty_adverts()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


# lambda_handler(event=None, context=None)