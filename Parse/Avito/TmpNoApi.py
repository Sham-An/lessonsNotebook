#URL https://habr.com/ru/post/537834/
import json
import requests
import sys
import time
from random import randint
from fake_useragent import UserAgent
#af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir
key = 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir' # ключ, с которым всё работает, не разбирался где его брать, но похоже он статичен, т.к. гуглится на различных форумах
cookie = '__cfduid=da6b6b5b9f01fd022f219ed53ac3935791610912291; sessid=ef757cc130c5cd228be88e869369c654.1610912291; _ga=GA1.2.559434019.1610912292; _gid=GA1.2.381990959.1610912292; _fbp=fb.1.1610912292358.1831979940; u=2oiycodt.1oaavs8.dyu0a4x7fxw0; v=1610912321; buyer_laas_location=641780; buyer_location_id=641780; luri=novosibirsk; buyer_selected_search_radius4=0_general; buyer_local_priority_v2=0; sx=H4sIAAAAAAACAxXLQQqAIBAF0Lv8dYvRLEdvU0MIBU0iKCHePXr71zGfefd1W5RLYick2kSakiB2VETclpf85n19RJMSp4vJOSlM%2F2BMOBDNaigE9taM8QH0oydNVAAAAA%3D%3D; dfp_group=100; _ym_uid=1610912323905107257; _ym_d=1610912323; _ym_visorc_34241905=b; _ym_isad=2; _ym_visorc_419506=w; _ym_visorc_188382=w; __gads=ID=2cff056a4e50a953-22d0341a94b900a6:T=1610912323:S=ALNI_MZMbOe0285QjW7EVvsYtSa-RA_Vpg; f=5.8696cbce96d2947c36b4dd61b04726f1a816010d61a371dda816010d61a371dda816010d61a371dda816010d61a371ddbb0992c943830ce0bb0992c943830ce0bb0992c943830ce0a816010d61a371dd2668c76b1faaa358c08fe24d747f54dc0df103df0c26013a0df103df0c26013a2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b978e38434be2a23fac7b9c4258fe3658d831064c92d93c3903815369ae2d1a81d04dbcad294c152cb0df103df0c26013a20f3d16ad0b1c5462da10fb74cac1eab2da10fb74cac1eab3c02ea8f64acc0bdf0c77052689da50d2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab91e52da22a560f5503c77801b122405c48ab0bfc8423929a6d7a5083cc1669877def5708993e2ca678f1dc04f891d61e35b0929bad7c1ea5dec762b46b6afe81f200c638bc3d18ce60768b50dd5e12c30e37135e8f7c6b64dc9f90003c0354a346b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7acf8b817f3dc0c3f21c1eac53cc61955882da10fb74cac1eab2da10fb74cac1eab5e5aa47e7d07c0f95e1e792141febc9cb841da6c7dc79d0b' \
# Если забанили, то добавьте свои куки, это не боевой код но он делает то, что надо
search = 'suzuki+gsx-r'     # Строка поиска на сайте и ниже параметры выбора города, радиуса разброса цены и т.п.
categoryId = 14
locationId = 641780         # Новосибирск
searchRadius = 200
priceMin = 200000
priceMax = 450000
sort = 'priceDesc'
withImagesOnly = 'true'     # Только с фото
limit_page = 50     # Количество объявлений на странице 50 максимум

def except_error(res): # Эту функцию можно дополнить, например обработку капчи
    print(res.status_code, res.text)
    sys.exit(1)

s = requests.Session()                          # Будем всё делать в рамках одной сессии
# Задаем заголовки:
proxiess = {'http': '79.143.225.152:60517'} #79.143.225.152:60517
UA = UserAgent().random

headers = { 'authority': 'm.avito.ru',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            #'user-agent': UserAgent().random, #'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36',
            #'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36',
            'user-agent': str(UA), #'user-agent': 'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36'
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'ru-RU,ru;q=0.9',}
if cookie:                                      # Добавим куки, если есть внешние куки
    headers['cookie'] = cookie
