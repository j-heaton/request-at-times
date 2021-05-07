from datetime import datetime as dt
from datetime import timedelta
import time
import csv
import requests
import _thread

#url to make requests to
url = 'https://ifconfig.co/'

#this variable holds the current time
time_now = dt.now()
#this variable is a datetime object representing the next midnight
time_midnight = time_now.replace(day=time_now.day+1, hour=0, minute=0, second=0, microsecond=0)
#this variable holds the amount of time until the next midnight
delta = time_midnight-time_now
#sleep until midnight
time.sleep(delta.seconds)
#get the timestamps from the csv file
with open('timestamps.csv') as csvfile:
    time_reader = csv.reader(csvfile)
    str_timestamps = list(time_reader)
#this variable holds the number of timestamps
n_timestamps = len(str_timestamps[0])
dt_timestamps = list()
#this loop converts the timestamps from strings to datetime objects
for i in range(n_timestamps):
    dt_timestamps.append(dt.strptime(str_timestamps[0][i], "%H:%M:%S"))
    dt_timestamps[i] = dt_timestamps[i].replace(year=dt.now().year, month=dt.now().month, day=dt.now().day)
#this loop iterates through the timestamps, sleeping until that time is reached, then making a request to the specified url
#if the next timestamp in the list has the same value as the current timestamp, a new thread will start to concurrently make requests
for i in range(n_timestamps):
    delta = dt_timestamps[i]-dt.now()
    time.sleep(delta.seconds)
    while i<n_timestamps-1 and dt_timestamps[i+1] == dt_timestamps[i]:
        _thread.start_new_thread(requests.get, (url, None))
        i += 1
    requests.get(url)