from bs4 import BeautifulSoup
import time
import requests
from requests.structures import CaseInsensitiveDict
import json
from datetime import datetime,timedelta
def time_exchange():
    s1 = "00:00:00"
    ahora = datetime.utcnow().strptime('%H:%M:%S')
    dentro_de_1_hora = ahora + timedelta(hours=1)
    return("Dentro de una hora: " + str(dentro_de_1_hora))
    
def request_api(bearer):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer "+bearer
    url_result = requests.get('https://backend-farm.plantvsundead.com/world-tree/datas', headers=headers)
    soup = BeautifulSoup(url_result.content, 'html.parser')
    site_json=json.loads(soup.text)
    return site_json

def messsage_info_tree(bearer):
    data_print = []
    data = request_api(bearer)
    m0 = f"<b>Nivel Actual: </b> {data['data']['level']} \n"        
    m0 += f"<b>Total Agua: </b>  <code>{data['data']['totalWater']}</code>  \n"
    m0 += f"<b>Agua que aportaste: </b>  <code>{data['data']['myWater']}</code>  \n"
    if data['data']['yesterdayReward']:
        m0 += f"<b>Recompensa de ayer: </b>  <code>{data['data']['yesterdayReward']}</code>  \n"    
    data_print.append(m0)
    if data['data']['level'] == len(data['data']['reward']):
        alerta = f" ¡ATENCIÓN! Se completo el arbol del mundo: Tienes hasta las 7:00 PM\nApurate y ve a reclamarlos\nhhttps://marketplace.plantvsundead.com/login#/worldtree\n"
        data_print.append(alerta)
                      
    print('Working tree')    
    return(data_print)

def messsage_info_tree_general(bearer):
    data = request_api(bearer)
    m ="Informe del árbo del mundo"+"\n"
    for data_data in data['data']['reward']:
        m += f"<b>Reward: </b> {data_data['type']} \n"
        m += f"<b>Estado: </b>  <code>{data_data['status']}</code>  \n"
        m = m+"\n"
    print('Working tree General')
    return(m)