s.headers.update(headers)                       # Сохраняем заголовки в сессию
#proxiess = {'http': '176.9.75.42:3128'}
#proxiess = {'http': '207.154.231.208:3128'}
#UA = UserAgent().random
s.get('https://m.avito.ru/', proxies = proxiess)#, useragent = UA) #   useragent = str(UA)                 # Делаем запрос на мобильную версию.
url_api_9 = 'https://m.avito.ru/api/9/items'    # Урл первого API, позволяет получить id и url объявлений по заданным фильтрам
                                                # Тут уже видно цену и название объявлений
#uag = useragent.Random()

# Print user agent
#print(f'UAG {uag}')

params = {
    'categoryId': 14,
    'params[30]': 4969,
    'locationId': locationId,
    'searchRadius': searchRadius,
    'priceMin': priceMin,
    'priceMax': priceMax,
    'params[110275]': 426645,
    'sort': sort,
    'withImagesOnly': withImagesOnly,
    'lastStamp': 1610905380,
    'display': 'list',
    'limit': limit_page,
    'query': search,
}
cicle_stop = True       # Переменная для остановки цикла
cikle = 0               # Переменная для перебора страниц с объявлениями
items = []              # Список, куда складываем объявления
params['key'] =  key
while cicle_stop:
    cikle += 1          # Так как страницы начинаются с 1, то сразу же итерируем
    params['page'] = cikle
    print(params)

    res = s.get(url_api_9, params=params, proxies = proxiess)#, useragent = UA) #, useragent = str(UA))
    print(f'PROXIIESS {proxiess}Agent {UA} \n HEADERS {headers}')
    try:
        res = res.json()
        print(f'res= {res}')

    except json.decoder.JSONDecodeError: #{'code': 403, 'error': {'message': 'Доступ с вашего IP-адреса временно ограничен', 'link': 'ru.avito://1/info/ipblock/show'}}
        except_error(res)

 #   if res['status'] != 'ok':
 #           print(res['result'])
 #           sys.exit(1)


    if res['status'] != 'ok':
            print(f'''result = {res['result']}''')
            sys.exit(1)
    if res['status'] == 'ok':
        items_page = int(len(res['result']['items']))

        if items_page > limit_page: # проверка на "snippet"
            items_page = items_page - 1

        for item in res['result']['items']:
            if item['type'] == 'item':
                items.append(item)
        if items_page < limit_page:
            cicle_stop = False
