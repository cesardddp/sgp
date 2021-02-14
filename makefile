run:
	export FLASK_APP=sgp.app;\
    export FLASK_ENV=development;\
	flask run
db:
	export FLASK_APP=sgp.app;\
	rm -rf migrations/;\
	rm sgp/test.db;\
	flask db init;\
	flask db migrate;\
	flask db upgrade;\

