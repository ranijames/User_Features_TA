# User_Features_TA
The TA_script.py scripts helps to define the three features,
   highly_active: Whether the user is highly active, i.e. has a large number of events (True/False)
   multiple_days: Whether the user is active for multiple days (True/False)
   weekday_biz: Whether the user's traffic tends to occur during weekday business hours (True/False)

The additional feature is defined using logistic regression. The prediction is based on highly active users based on time series information.

# Describe the rules and logic you use to compute each feature

The rules used here is to groupby each users based on the TimeStamp column (ts here)
Then I used a value of 5+ as a cut-off for each users to be called so.
For insatnce for Highly active users I used 5 or greater as call them True
And so as for Multiple days (including weekends).
For business days if the user is using the website between busniess hours (9:00 -18:00) and also on the 5 week days (Mon-Friday)
The additional feature is defined using logistic regression. The prediction is based on highly active users based on time series information.
The Logistic regression prediction is based on scores between 0.58 to 1
A score of 0.58 are for the customers showing least change or no chance of being buyers 
A score 1 shows they are potential buyers

