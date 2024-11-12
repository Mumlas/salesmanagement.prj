
# ---------------- Data Gerating ----------------------- #
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from setup.models import Staff, Branch
from datetime import date, timedelta
import pandas as pd
import numpy as np
import random
import os

os.system('pwd')
os.system('clear')


title_list = ['Alh.', 'Haj.', 'Mal', 'Mr', 'Mrs', 'Miss']
weight = [0.10,0.02,0.66,0.20,0.0,0.02]
title = random.choices(title_list, weights=weight,k=100)

fnames = [
'ALiyu', 'Hadiza', 'Mustapha', 'Dauda', 'Iliya', 'Garba','Salihu','Zainab', 'Aisha',
'Jamila','Zakari','Muhammad','David','Musa', 'Solomon','Uche','Isa','Yahya','Usman','Omar'
]
print('\nbuilding list of firstnames.....')
first_name = []
for i in range(0,100):
	name = random.choice(fnames)
	first_name.append(name)

snames = [
'Sale','Hamman','Zakari','Nuhu','Yau', 'Awwal','Rabiu','Kabiru','Nuhu','Usman',
'Imam','Wada','Turaki','Dauda','Bappayo','Madaki','Jega','Habu','Ardo','Lawal'
]
print('\nbuilding list of firstnames.....')
surname = []
for i in range(0,100):
	name = random.choice(snames)
	surname.append(name)


rank_list = [
'md_ceo','manager','cashier_accountant','supervisor','driver','security','pump_attendant'
]
print('\nbuilding list of designation.....')
weight = [0.01,0.05,0.05,0.05,0.07,0.05,0.72]
ranks = random.choices(rank_list, weights=weight, k=100)


# Sex
print('\nbuilding list of sex.....')
sex_list = ['Male','Female']
weight = [0.8, 0.2]
sex = random.choices(sex_list, weights = weight, k=100)


# Generating date - date of birth 
lower = "1/10/2006"
upper = '1/10/1974'

start , stop =  date(1974,10,1), date(2006,10,1)
number = 100
dates = [start]
print('\ngenerating pool of dates.....')
while start < stop:
	start += timedelta(days=20)
	dates.append(start)

dateofbirth = random.choices(dates, k=number)

# age
ages = []
for i in range(0,100):
	age = random.randint(18,50)
	ages.append(age)


# Branch
branch_list = [1, 2, 3, 4, 5]
print('\nbuilding list of branches.....')
branch=[]
for i in range(0,100):
	temp = random.choice(branch_list)
	branch.append(temp)

# generate email using first letter of surname, dot, and firstname
email = ""

# phone number
phone_numbers= []
print('\nbuilding phone numbers.....')
for i in range(0,100):
	number=random.randint(8022030124,8035290011)
	number = '0'+str(number)
	phone_numbers.append(number)

print('\nbuilding dictionary of staff records.....')
staff_dict = {
	'title':title,
	'firstname':first_name,
	'surname':surname,
	'sex':sex,
	'dateofbirth':dateofbirth,
	'employmentdate':None,
	'designation':ranks,
	'branch':branch,
	'email':None,
	'phonenumber':phone_numbers
}

print('\nbuilding dataframe of staff records.....')
staff_df = pd.DataFrame(staff_dict)

print('\ncreating emails address.....')
staff_df["email"] = staff_df['surname'].str.lower()+"."+staff_df['firstname'].str.lower()+"@gmail.com"

print('\ncreating functions to generate date of employment.....')
def age(dob):	
	now = date.today()
	# if not is_datetime(dob): this did not work
	#if not np.issubdtype(dob.dtype, np.datetime64):
	#	dob = datetime.strtime(dob,"%Y-%m-%d").date()
	return (now.year - dob.year) - ((now.month, now.day) < (dob.month, dob.day))

print('\ncreating date of employment.....')
staff_df['age'] = staff_df['dateofbirth'].apply(age)
staff_df['days'] = 18*365

staff_df['employmentdate'] = staff_df['dateofbirth'] +staff_df['days'].map(timedelta)
staff_df['seniority'] = staff_df['employmentdate'].apply(age)

print(staff_df)
print('\nRearranging columns.....')
staff_df = staff_df[['title','firstname','surname','sex','dateofbirth','employmentdate','designation','branch','email','phonenumber','seniority','age','days']]
print('\nWriting to csv.....')
staff_df.to_csv('staff_records')

print('\nupload the dataset into staff model in django...')

for index, row in staff_df.iterrows():
	staff, created = Staff.objects.get_or_create(
		title = row['title'],
		firstname = row['firstname'],
		surname = row['surname'],
		dateofbirth = row['dateofbirth'],
		sex= row['sex'],
		employmentdate = row['employmentdate'],
		designation = row['designation'],
		branch = Branch.objects.get(id = row['branch']),
		email = row['email'],
		phonenumber = row['phonenumber'],
		)

	staff.save()
print('\nData has been loaded into the database')