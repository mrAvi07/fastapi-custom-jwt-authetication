import jwt, string, math, random, datetime
from passlib.context import CryptContext
from fastapi_mail import MessageSchema, FastMail
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import EmailStr

from core.config import settings
from .schemas import *



def get_password_hash(password):
	# get hash password
	return settings.pwd_context.hash(password)


def verify_password(plain_password, hash_password):
	'''
		to verify plain password with hash password
	'''
	return settings.pwd_context.verify(plain_password, hash_password)


def authenticate_user(plain_password, hash_password):
	# to authenticate user
	if verify_password(plain_password, hash_password):
		return True
	else:
		return False


def generate_access_token(user):
	"""
		To generate JWT access token user data

		parameter
		---------
			user = {
				...user_model
			}

		return 
		------
			access_token - jwt token
	"""
	payload = {
		'sub': user.id,
		'exp': datetime.datetime.now() + datetime.timedelta(hours=settings.TOKEN_EXPIRE_HOURS, minutes=settings.TOKEN_EXPIRE_MINUTES),
		'iat': datetime.datetime.now()
	}
	access_token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
	return access_token



def generate_otp_token(email: EmailStr):
	# to generate otp token
	payload = {
		'sub': email,
		'exp': datetime.datetime.now() + datetime.timedelta(seconds=30),
		'iat': datetime.datetime.now()
	}
	otp_token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
	return otp_token




def decode_access_token(token):
	"""
		To decode the jwt token

		parameter
		---------
			access_token - jwt token

		return
		------
			payload = {
	
			}
	"""
	payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM,])
	return payload


def refresh_access_token(user: User, expires_delta: int = None):
	# create refresh token
	if expires_delta is not None:
		expires_delta = datetime.datetime.utcnow() + expires_delta
	else:
		expires_delta = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES)

	payload = {"sub": user.id, "exp": expires_delta, }
	enocded_jwt = jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)
	return enocded_jwt



def generate_otp():
	# to create a new otp
	digits = string.digits
	otp = ""

	for i in range(6):
		otp += digits[math.floor(random.random() * 10)]

	return otp



def send_email(msg: str, email: EmailStr):
	# send email
	client = FastMail(settings.conf)
	message = MessageSchema(
		subject="Reset account password",
		recipients=[email, ],
		body=msg,
		subtype='html',
		)

	client.send_message(message)
	return True