import os
# from var.variable import TOKEN
import pygsheets
import random

import requests


def send_notify(token, msg, filepath=None, stickerPackageId=None, stickerId=None):
    payload = {'message': msg}
    headers = {
        "Authorization": "Bearer " + token
    }
    if stickerPackageId and stickerId:
        payload['stickerPackageId'] = stickerPackageId
        payload['stickerId'] = stickerId

    if filepath:
        attachment = {'imageFile': open(filepath, 'rb')}
        print(attachment)
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload, files=attachment)
    else:
        print("attachment")
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code, r.text


def what_for_lunch() -> str:
    gs = pygsheets.authorize(service_account_file='google-credentials.json')
    spreadsheet = gs.open_by_url('https://docs.google.com/spreadsheets/d/1K0piS75lQSFEzP7RTcFpriAtUKlQ-7BW_0g7hrOMDtQ/')
    sheet = spreadsheet.worksheet_by_title("Sheet1")
    restaurants = sheet.get_col(1)
    restaurants = list(filter(None, restaurants))
    msg = f'''
閉嘴吧你們這群猶豫不決的人，今天午餐給我去吃 `{random.choice(restaurants)}` !!!!!!!!
'''
    return msg


if __name__ == '__main__':
    token = os.environ.get('TOKEN')
    gs_cred = os.environ.get('GOOGLE_SHEET_CREDENTIALS')
    send_notify(token=token, msg=what_for_lunch())
