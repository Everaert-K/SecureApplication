-- SET @@global.sql_mode= 'NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'

CREATE TABLE users (
  userid INT UNSIGNED AUTO_INCREMENT,
  username VARCHAR(45) UNIQUE NOT NULL,
  -- password VARCHAR(45) NOT NULL,
  password BINARY(60) NOT NULL,
  full_name VARCHAR(200) NOT NULL,
  company VARCHAR(50),
  email VARCHAR(50) NOT NULL,
  street_address VARCHAR(50),
  city VARCHAR(50),
  state VARCHAR(50),
  postal_code VARCHAR(50),
  country VARCHAR(50),
  ver_link BINARY(60),-- NOT NULL, --link value that is sent to user on email
  ver_expires DATETIME,-- NOT NULL, -- date and time when the link expires
  ver_active BOOLEAN, -- boolean showing whether user has activated account by clicking link
  temp_password BOOLEAN, -- NOT NULL, --flag for temporary password. 1 = temp password in use, 0 = normal password in use
  two_factor_key VARCHAR(200),
  PRIMARY KEY (userid)
);

-- TODO: add underscores to column names
CREATE TABLE login_attempt (
  loginid INT UNSIGNED AUTO_INCREMENT,
  loginname VARCHAR(45) NOT NULL, 
  ipaddress VARCHAR(45) NOT NULL, 
  logintime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
  PRIMARY KEY (loginid)
);

CREATE TABLE lockedout_users (
  lockoutid INT UNSIGNED AUTO_INCREMENT, 
  lockout_name VARCHAR(45) NOT NULL,
  start_lockout_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
  PRIMARY KEY (lockoutid)
);

CREATE TABLE project_category (
  categoryid INT UNSIGNED AUTO_INCREMENT,
  category_name VARCHAR(200) UNIQUE NOT NULL,
  PRIMARY KEY (categoryid)
);

CREATE TABLE users_categories (
  userid INT UNSIGNED NOT NULL,
  categoryid INT UNSIGNED NOT NULL,
  PRIMARY KEY (userid, categoryid),
  FOREIGN KEY (userid) REFERENCES users(userid),
  FOREIGN KEY (categoryid) REFERENCES project_category(categoryid)
);

CREATE TABLE projects (
  projectid INT UNSIGNED AUTO_INCREMENT,
  categoryid INT UNSIGNED NOT NULL,
  userid INT UNSIGNED NOT NULL,
  title VARCHAR(200) NOT NULL,
  project_description VARCHAR(500) NOT NULL,
  project_status VARCHAR(16) NOT NULL, -- This should be either open, in progress or finished
  PRIMARY KEY (projectid),
  FOREIGN KEY (categoryid) REFERENCES project_category(categoryid),
  FOREIGN KEY (userid) REFERENCES users(userid)
);

CREATE TABLE projects_users (
  projectid INT UNSIGNED NOT NULL,
  userid INT UNSIGNED NOT NULL,
  read_permission BOOLEAN,
  write_permission BOOLEAN,
  modify_permission BOOLEAN,
  PRIMARY KEY (projectid, userid),
  FOREIGN KEY (projectid)  REFERENCES projects(projectid),
  FOREIGN KEY (userid) REFERENCES users(userid)
);

CREATE TABLE tasks (
  taskid INT UNSIGNED AUTO_INCREMENT,
  projectid INT UNSIGNED NOT NULL,
  title VARCHAR(200) NOT NULL,
  task_description VARCHAR(500) NOT NULL,
  budget INT NOT NULL,
  task_status VARCHAR(64) NOT NULL, -- This should be Waiting for delivery, delivered, accepted and declined delivery
  feedback VARCHAR(500) NULL,
  PRIMARY KEY (taskid),
  FOREIGN KEY (projectid) REFERENCES projects(projectid)
);

CREATE TABLE task_files (
  fileid INT NOT NULL AUTO_INCREMENT,
  taskid INT UNSIGNED NOT NULL,
  filename VARCHAR(45) NOT NULL,
  PRIMARY KEY (fileid),
  FOREIGN KEY (taskid) REFERENCES tasks(taskid)
);

CREATE TABLE old_passwords (
  old_passwordid INT UNSIGNED AUTO_INCREMENT,
  userid INT UNSIGNED NOT NULL,
  old_password BINARY(60) NOT NULL,
  PRIMARY KEY (old_passwordid),
  FOREIGN KEY (userid) REFERENCES users(userid)
);

/*
* Initial data
*/

/*
-- insert into users values (NULL, "admin", "48bead1bb864138c2cafaf1bd41332ab", "Admin Modsen", "ntnu", 'mail@ntnu.no', "street", "trondheim", "trondheim", "1234", "norway", "48bead1bb864138c2cafaf1bd41332ab", '1000-01-01 00:00:00', true, false);
*/
insert into project_category values (NULL, "Gardening");
insert into project_category values (NULL, "Programming");
insert into project_category values (NULL, "Grocery shopping");

/*
Create default database user 
*/

CREATE USER 'root'@'10.5.0.6' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON db.* TO 'root'@'10.5.0.6';

