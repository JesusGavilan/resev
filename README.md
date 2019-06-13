# Resev app
## Requirements
- Docker version 18.05
- Docker compose version 1.21.2

## Architecture

Resev REST API (Falcon) <--------> PostgreSQL.

This API REST application is implemented using Falcon API REST framework for Python. 
For serving the services Gunicorn was the chosen one.
The information related to the users are stored on PostgreSQL database.
The application, the postgres instance and the pgadmin service are dockerized.

## Setting up

For running the application under Docker:

```bash
docker-compose -f docker-compose up -d
```

## API docs

### Create user

```json
POST /resev/v1/users HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Body:
{
	"username": "jesus",
	"email": "jesus@resev.com",
	"password": "dev_123456",
	"balance": 2500.0
}
```
### Login

```json
POST /resev/v1/users/login HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Body:
{
	"email": "karen@resev.com",
	"password": "dev_123456"
}
```

### Get User

```json
GET /resev/v1/users/1 HTTP/1.1
Host: localhost:8000
Authorization: gAAAAABdAYpiatTQUfTsM6YRgJi_PpjMlSL07sI1gy_39mGVDk2gqgmxy7_uke0gu1ObAHCRHVjLHkuTLhgZx9XA21NTvBYd9Q==
```
### Get Users

```json
GET /resev/v1/users HTTP/1.1
Host: localhost:8000
Authorization: gAAAAABdAYpiatTQUfTsM6YRgJi_PpjMlSL07sI1gy_39mGVDk2gqgmxy7_uke0gu1ObAHCRHVjLHkuTLhgZx9XA21NTvBYd9Q==
```

### Transfer money

```json
POST /resev/v1/users/1/transfer HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Authorization: "gAAAAABdAYpiatTQUfTsM6YRgJi_PpjMlSL07sI1gy_39mGVDk2gqgmxy7_uke0gu1ObAHCRHVjLHkuTLhgZx9XA21NTvBYd9Q==
Body:
{
	"borrower": "jesus",
	"quantity": 500
}
```

