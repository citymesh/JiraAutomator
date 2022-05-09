import json
import logging
from os import environ
from typing import Dict

import requests
from requests.exceptions import HTTPError

base_url = environ.get('JiraBaseUrl')
token = environ.get('JiraToken')


def get_all_boards() -> Dict:
    """ request all boards from Jira Cloud """
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json"
    }
    url = f'{base_url}/board'
    try:
        response = requests.request(
            method="GET",
            url=url,
            headers=headers,
            timeout=5
        )
    except HTTPError as http_err:
        logging.error(f'An HTTP error occurred connecting to Jira cloud: {http_err}')
    except Exception as err:
        logging.error(f'An error occurred connecting to Jira Cloud: {err}')
    else:
        if response.status_code == 200:
            return response.json()
        logging.error(f'Unable to fetch api data: {response.status_code}, {response.json()}')
    return {}


def move_issue_to_board(issue_key: str, board_id: str) -> None:
    """ move issue to board """
    response = None
    url = f'{base_url}/board/{board_id}/issue'
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "issues": [
            issue_key
        ]
    })
    try:
        response = requests.request(
            method="POST",
            url=url,
            headers=headers,
            data=payload,
            timeout=5
        )
    except HTTPError as http_err:
        logging.error(f'An HTTP error occurred connecting to Jira cloud: {http_err}')
    except Exception as err:
        logging.error(f'An error occurred connecting to Jira Cloud: {err}')
        if response.status_code == 200:
            logging.info(response.text)
    return
