import os
import json
from dotenv import dotenv_values

config ={**dotenv_values()}

region = config.get('REGION')

repositories = json.loads(os.popen(f'aws codecommit list-repositories --region={region}').read())

arnArray = []

for repository in repositories['repositories']:
  repositoryName = repository['repositoryName']
  repository_data = json.loads(os.popen(f'aws codecommit get-repository --repository-name {repositoryName}').read())
  repositoryMetadata = repository_data['repositoryMetadata']
  arnArray.append(repositoryMetadata['Arn'])

print(arnArray)