run:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate

dummy:
	python manage.py shell <dummy.py

