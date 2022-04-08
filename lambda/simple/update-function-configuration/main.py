import os
import json
from dotenv import dotenv_values

config ={**dotenv_values()}

AWS_LAMBDA='aws lambda'
UPDATE_FUNCTION_CONFIGURATION = 'update-function-configuration'

region = config.get('REGION')
function_name = config.get('FUNCTION_NAME')

REGION = f'--region {region}'
FUNCTION_NAME = f'--function-name {function_name}'
ENVIRONMENT='--environment'


variables={
  "ID": 'TROCOU',
  "xx": "y"
}

variable_command = ''
for key in variables:
  variable_command += f'{key}={variables[key]},'

variable_command=variable_command[:len(variable_command)-1]

ENVIRONMENT_VARIABLES=f'{ENVIRONMENT} "Variables={{{variable_command}}}"'

COMMAND=f'{AWS_LAMBDA} {UPDATE_FUNCTION_CONFIGURATION} {REGION} {FUNCTION_NAME} {ENVIRONMENT_VARIABLES}'

print(f'{COMMAND}\n')
configuration = json.loads(os.popen(COMMAND).read())

# print(configuration['Environment']['Variables'])
print(configuration)