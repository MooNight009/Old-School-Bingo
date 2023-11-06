import datetime

import requests

from local import API

headers = {
    'User-Agent': API.WOM_USER_AGENT,
    'x-api-key': API.WOM_API_KEY
}


def update_user(name):
    response = requests.post(f'https://api.wiseoldman.net/v2/players/{name}/')
    return check_response(response)

def get_user(name):
    response = requests.get(f'https://api.wiseoldman.net/v2/players/{name}/')
    return check_response(response)


def get_gained(name, start_date, end_date=None):
    # Set end_date to current if None
    if end_date is None:
        end_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    response = requests.get(
        f'https://api.wiseoldman.net/v2/players/{name}/gained?startDate={start_date}&endDate={end_date}')
    return check_response(response)


def check_response(response):
    # if response.status_code != 200 or response.status_code != 201:
    #     print(response.json())
    return response
