DROP TABLE IF EXISTS pending;
DROP TABLE IF EXISTS case_log;
DROP TABLE IF EXISTS exchange;
DROP TABLE IF EXISTS property;
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users(
userid VARCHAR(200) PRIMARY KEY,
first_name VARCHAR(64) NOT NULL,
last_name VARCHAR(64) NOT NULL,
email VARCHAR(64) UNIQUE NOT NULL,
country_code VARCHAR(16) NOT NULL, 
contact VARCHAR(16) UNIQUE NOT NULL,
CONSTRAINT my_constraint CHECK 
((country_code = '+65' AND LENGTH(contact) = 8) OR
 (country_code = '+66' AND LENGTH(contact) = 8) OR
 (country_code = '+60' AND (LENGTH(contact) = 9 OR LENGTH(contact) = 10))), 
credit_card VARCHAR(12) NOT NULL,
identification_card VARCHAR(32) NOT NULL,
passport VARCHAR(32) NOT NULL CONSTRAINT passport CHECK (LENGTH(passport) = 8 OR
														 LENGTH(passport) = 9),
rating NUMERIC NOT NULL DEFAULT 4 CONSTRAINT rating CHECK (rating >= 0),
wallet NUMERIC NOT NULL DEFAULT 0 CONSTRAINT wallet CHECK (wallet >= 0));

CREATE TABLE IF NOT EXISTS property(
propertyid VARCHAR(200) PRIMARY KEY,
address VARCHAR(128) UNIQUE NOT NULL,
city VARCHAR(16) NOT NULL,
country VARCHAR(16) NOT NULL CONSTRAINT country CHECK (country = 'Singapore' OR
													   country = 'Malaysia' OR
													   country = 'Thailand'),
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
start_available DATE NOT NULL,
end_available DATE NOT NULL,
CONSTRAINT date_constraint1 CHECK(end_available > start_available),
house_rules VARCHAR(128),
amenities VARCHAR(128),
userid VARCHAR(200) NOT NULL,
active BOOLEAN NOT NULL DEFAULT TRUE, 
FOREIGN KEY (userid) REFERENCES users(userid) ON DELETE CASCADE DEFERRABLE);


CREATE TABLE IF NOT EXISTS exchange(
exchangeid VARCHAR(200) PRIMARY KEY,
userid1 VARCHAR(200) REFERENCES users(userid) ON DELETE CASCADE DEFERRABLE,
userid2 VARCHAR(200) REFERENCES users(userid) ON DELETE CASCADE DEFERRABLE,
propertyid1 VARCHAR(200) REFERENCES property(propertyid) ON DELETE CASCADE DEFERRABLE,
propertyid2 VARCHAR(200) REFERENCES property(propertyid) ON DELETE CASCADE DEFERRABLE,
start DATE NOT NULL,
ends DATE NOT NULL,
CONSTRAINT date_constraint2 CHECK(ends > start),
deposit NUMERIC NOT NULL DEFAULT 500,
deposit_refunded BOOLEAN NOT NULL DEFAULT FALSE,
revenue NUMERIC NOT NULL DEFAULT 50,
status1 VARCHAR(200) NOT NULL DEFAULT 'Confirmed' CONSTRAINT status1 CHECK (status1 = 'Confirmed' OR
																		 status1 = 'Closed' OR
																		 status1 = 'Closed with Complain'),
status2 VARCHAR(200) NOT NULL DEFAULT 'Confirmed' CONSTRAINT status2 CHECK (status2 = 'Confirmed' OR
																		 status2 = 'Closed' OR
																		 status2 = 'Closed with Complain'));
																		 
CREATE TABLE IF NOT EXISTS case_log(
caseid VARCHAR(200) PRIMARY KEY,
reasons VARCHAR(64) NOT NULL CONSTRAINT reasons CHECK (reasons = 'lost item' OR
													   reasons = 'vandalism' OR
													   reasons = 'house rules violation' OR
													   reasons = 'other'),
exchangeid VARCHAR(200) REFERENCES exchange(exchangeid) ON DELETE CASCADE DEFERRABLE,
complain_by_userid VARCHAR(200) REFERENCES users(userid) ON DELETE CASCADE DEFERRABLE,
complain_of_userid VARCHAR(200) REFERENCES users(userid) ON DELETE CASCADE DEFERRABLE);


