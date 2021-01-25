import requests
from bs4 import BeautifulSoup
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
import time

class MultiThreadScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.root_url = '{}://{}'.format(urlparse(self.base_url).scheme, urlparse(self.base_url).netloc)
        self.pool = ThreadPoolExecutor(max_workers=10)
        self.scraped_pages = set([])                    #already scrapped pages
        self.to_crawl = Queue()                         #frontier queue
        self.to_crawl.put(self.base_url)
    def parse_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            url = link['href']
            if url.startswith('/') or url.startswith(self.root_url):
                url = urljoin(self.root_url, url)
                if url not in self.scraped_pages:
                    self.to_crawl.put(url)
    def scrape_info(self, html):
        return
    def post_scrape_callback(self, res):
        result = res.result()
        if result and result.status_code == 200:
            self.parse_links(result.text)
            self.scrape_info(result.text)
    def scrape_page(self, url):
        try:
            res = requests.get(url, timeout=(3, 10))
            return res
        except requests.RequestException:
            return
    def run_scraper(self):
        x = 0
        while x<500:
            try:
                target_url = self.to_crawl.get(timeout=10)
                if target_url not in self.scraped_pages:
                    x = x + 1
                    print(x,end=" ")
                    print("Scraping URL: {}".format(target_url))
                    self.scraped_pages.add(target_url)
                    job = self.pool.submit(self.scrape_page, target_url)
                    job.add_done_callback(self.post_scrape_callback)
            
            except Empty:
                return
            except Exception as e:
                print(e)
                continue


if __name__ == '__main__':
    t1 = time.perf_counter()
    s = MultiThreadScraper("https://finance.yahoo.com/")
    s.run_scraper()
    t2 = time.perf_counter()
    print(f'Finished in {t2-t1} seconds')