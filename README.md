# TicketSystemFlaskJune2022 REST API

A demo Flask REST API for my exam. 

## Install
1. You need Python version 3.8 or above instaleld on your computer.
2. Install the required non build in libraries using the requireemnst file:

    ``python3 -m pip install -r requirements.txt``
3. Create Postresql database and config it. If you are on windows, please follow this [detailed tutorial](https://www.guru99.com/download-install-postgresql.html) 
4. If you are on Windows, you will need to set "FLASK_APP" environment variable for the migrations:

    ``set FLASK_APP=./main.py``
    
## Run the app

    ``python main.py``

## Run the tests

1. Tests are build with pytest. You can set your favorite IDE to work with pytest, for pycharm please follow  this [detailed tutorial]([https://www.guru99.com/download-install-postgresql.html](https://www.jetbrains.com/help/pycharm/pytest.html#create-pytest-test))
2. In pycharm you can customise your test configuration so to run all test in one click. 


# REST API

The REST API to the Ticket System app is described below.

## Get list of Tickets

### Request

`GET /ticket/list/all/`

    curl -i -H 'Accept: application/json' http://localhost:5000/ticket/list/all/

### Response

    HTTP/1.1 200 OK
    Server: Werkzeug/2.2.2 Python/3.9.13
    Date: Thu, 25 Aug 2022 10:04:53 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 702

    []

## Create a new Tickets

### Request

`POST /ticket/create/`

    curl -i -H 'Accept: application/json' -d 'title=Foo&description=text' http://localhost:5000/ticket/create/

### Response

    HTTP/1.1 201 Created
    Server: Werkzeug/2.2.2 Python/3.9.13
    Date: Thu, 25 Aug 2022 10:12:24 GMT
    Status: 201 Created
    Connection: close
    Content-Type: application/json
    Content-Length: 200

    {"pk":1,
    "title":"Foo",
    "description":"text",
    "created_on": "2022-08-25T10:12:24.506680",
    "priority": "low",
    "status": "new"}

## Get a specific Ticket you need to be with role requester and to be the creator of the ticket

### Request

`GET /ticket/list/<int:pk>/requester/`

    curl -i -H 'Accept: application/json' http://localhost:5000/ticket/list/1/requester/

### Response

    Server: Werkzeug/2.2.2 Python/3.9.13
    Date: Thu, 25 Aug 2022 10:19:17 GMT
    Connection: close
    Content-Type: application/json
    Content-Length: 200

    {"pk":1,
    "title":"Foo",
    "description":"text",
    "created_on": "2022-08-25T10:12:24.506680",
    "priority": "low",
    "status": "new"}

## Get a non-existent Ticket you need to be with role requester and to be the creator of the ticket

### Request

`GET /ticket/list/<int:pk>/requester/`

    curl -i -H 'Accept: application/json' http://localhost:5000//ticket/list/1000/requester/

### Response
    
    Status: 400 BAD REQUEST
    Server: Werkzeug/2.2.2 Python/3.9.13
    Date: Thu, 25 Aug 2022 10:23:56 GMT
    Connection: close
    Content-Type: application/json
    Content-Length: 37

    {"message": "No such ticket!"}

## Delete a Ticket using you need to be with role administrator

### Request

`DELETE /administrators/delete/<int:pk>/`

    curl -i -H 'Accept: application/json' -X POST -d'_method=DELETE' http://localhost:5000/administrators/delete/5/

### Response

    Status: 200 OK
    Server: Werkzeug/2.2.2 Python/3.9.13
    Date: Werkzeug/2.2.2 Python/3.9.13
    Connection: close
    Content-Type: application/json
    Content-Length: 4

    204


