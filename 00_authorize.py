import json
import os
import secrets

import flask
import google.oauth2.credentials
import google_auth_oauthlib.flow
import requests

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

app = flask.Flask(__name__)
app.secret_key = secrets.token_hex()


@app.route("/")
def index():
    with open("authorize.html", "r") as file:
        return file.read()


@app.route("/authorize")
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = flask.url_for("oauth2callback", _external=True)
    authorization_url, state = flow.authorization_url(access_type="offline", include_granted_scopes="true")
    flask.session["state"] = state
    return flask.redirect(authorization_url)


@app.route("/oauth2callback")
def oauth2callback():
    state = flask.session["state"]
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for("oauth2callback", _external=True)
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)
    with open("user_credentials.json", "w") as file:
        json.dump(credentials_to_dict(flow.credentials), file, indent=2)
    return "Authorized...!"


@app.route("/revoke")
def revoke():
    with open("user_credentials.json", "r") as file:
        credentials = google.oauth2.credentials.Credentials(**json.loads(file.read()))
    result = requests.post("https://oauth2.googleapis.com/revoke",
                           params={"token": credentials.token},
                           headers={"content-type": "application/x-www-form-urlencoded"})
    status_code = getattr(result, "status_code")
    if status_code == 200:
        os.remove("user_credentials.json")
        return "Revoked!"
    else:
        return "Error!"


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes
    }


if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    app.run("localhost", 8080, debug=True)
