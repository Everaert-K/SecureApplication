import web
from views.forms import login_form
import models.user
from views.utils import get_nav_bar
import os, hmac, base64 #, pickle
import json
import hashlib
import logging
import bcrypt
from views.forms import send_new_password_form

# Get html templates
render = web.template.render('templates/')


class New_password():

    def GET(self):
        """
        Show the new password page
            
            :return: The new password page 
        """
        session = web.ctx.session
        nav = get_nav_bar(session)

        return render.newpassword(nav, send_new_password_form, "")

    def POST(self):
        """
        Send email to provided email address wth temporary password
            :return:  The new password page confirming that temporary password is sent
        """
        session = web.ctx.session
        nav = get_nav_bar(session)       

        data = web.input()

        # Check if provided email exists in database
        username = models.user.get_user_name_by_email(data.email)
        if username:
            # Generate new password
            password = str(bcrypt.hashpw(str.encode(str(data.email)),bcrypt.gensalt()))
            password = password[((len(password)//8)+2):(len(password)//3)]
            password.replace(".", "")
            password.replace("/","")

            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Change password in database
            models.user.change_password_by_email(data.email, password_hash)

            # Set flag for temporary password active
            models.user.change_temp_password_flag_by_email(data.email, 1)

            #TODO: Add expirement for temporary password (low priority)

            #Get username as string
            username = username[0][0]

            #Generate message for email
            out_message = ("[The following is meant for email. Just putting it here \
                in cleartext in case you run into problems] Your username \
                is " + username + ". Temporary password: " + password)

            #TODO: Send email with the temporary password
            #web.config.smtp_server = "molde.idi.ntnu.no:25"
            #web.sendmail('beelance@molde.idi.ntnu.no', str(data.email), "New password for Beelance", str(out_message))

            return render.newpassword(nav, None, out_message)

        else:
            return render.newpassword(nav, send_new_password_form, "Email not valid. Try again")

        




 