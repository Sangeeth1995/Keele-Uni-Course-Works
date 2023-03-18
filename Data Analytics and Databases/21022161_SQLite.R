#TASK-1
#Loading the DBI and RSQL Library
library(DBI)
library(RSQLite)

#Creating column vector for inserting column headers
col_name_vector = c("AAGE","ACLSWKR","ADTIND","ADTOCC","AHGA","AHRSPAY","AHSCOL","AMARITL",
                    "AMJIND","AMJOCC","ARACE","AREORGN","ASEX","AUNMEM","AUNTYPE","AWKSTAT",
                    "CAPGAIN","CAPLOSS","DIVVAL","FILESTAT","GRINREG","GRINST","HDFMX",
                    "HHDREL","MARSUPWT","MIGMTR1","MIGMTR3","MIGMTR4","MIGSAME","MIGSUN",
                    "NOEMP","PARENT","PEFNTVTY","PEMNTVTY","PENATVTY","PRCITSHP",
                    "SEOTR","VETQVA","VETYN","WKSWORK","YEAR","TRGT")

#Creating data frame from CSV and inserting appropriate column headers
library(readr)
census_income <- read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/census-income-mld/census-income.data.gz", 
                          col_names = col_name_vector)

#Creating db
db <- dbConnect(RSQLite::SQLite(), "census_income.db")

#Drop Table Income,if exists 
dbSendQuery(conn = db,"DROP TABLE IF EXISTS Income")

