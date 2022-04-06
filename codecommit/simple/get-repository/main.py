import os
import json
from dotenv import dotenv_values

config ={**dotenv_values()}

repository = config.get('REPOSITORY')

repository_data = json.loads(os.popen(f'aws codecommit get-repository --repository-name {repository}').read())

print(repository_data)
