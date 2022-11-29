import secrets
import threading
import webbrowser
from threading import Thread

import flask
import google_auth_oauthlib.flow
import requests
from werkzeug.serving import make_server

from _user_credentials import *


class ServerThread(threading.Thread):
    def __init__(self, web_app):
        threading.Thread.__init__(self)
        self.server = make_server('localhost', 8080, web_app)
        self.ctx = web_app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        Thread(target=self.server.shutdown).start()


CLIENT_SECRETS_FILE = "client_secret.json"


def authorize_user(scopes, load_from_cache=False):
    if load_from_cache and has_user_credentials():
        return load_user_credentials()

    # Revoking previous user credentials
    if has_user_credentials():
        print("User has credentials; removing it first...")
        credentials = load_user_credentials()
        result = requests.post("https://oauth2.googleapis.com/revoke",
                               params={"token": credentials.token},
                               headers={"content-type": "application/x-www-form-urlencoded"})
        status_code = getattr(result, "status_code")
        if status_code != 200:
            print("Warn :: Error while removing user credentials!")
        remove_user_credentials()
        print("User credentials removed!")

    print("Authorizing user...")

    # Starting the server
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    app = flask.Flask('Python-Authorize-Google')
    app.secret_key = secrets.token_hex()
    server = ServerThread(app)
    server.start()
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=scopes)
    flow.redirect_uri = "http://localhost:8080/oauth2callback"
    authorization_url, state = flow.authorization_url(access_type="offline", include_granted_scopes="true")
    print("Server started, now redirecting user in the browser...")
    webbrowser.open(authorization_url)

    @app.route("/oauth2callback")
    def oauth2callback():
        flow_callback = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=scopes, state=state)
        flow_callback.redirect_uri = flask.url_for("oauth2callback", _external=True)
        authorization_response = flask.request.url
        flow_callback.fetch_token(authorization_response=authorization_response)
        save_user_credentials(flow_callback.credentials)
        server.shutdown()
        print("Authorized...!")
        return "Authorized...!"

    server.join()
    return load_user_credentials()
