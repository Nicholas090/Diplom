import requests
from bs4 import BeautifulSoup as BS

def parse_price(url, default='0'):
    r = requests.get(url)
    soup = BS(r.text, 'lxml')
    quotes = soup.find_all('div', class_='b-pmi-col-left')
    result_price = False

    for el in quotes:
        if el:
            res = el.find(class_='b-price')
        if res:
            result_price = res.text[:-4]

    if result_price :
        print(result_price)
        return result_price

    if result_price == False:
        print('We have problem in parse or product is out of stock')
        return default



# parse_price('https://telemart.ua/products/intel-core-i5-12600k-3449ghz-s1700-tray/')

# def result_sum(*links):
#     res = 0
#     for el in links:
#       res += int((parse_price(el)).replace(' ', ''))
#     print(type(res))
#     print(res)
#     return res


# result_sum('https://telemart.ua/products/intel-core-i5-12600k-3449ghz-s1700-tray/', 'https://telemart.ua/products/asus-tuf-gaming-gt501-rgb-bez-bp-90dc0012-b49000-black/', 'https://telemart.ua/products/1stplayer-v3-a-4g6-bez-bp-black/')