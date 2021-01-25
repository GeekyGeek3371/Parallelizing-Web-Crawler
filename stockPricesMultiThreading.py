from threading import Thread
import concurrent.futures
import bs4
import time
import requests
from bs4 import BeautifulSoup

ls = open("companyNames.txt", "r").read().split(",")

t1 = time.perf_counter()

def th(ur):
    url = "https://finance.yahoo.com/quote/" + ur + ".NS"
    r = requests.get(url,timeout=4)
    soup = BeautifulSoup(r.text,"lxml")
    try:
        price = soup.find_all('div',{'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
        print(" the price of " + ur + " is " + price)
    except:
        oi = 0





with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    for u in ls:
        t = executor.submit(th,u)
    
        time.sleep(0.05)


t2 = time.perf_counter()
print(f'Finished in {t2-t1} seconds')





