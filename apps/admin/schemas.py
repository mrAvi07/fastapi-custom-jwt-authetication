from pydantic import BaseModel, validator



class UpdatePassword(BaseModel):
	# to update user password from admin panel
	old_password  		:	str
	new_password 		:  	str
	confirm_new_password: 	str

	@validator('old_password')
	def check_all_fields(cls, v, values):
		assert v is not None, "old password required"
		assert 'new_password' not in list(values.keys()), "New password required"
		assert ' confirm_new_password' not in list(values.keys()), " You should confirm new password"
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
			raise ValueError("password do not match")

		return v
		