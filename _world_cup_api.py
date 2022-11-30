import json
import os
from datetime import datetime

import requests

BASE_URL = "http://api.cup2022.ir/api/v1"
USER_INFO_FILE = "wc_user_info.json"


def matches():
    def fetch_token():
        def register_user(name, email, password):
            return requests.post(url=f"{BASE_URL}/user", json={
                "name": name,
                "email": email,
                "password": password,
                "passwordConfirm": password
            }).json().get("data").get("token")

        def login(email, password):
            return requests.post(url=f"{BASE_URL}/user/login", json={
                "email": email,
                "password": password
            }).json().get("data").get("token")

        user_name = os.getenv("WC_NAME")
        user_email = os.getenv("WC_EMAIL")
        user_password = os.getenv("WC_PASSWORD")

        if os.path.isfile(USER_INFO_FILE):
            with open(USER_INFO_FILE, "r") as file:
                user_info = json.loads(file.read())
            if user_info.get("registered"):
                return login(user_email, user_password)
        token = register_user(user_name, user_email, user_password)
        with open(USER_INFO_FILE, "w") as file:
            json.dump({"registered": True}, file, indent=2)
        return token

    def readable_match(item):
        return {
            "id": item.get("_id"),
            "date": datetime.strptime(item.get("local_date"), "%m/%d/%Y %H:%M"),
            "finished": item.get("finished").upper() == "TRUE",
            "home": item.get("home_team_en"),
            "away": item.get("away_team_en"),
            "home_score": item.get("home_score"),
            "away_score": item.get("away_score")
        }

    result = requests.get(f"{BASE_URL}/match", headers={"Authorization": f"Bearer {fetch_token()}"}).json().get("data")
    return sorted(map(readable_match, result), key=lambda x: x.get("date"))
