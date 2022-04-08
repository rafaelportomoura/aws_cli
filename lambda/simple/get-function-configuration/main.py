import os
import json
from dotenv import dotenv_values

config ={**dotenv_values()}

AWS_LAMBDA_COMMAND='aws lambda'
GET_FUNCTION_COMMAND = 'get-function-configuration'

region = config.get('REGION')
function_name = config.get('FUNCTION_NAME')

REGION_COMMAND = f'--region {region}'
FUNCTION_NAME_COMMAND = f'--function-name {function_name}'

print(f'{AWS_LAMBDA_COMMAND} {GET_FUNCTION_COMMAND} {REGION_COMMAND} {FUNCTION_NAME_COMMAND}')

configuration = json.loads(os.popen(f'{AWS_LAMBDA_COMMAND} {GET_FUNCTION_COMMAND} {REGION_COMMAND} {FUNCTION_NAME_COMMAND}').read())

# print(configuration['Environment']['Variables'])
print(configuration)