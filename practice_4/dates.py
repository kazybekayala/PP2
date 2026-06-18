from datetime import datetime, timedelta

#exercise 1, subtract five days from current date

current_date = datetime.now()
new_date = current_date - timedelta(days=5)

print("Current date:", current_date)
print("5 days ago:", new_date)
print("-" * 40)

#exercise 2, print yesterday, today, tomorrow

today = datetime.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday.date())
print("Today:", today.date())
print("Tomorrow:", tomorrow.date())
print("-" * 40)

#exercise 3, drop microseconds from datetime

now = datetime.now()

print("With microseconds:", now)
print("Without microseconds:", now.replace(microsecond=0))
print("-" * 40)

#exercise 4, calculate difference between two dates in seconds

date1 = datetime(2025, 1, 1, 12, 0, 0)
date2 = datetime(2025, 1, 2, 12, 0, 0)
difference = date2 - date1

print("Difference in seconds:", int(difference.total_seconds()))