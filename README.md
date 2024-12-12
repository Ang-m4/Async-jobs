# ITS Async Jobs

The **ITS Async Jobs** project is responsible for handling any asynchronous operations you might need. It is currently used for sending and receiving emails on demand and generating backups periodically. If you wish to add any other tasks, I recommend taking a look at the [Celery Documentation](https://docs.celeryq.dev/en/stable/#) to learn how to handle periodic tasks and their definitions.


This project originated from the need to send multiple emails regarding version request changes in the initial **RFC project**. The idea was to separate the email sending logic from the API logic to make things faster and more modular. We also leverage this background tasks model to perform periodic backups of our ITS Database and FTP data.

**Author:** Andres Felipe Giraldo - https://github.com/Ang-m4/

## Index
- [ITS Async Jobs](#its-async-jobs)
  - [Index](#index)
  - [1. How does it work?](#1-how-does-it-work)
  - [2. How To Run](#2-how-to-run)
  - [3. Environment Variables](#3-environment-variables)
      - [For broker configurations](#for-broker-configurations)
      - [For Database configurations](#for-database-configurations)
      - [For FTP Configurations](#for-ftp-configurations)
      - [For Notifications](#for-notifications)
      - [For Folder paths](#for-folder-paths)
  - [4. Project Structure](#4-project-structure)
    - [Config.py module](#configpy-module)
    - [Managers Sub-package](#managers-sub-package)
    - [Tasks Sub-package](#tasks-sub-package)


## 1. How does it work?

As the [Celery documentation](https://docs.celeryq.dev/en/stable/#) describes, we need a broker to publish and consume our task requests. In this case, we decided to use `redis` for its performance.

The main concept follows the publisher-consumer pattern. Everything works asynchronously, and once the workers are launched, we publish multiple tasks to our broker for the workers to start processing. Currently, we have two publishers linked to the service, The ```Tasks Scheduler``` and the ```ITS Requests API```. However, if you wish, you can execute any task you define by importing the Celery app and calling the task from your own different project.


![Async Jobs High level diagram](./documentation/diagram-simple-use/simple-use.svg)

**Caption:** High level diagram of the ITS Async Jobs project and how it communicates with the different parts of the ```ITS environmet Project```.

## 2. How To Run

I recommend launching this project as part of the `ITS Central Environment`, as described in its own documentation. However, if you need to launch it on its own, please follow these instructions:

1. Ensure you have installed ```python 3``` and ```pip```
2. Install the dependencies with ```pip install -r ./requirements.txt```
3. Execute the maintenance worker:
   
        celery -A app worker --log level=info -n maintenance -Q maintenance

4. Execute the Notifications worker:
   
        celery -A app worker --loglevel=info -n notifications -Q notifications 

5. Finally Execute the beat Scheduler in charge of publishing the periodic tasks for maintenance:
   
        celery -A app beat --loglevel=info

6. Check if the tasks were successfully registered and the workers correctly bound:

        celery -A app inspect registered


**Note:** Make sure to run you ```redis``` server or any other compatible brokers and create the ```.env``` file as described in section [3. Environment Variables](#3-environment-variables). 


## 3. Environment Variables

The ITS Async Jobs project uses some of the `.env` environment variables for database connections, FTP connections, and log file storage. Here we will detail which variables from the entire `.env` file are needed.

**Note:** If you are running this project as part of the `ITS Central Environment` compose app, you do not need to worry about this section. The general `.env` file will be provided during project initialization.


#### For broker configurations
-   `REDIS_HOST`
-   `REDIS_PORT`
-   `REDIS_TASKS_DB`
-   `REDIS_TASK_RESULTS_DB`
  
#### For Database configurations 
-  `CENTRAL_DB_HOST`
-  `CENTRAL_DB_PORT`
-  `CENTRAL_DB_NAME`
-  `CENTRAL_DB_USER`
-  `CENTRAL_DB_PASS`
-  `CENTRAL_DB_AUTH_SOURCE`
  
#### For FTP Configurations
- `FTP_SERVER_HOST`
- `FTP_SERVER_USER`
- `FTP_SERVER_PASS`
- `FTP_SERVER_ROOT`
  
#### For Notifications
- `ITS_SMTP_SERVER`
- `ITS_SMTP_PORT`
- `ITS_EMAIL_ACCOUNT`
- `ITS_EMAIL_PASSWORD`
- `ITS_FRONTEND_URL`
  
#### For Folder paths
- `BACKUP_FOLDER`
 
 
## 4. Project Structure

This project consists of two main components: a `Redis` database used as a task broker and our Python library integrated with `Celery` for executing those tasks. It's important to note that the `Redis` database doesn't require any additional configuration—just a simple Redis container is sufficient.

The `asyncjobs` package is organized as follows:

 ### [Config.py](./asyncjobs/config.py) module
  
  This file serves as the main configuration for the project, handling everything from **queue definitions** to the **task scheduler**. If you need to define additional queues or schedule periodic tasks, this is the appropriate place to do so.
 ### Managers Sub-package
  
  This sub-package includes a collection of managers responsible for various concerns, such as [***Database***](./asyncjobs/managers/database_manager.py), [***FTP***](./asyncjobs/managers/ftp_manager.py), and [***Email***](./asyncjobs/managers/email_manager.py). Each manager is organized into separate modules and is invoked by task definitions to execute its specific logic.

### Tasks Sub-package
  
  The tasks sub-package contains one module for each queue defined in the [config.py](./asyncjobs/config.py) module (e.g., Notifications and Maintenance). Here, tasks are individually defined and bound to the Celery app.


**Note:** The [app.py](app.py) file imports the tasks at the end of the file to ensure that tasks are correctly bound once the app is instantiated. Proper binding should be handled by the task discovery method (Fix).
