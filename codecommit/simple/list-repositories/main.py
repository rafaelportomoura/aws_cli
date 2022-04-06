import os
import json
from dotenv import dotenv_values

config ={**dotenv_values()}

region = config.get('REGION')

repositories = json.loads(os.popen(f'aws codecommit list-repositories --region={region}').read())

print(repositories)