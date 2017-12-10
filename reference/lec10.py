# CIS 192 Spring
# Lecture 7: HTTP Requests and HTML Parsing

# requests
import requests
GOOGLE_URL = 'http://www.google.com'

r = requests.get(GOOGLE_URL)
type(r)
r.text
type(r.text)
type(r.content)
r.encoding
r.headers
r.status_code


# Status codes

CIS192_URL = 'http://cis.upenn.edu/~cis192'

r = requests.get(CIS192_URL)
r.status_code
r = requests.get('{}/junk'.format(CIS192_URL))
r.status_code
r.raise_for_status() # if it fails, raise an error!

# parameterss

docs_search = 'https://docs.python.org/3/search.html'
query = '?q=itertools&check_keywords=yes&area=default'

r1 = requests.get('{}{}'.format(docs_search, query))

query_params = {'q': 'itertools', 'check_keywords': 'yes', 'area': 'default'}
r2 = requests.get(docs_search, params=query_params)
r2.url

r1.status_code
r2.status_code
r1.text == r2.text

import json

# APIs example: Wikipedia

WIKI_URL = 'https://en.wikipedia.org/w/api.php?'
query_params = {'action' : 'query', 'meta' : 'tokens', 'format' :'json'}
r = requests.get(WIKI_URL, params=query_params)
r.text
data = json.loads(r.text)
token = data['query']['tokens']['csrftoken']
rev_id = 456
query_params = {'action' : 'thank', 'revid' : rev_id, 'source' : 'cis192', 'token' : token}
r = requests.post(WIKI_URL, data=query_params)




# POSTing

post_end = 'http://httpbin.org/post'
r = requests.post(post_end, data=dict(zip(range(5), 'abcde')))
r.status_code
print(r.text)

# HTML

my_example = '''<html>
  <p>
    This is the <strong>first</strong> paragraph
    <p> Sub paragraph </p>
  </p>
  <p> This is the <strong>second</strong> paragraph
  </p>
</html>'''

three_sisters = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

# Beautiful Soup

from bs4 import BeautifulSoup

ex_soup = BeautifulSoup(my_example, "lxml")
sis_soup = BeautifulSoup(three_sisters, 'lxml')

ex_soup.html
ex_soup.strong
type(ex_soup.strong)

sis_soup.p['class']
sis_soup.p.attrs

# Text and Navigable String

print(sis_soup.text)
print(sis_soup.p.text)

sis_soup.string
sis_soup.p.string
type(sis_soup.p.string)
type(sis_soup.p.text)

nav_str = sis_soup.p.string
nav_str.split()
nav_str.parent
type(nav_str.parent)
nav_str.parent.parent.parent

# Moving about


def clean_if_str(s):
    if isinstance(s, str):
        return s.strip()
    return s

fst_p = ex_soup.html.p
[clean_if_str(x) for x in fst_p.children]
[clean_if_str(x) for x in fst_p.descendants]
[x.strip() for x in fst_p.strings if x.strip()]
fst_p.parent
fst_p.parent.name
fst_strong = fst_p.strong
fst_strong.previous_sibling
fst_strong.next_sibling
fst_strong.next_sibling.next_sibling
fst_strong.next_sibling.next_sibling.next_sibling
fst_strong.next_sibling.next_sibling.next_sibling.next_sibling

fst_strong.next_element
fst_strong.next_element.next_element
fst_strong.next_element.next_element.next_element
fst_strong.next_element.next_element.next_element.next_element
fst_strong.next_element.next_element.next_element.next_element.next_element.next_element.next_element

# searching
ex_soup.find_all('p')
sis_soup.find_all('a')
# can also use regex
import re
lower = re.compile('[a-z]')
lower_single = re.compile('^[a-z]$')

sis_soup.find_all(lower)
sis_soup.find_all(lower_single)
[t.name for t in sis_soup.find_all(lower_single)]

sis_soup.find(href='http://example.com/elsie')
sis_soup.find(class='sister')
sis_soup.find(class_='sister')

ends_ie = re.compile('.*\w+ie.*')
sis_soup.find_all(text=ends_ie)


def main():
    pass

if __name__ == '__main__':
    main()