import os
import json
from dotenv import dotenv_values

config ={**dotenv_values()}

tenant=config.get('TENANT')
region=config.get('REGION')
arn_code=config.get('ARN_CODE')
repositories = json.loads(os.popen(f'aws codecommit list-repositories --region={region}').read())

tenant_repositories = []

for repository in repositories['repositories']:
  repository = repository['repositoryName']
  arn=f'arn:aws:codecommit:{region}:{arn_code}:{repository}'
  resource=json.loads(os.popen(f'aws codecommit list-tags-for-resource --resource-arn {arn}').read())
  tags=resource['tags']
  if 'tenant' in tags and tags['tenant'] == tenant:
    tenant_repositories.append(repository)

print(tenant_repositories)
