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


def compairTwoString(a , b) :
    if a == b : return True
    return False

def includeAlarm(TimeOfEveniment , TimeOfAlarm)  :

    #TimeOfEveniment = TimeOfEveniment + ":00"
    datetime = parse(TimeOfEveniment)
    difference = datetime.hour + TimeOfAlarm
    if difference < 0 :
        return str(24+difference) + '0:' + str(datetime.minute)
    # if difference < 10 and datetime.minute < 10 :    return '0' + str(difference) + ':0' + str(datetime.minute)
    # elif difference < 10 : return  '0' +str(24+difference) + str(datetime.minute)
    # elif datetime.minute < 10 : return str(24+difference) + ':0' + str(datetime.minute)
    if difference < 10 and datetime.minute < 10 : return '0' + str(difference) +':0'+ str(datetime.minute)
    if difference < 10 : return  '0' +str(difference) +':'+ str(datetime.minute)
    if datetime.minute < 10 : return  str(difference) +':0'+ str(datetime.minute)
    return str(difference) + ':' + str(datetime.minute)

def checkIfDateNoChange(TimeOfEveniment , TimeOfAlarm) :
    TimeOfEveniment = TimeOfEveniment + ":00"
    datetime = parse(TimeOfEveniment)
    difference = datetime.hour + TimeOfAlarm
    return difference < 0

def Eveniment(cal,name,dtst,trig,triggerInfo) :

    event = Event()
    event.add('summary' , name)
    event.add('dtstart', dtst)
    alarm = Alarm()
    alarm.add('trigger' , trig ) 
    alarm.add('action','display')
    alarm.add('description' , triggerInfo)
    event.add_component(alarm)
    cal.add_component(event)
    with open ('myevents1.ics' , "wb") as f :
         f.write(cal.to_ical())

def icsFormat() :

    cal = Calendar()
    cal.add('summary' , 'Local Calendar/Python Project')

    DateForm = '%Y-%m-%d'
    HourForm = '%H:%M'

    Eveniment(cal,'Ziua de nastere a mamei' ,datetime.datetime(2021,1,12,9,37,0) , datetime.timedelta(hours=1,minutes=35) , 'Sa sun sa o felicit' )
    Eveniment(cal,'Sedinta la scoala' ,datetime.datetime(2021,1,9,20,21,0) , datetime.timedelta(hours=1) , 'Sa merg la scoala sa aflu ce se intampla' )
    Eveniment(cal,'Sedinta la serviciu' ,datetime.datetime(2021,1,9,17,26,0) , datetime.timedelta(hours=1) , '"Sa iau carnetul sa fac notite')
    Eveniment(cal,'Excursie la muzeu' ,datetime.datetime(2021,1,9,17,26,0) , datetime.timedelta(hours=1) , 'Sa imi cumpar bilet' )

    with open("myevents1.ics") as icsFile :
        gcal = Calendar.from_ical(icsFile.read())

    for eveniment in gcal.walk() :
        out = True 
        if eveniment.name == "VEVENT" :
                denumireEv = eveniment.get('summary')
                oraStart = eveniment.get('dtstart').dt 
        if eveniment.name == "VALARM" :
                triggerAlarm = eveniment.get('trigger').dt
                descriereEv = eveniment.get('description')  

                while out :
                        minutes = int(triggerAlarm.total_seconds()/60)
                        zile = int(triggerAlarm.total_seconds()/60 / 1440)
                        ore = int ( (minutes -  zile * 1440 ) / 60)
                        minute = int ((minutes -  zile * 1440 ) - ore * 60)

                        ora_alarma = oraStart - datetime.timedelta(days=zile,hours=ore,minutes=minute)
                        print(ora_alarma)
                        timpActual = datetime.datetime.now()

                        if ora_alarma + datetime.timedelta(seconds=59) < timpActual : 
                            toaster = ToastNotifier()
                            toaster.show_toast(denumireEv ,"Evenimentul a avut loc deja , " "ne pare foarte rau :(  ")
                            out = False
                        else :  
                            while ora_alarma > timpActual : 
                                timpActual = datetime.datetime.now()
                            toaster = ToastNotifier()
                            toaster.show_toast(denumireEv , descriereEv)
                            out = False

def jsonFormat() :
    

    with open("myevents2.json") as jsonFile:
        jsonObject = json.load(jsonFile)
    
    DateForm = '%Y-%m-%d'
    HourForm = '%H:%M'

    evenimente = jsonObject['Evenimente']

    for ev in evenimente : 
        out = True
        while out : 
            now = str(datetime.date.today())
            date_format_now = datetime.datetime.strptime(now , DateForm)
            date_format_cal = datetime.datetime.strptime(ev['Data'] , DateForm)
            OraAlarmei = includeAlarm(ev['Ora'] , ev['Alarma'])
            
            check = checkIfDateNoChange(ev['Ora'] , ev['Alarma'])

            if check : 
                date_format_cal = date_format_cal - datetime.timedelta(1)
            

            if date_format_now > date_format_cal : 
                toaster = ToastNotifier()
                toaster.show_toast(ev['Denumire'] ,"Evenimentul a avut loc deja , " "ne pare foarte rau :(  ")
                out = False
            elif compairTwoString(ev['Data'],now) : 
                hours_to_compare = str(datetime.datetime.now())
                hour_format_now = datetime.datetime.strptime(hours_to_compare[11:16],HourForm)
                hour_format_cal = datetime.datetime.strptime (OraAlarmei , HourForm)
                print(OraAlarmei)
                if hour_format_now <= hour_format_cal :
                    while not compairTwoString(hours_to_compare[11:16] ,OraAlarmei ) : 
                        hours_to_compare = str(datetime.datetime.now())
                    toaster = ToastNotifier()
                    toaster.show_toast(ev['Denumire'],ev['Descriere'])
                else :
                    toaster = ToastNotifier()
                    toaster.show_toast(ev['Denumire'] ,"Evenimentul a avut loc azi deja , " "ne pare rau :(")
                out = False

def StartProgram (format) :
    if format == "json" :
       jsonFormat()
    else : icsFormat()

if __name__ == '__main__' :

    RightFormat = False
    Repeating = 0
    while not RightFormat :
        if Repeating == 0 :
            format = input("Alegeti formatul in care va fi stocat calendarul cu evenimente (JSON/ICS) :  ")
            if format.lower() == "json" or format.lower() == "ics" :
                RightFormat = True
            Repeating = Repeating + 1
        else : 
            format = input("Format inexistent . Alegeti unul din ( JSON / ICS ) :  ")
            if format.lower() == "json" or format.lower() == "ics" :
                RightFormat = True
    StartProgram(format.lower())