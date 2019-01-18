#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from lxml import etree, html
from datetime import datetime
import requests


def main():
    now = datetime.now().hour
    get_afuav_meal(now)
    if now < 15 or now > 21:
        meal = 'Almoço'
    else:
        meal = 'Jantar'
    # shows canteens notifications
    for m in get_canteen_meal(meal):
        os.system(
            'notify-send "' + m.attrib['canteen'] + '" "' + format_query_output(m) + '"')


def get_canteen_meal(meal):
    f = requests.get(
        'http://services.web.ua.pt/sas/ementas?date=day&format=xml', headers={'Connection':'close'})
    doc = etree.fromstring(f.content)
    # returns only opened canteens
    return doc.xpath(
        '//menu[@meal="' + meal + '" and @disabled="0"]')


def format_query_output(menu):
    view = ''
    for i in menu[0]:
        if i.text != None:
            view += i.attrib['name'] + ': ' + i.text + '\n'
    return view


def get_afuav_meal(hour):
    f = requests.get('https://www.facebook.com/AFUAv-1411897009022037/', headers={'Connection':'close'})
    # parsing to etree from html string
    doc = html.fromstring(f.content)
    # filter by post
    posts = doc.xpath('//div[contains(@class, "userContentWrapper")]')
    ignore = ['Boa', 'Bom', 'Hoje', 'Ficamos', 'Ver', '...', '🍽️']
    for p in posts:
        # converts utc timestamp to datetime object
        t = datetime.utcfromtimestamp(int(p.xpath('.//@data-utime')[0]))
        view = None
        if hour >= t.hour and ((t.hour in [11, 12] and hour < 14) or (t.hour in [18, 19] and hour < 22)):
            show = True
        else:
            show = False
        if show:
            view = ''
            # get all text in the post
            meal = p.xpath(
                './/div[@class="text_exposed_root"]//*[self::p or self::span]/text()')
            for m in meal:
                # only show dishes
                if not any(sub in m for sub in ignore) and m != ' ':
                    view += m.strip() + '\n'
            # shows the notification
            os.system(
                'notify-send "' + 'AFUAv' + '" "' + view + '"')
            break
        else:
            continue


main()
