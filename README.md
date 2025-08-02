# Learning-Django
Learning Django rest framwork

## Database command:
- Make migration: `python real_world/manage.py makemigrations api --name "<migration name>"`
- Command Run migration: `python real_world/manage.py migrate api`

## Server command:
- Command start server: `python real_world/manage.py runserver`

## Show setting:
- Enable virtual enviroment: `source env/bin/activate`
- Install packages: `pip install -r .requirements`
- Get urls: `python real_world/manage.py show_urls`

## Create reauirement by pip-chill:
- Install pip-chill: `pip install pip-chill`
- Create file requirement: `pip-chill > .requirements`

## Testing and coverage:
- Run test coverage: `coverage run --source='api' real_world/manage.py test api`
- Generate coverage report: `coverage report`
- Generate HTML coverage report: `coverage html`
