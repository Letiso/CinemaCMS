
reload: stop run

run:
	docker-compose up --build

#stop:
#	sudo fuser -k 8000/tcp
stop:
	docker-compose down

# Works only for active containers | You have to run docker first
migrate:
	docker exec -it cinemacms-daphne-1 python3 cinema/manage.py makemigrations
	docker exec -it cinemacms-daphne-1 python3 cinema/manage.py migrate
