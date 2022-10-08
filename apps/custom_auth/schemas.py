from pydantic import BaseModel, EmailStr, ValidationError, validator, Field, HttpUrl
from enum import Enum
from typing import Optional, List
import datetime
import re



class Token(BaseModel):
	# token serializer
	access_token	:	str
	refresh_token	:	str
	token_type		:	str 


class LoginUser(BaseModel):
	# login user serializers
	email 	:	EmailStr
	password: 	str

	
	@validator('email')
	def check_fields(cls, v, values):
		assert 'email' not in list(values.keys()), "enter password"
		assert 'password' not in list(values.keys()), "Enter password"
		return v


class Gender(str, Enum):
	male = 'male'
	female = 'female'
	other = 'other'
	not_given = 'not_given'


class Branch(str, Enum):
	all_branch = "all"


class User(BaseModel):
	# User schema to list all details of user
	id              : 	int
	full_name		:	Optional[str]
	email 			:	EmailStr
	phone			: 	str 
	avatar			:	Optional[HttpUrl] 
	birth_date		:   Optional[datetime.date] 
	gender			:	str
	branch			:	str
	is_active		:	bool
	is_admin		:	bool
	date_joined		:	datetime.datetime
	date_updated	:	Optional[datetime.datetime] 

	class Config:
		orm_mode=True


class UserCreate(BaseModel):
	# to create a new user
	email 			:	EmailStr
	full_name		:	Optional[str]
	phone			: 	str 
	avatar			:	Optional[HttpUrl]
	birth_date		:   Optional[datetime.date]
	gender			:	Gender = Field(None) 
	branch			:	Branch = Field(None)
	password 		:	str 
	confirm_password: 	str 
	

	@validator('email')
	def check_all_fields(cls, v, values):
		# all fields are required
		assert v not in list(values.keys()), "Email field is required"
		assert 'password' not in list(values.keys()), "password field is required" 
		assert 'confirm_password' not in list(values.keys()), "confirm password field is required"
		return v

	@validator('password')
	def is_valid_password(cls, v, **kwargs):
		# check if password is valid or not
		if len(v) <= 8:
			raise ValueError("password length should be greater than 8")
		if len(v) >= 16:
			raise ValueError("password length should be less than 16")
		return v

	@validator('confirm_password')
	def password_match(cls, v, values, **kwargs):
		# check if password and confirm password are same or not
		if 'password' in values and v != values['password']:
			raise ValueError("password did not match")

		return v

	@validator("phone")
	def is_phone_valid(cls, v):
		# check if phone number is valid or not
		regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
		if v and not re.search(regex, v, re.I):
			raise ValueError("Invalid phone number.")
		return v


class ForgotPassword(BaseModel):
	# forgot password
	email : EmailStr


class ChangePassword(BaseModel):
	# change password 
	new_password 		:  	str
	confirm_new_password: 	str

	@validator('new_password')
	def check_all_fields(cls, v, values):
		assert v is not None, "New password required"
		assert 'confirm_new_password' not in list(values.keys()), "You should confirm new password"
		return v

	@validator('new_password')
	def is_valid_password(cls, v, **kwargs):
		# check if password is valid or not
		if len(v) <= 8:
			raise ValueError("password length should be greater than 8")
		if len(v) >= 16:
			raise ValueError("password length should be less than 16")
		return v

	@validator('confirm_new_password')
	def password_match(cls, v, values, **kwargs):
		if 'new_password' in values and v != values['new_password']:
			raise ValueError("password does not match")

		return v


class EmailSchema(BaseModel):
	email: List[EmailStr]






