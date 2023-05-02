import zipfile
from io import BytesIO, StringIO
from IPython.display import display

import pandas as pd
import requests
import hashlib
import fsspec

url = 'https://flibusta.site/catalog/catalog.zip'

md5hash_current = ''

r = requests.get(url)
print(r.status_code)

#md5hash_current = hashlib.md5(r.content).hexdigest()
#print(md5hash_current)

zipDocument = zipfile.ZipFile(BytesIO(r.content))
file = zipDocument.open('catalog.txt').read().decode('utf-8')

df = pd.read_csv(StringIO(file), delimiter=';', on_bad_lines='skip')

#print(df.head(20))
#print(df.info())

author = 'азимов'
book_name = ''

#search_string = ['foo', 'baz']
#search_string = 'Красный кефир'.split()
search_string = 'красный кефир'

display(search_string)

df_result = df[df['Title'].str.contains(search_string, na=False, case=False)]

display(df_result.head(10))
