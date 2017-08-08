# -*coding :utf-8-*-

import requests
from bs4 import BeautifulSoup
import xlrd
import re
#
# 6개 mall 상세상품명 정보가 들어있는 excel 읽어서
# 상품명을 dictionary에 넣어서 네이버 url에 붙여서 검색
#

# 엑셀 가져오기
EPG_workbook = xlrd.open_workbook("/home/lcy/Python_workspace/EPG Crawling_10_26.xls")
EPG_worksheet_name = EPG_workbook.sheet_by_name('test')
EPG_num_rows = EPG_worksheet_name.nrows  # 줄 수 가져오기

id = 1
detailed_dict = {}
for row_index in range(EPG_num_rows):
    detailed_product_name = EPG_worksheet_name.cell_value(row_index, 4)
    detailed_dict[id] = {
        'detailed_product_name': detailed_product_name,
    }
    id += 1

# 상품 명 중에서 제외할 단어 리스트로 나열
except_word = ['TV']

# candidate_category_list는 네이버 카테고리 가져오고
# final_category_list에다가 맨 마지막에 (3depth카테고리 정보)저장
text = ''
candidate_category_list = []
final_category_list = []

# detailed_product_name이 비어있으면 넘어가고
# 제외할 단어 지우며 url 주소 가져옴
count = 10
for (k, v) in detailed_dict.items():
    detailed_product_name = v['detailed_product_name']
    if not detailed_product_name:
        continue
    for word in except_word:
        detailed_product_name.replace(word, '')
    targetUrl = "http://shopping.naver.com/search/all.nhn"
    response = requests.get(targetUrl, params={
        'query': detailed_product_name,
        'frm': 'NVSHATC',
    })

    # soup 객체에 넣기
    # response.text 한 이유 : 111111111111111111111111111111
    # 여러개의 div중 첫번째 div 뽑아오기
    # <div class = "info">
    #   <a href = "/category/category.nhn?cat_id=[0-9]*" 중 title 뽑아오기기

    soup = BeautifulSoup(response.text, "lxml")

    first_div = soup.find('div', {'class': 'info'})
    if not first_div:
        continue
    items = first_div.findAll('a', {'class': re.compile('cat_id_[0-9]+')})
    item = items[-1]
    categories = item['title'].split(" > ")
    detailed_dict[k]['categories'] = categories
    print(detailed_dict[k])
    break


'''
    for item in soup.find_all("a"):
        #        if hasattr(item,'attrs') and item.attrs and item.attrs.get('title'):
        #       2번째 item.attrs는 왜하는지!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if hasattr(item, 'attrs') and item.attrs.get('title'):
            if detailed_product_name in item.attrs['title']:
                a = item.parent.find_all('a')
                for b in a:
                    if hasattr(b, 'attrs') and b.attrs.get('title'):
                        text = text + str(item.find_all(text=True))
                        candidate_category_list.append(b.attrs.get('title'))
                final_category_list.append(candidate_category_list[-1])
                print(final_category_list)
        final_category_list = []
'''


