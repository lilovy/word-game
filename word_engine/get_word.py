import requests

# Import the etree module from the lxml library.
from lxml import etree

# Import StringIO class from the io package.
from io import StringIO


def parse_html_url_link(page_url):
    # Create an instance of etree.HTMLParser class.
    html_parser = etree.HTMLParser()

    # Use the python requests module get method to get the web page object with the provided url.
    web_page = requests.get(page_url)

    # Convert the web page bytes content to text string withe the decode method.
    web_page_html_string = web_page.content.decode("utf-8")

    # Create a StringIO object with the above web page html string.
    str_io_obj = StringIO(web_page_html_string)
    # print(web_page_html_string)

    # Create an etree object.
    dom_tree = etree.parse(str_io_obj, parser=html_parser)

    # Get all <a href...> tag elements in a list
    a_tag_list = dom_tree.xpath("""//*[@id="Морфологические_и_синтаксические_свойства"]""")

    # Loop in the html a tag list
    for a in a_tag_list:
        # Get each a tag href attribute value, the value save the a tag URL link.
        url = a.get('href')

        # Print out the parsed out URL.
        print(url)


def ps():
    from lxml import html
    import requests

    # Request the page
    page = requests.get('https://ru.wiktionary.org/wiki/аванс')
    # print(page)

    # Parsing the page
    # (We need to use page.content rather than
    # page.text because html.fromstring implicitly
    # expects bytes as input.)
    tree = html.fromstring(page.content)
    print(tree)

    # Get element using XPath
    buyers = tree.xpath('//*[@id="mw-content-text"]/div[1]/ol[1]/li[1]')
    print(buyers)

if __name__ == '__main__':
    # parse_html_url_link('https://ru.wiktionary.org/wiki/аванс')
    ps()