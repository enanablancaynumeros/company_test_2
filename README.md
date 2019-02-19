# weather_etl_web

Toy example to collect weather stations locations in Germany and display them in a dash app.
The architecture is made up of asynchronous workers using celery with rabbitmq as a broker that 
runs a simple etl job that loads data in a postgres DB, that is accessible in the browser through 
a flask web server. The celery job is configured to be triggered when loading the flask webserver,
the status of that task can be monitored accessing the flower dashboard on `localhost:5555`.
To visualize the dash map, go to `localhost:8000/map`.
An additional container will run the db initial migration, 
which depending on synchronization may cause some troubles at the beginning.
The etl jobs are not idempotent, so following executions will raise Integrity exception 
in the DB.

To execute the the development environment just run `make up`.
Docker-compose and docker are system requirements.
Alternatively, just run `pip install -r requirements.txt` in a new python environment which 
also includes a working version of docker compose.
