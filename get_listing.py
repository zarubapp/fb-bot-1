import zipfile
from io import BytesIO, StringIO
from IPython.display import display

import pandas as pd
import requests
import hashlib
import fsspec
import re

url = 'https://flibusta.site/catalog/catalog.zip'

fb2_url = 'https://flibusta.is/b/{book_ID}/fb2'
epub_url = 'https://flibusta.is/b/{book_ID}/epub'
mobi_url = 'https://flibusta.is/b/{book_ID}/mobi'

md5hash_current = ''

#В переменной указываем получить новый каталог онлайн или работать с файлом с диска
GetNewCatalog = False

if GetNewCatalog:
    fileCatalog = open('data/catalog.zip', 'wb')
    # скчаивание файла
    r = requests.get(url)

    fileCatalog.write(r.content)
    fileCatalog.close()
    print("Get new catalog success")

# Распаковка каталога
zipDocument = zipfile.ZipFile('data/catalog.zip')

# извлекаем файл с каталогом библиотеки
file = zipDocument.open('catalog.txt').read().decode('utf-8')

df = pd.read_csv(StringIO(file), delimiter=';', on_bad_lines='skip')

#author = 'Гёте'
#book_name = 'фауст'

author = input('Введите автора: ')
book_name = input('Название книги: ')
#print(df.info())

# Search by author
# для упрощения поиска переводим в UPPER CASE

df['Last Name UPPER'] = df['Last Name'].str.upper()
df['Middle Name UPPER'] = df['Middle Name'].str.upper()
df['First Name UPPER'] = df['First Name'].str.upper()

# Разделяем поисковую строку на отдельные слова и переводим в UPPER CASE
search_string = author.upper().split()
display(search_string)

# поиск по только полному совпадению. Подумать как снять это ограничение
df_result = df

#проходим последовательно циклом по всему каталогу и оставлям только записи удовлетворяющие словам из поисковой строки
for x in search_string:
    df_result = df_result[(df_result['Last Name UPPER'] == x)
                          | (df_result['Middle Name UPPER'] == x)
                          | (df_result['First Name UPPER'] == x)]

# search book by Title
if book_name != '':
    search_string = book_name.upper().split()
    display(search_string)

    for x in search_string:
        df_result = df_result[df_result['Title'].str.contains(x, na=False, case=False, flags=re.IGNORECASE)]


df_result.to_csv('result/result.csv', index=False)
display(df_result[['Title', 'ID']])

#display(df_result)
#print(df_result)
