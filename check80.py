# -*- coding: utf-8 -*-
import requests, re, gc
from datetime import datetime 
from time import sleep
from bs4 import BeautifulSoup

# Avoid SSL error if you need
#requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
# Change directory
#os.chdir(os.path.dirname(os.path.abspath(__file__)))

# LINE Notify
line_url = "https://notify-api.line.me/api/notify"
token = (
"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # for report
"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx") # for debug
def line_out(msg, a=0):
    headers = {"Authorization": "Bearer " + token[a]}
    payload = {"message": msg}
    requests.post(line_url, headers=headers, data=payload)
    sleep(1)

# URL lists(tuple)
urls_tokyu = (
'https://www..co.jp/bukken-all/',
'https://www..co.jp/bukken-all/')
urls_sumifu = (
'https://www..co.jp/search/list/',)
urls_mitsui = (
'https://www..co.jp/bukkenList/',)
urls_nomura = (
'https://www..co.jp/land/',)
urls_mufj = (
'https://www..com/buyers/',)
urls_yuraku = (
'https://www..jp/land/',)
urls_c21 = (
'https://www..jp/tochi/',)
urls_test = (
'https://httpstat.us/200?sleep=10000',)

# Compile re
del_cc = re.compile(r'\n|\r|\t|\xa0|\u3000')
bukken_tokyu = re.compile(r'.......万円.*?容積率......')
kenpei_tokyu = re.compile(r'建ぺい率.{1,20}?/')
bukken_sumifu = re.compile(r'価格.{1,12}?万円.*?容積率.{1,12}?/......')
kenpei_sumifu = re.compile(r'建ぺい率 /.{1,20}?/')
bukken_mitsui = re.compile(r'価格.{1,12}?万円.*?容積率........')
kenpei_mitsui = re.compile(r'建ぺい率.{1,12}?容')
bukken_nomura = re.compile(r'.......万円.*?容積率......')
kenpei_nomura = re.compile(r'建ぺい率.{1,12}?容')
bukken_mufj = re.compile(r'価格.{1,12}?万円.*?容積率.{1,12}?／......')
kenpei_mufj = re.compile(r'建ぺい率／.{1,20}?／')
bukken_c21 = re.compile(r'.......万円 東京都.*?容積率.*?建築条件.....')
kenpei_c21 = re.compile(r'建ぺい/.{1,20}?/')
bukken_yuraku = re.compile(r'.......万円.{1,50}?東京都.*?容積率......')
kenpei_yuraku = re.compile(r'建ぺい率.{1,12}?容')

# Define dictionaries
companies = ('tokyu', 'sumifu', 'mitsui', 'nomura', 'mufj', 'yuraku', 'c21')
dict_kanji = {'tokyu':'XX不動産', 'sumifu':'XX不動産', 'mitsui':'XX不動産', 'nomura':'XX不動産' ,'mufj':'XX不動産', 'yuraku':'XX不動産' ,'c21':'XX不動産', 'test':'テスト'} 
dict_urls = {'tokyu':urls_tokyu, 'sumifu':urls_sumifu, 'mitsui':urls_mitsui, 'nomura':urls_nomura, 'mufj':urls_mufj, 'yuraku':urls_yuraku, 'c21':urls_c21, 'test':urls_test}
dict_bukken = {'tokyu':bukken_tokyu, 'sumifu':bukken_sumifu, 'mitsui':bukken_mitsui, 'nomura':bukken_nomura, 'mufj':bukken_mufj, 'yuraku':bukken_yuraku, 'c21':bukken_c21, 'test':bukken_tokyu}
dict_kenpei = {'tokyu':kenpei_tokyu, 'sumifu':kenpei_sumifu, 'mitsui':kenpei_mitsui, 'nomura':kenpei_nomura, 'mufj':kenpei_mufj, 'yuraku':kenpei_yuraku, 'c21':kenpei_c21, 'test':kenpei_tokyu}

def check80(name):
    print('Now:', datetime.now())
    print('==========' + dict_kanji[name] + '==========')
    # Read history file
    with open(name + '_history.txt', encoding='utf-8') as f:
        history = f.readlines()
    # Open history file to write
    f_out = open(name + '_history.txt','a', encoding='utf-8')
    cnt_bukken = 0
    # Get html from each url
    for url in dict_urls[name]:
        try:
            res = requests.get(url, timeout=(10.0, 30.0))
        except Exception as err:
            print(err.args)
            line_out(dict_kanji[name] + 'のWEBリクエストでエラーが発生しました。。。', 1)
            return
        soup = BeautifulSoup(res.text, 'html.parser')
        temp = soup.get_text()
        # Eliminate control charactor
        temp = del_cc.sub(' ', temp)
        # Extract bukken
        temp_list = dict_bukken[name].findall(temp)
        # Count number of bukkens
        cnt_bukken = cnt_bukken + len(temp_list)
        # Check 建蔽率 in each bukkens
        for i_str in temp_list:
            # Eliminate space
            i_str = i_str.replace('     ', '')
            # Extract kenpei x0 %
            temp = dict_kenpei[name].search(i_str).group()
            # If kenpei != 80% then next i
            if re.search(r'8|８', temp) == None:
                continue
            # If kenpei = 80%
            print(i_str)
            # Compare with history
            flag = 0
            for n_str in history:
                n_str = n_str.replace('\n', '')
                if i_str == n_str:
                    flag = flag + 1
                    break
            # If we know the one then next i
            if flag != 0:
                print('既出物件です。。。')
                print('================================')
                continue
            # If we do not know the one
            print('新規物件がありました！')
            f_out.write(str(datetime.now()) + '\n')
            f_out.write(i_str + '\n')
            line_out(url)
            line_out(i_str)
            print('================================')
        sleep(5)
    f_out.close()
    print('新着物件数:', cnt_bukken)
    if cnt_bukken == 0:
        line_out(dict_kanji[name] + 'の新着物件数がゼロでした。。。', 1)
    print('==========ループ終了============')

# main
for company in companies:
    check80(company)
    gc.collect()
line_out('不動産検索完了', 1)
