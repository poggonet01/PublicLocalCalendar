import icalendar
from icalendar import Calendar,Event,Alarm,Todo
from datetime import datetime,date,time
import pytz
import json
import datetime
import time
from win10toast import ToastNotifier
from dateutil.parser import parse

def addEvent(cal,name,dtst,dtnd,trig) :
    event = Event()
    event.add('summary' , name)
    event.add('dtstart', dtst)
    event.add('dtend', dtnd)
    alarm = Alarm()
    k = datetime(2021,1,3,18,0,0)
    alarm.add('action','display')
    alarm.add('trigger' ,k )
    event.add_component(alarm)
    cal.add_component(event)
    with open ('final1.ics' , "wb") as f :
         f.write(cal.to_ical())

def compairTwoString(a , b) :
    return a == b

def includeAlarm(TimeOfEveniment , TimeOfAlarm)  :

    TimeOfEveniment = TimeOfEveniment + ":00"
    datetime = parse(TimeOfEveniment)
    difference = datetime.hour + TimeOfAlarm
    if difference < 0 :
        return str(24+difference) + ':' + str(datetime.minute)
    return str(difference) + ':' + str(datetime.minute)

if __name__ == '__main__':

    # cal = Calendar()
    # cal.add('summary' , 'Local Calendar/Python Project')
    
    # addEvent(cal,'nume1' ,datetime(2021,1,3,18,0,0),datetime(2021,1,3,18,0,0) , 10 )
    # addEvent(cal,'nume2' ,datetime(2021,1,3,18,0,0),datetime(2021,1,3,18,0,0) , 10 )

    with open("myevents.json") as jsonFile:
        jsonObject = json.load(jsonFile)
    
    evenimente = jsonObject['Evenimente']
    now = str(date.today())

    for ev in evenimente : 
        if compairTwoString(ev['Data'],now):
            hours_to_compare = str(datetime.datetime.now())
            OraAlarmei = includeAlarm(ev['Ora'] , ev['Alarma'])
            while not compairTwoString(hours_to_compare[11:16] ,OraAlarmei ) : 
                hours_to_compare = str(datetime.datetime.now())
            toaster = ToastNotifier()
            toaster.show_toast(ev['Denumire'],ev['Descriere'])