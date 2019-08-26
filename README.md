# Yandex Task
This is an entrance test for yandex backend school, powered by Flask. It saves and analyzes data from provider.
## Getting Started
Below is some instructions to get the project building on your own. To see how to deploy project on server, see the server deploying section. To see how to deploy project on your machine for development and testing, see the development section.

## Server Deploying Section
Firstly, connect to your server using ssh
```
ssh username@ip
```
Next, update and install needful packages
```
sudo apt install build-essential
sudo apt-get install nginx supervisor python3 python3-virtualenv python3-psycopg2 libpq-dev python3-dev postgresql postgresql-contrib
```
Then, clone project from github repo, create virtual enviroment and install all python packages
```
git clone --single-branch --branch server https://github.com/Plunkerusr/yandex_task.git
cd yandex_task
virtualenv -p python3 .env
pip3 install -r requirements/production.txt
```
Create database with your own variables database_name, database_user and database_user_password
```
sudo -u postgres psql
CREATE USER database_user WITH password 'database_user_password';
CREATE DATABASE database_name OWNER database_user;
GRANT ALL privileges ON DATABASE database_name TO database_user;
\q
```
Create config.json for setup some project variables
```
nano /etc/config.json
```
```
{     
        "DATABASE_URL": "postgres://database_user:database_user_password@127.0.0.1:5432/database_name",
        "SECRET_KEY": "b752cd812b54ff790adbc13d371a98ea17e5af08bb6d2b2d88c96099e8d3eb9e"
}
```
Create database
```
cd app
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
cd ..
```
Next, add nginx configuration file.
```
nano /etc/nginx/sites-enabled/default
```
```
server {
        listen 8080;
        server_name 139.162.227.5;

        location / {
                proxy_pass http://localhost:8000;
                include /etc/nginx/proxy_params;
                proxy_redirect off;
        }
}
```
Then, restart nginx
```
systemctl restart nginx
```
Now, we should setup supervisor
```
sudo mkdir -p /var/log/yandex_task
touch /var/log/yandex_task/yandex_task.err.log
touch /var/log/yandex_task/yandex_task.out.log
```
If you don't know how many cores your machine has, use this command
```
nproc
```
Create supervisor configuration file
```
sudo nano /etc/supervisor/conf.d/yandex_task.conf
```
Change here your linux user instead of username and (2 x $num_cores) + 1 instead of 9.
```
[program: yandex_task]
directory=/username/yandex_task/app
command=/username/yandex_task/.env/bin/gunicorn -w 9 manage:app
user=root
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/yandex_task/yandex_task.err.log
stdout_logfile=/var/log/yandex_task/yandex_task.out.log
```
Restart the supervisor
```
supervisorctl reload
```
For now, everything is done and our server is working
## Development Section
### Requirements
* python3
* python3-virtualenv
* python3-psycopg2
* postgresql
### Installing Project
Then, clone project from github repo, create virtual enviroment and install all python packages
```
git clone https://github.com/Plunkerusr/yandex_task.git
cd yandex_task
virtualenv -p python3 .env
pip3 install -r requirements/development.txt
```
Create database with your own variables database_name, database_user and database_user_password
```
psql
CREATE USER database_user WITH password 'database_user_password';
CREATE DATABASE database_name OWNER database_user;
GRANT ALL privileges ON DATABASE database_name TO database_user;
\q
```
Create virtual enviroment variables for secret_key and database (setup your own secret key)
```
export DATABASE_URL="postgres://database_user:database_user_password@127.0.0.1:5432/database_name"
export SECRET_KEY="your_secret_key"
```
Create database
```
cd app
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
```
### Tests
This project has unit tests. You can test your project by using this command from app folder
```
python3 tests.py
```
### Run local server
You can run this project locally by using this command from app folder
```
python3 manage.py runserver
```
