SHELL := /bin/bash
run:
	source /home/cesar/sgp/.venv/bin/activate;\
	export FLASK_APP=app;\
    # export FLASK_ENV=development;\
	flask run
db:
	export FLASK_APP=sgp.app;\
	rm -rf migrations/;\
	rm sgp/test.db;\
	flask db init;\
	flask db migrate;\
	flask db upgrade;\

