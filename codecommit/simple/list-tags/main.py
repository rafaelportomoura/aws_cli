import os
import json
from dotenv import dotenv_values

config ={**dotenv_values()}

tenant=config.get('TENANT')
region=config.get('REGION')
arn_code=config.get('ARN_CODE')
repository=config.get('REPOSITORY')
arn=f'arn:aws:codecommit:{region}:{arn_code}:{repository}'

tags= json.loads(os.popen(f'aws codecommit list-tags-for-resource --resource-arn {arn}').read())

print(tags)