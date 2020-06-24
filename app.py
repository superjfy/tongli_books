# -*- coding: utf-8 -*
import requests
import time
from bs4 import BeautifulSoup
import os.path



def lineNotify(token, msg):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = requests.post(url, headers=headers, params=payload)

    return r.status_code


bookFile = "/home/jeffyang/books.txt"
oldbook_list = []
if os.path.exists(bookFile):
    with open(bookFile, "r+" , encoding="utf-8-sig") as f:
        for line in f:
            line = line.rstrip("\n")
            oldbook_list.append(line)
else:
    with open(bookFile, "w+", encoding="utf-8-sig") as fe:
        pass


store_old_books = set()
# 欲取得的書名關鍵字
wantBook_list = [u"火影", u"七龍珠", u"鬼滅"]
token = "URcWh4jqXmWSxmpiPoraXBDeTXu0WWcFO0fFMkIdyHp"
session = requests.Session()
page_num = 1
url = "https://www.tongli.com.tw/webpagebooks.aspx?page=" + str(page_num) + "&s=1"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
page_list = []
book_set = set()
req = session.get(url, headers=headers)
soup = BeautifulSoup(req.text, 'html.parser')
for page_tag in soup.find_all("a", class_="page_numbers"):
    page_list.append(page_tag.text)
total_page = int(len(page_list))

for page in range(total_page):
    getPage = str((int(page) + 1))
    url2 = "https://www.tongli.com.tw/webpagebooks.aspx?page=" + getPage + "&s=1"
    req2 = session.get(url2, headers=headers)
    soup2 = BeautifulSoup(req2.text, 'html.parser')
    for p_tag2 in soup2.find_all("div", class_='pk_txt'):
        book_set.add(p_tag2.text)

for wantBook in wantBook_list:
    for book in book_set:
        if wantBook in book:
            if book not in oldbook_list:
                store_old_books.add(book)
if len(store_old_books) != 0:
    # lineNotify(token, str(store_old_books))
    print(store_old_books)
    with open(bookFile, "w+", encoding="utf-8-sig") as fw:
        for item in store_old_books:
            fw.write("{}\n".format(item))
else:
    print("no new book.")