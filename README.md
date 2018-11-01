# api-indentikey
API for identi-key system 


## Current Flask Project Structure

https://medium.freecodecamp.org/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563


## Other Resources

https://docs.sqlalchemy.org/en/latest/dialects/mysql.html#module-sqlalchemy.dialects.mysql.mysqldb


## Important Things to consider

#### Connect String for sqlalchemy: mysql

mysql+pymysql://username:password@host/dbname


#### Run Project

python3 manage.py run

#### Migrate model changes and update migration changes

This is done everytime a change is made in one of our models.

#### Migration Commit

python manage.py db migrate --message 'Added public_id to users model'

#### Update Migration Changes

python manage.py db upgrade

#### To update project requirements file

pip3 freeze > requirements.txt


#### Remember to:

yum install MySQL-python

#### In Ubuntu 18.04 for mysql to work

pip3 install flask_migrate

#### Install  php7.2-mysql for ubuntu

sudo apt install php7.2-mysql





