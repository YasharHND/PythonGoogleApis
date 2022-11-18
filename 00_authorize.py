import secrets

import flask
import google_auth_oauthlib.flow
import requests

from _constants import *
from auth_manager import *

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
    save_user_credentials(flow.credentials)
    return "Authorized...!"


@app.route("/revoke")
def revoke():
    credentials = load_user_credentials()
    result = requests.post("https://oauth2.googleapis.com/revoke",
                           params={"token": credentials.token},
                           headers={"content-type": "application/x-www-form-urlencoded"})
    status_code = getattr(result, "status_code")
    if status_code == 200:
        remove_user_credentials()
        return "Revoked!"
    else:
        return "Error!"


if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    app.run("localhost", 8080, debug=True)
