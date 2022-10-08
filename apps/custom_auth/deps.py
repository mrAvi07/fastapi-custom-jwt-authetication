from fastapi import HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import ValidationError
from jwt.exceptions import *
import datetime

from .utils import *
from db.models.users import Users
from db.base import get_db
from core.config import settings


reuseable_auth = OAuth2PasswordBearer(
	tokenUrl="/v1/token",
	scheme_name="JWT"
	)



def _verify_token_payload(req: Request, db: Session = Depends(get_db)):
	try:
		token_prefix = req.headers["token"].split(' ')[0]
		if token_prefix != "Bearer":
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
		token = req.headers["token"].split(' ')[1]
		payload = jwt.decode(
			token,
			settings.JWT_SECRET,
			algorithms=[settings.JWT_ALGORITHM]
			)

		if datetime.datetime.fromtimestamp(payload["exp"]) < datetime.datetime.now():
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Token expired",
				headers={"WWW-Authenticate": "Bearer"}
				)
	except KeyError:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Unauthorize user"
			)
	except IndexError:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid Token"
			)
	except InvalidTokenError:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Invalid Token",
			headers={"WWW-Authenticate": "Bearer"}
			)

	return payload


async def get_current_user(req: Request, db: Session = Depends(get_db)):
	# get current user 
	payload = _verify_token_payload(req, db)
	try:
		user = db.query(Users).filter(Users.id == payload["sub"]).first()
	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Invalid Token"
			)

	if user is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="User not found"
			)

	return user



async def otp_token_verification(req: Request, db: Session = Depends(get_db)):
	# get otp token verification code
	payload = _verify_token_payload(req, db)
	user = db.query(Users).filter(Users.email == payload["sub"]).first()
	if user is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="User not found"
			)

	return user


"""
async def public_api_token_check(req: Request, db: Session = Depends(get_db)):
	# get otp token verification code
	try:
		token_prefix = req.headers["token"].split(' ')[0]
		if token_prefix != "Bearer":
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Token")

		token = req.headers["token"].split(' ')[1]
	
		payload = jwt.decode(
			token,
			settings.JWT_SECRET,
			algorithms=[settings.JWT_ALGORITHM]
			)
		return payload
	except KeyError:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
	except IndexError:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
	except DecodeError:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized User")
	

"""