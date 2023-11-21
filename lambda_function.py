import json

from modules.Otomoto.otomoto_manager import OtomotoManager
from modules.excel_handler import ExcelHandler
from modules.onedrive_manager import OneDriveManager


def lambda_handler(event, context):
    # otomoto_manager = OtomotoManager(excel_file_name=r"Final_exel_file 21-11-2023.xlsx", sheet_name="OtoMoto")
    # otomoto_manager.create_next_twenty_adverts()

    excel_handler = ExcelHandler()
    excel_handler.update_excel_from_success_report(current_day="21-11-2023")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


# lambda_handler(event=None, context=None)