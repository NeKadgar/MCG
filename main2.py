import requests
import json
import time
import pyotp
from numba import jit
import logging as logger

from multiprocessing import Pool


logger.basicConfig(filename="sample.log", level=logger.INFO)
start_time = time.time()
secret = 'secret'
API_CODE = 'api'
list1 = []





def get_code():
    # get a token that's valid right now
    my_secret = 'YMLGKHWOINVTEI2X'
    my_token = pyotp.TOTP(my_secret)

    # print the valid token
    return my_token.now()
#print(get_code())
def get_data_price(APP_ID): #возвращает все цены

    url_data='https://bitskins.com/api/v1/get_price_data_for_items_on_sale/?api_key='+API_CODE+'&code='+get_code()+'&app_id='+str(APP_ID)
    #data = requests.get(url_data)
    data = requests.get(url_data).json()
    filename = 'mylowlist.json'
    myfile = open(filename, mode='r', encoding='utf-8')
    lines = myfile.read().split(',')
    data2 = []
    for i in range(0,len(lines)):
        for n in range(0,len(data['data']['items'])):
            if lines[i]==data['data']['items'][n]['market_hash_name']:
              data2.append(data['data']['items'][n])
    filename = 'AVERAGE.json'
    myfile = open(filename, mode='w', encoding='utf-8')
    json.dump(data2, myfile, sort_keys=True, indent=4)
    myfile.close()
    #print(data2)


    print('----------------------------')
#get_data_price(570)



def average(classid,instanceid):
    url = 'https://market.csgo.com/api/ItemHistory/' +classid + '_' +instanceid +'/?key=' +secret



def balance():
    url = 'https://market.csgo.com/api/GetMoney/?key=' + secret
    balance = requests.get(url).json()
    logger.info(balance)
    return balance['money']


def ping():
    url = 'https://market.csgo.com/api/PingPong/?key=' + secret
    pong = requests.get(url).json()
    print(pong['success'])

def BestBuyOffer(classid,instanceid):
    url = 'https://market.csgo.com/api/BuyOffers/'+ str(classid) +'_' + str(instanceid) +'/?key=' + secret
    check = requests.get(url)
    try:
        if check.raise_for_status() == None:
            check = check.json()
            if check["success"] == True and check["offers"][0]["my_count"] == '0':
                return check["best_offer"]
            else:
                return 'er'
        else:

            return 'er'
    except:
        time.sleep(2)
        return 'er'
#BestBuyOffer(2693087297,188530139)
def ProcessOrder(classid,instanceid,price):
    url = 'https://market.csgo.com/api/ProcessOrder/'+str(classid)+'/'+str(instanceid)+'/'+str(price)+'/?key=' + secret
    requests.get(url)
    #logger.info(response.json()["success"])


def get_id_class(name):
    url = 'https://market.csgo.com/api/SearchItemByName/'+ name +'/?key=' + secret

    classid = requests.get(url)
    try:
        if classid.raise_for_status() == None:
            classid = classid.json()
            logger.info(classid["success"])
            class_id = classid
            ls = []
            if class_id["success"]==True:
                for i in range(0,len(class_id["list"])):
                    a = []
                    instanceid =  class_id["list"][i]["i_instanceid"]
                    classid = class_id["list"][i]["i_classid"]
                    a.append(classid)
                    a.append(instanceid)
                    ls.append(a)
        return ls
    except:
        ls = []
        time.sleep(2)
        return ls
#get_id_class('Fiery Soul of the Slayer')
'''
filename = 'mylist.json'
myfile = open(filename, mode='r', encoding='utf-8')
lines = myfile.read().split(',')'''

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


def letsgou(name1):
    market_name = name1[0]
    print(market_name)
    av_price = name1[1]
    info = get_id_class(market_name)
    if len(info) > 0:

        for i in range(0, len(info)):
            classid = info[i][0]
            instanceid = info[i][1]


            answer = BestBuyOffer(classid, instanceid)

            if answer != 'er':

                price = int(answer) + 1
                pricedol = price / 100 * 0.015
                av_dol = float(av_price) * 0.88

                if toFixed(pricedol,2) < toFixed(av_dol,2):


                    if pricedol < (float(av_price) * 0.7):
                        price = int((float(av_price) * 0.7) / 0.015 * 100)
                        ProcessOrder(classid, instanceid, price)
                        print(1)
                        print("--- %s seconds ---" % (time.time() - start_time))
                    else:
                        ProcessOrder(classid, instanceid, price)

                        print("--- %s seconds ---" % (time.time() - start_time))


def list():
    filename = 'AVERAGE.json'
    myfile = open(filename, mode='r', encoding='utf-8')
    AVERAGE = json.loads(myfile.read())
    bal = balance()

    for item in range(0, len(AVERAGE)):


        market_name = AVERAGE[item]["market_hash_name"]
        if AVERAGE[item]["recent_sales_info"] != None:
            av_price = AVERAGE[item]["recent_sales_info"]["average_price"]
            if float(av_price) <= (float(bal) / 100 * 0.015):
                if float(av_price) > 0:
                    a = []
                    a.append(market_name)
                    a.append(av_price)
                    list1.append(a)
    print(list1)

#start(1)

if __name__ == '__main__':
    get_data_price(730)
    balance()
    list()
    while True:
        try:

            pool = Pool()
            pool.map(letsgou, list1)
            pool.close()
            pool.join()
        finally:  # To make sure processes are closed in the end, even if errors happen
            pool.close()
            pool.join()
