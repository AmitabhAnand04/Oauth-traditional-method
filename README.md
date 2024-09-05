# Oauth-traditional-method

This is a simple OAuth demonstration API built using Flask, SQLAlchemy, Bcrypt for password hashing, and JWT (JSON Web Tokens) for authentication. The API allows users to register, log in, generate JWT tokens, access protected routes, and revoke tokens.

## Table of Contents

- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
  - [Register User](#register-user)
  - [Create Token (Login)](#create-token-login)
  - [Get Token](#get-token)
  - [Revoke Token](#revoke-token)
  - [Protected Dashboard](#protected-dashboard)
- [JWT Token Verification](#jwt-token-verification)
- [Run the Application](#run-the-application)

## Installation

1. Clone this repository:
    ```bash
    git clone <repository-url>
    ```

2. Navigate to the project directory:
    ```bash
    cd Oauth-traditional-method
    ```

3. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Linux/Mac
    # For Windows, use:
    # venv\Scripts\activate
    ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Set up the database by initializing the Flask-SQLAlchemy model:
    ```bash
    flask shell
    >>> from app import db
    >>> db.create_all()
    >>> exit()
    ```

## Environment Variables

Create a `.env` file in the root directory and provide the following environment variables:

```bash
SECRET_KEY=your_secret_key
SQLALCHEMY_DATABASE_URI=your_database_uri  # Example: sqlite:///site.db
```

- `SECRET_KEY`: A secret key used to encode and decode JWT tokens.
- `SQLALCHEMY_DATABASE_URI`: URI of the database (e.g., SQLite, PostgreSQL, etc.).

## API Endpoints

### Register User

- **Endpoint**: `/register`
- **Method**: `POST`
- **Description**: Registers a new user by storing the username and hashed password in the database.

- **Request Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```

- **Response**:
  ```json
  {
    "message": "User registered successfully!"
  }
  ```

### Create Token (Login)

- **Endpoint**: `/createtoken`
- **Method**: `POST`
- **Description**: Logs in a user, verifies the password, and returns a JWT token.

- **Request Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```

- **Response**:
  ```json
  {
    "token": "your_jwt_token"
  }
  ```

### Get Token

- **Endpoint**: `/gettoken`
- **Method**: `POST`
- **Description**: Retrieves the JWT token of a user if it exists.

- **Request Body**:
  ```json
  {
    "username": "your_username"
  }
  ```

- **Response**:
  - If the token exists:
    ```json
    {
      "token": "your_jwt_token"
    }
    ```
  - If no token is found:
    ```json
    {
      "message": "No token found for this user!"
    }
    ```

### Revoke Token

- **Endpoint**: `/revoketoken`
- **Method**: `POST`
- **Description**: Revokes the JWT token of a user by clearing the stored token.

- **Request Header**:  
  `x-access-token: <jwt_token>`

- **Response**:
  ```json
  {
    "message": "token revoked successfully!"
  }
  ```

### Protected Dashboard

- **Endpoint**: `/dashboard`
- **Method**: `GET`
- **Description**: A protected route that requires a valid JWT token to access.

- **Request Header**:  
  `x-access-token: <jwt_token>`

- **Response**:
  ```json
  {
    "message": "Welcome to the protected dashboard, {username}!"
  }
  ```

## JWT Token Verification

Tokens are validated using a `token_required` decorator that checks the `x-access-token` header. If the token is valid, the user gains access to protected routes. Invalid or missing tokens will result in an error response.

## Run the Application

To run the Flask application:

1. Make sure your virtual environment is activated.
2. Start the server:
    ```bash
    python app.py
    ```
3. The API will be available at `http://127.0.0.1:9000/`.

---

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

### Contributing

Contributions are welcome! If you'd like to improve this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push the branch.
4. Submit a pull request.

### Contact

If you have any questions or feedback, feel free to reach out to [Me](amitabhanand76@gmail.com).

Happy coding!


