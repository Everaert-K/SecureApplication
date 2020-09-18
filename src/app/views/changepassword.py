import web
from views.forms import changepassword_form
import models.user
from views.utils import get_nav_bar
import json
import hashlib
import logging
import bcrypt
import re

# Get html templates
render = web.template.render('templates/')


class Change_password():

	def GET(self):
		"""
		Show the change password page where user can change password to a new
			
			:return: The change password page with a form to change password
		"""
		session = web.ctx.session
		nav = get_nav_bar(session)

		return render.changepassword(nav, changepassword_form, "")

	def POST(self):
		"""
		Change the password
			:return:  The change password page with message if the password was change with success
		"""
		session = web.ctx.session
		nav = get_nav_bar(session)
		data = web.input()

		# Check if new password matches twice
		if data.new_password1 != data.new_password2:
			return render.changepassword(nav, changepassword_form, "The new password did not match both times")

		# Get list of users and password hashes: [(userid1, password_hash1),(userid1, password_hash2), ...]
		users = models.user.get_all_userid_password()

		# Find userid related to the temporary password
		userid = None
		for user in users:
			if (bcrypt.checkpw(data.old_password.encode("utf-8"), user[1].encode("utf-8"))):
				userid = user[0]
				break

		# Do more validation tests on password strength
		extra_validation = passwordValidation(data.old_password, data.new_password1, userid)

		# If password validation tests fail, render the page again and let user try again
		if extra_validation:
			return render.changepassword(nav, changepassword_form, extra_validation)        

		# If the password related to the userid is registered as temporary, the user can change password
		if models.user.check_temporary_password_by_user_id(userid):
			#Set new password hash
			new_password_hash = bcrypt.hashpw(data.new_password1.encode("utf-8"), bcrypt.gensalt())
			#Change to the new password
			models.user.set_password_by_user_id(userid, new_password_hash)
			#Turn off temporary password flag
			models.user.set_temp_password_flag_by_user_id(userid, 0)
			#Save new password in old passwords table
			models.user.register_old_password(userid, new_password_hash)
			return render.changepassword(nav, None, "Password changed. You can now log in")
		else:
			return render.changepassword(nav, changepassword_form, "Temporary password not valid. Try again")

#The regex validation for forms was very buggy for several tests. We use our own below.
def passwordValidation(temporary_password, new_password, userid):
	#Check for lowercase letters
	if not re.search(r"[a-z]",new_password):
		return "Invalid input: no lowercase. Password must include lowercase letters [a-z], uppercase letters [A-Z], integers [0-9] and symbols [!-?]"
	#Check for uppercase let	ters
	if not re.search(r"[A-Z]",new_password):
		return "Invalid input: no uppercase. Password must include lowercase letters [a-z], uppercase letters [A-Z], integers [0-9] and symbols [!-?]"
	#Check for integers
	if not re.search(r"[0-9]",new_password):
		return "Invalid input: no integers. Password must include lowercase letters [a-z], uppercase letters [A-Z], integers [0-9] and symbols [!-?]"
	#Check for symbols
	if not re.search(r"\W",new_password):
		return "Invalid input: no symbols. Password must include lowercase letters [a-z], uppercase letters [A-Z], integers [0-9] and symbols [!-?]"
	# Get list of old passwords hashes related to user with userid: [(password_hash1,),(password_hash2,)]
	old_password_hashes = models.user.get_old_password_hashes_by_user_id(userid)
	# Check if user with userid has used any of the passwords before
	for old_password_hash in old_password_hashes:
		if bcrypt.checkpw(new_password.encode("utf-8"), old_password_hash[0].encode("utf-8")):
			return "Invalid input. Choose a password that you have not used before"
	return None

		

