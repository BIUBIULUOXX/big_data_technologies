# given code 
from pyspark import SparkContext
from operator import add

sc = SparkContext('local', 'pyspark')

def age_group(age):
  if age < 10 :
    return '0-10'
  elif age < 20:
    return '10-20'
  elif age < 30:
    return '20-30'
  elif age < 40:
    return '30-40'
  elif age < 50:
    return '40-50'
  elif age < 60:
    return '50-60'
  elif age < 70:
    return '60-70'
  elif age < 80:
    return '70-80'
  else :
    return '80+'

def parse_with_age_group(data):
  userid,age,gender,occupation,zip = data.split("|")
  return userid,age_group(int(age)),gender,occupation,zip,int(age)

#---------------------- write my code below -----------------------#

# Import the u.user file to fs variable
fs = sc.textFile("file:///Users/luochacha/Desktop/BigData_CW2/u.user")

# apply function parse_with_age_group to fs
fs_new = fs.map(parse_with_age_group)

# filter 40-50 and 50-60 age group respectively
fs_40_50 = fs_new.filter(lambda x: '40-50' in x)
fs_50_60 = fs_new.filter(lambda x: '50-60' in x)


----
# extract occupation in these two age groups
fs_40_50_s = fs_40_50.map(lambda x: x[3]).countByValue().items()
fs_50_60_s = fs_50_60.map(lambda x: x[3]).countByValue().items()

# extract 10 most common occupations for the users in each age group
fs_40_50_ss = sorted(fs_40_50_s, reverse = True, key  = lambda x : x[1])[:10]
fs_50_60_ss = sorted(fs_50_60_s, reverse = True, key  = lambda x : x[1])[:10]
# store data into list 
fs_40_50_lst = [item[0] for item in fs_40_50_ss]
fs_50_60_lst = [item[0] for item in fs_50_60_ss]

# convert list into rdd:
fs_40_50_lst = sc.parallelize(fs_40_50_lst)
fs_50_60_lst = sc.parallelize(fs_50_60_lst)

# intersection 40-50,50-60 and 10 occupations in all age groups
common=(fs_40_50_lst.distinct()).intersection(fs_50_60_lst.distinct())

# print the output
print (sorted(common.collect()))
