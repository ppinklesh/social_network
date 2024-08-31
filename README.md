### README.md

```markdown
# Social Networking Application

This is a social networking application built using Django and Django REST Framework (DRF). The application provides functionalities for user signup, login, searching users, sending/accepting/rejecting friend requests, listing friends, and listing pending friend requests.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Testing](#testing)

## Installation

### Prerequisites

- Python 3.x
- Django
- Django REST Framework
- Django REST Framework Token Authentication

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/social-networking-app.git
   cd social-networking-app
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

## Usage

The application provides the following functionalities:

- User signup and login
- Searching users by email or name
- Sending, accepting, and rejecting friend requests
- Listing friends
- Listing pending friend requests

## Endpoints

### User Signup

- **URL**: `/api/signup/`
- **Method**: `POST`
- **Payload**:

  ```json
  {
      "email": "test@example.com",
      "name": "Test User",
      "password": "your_password"
  }
  ```

### User Login

- **URL**: `/api/login/`
- **Method**: `POST`
- **Payload**:

  ```json
  {
      "email": "test@example.com",
      "password": "your_password"
  }
  ```

### Search Users

- **URL**: `/api/search/`
- **Method**: `GET`
- **Query Parameters**:
  - `query`: The search keyword (email or name)

### Send Friend Request

- **URL**: `/api/friend-request/`
- **Method**: `POST`
- **Payload**:

  ```json
  {
      "to_user": <user_id>
  }
  ```

### Accept/Reject Friend Request

- **URL**: `/api/friend-request/<request_id>/`
- **Method**: `PUT`
- **Payload**:

  ```json
  {
      "is_accepted": true  # Set to false to reject
  }
  ```

### List Friends

- **URL**: `/api/friends/`
- **Method**: `GET`

### List Pending Friend Requests

- **URL**: `/api/pending-requests/`
- **Method**: `GET`

## Testing

You can test the endpoints using tools like Postman or cURL. Below are some example requests:

### Signup

```bash
curl -X POST http://127.0.0.1:8000/api/signup/ -H "Content-Type: application/json" -d '{"email": "test@example.com", "name": "Test User", "password": "your_password"}'
```

### Login

```bash
curl -X POST http://127.0.0.1:8000/api/login/ -H "Content-Type: application/json" -d '{"email": "test@example.com", "password": "your_password"}'
```

### Search Users

```bash
curl -X GET "http://127.0.0.1:8000/api/search/?query=test" -H "Authorization: Token your_token_here"
```

### Send Friend Request

```bash
curl -X POST http://127.0.0.1:8000/api/friend-request/ -H "Content-Type: application/json" -H "Authorization: Token your_token_here" -d '{"to_user": 2}'
```

### Accept/Reject Friend Request

```bash
curl -X PUT http://127.0.0.1:8000/api/friend-request/1/ -H "Content-Type: application/json" -H "Authorization: Token your_token_here" -d '{"is_accepted": true}'
```

### List Friends

```bash
curl -X GET http://127.0.0.1:8000/api/friends/ -H "Authorization: Token your_token_here"
```

### List Pending Friend Requests

```bash
curl -X GET http://127.0.0.1:8000/api/pending-requests/ -H "Authorization: Token your_token_here"
```
