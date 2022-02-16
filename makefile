SHELL := /bin/bash
run:
	source /home/cesar/sgp/.venv/bin/activate;\
	export FLASK_ENV=development;\
	export FLASK_APP=sgp.app:app;\
	flask run -p 5000
db:
	export FLASK_APP=sgp.app:app;\
	rm -rf migrations/;\
	rm test.db;\
	flask db init;\
	flask db migrate;\
	flask db upgrade;\

purge_css:
	export FLASK_PROD=production;\
	rm -rf static/.webassets-cache static/dist;\
	export FLASK_APP=app;\
	flask run -p 5000