#!/usr/bin/env python
# -*-coding:utf-8 -*-
#
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------
# File          : read_epub.py
# Author        : BMV System Integration Pvt Ltd.
# Version       : 1.0.0
# Date          : 24th January 2023
# Contact       : info@systemintegration.in
# Purpose       : This is the python script read the .epub file and get the content of the chapters from it.
# import        : ebooklib - to read the .epub file.
#                 bs4      - to get the text from html content of the .epub chapters.
#----------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------

from ebooklib import epub
import ebooklib
from bs4 import BeautifulSoup

def value(r):
    if (r == 'I'):
        return 1
    if (r == 'V'):
        return 5
    if (r == 'X'):
        return 10
    if (r == 'L'):
        return 50
    if (r == 'C'):
        return 100
    if (r == 'D'):
        return 500
    if (r == 'M'):
        return 1000
    return -1
 
def romanToDecimal(str):
    res = 0
    i = 0
 
    while (i < len(str)):
 
        s1 = value(str[i])
        if (i + 1 < len(str)):
            s2 = value(str[i + 1])
            if (s1 >= s2):
                res = res + s1
                i = i + 1
            else:
                res = res + s2 - s1
                i = i + 2
        else:
            res = res + s1
            i = i + 1
 
    return res

def book_to_chapters(book_to_read):
    book = epub.read_epub(book_to_read)
    items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    chapters = []
    chapters_dict = {}
    for item in items:
        if item.is_chapter():
            chapters.append(item)
    for chap in chapters:
        soup = BeautifulSoup(chap.get_content(), 'html.parser')
        chap_no = [para.get_text() for para in soup.find_all('h3')]
        
        if len(chap_no) > 0:
            chap_no = str(chap_no[0]).split(' ')
            if len(chap_no) >= 3:
                chap_name = ' '.join(chap_no[2:])
                chap_no = romanToDecimal(str(chap_no[1]).replace('.', '').replace('1',''))
                text = [para.get_text() for para in soup.find_all('p', attrs={'class' : 'left'})]

                chapters_dict[chap_no] = {"name" : chap_name, "content" : ''.join(text)}
    return chapters_dict
