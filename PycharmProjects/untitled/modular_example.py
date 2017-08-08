# -*coding :utf-8-*-

from datetime import datetime
import arrow
import requests
from bs4 import BeautifulSoup
import xlrd
import re

#import refact_example

from requests import HTTPError

def main():
#    refact_example.iam_a_caller()
    detailed_dict = load_excel()
    detailed_dict2 = crawling_naver(detailed_dict)
    export_excel(detailed_dict2)


nowDate = arrow.utcnow().to('Asia/Seoul').format('YYYY-MM-DD_HH')

def load_excel(filename="/home/lcy/crawler/homeshopping_crawler/"+nowDate+"epg.xls"):
    EPG_workbook = xlrd.open_workbook(filename)
    EPG_worksheet_name = EPG_workbook.sheet_by_name('test')
    EPG_num_rows = EPG_worksheet_name.nrows  # 줄 수 가져오기

    id = 1
    detailed_dict = {}
    for row_index in range(EPG_num_rows):
        start_date = EPG_worksheet_name.cell_value(row_index, 0)
        # print(start_cell, type(start_cell))
        end_date = EPG_worksheet_name.cell_value(row_index, 1)
        # if not start_cell or not isinstance(start_cell, float):
        #     continue
        # if not end_cell or not isinstance(end_cell, float):
        #     continue
        # # From excel date expression to python datetime
      #  start_date = arrow.get(datetime(*xlrd.xldate_as_tuple(start_cell, EPG_workbook.datemode))).datetime
       # end_date = arrow.get(datetime(*xlrd.xldate_as_tuple(end_cell, EPG_workbook.datemode))).datetime

        # worksheet.write(row, 0, product.start_time)
        # worksheet.write(row, 1, product.end_time)
        # worksheet.write(row, 2, product.market_name)
        # worksheet.write(row, 3, product.shop_code)
        # worksheet.write(row, 4, product.category)
        # worksheet.write(row, 5, product.name)
        # worksheet.write(row, 6, product.shop_prod_id)
        # worksheet.write(row, 7, product.product_id)
        # worksheet.write(row, 8, product.image)
        # worksheet.write(row, 9, product.price)
        # worksheet.write(row, 10, product.detail_product_url)



        mall_name = EPG_worksheet_name.cell_value(row_index, 2)
       # category = EPG_worksheet_name.cell_value(row_index, 5)
        shop_code = EPG_worksheet_name.cell_value(row_index, 3)
        ch_no = EPG_worksheet_name.cell_value(row_index,4)
        detailed_product_name = EPG_worksheet_name.cell_value(row_index, 6)
        shop_prod_id = EPG_worksheet_name.cell_value(row_index,7)
        prod_id = EPG_worksheet_name.cell_value(row_index,8)
        image_url = EPG_worksheet_name.cell_value(row_index,9)
        price = EPG_worksheet_name.cell_value(row_index,10)
        detailed_product_url =EPG_worksheet_name.cell_value(row_index,11)

        detailed_dict[id] = {
            'start_date': start_date,
            'end_date': end_date,
            'mall_name': mall_name,
            'shop_code': shop_code,
            'ch_no': ch_no,
            'detailed_product_name': detailed_product_name,
            'shop_prod_id': shop_prod_id,
            'prod_id': prod_id,
            'image_url': image_url,
            'price': price,
            'detailed_product_url': detailed_product_url
        }
        id += 1

    return detailed_dict



