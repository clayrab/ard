#sudo mysqladmin create ard
#login as root and run:
#CREATE USER 'clay'@'localhost' IDENTIFIED BY 'password';
#GRANT ALL on ard.* to clay;
#Run this script as clay

use ard;
CREATE TABLE users (username VARCHAR(50) PRIMARY KEY, passhash VARCHAR(64) NOT NULL);
#INSERT INTO users VALUES ('clay','asdf');