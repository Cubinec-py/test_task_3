# Test task for Savvy Service company

First, need to create and asset .env file in the root directory. Api token can get from [BotFather](https://t.me/BotFather)
```dotenv
SECRET_KEY=
API_TOKEN=
```
Install dependencies:
```bash
python3 pip install -r requirements.txt
```
Before start project need to make migrations:
```bash
python3 manage.py migrate --settings=core.settings.local
```
To start project:
```bash
python3 manage.py runserver 127.0.0.1:8000 --settings=core.settings.local
```
To create superuser:
```bash
python3 manage.py createsuperuser --settings=core.settings.local
```
Last one, to run telegram bot:
```bash
python3 manage.py start_bot --settings=core.settings.local
```
