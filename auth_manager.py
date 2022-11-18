import json
import os

import google.oauth2.credentials

from _constants import USER_CREDENTIALS_FILE


def save_user_credentials(credentials):
    with open(USER_CREDENTIALS_FILE, "w") as file:
        json.dump(credentials_to_dict(credentials), file, indent=2)


def load_user_credentials():
    with open(USER_CREDENTIALS_FILE, "r") as file:
        return google.oauth2.credentials.Credentials(**json.loads(file.read()))


def remove_user_credentials():
    os.remove(USER_CREDENTIALS_FILE)


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes
    }