CREATE TABLE pending(
requested_from VARCHAR(200) REFERENCES users(userid) ON DELETE CASCADE DEFERRABLE,
requested_to VARCHAR(200) REFERENCES users(userid) ON DELETE CASCADE DEFERRABLE,
requested_property VARCHAR(200) REFERENCES property(propertyid) ON DELETE CASCADE DEFERRABLE,
start_date DATE NOT NULL,
end_date DATE NOT NULL,
CONSTRAINT date_constraint4 CHECK (end_date > start_date),
PRIMARY KEY(requested_from,requested_to)
);



CREATE OR REPLACE FUNCTION user_update() 
RETURNS TRIGGER AS $$
    BEGIN
        -- when insertion is made in case_log table,
		-- update users table by:
        -- deduct user rating by 1
		-- give penalty to the user who get complain by -450 in wallet
		UPDATE users u
		SET rating = GREATEST(rating - 2, 0), wallet = GREATEST(wallet - 450, 0)
		WHERE NEW.complain_of_userid = u.userid;
		
		UPDATE users v
		SET wallet = wallet + 450
		WHERE NEW.complain_by_userid = v.userid;
		RETURN NEW;

	END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER complain
	AFTER INSERT ON case_log
    FOR EACH ROW
	EXECUTE FUNCTION user_update(); 

----- TEST CASES -----
/*
SELECT * FROM users;
insert into users (userid, first_name, last_name, email, country_code, contact, credit_card, identification_card, passport) values (4, 'Arthur', 'Loudyan', 'aloudyan3@gov.uk', '+60','430284400', '3050939856', '632-80-7129', '69447475');
insert into users (userid, first_name, last_name, email, country_code, contact, credit_card, identification_card, passport) values (5, 'Garret', 'Common', 'gcommon4@moonfruit.com', '+65','44676111', '4848841942', '123-70-3359', 'A1222405');

SELECT * FROM property;
insert into property (propertyid, address, city, country, longitute, latitude, house_type, number_of_bedrooms, number_of_guests_allowed, start_available, end_available, house_rules, amenities, userid) values (4, '12803 Old Shore Way', 'Kangdong-ŭp', 'Singapore', null, null, 'villa', 4, 4, '29/1/2022', '2/2/2022', null, null, 4);
insert into property (propertyid, address, city, country, longitute, latitude, house_type, number_of_bedrooms, number_of_guests_allowed, start_available, end_available, house_rules, amenities, userid) values (5, '29205 Sullivan Terrace', 'Darungan', 'Singapore', null, null, 'villa', 5, 5, '21/12/2021', '2/1/2022', null, null, 5);

SELECT * FROM exchange;
insert into exchange (exchangeid, userid1, userid2, propertyid1, propertyid2, start, ends) 
values (1,4,5,4,5,'29/1/2022', '2/2/2022');


SELECT * FROM case_log;
insert into case_log (caseid, reasons, exchangeid, complain_by_userid, complain_of_userid)
values (2,'lost item', 1,4,5);
insert into case_log (caseid, reasons, exchangeid, complain_by_userid, complain_of_userid)
values (6,'lost item', 1,5,4);

*/
create table geometry_test2(
userid varchar(20),
latitude decimal(9,6),
longitude decimal(9,6),
geom GEOMETRY(POINT, 4326));

UPDATE geometry_test2
  SET  geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
;

CREATE OR REPLACE FUNCTION updategeom ()
RETURNS Trigger
LANGUAGE plpgsql
AS $$
BEGIN
   NEW.geom = st_setsrid(st_point(NEW.longitude, NEW.latitude), 4326);
   RETURN NEW;
END;
$$;

CREATE TRIGGER 
geometry_test
BEFORE INSERT OR UPDATE of latitude,longitude on 
geometry_test2
FOR EACH ROW EXECUTE PROCEDURE updategeom ();
