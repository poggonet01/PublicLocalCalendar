#SOME CODE VERIFICATION / Not included in project

from icalendar import Calendar,Event,Alarm,Todo
import duration
from duration import to_iso8601
from pytz import UTC
import json
from datetime import date,time,datetime,timedelta
import datetime
import time
from win10toast import ToastNotifier
from dateutil.parser import parse

# with open("final1.ics") as icsFile :
#     gcal = Calendar.from_ical(icsFile.read())

# g = open('final1.ics','rb')
# gcal = Calendar.from_ical(g.read())
# for component in gcal.walk():
#     if component.name == "VEVENT":
#         print("Dawfawefawf")
#         print(component.get('summary'))
#         startul = component.get('dtstart').dt
#     if component.name == "VALARM" :
#         #print(component.get('trigger').dt)
#         var = component.get('trigger').dt
        
#         minutes = int(var.total_seconds()/60)
#         # print(component.get('action'))
#         # print(component.get('description'))

#         zile = int(var.total_seconds()/60 / 1440)
#         ore = int ( (minutes -  zile * 1440 ) / 60)
#         minute = int ((minutes -  zile * 1440 ) - ore * 60)

#         ora_start = startul - datetime.timedelta(days=zile , hours=ore , minutes=minute)
#         timp = datetime.datetime.now()
#         print(ora_start > timp)

#         print(ora_start)
#         # print(minutes)
#         # print(hour)
#         # print(days)

# g.close()





# now = str(datetime.date.today())
# print(now)

# luni = datetime.datetime(2021,1,9,18,0,0) - datetime.timedelta(days=2,hours=2)

# print(luni)

# now = datetime.datetime.now() - datetime.timedelta(hours=2)
# print (datetime.datetime.now() > now)


now = datetime.datetime.now()
print(now)