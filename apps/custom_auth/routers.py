from fastapi import APIRouter, Request, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from pydantic import ValidationError, EmailStr
from fastapi import status, HTTPException
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from sqlalchemy import or_
import jwt, datetime
import json

from core.config import settings
from db.base import get_db
from .crud import *
from .schemas import *
from db.models.users import Users
from .deps import *
from .utils import *


router = APIRouter(
	prefix="/v1/auth",
	tags=['AUTH API'],
	)


@router.post("/login/", response_model=Token)
async def login(config: LoginUser, db: Session = Depends(get_db)):
	"""	
	Login user  
	----------
		url: /v1/auth/login/

	parameters 
	----------
		config = {
			email	: str 
			password: str
		}
		

	returns
	-------
		payload = {
			access_token 	:	str  = jwt_token,
			refresh_token 	: 	str  = jwt token,
			type 		:	str  = token type
		}
	"""
	try:

		user = db.query(Users).filter(Users.email==config.email).first()
		if user is None:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="User not found"
				)
	except ValueError:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Both fields are required"
			)

	is_Authenticated = verify_password(config.password, user.hashed_password)
	if not is_Authenticated:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Username and password combination is not correct!",
			headers={"WWW-Authenticate": "Bearer"}
			)
	access_token = generate_access_token(user)
	refresh_token = refresh_access_token(user)
	return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}



@router.post("/register/", response_model=User)
async def register(config: UserCreate, token: str = Header(default=None), db: Session = Depends(get_db), payload: dict = Depends(public_api_token_check)):
	"""
	Register
	--------
		url: /v1/auth/register/
		Create new user account 

	Parameters
	---------
		config = {
			full_name		:	str 
			email			: 	str
			phone			: 	int
			avatar			: 	str
			birth_date		: 	datetime 
			gender			: 	str
			branch			: 	str
			password 		: 	str - should be greater than 8
			confirm password 	:	str - should be greater than 8
		}

	returns
	------
		payload = {
			id 			:	int
			full_name	:	str
			email 		:	emailstr
			phone		:	int
			avatar		:	url
			birth_date	:	datetime
			gender		: 	str
			branch		:	str
			is_active	:	bool
			is_admin	:	bool
			date_joined	:	datetime
			date_updated	:	datetime
		}

	"""
	if not payload["secret"]:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not authorized!")

	try:
		user = db.query(Users).filter(or_(Users.email == config.email, Users.phone == str(config.phone))).first()
	except ValidationError as e:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=str(e)
			)
	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=str(e)
			)
	except KeyError as e:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=str(e)
			)
	
	if user:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="account associated with provided email or phone number, already exists."
			)
	try:	
		user = create_user(db, config)
		return user
	except Exception as e:
		return JSONResponse(status_code=400, content={"error": str(e)})

	

@router.post("/forgotpassword/")
async def forgot_password(config: ForgotPassword, db: Session = Depends(get_db)):
	"""
	Forgot Password
	---------------
		url: /v1/auth/forgotpassword/
		Request to reset password

	parameters
	----------
		email: user email address

	returns
	-------
		Will send reset password url on particular email address if provided email has an active user account 
	"""
	user = get_user_by_email(db, config.email)
	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user account is associated with provided email.")

	try:
		otp_token = generate_otp_token(config.email)
		#await send_otp(msg, email)

		msg = f"Url to reset password has been sent to your account. Please check your email address."

		return JSONResponse(status_code=status.HTTP_200_OK, content={ "msg": msg, "token": otp_token })
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))




@router.post("/resetpassword")
async def verify_token_reset_password(config: ChangePassword, token: str = Header(default=None), db: Session = Depends(get_db), user: User = Depends(otp_token_verification)):
	"""
	Verify otp token and Reset Password
	-----------------------------------
		url: /v1/auth/changepassword/
		verify otp token and reset password

	parameters
	----------
		headers = {
			"token": Bearer <otp_token>
		}

		payload = {
			new_password	:	str
			confirm_new_password:	str
		}
	
	returns
	-------
		Json Response with 201_OK status code
	"""
	try:
		user.hashed_password = get_password_hash(config.new_password)
		user.date_updated = datetime.datetime.now()

		db.commit()
		db.refresh(user)
		return JSONResponse(status_code=201, content={"msg": "Password Updated. Go to login page"})

	except Exception as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

