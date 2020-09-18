import web
from views.forms import register_form
import models.register
import models.user
from views.utils import get_nav_bar
import hashlib
import re
import bcrypt
from datetime import datetime, timedelta

# Get html templates
render = web.template.render('templates/')


class Register:

    def GET(self):
        """
        Get the registration form

            :return: A page with the registration form
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        return render.register(nav, register_form, "")

    def POST(self):
        """
        Handle input data and register new user in database

            :return: Main page
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        data = web.input()

        register = register_form()

        if not register.validates():
            return render.register(nav, register, "All fields must be valid.")

        #Do more validation tests on password strength
        extra_validation = passwordValidation(data.password)

        #Do more validation tests on password strength
        if extra_validation:
        	return render.register(nav, register, extra_validation)

        # Check if user exists
        if models.user.get_user_id_by_name(data.username):
            return render.register(nav, register, "Invalid user, already exists.")

        #Check if email exists
        if models.user.get_user_id_by_email(data.email):
            return render.register(nav, register, "Invalid email, email already exists.")

        # Generate value for verification link
        verification_link = bcrypt.hashpw(str.encode(str(data.email)),bcrypt.gensalt())

        #Generate expirement time for verification link
        verification_expires = str(datetime.now() + timedelta(minutes=15))[0:19]

        #Generate password hash
        password_hash = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt())

        #Register user
        models.register.set_user(data.username, password_hash,
            data.full_name, data.company, data.email, data.street_address, 
            data.city, data.state, data.postal_code, data.country, verification_link, 
            verification_expires, '0', '0', data.two_factor_key)

        #Register password in old passwords table
        userid = int(models.user.get_user_id_by_name(data.username))
        models.user.register_old_password(userid, password_hash)

        #TODO: Send email with verification link.
        """
        message = ("Your username is " + data.username + ". Please click this link to verify: \n" + \
            "https://molde.idi.ntnu.no:8022/verification?verification=" + (str(verification_link))[2:len(str(verification_link))-1])
        subject = '[Beelance] Verify your email address'
        web.sendmail('beelance@molde.idi.ntnu.no', str(data.email), str(subject), str(message))
        """

        return render.register(nav, register_form, "User registered! You have received an email \
            on your provided email address. Please click the activation link \
            in order to activate your account. [The following is thought for email only, \
            but showing as cleartext in case you run into problems] Your verification link is \
            https://molde.idi.ntnu.no:8022/verification?verification=" + (str(verification_link))[2:len(str(verification_link))-1])

#The regex validation for forms was very buggy for several tests. We use our own below.
def passwordValidation(password):
	if not re.search(r"[a-z]",password):
		return "Invalid input: no lowercase. Password must include lowercase letters [a-z], uppercase letters [A-Z], integers [0-9] and symbols [!-?]"
	if not re.search(r"[A-Z]",password):
		return "Invalid input: no uppercase. Password must include lowercase letters [a-z], uppercase letters [A-Z], integers [0-9] and symbols [!-?]"
	if not re.search(r"[0-9]",password):
		return "Invalid input: no integers. Password must include lowercase letters [a-z], uppercase letters [A-Z], integers [0-9] and symbols [!-?]"
	if not re.search(r"\W",password):
		return "Invalid input: no symbols. Password must include lowercase letters [a-z], uppercase letters [A-Z], integers [0-9] and symbols [!-?]"
	return None
