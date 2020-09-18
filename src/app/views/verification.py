import web
import models.user
from views.utils import get_nav_bar
import datetime

# Get html templates
render = web.template.render('templates/')

class Verification():

    def GET(self):
        """
        Show the verification page
            
            :return: The verification page showing a confirmation that the user i verified
        """
        session = web.ctx.session
        nav = get_nav_bar(session)

        #Get verification link value as URL input. "Invalid" by default
        data = web.input(verification="invalid")

        ver = "Verification link not valid"

        if data.verification:
        	#Check if the verification link exists in the database
            if models.user.check_verification_link(data.verification):
            	#Get expirement date and time for the provided verification link
            	ver_expires = models.user.get_ver_expires_by_verification_link(data.verification)[0][0]
            	#Check if expirement date is later than today
            	if check_verification_expirement(ver_expires):
            		models.user.verify_user(data.verification)
            		ver = "Thank you for verifying. You can now log in"
            	else:
            		ver = "Verification link expired. Your user has been deleted. Please register again"
            		models.user.delete_user_by_verification_link(data.verification)

        return render.verification(nav, ver)

#Return true if verification link has not expired, i.e. ver_expires > now
def check_verification_expirement(ver_expires):
	date_now = str(datetime.datetime.now())
	ver_expires = str(ver_expires)
	#Check yyyy (not really necessary, but as an edge case it's ok to include)
	if int(ver_expires[0:4]) < int(date_now[0:4]):
		#Return False if expirement year is less than date now
		return False
	if int(ver_expires[0:4]) > int(date_now[0:4]):
		#Return True if expirement year is bigger than date now
		return True
	#Check mm,dd,hh,mm,ss
	for i in range(5,15,3):
		if int(ver_expires[i:(i+2)]) < int(date_now[i:(i+2)]):
			#Return False if value of expirement date is less than date now
			return False
		if int(ver_expires[i:(i+2)]) > int(date_now[i:(i+2)]):
			#Return True if value of expirement date is bigger than date now
			return True
	#Return true if they are the same
	return True