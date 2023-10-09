import json

from start_program import StartProgram


def lambda_handler(event, context):
    # TODO implement
    start_program = StartProgram()
    start_program.otomoto_test()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
