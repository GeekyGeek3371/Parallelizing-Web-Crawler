import concurrent.futures
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from queue import Queue
import pybloomfilter

ls = open("companyNames.txt", "r").read().split(",")

t1 = time.perf_counter()

def th(ur):
    url = "https://finance.yahoo.com/quote/" + ur + ".NS"
    try:
        r = requests.get(url,timeout=6)
        soup = BeautifulSoup(r.text,"lxml")
        price = soup.find_all('div',{'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
        print(" the price of " + ur + " is " + price)
    except:
        oi=0
    

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    for u in ls:
        t = executor.submit(th,u)
   
        # time.sleep(0.05)
   
  

t2 = time.perf_counter()
print("*****-----******")
print(f'Finished in {t2-t1} seconds')
print("*****-----******")

t1 = time.perf_counter()

scraped_pages= pybloomfilter.BloomFilter(100000,0.05,'pages')
to_crawl = Queue()

def start(url): 
    
    source_code = requests.get(url).text 
    soup = BeautifulSoup(source_code, 'html.parser') 
    links = soup.find_all('a', href=True)
    for link in links:
        each_text = link['href']
        if each_text.startswith('/') or each_text.startswith(root_url):
            each_text = urljoin(root_url, each_text)
            if not scraped_pages.__contains__(each_text):
                to_crawl.put(each_text)
                scraped_pages.add(url)
                
                  
root_url = "https://finance.yahoo.com/"
to_crawl.put(root_url)

x=0

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    while x<500:
        target_url = to_crawl.get()

        if not scraped_pages.__contains__(target_url):
            print(x,end=" ")
            print("url = "+ target_url)
            t = executor.submit(start,target_url)
            # time.sleep(0.05)
            x = x+1
        
    t2 = time.perf_counter()
    print("*****-----******")
    print(f'Finished in {t2-t1} seconds')

    


