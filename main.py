import time
import requests
from requests import RequestException
from lxml import etree
from twilio.rest import Client
import Email


def call():
    # Register on 'www.twilio.com' to get account sid&token
    account_sid = 'xxx'
    auth_token = 'xxx'
    client = Client(account_sid, auth_token)
    call = client.calls.create(
            url='http://demo.twilio.com/docs/voice.xml',
            to='Your Phone Number',
            from_='Your Virtual Phone Number'
        )
    print('Outgoing Call!')


def getproxy():
    pass


def methodGet(url, params=None, proxy=True, redo=30, headers=None):

    if proxy:
        proxies = getproxy()
    else:
        proxies = None
    if not headers:
        headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36' \
                            '(KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    for i in range(redo):
        try:
            t = requests.get(url, timeout=30, params=params, proxies=proxies, headers=headers)
            state = t.status_code
            # print(state, t.url)
            if state in [400, 403, 500]:
                headers['Proxy-Switch-Ip'] = "yes"
                time.sleep(0.1)
                continue
            if state == 429:
                time.sleep(0.5)
                continue
            if 399 < state < 500:
                print(state)
                return None
            t.raise_for_status()
            t.close()
        except RequestException as e:
            time.sleep(2)
            print(e)
        else:
            return t.content.decode('utf-8')
    print(url)
    return None


def parse_url(url):
    resp = methodGet(url)
    html = etree.HTML(resp)
    text = html.xpath("//div[@class='availabilityMessageProduct_29UPa']//span[2]/text()")[0]
    return text


def main():
    url_list = ['https://www.bestbuy.ca/en-ca/product/nintendo-switch-console-with-neon-red-blue-joy-con/13817625',
                'https://www.bestbuy.ca/en-ca/product/nintendo-switch-console-with-grey-joy-con/13817626']

    attempts = 1

    while True:
        status_list = []
        for url in url_list:
            status = parse_url(url)
            status_list.append(status)
        print(f'Attempt Number:{attempts}')
        print(status_list)
        attempts += 1
        if 'Available online' in status_list:
            call()
            Email.email()
            break

        time.sleep(1)


if __name__ == '__main__':
    main()