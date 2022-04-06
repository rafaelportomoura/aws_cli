import os
import json
from dotenv import dotenv_values

config ={**dotenv_values()}

repository = config.get('REPOSITORY')
branch = config.get('BRANCH')

try:
  branch_data = json.loads(os.popen(f'aws codecommit get-branch --repository-name {repository} --branch-name {branch}').read())
except:
  print('ERRO')

print(branch_data)