import requests
import re
import datetime
import MySQLdb
from urllib.parse import urlparse
from bs4 import BeautifulSoup

class URL_to_list():
    def __init__(self, url):
        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.parsed_url = urlparse(url)

        # 取得内容を保存するための辞書型変数
        self.page_contents = {}
        # 現在の日時を取得
        self.now = datetime.datetime.now()
        
        try:
            self.response = requests.get(self.url, headers=self.headers, timeout=30)
            self.response.raise_for_status()
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
            print(
                "ページURL: {}, HTTPステータス: {}, 処理時間(秒): {}, 現在時刻: {}".format(
                    self.url,
                    self.response.status_code,
                    self.response.elapsed.total_seconds(),
                    self.now
                    )
            )
            #self.page_contents[self.url] = self.response.text
        except requests.exceptions.RequestException as e:
            msg = "[ERROR] {exception} {now}\n".format(
                exception=e,
                now=self.now
            )
            print(msg)
        

    # 1.1.1 Using the IP Address
    def using_ip_address(self):
        re_addr = re.compile("((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))")
        check = re_addr.search(self.url)
        if(check != None):
            return -1
        elif(check == None):
            return 1
        
    # 1.1.2 Long URL to Hide the Suspicious Part
    def url_length(self):
        url_len = len(self.url)
        if 75 >= url_len >= 54:
            ans = 0
        elif url_len >= 54:
            ans = -1
        elif url_len < 54:
            ans = 1
        return ans

    # 1.1.3 Using URL Shortening Services "TinyURL"
        
    # 1.1.4 URL's having "@" Symbol
    def at_sign_symbol(self):
        for character in self.url:
            if(character == "@"):
                ans = -1
                break
            else:
                ans = 0
        return ans

    # 1.1.5 Redirecting using "//"


    # 1.1.6 Adding Prefix or Suffix Separated by (-) to the Domain

    # 1.1.7 Sub Domain and Multi Sub Domains

    # 1.1.8 HTTPS(Hyper Text Transfer Protocol with Secure Sockets Layer)

    # 1.1.9 Domain Registration Length

    # 1.1.10 Favicon

    # 1.1.11 Using Non-Standard Port

    # 1.1.12 The Existence of "HTTPS" Token in the Domain Part of the URL

    # 1.2.1 Request URL
    
    # 1.2.2 URL of Anchor
    def url_of_anchor(self):
        cnt = 0.01
        anc_cnt = 0.0
        for link in self.soup.findAll('a', href=True):
            cnt += 1.0
            if "#" == link['href']:
                anc_cnt += 1.0
            elif "#content" == link['href']:
                anc_cnt += 1.0
            elif "#skip" == link['href']:
                anc_cnt += 1.0
            elif "JavaScript::void(0)" in link['href']:
                anc_cnt += 1.0

        per = anc_cnt / cnt*100
        if per < 31:
            return 1
        elif 31 <= per and per >= 67:
            return 0
        else:
            return -1

    # 1.2.3 Links in <Meta>, <Script> and <Link> tags

    # 1.2.4 Server Form Handler (SFH)

    # 1.2.5 Submitting Information to Email
    def is_send_email(self):
        cnt = 0.0
        anc_cnt = 0.0
        for link in self.soup.findAll('a', href=True):
            cnt += 1.0
            if "mailto" in link['href']:
                return -1
            elif "mail()" in link['href']:
                return -1
        return 1
    
    def result(self):
        url_data_list = []
        url_data_list.append(self.at_sign_symbol())
        url_data_list.append(self.url_of_anchor())
        url_data_list.append(self.url_length())
        url_data_list.append(self.is_send_email())
        return url_data_list
