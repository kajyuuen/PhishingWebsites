import requests
import re
import datetime
from urllib.request import urlopen
import ssl
import OpenSSL
import MySQLdb

from urllib.parse import urlparse
from bs4 import BeautifulSoup

class URL_to_list():
    """
    このクラスはUCI Machine Learning Repository
    Phishing WebSites Datasetの基づいた特徴量を任意のURLから抽出する.
    """
    def __init__(self, url):
        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.parsed_url = urlparse(url)

        # 取得内容を保存するための辞書型変数
        self.page_contents = {}
        # 現在の日時を取得
        self.now = datetime.datetime.now()
        
        try:
            # 短縮URLかチェックする
            # 短縮URLの場合は, 本当のURLをself.urlにする
            self.real_url = urlopen(self.url).geturl()
            self.old_url = self.url
            self.url = self.real_url
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
    #
    def having_IP_Address(self):
        # {-1, 1}
        re_addr = re.compile("((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))")
        check = re_addr.search(self.url)
        if(check != None):
            return -1
        elif(check == None):
            return 1
        
    # 1.1.2 Long URL to Hide the Suspicious Part
    def URL_Length(self):
        url_len = len(self.url)
        if 75 >= url_len >= 54:
            ans = 0
        elif url_len >= 54:
            ans = -1
        elif url_len < 54:
            ans = 1
        return ans

    # 1.1.3 Using URL Shortening Services "TinyURL"
    # return があっている分からない
    def Shortining_Service(self):
        # {1,-1}
        if(self.url == self.old_url):
            return 1
        elif(self.url != self.old_url):
            return -1
    
    # 1.1.4 URL's having "@" Symbol
    def having_At_Symbol(self):
        for character in self.url:
            if(character == "@"):
                ans = -1
                break
            else:
                ans = 0
        return ans

    # 1.1.5 Redirecting using "//"
    def double_slash_redirecting(self):
        # {-1, 1}
        pass

    # 1.1.6 Adding Prefix or Suffix Separated by (-) to the Domain
    def Prefix_Suffix(self):
        # {-1, 1}
        for character in self.url:
            if(character == "-"):
                ans = -1
                break
            else:
                ans = 0
        return ans
    
    # 1.1.7 Sub Domain and Multi Sub Domains
    def having_Sub_Domain(self):
        # {-1,0,1}
        pass
    
    # 1.1.8 HTTPS(Hyper Text Transfer Protocol with Secure Sockets Layer)
    def SSLfinal_State(self):
        # {-1, 1, 0}
        
        pass
    
    # 1.1.9 Domain Registration Length
    def Domain_registeration_length(self):
        # {-1, 1}
        pass
    
    # 1.1.10 Favicon
    def Favicon(self):
        # {-1, 1}
        pass

    # 1.1.11 Using Non-Standard Port
    def port(self):
        # {1, -1}
        pass
    # 1.1.12 The Existence of "HTTPS" Token in the Domain Part of the URL
    def HTTPS_token(self):
        # {-1, 1}
        pass
    # 1.2.1 Request URL
    def Request_URL(self):
        # {-1, 1}
        pass
    # 1.2.2 URL of Anchor
    def URL_of_Anchor(self):
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
    def Links_in_tags(self):
        pass
    # 1.2.4 Server Form Handler (SFH)
    def SFH(self):
        pass
    
    # 1.2.5 Submitting Information to Email
    def Submitting_to_email(self):
        cnt = 0.0
        anc_cnt = 0.0
        for link in self.soup.findAll('a', href=True):
            cnt += 1.0
            if "mailto" in link['href']:
                return -1
            elif "mail()" in link['href']:
                return -1
        return 1

    # 1.2.6 Abnormal URL
    def Abnormal_URL(self):
        pass

    # 1.3.1 Website Forwarding
    def Redirect(self):
        pass

    # 1.3.2 Status Bar Customization
    def Redirect(self):
        pass

    # 1.3.3 Disabling Right Click
    def on_mouseover(self):
        pass

    # 1.3.4 Using Pop-up Window
    def popUpWindow(self):
        pass

    # 1.3.5 IFrame Redirection
    def Iframe(self):
        #if (self.soup.find_all('iframe') == []):                    # iframeだけ使用
        if (self.soup.find_all('iframe',{"frameborder":"0"}) == []):  # フレームなしで非表示
            return 1
        else:
            return -1

    # 1.4.1 Age of Domain
    def age_of_domain(self):
        pass

    # 1.4.2 DNS Record
    def DNSRecord(self):
        pass

    # 1.4.3 Website Traffic
    def web_traffic(self):
        pass

    # 1.4.4 PageRank
    def Page_Rank(self):
        pass

    # 1.4.5 Google Index
    def Google_Index(self):
        pass

    # 1.4.6 Number of Links Pointing to Page
    def Links_pointing_to_page(self):
        pass

    # 1.4.7 Statistical-Reports Based Feature
    def Statistical_report(self):
        pass
    
    def result(self):
        """
        result関数は全ての特徴量をlistとして返す
        """
        url_data_list = []
        url_data_list.append(self.having_IP_Address())       # 1.1.1
        url_data_list.append(self.URL_Length())              # 1.1.2
        url_data_list.append(self.Shortining_Service())      # 1.1.3
        url_data_list.append(self.having_At_Symbol())        # 1.1.4
        url_data_list.append(self.URL_of_Anchor())           # 1.2.2
        url_data_list.append(self.Submitting_to_email())     # 1.2.5
        return url_data_list
