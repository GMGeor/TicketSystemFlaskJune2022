# TicketSystemFlaskJune2022 REST API

A Flask REST API that provides endpoints for creation and loging of different types of users, and creation, update, list and deletion of tickets, that are protected acording to the business logic.

**PLEASE NOTICE!** *Initialy my idea was to create a chat bot to consume this API. However, the lack of time and mainly the lack of front end knowledge didn't allow me to do it. So why I created this project to cover the exam requirements.  And another one which has basic functionality, but it is deployed and integrated with Watson Assistant chatbot. Please refer to the other project* <a href="https://github.com/GMGeor/TicketSystemDemo4WatsonAssistantIntegration" target="_blank">here</a>

## Users
There are 4 user roles:
1. Administrator. Can create administrators, managers and agents. Can delete tickets. Can list all tickets.
2. Manager. Can assign tickets to agents and update tickets priority. Can list all tickets, but only those that are asigned by him to an agent.
3. Agents. Can update ticket status to pendiong or resolved. Can list all tickets, but only those that are asigned to him by the manager.
4. Requester. Can register himself to the system. Can create ticket. Can update ticket description if he is the creator. Can list all tickets or just one ticket, but only those that are created by him. Can close the ticket by changing the status to closed, again if he is the creator. 
    - on requester creation are provided email and prefered language for communication. Those 2 variables are used by external services. When an agent updates the ticket status, the requester will receive notification email with text provided by the agent translated to the prefered language.
    
    
## Install
### Prerequisites
1. You need Python version 3.8 or above instaled on your computer.
2. You need a database to be created and set. Create Postresql database and config it. If you are on windows, please follow this <a href="https://www.guru99.com/download-install-postgresql.html" target="_blank">detailed tutorial</a>

3. If you are on Windows, you will need to set "FLASK_APP" environment variable for the migrations:

    ``set FLASK_APP=./main.py``
    
4. Two services of external providers are integrated. You need to setup the respective credentials, for more info please refer to the providers documentation: 
<a href="https://sendgrid.com/" target="_blank">Sendgrid</a> and <a href="https://cloud.ibm.com/catalog/services/language-translator" target="_blank">Language-translator</a>

5. Install the required non build in libraries using the requiremenst file:

    ``python3 -m pip install -r requirements.txt``
6. Two services are integrated, 
    
### Run the app

    ``python main.py``

## Run the tests

Tests are build with pytest. You can set your favorite IDE to work with pytest. For pycharm please follow  this <a href="https://www.jetbrains.com/help/pycharm/pytest.html#create-pytest-test" target="_blank">tutorial</a>

In pycharm you can customise your test configuration so to run all test in one click. 


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
  
## Full list of endpoints is not available yet. 
Please refer to [routes](https://github.com/GMGeor/TicketSystemFlaskJune2022/blob/490ab28da409b5fc106a17b6bb6fe2a8ba116f6d/resources/routes.py#L27) in order to see all available endpoints.
