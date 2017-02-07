import json

CREDS_FILE = "credentials.json"
API_KEY_KEY = "api_key"
DEBUG_KEY = "debug"


def get_config(name):
    with open(CREDS_FILE, 'r') as data_file:  # b for binary
        data = json.loads(data_file.read())
    return data[name]