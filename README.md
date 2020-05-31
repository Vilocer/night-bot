# night-bot

<div align="center">
  <a href="https://github.com/Vilocer/night-bot-django-webapp">
    <img width="150" height="150" src="https://sun9-28.userapi.com/c851328/v851328430/12f4d2/z_Z837L-q-o.jpg">
  </a>
  <br>
  <br>
</div>


## Installation

`$ git clone https://github.com/Vilocer/night-bot`

`$ apt install python3 python3-venv python3-pip`

`$ python3 -m pip install pipenv && pipenv install`

`$ chmod +x bin/*.sh`

## Configuration

- `$ ./bin/add_env.sh` - Configure Env Variables

- gunicorn_config.py - Gunicorn Config

- bin/start_gunicorn.sh - Start gunicorn server command

- web/config/settings.py - Django Settings

## Run

### Heroku

- Procfile already exist. You only need to add vars in project settings

### Unix

`$ ./bin/start_gunicorn.sh` - to start prod. djangk serve

`$ pipenv run python web/manage.py runserver` - to start dev. django server

`$ pipenv run bot/bot.py` - to run vk bot 
