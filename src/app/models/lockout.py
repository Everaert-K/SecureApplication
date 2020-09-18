from models.database import db
import mysql.connector

def set_lockout(lockout_name):
    """
    Register a username as locked out of the system 
        :param lockout_name: Username to lockout of system
        :type lockout_name: str
    """
    db.connect()
    cursor = db.cursor()
    query = ("INSERT INTO lockedout_users VALUES (NULL, \"" + lockout_name + "\", NULL)")
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

def check_lockout(lockout_name):
    """
    Check if user is marked as locked out of system
        :param lockout_name: Username used to attempt login
        :return: start time for the lockout
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT start_lockout_time from lockedout_users where lockout_name = \"" + lockout_name + "\" and start_lockout_time >= NOW() - INTERVAL 10 MINUTE")
    start_lockout_time = None
    try:
        cursor.execute(query)
        start_lockout_time = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return start_lockout_time

def set_login(loginname, ipaddress):
    """
    Register a new failed login attempt in the database
        :param loginname: Username used to attempt login
        :param ipaddress: The ipaddress 
        :type loginname: str
        :type ipaddress: str
    """
    db.connect()
    cursor = db.cursor()
    query = ("INSERT INTO login_attempt VALUES (NULL, \"" + loginname + "\", \"" + ipaddress + "\" , NULL)")
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

def delete_logins(loginname):
    """
    Delete login attempts for a user in the database
        :param loginname: Username to remove from table
        :type loginname: str
    """
    db.connect()
    cursor = db.cursor()
    query = ("DELETE FROM login_attempt WHERE loginname =\"" + loginname + "\"")
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

def get_timestaps(loginname): 
    """
    Retreive all timestamps of login attempts in the last 10 mintues for a specific user
        :param loginname: Username used to attempt login
        :return: timestamps
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT logintime from login_attempt WHERE loginname =\"" + loginname + "\" and logintime >= NOW() - INTERVAL 10 MINUTE")

    try:
        cursor.execute(query)
        timestamps = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        timestamps = []
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return timestamps