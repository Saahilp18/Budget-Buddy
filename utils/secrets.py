import json
import os

class Secrets:
    """This class will be used to read the secrets from the secrets.py file"""

    def read_gcp_secrets(self):
        try:
            # Read the secrets from secrets.json
            with open('secrets.json', 'r') as f:
                secrets = f.read()
                secrets = json.loads(secrets)

                # Assign secrets to environment variables
                os.environ['project_id'] = secrets['project_id']
                os.environ['bucket'] = secrets['bucket']
        except Exception as e:
            print(e)
