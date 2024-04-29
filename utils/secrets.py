import json
import os

class Secrets:
    """This class will be used to read the secrets from the secrets.py file"""

    def read_gcp_secrets(self):
        try:
            with open('secrets.json', 'r') as f:
                secrets = f.read()
                secrets = json.loads(secrets)
                os.environ['project_id'] = secrets['project_id']
                os.environ['bucket'] = secrets['bucket']
        except Exception as e:
            print(e)
