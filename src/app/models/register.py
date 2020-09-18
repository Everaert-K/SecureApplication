from models.database import db
import mysql.connector

def set_user(username, password, full_name, company, email, 
        street_address, city, state, postal_code, country, 
        ver_link, ver_expires, ver_active, temp_password,twofactorpassword):
    """
    Register a new user in the database
        :param username: The users unique user name
        :param password: The password
        :param full_name: The users full name
        :param company: The company the user represents
        :param email: The users email address
        :param street_address: The street address of the user
        :param city: The city where the user lives
        :param state: The state where the user lives
        :param postal_code: The corresponding postal code
        :param country: The users country
        :param ver_link: Verification link for verifying upon registration
        :param ver_expires: Expiration time for verification link
        :param ver_active: Checking whether user has verified registration or not
        :type username: str
        :type password: str
        :type full_name: str
        :type company: str
        :type email: str
        :type street_address: str
        :type city: str
        :type state: str
        :type postal_code: str
        :type country: str
        :type ver_link: str
        :type ver_expires: datetime
        :type ver_active: boolean
    """
    db.connect()
    cursor = db.cursor() 
    try:
        # cursor.execute(query)
        cursor.execute("INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (username, password.decode("utf-8"), full_name, company, email, street_address, city, state, 
                        postal_code, country, ver_link.decode("utf-8"), ver_expires, ver_active, temp_password, twofactorpassword))
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
