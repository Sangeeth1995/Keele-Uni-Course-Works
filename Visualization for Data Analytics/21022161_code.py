#!/usr/bin/env python
# coding: utf-8

#Importing Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#Loading Dataset
ds_data = pd.read_csv('/Users/macbook/Downloads/Course work/Visualisation/DataScientist.csv',index_col=0)
ds_data.head()


#Removing unnecessary attributes in the Dataframe
del ds_data["index"]
ds_data.head()

#To display the information of dataframe 
ds_data.info()

#Checked every column for detecting the missing values
#Example
#ds_data.loc[ds_data['Job Title '] == "-1"]
#ds_data.loc[ds_data['Rating'] == -1]
#ds_data.loc[ds_data['Industry'] == "Unknown"]

#Got the count of missing value attributes 

#409 Rating entries are -1 
#240 Headquarters entries are -1
#229 Size entries are -1 and Size entries 77 are Unknown
#977 Founded entries are -1 
#229 Type of ownership entries are -1 and 38 Type of ownership entries are Unknown
#546 Industry entries are -1 
#546 Sector entries are -1 
#229 Revenue entries are -1 
#2760 Competitors entries are -1 
#3745 Easy Apply entries are -1 

#Dropping attributes : Founded,Competitors and Easy Apply since it has more missing values
ds_data.drop(['Founded','Competitors','Easy Apply'],axis=1,inplace=True)
#Dropping attributes : Job Description,Revenue since these data doesn't provide insights for further analysis
ds_data.drop(['Job Description','Revenue','Sector'],axis=1,inplace=True)


#Replacing  missing values values with NAN.
#NaN stands for Not A Number and is one of the common ways to represent the missing value in the data
ds_data['Rating']= ds_data['Rating'].replace([-1],np.nan)
ds_data['Headquarters']= ds_data['Headquarters'].replace(['-1'],np.nan)
ds_data['Size']= ds_data['Size'].replace(['-1'],np.nan)
ds_data['Size']= ds_data['Size'].replace(['Unknown'],np.nan)
ds_data['Type of ownership']= ds_data['Type of ownership'].replace(['-1'],np.nan)
ds_data['Type of ownership']= ds_data['Type of ownership'].replace(['Unknown'],np.nan)
ds_data['Industry']= ds_data['Industry'].replace(['-1'],np.nan)


#Dropping Nan values records
ds_data=ds_data.dropna(how='any',axis=0)
ds_data=ds_data.reset_index(drop=True)


#Displaying Job Title before preprocessing
ds_data['Job Title'].value_counts()
#Job Title - Eliminating ',','/','-' terms from it 
ds_data['Job Title']= ds_data['Job Title'].apply(lambda x:x.join(x.split(',')[:1]))
ds_data['Job Title']= ds_data['Job Title'].apply(lambda x:x.join(x.split('/')[:1]))
ds_data['Job Title']= ds_data['Job Title'].apply(lambda x:x.join(x.split('-')[:1]))
ds_data['Job Title']= ds_data['Job Title'].apply(lambda x:x.replace('Data Scientist ','Data Scientist'))
#Displaying Job Title after preprocessing
ds_data['Job Title'].value_counts()


#Displaying Salary Estimate before preprocessing
ds_data['Salary Estimate']
#Eliminating the salary source string from the salary estimate
ds_data['Salary Estimate']=ds_data['Salary Estimate'].apply(lambda x:x.split()[0])
ds_data['Salary Estimate']=ds_data['Salary Estimate'].apply(lambda x:x.split('(Employer')[0])
ds_data['Salary Estimate']
#Breaking Salary Estimate to lower and upperbound for further analysis
ds_data['Salary Estimate_lower_bound'] = ds_data['Salary Estimate'].apply(lambda x:x.split("-")[0])
ds_data['Salary Estimate_upper_bound'] = ds_data['Salary Estimate'].apply(lambda x:x.split("-")[1])
#Filering only the numerical values
ds_data['Salary Estimate_lower_bound']=ds_data['Salary Estimate_lower_bound'].apply(lambda x:x.replace('$',''))
ds_data['Salary Estimate_lower_bound']=ds_data['Salary Estimate_lower_bound'].apply(lambda x:x.replace('K',''))
ds_data['Salary Estimate_lower_bound']
#Filering only the numerical values
ds_data['Salary Estimate_upper_bound']=ds_data['Salary Estimate_upper_bound'].apply(lambda x:x.replace('$',''))
ds_data['Salary Estimate_upper_bound']=ds_data['Salary Estimate_upper_bound'].apply(lambda x:x.replace('K',''))
ds_data['Salary Estimate_upper_bound']



