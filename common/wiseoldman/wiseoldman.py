import datetime
import json
import os.path

import requests

headers = {
    'User-Agent': os.environ['WOM_USER_AGENT'],
    'x-api-key': os.environ['WOM_API_KEY'],
    'Content-type': 'application/json'
}


def update_user(name):
    """
        Updates a user profile in WOM
    """
    response = requests.post(f'https://api.wiseoldman.net/v2/players/{name}/', headers=headers)
    return check_response(response)


def get_user(name):
    """
        Returns the latest user profile in WOM
    """
    response = requests.get(f'https://api.wiseoldman.net/v2/players/{name}/', headers=headers)
    return check_response(response)


def get_gained(name, start_date, end_date=None):
    """
        Returns the gained amount of a profile from start_date
        end_date default is now
    """
    # Set end_date to current if None
    if end_date is None:
        end_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    response = requests.get(
        f'https://api.wiseoldman.net/v2/players/{name}/gained?startDate={start_date}&endDate={end_date}',
        headers=headers)
    return check_response(response)


def create_competition(bingo):
    data = {
        "title": bingo.name,
        "metric": "overall",
        "startsAt": bingo.start_date.strftime("%Y-%m-%dT%H:%M:%S"),
        "endsAt": bingo.end_date.strftime("%Y-%m-%dT%H:%M:%S"),
        "teams": [
            {
                "name": "test",
                "participants": [
                    "osb"
                ]
            }
        ]
    }
    data_json = json.dumps(data)
    response = requests.post(f'https://api.wiseoldman.net/v2/competitions', headers=headers, data=data_json)
    bingo.competition_id = response.json()['competition']['id']
    bingo.competition_verification_code = response.json()['verificationCode']
    bingo.save()
    return response


def update_competition(bingo):
    data = {
        "verificationCode": bingo.competition_verification_code,
    }
    data_json = json.dumps(data)
    response = requests.post(f'https://api.wiseoldman.net/v2/competitions/{bingo.competition_id}/update-all',
                             headers=headers, data=data_json)
    return response


def update_team(team, older_name=None):
    players = team.playerbingodetail_set.all()

    # Get all the account names
    account_names = []
    for player in players:
        account_names += player.account_names.split(',')

    # Delete the team
    data = {
        "verificationCode": team.bingo.competition_verification_code,
        "teamNames": [older_name if older_name is not None else team.team_name]
    }
    data_json = json.dumps(data)
    response_delete = requests.delete(f'https://api.wiseoldman.net/v2/competitions/{team.bingo.competition_id}/teams',
                                      headers=headers, data=data_json)

    # Create another team
    data = {
        "verificationCode": team.bingo.competition_verification_code,
        "teams": [
            {
                "name": team.team_name,
                "participants": account_names
            },
        ]
    }
    data_json = json.dumps(data)
    response_create = requests.post(f'https://api.wiseoldman.net/v2/competitions/{team.bingo.competition_id}/teams',
                                    headers=headers, data=data_json)


    return response_delete, response_create


def update_team_tile(team_tile, type_names):
    update_competition(team_tile.team.bingo)

    score = 0
    for type_name in type_names:
        params = {
            "metric": type_name
        }
        response = requests.get(f'https://api.wiseoldman.net/v2/competitions/{team_tile.team.bingo.competition_id}/',
                                headers=headers, params=params)
        print(response.json())
        players = response.json()['participations']
        for player in players:
            if player['teamName'] == team_tile.team.team_name:
                score += int(player['progress']['gained'])

    return score


def remove_team(team):
    data = {
        "verificationCode": team.bingo.competition_verification_code,
        "teamNames": [team.team_name]
    }
    data_json = json.dumps(data)
    response_delete = requests.delete(f'https://api.wiseoldman.net/v2/competitions/{team.bingo.competition_id}/teams',
                                      headers=headers, data=data_json)

    return response_delete


# TODO: Add delete() of a bingo model
def delete_competition(bingo):
    data = {
        "verificationCode": bingo.competition_verification_code,
    }
    data_json = json.dumps(data)
    response = requests.delete(f'https://api.wiseoldman.net/v2/competitions/{bingo.competition_id}', headers=headers,
                               data=data_json)

    return response


def check_response(response):
    # if response.status_code != 200 or response.status_code != 201:
    #     print(response.json())
    return response
