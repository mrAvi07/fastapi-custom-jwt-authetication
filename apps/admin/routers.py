from fastapi import APIRouter, status, Header, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import Page, paginate
import datetime

from db.base import get_db
from apps.admin.schemas import UpdatePassword
from apps.admin import crud as crud
from apps.custom_auth.deps import get_current_user
from apps.custom_auth.crud import get_user_by_email
from apps.custom_auth.utils import *
from apps.custom_auth.schemas import User

router = APIRouter(
	prefix="/v1/admin",
	tags=['Admin API'],
	)


@router.get("/dashboard/", response_model= User)
async def dashboard(token: str = Header(default=None), user: User = Depends(get_current_user)):
	"""
	DashBoard
	---------
		url: /v1/admin/dashboard
		User Dashboard

	returns
	-------
		payload = {
			id 		:	int
			username 	:	str
			email		:	str
			is_active	:	bool
			is_admin 	:	bool
			date_joined	:	bool
			date_updated	: 	bool
		}

	"""
	if not user.is_admin:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only admin can access dashboard!")

	return user


@router.put("/updatepassword/")
async def update_password(config: UpdatePassword, token: str = Header(default=None), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
	"""
	Update Password
	---------------
		url: /v1/admin/updatepassword/
		User Dashboard - Update Password

	parameters
	----------
		payload = {
			old_password	:	str
			new_password	:	str
			confirm_new_password:	str
		}
	
	returns
	-------
		Json Response with 201_OK status code
	"""
	try:
		user_account = get_user_by_email(db, user.email)
		is_authenticated = verify_password(config.old_password, user_account.hashed_password)

	except Exception as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


	if not is_authenticated:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provided credentials not correct. Please check your credentials again")

	if config.old_password == config.new_password:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Both(old_password and new_password) password are same try something different")
	
	try: 
		user_account.hashed_password = get_password_hash(config.new_password)
		user_account.date_updated = datetime.datetime.now()
		db.commit()
		db.refresh(user_account)
		return JSONResponse(status_code=201, content={"msg": "Your password has been changed successfully!"})
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

