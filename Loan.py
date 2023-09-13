#to import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")


pd.set_option("display.max_rows",50)
pd.set_option("display.max_columns",120)

#to read the actual csv and import it here
loanData = pd.read_csv('C://Users/hpasu/OneDrive/Desktop/loan.csv')
#to check the data and their range to see what data types there are in here
loanData.info()

#data cleaning
#need to drop columns that have no use to data analysis as they provide no information regarding driving factors as they unique values or singular values
loanData.isnull().sum(axis=0).sort_values() #check which values have null has value
loanData = loanData.loc[:,loanData.isnull().sum(axis=0)!=39717] #remove the columns that have null as value

#dropping columns that have no factor on data analysis
loanData = loanData.drop(columns = ['next_pymnt_d','last_pymnt_amnt', 'last_pymnt_d', 'url', 'desc','title','zip_code','pymnt_plan','collections_12_mths_ex_med','application_type','policy_code','acc_now_delinq','chargeoff_within_12_mths','delinq_amnt','initial_list_status','tax_liens'])

#now need to convert the remaining string values into integer so converting the date and time
loanData["issue_d"]= pd.to_datetime(loanData["issue_d"],format = '%b-%y')
loanData["last_credit_pull_d"]= pd.to_datetime(loanData["last_credit_pull_d"],format = '%b-%y')
loanData.info()

#need to format the date columns into integer
loanData["issue_d"]= pd.to_datetime(loanData["issue_d"],format = '%b-%y')
loanData["last_credit_pull_d"]= pd.to_datetime(loanData["last_credit_pull_d"],format = '%b-%y')


#From research, annual income could play a factor into defaulting on a loan. Let's check with this data to see if there is a corerlation.
loanData.annual_inc.describe()

#need to put people in categories of income to demonstrate a correlation between categorical variables
#so let's define people in low, middle class, low high class, high

incomeBinRanges=[0,40000,80000,120000,6000000]
incomeBinNames= ["low", "low MC", "upper MC", "highClass"]
loanData["income_bins"]= pd.cut(loanData["annual_inc"],bins=incomeBinRanges,labels=incomeBinNames)
loanData["income_bins"].count()

#need to put the data in the bins assigned
loanData_pivoted= loanData.pivot_table(index=["income_bins"],values="id",columns="loan_status",aggfunc="count")
loanData_pivoted.reset_index(inplace=True)


loanData_pivoted["total"]= loanData_pivoted["Charged Off"]+loanData_pivoted["Current"]+loanData_pivoted["Fully Paid"]
loanData_pivoted["Charged Off"]= round((loanData_pivoted["Charged Off"]/loanData_pivoted["total"])*100,2) # to find out how many people in this bin are either in the charged off, current or fully paid bins

loanData_pivoted["Current"]= round((loanData_pivoted["Current"]/loanData_pivoted["total"])*100,2)

loanData_pivoted["Fully Paid"]= round((loanData_pivoted["Fully Paid"]/loanData_pivoted["total"])*100,2)

loan_data_pivoted_2=loanData_pivoted.drop("total",axis=1)
loan_data_pivoted_2

loan_data_pivoted_2.plot(kind="bar",x="income_bins",stacked=True,figsize=(12,6))
plt.show()





#Checking verification status corerlation
loanData["verification_status"].value_counts()
loanData_veri= loanData.pivot_table(index="verification_status",columns="loan_status",values="id",aggfunc="count")
loanData_veri.reset_index(inplace=True)

loanData_veri["Total"]= loanData_veri["Charged Off"]+loanData_veri["Current"]+loanData_veri["Fully Paid"]
loanData_veri["Charged Off"]= round((loanData_veri["Charged Off"]/loanData_veri["Total"])*100,2)
loanData_veri["Current"]= round((loanData_veri["Current"]/loanData_veri["Total"])*100,2)
loanData_veri["Fully Paid"]= round((loanData_veri["Fully Paid"]/loanData_veri["Total"])*100,2)
loanData_veri= loanData_veri.drop("Total",axis=1)
loanData_veri.plot(kind="bar",stacked=True,x="verification_status",figsize=(12,6))
plt.show()





#Checking how grade is correlated
loanGradeGroup = loanData.groupby(['grade','loan_status'])['id'].count()
loanGradeGroup= loanGradeGroup.unstack()
loanGradeGroup['Total'] = loanGradeGroup['Charged Off'] + loanGradeGroup['Current'] + loanGradeGroup['Fully Paid']
loanGradeGroup['Charged Off'] = (loanGradeGroup['Charged Off']/loanGradeGroup['Total'])*100
loanGradeGroup['Current'] = (loanGradeGroup['Current']/loanGradeGroup['Total'])*100
loanGradeGroup['Fully Paid'] = (loanGradeGroup['Fully Paid']/loanGradeGroup['Total'])*100

loanGradeGroup = loanGradeGroup.drop(columns = ['Total'])

Loan_Plot = loanGradeGroup.plot(kind='bar',stacked=True,figsize=(12,6))
plt.show()



#Checking how home ownership is correlated
loanDataHome=loanData.pivot_table(index=["home_ownership"],values="id",columns="loan_status",aggfunc="count",fill_value=0)
loanDataHome.reset_index(inplace=True)
loanDataHome["total"]= loanDataHome["Charged Off"]+loanDataHome["Current"]+loanDataHome["Fully Paid"]
loanDataHome= loanDataHome.drop("total",axis=1) #need to drop total from plot
loanDataHome= loanDataHome.loc[loanDataHome["home_ownership"]!="NONE",] # need to drop none value
loanDataHome.plot(x="home_ownership",kind="bar",stacked=True,figsize=(12,6))
plt.show()
