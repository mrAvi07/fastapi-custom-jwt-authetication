from sqlalchemy.orm import Session

from core.config import settings
from db.models.users import Users


def get_all_users(db: Session):
	# to get all users details
	result = db.query(Users).filter(Users.is_active == True)
	return result


