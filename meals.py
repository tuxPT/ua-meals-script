#encoding: utf-8

import os
from lxml import etree
from datetime import datetime
from bs4 import BeautifulSoup, element
import requests


def main():
    get_afuav_meal()
    doc = etree.parse(
        'http://services.web.ua.pt/sas/ementas?date=day&format=xml')
    if datetime.now().hour < 15:
        meal = 'Almoço'
    else:
        meal = 'Jantar'
    for m in get_canteen_meal(doc, meal):
        os.system(
            'notify-send "' + m.attrib['canteen'] + '" "' + format_query_output(m) + '"')


def get_canteen_meal(doc, meal):
    return doc.xpath(
        '//menu[@meal="' + meal + '" and @disabled="0"]')


def format_query_output(menu):
    view = ''
    for i in menu[0]:
        if i.text != None:
            view += i.attrib['name'] + ': ' + i.text + '\n'
    return view


def get_afuav_meal():
    page = requests.get('https://www.facebook.com/AFUAv-1411897009022037/')
    soup = BeautifulSoup(page.content.decode('utf-8', 'ignore'), 'lxml')
    divs = soup.find_all('div', {'class': 'userContent'})
    ignore = ['Boa', 'Bom', 'Hoje', 'Ficamos', 'Ver', '...', '🍽️']
    view = ''
    paragraphs = divs[0].find_all(['p', 'span'])
    for p in paragraphs:
        paragraph = p.contents
        for e in paragraph:
            if not any(sub in e for sub in ignore) and not isinstance(e, element.Tag) and e != ' ':
                view += e.strip() + '\n'
    os.system(
        'notify-send "' + 'AFUAv' + '" "' + view + '"')


main()
