from wikipediaapi import Wikipedia
import requests
from lxml import etree


wiki = Wikipedia('ru')


def parse_page(url):
    url = url
    headers = {'Content-Type': 'text/html', }
    respons = requests.get(url, headers=headers)
    # html = response.text


    # read local html file and set up lxml html parser
    # response = urlopen(html)
    htmlparser = etree.HTMLParser()
    tree = etree.parse(respons)
    return tree.xpath('//*[@id="mw-content-text"]/div[1]/ol[1]')


def find_word(word):
    try:
        page = wiki.page(word)
        if page.exists():
            return page.summary
        else:
            # return 'page not found'
            raise 'page not found'
    except:
        return 'слова нет в wikipedia'


def return_categories(word):
    page = wiki.page(word)
    categories = page.categories
    for title in sorted(categories.keys()):
        # if 'Википедия' not in title:
            print((title, categories[title]))
    # return page.categories


if __name__ == '__main__':
    # word = input('input word: ')
    # print(find_word(word))
    #
    # (return_categories(word))
    print(parse_page('https://ru.wiktionary.org/wiki/аванс'))

