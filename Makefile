migrun: migrate run

run:
	python3 cinema/manage.py runserver

migrate:
	python3 cinema/manage.py makemigrations
	python3 cinema/manage.py migrate
