import json

from modules.otomoto.otomoto_manager import OtomotoManager


def lambda_handler(event, context):
    otomoto_manager = OtomotoManager(excel_file_name=r"otomoto.xlsx", sheet_name="otomoto")
    otomoto_manager.create_all_adverts()
    # client = boto3.client('lambda')
    # response = client.invoke(
    #     FunctionName='prod-spaceplus-create-advert',
    #     InvocationType='Event',
    #     Payload='{}',
    # )
    # print(response)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


# lambda_handler(event=None, context=None)