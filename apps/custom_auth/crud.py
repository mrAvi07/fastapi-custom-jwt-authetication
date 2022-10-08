from sqlalchemy.orm import Session
from pydantic import EmailStr

from datetime import datetime 

from db.base import get_db
from .schemas import UserCreate
from core.config import settings
from db.models.users import Users
from .utils import *



def get_user_by_email(db: Session, email: str):
	# get user by email
	user = db.query(Users).filter(Users.email==email).first()
	if not user:
		return False
	return user


def create_user(db: Session, config: UserCreate):
	'''
		create new user
	'''
	hashed_password = get_password_hash(config.password)
	user = Users(
		full_name=config.full_name, 
		email=config.email, 
		gender=config.gender,
		branch=config.branch,
		phone=str(config.phone),
		is_admin=True,
		birth_date=config.birth_date,
		avatar=config.avatar,
		hashed_password=hashed_password
		)

	db.add(user)
	db.commit()
	db.refresh(user)
	return user
	









