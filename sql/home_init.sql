DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS property;

CREATE TABLE IF NOT EXISTS users(
userid VARCHAR(16) PRIMARY KEY,
first_name VARCHAR(64) NOT NULL,
last_name VARCHAR(64) NOT NULL,
email VARCHAR(64) UNIQUE NOT NULL,
contact VARCHAR(16) UNIQUE NOT NULL,
credit_card VARCHAR(32) NOT NULL,
identification_card VARCHAR(32) NOT NULL,
passport VARCHAR(32) NOT NULL,
rating NUMERIC NOT NULL DEFAULT 4);

CREATE TABLE IF NOT EXISTS property(
propertyid VARCHAR(16) PRIMARY KEY,
	--- same address ---
address VARCHAR(128) UNIQUE NOT NULL,
city VARCHAR(16) NOT NULL,
country VARCHAR(16) NOT NULL,
longitute DECIMAL(9,6) DEFAULT NULL,
latitude DECIMAL(9,6) DEFAULT NULL,
house_type VARCHAR(64) NOT NULL CONSTRAINT house_type CHECK (house_type = 'condominium' OR
															 house_type = 'villa' OR
															 house_type = 'studio' OR
															 house_type = 'single-storey' OR
															 house_type = 'double-storey' OR													 
															 house_type = 'other'),
number_of_bedrooms NUMERIC NOT NULL,
number_of_guests_allowed NUMERIC NOT NULL,
date_available DATE,
house_rules VARCHAR(128),
amenities VARCHAR(128),
duration NUMERIC NOT NULL, 
userid VARCHAR(16) NOT NULL,
FOREIGN KEY (userid) REFERENCES users(userid) ON DELETE CASCADE DEFERRABLE);
