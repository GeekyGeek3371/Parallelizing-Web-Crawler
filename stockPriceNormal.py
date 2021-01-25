
import bs4
import time
import requests
from bs4 import BeautifulSoup

ls = open("companyNames.txt", "r").read().split(",")

t1 = time.perf_counter()

def th(ur):
    url = "https://finance.yahoo.com/quote/" + ur + ".NS"
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"lxml")
    price = 0
    try:
        price = soup.find_all('div',{'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
        print(" the price of " + ur + " is " + price)
    except:
        oi = 0



for u in ls:
    th(u)


t2 = time.perf_counter()

print(f'Finished in {t2-t1} seconds')
