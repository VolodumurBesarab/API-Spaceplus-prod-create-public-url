import json

from modules.Otomoto.otomoto_manager import OtomotoManager
from modules.excel_handler import ExcelHandler
from modules.onedrive_manager import OneDriveManager


def lambda_handler(event, context):
    otomoto_manager = OtomotoManager(excel_file_name=r"Final_exel_file.xlsx", sheet_name="OtoMoto")
    otomoto_manager.create_lists()
    # one_drive_manager = OneDriveManager()
    # one_drive_manager.download_reports_to_tmp(current_day="First start progmam reports")
    # otomoto_manager.create_reports_from_base()
    # excel_handler = ExcelHandler()
    # excel_handler.update_excel_from_success_report(current_day="Second start program reports")
    # otomoto_manager = OtomotoManager(excel_file_name=r"Otomoto.xlsx", sheet_name="OtoMoto")
    # otomoto_manager.create_page()
    # try:
    #     # otomoto_manager.create_list_to_create_in_s3()
    #     otomoto_manager.create_reports_from_base()
    #     excel_handler = ExcelHandler()
    #     excel_handler.update_excel_from_success_report()
    # except Exception as e:
    #     print(e)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


# lambda_handler(event=None, context=None)