import json

from modules.Otomoto.otomoto_manager import OtomotoManager
from start_program import StartProgram


def lambda_handler(event, context):
    otomoto_manager = OtomotoManager(excel_file_name=r"Otomoto.xlsx", sheet_name="OtoMoto")
    otomoto_manager.create_page()
    try:
        otomoto_manager.rename_me()
    except Exception as e:
        print(e)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
