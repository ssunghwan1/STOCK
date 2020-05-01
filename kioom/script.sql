Create table BASE_DATA(
	STOCK_CODE VARCHAR(40),
STOCK_NAME VARCHAR(40),
TOTAL VARCHAR(40),
PER VARCHAR(40),
EPS VARCHAR(40),
ROE VARCHAR(40),
PBR VARCHAR(40),
BPS VARCHAR(40),
SALES VARCHAR(40),
BENEFIT VARCHAR(40),
AFTERBENEFIT VARCHAR(40),
CURRENT_PRICE varchar(40)
);
alter table BASE_DATA add CURRENT_PRICE varchar(40);
SELECT * FROM BASE_DATA;
delete from BASE_DATA;


CREATE TABLE PLAYER (
       PLAYER_ID                CHAR(7)             NOT NULL,
       PLAYER_NAME        VARCHAR2(20)  NOT NULL,
       TEAM_ID                   CHAR(3)             NOT NULL,
       E_PLAYER_NAME   VARCHAR2(40),
       NICKNAME               VARCHAR2(30),
       JOIN_YYYY               CHAR(4),
       POSITION                  VARCHAR2(10),
       BACK_NO                 NUMBER(2),
       NATION                     VARCHAR2(20),
       BIRTH_DATE            DATE,
       SOLAR                      CHAR(1),
       HEIGHT                    NUMBER(3),
       WEIGHT                   NUMBER(3),

