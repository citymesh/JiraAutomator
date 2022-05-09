import logging
import azure.functions as func
from MoveIssue import jira
from typing import Dict


def main(request: func.HttpRequest):
    post_data = request.get_json()
    issue = {}
    try:
        status = normalize(post_data.get('fields').get('status').get('name'))
        issue['key'] = post_data.get('key')
        issue['project_id'] = post_data.get('fields').get('project').get('id')
    except (ValueError, KeyError):
        return func.HttpResponse('Unable to process request', status_code=400)
    if status != 'open':
        logging.info('Issue status is not \'open\', move to board')
        move_to_board(issue)
    else:
        logging.info('Issue status open, do not move to board')

    return func.HttpResponse('OK', status_code=200)


def move_to_board(issue: Dict) -> None:
    jira_boards = jira.get_all_boards()
    boards = format_boards(jira_boards)
    for project_id in boards:
        if issue['project_id'] == project_id:
            logging.info(f'Project id: {project_id}, board id: {boards[project_id]}')
            jira.move_issue_to_board(issue['key'], boards[project_id])
            return


def normalize(status: str) -> str:
    return status.strip().replace(' ', '_').lower()


def format_boards(jira_boards: Dict) -> Dict:
    raw_data = jira_boards.get('values', {})
    formatted = {}
    for board in raw_data:
        board_id = board.get('id')
        project_id = board.get('location').get('projectId')
        formatted[project_id] = board_id

    return formatted
