# JiraAutomator

A simple Azure Function app. This app has an endpoint that accepts post requests for issues of which the status
has changed.
If the status is anything else than 'open' the issue is moved from the backlog to the corresponding board.
 
## Development environment

Create virtual environment and install (dev) dependencies

`pipenv sync --dev`

## Usage

`func start`

## Authors

-  Cédric Verhaeghe <cedric.verhaeghe@citymesh.com>
