SHELL := /bin/bash
run:
	source /home/cesar/sgp/.venv/bin/activate;\
    export FLASK_ENV=development;\
	export FLASK_APP=app;\
	flask run -p 5050
db:
	export FLASK_APP=app;\
	rm -rf migrations/;\
	rm sgp/test.db;\
	flask db init;\
	flask db migrate;\
	flask db upgrade;\

purge_css:
	export FLASK_PROD=production;\
	rm -rf static/.webassets-cache static/dist;\
	export FLASK_APP=app;\
	flask run -p 5050