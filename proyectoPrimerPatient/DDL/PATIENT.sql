CREATE TABLE PATIENT (
	ID INT NOT NULL AUTO_INCREMENT,
	IDENTIFIER VARCHAR(50),
	FIRST_NAME VARCHAR(30),
	LAST_NAME VARCHAR(30),
	ACTIVE BOOLEAN,
	GENDER VARCHAR(1),
	BIRTH_DATE DATE,
	PRIMARY KEY (ID)
);