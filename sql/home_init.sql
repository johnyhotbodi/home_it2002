DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS property;
DROP TABLE IF EXISTS exchange;
DROP TABLE IF EXISTS case_log;
DROP TABLE IF EXISTS pending;

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
propertyid VARCHAR(200) PRIMARY KEY,
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


CREATE TABLE IF NOT EXISTS exchange(
exchangeid VARCHAR(16) PRIMARY KEY,
userid1 VARCHAR(16) REFERENCES users(userid) ON DELETE CASCADE DEFERRABLE,
userid2 VARCHAR(16) REFERENCES users(userid) ON DELETE CASCADE DEFERRABLE,
propertyid1 VARCHAR(200) REFERENCES property(propertyid) ON DELETE CASCADE DEFERRABLE,
propertyid2 VARCHAR(200) REFERENCES property(propertyid) ON DELETE CASCADE DEFERRABLE,
start DATE NOT NULL,
ends DATE NOT NULL,
deposit NUMERIC NOT NULL DEFAULT 500,
insurance BOOLEAN NOT NULL,
deposit_refunded BOOLEAN NOT NULL DEFAULT FALSE,
revenue NUMERIC NOT NULL DEFAULT 50);

CREATE TABLE IF NOT EXISTS case_log(
caseid VARCHAR(16) PRIMARY KEY,
reasons VARCHAR(64) NOT NULL CONSTRAINT reasons CHECK (reasons = 'lost item' OR
													   reasons = 'vandalism' OR
													   reasons = 'house rules violation' OR
													   reasons = 'other'),
complain_by_userid VARCHAR(16) REFERENCES users(userid) ON DELETE CASCADE DEFERRABLE,
complain_of_userid VARCHAR(16) REFERENCES users(userid) ON DELETE CASCADE DEFERRABLE,
deposit_deduction BOOLEAN NOT NULL DEFAULT FALSE,
rating_deduction BOOLEAN NOT NULL DEFAULT FALSE,
status BOOLEAN NOT NULL DEFAULT FALSE,
remarks VARCHAR(128) DEFAULT 'None');

CREATE TABLE pending(
requested_from VARCHAR(16) REFERENCES users(userid) ON DELETE CASCADE DEFERRABLE,
requested_to VARCHAR(16) REFERENCES users(userid) ON DELETE CASCADE DEFERRABLE,
start_date DATE NOT NULL,
end_date DATE NOT NULL,
from_insurance BOOLEAN NOT NULL,
PRIMARY KEY(requested_from,requested_to)
);