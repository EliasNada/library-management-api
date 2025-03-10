# Library Management API

A RESTful API for library management with JWT-based authentication, book tracking, and role based access control.
bundled with Database using Docker for easy setup.

## Features

- ✅ JWT/API key Authentication
- ✅ Role Based Access Control
- ✅ CRUD for Books, Users, Borrowings
- ✅ RESTful APIs
- ✅ Advanced search
- ✅ Swagger/OpenAPI documentation for interactive API testing.
- ✅ Rate Limiting
- ✅ Documented code

## Quick Start

### Prerequisites

- Docker
- Python 3.13 + pipenv
- GNU Make
- curl/httpie or postman (for testing)

### Installation
Make sure the prerequisites are installed correctly and running.

### Option one (Recommended):

You can then simply run the app by doing
```bash
make run
```
### Option two:
if you have your own Postgres database that you prefer to connect to,
please modify the [.env](.env) file with the correct connection string.

You can then run the following commands to get the application running:
```bash
pipenv --python 3.13
pipenv install -r requirements.txt
pipenv run alembic upgrade head
pipenv run uvicorn app.main:app --port 8080
```


This will cover all the setup.

And the API will be available at:
http://localhost:8080

### Project Structure
```aiignore
library_app/
├── app/                  # Application code
├── alembic/              # Database migrations
├── core/                 # Core functionality required by the app
├── docs/                 # Documentation and case study
│   ├── case_study.pdf    # case study PDF
│   └── openapi.json      # Open API Spec document
├── README.md             # Project overview
├── Makefile              # contains script to run application
└── requirements.txt      # Python dependencies
```

### APIs

All models support CRUD operations and more!  
You can find a list of the APIs in the [openapi.json](docs/openapi.json)
(Recommend to import it into Postman to get a full list if the APIs)

### Credentials

You will get an `api_key` and a bearer `access_token` once you register:

#### Request example:

```bash
curl --location 'http://localhost:8080/api/common/auth/register' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--data-raw '{
  "username": "john",
  "password": "Pass123!",
  "email": "john.doe@example.com",
  "role": "librarian"
}'
```
#### Response example:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzQxNTg2NDkyfQ.eW9DB5gFbe4tOBJdHTwh3aD1fwFASLnBqn1D_QIc4Dg",
    "token_type": "bearer",
    "api_key": "5ejZ7RUJoRFUSNdxeeiA4VL_DavC44QMqulSXY8zsAA"
}
```
#### Credentials usage examples:
##### API KEY:
```bash
curl --location 'http://localhost:8080/api/librarian/books/' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header 'X-API-Key: 5ejZ7RUJoRFUSNdxeeiA4VL_DavC44QMqulSXY8zsAA' \
--data '{
  "title": "Harry Potter",
  "author": "J.K Rowling",
  "isbn": "12345678",
  "category": "fantasy",
  "published_date": "1997-06-26"
}'
```
##### JWT:
```bash
curl --location 'http://localhost:8080/api/librarian/books/' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzQxNTg2NDkyfQ.eW9DB5gFbe4tOBJdHTwh3aD1fwFASLnBqn1D_QIc4Dg' \
--data '{
  "title": "Harry Potter",
  "author": "J.K Rowling",
  "isbn": "12345678",
  "category": "fantasy",
  "published_date": "1997-06-26"
}'
```
**Both ways are supported.**

Note down your api_key as you will not be able to retrieve it again (you can still re-generate it, however..) 


Note: if you imported the collection mentioned in the API section into Postman, you can set the api key (`apiKey`) as an environment variable in the parent directory so that all child requests have it automatically.

or you can navigate to http://localhost:8080/docs to use the interactive REST API client! (don't forget to click 'Authorize'!)
![img.png](img.png)


Please reach out to <eliasmnada@gmail.com> if you have any questions in inquiries.
