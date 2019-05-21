import random
from itertools import cycle

import requests
from lxml.html import fromstring

'''
This function will help to scrape proxies from a website
The return will be set of proxies
'''


def get_proxies():
    try:
        url = 'https://free-proxy-list.net/'
        response = requests.get(url)
        parser = fromstring(response.text)
        proxies = set()
        for i in parser.xpath('//tbody/tr'):
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxies.add(proxy)
        print("Successfully scraped the proxies! Total: ", len(proxies))
        return proxies
    except requests.exceptions as e:
        print("Error Occurred: ", e)


'''
This function will help to check if a proxy works for certain website
@:param url takes a string of the website you want to test
@:returns list of proxies
This function will also create a .txt file with the proxies
'''


def proxy_test(url='http://www.stackoverflow.com'):
    proxy_list = open("proxy_list.txt", "a")
    proxies = get_proxies()
    proxy = list(proxies)
    for i in range(0, len(proxy)):
        # Get a proxy from the pool
        try:
            proxies = {
                'http': 'http://' + proxy[i],
                'https': 'http://' + proxy[i],
            }
            # Create the session and set the proxies.
            s = requests.Session()
            s.proxies = proxies

            # Make the HTTP request through the session.
            # Change the timeout according to your need
            r = s.get(url, timeout=1)

            # Check if the proxy was indeed used (the text should contain the proxy IP).
            if r.status_code == 200:
                proxy_list.write(proxy[i] + "\n")
                print(proxy[i])
        except Exception as e:
            '''
            Most free proxies will often get connection errors. 
            You will have retry the entire request using another proxy to work.
            We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url.
            '''
            print("Proxy: ", proxy[i], "Error: ", e)
    proxy_list.close()
    return proxy


'''
This is just a helping function to get the proxies form the text file
@:returns proxies as list
'''


def proxy_from_file(filename):
    proxies = []
    proxy_list = open(filename, 'r')
    for i in proxy_list:
        i = i.split("\n")[0]
        proxies.append(i)
    print("Got the proxies! Total proxies: ", len(proxies))
    return proxies


def pool_of_proxy():
    proxy_list = proxy_from_file("proxy_list.txt")
    random.shuffle(proxy_list)
    return cycle(proxy_list)


if __name__ == '__main__':
    proxy_test()
