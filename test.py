from datetime import datetime, date

# Given date string
given_date_str = '17/02/2023'

# Convert given date string to datetime object
given_date = datetime.strptime(given_date_str, '%d/%m/%Y')

# Get today's date as a date object
today = date.today()

# Compare the dates
if given_date.date() == today:
    print('The given date is today')
elif given_date.date() > today:
    print('The given date is in the future')
else:
    print('The given date is in the past')
