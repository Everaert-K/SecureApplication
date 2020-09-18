from models.database import db
import mysql.connector

def get_users():
    """
    Retreive all registrered users from the database
        :return: users
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT userid, username from users")
    try:
        cursor.execute(query)
        users = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        users = []
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return users

def get_user_id_by_name(username):
    """
    Get the id of the unique username
        :param username: Name of the user
        :return: The id of the user
    """
    db.connect()
    cursor = db.cursor(prepared=True)
    query1 = ("SELECT userid from users WHERE username =\"" + username + "\"")
    userid = None
    try:
        # cursor.execute(query)
        cursor.execute("select userid from users where username = ?",(username,))
        # cursor.execute("select userid from users where username = %s",(username))
        # cursor.execute("select userid from users where username = \"?\"",(username))
        # cursor.execute("select userid from users where username = \"%s\"",(username))
        print(cursor.statement)
        users = cursor.fetchall()
        if(len(users)):
            userid = users[0][0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return userid

def get_user_name_by_id(userid):
    """
    Get username from user id
        :param userid: The id of the user
        :return: The name of the user
    """
    db.connect()
    cursor = db.cursor()
    # query = ("SELECT username from users WHERE userid =\"" + userid + "\"")
    username = None
    try:
        # cursor.execute(query)
        cursor.execute("SELECT username from users WHERE userid = %s"
                       , (userid,))
        users = cursor.fetchall()
        if len(users):
            username = users[0][0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return username

def get_twofactorpassword_by_username(username):
    db.connect()
    cursor = db.cursor()
    password = None
    try:
        cursor.execute("SELECT two_factor_key from users WHERE username = %s"
                       , (username,))
        users = cursor.fetchall()
        if len(users):
            password = users[0][0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return password

def match_user(username, password):
    """
    Check if user credentials are correct, return if exists

        :param username: The user attempting to authenticate
        :param password: The corresponding password
        :type username: str
        :type password: str
        :return: user
    """
    db.connect()
    cursor = db.cursor()
    user = None
    try:
        # cursor.execute(query)
        cursor.execute("SELECT userid, username from users where username = %s and password = %s"
                       , (username, password.decode("utf-8")))
        users = cursor.fetchall()
        if len(users):
            user = users[0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return user

def check_verification_link(verification_link):
    db.connect()
    cursor = db.cursor()
    query = ("SELECT username FROM users WHERE ver_link = \"" + verification_link + "\"")
    try:
        cursor.execute(query)
        username = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return username      

def get_ver_expires_by_verification_link(verification_link):
    db.connect()
    cursor = db.cursor()
    query = ("SELECT ver_expires FROM users WHERE ver_link = \"" + verification_link + "\"")
    try:
        cursor.execute(query)
        ver_expires = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return ver_expires    

def verify_user(verification_link):
    db.connect()
    cursor = db.cursor()
    query = ("UPDATE users SET ver_active = 1 WHERE ver_link = \"" + verification_link + "\"")
    try:
        cursor.execute(query)
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()

def get_ver_active_by_user_name(username):
    db.connect()
    cursor = db.cursor()
    query = ("SELECT ver_active FROM users WHERE username = \"" + username + "\"")
    try:
        cursor.execute(query)
        user = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return user 

def delete_user_by_verification_link(verification_link):
    db.connect()
    cursor = db.cursor()
    query = ("DELETE FROM users WHERE ver_link = \"" + verification_link + "\"")
    try:
        cursor.execute(query)
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()   

def change_password_by_email(email, new_password):
    db.connect()
    cursor = db.cursor()
    query = ("UPDATE users SET password = \"" + new_password.decode("utf-8") + "\" WHERE email = \"" + email + "\"") 
    try:
        cursor.execute(query)
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()  

def change_temp_password_flag_by_email(email, flag):
    db.connect()
    cursor = db.cursor()
    query = ("UPDATE users SET temp_password = " + str(flag) + " WHERE email = \"" + email + "\"")
    try:
        cursor.execute(query)
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()    

def change_temp_password_flag_by_password(password, flag):
    db.connect()
    cursor = db.cursor()
    query = ("UPDATE users SET temp_password = " + str(flag) + " WHERE password = \"" + password.decode("utf-8") + "\"")
    try:
        cursor.execute(query)
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()  

def get_temp_password_flag_by_user_name(username):
    db.connect()
    cursor = db.cursor()
    query = ("SELECT temp_password FROM users WHERE username = \"" + username + "\"")
    try:
        cursor.execute(query)
        flag = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return flag     

def check_temporary_password_by_user_id(userid):
    db.connect()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT username FROM users WHERE userid = %s AND temp_password = 1", (userid,))
        username = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return username   

def set_password_by_temporary_password(old_password, new_password):
    db.connect()
    cursor = db.cursor()
    query = ("UPDATE users SET password = \"" + new_password.decode("utf-8") + "\" WHERE password = \"" + old_password.decode("utf-8") + "\"")
    try:
        cursor.execute(query)
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()  

def get_user_id_by_temporary_password(temporary_password):
    db.connect()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT userid FROM users WHERE password=%s", (temporary_password.decode("utf-8"),)) 
        userid = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()   
    return userid

def get_user_id_by_email(email):
    db.connect()
    cursor = db.cursor()
    query = ("SELECT userid FROM users WHERE email = \"" + email + "\"")
    try:
        cursor.execute(query)
        userid = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return userid 

def get_user_name_by_email(email):
    db.connect()
    cursor = db.cursor()
    query = ("SELECT username FROM users WHERE email = \"" + email + "\"")
    try:
        cursor.execute(query)
        username = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return username 

def register_old_password(userid, password):
    db.connect()
    cursor = db.cursor()
    #query = ("INSERT INTO old_passwords VALUES (NULL, %s, %s)", (userid, password.decode("utf-8")))
    try:
        #cursor.execute(query)
        cursor.execute("INSERT INTO old_passwords VALUES (NULL, %s, %s)",
        (userid, password.decode('utf-8'))) 
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close() 

def match_user_id_and_old_password(userid, password):
    db.connect()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT old_passwordid FROM old_passwords WHERE userid = %s AND old_password  =%s", (userid,password.decode("utf-8")))
        old_passwordid = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close() 
    return old_passwordid    

def get_password_hash_by_username(username):
    db.connect()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        password_hash = cursor.fetchall()[0][0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close() 
    return password_hash    

def get_all_userid_password():
    db.connect()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT userid, password FROM users")
        users = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close() 
    return users    

def get_old_password_hashes_by_user_id(userid):
    db.connect()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT old_password FROM old_passwords WHERE userid = %s", (userid,))
        password_hashes = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close() 
    return password_hashes   

def set_password_by_user_id(userid, password):
    db.connect()
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE users SET password = %s WHERE userid = %s", 
            (password.decode("utf-8"),userid))
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close() 

def set_temp_password_flag_by_user_id(userid, flag_value):
    db.connect()
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE users SET temp_password = %s WHERE userid = %s", 
            (flag_value,userid))
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()     




  