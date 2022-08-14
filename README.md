# petproject
# download project from repo
https://github.com/Artem-1313/petproject.git 
# move to project work directory
cd petproject/newsite
# make migrations

docker-compose run wen python manage.py makemigrations
docker-compose run wen python manage.py migrate
# create a superuser
docker-compose run web python manage.py createsuperuser
# run project
docker-compose up -d
# acces project
http://0.0.0.0:8000/
