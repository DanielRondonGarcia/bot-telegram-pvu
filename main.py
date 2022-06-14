import telebot
import json
from pprint import pprint
from json import JSONEncoder
import scrapping
import scrapping_tree
import schedule
from threading import Thread
from time import sleep

class ToJson(JSONEncoder):
        def default(self, o):
            return o.__dict__ 

bot_token = '2016312685:AAHwFfCKElx4GuYFIU5SvjvdHabWTiHMVOs'
chat_id = ''
parse_mode = 'HTML'
""" bot = telebot.TeleBot(bot_token) """
bot = telebot.TeleBot(bot_token)
flag_data_json = False
data = {}
token= ''
data['config'] = []

try:
    with open('data.json') as file:
        data = json.load(file)
except:
  print("No hay data")
  flag_data_json=True
pprint(data)


def uno():
    for data_ in data["config"]:
        bot.send_message(data_["id"], scrapping.messsage_info_general(data_["token"]), parse_mode=parse_mode)    
        bot.send_message(data_["id"], str(data_["username"]))
def dos():
    for data_ in data["config"]:        
        alerta = scrapping.messsage_info(data_["token"])        
        if not alerta:
            print("Empty")
        else:            
            for i in alerta:
                print(i)
                bot.send_message(data_["id"], i, parse_mode=parse_mode)
def tres():
    for data_ in data["config"]:        
        alerta = scrapping_tree.messsage_info_tree(data_["token"])
        if not alerta:
            print("Empty")
        else:
            print(alerta)
            for i in alerta:
                bot.send_message(data_["id"], i, parse_mode=parse_mode)
def cuatro():
    for data_ in data["config"]:                
            bot.send_message(data_["id"], scrapping_tree.messsage_info_tree_general(data_["token"]), parse_mode=parse_mode)        

def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)
        
# Create the job in schedule.
schedule.every(1).hours.do(uno)
schedule.every(10).minutes.do(dos)
schedule.every(1).hours.do(tres)
schedule.every(2).hours.do(cuatro)

# Spin up a thread to run the schedule check so it doesn't block your bot.
# This will take the function schedule_checker which will check every second
# to see if the scheduled job needs to be ran.
Thread(target=schedule_checker).start()

def getUpdates():
    a = ToJson().encode(bot.get_updates())
    a = json.loads(a)
    return a


info = {
    'TOKEN' : 'Para obtener el TOKEN DE SESION Bearer de Plants Vs Undead deber de ejecutar el siguiente codigo en la consola de Herramienta para desarrolladores',
    'codigo' : 'var x = localStorage.getItem("token"); x',    
    }
commands = {
    '/messsage_info_tree' : 'Muestra la relevante del arbol del mundo',
    '/messsage_info_tree_general' : 'Muestra la información general del arbol',
    '/messsage_info' : 'Muestra la Las alertas de tu granja',
    '/messsage_info_general' : 'Muestra la informacion general de tu granja',
    '/info' : 'Información de uso',
    '/shutdown' : 'Apaga el servidor',
    }



def request_create_user_json(array):
    @bot.message_handler(regexp=".{268,268}$")
    def handle_message(message):
        json_ = ToJson().encode(message)
        json_ = json.loads(json_)        
        private_id = json_["from_user"]["id"]
        username = str(json_["from_user"]["username"])
        token = json_["text"]
        flag_= False
        for data_ in data["config"]:   
            if data_["id"] == private_id  or data_["token"] == token:
                flag_= True
                bot.send_message(private_id, 'Ya te encuentras registrado', parse_mode=parse_mode)
        if flag_ == False: #Entra a registrarse
            bot.send_message(private_id, 'Estamos validando los datos', parse_mode=parse_mode)        
            if not token:
                bot.send_message(private_id, 'No enviaste el token')
            else:
                data['config'].append({
                    'id':private_id,
                    'username':username,
                    'token':token,
                })
                with open('data.json', 'w') as file:
                    json.dump(data, file, indent=4)
                texto =''
                m = f"<b>Usuario: </b> <code> {username} </code> \n"
                m += f"<b> acaba de ser registrado con el id: </b> <code>{private_id}</code> \n"        
                m += f"<code> En breve podras ver tu informacion de Plants vs Undead</code>  \n"                 
                texto = texto+m+"\n"
                bot.send_message(private_id, texto, parse_mode=parse_mode)
        print('Creancion de usuario existe json')

