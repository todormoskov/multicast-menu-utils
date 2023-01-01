# multicast-menu-utils

This repository contains tools for the containerization, monitoring and performance testing of the multicast content portal MulticastMenu.

# 1. Testing Environment
The folder testing_environment contains a Docker Compose configuration of the services required to run MulticastMenu and to monitor its used resources during execution.

## 1.0 Prerequisites

In order to use the testing environment the following prerequisites should be fulfilled first.

### 1.0.1 Tools
Docker and Docker Compose has to be installed:

* Docker - [Installation Guide](https://docs.docker.com/get-docker/)
* Docker Compose - [Installation Guide](https://docs.docker.com/compose/install/)

### 1.0.2 Testing environment definition
After installing the tools, the contents of the folder testing_environment, which contain the definition of the testing environment, should be copied to the root directory of MulticastMenu.

### 1.0.3 MulticastMenu dependencies
Next, the following command should be executed in the root directory of MulticastMenu:

```bash
pip freeze > requirements.txt
```

This will export a list with all Python packages (libraries) used by MulticastMenu in a requirements.txt file. This file will allow Docker to build the MulticastMenu container.

## 1.1 Testing Environment Details
The testing environment is composed of multiple services (specified in the docker-compose.yml file):

### 1.1.1 Application setup:

* multicast_menu: MulticastMenu (the Django web application)
* db: a Postgres database (a relational database used by MulticastMenu)
* celery: a celery worker (a process that will be executing tasks submitted to a celery task queue by MulticastMenu)
* redis: a redis message broker (used as a task queue by celery)

### 1.1.2 Monitoring setup:

* cAdvisor (Container Advisor) (An application that will be exporting data about the running containers)
* Prometheus (A time series database that will be saving the exported data)
* Grafana (A web application that will be used for the data visualisation)

## 1.2 Starting the environment

Once the prerequisites are fulfilled, the environment can be started with the following command:

```bash
docker-compose up -d
```

This will start all services specified in the docker-compose.yml file. MulticastMenu should then be available on http://localhost:8080.

# 2. Performance Testing
The performance testing is done through a tool called locust. The folder performance_testing contains the locust file, which contains all actions that can be performed by a MulticastMenu user, two utility functions and example data to use during the tests.

## 2.0 Prerequisites

### 2.0.1 Copying the performance_testing folder
The performance_testing folder should be copied to the root directory of MulticastMenu.

### 2.0.2 Creating example data
The tests will simulate real MulticastMenu users and real MulticastMenu requests. For this we need to create example users, categories and streams. While the categories and streams can be created manually, setting up 100 users manually can take time. In order to automate this a python script for the creation of example users is available in performance_testing/util.py.

To allow the script to put data in the MulticastMenu database, it should be executed from the Django shell. Executing the following command in the root folder of MulticastMenu will open up a terminal that has all the Django settings already imported:

```bash
python manage.py shell
```

Now we can import the create_dummy_users() function from the util.py file in the terminal and execute it to create the users.

```python
from performance_testing.util import create_dummy_users

create_dummy_users("./performance_testing/data/credentials.csv")
```

## 2.1 Starting the performance testing tool

In order to start the performance testing tool, we need to navigate to the performance_testing folder within the terminal and run:

```bash
locust
```

Once Locust is started, its web interface should be available on http://localhost:8089.

## 2.2 Start the performance tests

The performance tests can be started from the web interface of Locust. There we can specify the number of users to be spawned, the spawn rate and the address of MulticastMenu.