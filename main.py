import requests
import lxml
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from nott import NotificationManager
import pandas as pd

def sendsms (sms) :
    ME = "+905343936779"
    notification_manager = NotificationManager()
    m2 = sms
    notification_manager.send_sms(m2, number=ME)

suitableDays = {}
fasms = ''
def checkmonth (rmonth,destination,currency,depar):
    global suitableDays
    global fasms
    fasms = ''
    suitableDays = {}
    options = webdriver.ChromeOptions()
    # options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    # options.headless= True
    # options.add_argument('window-size=0x0')
    # options.add_argument('--disable-gpu')
    dev  = webdriver.Chrome(options=options)
    print("fetching site...")
    # dev.minimize_window()
    dev.get(
        f"https://web.flypgs.com/flexible-search?adultCount=1&arrivalPort={destination}&currency={currency}&departureDate=2022-{rmonth}-22&departurePort={depar}&language=en")

    print('getting month data ... ')
    monthes = dev.find_elements(By.CLASS_NAME, "flexible-search-slider-date")
    pricess = dev.find_elements(By.CLASS_NAME, "flexible-search-slider-amount")
    topmonths = [month.text for month in monthes if not month.text == '']
    bestprices = [price.text for price in pricess if not price.text == '']
    fasms += f'This month ({topmonths[1]}) best price :{bestprices[1]}\n'
    print(f'This month ({topmonths[1]}) best price :{bestprices[1]} ')
    day = dev.find_elements(By.CLASS_NAME, 'day')
    ind = 0
    start = False
    days = []
    print('findig best price days...')
    ind = 0
    for dayy in day :
        if dayy.text == '1' :
            start = True
        if start :
            if ind > 10 :
                if not dayy.text == '':
                    if ind-1 < int(dayy.text) :
                        days.append(dayy.text)
                        ind+=1
            else :
                if not dayy.text == '':
                    days.append(dayy.text)
                    ind +=1
    prices = dev.find_elements(By.CLASS_NAME, "amount")
    price_list = [price.text for price in prices if not price.text=='']
    # print(f'len of prices : {len(price_list)} ,,,\n len of days : {len(days)} ,,,  ')
    holder = 0
    chartdict = {}
    for da in days:
        chartdict[da]=price_list[holder]
        holder+=1
    # print(chartdict)
    MonthBestPrice = int(bestprices[1].split()[0].split('.')[0])

    for day in chartdict :
        if int(chartdict[day]) <= MonthBestPrice +5 :
            suitableDays[f'{day}/{rmonth}/2022'] = int(chartdict[day])
    dev.close()
monthsli = ['01','02','03','04','05','06','07','08','09','10','11','12']
iata = pd.read_excel('data.xlsx').values.tolist()
iatalist = [code[0] for code in iata]
curs = ['USD' , 'GPB' , 'TRY' , 'EUR' , 'AED ', 'CHF' , 'DKK' , 'KGS'  ,'KWD', 'NOK' , 'PKR','SAR','SEK','USD']
# print(iatalist)
depar = input('Enter departure Airport ...')
while not depar.upper() in iatalist:
    depar = input('we dont go there , chose other departure Airport ...')
destination = input('Enter destination Airport ...')
while not destination.upper() in iatalist:
    destination = input('we dont go there , chose other destination Airport ...')
currency = input('Enter currency Code ...')
while not currency.upper() in curs:
    print(f'we dont accept that , try one of :\n{curs}')
    currency = input('Enter currency Code ...')
rmonth = input('Enter Month like : 01 or 12 ...')
while not rmonth.upper() in monthsli:
    rmonth = input(f'Enter Month like : {monthsli}  ...')
checkmonth(rmonth,destination,currency,depar)

fasms += f'Best days to fly from {depar} to {destination}  :\n'
for  day in suitableDays :
    fasms += f'{day} for : {suitableDays[day]} {currency}\n'
print(fasms)
sendsms(fasms)
print(f"Getting Next Month : 0{int(rmonth) + 1} information , please wait..")
rmonth =f'0{int(rmonth) + 1}'
time.sleep(5)
checkmonth(rmonth,destination,currency,depar)
fasms += f'Best days to fly from {depar} to {destination} in {rmonth}/2022 is :\n'
print(f'Next Month Best days to fly to {destination} is : ')
for  day in suitableDays :
    fasms += f'{day} for : {suitableDays[day]} {currency}\n'
    print(f'{day} for : {suitableDays[day]} {currency}')
sendsms(fasms)
