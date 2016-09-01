# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.utils.encoding import smart_text
from scrapper import *


# Create your views here.
def index(request):

    tag = '儿童文学'

    if tag is not "":
        search_book_by_tag(tag, 6, 10)

    #parse_book_details(get_detail_by_url('https://book.douban.com/subject/1046209/'))

    return HttpResponse("Hello, world. You're at the book index.")
