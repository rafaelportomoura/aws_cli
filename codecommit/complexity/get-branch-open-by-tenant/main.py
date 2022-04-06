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

print(f'Before: {tenant_repositories}')


branch = config.get('BRANCH')

repositories_with_deploy_branches = []

for repository in tenant_repositories:
  print(f'\n\nRepository: {repository}')
  try:
    branch_data = json.loads(os.popen(f'aws codecommit get-branch --repository-name {repository} --branch-name {branch}').read())
    repositories_with_deploy_branches.append(repository)
    print(f'✅\t[{repository}]: possui deploy')
  except:
    print(f'❌\t[{repository}]: não possui deploy!')

print(f'\n\n🚀: {repositories_with_deploy_branches}\n\n')