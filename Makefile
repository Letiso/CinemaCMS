
reload: stop run
rebuild: down build

run:
	docker-compose up
build:
	docker-compose up --build

#stop:
#	sudo fuser -k 8000/tcp
stop:
	docker-compose stop
down:
	docker-compose down

# Works only for active containers | You have to run docker first
migrate:
	docker exec -it cinemacms-daphne-1 python3 manage.py makemigrations
	docker exec -it cinemacms-daphne-1 python3 manage.py migrate

su:
	docker exec -it cinemacms-daphne-1 python3 manage.py createsuperuser