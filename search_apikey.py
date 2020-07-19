"""
Search API Key from github
code by @dyjang
"""

__author__ = "dyjnag"

from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import config

_DRIVER_PATH = config.DRIVER_PATH
_GITHUB_USERNAME = config.GITHUB_USERNAME
_GITHUB_PWD = config.GITHUB_PWD
_KEYWORD = config.KEYWORD

# chrome webdriver
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')
browser = webdriver.Chrome(executable_path = _DRIVER_PATH ,chrome_options=options)

# Auto login to Github
def auto_login():
    url = "https://github.com/login"
    browser.get(url)

    username = browser.find_element_by_name('login')
    username.send_keys(_GITHUB_USERNAME)

    password = browser.find_element_by_name('password')
    password.send_keys(_GITHUB_PWD)

    form = browser.find_element_by_name('commit')
    form.submit()

# Github search로 korbit, api 검색되는 코드 가져오기
def crwl():
    kw = '+'.join(_KEYWORD)
    for cnt in range(80):
        browser.get("https://github.com/search?p={page}&q={keyword}}&type=Code&utf8=%E2%9C%93".format(page=cnt, keyword=kw))
        html = browser.page_source

        with open("github", "a",  encoding='utf8') as f: # github 파일에 저장
            f.write(html)

# 가져온 코드에서 api 키 추출
def find_key():
    with open("github", "r", encoding='utf8') as f:
        data = f.read()
        buf = re.findall('[\"\']\</span\>([a-zA-Z0-9]{61})\<', data)
    try:
        print(data)
    except UnicodeEncodeError:
        print("err")

    key_list = list(set(buf))
    for a in range(len(key_list)):
        with open("api_key_list", "a+", encoding='utf8') as k: # api_key_list 파일에 저장
            before_keylist = k.readlines()
            if(key_list[a] not in before_keylist):
                k.write("{0}\n".format(key_list[a]))
    print(key_list)

if __name__ == '__main__':
    auto_login()
    crwl()
    find_key()
