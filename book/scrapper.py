# -*- coding: UTF-8 -*-

import sys
import argparse
import time
import urllib
import urllib2
from random import randint
from bs4 import BeautifulSoup
from models import *

reload(sys)
sys.setdefaultencoding('utf8')

# Some User Agents
hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}, \
       {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'}, \
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]



def search_book_by_name(name):
    html_text = ""
    page_num = 0

    # url = "https://book.douban.com/subject_search?search_text=%E8%A7%A3%E5%BF%A7"
    url = "https://book.douban.com/subject_search?search_text=" + urllib.quote(name.encode('utf8'))

    try:
        req = urllib2.Request(url, headers=hds[page_num % len(hds)])
        source_code = urllib2.urlopen(req).read()
        html_text = str(source_code)
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e

    return html_text


def search_book_on_z(name):
    html_text = ""
    page_num = 0

    # https://www.amazon.cn/s/ref=nb_sb_noss?__mk_zh_CN=亚马逊网站&url=search-alias%3Daps&field-keywords=活着
    url = "https://www.amazon.cn/s/ref=nb_sb_noss?__mk_zh_CN=亚马逊网站&url=search-alias%3Daps&field-keywords=" + urllib.quote(name.encode('utf8'))

    try:
        req = urllib2.Request(url, headers=hds[page_num % len(hds)])
        source_code = urllib2.urlopen(req).read()
        html_text = str(source_code)
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e

    return html_text


def search_book_on_j(name):
    html_text = ""
    page_num = 0

    # http://search.jd.com/Search?keyword=%E9%B2%81%E8%BF%85&enc=utf-8
    url = "http://search.jd.com/Search?keyword=%s&enc=utf-8" % urllib.quote(name.encode('utf8'))

    try:
        req = urllib2.Request(url, headers=hds[page_num % len(hds)])
        source_code = urllib2.urlopen(req).read()
        html_text = str(source_code)
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e

    return html_text


# pages <= 1000 / 20 = 50, otherwise douban will return no result
def search_book_by_tag(tag, start=1, end=50):
    # https://book.douban.com/tag/%E5%84%BF%E7%AB%A5%E6%96%87%E5%AD%A6
    # https://book.douban.com/tag/%E5%84%BF%E7%AB%A5%E6%96%87%E5%AD%A6?start=40&type=T
    # 40 is the page number, T means "综合排序"
    pages_limitation = 50
    number_per_page = 20

    if end > pages_limitation:
        end = pages_limitation

    page_counter = start

    while page_counter <= end:
        page_num = number_per_page * (page_counter - 1)
        url = "https://book.douban.com/tag/%s?start=%d&type=T" % (urllib.quote(tag), page_num)

        try:
            req = urllib2.Request(url, headers=hds[page_num % len(hds)])
            source_code = urllib2.urlopen(req).read()
            html_text = str(source_code)
            page_counter += 1

            urls = parse_book_urls(html_text, number_per_page)

            if urls is not None:
                for url in urls:
                    print url
                    time.sleep(randint(0, 9))
                    book = parse_book_details(get_detail_by_url(url))
                    print book['title']

        except (urllib2.HTTPError, urllib2.URLError), e:
            print e

    return "OK"


def parse_book_urls(html_text, counter=1):
    urls = []
    tmp_counter = 0

    soup = BeautifulSoup(html_text, "html.parser")
    list_soup = soup.find('ul', {'class': 'subject-list'})

    if list_soup is not None:
        for book_info in list_soup.findAll('li'):
            tmp_counter += 1
            if tmp_counter > counter:
                break
            book_url = book_info.find('a', {'class': 'nbg'}).get('href')
            urls.append(book_url)

    return urls


def get_detail_by_url(url):
    # https://book.douban.com/subject/1433640/
    page_num = 0
    html_text = ""

    try:
        req = urllib2.Request(url, headers=hds[page_num % len(hds)])
        source_code = urllib2.urlopen(req).read()
        html_text = str(source_code)
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e

    return html_text


def parse_book_details(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    book_html = soup.find('div', {'id': 'wrapper'})
    title = book_html.find('h1').find('span').text.strip()

    list_details = book_html.find(id='info').find_all('span', {'class': 'pl'})

    book = {}

    book['title'] = title

    book['description'] = ""
    if list_details is not None:
        for item in list_details:
            if item.nextSibling.nextSibling.has_attr('href'):
                book['description'] = book['description'] + item.string.strip().strip(':') + \
                                      ":" + item.nextSibling.nextSibling.string.strip() + ";"
            else:
                book['description'] = book['description'] + item.string.strip().strip(':') + \
                                      ":" + item.nextSibling.string.strip() + ";"

    book['rating'] = ""
    rating_html = book_html.find('strong', {'class': 'rating_num'})
    if rating_html is not None:
        book['rating'] = rating_html.string.strip()

    book['rating_people'] = ""
    rating_people_html = book_html.find('a', {'class': 'rating_people'})
    if rating_people_html is not None:
        book['rating_people'] = rating_people_html.find('span').string.strip()

    book['introduction'] = ""
    intros_html = book_html.find(id='link-report')
    if intros_html is not None:
        intros = intros_html.find('div', {'class': 'intro'}).find_all('p')
        if intros is not None:
            for intro in intros:
                if intro is not None:
                    print intro
                    book['introduction'] = book['introduction'] + intro.text

    obj, created = Book.objects.get_or_create(
        title=book['title'],
        description=book['description'],
        rating=book['rating'],
        rating_people=book['rating_people'],
        introduction=book['introduction'],
    )

    return book


def parse_book_sale_on_z(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    book_list = soup.find(id='atfResults').find('ul').find_all('li')
    if book_list is not None and len(book_list) > 0:
        book = book_list[0]
        title = book.find('h2', {'class': 's-access-title'}).text
        price = book.find('span', {'class': 's-price'}).text
    print title, price
    return price


def parse_book_sale_on_j(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    book_list = soup.find(id='J_goodsList').find('ul').find_all('li')
    if book_list is not None and len(book_list) > 0:
        book = book_list[0]
        title = book.find('div', {'class': 'p-name'}).find('font', {'class': 'skcolor_ljg'}).text
        price = book.find('div', {'class': 'p-price'}).find('i').text
    print title, price
    return price


def get_args():
    parser = argparse.ArgumentParser(description='Douban Spider.')
    parser.add_argument('-n', '--name', type=str, default="计算机", help='Add a name which you are interested in.')
    parser.add_argument('-t', '--tag', type=str, default="计算机", help='Add a tag which you are interested in.')
    parser.add_argument('-s', '--spider', action='store_true', help='Spider all.')
    args = parser.parse_args()
    name = args.name
    tag = args.tag
    spider = args.spider
    return name, tag, spider


if __name__ == '__main__':
    name, tag, spider = get_args()
    '''
    if tag is not "":
        urls = parse_book_urls(search_book_by_tag(tag))
        if urls is not None:
            for url in urls:
                book = parse_book_details(get_detail_by_url(url))
                print book['title']
                parse_book_sale_on_z(search_book_on_z(book['title']))
                parse_book_sale_on_j(search_book_on_j(book['title']))
    '''
    if name is not None:
        urls = parse_book_urls(search_book_by_name(name))

        if urls is not None:
            for url in urls:
                book = parse_book_details(get_detail_by_url(url))
                print book['title']
                #parse_book_sale_on_z(search_book_on_z(book['title']))
                #parse_book_sale_on_j(search_book_on_j(book['title']))