def request_create_user():
    @bot.message_handler(regexp=".{268,268}$")
    def handle_message(message):
        json_ = ToJson().encode(message)
        json_ = json.loads(json_)        
        private_id = json_["from_user"]["id"]
        username = str(json_["from_user"]["username"])
        token = json_["text"]
        flag_= False
        for data_ in data["config"]:   
            if data_["id"] == private_id  or data_["token"] == token:
                flag_= True
                bot.send_message(private_id, 'Ya te encuentras registrado', parse_mode=parse_mode)
        if flag_ == False: #Entra a registrarse
            bot.send_message(private_id, 'Estamos validando los datos', parse_mode=parse_mode)        
            if not token:
                bot.send_message(private_id, 'No enviaste el token')
            else:
                data['config'].append({
                    'id':private_id,
                    'username':username,
                    'token':token,
                })
                with open('data.json', 'w') as file:
                    json.dump(data, file, indent=4)
                texto =''
                m = f"<b>Usuario: </b> <code> {username} </code> \n"
                m += f"<b> acaba de ser registrado con el id: </b> <code>{private_id}</code> \n"        
                m += f"<code> En breve podras ver tu informacion de Plants vs Undead</code>  \n"                 
                texto = texto+m+"\n"
                bot.send_message(private_id, texto, parse_mode=parse_mode)
        print('Creancion de usuario')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    json_ = ToJson().encode(message)
    json_ = json.loads(json_)
    private_id = json_["from_user"]["id"]
    username = str(json_["from_user"]["username"])
    print(json_["from_user"]["id"])
    if flag_data_json:
        bot.send_message(private_id, 'Escribe tu token exactamente...')
        request_create_user()
    else:
        bot.send_message(private_id, 'Escribe tu token exactamente...')
        request_create_user_json(json_)
            

##########################################Comandos##########################################

@bot.message_handler(commands=['messsage_info_tree'])
def send_welcome(message):
    json_ = ToJson().encode(message)
    json_ = json.loads(json_)
    private_id = json_["from_user"]["id"]
    for data_ in data["config"]:   
        if data_["id"] == private_id:            
            alerta = scrapping_tree.messsage_info_tree(data_["token"])
            if not alerta:
                print("Empty")
            else:
                print(alerta)
                for i in alerta:
                    bot.send_message(private_id, i, parse_mode=parse_mode)
        else:
            bot.send_message(private_id, 'No has iniciado el bot', parse_mode=parse_mode)

@bot.message_handler(commands=['messsage_info_tree_general'])
def send_welcome(message):
    json_ = ToJson().encode(message)
    json_ = json.loads(json_)
    private_id = json_["from_user"]["id"]
    for data_ in data["config"]:   
        if data_["id"] == private_id:
            bot.send_message(private_id, scrapping_tree.messsage_info_tree_general(data_["token"]), parse_mode=parse_mode)
        else:
            bot.send_message(private_id, 'No has iniciado el bot', parse_mode=parse_mode)
            
@bot.message_handler(commands=['messsage_info_general'])
def send_welcome(message):
    json_ = ToJson().encode(message)
    json_ = json.loads(json_)
    private_id = json_["from_user"]["id"]
    for data_ in data["config"]:   
        if data_["id"] == private_id:
            bot.send_message(private_id, scrapping.messsage_info_general(data_["token"]), parse_mode=parse_mode)
        else:
            bot.send_message(private_id, 'No has iniciado el bot', parse_mode=parse_mode)

@bot.message_handler(commands=['messsage_info'])
def send_welcome(message):
    json_ = ToJson().encode(message)
    json_ = json.loads(json_)
    private_id = json_["from_user"]["id"]
    for data_ in data["config"]:   
        if data_["id"] == private_id:
            alerta = scrapping.messsage_info(data_["token"])            
            print(alerta)
            if not alerta:
                print("Empty")
            else:
                print(alerta)
                for i in alerta:
                    bot.send_message(private_id, i, parse_mode=parse_mode)
        else:
            bot.send_message(private_id, 'No has iniciado el bot', parse_mode=parse_mode)



@bot.message_handler(commands=['info'])
def send_welcome(message):
    json_ = ToJson().encode(message)
    json_ = json.loads(json_)
    private_id = json_["from_user"]["id"]
    for info_ in info: 
        bot.send_message(private_id, info[info_])
@bot.message_handler(commands=['help'])
def send_welcome(message):
    json_ = ToJson().encode(message)
    json_ = json.loads(json_)
    private_id = json_["from_user"]["id"]
    for command_ in commands: 
        bot.send_message(private_id, command_+' - '+commands[command_])

@bot.message_handler(commands=['data'])
def send_welcome(message):
    json_ = ToJson().encode(message)
    json_ = json.loads(json_)
    private_id = json_["from_user"]["id"]
    for data_ in data["config"]:
        bot.send_message(private_id, str(data_["username"]))

bot.infinity_polling()