#Creating Table named Income
dbSendQuery(conn = db,"CREATE TABLE Income 
            (
            AAGE INT,
            ACLSWKR  TEXT,
            ADTIND  TEXT,
            ADTOCC  TEXT,
            AHGA  TEXT,
            AHRSPAY  NUM,
            AHSCOL  TEXT,
            AMARITL  TEXT,
            AMJIND  TEXT,
            AMJOCC  TEXT,
            ARACE  TEXT,
            AREORGN  TEXT,
            ASEX  TEXT,
            AUNMEM  TEXT,
            AUNTYPE  TEXT,
            AWKSTAT  TEXT,
            CAPGAIN  NUM,
            CAPLOSS  NUM,
            DIVVAL  NUM,
            FILESTAT  TEXT,
            GRINREG  TEXT,
            GRINST  TEXT,
            HDFMX  TEXT,
            HHDREL  TEXT,
            MARSUPWT  NUM,
            MIGMTR1  TEXT,
            MIGMTR3  TEXT,
            MIGMTR4  TEXT,
            MIGSAME  TEXT,
            MIGSUN  TEXT,
            NOEMP  NUM,
            PARENT  TEXT,
            PEFNTVTY  TEXT,
            PEMNTVTY  TEXT,
            PENATVTY  TEXT,
            PRCITSHP  TEXT,
            SEOTR  TEXT,
            VETQVA  TEXT,
            VETYN  TEXT,
            WKSWORK  NUM,
            YEAR  TEXT,
            TRGT  TEXT)")

#Importing dataframe into the Db
dbWriteTable(conn = db, name = "Income", value = census_income, 
             row.names = FALSE, append = TRUE)

# df1 <- dbReadTable(db,"Income") - Returns the table data to the data frame

#TASK-2
#Changing table name of Income to Old_table
dbSendQuery(conn = db,"ALTER TABLE Income RENAME TO Old_table")

#Inserting Primary Key SS_ID with Autoincrement feature with newly created Income Table
dbSendQuery(conn = db,"CREATE TABLE Income 
           (
           SS_ID INTEGER PRIMARY KEY AUTOINCREMENT,
           AAGE INT,
           ACLSWKR  TEXT,
           ADTIND  TEXT,
           ADTOCC  TEXT,
           AHGA  TEXT,
           AHRSPAY  NUM,
           AHSCOL  TEXT,
           AMARITL  TEXT,
           AMJIND  TEXT,
           AMJOCC  TEXT,
           ARACE  TEXT,
           AREORGN  TEXT,
           ASEX  TEXT,
           AUNMEM  TEXT,
           AUNTYPE  TEXT,
           AWKSTAT  TEXT,
           CAPGAIN  NUM,
           CAPLOSS  NUM,
           DIVVAL  NUM,
           FILESTAT  TEXT,
           GRINREG  TEXT,
           GRINST  TEXT,
           HDFMX  TEXT,
           HHDREL  TEXT,
           MARSUPWT  NUM,
           MIGMTR1  TEXT,
           MIGMTR3  TEXT,
           MIGMTR4  TEXT,
           MIGSAME  TEXT,
           MIGSUN  TEXT,
           NOEMP  NUM,
           PARENT  TEXT,
           PEFNTVTY  TEXT,
           PEMNTVTY  TEXT,
           PENATVTY  TEXT,
           PRCITSHP  TEXT,
           SEOTR  TEXT,
           VETQVA  TEXT,
           VETYN  TEXT,
           WKSWORK  NUM,
           YEAR  TEXT,
           TRGT  TEXT)")


#Inserting table data to the Income from the Old_table
dbSendQuery(conn = db,"INSERT INTO Income 
           (
           AAGE,
           ACLSWKR,
           ADTIND,
           ADTOCC,
           AHGA,
           AHRSPAY,
           AHSCOL,
           AMARITL,
           AMJIND,
           AMJOCC,
           ARACE,
           AREORGN,
           ASEX,
           AUNMEM,
           AUNTYPE,
           AWKSTAT,
           CAPGAIN,
           CAPLOSS,
           DIVVAL,
           FILESTAT,
           GRINREG,
           GRINST,
           HDFMX,
           HHDREL,
           MARSUPWT,
           MIGMTR1,
           MIGMTR3,
           MIGMTR4,
           MIGSAME,
           MIGSUN,
           NOEMP,
           PARENT,
           PEFNTVTY,
           PEMNTVTY,
           PENATVTY,
           PRCITSHP,
           SEOTR,
           VETQVA,
           VETYN,
           WKSWORK,
           YEAR,
           TRGT    
           )
           SELECT
           AAGE,
           ACLSWKR,
           ADTIND,
           ADTOCC,
           AHGA,
           AHRSPAY,
           AHSCOL,
           AMARITL,
           AMJIND,
           AMJOCC,
           ARACE,
           AREORGN,
           ASEX,
           AUNMEM,
           AUNTYPE,
           AWKSTAT,
           CAPGAIN,
           CAPLOSS,
           DIVVAL,
           FILESTAT,
           GRINREG,
           GRINST,
           HDFMX,
           HHDREL,
           MARSUPWT,
           MIGMTR1,
           MIGMTR3,
           MIGMTR4,
           MIGSAME,
           MIGSUN,
           NOEMP,
           PARENT,
           PEFNTVTY,
           PEMNTVTY,
           PENATVTY,
           PRCITSHP,
           SEOTR,
           VETQVA,
           VETYN,
           WKSWORK,
           YEAR,
           TRGT            
           FROM Old_table")

# df2 <- dbReadTable(db,"Income") - Returns the table data to the data frame
# dbGetQuery(db,"PRAGMA table_info(Income)") - Returns Table structure/description

#Deleting the Old_table
dbSendQuery(conn = db,"DROP TABLE Old_table")

#TASK-3
#To check the total number of males and females for each 
#race group reported in the data
query1 <- dbGetQuery(db,"SELECT ARACE AS RACE ,ASEX AS SEX ,COUNT(ARACE) AS COUNT 
                     FROM Income 
                     GROUP BY ARACE , ASEX")

#TASK-4
#To calculate the average annual income of the 
#reported individuals for eachrace groups
query2 <- dbGetQuery(db,"SELECT ARACE AS RACE, AVG(WKSWORK*(AHRSPAY * 40)) AS AvgAnualIncm 
                     FROM Income WHERE AHRSPAY > 0
                     GROUP BY ARACE")

#TASK-5
# Create 3 tables named: Person, Job and Pay, by extracting the particular fields
# respectively from the Income table

#Drop Table Person,if exists 
dbSendQuery(conn = db,"DROP TABLE IF EXISTS Person")

#Creating Table Person 
dbSendQuery(conn = db,"CREATE TABLE Person
           (
           Id INTEGER PRIMARY KEY AUTOINCREMENT,
           Age INT,
           education TEXT,
           sex TEXT,
           citizenship TEXT,
           family_members_under_18 TEXT,
           previous_state TEXT,
           previous_region TEXT,
           Hispanic_origin TEXT,
           employment_stat TEXT)")

#Inserting particular attribute data to Peroson from the Income table
dbSendQuery(conn = db,"INSERT INTO Person 
           (
           Age,
           education,
           sex,
           citizenship,
           family_members_under_18,
           previous_state,
           previous_region,
           Hispanic_origin,
           employment_stat
           )
           SELECT 
           AAGE,
           AHGA,
           ASEX,
           PRCITSHP,
           PARENT,
           GRINST,
           GRINREG,
           AREORGN,
           AWKSTAT 
           FROM Income")

# df3 <- dbReadTable(db,"Person") - Returns the table data to the data frame
# dbGetQuery(db,"PRAGMA table_info(Person)") - Returns Table structure/description


#Drop Table Job,if exists 
dbSendQuery(conn = db,"DROP TABLE IF EXISTS Job")

#Creating Table Job 
dbSendQuery(conn = db,"CREATE TABLE Job
           (
           occjd INTEGER PRIMARY KEY AUTOINCREMENT,
           Detailed_Industry_code TEXT,
           detailed_occupation_code TEXT,
           major_industry_code TEXT,
           major_occupation_code TEXT)")

#Inserting particular attribute data to Job from the Income table
dbSendQuery(conn = db,"INSERT INTO Job 
           (
           Detailed_Industry_code,
           detailed_occupation_code,
           major_industry_code,
           major_occupation_code
           ) 
           SELECT 
           ADTIND,
           ADTOCC,
           AMJOCC,
           AMJIND 
           FROM Income")

# df4 <- dbReadTable(db,"Job") - Returns the table data to the data frame
# dbGetQuery(db,"PRAGMA table_info(Job)") - Returns Table structure/description


#Drop Table Pay,if exists 
dbSendQuery(conn = db,"DROP TABLE IF EXISTS Pay")

#Creating Table Pay 
dbSendQuery(conn = db,"CREATE TABLE Pay
           (
           job_id INTEGER PRIMARY KEY AUTOINCREMENT,
           Wage_per_hour NUM,
           weeks_worked_per_year NUM)")

#Inserting particular attribute data to Pay from the Income table
dbSendQuery(conn = db,"INSERT INTO Pay 
           (
           Wage_per_hour,
           weeks_worked_per_year
           )
           SELECT 
           AHRSPAY,
           WKSWORK 
           FROM Income")

# df5 <- dbReadTable(db,"Pay") - Returns the table data to the data frame
# dbGetQuery(db,"PRAGMA table_info(Pay)") - Returns Table structure/description
            
#TASK-6
# i. Given the data in your tables, create an SQL statement to select the highest hourly wage, the
# number of people residing in each state (GRINST) employed in this job, the state, the job
# type and major industry.

query3 <- dbGetQuery(db,"SELECT Pay.Wage_per_hour,COUNT(Person.previous_state) AS State_Count,Person.previous_state,
                    job.major_occupation_code, job.major_industry_code 
                    FROM Person INNER JOIN Job ON Person.Id = job.occjd INNER JOIN Pay ON Person.Id = Pay.job_id 
                    WHERE Pay.Wage_per_hour = (SELECT MAX(Wage_per_hour) FROM Pay) ")

# ii. Write an SQL query to determine the employment of people of Hispanic origin with BSc
# (Bachelors degree), MSc (Masters degree), and PhD (Doctorate degree) showing the type of
# industry they are employed in, their average hourly wage and average number of weeks
# worked per year for each industry.

query4 <- dbGetQuery(db,"SELECT job.major_occupation_code AS Industries, AVG(Pay.Wage_per_hour) AS AvgWage_per_hour, 
                    AVG(Pay.weeks_worked_per_year) AS AvgWeeks_worked_per_year 
                    FROM Person INNER JOIN Job ON Person.Id = job.occjd INNER JOIN Pay ON Person.Id = Pay.job_id 
                    WHERE 
                    (
                    Person.education='Doctorate degree(PhD EdD)' OR 
                    Person.education='Bachelors degree(BA AB BS)' OR 
                    Person.education='Masters degree(MA MS MEng MEd MSW MBA)' 
                    ) 
                    AND 
                    (
                    Hispanic_origin NOT IN ('All other', 'Do not know', 'NA')
                    ) 
                    GROUP BY job.major_occupation_code")









            
            
            