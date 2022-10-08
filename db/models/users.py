from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
from sqlalchemy_utils import URLType
from sqlalchemy.sql import func

from db.base import Base


class Users(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	full_name = Column(String, nullable=True)
	email = Column(String, unique=True, index=True)
	phone = Column(String, unique=True)
	avatar = Column(URLType, nullable=True)
	branch = Column(String, nullable=True)
	gender = Column(String, nullable=True)
	birth_date = Column(Date, nullable=True)

	hashed_password = Column(String)
	is_active = Column(Boolean, default=True, nullable=True)
	is_admin = Column(Boolean, default=False, nullable=True)

	date_joined = Column(DateTime(timezone=True), server_default=func.now())
	date_updated = Column(DateTime(timezone=True), nullable=True)


