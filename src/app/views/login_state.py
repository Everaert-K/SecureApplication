import models.user, models.lockout
from views.forms import login_form
import bcrypt
import views.login_utils as utils
import web
import logging

# Log config
logging.basicConfig(filename='beelance.log',level=logging.INFO, format='%(asctime)s %(message)s')

Yes = True
No = False


class AppData:
    def __init__(self,session, nav, data, render):
        self.session = session
        self.nav = nav
        self.data = data
        self.render = render
        self.return_value = None
        self.success = False

class State:

    @staticmethod
    def nextYes(): 
        return None

    @staticmethod
    def nextNo():
        return None

    @staticmethod
    def isValid(app):
        return False


class IsLockedOutState(State):

    @staticmethod
    def nextYes(): 
        return RenderLoginLockedOutState

    @staticmethod
    def nextNo():
        return IsUsernameValidState

    @staticmethod
    def isValid(app):

        if (models.lockout.check_lockout(app.data.username)):
            return Yes
        return No



class RenderLoginLockedOutState(State):
    
    @staticmethod
    def nextYes(): 
        return None

    @staticmethod
    def nextNo():
        return None

    @staticmethod
    def isValid(app):
        app.return_value = app.render.login(app.nav, login_form, "- User locked out")
        return No

class IsUsernameValidState(State):

    @staticmethod
    def nextYes(): 
        return IsMatchingUsernamePasswordState

    @staticmethod
    def nextNo():
        return IsLoginAttemptsExceededState

    @staticmethod
    def isValid(app):
        if models.user.get_user_id_by_name(app.data.username):
            return Yes
        return No

class IsMatchingUsernamePasswordState(State):
    
    @staticmethod
    def nextYes(): 
        return IsMatchingTokenTwoFactorState

    @staticmethod
    def nextNo():
        return IsLoginAttemptsExceededState

    @staticmethod
    def isValid(app):

        password_hash = models.user.get_password_hash_by_username(app.data.username)

        if bcrypt.checkpw(app.data.password.encode("utf-8"), password_hash.encode("utf-8")):

            if models.user.match_user(app.data.username, password_hash.encode("utf-8")):
                return Yes

        return No

class IsMatchingTokenTwoFactorState(State):
    
    @staticmethod
    def nextYes(): 
        return DoDeleteLoginAttemptsState

    @staticmethod
    def nextNo():
        return IsLoginAttemptsExceededState

    @staticmethod
    def isValid(app):        
        twoFactorPassword = app.data.twoFactor
        token = utils.give_token(app.data.username)

        if twoFactorPassword == token:
            return Yes
        return No

class DoDeleteLoginAttemptsState(State):
    
    @staticmethod
    def nextYes(): 
        return IsUserAccountVerifiedState

    @staticmethod
    def nextNo():
        return None

    @staticmethod
    def isValid(app):
        models.lockout.delete_logins(app.data.username)
        return Yes # Should ALWAYS return Yes


class IsUserAccountVerifiedState(State):
    
    @staticmethod
    def nextYes(): 
        return IsUsingTemporaryPasswordState

    @staticmethod
    def nextNo():
        return RenderLoginEmailMessageState

    @staticmethod
    def isValid(app):
        if (models.user.get_ver_active_by_user_name(app.data.username)[0][0] == 1):
            return Yes
        return No



class IsUsingTemporaryPasswordState(State):
    
    @staticmethod
    def nextYes(): 
        return SendToChangePasswordState

    @staticmethod
    def nextNo():
        return DoLoginState

    @staticmethod
    def isValid(app):
        if models.user.get_temp_password_flag_by_user_name(app.data.username)[0][0] == 1:
            return Yes
        return No

class RenderLoginEmailMessageState(State):
    
    @staticmethod
    def nextYes(): 
        return None

    @staticmethod
    def nextNo():
        return None

    @staticmethod
    def isValid(app):
        app.return_value = app.render.login(app.nav, login_form, "- User not verified. Please check your email")
        return Yes

class SendToChangePasswordState(State):
    
    @staticmethod
    def nextYes(): 
        return None

    @staticmethod
    def nextNo():
        return None

    @staticmethod
    def isValid(app):
        raise web.seeother("/changepassword")
       #return Yes

class DoAddLoginAttemptState(State):
    
    @staticmethod
    def nextYes(): 
        return RenderLoginFailedAuthState

    @staticmethod
    def nextNo():
        return None

    @staticmethod
    def isValid(app):
        models.lockout.set_login(app.data.username, app.session.ip)
        logging.info("LOGIN failed: %s | %s | %s" % (app.data.username, bool(models.user.get_user_id_by_name(app.data.username)), app.session.ip))
        return Yes # Always return Yes

class RenderLoginFailedAuthState(State):
    
    @staticmethod
    def nextYes(): 
        return None

    @staticmethod
    def nextNo():
        return None

    @staticmethod
    def isValid(app):
        app.return_value = app.render.login(app.nav, login_form, "- User authentication failed")
        return Yes

class IsLoginAttemptsExceededState(State):
    
    @staticmethod
    def nextYes(): 
        return DoAddUserLockedOutState

    @staticmethod
    def nextNo():
        return DoAddLoginAttemptState

    @staticmethod
    def isValid(app):
        timestamps = models.lockout.get_timestaps(app.data.username)
        if len(timestamps) >= 4:
            return Yes
        return No
    
class DoAddUserLockedOutState(State):
    
    @staticmethod
    def nextYes(): 
        return RenderLoginLockedOutState

    @staticmethod
    def nextNo():
        return None

    @staticmethod
    def isValid(app):
        models.lockout.set_lockout(app.data.username)
        logging.info("LOCKED OUT: %s | %s | %s" % (app.data.username, bool(models.user.get_user_id_by_name(app.data.username)), app.session.ip))
        return Yes # Always yes    

class DoLoginState(State):
    
    @staticmethod
    def nextYes(): 
        return None

    @staticmethod
    def nextNo():
        return None

    @staticmethod
    def isValid(app):
        app.success = True

        return Yes # Always yes


def tryLogin(app):
    state = IsLockedOutState

    while state:

        if state.isValid(app):
            state = state.nextYes()
        else:
            state = state.nextNo()
    
    return app.success
        

if __name__ == "__main__":
    pass