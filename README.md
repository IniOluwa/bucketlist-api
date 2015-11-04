# Bucketlist-API

## Description
A Flask API for a bucket list service.
The bucketlist service is a service that allows users to create and manage one o r more bucket lists. Users can have multiple bucket lists and bucket lists can have multiple items.
This is a RESTful Flask API, it uses a Token Based Authentication system to authenticate users and therefore gives access rights to only registered users.
The MultiPurpose Internet Mail Extention ```MIME``` type used for the bucket list service is ```application/json```.

#### Language
```PYTHON version 2.7```

#### Framework
```FLASK```

#### Database
```SQLALCHEMY```

#### Requirements
alembic==0.8.3
Flask==0.10.1
Flask-HTTPAuth==2.7.0
Flask-Migrate==1.6.0
Flask-Script==2.0.5
Flask-SQLAlchemy==2.1
itsdangerous==0.24
Jinja2==2.8
Mako==1.0.3
MarkupSafe==0.23
passlib==1.6.5
python-editor==0.4
SQLAlchemy==1.0.9
Werkzeug==0.10.4
wheel==0.24.0

#### Requests
POST: Saves a new bucket list or item
GET: Retrieves bucket lists with items
PUT: Edits bucket lists or items
DELETE: Remove bucket lists or items

#### API Endpoints
The API Endpoints are the structured addresses to every response triggered by a request to perform specific API tasks.

Request|EndPoint|Functionality|Public Access
-------|--------|-------------|-------------
POST|/register|Registers a new user|True
POST|auth/login|Logs in a registered user|False
GET|auth/logout|Logs out a registered user|False
POST|/bucketlists/|Creates a new bucket list|False
GET|/bucketlists/|Rietrieves bucket list pagination|False
GET|/bucketlists/:id|Retrieves a bucket list by the id|False
PUT|/bucketlists/:id|Edits a bucket list|False
DELETE|/bucketlists/:id|Deletes a bucket list|False
POST|/bucketlists/:id/items|Creates a new bucket list item|False
PUT|/bucketlists/:id/items/:item_id|Edits a bucket list item|False
DELETE|/bucketlists/:id/items/:item_id|Deletes a bucket list item|False
