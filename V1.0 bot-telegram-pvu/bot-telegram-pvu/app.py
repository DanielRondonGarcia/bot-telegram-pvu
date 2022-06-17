import json
from logging import captureWarnings
from bs4 import BeautifulSoup
import requests
from requests.structures import CaseInsensitiveDict
import gspread
from json import JSONEncoder
from datetime import datetime,timedelta
from google.oauth2.service_account import Credentials
import os
import re
import telebot
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
jason_ = {
    "type": "service_account",
    "project_id": "stalwart-cable-327515",
    "private_key_id": "df685b4dd69ba65427820469c1eb5727ca4afd90",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQDYtmTC/vhEDwg6\nlhA31QOLpweUA3WeiH0ZBJxlHozXDQPTkYtZbNOSQ3KHSLB58IaCuaMKq+wgourG\nIzP5xJApSx+76l9XKcY0BxI8+2YvJoXk2TDCH+80aAT95pXsO2vif5HW5jwmiF4Y\nVXLVhAdHWeQgqrzZKIIqJuun4KC1kxWkU3gd4Mja6oMC4X2kEY/KIUbZztAsHlO7\nGTnx2z0XFTu+S8iIyHeyE4HS7qU1a331kpGvtuqmVYdf0bSsQ6yIH6b6FPfHaxeQ\n+fMJMUQTDJCyjvOd4wrdBoJyyFiXZEhQJqnbQmBPnmiZtBfDBR2dFioAVjEQx/+h\nsJYnksMJAgMBAAECgf8yAyhqQSKGTD3IF47TBpRaFe/2WM8F/XUSZp2Sy0A+VUBA\nP55jSA3BVWBmsGrljNxgysKZht8HTMeZK6BWmPaNrkiizqyWj/tWLQaf3W4gORKe\nLDDDNBK15CKoenMHmI5JLLGRHQYKzO5d7A5j0TuR+vjCv/UTIsTuXEZW53rS3GDe\nWB4LiADw3I8qt7rRCT1Rg8SG6zKb9LbX1EXYAfj+rx1YJGDD4HAInKTYiViHAzWa\nHGV6UEArC8/X3Ghz2dBOSTzMXSnA56WVJQc/OSUBkHmeFgCT7saRSbUjGoPzwNqC\ndazW4x63Gp++9Eqer+bIYvnc1xWK/2wm4oGD2hcCgYEA8xcPRoQJHscXxnRi5/FR\n3G9V0++ZsYyPFD4fK9mN2CHH7QnE98gaBubCtp0WMpjqlqnZtw0/s5LsBzziaLtK\nrYPXknfIrWIMRWCjHf+VQQz67wbK5xvPO5CnbD8ZEUDcPJyEg3qaWYUBTql9tpiG\niWVnrVgoZn5akM8OT8PO7r8CgYEA5Di3XAHWEXiDkpicrAlbeDO0QLSPuZgT5WS4\nFMt5kgoIDByRAGdA40m7GIdiB5HW4EzCCCI+a0qTRBxRuKbe5HpRPchlNcZQUIRN\n2oNXLoTDUkDvPKZUdjiY0S/c/GKIyeRfxNfN2GABlAPJrAf91BkmZWCCaJ+qX/pe\nP/K4iDcCgYAEaBKa0KHpsOo5arqwQaueN1Zy9RDwKwAc+dNO1C7CEDqzjU3IwBPY\ntC4raUWRvTvjZ0jPDKpu8ubcarof8+UyqAUsXoeAvRpD17CdRpjKCRYzZwgekF59\nUe33BF3L9kUHxD6Ss5JAtSyE5IWm3bTyoKf0eHijAv9ZSKeVwpLpuQKBgQDL7qpa\nOwHQxsG7g0esqwfjV0Bg+Xfcvjo5J1Ees9vEVdZvDC++DoX7E+1ts7wzS2yZLb3M\nitz//rmtiSi1Ode+jlZ+QM2/yaAG8tKmyepjlRr8Ky4cIf0jTtuvQXfUxy+4SKwT\nN0unZ9LBMslJQjLdDkQzHpQpbVNPRGhn+DpQ7QKBgFjSBueddWojM969KYmtPp9E\nAfpIqHcS5i9Gqrk9pMtwSyEFHIz65elNAl4oykXR9CDnWO56KE+cv6UwF/zUekaZ\ntk1IFDzgQj4l4vY0oCg/optdtYbl69xYJS6ylykBDspZZuUeYE+lvxFGM1xDdL3z\nCRa3pZmfyXjuDthZ5i2T\n-----END PRIVATE KEY-----\n",
    "client_email": "datapvu@stalwart-cable-327515.iam.gserviceaccount.com",
    "client_id": "110707326515945313468",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/datapvu%40stalwart-cable-327515.iam.gserviceaccount.com"
}
bot = telebot.TeleBot('1917056678:AAHCY_656ehvUtTl9DIBifXEYTILn0yuOP8')

