import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = 'TOKEN'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = build('sheets', 'v4', http=httpAuth)


def tax_data(data):
    id = str(data[0] + 1)
    service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f"A{id}:K{id}",
                 "majorDimension": "ROWS",
                 "values": [data]}, ]}).execute()


def tax_transaction(data, id):
    ind = ["N", "P", "R", "T", "V", "X", "Z"]
    data_c = []
    data_all = []
    id0 = str(id + 1)
    if len(data) < 8:
        [[data_c.append(i) for i in _] for _ in data]
        print(data_c)
        service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": f"M{id0}:{ind[len(data) - 1]}{id0}",
                     "majorDimension": "ROWS",
                     "values": [data_c]}, ]}).execute()
    else:
        [[data_c.append(i) for i in _] for _ in data[:7]]
        service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": f"M{id0}:Z{id0}",
                     "majorDimension": "ROWS",
                     "values": [data_c]
                     }, ]}).execute()
        if len(data) == 8:
            data_all = [" - ".join(list(i)) for i in data[7:]]

            service.spreadsheets().values().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={
                    "valueInputOption": "RAW",
                    "data": [
                        {"range": f"AA{id0}",
                         "values": [data_all]
                         }, ]}).execute()
        else:
            data_all = [", ".join([" - ".join(list(i)) for i in data[7:]])]

            service.spreadsheets().values().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={
                    "valueInputOption": "RAW",
                    "data": [
                        {"range": f"AA{id0}",
                         "values": [data_all]
                         }, ]}).execute()
