def new_row(index, match_name, match_id):
    return [
        {
            "appendDimension": {
                "dimension": "ROWS",
                "length": 1
            }
        }, {
            "copyPaste": {
                "source": {
                    "startRowIndex": 1,
                    "endRowIndex": 2,
                    "startColumnIndex": 9,
                    "endColumnIndex": 10
                },
                "destination": {
                    "startRowIndex": index,
                    "endRowIndex": index + 1,
                    "startColumnIndex": 9,
                    "endColumnIndex": 10
                },
                "pasteType": "PASTE_FORMULA"
            }
        }, {
            "copyPaste": {
                "source": {
                    "startRowIndex": 1,
                    "endRowIndex": 2,
                    "startColumnIndex": 10,
                    "endColumnIndex": 11
                },
                "destination": {
                    "startRowIndex": index,
                    "endRowIndex": index + 1,
                    "startColumnIndex": 10,
                    "endColumnIndex": 11
                },
                "pasteType": "PASTE_FORMULA"
            }
        }, {
            "copyPaste": {
                "source": {
                    "startRowIndex": 1,
                    "endRowIndex": 2,
                    "startColumnIndex": 11,
                    "endColumnIndex": 12
                },
                "destination": {
                    "startRowIndex": index,
                    "endRowIndex": index + 1,
                    "startColumnIndex": 11,
                    "endColumnIndex": 12
                },
                "pasteType": "PASTE_FORMULA"
            }
        }, {
            "updateCells": {
                "rows": [{
                    "values": [{
                        "userEnteredValue": {"stringValue": match_name}
                    }]
                }],
                "fields": "userEnteredValue",
                "start": {
                    "rowIndex": index,
                    "columnIndex": 0
                }
            }
        }, {
            "updateCells": {
                "rows": [{
                    "values": [{
                        "userEnteredValue": {"stringValue": match_id}
                    }]
                }],
                "fields": "userEnteredValue",
                "start": {
                    "rowIndex": index,
                    "columnIndex": 12
                }
            }
        }, {
            "updateCells": {
                "rows": [{
                    "values": [{
                        "userEnteredValue": {"stringValue": "NO"}
                    }]
                }],
                "fields": "userEnteredValue",
                "start": {
                    "rowIndex": index,
                    "columnIndex": 13
                }
            }
        }
    ]


def finalize_row(index, home_score, away_score):
    return [
        {
            "updateCells": {
                "rows": [{
                    "values": [{
                        "userEnteredValue": {"numberValue": home_score}
                    }]
                }],
                "fields": "userEnteredValue",
                "start": {
                    "rowIndex": index,
                    "columnIndex": 7
                }
            }
        }, {
            "updateCells": {
                "rows": [{
                    "values": [{
                        "userEnteredValue": {"numberValue": away_score}
                    }]
                }],
                "fields": "userEnteredValue",
                "start": {
                    "rowIndex": index,
                    "columnIndex": 8
                }
            }
        }, {
            "updateCells": {
                "rows": [{
                    "values": [{
                        "userEnteredValue": {"stringValue": "YES"}
                    }]
                }],
                "fields": "userEnteredValue",
                "start": {
                    "rowIndex": index,
                    "columnIndex": 13
                }
            }
        }
    ]