def crawling_naver(detailed_dict):
    # 상품 명 중에서 제외할 단어 리스트로 나열
    except_word = ['[본품론칭이후최다구성]','◆16FW 신상 바로 그 느낌!◆',' 백화점 인기상품 긴급물량★','★전 고객 조건없이 5개 용량★',
                   '[오직 방송중에만 상담예약 가능]','★프리미엄 커튼/블라인드의 명가 벽창호★','★런칭가 159,000원★','★17년 SS 최신상★',
                   '★공식수입원 정품★','★백화점 판매동일 모델 사운드 바 증정★','시중동일모델 최저가 보상/차액의 100% 보상★','★TV상품★',
                   '★무료체험 14일★','★3/1 특집전 총4천만원 상당 행운찬스★','*14회방송매진*방송동일*★크림6개최다구성★','★2017년 최신상★',
                   '★전 성분 100% 자연유래★','★여배우들의 뷰티템! 먹는 콜라겐★','(방송에서만 구성)','(상시 구성)',
                   '17년 봄 팬츠 최신상품 // ','★17년 봄 팬츠 최신상품!★','★4회 방송 모두 완판! 방송중에만 특별한 가격★','♥17신상, 백화점 인기물량, 스타일업♥',
                   '★GS 단독구성★ ','★백화점 동일 상품, 백화점 판매가 239,000원★','*14회방송매진*방송동일*','[영국아두나]',
                   '★GS단독 사은품 러셀홉스 브펙퍼스트 세트★','★TV상품★','방송 동일조건 !!',' GS단독','★2017 마지막 생방송★','★방송동일조건★[AMing]','★최초2만원인하★',
                   '★여배우들의 뷰티템! 먹는 콜라겐 돌풍★','★파이널 최저가! 막바지 물량!★','(방송에서만 구성)','(미리주문)','(단품)','[단품]','(직)','★16FW 최신상★',
                   '[고객감사5만원↓]','★최저가! 단 59,000원!!!★','★1/2일 월요일 07시15분 마지막 생방송!!!★','★최초2만원인하★','디자이너가 선택한 NEW소재!',
                   '★2017년 봄신상★','런칭 사은품 책장 25일에만 드려요~','★방송동일조건★','[TV홈쇼핑]','(방송중)','(TV방송)','(TV)','_직택','(TV_직매입)','(1만원 인하)',
                   '_1만원인하',' (특약)','(TV방송_직)','(TV_기습)','[17년 최신상! 핫트렌드]','_50프로 할인','_특약','_무료체험15일',' 방송단독구성_조건변경',
                   '(직_리2)','(1-1)','(형성)','★2017년 여름 신상품★','17년 최신상','★2017 봄신상★','★2017년 봄신상★','★17SS 최신상★','_구성변경','★방송중 6만원세일! ',
                   '_직매입','(방송_정률)','세일','(TV_리뉴얼/직매)','(전용의자증정)','(TV_방송_직)',' ver1','5차','(TV_방송)','_15봉',' 5종+사은품','(16+6평형)',
                   '(18+6평형)','(18평형)','(TV기습)','(TV_초특가)','점보특대형','대형','(방송)','5차','(TV_2만원할인)','_직택배','(방송_직_1+1)','(1+1)',
                   '더블구성','(직)','기본구성',' 5팩','34팩_직택배','직매입_','(TV_형성)','[여름SALE3만원인하!]','_최대','(직매입)','(직_리2)','(TV_방_직)','(TV_특)','(TV_방송)',
                   '_배송','(특대형)','+사은품','(TV_5만원할인)','_1만인하','_사은품 추가','_ARS3천원',' ★여름에빛나는매력★','(특약)','대형','(사은품변경_정액)','(혼합형)',
                   '_직택배','_방송최저가','_더블구성','_기본구성','슈퍼특대형','특대형','_SALE','_최저가찬스','_직','(3차)','_최다구성','(방송중)','34팩','(TV_방_특)','(80매)',
                   '(TV_혼합)','기본세트','3종 세트','15마리','(사은품 포함)','12박스','_프로모션 강화','(프리미엄팩)','(기본팩)','(방송_세일)','역대최저가!','(기습초특가)','(직_리3)',
                   '(혼합형)','_사은품변경'

                   ]
