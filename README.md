# Flask-microservices-task

# Requirements
- Python 3.9
- Linux
- Docker

## Description
This repo contains three folders, every folder for one microservice. In every microservice folder there are a config file.
#### train_microservice 
It simulates in a simplified way the work of a train. Information about the current speed of the train is send to central microservice for every 10 seconds. Information about the station, the train is approaching, is sent to the central microservice every 180 seconds

#### gateman_microservice
Is responsible for open and close a railway barrier.
Created as an API
- barrier state
curl http://127.0.0.1:9001/gateman/train/barrier
- barrier open
curl --request PUT http://127.0.0.1:9001/gateman/barrier/open
- barrier close
curl --request PUT http://127.0.0.1:9001/gateman/barrier/close

Example API output
```sh
{                                                                                                                                                                                            
  "last_modify": "Sat, 09 Oct 2021 16:53:37 GMT", 
  "state": 1
}
```
In case of any error:
```sh
{
    "error": "error_msg"
}
```

#### central_microservice
Responsible for communication between train_microservice and gateman_microservice. It implements the following business rules:
- Information about the current speed of the train sended by train_microservice is saved to specific files in central_microservice/speed_files/ folder
- Information about the station, the train approaching is saved in central_microservice/log file.
  Additionaly central_microservice is responsible for sending an info about open or close the railway barrier to gateman_microservice.
  Information about open or close the railway barrier is also saved in central_microservice/log file


# Install
- You can use virtualenv if you want. To activate virtualenv run: source <path_to_venv>/bin/activate
- install dependencies:
  ```sh
  cd Flask-microservices-task
  source venv/bin/activate
  python -m pip install -r requirements.txt
  ```


# Run
### Without docker-compose
Run commands from every section in new terminal

- start rabbitmq from docker image:  
   ```sh
   docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management
   ```

- run gateman_microservice
  ```sh
  # check central_microservice/config.ini
  # go to main repo folder
  export PYTHONPATH="${PYTHONPATH}:."
  python3 central_microservice/app.py
  ```
- run central_microservice
  ```sh
  # check gateman_microservice/config.ini
  # go to main repo folder
  export PYTHONPATH="${PYTHONPATH}:."
  python3 gateman_microservice/app.py
  ```
- run celery train_microservice worker and beat
  ```sh
  # check train_microservice/config.ini
  # go to main repo folder
  
  # You can run worker and beat separately, using two terminal instances
  celery -A train_microservice.celery_runner worker -n "train" -Q "celery_periodic" --loglevel=INFO
  celery -A train_microservice.celery_runner beat --loglevel=INFO
  
  # or run by one command (only for Linux, only for development purposes)
  celery -A train_microservice.celery_runner worker -n "train" -Q "celery_periodic" --loglevel=INFO -B
  ```
- run celery worker for central microservice
  ```sh
  # go to main repo folder
  export PYTHONPATH="${PYTHONPATH}:."
  celery -A central_microservice.celery_runner worker -n "central" --loglevel=INFO
  ```
  
# Run tests
- For testing, rabbitmq, central_microservice and gateman_microservice must be running first!
- To run test:
  ```sh
  # go to main repo folder
  pytest -v
  ```
  
## What could have been done better
- Microservices, celery workers and beat should have been put into separate docker containers
- central_microservice and gateman_microservice use develop server. Develop server is not recommended for production environment. It would be better to use Nginx + uWSGI