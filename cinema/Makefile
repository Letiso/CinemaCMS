# project docker-compose file related
django_asgi_server:
	python3 manage.py migrate --no-input
	python3 manage.py collectstatic --no-input
	gunicorn --bind 0.0.0.0:8000 cinema.asgi -w 4 -k uvicorn.workers.UvicornWorker --reload
	#python3 manage.py runserver 0.0.0.0:8000
#	uvicorn cinema.asgi:application --host 0.0.0.0 --port 8000 --workers 4 --reload
#	daphne -b 0.0.0.0 -p 8000 cinema.asgi:application"

celery:
	celery -A cinema worker -l info