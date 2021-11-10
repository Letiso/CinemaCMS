migrun: migrate run

runf: port_fix run

run:
	python3 cinema/manage.py runserver

migrate:
	python3 cinema/manage.py makemigrations
	python3 cinema/manage.py migrate

port_fix:
	sudo fuser -k 8000/tcp