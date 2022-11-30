import os

import googleapiclient.discovery

import _sheets_world_cup_row as sheet_row
import _world_cup_api as wc
from _authorize import authorize_user

wc_matches = wc.matches()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_ID = os.getenv("SHEET_ID")
credentials = authorize_user(SCOPES, load_from_cache=True)
service = googleapiclient.discovery.build("sheets", "v4", credentials=credentials)


def get_matches_in_sheet():
    out = {}
    rows = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range="M2:N").execute().get('values', [])
    for i, row in enumerate(rows):
        out.update({
            row[0]: {
                "final": row[1] == "YES",
                "row_index": i + 1
            },
        })
    return out


sheet_rows = get_matches_in_sheet()
last_row_index = len(sheet_rows)
for match in wc_matches:
    match_id = match.get("id")
    if match_id not in sheet_rows:
        print(f"Inserting match {match_id}...")
        last_row_index += 1
        service.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID, body=sheet_row.new_row(last_row_index, f"{match.get('home')} - {match.get('away')}", match_id)).execute()
        sheet_rows.update({
            match_id: {
                "final": False,
                "row_index": last_row_index
            }
        })

not_updated_rows = {k: v for k, v in sheet_rows.items() if not v.get("final")}
if not_updated_rows:
    finalized_matches = [match for match in wc_matches if match.get("finished")]
    for match in finalized_matches:
        match_id = match.get("id")
        if match_id in not_updated_rows:
            print(f"Finalizing match {match_id}...")
            row_index = not_updated_rows.get(match_id).get("row_index")
            service.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID, body=sheet_row.finalize_row(row_index, match.get("home_score"), match.get("away_score"))).execute()
