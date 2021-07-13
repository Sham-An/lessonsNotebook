import requests
import random
import time
from bs4 import BeautifulSoup as bs

################
#Следующая функция принимает список прокси и создает сеанс запросов, который случайным образом выбирает один из переданных прокси:
def get_session(proxies):
    # создать HTTP‑сеанс
    session = requests.Session()
    # выбираем один случайный прокси
    proxy = random.choice(proxies)
    session.proxies = {"http": proxy, "https": proxy}
    return session


def get_free_proxies():
    url = "https://free-proxy-list.net/"
    # получаем ответ HTTP и создаем объект soup
    soup = bs(requests.get(url).content, "html.parser")
    proxies = []
    for row in soup.find("table", attrs={"id": "proxylisttable"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            proxies.append(host)
        except IndexError:
            continue
    return proxies
free_proxies = get_free_proxies()
print(f'Обнаружено бесплатных прокси - {len(free_proxies)}:')
for i in range(len(free_proxies)):
    print(f"{i+1}) {free_proxies[i]}")


# #Следующая функция принимает список прокси и создает сеанс запросов, который случайным образом выбирает один из переданных прокси:
# def get_session(proxies):
#     # создать HTTP‑сеанс
#     session = requests.Session()
#     # выбираем один случайный прокси
#     proxy = random.choice(proxies)
#     session.proxies = {"http": proxy, "https": proxy}
#     return session
#
# #Проверим отправив запрос на веб‑сайт, который возвращает наш IP‑адрес:
# for i in range(5):
#     s = get_session(proxies)
#     try:
#         print("Страница запроса с IP:", s.get("http://icanhazip.com", timeout=1.5).text.strip())
#     except Exception as e:
#         continue
#

#Проверим отправив запрос на веб‑сайт, который возвращает наш IP‑адрес:
#proxiess=get_session(free_proxies)
for i in range(5):
    s = get_session(free_proxies)
#    time.sleep(3)
    try:
        print("Страница запроса с IP:", s.get("http://icanhazip.com", timeout=1.5).text.strip())
    except Exception as e:
        continue

for i in range(30):
    s = get_session(free_proxies)
    time.sleep(3)
    try:
        print(f"Страница {i} запроса с IP:", s.get("http://icanhazip.com", timeout=1.5).text.strip())
    except Exception as e:
        continue

################