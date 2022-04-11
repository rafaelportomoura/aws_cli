import os
import json
import sys
from dotenv import dotenv_values

config ={**dotenv_values()}


# !CONSTANTES

KEY = sys.argv[1]
VALUE = sys.argv[2]
CHANNEL_ID = '123'

region = config.get('REGION')
function_name = config.get('FUNCTION_NAME')


AWS_LAMBDA='aws lambda'
GET_FUNCTION_CONFIGURATION = 'get-function-configuration'
REGION = f'--region "{region}"'
FUNCTION_NAME = f'--function-name "{function_name}"'
GET_FUNCTION_CONFIGURATION_COMMAND=f'{AWS_LAMBDA} {GET_FUNCTION_CONFIGURATION} {REGION} {FUNCTION_NAME}'

CHANGE_BLOCK_LIST =['STAGE','REGION','TENANT']
STAGE_FREE_LIST=['dev','qa','hml']


UPDATE_FUNCTION_CONFIGURATION = 'update-function-configuration'
ENVIRONMENT='--environment'

# !--------------------------------------------------

# ?FUNCTIONS

def os_return_object(_command):
  return json.loads(os.popen(_command).read())

def checkIfHaveEnvironmentVariables(_configuration):
  if 'Environment' in _configuration:
    if 'Variables' in _configuration['Environment']:
      return bool(1)
  return bool(0)

def returnVariables(_key,_value,_variables):
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

def speak(_channel_id, _message):
  print(_channel_id, _message)

def validate(_variables,_key):
  try:

    if ('STAGE' in _variables) and (not _variables['STAGE'] in STAGE_FREE_LIST):
      raise Exception('Não é permitido alterar variavel neste ambiente pelo bot!')

    if _key in CHANGE_BLOCK_LIST:
      raise Exception('Não é permitido alterar esta variavel!')

    if len(_key) < 2:
      raise Exception('A chave tem que ter o número de caracteres maior igual a 2')
  
    return bool(1)

  except Exception as e:
    speak(CHANNEL_ID,str(e))
    return bool(0)

  

def main(key,value):
  print(GET_FUNCTION_CONFIGURATION_COMMAND)
  function_configuration = os_return_object(GET_FUNCTION_CONFIGURATION_COMMAND)
  variables={}


  if checkIfHaveEnvironmentVariables(function_configuration):
    variables=function_configuration['Environment']['Variables']

  if not validate(variables,key):
    raise Exception('Operação inválida!')

  
  variables = returnVariables(key,value,variables)
  ENVIRONMENT_VARIABLES=f'{ENVIRONMENT} "Variables={{{variables}}}"'
  UPDATE_FUNCTION_CONFIGURATION_COMMAND=f'{AWS_LAMBDA} {UPDATE_FUNCTION_CONFIGURATION} {REGION} {FUNCTION_NAME} {ENVIRONMENT_VARIABLES}'
  update_function_configuration = os_return_object(UPDATE_FUNCTION_CONFIGURATION_COMMAND)



# ?-------------------------------------------------------

try:
  main(KEY,VALUE)
except Exception as e:
  print(str(e))