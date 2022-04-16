# Docker-compose shorts
reload: stop run
restart: down run
rebuild: down build

run:
	docker-compose up -d
build:
	docker-compose up -d --build

stop:
	docker-compose stop
down:
	docker-compose down


# Works only for active containers | You have to run docker first
migrate:
	docker exec -it cinemacms-django_asgi-1 python3 manage.py makemigrations
	docker exec -it cinemacms-django_asgi-1 python3 manage.py migrate
db:
	docker exec -it cinemacms-db-1 psql -U postgres postgres
sync_model:
	docker exec -it cinemacms-django_asgi-1 python3 manage.py sync_translation_fields
update_model:
	docker exec -it cinemacms-django_asgi-1 python3 manage.py update_translation_fields

superuser:
	docker exec -it cinemacms-django_asgi-1 python3 manage.py createsuperuser
test_users:
	docker exec -it cinemacms-django_asgi-1 python3 manage.py generate_test_users $(count)
test_sessions:
	docker exec -it cinemacms-django_asgi-1 python3 manage.py generate_movie_sessions $(count)


init_messages:
	docker exec -it cinemacms-django_asgi-1 python3 manage.py makemessages -l ru
	docker exec -it cinemacms-django_asgi-1 python3 manage.py makemessages -l uk
	docker exec -it cinemacms-django_asgi-1 python3 manage.py makemessages -l en

update_js:
	docker exec -it cinemacms-django_asgi-1 python3 manage.py makemessages -d djangojs -a

update_loc:
	docker exec -it cinemacms-django_asgi-1 python3 manage.py makemessages -a

compile_loc:
	docker exec -it cinemacms-django_asgi-1 python3 manage.py compilemessages


#purge:
#	docker exec -it cinemacms-django_asgi-1 celery -A cinema purge
#tasks:
#	docker exec -it cinemacms-django_asgi-1 celery -A cinema inspect scheduled