#Displaying Company Name before preprocessing
ds_data['Company Name']
#Now we can split the "\n & rating" from company Name
ds_data['Company Name'] = ds_data['Company Name'].apply(lambda x:x.split('\n')[0])
ds_data['Company Name']


#Displaying Location before preprocessing
ds_data['Location']
#Filtering Location, eliminating the abbrevation terms
ds_data['Location']=ds_data['Location'].apply(lambda x:x.join(x.split(',')[:1]))
ds_data['Location']


#Displaying Headquarters before preprocessing
ds_data['Headquarters']
#Filtering Headquarters, eliminating the abbrevation terms
ds_data['Headquarters']= ds_data['Headquarters'].astype(str)
ds_data['Headquarters'] = ds_data['Headquarters'].apply(lambda x:x.join(x.split(',')[:1]))
ds_data['Headquarters']


#Displaying Size before preprocessing
ds_data['Size']
#Eliminating the string 'employess' from the Size attribute
ds_data['Size']= ds_data['Size'].astype(str)
ds_data['Size']=ds_data['Size'].apply(lambda x:x.split('employees')[0])
ds_data['Size']
#Breaking Size to minimum and maximum for further analysis
ds_data['Size_Minimum']=ds_data['Size'].apply(lambda x:x.split()[0])
ds_data['Size_Maximum']=ds_data['Size'].apply(lambda x:x.split()[-1])
#Eliminating the + symbol in the 10000+ value
ds_data['Size_Minimum']=ds_data['Size_Minimum'].apply(lambda x:x.split('+')[0])
ds_data['Size_Maximum']=ds_data['Size_Maximum'].apply(lambda x:x.split('+')[0])
ds_data['Size_Minimum']
ds_data['Size_Maximum']


#Displaying Type of ownership before preprocessing
ds_data['Type of ownership'].value_counts()
#Formatting the Type of ownership
ds_data['Type of ownership'] = ds_data['Type of ownership'].astype(str)
ds_data['Type of ownership']=ds_data['Type of ownership'].apply(lambda x:x.split('/')[0])
ds_data['Type of ownership']=ds_data['Type of ownership'].apply(lambda x:x.split(' - ')[-1])
ds_data['Type of ownership']=ds_data['Type of ownership'].apply(lambda x:x.split('or')[-1])
ds_data['Type of ownership']=ds_data['Type of ownership'].apply(lambda x:x.split()[0])
#Displaying Type of ownership after preprocessing
ds_data['Type of ownership'].value_counts()


#Preprocessed Dataframe
ds_data.head()


#Converting the Preprocessed Dataframe to csv file
ds_data.to_csv('PREPROCESSED_DATA.csv')


#Visualizing the Data

#Top 10 Companies with Highest number of job vaccanicies for data scientist roles
#Creatind dataframe to count the unique Company Name entries and sorted it int descending order
df1 = ds_data["Company Name"].value_counts().head(10)
#Plotting the bar graph
#Set the width and height of the figure
plt.figure(figsize=(10,6))
# Add title
plt.title("Top 10 Companies with Highest number of job vaccanicies for data scientist roles ",fontsize=16)
plt.xticks(rotation=90)
# Bar chart 
sns.set_style('darkgrid')
sns.barplot(x=df1.index, y=df1[:],color='#42b7bd')
plt.ylabel('Count')
plt.xlabel('Company Names')
plt.show()


