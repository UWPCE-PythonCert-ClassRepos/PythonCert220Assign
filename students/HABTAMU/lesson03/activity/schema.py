sqlite > .schema

CREATE TABLE "person" ("person_name" VARCHAR(30) NOT NULL PRIMARY KEY, "lives_in_town" VARCHAR(40) NOT NULL, "nickname" VARCHAR(20))
CREATE TABLE "job" ("job_name" VARCHAR(30) NOT NULL PRIMARY KEY, "start_date" DATE NOT NULL, "end_date" DATE NOT NULL, "salary" DECIMAL(7, 2) NOT NULL, "person_employed_id" VARCHAR(30) NOT NULL, FOREIGN KEY("person_employed_id") REFERENCES "person" ("person_name"))
CREATE INDEX "job_person_employed_id" ON "job" ("person_employed_id")
CREATE TABLE "personnumkey" ("id" INTEGER NOT NULL PRIMARY KEY, "person_name" VARCHAR(30) NOT NULL, "lives_in_town" VARCHAR(40) NOT NULL, "nickname" VARCHAR(20))

sqlite > .mode column
sqlite > .width 15 15 15 15 15
sqlite > .headers on

sqlite > select * from person
person_name      lives_in_town    nickname
--------------- --------------- ---------------
Andrew           Sumner           Andy
Peter            Seattle          Painter
Susan            Boston           Beannie
Pam              Coventry         PJ
Steven           Colchester


sqlite > select * from job
job_name         start_date       end_date         salary           person_employed
--------------- --------------- --------------- --------------- ---------------
Analyst          2001-09-22       2003-01-30       65500            Andrew
Senior analyst   2003-02-01       2006-10-22       70000            Andrew
Senior business  2006-10-23       2016-12-24       80000            Andrew
Admin superviso  2012-10-01       2014-11, 10       45900            Peter
Admin manager    2014-11-14       2018-01, 05       45900            Peter

