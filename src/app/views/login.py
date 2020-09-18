import web
from views.forms import login_form
import models.user, models.lockout
from views.forms import changepassword_form
from views.utils import get_nav_bar
import os, hmac, base64 #, pickle
import json
import hashlib
import logging
import bcrypt
import struct, time

from views.login_utils import *
import views.login_state as ls


# Get html templates
render = web.template.render('templates/')
# Log config
logging.basicConfig(filename='beelance.log',level=logging.INFO, format='%(asctime)s %(message)s')


class Login():

    # Get the server secret to perform signatures
    secret = web.config.get('session_parameters')['secret_key']

    def GET(self):
        """
        Show the login page
            
            :return: The login page showing other users if logged in
        """
        session = web.ctx.session
        nav = get_nav_bar(session)

        # Log the user in if the rememberme cookie is set and valid
        self.check_rememberme()
        return render.login(nav, login_form, "")

    def POST(self):
        """
        Log in to the web application and register the session
            :return:  The login page showing other users if logged in
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        data = web.input(username="", password="", remember=False, twoFactor="")

        app = ls.AppData( 
            session,
            nav,
            data,
            render
        )

        if ls.tryLogin(app):
            self.login(
                data.username, 
                models.user.get_user_id_by_name(data.username), 
                data.remember
                )
            raise web.seeother("/")
        else:
            return app.return_value
       

        

        

    def login(self, username, userid, remember):
        """
        Log in to the application
        """
        session = web.ctx.session
        session.username = username
        session.userid = userid
        logging.info("LOGIN success: %s | True | %s" % (session.username, session.ip))
        if remember:
            rememberme = self.rememberme()
            # web.setcookie('remember', rememberme , 600, None, True)
            web.setcookie('remember', rememberme, 600)

    def check_rememberme(self):
        """
        Validate the rememberme cookie and log in
        """
        username = ""
        sign = ""
        # If the user selected 'remember me' they log in automatically
        try:
            # Fetch the users cookies if it exists
            cookies = web.cookies()
            # Fetch the remember cookie and convert from string to bytes
            remember_hash = bytes(cookies.remember[2:][:-1], 'ascii')
            # Decode the hash
            decode = base64.b64decode(remember_hash)
            # Load the decoded hash to receive the host signature and the username
            # username, sign = pickle.loads(decode)
            username, sign = json.load(decode)
        except AttributeError as e:
            # The user did not have the stored remember me cookie
            pass

        # If the users signed cookie matches the host signature then log in
        if self.sign_username(username) == sign:
            userid = models.user.get_user_id_by_name(username)
            self.login(username, userid, False)

    def rememberme(self):
        """
        Encode a base64 object consisting of the username signed with the
        host secret key and the username. Can be reassembled with the
        hosts secret key to validate user.
            :return: base64 object consisting of signed username and username
        """
        session = web.ctx.session
        creds = [ session.username, self.sign_username(session.username) ]
        # return base64.b64encode(pickle.dumps(creds))
        return json.dumps(creds)

    @classmethod
    def sign_username(self, username):
        """
        Sign the current users name with the hosts secret key
            :return: The users signed name
        """
        secret = base64.b64decode(self.secret)
        return hmac.HMAC(secret, username.encode('ascii')).hexdigest()
 