####################################################################
params = {'key': key}
print(f'!!!!! ПОЛУЧИЛИ ИТЕМС {items}')
index = 1
for i in items: # Теперь идем по ябъявлениям:
    ad_id = str(i['value']['id'])
    # url_more_data_1 = 'https://m.avito.ru/api/1/rmp/show/' + ad_id  # more_data_1 = s.get(url_more_data_1, params=params).json() # Тут тоже моного информации, можете посмотреть
    url_more_data_2 = 'https://m.avito.ru/api/15/items/' + ad_id
    more_data_2 = s.get(url_more_data_2, params=params, proxies = {'http': '176.9.119.170:8080'}).json()
    print(f'1.) URL url_more_data_2 {url_more_data_2}',end='\n')
    if not 'error' in more_data_2:
        print(f'2.) more_data_2 = {more_data_2}',end='\n')            # В more_data_2 есть всё, что надо, я вывел на принт наиболее интересные для наглядности:
        #more_data_2 = {'id': 2032588517, 'categoryId': 14, 'locationId': 641780, 'metroId': 2024, 'metroType': 'text', 'districtId': 808, 'sharing': {'fb': 'https://www.avito.ru/novosibirsk/mototsikly_i_mototehnika/suzuki_gsxr_600_k7_2032588517?utm_campaign=fb&utm_medium=item_page_mavnew&utm_source=soc_sharing', 'gp': 'https://www.avito.ru/novosibirsk/mototsikly_i_mototehnika/suzuki_gsxr_600_k7_2032588517?utm_campaign=gp&utm_medium=item_page_mavnew&utm_source=soc_sharing', 'lj': 'https://www.avito.ru/novosibirsk/mototsikly_i_mototehnika/suzuki_gsxr_600_k7_2032588517?utm_campaign=lj&utm_medium=item_page_mavnew&utm_source=soc_sharing', 'mm': 'https://www.avito.ru/novosibirsk/mototsikly_i_mototehnika/suzuki_gsxr_600_k7_2032588517?utm_campaign=mm&utm_medium=item_page_mavnew&utm_source=soc_sharing', 'native': 'https://www.avito.ru/novosibirsk/mototsikly_i_mototehnika/suzuki_gsxr_600_k7_2032588517?utm_campaign=native&utm_medium=item_page_mavnew&utm_source=soc_sharing', 'ok': 'https://www.avito.ru/novosibirsk/mototsikly_i_mototehnika/suzuki_gsxr_600_k7_2032588517?utm_campaign=ok&utm_medium=item_page_mavnew&utm_source=soc_sharing', 'tw': 'https://www.avito.ru/novosibirsk/mototsikly_i_mototehnika/suzuki_gsxr_600_k7_2032588517?utm_campaign=tw&utm_medium=item_page_mavnew&utm_source=soc_sharing', 'vk': 'https://www.avito.ru/novosibirsk/mototsikly_i_mototehnika/suzuki_gsxr_600_k7_2032588517?utm_campaign=vk&utm_medium=item_page_mavnew&utm_source=soc_sharing', 'url': 'https://www.avito.ru/novosibirsk/mototsikly_i_mototehnika/suzuki_gsxr_600_k7_2032588517'}, 'coords': {'lat': 54.9760095778691, 'lng': 82.870258256977}, 'shouldShowMapPreview': True, 'address': 'Новосибирская область, Новосибирск, Степная ул., 45', 'geoReferences': [{'content': 'Площадь Маркса', 'after': ' 1,6 км', 'colors': ['#CD0505']}], 'title': 'Suzuki gsxr 600 K7', 'userType': 'private', 'time': 1625643723,
        ##'description': 'Suzuki GSX-R 600 K7\nГод 2007\nOбъём двигaтеля 600 куб. cм.\nДвигатель 4х тактный\nИспpавeн\nОбщий пpoбeг 32 864 км\nЕcть ПТС\n\nBнeшний вид, oбвecы....\nKрасная подcветка пoд плacтикoм. Hoчью выглядит очень эффектнo. Банкa Китaй ,но звук кpасивый, баccoвитый. Hе звонкий. Ножка тюнинг. Имeeтcя GPS навигатoр. Пpиcылает cмс нa телeфoн с мeстом нaхoждeния мотоциклa. Его поставил первым делом. Дизайнерский пластик. Оригинальный. \nРезина новая( 06.2021).\nМасло новое.\nКолодки тормозные новые.\nПолностью обслужен.\nСел - поехал.\n\nДвигатель и рама....\nДвигатель работает как часты, звук приятный и тихий. Ни каких нареканий нет. Мало менял каждый сезон. Так же перед каждый мезоном делал полную диагностику.\n\nЦепь, звезды, колеса....\nЦепь, звезда состояние отличное. Еще 1-2 сезона точно походят. Цепь смазывал каждые 300-500км. Болоны поз замену. По сути ездить на них можно спокойно, но лучше заменить. Уже на свое усмотрение.\n\nПримечание....\nКоцки по пластику не значительные вообще. Слайдеры протерты. Скользячка была. Слайднеры затащили. Ножки сам красил балончиком, пошерканы. Ручки потерты. Больше замечаний нет. Мот в идеальном состоянии.\n\nЗа мотом ухаживал как за своим ребенком. Любимый и родной аппарат. Мот не отжат. Валит что надо.\nПродую в связи с предпринимательской деятельностью.\nОБМЕН НЕ ИНТЕРЕСУЕТ ВООБЩЕ!!!\nМИНИМАЛЬНЫЙ ТОРГ РЕАЛЬНОМУ ПОКУПАТЕЛЮ!!!\n\nГарантия и условия возврата\nПриезжайте, проверяйте.. Любые проверки на месте. Если вы из другого города, найдите общего знакомого в Новосибирске что бы он все посмотрел и через него была сделка. Я именно так и покупал этот мотоцикл.\nЖелательно предварительно писать в ВАЦАП.', 'advertOptions': [], 'parameters': {'flat': [{'title': 'Вид техники', 'description': 'Мотоциклы'}, {'title': 'Вид мотоцикла', 'description': 'Спортивные'}, {'title': 'Состояние', 'description': 'Б/у'}, {'title': 'Категория', 'description': 'Мотоциклы и мототехника'}], 'groups': []}, 'images': [{'140x105': 'https://63.img.avito.st/image/1/wrBsrra_bllCD75aZI2ImZINaFPSrW_j2A1sXdiVbonbDQ', '100x75': 'https://63.img.avito.st/image/1/wrBsrra_blkSDPpaZI2ImZINaFPSrW_j2A1sXdjFbc3bDQ', '1280x960': 'https://63.img.avito.st/image/1/wrBsrraxbllaGexUZI2ImZINbl3QD2Rb', '640x480': 'https://63.img.avito.st/640x480/9733701663.jpg', '432x324': 'https://63.img.avito.st/image/1/wrBsrraublk6C-ReZI2ImZINbA', '240x180': 'https://63.img.avito.st/image/1/wrBsrra2blk6DoRZZI2ImZINblPS7W-z2A1s'}, {'140x105': 'https://41.img.avito.st/image/1/nGjjqba_MIHNCOCC1_fRQR0KNotdqjE7VwoyhVeSMFFUCg', '100x75': 'https://41.img.avito.st/image/1/nGjjqba_MIGdC6SC1_fRQR0KNotdqjE7VwoyhVfCMxVUCg', '1280x960': 'https://41.img.avito.st/image/1/nGjjqbaxMIHVHrKM1_fRQR0KMIVfCDqD', '640x480': 'https://41.img.avito.st/640x480/9733701441.jpg', '432x324': 'https://41.img.avito.st/image/1/nGjjqbauMIG1DLqG1_fRQR0KMg', '240x180': 'https://41.img.avito.st/image/1/nGjjqba2MIG1CdqB1_fRQR0KMItd6jFrVwoy'}, {'640x480': 'https://49.img.avito.st/640x480/9733701449.jpg', '432x324': 'https://49.img.avito.st/image/1/lL68ILauOFfqhbJQmH7Zl0KDOg', '240x180': 'https://49.img.avito.st/image/1/lL68ILa2OFfqgNJXmH7Zl0KDOF0CYzm9CIM6', '140x105': 'https://49.img.avito.st/image/1/lL68ILa_OFeSgehUmH7Zl0KDPl0CIzntCIM6UwgbOIcLgw', '100x75': 'https://49.img.avito.st/image/1/lL68ILa_OFfCgqxUmH7Zl0KDPl0CIzntCIM6UwhLO8MLgw', '1280x960': 'https://49.img.avito.st/image/1/lL68ILaxOFeKl7pamH7Zl0KDOFMAgTJV'}, {'140x105': 'https://08.img.avito.st/image/1/WYEX87a_9Wg5UiVrKa4UqOlQ82Kp8PTSo1D3bKPI9bigUA', '100x75': 'https://08.img.avito.st/image/1/WYEX87a_9WhpUWFrKa4UqOlQ82Kp8PTSo1D3bKOY9vygUA', '1280x960': 'https://08.img.avito.st/image/1/WYEX87ax9WghRHdlKa4UqOlQ9WyrUv9q', '640x480': 'https://08.img.avito.st/640x480/9733701508.jpg', '432x324': 'https://08.img.avito.st/image/1/WYEX87au9WhBVn9vKa4UqOlQ9w', '240x180': 'https://08.img.avito.st/image/1/WYEX87a29WhBUx9oKa4UqOlQ9WKpsPSCo1D3'}, {'432x324': 'https://63.img.avito.st/image/1/Zj70A7auyteipkDQtF4rFwqgyA', '240x180': 'https://63.img.avito.st/image/1/Zj70A7a2yteioyDXtF4rFwqgyt1KQMs9QKDI', '140x105': 'https://63.img.avito.st/image/1/Zj70A7a_ytfaohrUtF4rFwqgzN1KAMttQKDI00A4ygdDoA', '100x75': 'https://63.img.avito.st/image/1/Zj70A7a_yteKoV7UtF4rFwqgzN1KAMttQKDI00BoyUNDoA', '1280x960': 'https://63.img.avito.st/image/1/Zj70A7axytfCtEjatF4rFwqgytNIosDV', '640x480': 'https://63.img.avito.st/640x480/9733701563.jpg'}, {'1280x960': 'https://48.img.avito.st/image/1/Be0bTraxqQQt-SsJHW5PxOXtqQCn76MG', '640x480': 'https://48.img.avito.st/640x480/9733701848.jpg', '432x324': 'https://48.img.avito.st/image/1/Be0bTrauqQRN6yMDHW5PxOXtqw', '240x180': 'https://48.img.avito.st/image/1/Be0bTra2qQRN7kMEHW5PxOXtqQ6lDajur-2r', '140x105': 'https://48.img.avito.st/image/1/Be0bTra_qQQ173kHHW5PxOXtrw6lTai-r-2rAK91qdSs7Q', '100x75': 'https://48.img.avito.st/image/1/Be0bTra_qQRl7D0HHW5PxOXtrw6lTai-r-2rAK8lqpCs7Q'}, {'240x180': 'https://35.img.avito.st/image/1/8iG7-La2XsjtWLTI09-4CEVbXsIFu18iD1tc', '140x105': 'https://35.img.avito.st/image/1/8iG7-La_XsiVWY7L09-4CEVbWMIF-19yD1tczA_DXhgMWw', '100x75': 'https://35.img.avito.st/image/1/8iG7-La_XsjFWsrL09-4CEVbWMIF-19yD1tczA-TXVwMWw', '1280x960': 'https://35.img.avito.st/image/1/8iG7-LaxXsiNT9zF09-4CEVbXswHWVTK', '640x480': 'https://35.img.avito.st/640x480/9733701935.jpg', '432x324': 'https://35.img.avito.st/image/1/8iG7-LauXsjtXdTP09-4CEVbXA'}, {'640x480': 'https://59.img.avito.st/640x480/9733701559.jpg', '432x324': 'https://59.img.avito.st/image/1/aubiibauxg-0LEwIutQnzxwqxA', '240x180': 'https://59.img.avito.st/image/1/aubiiba2xg-0KSwPutQnzxwqxgVcysflVirE', '140x105': 'https://59.img.avito.st/image/1/aubiiba_xg_MKBYMutQnzxwqwAVcise1VirEC1ayxt9VKg', '100x75': 'https://59.img.avito.st/image/1/aubiiba_xg-cK1IMutQnzxwqwAVcise1VirEC1bixZtVKg', '1280x960': 'https://59.img.avito.st/image/1/aubiibaxxg_UPkQCutQnzxwqxgteKMwN'}, {'640x480': 'https://01.img.avito.st/640x480/9733701801.jpg', '432x324': 'https://01.img.avito.st/image/1/dGjgVbau2IG28FKGhHQ-QR722g', '240x180': 'https://01.img.avito.st/image/1/dGjgVba22IG29TKBhHQ-QR722IteFtlrVPba', '140x105': 'https://01.img.avito.st/image/1/dGjgVba_2IHO9AiChHQ-QR723oteVtk7VPbahVRu2FFX9g', '100x75': 'https://01.img.avito.st/image/1/dGjgVba_2IGe90yChHQ-QR723oteVtk7VPbahVQ-2xVX9g', '1280x960': 'https://01.img.avito.st/image/1/dGjgVbax2IHW4lqMhHQ-QR722IVc9NKD'}, {'100x75': 'https://29.img.avito.st/image/1/GITelra_tG2gNCBu4rZSrSA1smdglbXXajW2aWr9t_lpNQ', '1280x960': 'https://29.img.avito.st/image/1/GITelraxtG3oITZg4rZSrSA1tGliN75v', '640x480': 'https://29.img.avito.st/640x480/9733701829.jpg', '432x324': 'https://29.img.avito.st/image/1/GITelrautG2IMz5q4rZSrSA1tg', '240x180': 'https://29.img.avito.st/image/1/GITelra2tG2INl5t4rZSrSA1tGdg1bWHajW2', '140x105': 'https://29.img.avito.st/image/1/GITelra_tG3wN2Ru4rZSrSA1smdglbXXajW2aWqttL1pNQ'}, {'640x480': 'https://88.img.avito.st/640x480/9733702388.jpg', '432x324': 'https://88.img.avito.st/image/1/KTRmybauhd0wbA_aOOFjHZhqhw', '240x180': 'https://88.img.avito.st/image/1/KTRmyba2hd0waW_dOOFjHZhqhdfYioQ30mqH', '140x105': 'https://88.img.avito.st/image/1/KTRmyba_hd1IaFXeOOFjHZhqg9fYyoRn0mqH2dLyhQ3Rag', '100x75': 'https://88.img.avito.st/image/1/KTRmyba_hd0YaxHeOOFjHZhqg9fYyoRn0mqH2dKihknRag', '1280x960': 'https://88.img.avito.st/image/1/KTRmybaxhd1QfgfQOOFjHZhqhdnaaI_f'}, {'100x75': 'https://56.img.avito.st/image/1/de0bRra_2QRl5E0HfWM_xOXl3w6lRdi-r-XbAK8t2pCs5Q', '1280x960': 'https://56.img.avito.st/image/1/de0bRrax2QQt8VsJfWM_xOXl2QCn59MG', '640x480': 'https://56.img.avito.st/640x480/9733702056.jpg', '432x324': 'https://56.img.avito.st/image/1/de0bRrau2QRN41MDfWM_xOXl2w', '240x180': 'https://56.img.avito.st/image/1/de0bRra22QRN5jMEfWM_xOXl2Q6lBdjur-Xb', '140x105': 'https://56.img.avito.st/image/1/de0bRra_2QQ15wkHfWM_xOXl3w6lRdi-r-XbAK992dSs5Q'}, {'640x480': 'https://85.img.avito.st/640x480/9733702085.jpg', '432x324': 'https://85.img.avito.st/image/1/GISelrautG3IMz5qorJSrWA1tg', '240x180': 'https://85.img.avito.st/image/1/GISelra2tG3INl5torJSrWA1tGcg1bWHKjW2', '140x105': 'https://85.img.avito.st/image/1/GISelra_tG2wN2RuorJSrWA1smcglbXXKjW2aSqttL0pNQ', '100x75': 'https://85.img.avito.st/image/1/GISelra_tG3gNCBuorJSrWA1smcglbXXKjW2aSr9t_kpNQ', '1280x960': 'https://85.img.avito.st/image/1/GISelraxtG2oITZgorJSrWA1tGkiN75v'}, {'240x180': 'https://61.img.avito.st/image/1/zGjgXba2YIG2_YqB9HaGQR7-YIteHmFrVP5i', '140x105': 'https://61.img.avito.st/image/1/zGjgXba_YIHO_LCC9HaGQR7-ZoteXmE7VP5ihVRmYFFX_g', '100x75': 'https://61.img.avito.st/image/1/zGjgXba_YIGe__SC9HaGQR7-ZoteXmE7VP5ihVQ2YxVX_g', '1280x960': 'https://61.img.avito.st/image/1/zGjgXbaxYIHW6uKM9HaGQR7-YIVc_GqD', '640x480': 'https://61.img.avito.st/640x480/9733702161.jpg', '432x324': 'https://61.img.avito.st/image/1/zGjgXbauYIG2-OqG9HaGQR7-Yg'}, {'640x480': 'https://22.img.avito.st/640x480/9733702222.jpg', '432x324': 'https://22.img.avito.st/image/1/k1xCubauP7UUHLWyaJPZdbwaPQ', '240x180': 'https://22.img.avito.st/image/1/k1xCuba2P7UUGdW1aJPZdbwaP7_8-j5f9ho9', '140x105': 'https://22.img.avito.st/image/1/k1xCuba_P7VsGO-2aJPZdbwaOb_8uj4P9ho9sfaCP2X1Gg', '100x75': 'https://22.img.avito.st/image/1/k1xCuba_P7U8G6u2aJPZdbwaOb_8uj4P9ho9sfbSPCH1Gg', '1280x960': 'https://22.img.avito.st/image/1/k1xCubaxP7V0Dr24aJPZdbwaP7H-GDW3'}], 'price': {'title': 'Цена', 'value': '350\xa0000', 'value_signed': '350\xa0000 ₽', 'metric': '₽'}, 'seller': {'title': 'Частное лицо', 'name': 'Евгений', 'registrationTime': 1295180824, 'connection': {'title': 'Подтверждён', 'sources': [{'type': 'phone'}, {'type': 'email'}]}, 'link': 'ru.avito://1/user/profile?userKey=701e37a8c8d43cc77b43dcfc39279853&context=H4sIAAAAAAAAA0u0MrKqLgYSSpkpStaZVkYGxkamFhamhubWxVbGVkrFRclKQJYJUL4kNVfJuhYAmCNA2jEAAAA', 'images': {'192x192': 'https://08.img.avito.st/avatar/social/192x192/4689137708.jpg', '256x256': 'https://08.img.avito.st/avatar/social/256x256/4689137708.jpg', '1024x1024': 'https://08.img.avito.st/avatar/social/1024x1024/4689137708.jpg', '64x64': 'https://08.img.avito.st/avatar/social/64x64/4689137708.jpg', '96x96': 'https://08.img.avito.st/avatar/social/96x96/4689137708.jpg', '128x128': 'https://08.img.avito.st/avatar/social/128x128/4689137708.jpg'}, 'summary': '7 объявлений', 'postfix': 'Частное лицо', 'userHashId': '1930898', 'online': False, 'isVerified': False, 'subscribeInfo': {'isSubscribed': False}, 'userHash': '701e37a8c8d43cc77b43dcfc39279853'}, 'video': {'videoUrl': 'https://www.youtube.com/embed/7_OJR-xpdes', 'videoImages': {'1280x960': 'https://85.img.avito.st/video/1280x960/9733706885.jpg', '640x480': 'https://85.img.avito.st/video/640x480/9733706885.jpg', '432x324': 'https://85.img.avito.st/image/1/WN7cy7au7jeKbn4w4LoS9yJo9g', '240x180': 'https://85.img.avito.st/image/1/WN7cy7a27jeKax434LoS9yJo9D1iiPXdaGj2', '140x105': 'https://85.img.avito.st/video/140x105/9733706885.jpg', '100x75': 'https://85.img.avito.st/image/1/WN7cy7au7jeiaWA04LoS9yJo9g'}}, 'stats': {'views': {'today': 14, 'total': 1836}}, 'contacts': {'list': [{'type': 'phone', 'value': {'title': 'Позвонить', 'uri': 'ru.avito://1/phone/get?itemId=2032588517'}}, {'type': 'messenger', 'value': {'title': 'Написать', 'uri': 'ru.avito://1/item/channel/create?itemId=2032588517'}}]}, 'firebaseParams': {'itemID': '2032588517', 'itemPrice': '350000', 'withDelivery': '0', 'vid_tekhniki': 'Мотоциклы', 'condition': 'Б/у', 'vid_mototsikla': 'Спортивные', 'userAuth': '0', 'isShop': '0', 'isASDClient': '0', 'vertical': 'AUTO', 'categoryId': '14', 'categorySlug': 'mototsikly_i_mototehnika', 'microCategoryId': '3727', 'locationId': '641780'}, 'needToCheckCreditInfo': True, 'adjustParams': {'categoryId': '14', 'vertical': 'AUTO', 'microCategoryId': '3727'}, 'needToCheckSimilarItems': True, 'seo': {'title': 'Suzuki gsxr 600 K7 купить в\xa0Новосибирске | Транспорт | Авито', 'description': '<Suzuki gsxr 600 K7>: объявление о\xa0продаже в <Новосибирске> на\xa0Авито. Suzuki GSX-R 600 K7 Год 2007 Объём двигателя 600 куб. см. Двигатель 4х тактный Исправен Общий пробег 32 864 км\xa0Есть ПТС Внешний вид, обвесы.... Красная подсветка под пластиком. Ночью выглядит очень эффектно. Банка Китай ,но звук красивый, бассовитый. Не\xa0звонкий. Ножка тюнинг. Имеется GPS навигатор. Присылает смс на\xa0телефон с\xa0местом нахождения мотоцикла. Его поставил первым делом. Дизайнерский пластик. Оригинальный. Резина новая( 06.2021). Масло новое. Колодки тормозные новые. Полностью обслужен. Сел - поехал. Двигатель и\xa0рам...', 'canonicalUrl': 'https://www.avito.ru/novosibirsk/mototsikly_i_mototehnika/suzuki_gsxr_600_k7_2032588517'}, 'customerValue': 1.3, 'breadcrumbs': [{'name': 'Мотоциклы и мототехника', 'title': 'Мотоциклы и мототехника в Новосибирске', 'url': '/novosibirsk/mototsikly_i_mototehnika', 'deeplink': 'ru.avito://1/items/search?categoryId=14&locationId=641780'}, {'name': 'Мотоциклы', 'title': 'Мотоциклы', 'url': '/novosibirsk/mototsikly_i_mototehnika/mototsikly-ASgBAgICAUQ80k0', 'deeplink': 'ru.avito://1/items/search?params%5B30%5D=4969&categoryId=14&locationId=641780'}, {'name': 'Спортивные', 'title': 'Спортивные', 'url': '/novosibirsk/mototsikly_i_mototehnika/mototsikly/sportivnye-ASgBAgICAkQ80k2~B9gB', 'deeplink': 'ru.avito://1/items/search?params%5B30%5D=4969&params%5B479%5D=108&categoryId=14&locationId=641780'}], 'viewItemAndBuyerEventsParams': {'item_id': '2032588517', 'item_location_id': 'Transport', 'logcat': 'Moto'}}

        print(f'''3.) title {more_data_2['title']}''',end='\n')
        #time.sleep(randint(6,14))

        time.sleep((randint(6,14)) if index % 10 != 0 else 20)
        index += 1
        print(f'''4.) price {more_data_2['price']}   Addres ''')
        print(f'''5.) PPrice2 {more_data_2['price']['value']}  ''')
        print(f'''6.) Addres {more_data_2['address']}''')
        url_get_phone = 'https://m.avito.ru/api/1/items/' + ad_id + '/phone'    # URL для получения телефона
        phone = s.get(url_get_phone, params=params).json()                      # Сам запрос
        if phone['status'] == 'ok': phone_number = requests.utils.unquote(phone['result']['action']['uri'].split('number=')[1]) # Прверка на наличие телефона, такой странный синтсксис, чтоб уместиться в 100 сторочек кода)))
        else: phone_number = phone['result']['message']
        print(f'7.) телефон {phone_number}')
        print(f'''8.) seller {more_data_2['seller']}''')
        print(f'''9.) Name {more_data_2['seller']['name']}''')
        print(f'''10.) registrationTime {more_data_2['seller']['registrationTime']}''')
        #connection пропускаю пока
        print(f'''11.) link {more_data_2['seller']['link']}''')


        print(f'''12.) description {more_data_2['description']}''') # Скрыл, т.к. много букв
        print('=======================================================\n')