#'★[가-핳]+.★'
    for (k, v) in detailed_dict.items():
        sart_date= v['start_date']
        end_date = v['end_date']
        detailed_product_name = v['detailed_product_name']
        if not detailed_product_name:
            continue
        for word in except_word:
            detailed_product_name=detailed_product_name.replace(word, '')
            re.sub("[0-9]종", "", detailed_product_name)
            re.sub("총 [0-9]통","",detailed_product_name)

        try:
            targetUrl = "http://shopping.naver.com/search/all.nhn"
            response = requests.get(targetUrl, params={
                'query': detailed_product_name,
                'frm': 'NVSHATC',
            })
            response.raise_for_status()
        except HTTPError as e:
            return None

        # soup 객체에 넣기
        # 여러개의 div중 첫번째 div 뽑아오기
        # <div class = "info">
        #   <a href = "/category/category.nhn?cat_id=[0-9]*" 중 title 뽑아오기기
        soup = BeautifulSoup(response.text, "lxml")
        first_div = soup.find('div', {'class': 'info'})
        detailed_dict[k]['categories'] = []
        if first_div:
            items = first_div.findAll('a', {'class': re.compile('cat_id_[0-9]+')})
            if items:
                item = items[-1]
                categories = item['title'].split(" > ")
                #item의 마지막 categories까지 뽑아오기위해 append(item.text)
                categories.append(item.text)
                print(categories)

                a = ",".join(categories)
                categories1=a.split(',')[0]
                detailed_dict[k]['categories1']=categories1
                categories2=a.split(',')[1]
                detailed_dict[k]['categories2']=categories2
                try:
                    categories3=a.split(',')[2]
                    detailed_dict[k]['categories3']=categories3
                except:
                    pass
                try:
                    categories4=a.split(',')[3]
                    detailed_dict[k]['categories4']=categories4
                except:
                    pass
                detailed_dict[k]['categories'] = categories
            else:
                print('categories info is empty')
        else:
            print('first_div is empty')
        print(detailed_dict[k])
    return detailed_dict


def export_excel(detailed_dict2):
    with open(nowDate+'epg.csv', 'w') as f:
        #[f.write('{0},{1}\n'.format(key, value)) for key, value in detailed_dict2.items()]
        for (k, v) in detailed_dict2.items():
            start_date = v['start_date']
            end_date = v['end_date']
            mall_name = v['mall_name']
            shop_code = v['shop_code']
            ch_no= v['ch_no']
          #  category = v['category']
            detailed_product_name = v['detailed_product_name']
#             categories1=str(v['categories1'] or "  ")
            categories1=str(v.get('categories1') or "  ")

            categories2=str(v.get('categories2') or "  ")
            categories3=str(v.get('categories3') or "  ")
            try:
                categories4=(v.get('categories4') or "  ")
            except:
                pass
            categories = str(v.get('categories')or "  ")
            shop_prod_id =v['shop_prod_id']
            prod_id = v['prod_id']
            image_url=v['image_url']
            price=v['price']
            detailed_product_url=v['detailed_product_url']

          #  print(str(start_date)+'{'+str(end_date)+'{''+mall_name+'{'+category+'{'+detailed_product_name+'{'+categories+'\n')

            f.write(str(start_date)+'{'+str(end_date)+'{'+mall_name+'{'+shop_code+'{'+ch_no+'{'+detailed_product_name+'{'+categories1+'{'+categories2+'{'+categories3+'{'+categories4+'{'+str(shop_prod_id)+'{'+str(prod_id)+'{'+str(image_url)+'{'+format(price)+'{'+str(detailed_product_url)+'\n')


'''
    for (k, v) in detailed_dict2.items():
        print('key: ', k)
        print('start_date: ', v['start_date'])
        print('end_date: ', v['end_date'])
        print('mall_name: ', v['mall_name'])
        print('category: ', v['category'])
        print('categories:', str(v['categories']))
        print('detailed_product_name: ', v['detailed_product_name'])
'''


if __name__ == '__main__':
    main()