class ToJson(JSONEncoder):
        def default(self, o):
            return o.__dict__ 

def parse_timedelta(stamp):
    if 'day' in stamp:
        m = re.match(r'(?P<d>[-\d]+) day[s]*, (?P<h>\d+):'
                     r'(?P<m>\d+):(?P<s>\d[\.\d+]*)', stamp)
    else:
        m = re.match(r'(?P<h>\d+):(?P<m>\d+):'
                     r'(?P<s>\d[\.\d+]*)', stamp)
    if not m:
        return ''

    time_dict = {key: float(val) for key, val in m.groupdict().items()}
    if 'd' in time_dict:
        return timedelta(days=time_dict['d'], hours=time_dict['h'],
                         minutes=time_dict['m'], seconds=time_dict['s'])
    else:
        return timedelta(hours=time_dict['h'],
                         minutes=time_dict['m'], seconds=time_dict['s'])

def get_user(id_user):
    print('check user data')
    scopes = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_file(
        json.loads(json.dumps(jason_)),        
        scopes=scopes
    )
    client = gspread.authorize(creds)
    sh = client.open("data_pvu")
    shw = sh.get_worksheet(3)
    id_ = shw.find(str(id_user))          
    if id_:
        values_list = shw.row_values(id_.row)
        if values_list[3] == 'INACTIVO':
            print('Existing user INACTIVO')
            bot.send_message(values_list[0], text='Tu suscripcion se encuentra INACTIVA\n Deber volver a pagar la suscripcion para activarla\n Visita el bot de configuración <a href="t.me/utilitiesPVU_bot">utilities Plant Vs Undead</a>',parse_mode='HTML')
            return True
        elif values_list[3] == 'PENDIENTE':
            print('Existing user PENDIENTE')
            bot.send_message(values_list[0], text='Tu suscripcion se encuentra PENDIENTE de activación',parse_mode='HTML')
            return True
        elif values_list[3] == 'ACTIVO':
            print('Existing user ACTIVO')
            try:
                time_ = datetime.strptime(values_list[4].replace("'",''), '%Y-%m-%d %H:%M:%S')
            except:
                time_ = datetime.strptime(values_list[4].replace("'",''), '%Y-%m-%dT%H:%M:%S')
            today = datetime.utcnow()            
            diferencia = today-time_        
            bot.send_message(values_list[0], text='Tu suscripcion se encuentra ACTIVA y EXPIRA en: '+str(parse_timedelta(values_list[5]) - diferencia),parse_mode='HTML')
            return True    
    return False

def get_user_active(id):
    print('check user data')
    scopes = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_file(
        json.loads(json.dumps(jason_)),        
        scopes=scopes
    )
    client = gspread.authorize(creds)
    sh = client.open("data_pvu")
    shw = sh.get_worksheet(3)
    id_ = shw.find(str(str(id)))          
    if id_:
        values_list = shw.row_values(id_.row)
        if values_list[3] == 'ACTIVO':
            print('Existing user')
            return True
        else:
            print('Usuario se encuentra: '+values_list[3]+' '+values_list[1])
            bot.send_message(values_list[0], text='Tu cuenta aun se encuentra: '+ str(values_list[3]) ,parse_mode='HTML')
            return False
    print('User not registered ')
    return False

def get_all_data_user_active(id):
    print('check user data')
    scopes = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_file(
        json.loads(json.dumps(jason_)),        
        scopes=scopes
    )
    client = gspread.authorize(creds)
    sh = client.open("data_pvu")
    shw = sh.get_worksheet(3)
    id_ = shw.find(str(str(id)))          
    if id_:
        values_list = shw.row_values(id_.row)
        if values_list[3] == 'ACTIVO':
            print('Existing user')
            values_list = shw.row_values(id_.row)
            return values_list
        else:
            print('Usuario se encuentra: '+values_list[3]+' '+values_list[1])
            bot.send_message(values_list[0], text='Tu cuenta aun se encuentra: '+ str(values_list[3]) ,parse_mode='HTML')        
