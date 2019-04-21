# se-project
Software Engineering project, 2nd semester 2018-19

## Setup enviornment
1. Python env
  - conda create --name django python=3.6.5
  - conda activate django (or source activate django)
  - pip install -r requirements.txt
  
2. Database setup
  - sudo apt update && sudo apt upgrade
  - Follow this [tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04)
  
3. create database and give permissions
  - sudo -i -u postgres
  - psql
  - create user se19 with password '12qwaszx';
  - create database "openstore";
  - grant all on database "openstore" to se19;
  - \q
  - exit
  
4. Test
  - python manage.py makemigrations
  - python manage.py migrate
  - python manage.py runserver
  
 
