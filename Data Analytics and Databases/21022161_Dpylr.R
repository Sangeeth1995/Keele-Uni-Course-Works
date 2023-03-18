#TASK-1
#Loading the dbplyr,DBI and dplyr Library
install.packages("dbplyr")
library(dbplyr)
library(DBI)
library(dplyr)

#Creating column vector for inserting column headers
col_name_vector = c("AAGE","ACLSWKR","ADTIND","ADTOCC","AHGA","AHRSPAY","AHSCOL","AMARITL",
                    "AMJIND","AMJOCC","ARACE","AREORGN","ASEX","AUNMEM","AUNTYPE","AWKSTAT",
                    "CAPGAIN","CAPLOSS","DIVVAL","FILESTAT","GRINREG","GRINST","HDFMX",
                    "HHDREL","MARSUPWT","MIGMTR1","MIGMTR3","MIGMTR4","MIGSAME","MIGSUN",
                    "NOEMP","PARENT","PEFNTVTY","PEMNTVTY","PENATVTY","PRCITSHP",
                    "SEOTR","VETQVA","VETYN","WKSWORK","YEAR","TRGT")


#Creating data frame Income from CSV and inserting appropriate column headers
library(readr)
Income <- read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/census-income-mld/census-income.data.gz", 
                          col_names = col_name_vector)

#TASK-2
#Inserting Primary Key SS_ID with Autoincrement feature
Income <- Income %>% 
          mutate(SS_ID = row_number(), .before = "AAGE")

#TASK-3
#To check the total number of males and females for each
#race group reported in the data
query1 <-  Income %>%  
           group_by(ARACE,ASEX) %>%  
           summarise(Count = n()) %>%  
           rename(Race=ARACE,Sex=ASEX)


#TASK-4
#To calculate the average annual income of the
#reported individuals for each race groups
query2 <- Income %>%
          filter(AHRSPAY > 0) %>%
          group_by(ARACE) %>%
          summarize(
            AvgAnnualIncome = mean(WKSWORK*(AHRSPAY * 40))
            )

#TASK-5
# Create 3 tables named: Person, Job and Pay, by extracting the particular fields
# respectively from the Income table

#Creating dataframe Person 
Person <- Income %>% 
          select(Id=SS_ID,Age=AAGE,education=AHGA,sex=ASEX,citizenship=PRCITSHP,
                 family_members_under_18=PARENT,previous_state=GRINST,
                 previous_region=GRINREG,Hispanic_origin=AREORGN,employment_stat=AWKSTAT)

#Creating dataframe Job 
Job <- Income %>% 
       select(occjd=SS_ID,Detailed_Industry_code=ADTIND,detailed_occupation_code=ADTOCC,
              major_industry_code=AMJOCC,major_occupation_code=AMJIND)

#Creating dataframe Pay 
Pay <- Income %>% select(job_id=SS_ID,Wage_per_hour=AHRSPAY,weeks_worked_per_year=WKSWORK)

                           
#TASK-6

# i. Given the data in your tables, create an SQL statement to select the highest hourly wage, the
# number of people residing in each state (GRINST) employed in this job, the state, the job
# type and major industry.

query3 <- Person %>% 
          inner_join(Job, by = c("Id" = "occjd")) %>%
          inner_join(Pay, by = c("Id" = "job_id")) %>%
          filter(Wage_per_hour == max(Wage_per_hour)) %>%
          group_by(previous_state) %>%
          summarise(
            Wage_per_hour,
            stateCount = n(),
            previous_state,
            major_occupation_code,
            major_industry_code
            ) 


# ii. Write an SQL query to determine the employment of people of Hispanic origin with BSc
# (Bachelors degree), MSc (Masters degree), and PhD (Doctorate degree) showing the type of
# industry they are employed in, their average hourly wage and average number of weeks
# worked per year for each industry.


query4 <- Person %>% 
          inner_join(Job, by = c("Id" = "occjd")) %>%
          inner_join(Pay, by = c("Id" = "job_id")) %>%
          filter(education == 'Doctorate degree(PhD EdD)' | 
           education == 'Bachelors degree(BA AB BS)' | 
           education == 'Masters degree(MA MS MEng MEd MSW MBA)',
           Hispanic_origin != "All other",
           Hispanic_origin != "Do not know",
           Hispanic_origin != "NA") %>%
          select(Hispanic_origin, education,major_occupation_code,Wage_per_hour, weeks_worked_per_year) %>%
          group_by(major_occupation_code) %>%
          summarise(AvgWage_per_hour = mean(Wage_per_hour),
            AvgWeeks_worked_per_year = mean(weeks_worked_per_year))%>%
          rename(Industries = major_occupation_code)









