from datetime import tzinfo, timedelta, datetime, timezone
from pytz import timezone
import pytz
import tzlocal
import tzlocal  # $ pip install tzlocal
import dateutil.parser
import time
from dateutil.tz import gettz

# print(datetime.now())

print(datetime.now(tzlocal.get_localzone()))




local_timezone = tzlocal.get_localzone()  # pytz-timezone

future_in_half_hour = datetime.now(pytz.utc) + timedelta(minutes=30)
local_time = future_in_half_hour.astimezone(local_timezone)

#print(future_in_half_hour)
#print(local_time)

datestring = '2019-05-03 11:12:53.288829-04'
# utc_dt = datetime.utcfromtimestamp(fd)



format = '%Y-%m-%dT%H:%M:%S%z'
# datestring = '2016-09-20T16:43:45-07:00'

#d = datetime.strptime(datestring, format)     #3.2+
# print(d)

now = datetime.now()
# print (now)

date_time_str = '2019-05-03 16:07:38.742325+00:00'
date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f+00:00')

print(type(date_time_obj))


print(datetime.now(timezone('UTC')))


# result = datetime.strptime('2019-05-03 16:07:38.742325+00:00','%Y-%m-%d %H:%M:%S.%f00:00%z')

# print(result)
aware_local_now = datetime.now(
    tz=datetime.strptime(time.strftime("%z", time.localtime()), "%z").tzinfo)

print(aware_local_now)

print(aware_local_now.timestamp())


print(datetime.now(pytz.utc))