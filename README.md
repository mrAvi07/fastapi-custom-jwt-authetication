# FastAPI JWT Authentication

This repository provides a simple setup for JWT (JSON Web Token) authentication in FastAPI.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/your-username/fastapi-jwt-authentication.git
cd fastapi-jwt-authentication
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the FastAPI application:
```bash
uvicorn main:app --reload
```
### Visit http://localhost:8000/docs in your browser to access the FastAPI Swagger documentation and interact with the API.


This repository serves as a starting point for implementing JWT authentication in FastAPI. FastAPI is a modern, fast, web framework for building APIs with Python 3.7+ based on standard Python type hints.
JWT authentication provides a secure way to handle user 
authentication by issuing a token that can be verified on subsequent requests. 

This repository includes basic configurations to demonstrate user authentication using JWTs.

Feel free to explore and customize the code according to your project requirements.
