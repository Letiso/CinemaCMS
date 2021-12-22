
reload: stop run

run:
	python3 cinema/manage.py runserver

stop:
	sudo fuser -k 8000/tcp

migrate:
	python3 cinema/manage.py makemigrations
	python3 cinema/manage.py migrate

celery:
	cd cinema; \
	  celery --app=cinema worker -l INFO

status:
	cd cinema; \
	  celery --app=cinema status