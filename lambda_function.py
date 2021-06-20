import json
import queue
import requests
import threading
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse



def lambda_handler(event, context):
    # 1. Parse out query string params

    input_url = event['queryStringParameters']['input_url']
    # transactionType = event['queryStringParameters']['type']
    # transactionAmount = event['queryStringParameters']['amount']

    # print('transactionId=' + transactionId)
    # print('transactionType=' + transactionType)
    # print('transactionAmount=' + transactionAmount)

    # 2. Construct the body of the response object
    # transactionResponse = {}
    # transactionResponse['input_url'] = transactionId
    transactionResponse = {'output_list': tesla(input_url)}



    # transactionResponse['message'] = 'Hello from Lambda land'

    # 3. Construct http response object - Final commit
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(transactionResponse)

    # 4. Return the response object
    return responseObject



def brute_search(q, urls, seen):
    while True:
        try:
            url, level = q.get()
        except queue.Empty:
            continue

        if level <= 0:
            break

        try:
            soup = BeautifulSoup(requests.get(url).text, "lxml")

            for x in soup.find_all("a", href=True):

                link = x["href"]
                parsed = urlparse(link)

                if bool(parsed.netloc) and bool(parsed.scheme):

                    if link and link[0] in "#/":
                        link = url + link[1:]

                    if link not in seen:
                        seen.add(link)
                        urls.append(link)
                        q.put((link, level - 1))

        except (requests.exceptions.ConnectionError):
            pass


def tesla(input_url):
    # config = ConfigParser()
    # config.read('config.ini')
    depth = 1
    workers = 15
    given_url = input_url
    seen = set()
    urls = []
    threads = []
    q = queue.Queue()

    q.put((given_url, depth))

    start = time.time()

    for _ in range(workers):
        t = threading.Thread(target=brute_search, args=(q, urls, seen))
        threads.append(t)
        t.daemon = True
        t.start()

    for thread in threads:
        thread.join()

    return urls
