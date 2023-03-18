#!/usr/bin/env python
# coding: utf-8

# In[8]:


n = int(input('enter the radius:'))
area =  3.14 * n * n
print(area)


# In[13]:


n1 = int(input('enter the number:'))
for i in range(1,6):
    print(n1,'*',i,' =',n1*i)


# In[20]:


usr = input('enter the user name :')
pwd = input('enter the password:')
if (pwd.find(usr) == -1):
        print("Valid")
else:
        print("Invalid")


# In[26]:


n = int(input('enter the number: '))

def digit(n):
    if n < 10:
          return 1
    else:
          return 1 + digit(n/10)

print(digit(n))


# In[31]:


import pandas as pd
# initialize list of lists
data = [[10, 'Sujeet'], [11,'Sameer'], [12,'Sumit']]
 
# Create the pandas DataFrame
df = pd.DataFrame(data, columns = ['age', 'name'])
 
# print dataframe.
print(df[['name','age']].to_string(index=False))


# In[32]:


def fact(i):
    i=i+10
    return i



def fact2(i):
    i= i-10
    
    return i


def fun(f1, f2, x):
    y  =0
    z=0
    if x<1:
       y =  f1(x)
        
    else:
      z =  f2(x)
      
    print('z=', z, 'x=', x)
    print('y=', y, 'x=', x)
     
fun(fact, fact2, 6)
fun(fact, fact2, -1)