#Most Popular Data Science Job Titles
#Creatind dataframe to count the unique Job titles entries and sorted it int descending order
df2 = ds_data["Job Title"].value_counts().sort_values(ascending=False).head(10)
#Plotting the bar graph
#Set the width and height of the figure
plt.figure(figsize=(10,6))
# Add title
plt.title("Most Popular Data Science Job Titles",fontsize=16)
plt.xticks(rotation=90)
# Bar chart 
sns.set_style('darkgrid')
sns.barplot(x=df2.index, y=df2[:])
plt.ylabel('Count')
plt.xlabel('Job Titles')
plt.show()


#Top 10 locations for Data Science Job
#Creatind dataframe to count the unique Job Locations entries and sorted it int descending order
df3 = ds_data["Location"].value_counts().head(10)
# Plotting the bar graph
# Set the width and height of the figure
plt.figure(figsize=(10,6))
# Add title
plt.title("Top 10 locations for Data Science Job",fontsize=16)
# Bar chart 
sns.barplot(x=df3[:], y=  df3.index,palette = 'hls')
plt.xlabel('Count')
plt.ylabel('Location')
plt.show()


#Word cloud for Most available Job Title
#importing WordCloud & STOPWORDS libraries
from wordcloud import WordCloud
from wordcloud import STOPWORDS
stopwords = set(STOPWORDS)
text = ds_data['Job Title'].values 
wordcloud = WordCloud(background_color ="black").generate(str(text))
#Plotting wordcloud
plt.imshow(wordcloud)
plt.title("Most available Job Titles",fontsize=16)
plt.axis("off")
plt.show()


#Word cloud for Most available Job Locations
#importing WordCloud & STOPWORDS libraries
from wordcloud import WordCloud
from wordcloud import STOPWORDS
stopwords = set(STOPWORDS)
text = ds_data['Location'].values 
wordcloud = WordCloud(background_color ="black").generate(str(text))
#Plotting wordcloud
plt.imshow(wordcloud)
plt.title("Most available Job locations",fontsize=16)
plt.axis("off")
plt.show()


#Word cloud for Most available Company Names
#importing WordCloud & STOPWORDS libraries
from wordcloud import WordCloud
from wordcloud import STOPWORDS
stopwords = set(STOPWORDS)
text = ds_data['Company Name'].values 
wordcloud = WordCloud(background_color ="black").generate(str(text))
#Plotting wordcloud
plt.imshow(wordcloud)
plt.title("Most available Company Names",fontsize=16)
plt.axis("off")
plt.show()


#Top 5 Head Quarters of Job Holder Company 
#Creatind dataframe to count the unique Job Headquarters entries and sorted it int descending order
df4 = ds_data["Headquarters"].value_counts().head()
# Plotting the dataframe into piechart
# define Seaborn color palette to use
colors = sns.color_palette('pastel')[0:5]
plt.pie(df4, labels=df4.index, autopct='%.0f%%', colors = colors)
plt.title('Top 5 Head Quarters of Job Holder Companies',fontsize=16)
plt.axis('equal')
plt.rcParams["figure.figsize"] = (8,8)
plt.show()


#Top 5 industries for datascience 
#Creatind dataframe to count the unique Industry entries and sorted it int descending order
df5 = ds_data["Industry"].value_counts().sort_values(ascending=False).head(5)
# Plotting the dataframe into piechart
#define Seaborn color palette to use
colors = sns.color_palette('pastel')[0:5]
plt.pie(df5,  autopct='%.0f%%', colors = colors)
plt.title('Top 5 industries',fontsize=16)
plt.axis('equal')
plt.rcParams["figure.figsize"] = (5,5)
labels = df5.index
plt.legend( labels, loc="best")
plt.axis('equal')
plt.tight_layout()
plt.show()


#Histogram for plotting the salary distribution of datasceintist job vaccancies
sns.distplot(a=ds_data['Salary Estimate_upper_bound'], kde=False)
# plt.figure(figsize=(10,20))
# Increase size of plot in jupyter
sns.set_style('darkgrid')
plt.rcParams["figure.figsize"] = (10,5)
plt.title('Salary Estimate disribution for data scientist roles',fontsize=16)
plt.xlabel('Salary')
plt.ylabel('Count')
plt.show()


