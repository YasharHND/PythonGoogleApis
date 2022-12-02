import os

import googleapiclient.discovery

from _authorize import authorize_user
from _sheet_world_cup_row import *
from _world_cup_api import matches

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_ID = os.getenv("SHEET_ID")

credentials = authorize_user(SCOPES, load_from_cache=True)
service = googleapiclient.discovery.build("sheets", "v4", credentials=credentials)


def get_matches_in_sheet():
    values = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range="M2:N").execute().get("values", [])
    out = {}
    for i, value in enumerate(values):
        out.update({
            value[0]: {
                "final": value[1] == "YES",
                "row_index": i + 1
            }
        })
    return out


spreadsheet_matches = get_matches_in_sheet()
next_row_index = len(spreadsheet_matches) + 1

batch_update_requests = []
wc_matches = matches()

for match in wc_matches:
    match_id = match.get("id")
    if match_id not in spreadsheet_matches:
        batch_update_requests.extend(new_row(next_row_index, f"{match.get('home')} - {match.get('away')}", match_id))
        spreadsheet_matches.update({
            match_id: {
                "final": "NO",
                "row_index": next_row_index
            }
        })
        next_row_index += 1

not_finalized_rows = {k: v for k, v in spreadsheet_matches.items() if not v.get("final")}
if not_finalized_rows:
    finalized_matches = [match for match in wc_matches if match.get("final")]
    for match in finalized_matches:
        match_id = match.get("id")
        row = spreadsheet_matches.get(match_id)
        batch_update_requests.extend(finalize_row(row.get("row_index"), match.get("home_score"), match.get("away_score")))

if batch_update_requests:
    service.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID, body={"requests": batch_update_requests}).execute()
