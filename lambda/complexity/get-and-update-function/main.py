import os
import json
import sys
from dotenv import dotenv_values

config ={**dotenv_values()}

region = config.get('REGION')
function_name = config.get('FUNCTION_NAME')

key = sys.argv[1]
value = sys.argv[2]

def os_return_object(_command):
  return json.loads(os.popen(_command).read())

def checkIfHaveEnvironmentVariables(_configuration):
  if 'Environment' in _configuration:
    if 'Variables' in _configuration['Environment']:
      return bool(1)
  return bool(0)

def returnVariableCommand(_key,_value,_variables):
  _variable_command = ''
  _finded = bool(0)
  for _loop_key in _variables:
    if _loop_key==_key:
      _variables[_loop_key]=_value
      _finded = bool(1)
    
    _variable_command += f'{_loop_key}={_variables[_loop_key]},'

  if not _finded: 
    _variable_command += f'{_key}={_value},'

  return _variable_command[:len(_variable_command)-1]

AWS_LAMBDA='aws lambda'
GET_FUNCTION_CONFIGURATION = 'get-function-configuration'
REGION = f'--region {region}'
FUNCTION_NAME = f'--function-name {function_name}'
GET_FUNCTION_CONFIGURATION_COMMAND=f'{AWS_LAMBDA} {GET_FUNCTION_CONFIGURATION} {REGION} {FUNCTION_NAME}'


function_configuration = os_return_object(GET_FUNCTION_CONFIGURATION_COMMAND)

variables={}

if checkIfHaveEnvironmentVariables(function_configuration):
  variables=function_configuration['Environment']['Variables']


variable_command = returnVariableCommand(key,value,variables)

UPDATE_FUNCTION_CONFIGURATION = 'update-function-configuration'
ENVIRONMENT='--environment'
ENVIRONMENT_VARIABLES=f'{ENVIRONMENT} "Variables={{{variable_command}}}"'

UPDATE_FUNCTION_CONFIGURATION_COMMAND=f'{AWS_LAMBDA} {UPDATE_FUNCTION_CONFIGURATION} {REGION} {FUNCTION_NAME} {ENVIRONMENT_VARIABLES}'


update_function_configuration = os_return_object(UPDATE_FUNCTION_CONFIGURATION_COMMAND)

print(update_function_configuration['Environment']['Variables'])