#Companies having higest salary
ds_data['Salary Estimate_upper_bound']= ds_data['Salary Estimate_upper_bound'].astype(int)
#Creating dataframe to filer the records having salary greater than 250K
df6 = ds_data.loc[(ds_data['Salary Estimate_upper_bound'] >= 250)]
#Creatind dataframe from the above filtered df,
#to count the unique Company name entries and sorted it int descending order
df7 = df6["Company Name"].value_counts().head()
# Plotting the dataframe into linechart
sns.barplot(x=df7.index, y=df7[:],color="red")
plt.title('Companies having higest salary',fontsize=16)
plt.xlabel('Company names')
plt.ylabel('Count')
plt.rcParams["figure.figsize"] = (10,5)
plt.show()


#Histogram for plotting the company size distribution of datasceintist job vaccancies
sns.distplot(a=ds_data['Size_Maximum'], kde=False,color='green')
# plt.figure(figsize=(10,20))
# Increase size of plot in jupyter
plt.rcParams["figure.figsize"] = (5,6)
plt.title('Company Employee Max size disribution for data scientist roles',fontsize=16)
plt.xlabel('Employees Size')
plt.ylabel('Count')
plt.show()


#Top 5 Company's with Highest Number of Employees,
#whereall of these Company's has employees higher than 10000
#Creating dataframe to filer the records having employee size maximum ie;10000 
df8 = ds_data.loc[(ds_data['Size_Maximum'] == ds_data["Size_Maximum"].max())]
#Creatind dataframe from the above filtered df,
#to count the unique Company name entries and sorted it int descending order
df9 = df8["Company Name"].value_counts().sort_values(ascending=False).head()
# Plotting the dataframe into linechart
sns.barplot(x=df9.index, y=df9[:],color="indigo")
plt.title('Companies having higest employee size',fontsize=16)
plt.xlabel('Company names')
plt.ylabel('Count')
plt.rcParams["figure.figsize"] = (10,6)
plt.show()


#Types of Ownership
#Creatind dataframe to count the unique Type of ownership entries.
df10 = ds_data["Type of ownership"].value_counts().sort_index()
# Plotting the bar graph
# Set the width and height of the figure
plt.figure(figsize=(10,6))
# Bar chart 
sns.set_style('darkgrid')
sns.barplot(x=df10.index, y=df10[:],color='blue')
# Add title
plt.title("Type of ownership",fontsize=16)
plt.xticks(rotation=90)
plt.ylabel('Count')
plt.xlabel('Type of ownership')
plt.show()


#Top five companies having maximum rating
#Creating dataframe to filer the records having maximum rating ie;5.0
df12 = ds_data.loc[(ds_data['Rating'] == ds_data["Rating"].max())]
#Creatind dataframe from the above filtered df,
#to count the unique Company name entries and sorted it int descending order
df13 = df12["Company Name"].value_counts().head(5)
# Set the width and height of the figure
plt.figure(figsize=(14,6))
# Add title
plt.title("Top five companies having maximum rating",fontsize=16)
# Plotting the bar graph
sns.barplot(x=df13.index, y=df13[:],color="Orange")
plt.ylabel('Count')
plt.xlabel('Company Name')
plt.show()


#Companies having rating less than 2
#Creating dataframe to filer the records having rating less than 2.0
df14 = ds_data.loc[(ds_data['Rating'] <= 2.0)]
#Creatind dataframe from the above filtered df,
#to count the unique Company name entries and sorted it int descending order
df15 = df14["Company Name"].value_counts()
# Plotting the bar graph
# Set the width and height of the figure
plt.figure(figsize=(14,6))
# Add title
plt.title("Companies having rating less than 2 ",fontsize=16)
sns.barplot(x=df15.index, y=df15[:],color="violet")
plt.ylabel('Count')
plt.xlabel('Company Name')
plt.xticks(rotation=90)
plt.show()


