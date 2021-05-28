import requests
import json
from bs4 import BeautifulSoup

KAKAO_TOKEN = ''

send_lists = [] # data cache
def send_to_kakao(text):
    header = {"Authorization" : 'Bearer ' + KAKAO_TOKEN}
    url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'
    post = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        },
        "button_title": "바로 확인"
    }
    
    data = {'template_object' : json.dumps(post)}
    return requests.post(url, headers=header, data=data)

def hotdeal(condition):
    url = ''
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.select_one('div.fm_best_widget')

        titles = div.select('ul > li > div > h3.title > a.hotdeal_var8')
        prices = div.select('ul > li > div > div.hotdeal_info > span:nth-child(2)')
        categorys = div.select('ul > li > div > div > span.category > a')
        for idx, title in enumerate(titles):
            link = url + title['href']
            title = title.get_text().strip()
            price = prices[idx].get_text().strip()
            category = categorys[idx].get_text().strip()
            for select in condition['category'] :
                if category == select : # 찾는 카테고리
                    send = True
                    for sended in send_lists:
                        if sended['title'] == title :
                            print('보낸 데이터')
                            send = False
                    if send :
                        text = "{} {} {} {}".format(title, price, category, link)
                        print(text)
                        r = send_to_kakao(text)
                        print(r.text)
                        # 데이터 캐시화
                        send_lists.append({
                            'title' : title,
                            'price' : price,
                            'category' : category,
                            'link' : link,
                        })
            #print(datas)
        
    else:
        print(response.status_code)

import time
if __name__ == '__main__' :
    condition = {'category' : [
        '먹거리', '의류', 'SW/게임', 'PC제품'
        ]}
    
    while True :
        hotdeal(condition)
        time.sleep(60 * 5)