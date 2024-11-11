import re
import time
from datetime import datetime
from api_paper import judging_criteria, paper_queue_success, paper_queue_fail, paper_queue_delay, upload_file_by_url, \
    judge_bm_repeat, judging_bm_criteria
import mysql.connector
import requests
from lxml import etree


paper = "华夏早报"
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'ASPSESSIONIDQQADCTQC=INDDMJCDHHKOBFKLNPJPFOKN; ASPSESSIONIDSQBCBTRC=EOHJOPJDMAPCPDMKJNCDIGAB; _d_id=777e02cd871a3fa77809b749782e79',
    'Pragma': 'no-cache',
    'Referer': 'http://epaper.cmnpnews.com/index.asp?Nid=366',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

date_dict = {'2017-07-01': 'http://epaper.cmnpnews.com/index.asp?Nid=37', '2017-10-01': 'http://epaper.cmnpnews.com/index.asp?Nid=38', '2018-01-01': 'http://epaper.cmnpnews.com/index.asp?Nid=39', '2018-04-01': 'http://epaper.cmnpnews.com/index.asp?Nid=40', '2018-05-11': 'http://epaper.cmnpnews.com/index.asp?Nid=41', '2018-05-18': 'http://epaper.cmnpnews.com/index.asp?Nid=42', '2018-05-25': 'http://epaper.cmnpnews.com/index.asp?Nid=43', '2018-06-01': 'http://epaper.cmnpnews.com/index.asp?Nid=44', '2018-06-08': 'http://epaper.cmnpnews.com/index.asp?Nid=45', '2018-06-15': 'http://epaper.cmnpnews.com/index.asp?Nid=46', '2018-06-22': 'http://epaper.cmnpnews.com/index.asp?Nid=47', '2018-06-29': 'http://epaper.cmnpnews.com/index.asp?Nid=48', '2018-07-06': 'http://epaper.cmnpnews.com/index.asp?Nid=49', '2018-07-13': 'http://epaper.cmnpnews.com/index.asp?Nid=50', '2018-07-20': 'http://epaper.cmnpnews.com/index.asp?Nid=51', '2018-07-27': 'http://epaper.cmnpnews.com/index.asp?Nid=52', '2018-08-03': 'http://epaper.cmnpnews.com/index.asp?Nid=53', '2018-08-10': 'http://epaper.cmnpnews.com/index.asp?Nid=54', '2018-08-17': 'http://epaper.cmnpnews.com/index.asp?Nid=55', '2018-08-24': 'http://epaper.cmnpnews.com/index.asp?Nid=56', '2018-08-31': 'http://epaper.cmnpnews.com/index.asp?Nid=57', '2018-09-07': 'http://epaper.cmnpnews.com/index.asp?Nid=58', '2018-09-14': 'http://epaper.cmnpnews.com/index.asp?Nid=59', '2018-09-21': 'http://epaper.cmnpnews.com/index.asp?Nid=60', '2018-09-28': 'http://epaper.cmnpnews.com/index.asp?Nid=61', '2018-10-05': 'http://epaper.cmnpnews.com/index.asp?Nid=62', '2018-10-12': 'http://epaper.cmnpnews.com/index.asp?Nid=63', '2018-10-19': 'http://epaper.cmnpnews.com/index.asp?Nid=64', '2018-10-26': 'http://epaper.cmnpnews.com/index.asp?Nid=65', '2018-11-02': 'http://epaper.cmnpnews.com/index.asp?Nid=66', '2018-11-09': 'http://epaper.cmnpnews.com/index.asp?Nid=67', '2018-11-16': 'http://epaper.cmnpnews.com/index.asp?Nid=68', '2018-11-23': 'http://epaper.cmnpnews.com/index.asp?Nid=69', '2018-11-30': 'http://epaper.cmnpnews.com/index.asp?Nid=70', '2018-12-21': 'http://epaper.cmnpnews.com/index.asp?Nid=71', '2018-12-28': 'http://epaper.cmnpnews.com/index.asp?Nid=72', '2019-01-04': 'http://epaper.cmnpnews.com/index.asp?Nid=73', '2019-01-11': 'http://epaper.cmnpnews.com/index.asp?Nid=74', '2019-01-18': 'http://epaper.cmnpnews.com/index.asp?Nid=75', '2019-01-25': 'http://epaper.cmnpnews.com/index.asp?Nid=76', '2019-02-01': 'http://epaper.cmnpnews.com/index.asp?Nid=77', '2019-02-08': 'http://epaper.cmnpnews.com/index.asp?Nid=78', '2019-02-15': 'http://epaper.cmnpnews.com/index.asp?Nid=79', '2019-02-22': 'http://epaper.cmnpnews.com/index.asp?Nid=80', '2019-03-01': 'http://epaper.cmnpnews.com/index.asp?Nid=81', '2019-03-08': 'http://epaper.cmnpnews.com/index.asp?Nid=82', '2019-03-15': 'http://epaper.cmnpnews.com/index.asp?Nid=83', '2019-03-22': 'http://epaper.cmnpnews.com/index.asp?Nid=84', '2019-03-29': 'http://epaper.cmnpnews.com/index.asp?Nid=85', '2019-04-05': 'http://epaper.cmnpnews.com/index.asp?Nid=86', '2019-04-12': 'http://epaper.cmnpnews.com/index.asp?Nid=87', '2019-04-19': 'http://epaper.cmnpnews.com/index.asp?Nid=88', '2019-04-26': 'http://epaper.cmnpnews.com/index.asp?Nid=89', '2019-05-03': 'http://epaper.cmnpnews.com/index.asp?Nid=90', '2019-05-10': 'http://epaper.cmnpnews.com/index.asp?Nid=91', '2019-05-17': 'http://epaper.cmnpnews.com/index.asp?Nid=92', '2019-05-24': 'http://epaper.cmnpnews.com/index.asp?Nid=93', '2019-05-31': 'http://epaper.cmnpnews.com/index.asp?Nid=94', '2019-06-07': 'http://epaper.cmnpnews.com/index.asp?Nid=95', '2019-06-14': 'http://epaper.cmnpnews.com/index.asp?Nid=96', '2019-06-21': 'http://epaper.cmnpnews.com/index.asp?Nid=97', '2019-06-28': 'http://epaper.cmnpnews.com/index.asp?Nid=98', '2019-07-05': 'http://epaper.cmnpnews.com/index.asp?Nid=99', '2019-07-12': 'http://epaper.cmnpnews.com/index.asp?Nid=100', '2019-07-19': 'http://epaper.cmnpnews.com/index.asp?Nid=101', '2019-07-26': 'http://epaper.cmnpnews.com/index.asp?Nid=102', '2019-08-02': 'http://epaper.cmnpnews.com/index.asp?Nid=103', '2019-08-09': 'http://epaper.cmnpnews.com/index.asp?Nid=104', '2019-08-16': 'http://epaper.cmnpnews.com/index.asp?Nid=105', '2019-08-23': 'http://epaper.cmnpnews.com/index.asp?Nid=106', '2019-08-30': 'http://epaper.cmnpnews.com/index.asp?Nid=107', '2019-09-06': 'http://epaper.cmnpnews.com/index.asp?Nid=108', '2019-09-13': 'http://epaper.cmnpnews.com/index.asp?Nid=109', '2019-09-20': 'http://epaper.cmnpnews.com/index.asp?Nid=110', '2019-09-27': 'http://epaper.cmnpnews.com/index.asp?Nid=111', '2019-10-04': 'http://epaper.cmnpnews.com/index.asp?Nid=112', '2019-10-11': 'http://epaper.cmnpnews.com/index.asp?Nid=113', '2019-10-18': 'http://epaper.cmnpnews.com/index.asp?Nid=114', '2019-10-25': 'http://epaper.cmnpnews.com/index.asp?Nid=115', '2019-11-01': 'http://epaper.cmnpnews.com/index.asp?Nid=116', '2019-11-08': 'http://epaper.cmnpnews.com/index.asp?Nid=117', '2019-11-15': 'http://epaper.cmnpnews.com/index.asp?Nid=118', '2019-11-22': 'http://epaper.cmnpnews.com/index.asp?Nid=119', '2019-11-29': 'http://epaper.cmnpnews.com/index.asp?Nid=120', '2019-12-06': 'http://epaper.cmnpnews.com/index.asp?Nid=121', '2019-12-13': 'http://epaper.cmnpnews.com/index.asp?Nid=122', '2019-12-20': 'http://epaper.cmnpnews.com/index.asp?Nid=123', '2019-12-27': 'http://epaper.cmnpnews.com/index.asp?Nid=124', '2020-01-03': 'http://epaper.cmnpnews.com/index.asp?Nid=125', '2020-01-10': 'http://epaper.cmnpnews.com/index.asp?Nid=126', '2020-01-17': 'http://epaper.cmnpnews.com/index.asp?Nid=127', '2020-01-24': 'http://epaper.cmnpnews.com/index.asp?Nid=128', '2020-01-31': 'http://epaper.cmnpnews.com/index.asp?Nid=129', '2020-02-07': 'http://epaper.cmnpnews.com/index.asp?Nid=130', '2020-02-14': 'http://epaper.cmnpnews.com/index.asp?Nid=131', '2020-02-21': 'http://epaper.cmnpnews.com/index.asp?Nid=132', '2020-02-28': 'http://epaper.cmnpnews.com/index.asp?Nid=133', '2020-03-06': 'http://epaper.cmnpnews.com/index.asp?Nid=134', '2020-03-13': 'http://epaper.cmnpnews.com/index.asp?Nid=135', '2020-03-20': 'http://epaper.cmnpnews.com/index.asp?Nid=136', '2020-03-27': 'http://epaper.cmnpnews.com/index.asp?Nid=137', '2020-04-03': 'http://epaper.cmnpnews.com/index.asp?Nid=138', '2020-04-10': 'http://epaper.cmnpnews.com/index.asp?Nid=139', '2020-04-17': 'http://epaper.cmnpnews.com/index.asp?Nid=140', '2020-04-24': 'http://epaper.cmnpnews.com/index.asp?Nid=141', '2020-05-01': 'http://epaper.cmnpnews.com/index.asp?Nid=142', '2020-05-08': 'http://epaper.cmnpnews.com/index.asp?Nid=143', '2020-05-15': 'http://epaper.cmnpnews.com/index.asp?Nid=144', '2020-05-22': 'http://epaper.cmnpnews.com/index.asp?Nid=145', '2020-05-29': 'http://epaper.cmnpnews.com/index.asp?Nid=146', '2020-06-05': 'http://epaper.cmnpnews.com/index.asp?Nid=147', '2020-06-12': 'http://epaper.cmnpnews.com/index.asp?Nid=148', '2020-06-19': 'http://epaper.cmnpnews.com/index.asp?Nid=149', '2020-06-26': 'http://epaper.cmnpnews.com/index.asp?Nid=150', '2020-07-03': 'http://epaper.cmnpnews.com/index.asp?Nid=151', '2020-07-10': 'http://epaper.cmnpnews.com/index.asp?Nid=152', '2020-07-17': 'http://epaper.cmnpnews.com/index.asp?Nid=153', '2020-07-24': 'http://epaper.cmnpnews.com/index.asp?Nid=154', '2020-07-31': 'http://epaper.cmnpnews.com/index.asp?Nid=156', '2020-08-07': 'http://epaper.cmnpnews.com/index.asp?Nid=157', '2020-08-14': 'http://epaper.cmnpnews.com/index.asp?Nid=158', '2020-08-21': 'http://epaper.cmnpnews.com/index.asp?Nid=159', '2020-08-28': 'http://epaper.cmnpnews.com/index.asp?Nid=160', '2020-09-04': 'http://epaper.cmnpnews.com/index.asp?Nid=161', '2020-09-11': 'http://epaper.cmnpnews.com/index.asp?Nid=162', '2020-09-18': 'http://epaper.cmnpnews.com/index.asp?Nid=163', '2020-09-25': 'http://epaper.cmnpnews.com/index.asp?Nid=164', '2020-10-02': 'http://epaper.cmnpnews.com/index.asp?Nid=165', '2020-10-09': 'http://epaper.cmnpnews.com/index.asp?Nid=166', '2020-10-16': 'http://epaper.cmnpnews.com/index.asp?Nid=167', '2020-10-23': 'http://epaper.cmnpnews.com/index.asp?Nid=168', '2020-10-30': 'http://epaper.cmnpnews.com/index.asp?Nid=169', '2020-11-06': 'http://epaper.cmnpnews.com/index.asp?Nid=170', '2020-11-13': 'http://epaper.cmnpnews.com/index.asp?Nid=171', '2020-11-20': 'http://epaper.cmnpnews.com/index.asp?Nid=172', '2020-11-27': 'http://epaper.cmnpnews.com/index.asp?Nid=173', '2020-12-04': 'http://epaper.cmnpnews.com/index.asp?Nid=174', '2020-12-11': 'http://epaper.cmnpnews.com/index.asp?Nid=175', '2020-12-18': 'http://epaper.cmnpnews.com/index.asp?Nid=176', '2020-12-25': 'http://epaper.cmnpnews.com/index.asp?Nid=177', '2021-01-01': 'http://epaper.cmnpnews.com/index.asp?Nid=178', '2021-01-08': 'http://epaper.cmnpnews.com/index.asp?Nid=179', '2021-01-15': 'http://epaper.cmnpnews.com/index.asp?Nid=180', '2021-01-22': 'http://epaper.cmnpnews.com/index.asp?Nid=181', '2021-01-29': 'http://epaper.cmnpnews.com/index.asp?Nid=182', '2021-02-05': 'http://epaper.cmnpnews.com/index.asp?Nid=183', '2021-02-12': 'http://epaper.cmnpnews.com/index.asp?Nid=184', '2021-02-19': 'http://epaper.cmnpnews.com/index.asp?Nid=185', '2021-02-26': 'http://epaper.cmnpnews.com/index.asp?Nid=186', '2021-03-05': 'http://epaper.cmnpnews.com/index.asp?Nid=187', '2021-03-12': 'http://epaper.cmnpnews.com/index.asp?Nid=188', '2021-03-19': 'http://epaper.cmnpnews.com/index.asp?Nid=189', '2021-03-26': 'http://epaper.cmnpnews.com/index.asp?Nid=190', '2021-04-02': 'http://epaper.cmnpnews.com/index.asp?Nid=191', '2021-04-09': 'http://epaper.cmnpnews.com/index.asp?Nid=192', '2021-04-16': 'http://epaper.cmnpnews.com/index.asp?Nid=193', '2021-04-23': 'http://epaper.cmnpnews.com/index.asp?Nid=194', '2021-04-30': 'http://epaper.cmnpnews.com/index.asp?Nid=195', '2021-05-07': 'http://epaper.cmnpnews.com/index.asp?Nid=196', '2021-05-14': 'http://epaper.cmnpnews.com/index.asp?Nid=197', '2021-05-21': 'http://epaper.cmnpnews.com/index.asp?Nid=198', '2021-05-28': 'http://epaper.cmnpnews.com/index.asp?Nid=199', '2021-06-04': 'http://epaper.cmnpnews.com/index.asp?Nid=200', '2021-06-11': 'http://epaper.cmnpnews.com/index.asp?Nid=201', '2021-06-18': 'http://epaper.cmnpnews.com/index.asp?Nid=202', '2021-06-25': 'http://epaper.cmnpnews.com/index.asp?Nid=203', '2021-07-02': 'http://epaper.cmnpnews.com/index.asp?Nid=204', '2021-07-09': 'http://epaper.cmnpnews.com/index.asp?Nid=205', '2021-07-16': 'http://epaper.cmnpnews.com/index.asp?Nid=206', '2021-07-23': 'http://epaper.cmnpnews.com/index.asp?Nid=207', '2021-07-30': 'http://epaper.cmnpnews.com/index.asp?Nid=208', '2021-08-06': 'http://epaper.cmnpnews.com/index.asp?Nid=209', '2021-08-13': 'http://epaper.cmnpnews.com/index.asp?Nid=210', '2021-08-20': 'http://epaper.cmnpnews.com/index.asp?Nid=211', '2021-08-27': 'http://epaper.cmnpnews.com/index.asp?Nid=212', '2021-09-03': 'http://epaper.cmnpnews.com/index.asp?Nid=213', '2021-09-10': 'http://epaper.cmnpnews.com/index.asp?Nid=214', '2021-09-17': 'http://epaper.cmnpnews.com/index.asp?Nid=215', '2021-09-24': 'http://epaper.cmnpnews.com/index.asp?Nid=216', '2021-10-01': 'http://epaper.cmnpnews.com/index.asp?Nid=217', '2021-10-08': 'http://epaper.cmnpnews.com/index.asp?Nid=218', '2021-10-15': 'http://epaper.cmnpnews.com/index.asp?Nid=219', '2021-10-22': 'http://epaper.cmnpnews.com/index.asp?Nid=220', '2021-10-29': 'http://epaper.cmnpnews.com/index.asp?Nid=221', '2021-11-05': 'http://epaper.cmnpnews.com/index.asp?Nid=222', '2021-11-12': 'http://epaper.cmnpnews.com/index.asp?Nid=223', '2021-11-19': 'http://epaper.cmnpnews.com/index.asp?Nid=224', '2021-11-26': 'http://epaper.cmnpnews.com/index.asp?Nid=225', '2021-12-03': 'http://epaper.cmnpnews.com/index.asp?Nid=226', '2021-12-10': 'http://epaper.cmnpnews.com/index.asp?Nid=227', '2021-12-17': 'http://epaper.cmnpnews.com/index.asp?Nid=228', '2021-12-24': 'http://epaper.cmnpnews.com/index.asp?Nid=229', '2021-12-31': 'http://epaper.cmnpnews.com/index.asp?Nid=230', '2022-01-07': 'http://epaper.cmnpnews.com/index.asp?Nid=231', '2022-01-14': 'http://epaper.cmnpnews.com/index.asp?Nid=232', '2022-01-21': 'http://epaper.cmnpnews.com/index.asp?Nid=233', '2022-01-28': 'http://epaper.cmnpnews.com/index.asp?Nid=234', '2022-02-04': 'http://epaper.cmnpnews.com/index.asp?Nid=235', '2022-02-11': 'http://epaper.cmnpnews.com/index.asp?Nid=236', '2022-02-18': 'http://epaper.cmnpnews.com/index.asp?Nid=237', '2022-02-25': 'http://epaper.cmnpnews.com/index.asp?Nid=238', '2022-03-04': 'http://epaper.cmnpnews.com/index.asp?Nid=239', '2022-03-11': 'http://epaper.cmnpnews.com/index.asp?Nid=240', '2022-03-18': 'http://epaper.cmnpnews.com/index.asp?Nid=241', '2022-03-25': 'http://epaper.cmnpnews.com/index.asp?Nid=242', '2022-04-01': 'http://epaper.cmnpnews.com/index.asp?Nid=243', '2022-04-08': 'http://epaper.cmnpnews.com/index.asp?Nid=244', '2022-04-15': 'http://epaper.cmnpnews.com/index.asp?Nid=245', '2022-04-22': 'http://epaper.cmnpnews.com/index.asp?Nid=246', '2022-04-29': 'http://epaper.cmnpnews.com/index.asp?Nid=247', '2022-05-06': 'http://epaper.cmnpnews.com/index.asp?Nid=248', '2022-05-13': 'http://epaper.cmnpnews.com/index.asp?Nid=249', '2022-05-20': 'http://epaper.cmnpnews.com/index.asp?Nid=250', '2022-05-27': 'http://epaper.cmnpnews.com/index.asp?Nid=251', '2022-06-03': 'http://epaper.cmnpnews.com/index.asp?Nid=252', '2022-06-10': 'http://epaper.cmnpnews.com/index.asp?Nid=253', '2022-06-17': 'http://epaper.cmnpnews.com/index.asp?Nid=254', '2022-06-24': 'http://epaper.cmnpnews.com/index.asp?Nid=255', '2022-07-01': 'http://epaper.cmnpnews.com/index.asp?Nid=256', '2022-07-08': 'http://epaper.cmnpnews.com/index.asp?Nid=257', '2022-07-15': 'http://epaper.cmnpnews.com/index.asp?Nid=258', '2022-07-22': 'http://epaper.cmnpnews.com/index.asp?Nid=259', '2022-07-29': 'http://epaper.cmnpnews.com/index.asp?Nid=260', '2022-08-05': 'http://epaper.cmnpnews.com/index.asp?Nid=261', '2022-08-12': 'http://epaper.cmnpnews.com/index.asp?Nid=262', '2022-08-19': 'http://epaper.cmnpnews.com/index.asp?Nid=263', '2022-08-26': 'http://epaper.cmnpnews.com/index.asp?Nid=264', '2022-09-02': 'http://epaper.cmnpnews.com/index.asp?Nid=265', '2022-09-09': 'http://epaper.cmnpnews.com/index.asp?Nid=266', '2022-09-16': 'http://epaper.cmnpnews.com/index.asp?Nid=267', '2022-09-23': 'http://epaper.cmnpnews.com/index.asp?Nid=268', '2022-09-30': 'http://epaper.cmnpnews.com/index.asp?Nid=269', '2022-10-07': 'http://epaper.cmnpnews.com/index.asp?Nid=270', '2022-10-14': 'http://epaper.cmnpnews.com/index.asp?Nid=271', '2022-10-21': 'http://epaper.cmnpnews.com/index.asp?Nid=272', '2022-10-28': 'http://epaper.cmnpnews.com/index.asp?Nid=273', '2022-11-04': 'http://epaper.cmnpnews.com/index.asp?Nid=274', '2022-11-11': 'http://epaper.cmnpnews.com/index.asp?Nid=275', '2022-11-18': 'http://epaper.cmnpnews.com/index.asp?Nid=276', '2022-11-25': 'http://epaper.cmnpnews.com/index.asp?Nid=277', '2022-12-02': 'http://epaper.cmnpnews.com/index.asp?Nid=278', '2022-12-09': 'http://epaper.cmnpnews.com/index.asp?Nid=279', '2022-12-16': 'http://epaper.cmnpnews.com/index.asp?Nid=280', '2022-12-23': 'http://epaper.cmnpnews.com/index.asp?Nid=281', '2022-12-30': 'http://epaper.cmnpnews.com/index.asp?Nid=282', '2023-01-06': 'http://epaper.cmnpnews.com/index.asp?Nid=283', '2023-01-13': 'http://epaper.cmnpnews.com/index.asp?Nid=284', '2023-01-20': 'http://epaper.cmnpnews.com/index.asp?Nid=285', '2023-01-27': 'http://epaper.cmnpnews.com/index.asp?Nid=286', '2023-02-03': 'http://epaper.cmnpnews.com/index.asp?Nid=287', '2023-02-10': 'http://epaper.cmnpnews.com/index.asp?Nid=288', '2023-02-17': 'http://epaper.cmnpnews.com/index.asp?Nid=289', '2023-02-24': 'http://epaper.cmnpnews.com/index.asp?Nid=290', '2023-03-03': 'http://epaper.cmnpnews.com/index.asp?Nid=291', '2023-03-10': 'http://epaper.cmnpnews.com/index.asp?Nid=292', '2023-03-17': 'http://epaper.cmnpnews.com/index.asp?Nid=293', '2023-03-24': 'http://epaper.cmnpnews.com/index.asp?Nid=294', '2023-03-31': 'http://epaper.cmnpnews.com/index.asp?Nid=295', '2023-04-07': 'http://epaper.cmnpnews.com/index.asp?Nid=296', '2023-04-14': 'http://epaper.cmnpnews.com/index.asp?Nid=297', '2023-04-21': 'http://epaper.cmnpnews.com/index.asp?Nid=298', '2023-04-28': 'http://epaper.cmnpnews.com/index.asp?Nid=299', '2023-05-05': 'http://epaper.cmnpnews.com/index.asp?Nid=300', '2023-05-12': 'http://epaper.cmnpnews.com/index.asp?Nid=301', '2023-05-19': 'http://epaper.cmnpnews.com/index.asp?Nid=302', '2023-05-26': 'http://epaper.cmnpnews.com/index.asp?Nid=303', '2023-06-02': 'http://epaper.cmnpnews.com/index.asp?Nid=304', '2023-06-09': 'http://epaper.cmnpnews.com/index.asp?Nid=306', '2023-06-16': 'http://epaper.cmnpnews.com/index.asp?Nid=307', '2023-06-23': 'http://epaper.cmnpnews.com/index.asp?Nid=308', '2023-06-30': 'http://epaper.cmnpnews.com/index.asp?Nid=309', '2023-07-07': 'http://epaper.cmnpnews.com/index.asp?Nid=310', '2023-07-14': 'http://epaper.cmnpnews.com/index.asp?Nid=311', '2023-07-21': 'http://epaper.cmnpnews.com/index.asp?Nid=312', '2023-07-28': 'http://epaper.cmnpnews.com/index.asp?Nid=313', '2023-08-04': 'http://epaper.cmnpnews.com/index.asp?Nid=314', '2023-08-11': 'http://epaper.cmnpnews.com/index.asp?Nid=315', '2023-08-18': 'http://epaper.cmnpnews.com/index.asp?Nid=316', '2023-08-25': 'http://epaper.cmnpnews.com/index.asp?Nid=317', '2023-09-01': 'http://epaper.cmnpnews.com/index.asp?Nid=318', '2023-09-08': 'http://epaper.cmnpnews.com/index.asp?Nid=319', '2023-09-15': 'http://epaper.cmnpnews.com/index.asp?Nid=320', '2023-09-22': 'http://epaper.cmnpnews.com/index.asp?Nid=321', '2023-09-29': 'http://epaper.cmnpnews.com/index.asp?Nid=322', '2023-10-06': 'http://epaper.cmnpnews.com/index.asp?Nid=323', '2023-10-13': 'http://epaper.cmnpnews.com/index.asp?Nid=324', '2023-10-20': 'http://epaper.cmnpnews.com/index.asp?Nid=325', '2023-10-27': 'http://epaper.cmnpnews.com/index.asp?Nid=326', '2023-11-03': 'http://epaper.cmnpnews.com/index.asp?Nid=327', '2023-11-10': 'http://epaper.cmnpnews.com/index.asp?Nid=328', '2023-11-17': 'http://epaper.cmnpnews.com/index.asp?Nid=329', '2023-11-24': 'http://epaper.cmnpnews.com/index.asp?Nid=330', '2023-12-01': 'http://epaper.cmnpnews.com/index.asp?Nid=331', '2023-12-08': 'http://epaper.cmnpnews.com/index.asp?Nid=332', '2023-12-15': 'http://epaper.cmnpnews.com/index.asp?Nid=333', '2023-12-22': 'http://epaper.cmnpnews.com/index.asp?Nid=334', '2023-12-29': 'http://epaper.cmnpnews.com/index.asp?Nid=335', '2024-01-05': 'http://epaper.cmnpnews.com/index.asp?Nid=336', '2024-01-12': 'http://epaper.cmnpnews.com/index.asp?Nid=337', '2024-01-19': 'http://epaper.cmnpnews.com/index.asp?Nid=338', '2024-01-26': 'http://epaper.cmnpnews.com/index.asp?Nid=339', '2024-02-02': 'http://epaper.cmnpnews.com/index.asp?Nid=340', '2024-02-09': 'http://epaper.cmnpnews.com/index.asp?Nid=341', '2024-02-16': 'http://epaper.cmnpnews.com/index.asp?Nid=342', '2024-02-23': 'http://epaper.cmnpnews.com/index.asp?Nid=343', '2024-03-01': 'http://epaper.cmnpnews.com/index.asp?Nid=344', '2024-03-08': 'http://epaper.cmnpnews.com/index.asp?Nid=345', '2024-03-15': 'http://epaper.cmnpnews.com/index.asp?Nid=346', '2024-03-22': 'http://epaper.cmnpnews.com/index.asp?Nid=347', '2024-03-29': 'http://epaper.cmnpnews.com/index.asp?Nid=348', '2024-04-05': 'http://epaper.cmnpnews.com/index.asp?Nid=349', '2024-04-12': 'http://epaper.cmnpnews.com/index.asp?Nid=350', '2024-04-19': 'http://epaper.cmnpnews.com/index.asp?Nid=351', '2024-04-26': 'http://epaper.cmnpnews.com/index.asp?Nid=352', '2024-05-03': 'http://epaper.cmnpnews.com/index.asp?Nid=353', '2024-05-10': 'http://epaper.cmnpnews.com/index.asp?Nid=354', '2024-05-17': 'http://epaper.cmnpnews.com/index.asp?Nid=355', '2024-05-24': 'http://epaper.cmnpnews.com/index.asp?Nid=356', '2024-05-31': 'http://epaper.cmnpnews.com/index.asp?Nid=357', '2024-06-07': 'http://epaper.cmnpnews.com/index.asp?Nid=358', '2024-06-14': 'http://epaper.cmnpnews.com/index.asp?Nid=359', '2024-06-21': 'http://epaper.cmnpnews.com/index.asp?Nid=360', '2024-06-28': 'http://epaper.cmnpnews.com/index.asp?Nid=361', '2024-07-04': 'http://epaper.cmnpnews.com/index.asp?Nid=362', '2024-07-12': 'http://epaper.cmnpnews.com/index.asp?Nid=363', '2024-07-19': 'http://epaper.cmnpnews.com/index.asp?Nid=364', '2024-07-26': 'http://epaper.cmnpnews.com/index.asp?Nid=365', '2024-08-02': 'http://epaper.cmnpnews.com/index.asp?Nid=366', '2024-08-09': 'http://epaper.cmnpnews.com/index.asp?Nid=367', '2024-08-16': 'http://epaper.cmnpnews.com/index.asp?Nid=368', '2024-08-23': 'http://epaper.cmnpnews.com/index.asp?Nid=369', '2024-08-30': 'http://epaper.cmnpnews.com/index.asp?Nid=370', '2024-09-06': 'http://epaper.cmnpnews.com/index.asp?Nid=371', '2024-09-13': 'http://epaper.cmnpnews.com/index.asp?Nid=372', '2024-09-20': 'http://epaper.cmnpnews.com/index.asp?Nid=373', '2024-09-27': 'http://epaper.cmnpnews.com/index.asp?Nid=374', '2024-10-04': 'http://epaper.cmnpnews.com/index.asp?Nid=375'}

