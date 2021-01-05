# Парсинг сайта и запись данных в excel книгу

from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook

# Генерация списка ссылок на страницы каталога магазина
urls = []
for i in range(1, 10):
    urls.append(f'https://digitik.ru/catalog/kompyuternaya_tekhnika/monitory/?PAGEN_1={i}')

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko)'
                  'Chrome/87.0.4280.88 Mobile Safari/537.36'
}


# Функция записывает в файл html-код страницы по ссылке
def get_page(url):
    req = requests.get(url, headers=headers)
    with open('monitors.html', 'w', encoding='utf-8') as f:
        f.write(req.text)


j = 2
i = 1
# Создание книги
wb = Workbook()
dest_filename = 'data.xlsx'
# ws1 принимает аткивный лист таблицы
ws1 = wb.active
# Установка названия листа
ws1.title = "data"
data = {'Название': [], 'Цена': [], 'Артикул': []}
# Перебираем все страницы
for z in urls:
    # Записываем текущую страницу в файл
    get_page(z)
    with open('monitors.html', 'r', encoding='utf-8') as file:
        src = file.read()
    # Создаём конструктур bs
    soup = BeautifulSoup(src, 'lxml')
    # Парсим страницу и результат сохраняем в data
    cards = soup.find_all('div', class_='catalog_item main_item_wrapper item_wrap')
    for card in cards:
        data['Название'].append(card.find('div', 'item-title').text.strip('\n'))
        data['Цена'].append(card.find('div', class_='price').get('data-value') + ' Pуб')
        data['Артикул'].append(card.find('div', class_='article_block').text.lstrip('\n').lstrip('\t').rstrip('\t')[8:])

# Записываем заголовки в таблицу
keys = []
for x in data.keys():
    keys.append(x)
ws1.append(keys)
# Записываем остальные данные из словаря
for x in range(len(data['Название']) - 1):
    ws1[j][0].value = data['Название'][i]
    ws1[j][1].value = data['Цена'][i]
    ws1[j][2].value = data['Артикул'][i]
    j += 1
    i += 1
# Сохраняем и закрываем таблицу
wb.save(filename=dest_filename)
wb.close()
