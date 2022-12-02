import json
import os
from datetime import datetime

import requests


def matches():
    base_url = "http://api.cup2022.ir/api/v1"  # NOQA
    user_info_file = "wc_user_info.json"

    def register(name, email, password):
        print("Registering WC user...")
        return requests.post(f"{base_url}/user", json={
            "name": name,
            "email": email,
            "password": password,
            "passwordConfirm": os.getenv("WC_PASSWORD")
        }).json().get("data").get("token")

    def login(email, password):
        print("Logging-in WC user...")
        return requests.post(f"{base_url}/user/login", json={
            "email": email,
            "password": password
        }).json().get("data").get("token")

    if not os.path.isfile(user_info_file):
        with open(user_info_file, "w") as file:
            json.dump({"registered": False}, file, indent=2)

    with open(user_info_file, "r") as file:
        user_info = json.load(file)

    if not user_info.get("registered"):
        user_name = os.getenv("WC_NAME")
        user_email = os.getenv("WC_EMAIL")
        user_password = os.getenv("WC_PASSWORD")
        token = register(user_name, user_email, user_password)
        with open(user_info_file, "w") as file:
            json.dump({
                "registered": True,
                "email": user_email,
                "password": user_password
            }, file, indent=2)
    else:
        token = login(user_info.get("email"), user_info.get("password"))

    def readable_match(item):
        return {
            "id": item.get("_id"),
            "final": item.get("finished").upper() == "TRUE",
            "date": datetime.strptime(item.get("local_date"), "%m/%d/%Y %H:%M"),
            "home": item.get("home_team_en"),
            "away": item.get("away_team_en"),
            "home_score": item.get("home_score"),
            "away_score": item.get("away_score")
        }

    return sorted(map(readable_match, requests.get(f"{base_url}/match", headers={"Authorization": f"Bearer {token}"}).json().get("data")), key=lambda i: i.get("date"))