def get_date():
    date_dict = {}
    for i in range(500, 375 - 1, -1):
        url = f'http://epaper.cmnpnews.com/index.asp?Nid={i}'
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            content = response.content.decode('gbk')
            html = etree.HTML(content)
            date = ''.join(html.xpath("//span[@class='fl qikan_menu']/text()"))
            # 华夏早报数字报 每周五出版 - 总第63期 2019年7月5日出版
            date_time = re.findall(r'(\d{4}年\d{1,2}月\d{1,2}日)', date)
            if date_time:
                date_time = date_time[0]
                # 将小于10的月和日前面添加0
                date_time = datetime.strptime(date_time, '%Y年%m月%d日').strftime('%Y-%m-%d')
                if date_time not in date_dict:
                    date_dict[date_time] = url
                else:
                    continue
        else:
            continue
    return date_dict


# print(get_date())


def get_huaxiazao_paper(paper_time, queue_id, webpage_id):
    get_date()
    # 将today的格式进行改变
    day = paper_time
    if paper_time not in date_dict:
        raise Exception(f'该日期没有报纸')
    url = date_dict[paper_time]
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.content.decode('gbk')
        html_1 = etree.HTML(content)
        # 获取所有版面的的链接
        all_bm = html_1.xpath("//div[@id='index_f_list']/ul/li/a")
        for bm in all_bm:
            # 版面名称
            bm_name = "".join(bm.xpath("./text()")).strip()
            # 版面链接
            bm_url = 'http://epaper.cmnpnews.com/' + ''.join(bm.xpath("./@href"))
            # 获取版面详情
            bm_response = requests.get(bm_url, headers=headers)
            time.sleep(1)
            bm_content = bm_response.content.decode('gbk')
            bm_html = etree.HTML(bm_content)
            # 版面的pdf
            bm_pdf = 'http://epaper.cmnpnews.com' + "".join(bm_html.xpath("//span[@class='fr pdf_down']/a/@href"))

            # 获取所有文章的链接
            all_article = bm_html.xpath("//div[@id='index_a_list']/ul/li/a")
            pdf_set = set()
            for article in all_article:
                # 获取文章链接
                article_url = 'http://epaper.cmnpnews.com/' + ''.join(article.xpath("./@href"))
                # 获取文章名称
                article_name = ''.join(article.xpath("./text()")).strip()
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.now().strftime('%Y-%m-%d')
                # 获取文章内容
                article_response = requests.get(article_url, headers=headers)
                time.sleep(1)
                article_content = article_response.content.decode('gbk')
                article_html = etree.HTML(article_content)
                # 获取文章内容
                content = ''.join(article_html.xpath("//div[@id='Zoom']//text()")).strip()
                # 上传到测试数据库
                conn_test = mysql.connector.connect(
                    host="rm-bp1t2339v742zh9165o.mysql.rds.aliyuncs.com",
                    user="col2024",
                    password="Bm_a12a06",
                    database="col",
                )
                cursor_test = conn_test.cursor()
                # print(bm_name, article_name, article_url, bm_pdf, content)
                if bm_pdf not in pdf_set and judging_bm_criteria(article_name) and judge_bm_repeat(paper, bm_url):
                    # 将报纸url上传
                    up_pdf = upload_file_by_url(bm_pdf, paper, "pdf", "paper")
                    pdf_set.add(bm_pdf)
                    # 上传到报纸的图片或PDF
                    insert_sql = "INSERT INTO col_paper_page (day, paper, name, original_pdf, page_url, pdf_url, create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s, %s,%s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (day, paper, bm_name, bm_pdf, bm_url, up_pdf, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                if judging_criteria(article_name, content):
                # if 1:

                    # print(content)
                    # return

                    # 上传到报纸的内容
                    insert_sql = "INSERT INTO col_paper_notice (page_url, day, paper, title, content, content_url,  create_time, from_queue, create_date, webpage_id) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"

                    cursor_test.execute(insert_sql,
                                        (bm_url, day, paper, article_name, content, article_url, create_time, queue_id,
                                         create_date, webpage_id))
                    conn_test.commit()

                cursor_test.close()
                conn_test.close()


        success_data = {
            'id': queue_id,
            'description': '数据获取成功',
        }
        paper_queue_success(success_data)

    else:
        raise Exception(f'该日期没有报纸')


# get_huaxiazao_paper('2024-10-31', 111, 1111)
