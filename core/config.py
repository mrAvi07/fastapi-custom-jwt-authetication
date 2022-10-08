import os
from dotenv import load_dotenv
from passlib.context import CryptContext


load_dotenv()

class Settings:
	PROJECT_NAME: str = "Custom Authentication FastAPI"
	PROJECT_VERSION: str = "1.0.0"

	# database settings
	POSTGRES_USER = os.getenv("POSTGRES_USER")
	POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
	POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
	POSTGRES_PORT = os.getenv("POSTGRES_PORT")
	POSTGRES_DB = os.getenv("POSTGRES_DB")


	SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

	# jwt authentication settings
	JWT_SECRET = "JWT_SECRET"
	JWT_ALGORITHM = "HS256"
	TOKEN_EXPIRE_HOURS = 0
	TOKEN_EXPIRE_MINUTES = 10
	REFRESH_TOKEN_EXPIRES = 60 * 24 

	pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


settings = Settings()