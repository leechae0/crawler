import requests
import json


def request_schedule():
    url = 'http://apitest.skymall.co.kr/apiv4/tv/today-goods-list?'
    params = {
        'mediaCode': 'TV07',
        'uk': 'TT131127012',
        'ck':'20170417145200',
        'nolog':'EPG'
    }
    response = requests.get(
        url,
        params=params,
        timeout=2.0,
    )

    response_json = response.json()

#    print(response_json)

    goodList = response_json['data']['goodsList']


    for goods in goodList:
        startTime = goods['startTime']
        endTime = goods['endTime']


        sub_goodList = goods['subGoodsList']
        for item in sub_goodList:
            goodUrl = item['goodsUrl']
            goodsCode = item['goodsCode']
            goodsName = item['goodsName']
            saleDcAmt = item['saleDcAmt']

            imageUrl = get_imageUrl(goodUrl)


            print("startTime    : " + startTime)
            print("endTime      : " + endTime)
            print("goodName     : " + goodsName)
            print("goodCode     : " + goodsCode)
            print("imageUrl     : " + imageUrl)
            print("saleDcAmt    : " + str(saleDcAmt))
            print("detailURl    : " + "http://www.kshop.co.kr/goods/"+goodsCode)



# def make_up_time(goodUrl,time):
#     # input : 2450 --> output : YYYY/MM/DD HH/mm/ss
#     MMDD = goodUrl.split('_i_')
#     print(MMDD[1])
#     MM = MMDD[1][4:5]
#     DD = MMDD[1][6:7]
#     HH = time[0:1]
#     mm = time[2:3]
#
#     time = "2016/"+MM+"/"+DD +""+ HH+":" + mm + ":00"
#
#     return time
#

def get_imageUrl(goodUrl):
    url=goodUrl.replace('/w240','')
    r_url = url.replace('_i_','_g_')
    imageUrl=r_url.strip()

    return imageUrl




request_schedule()

# "goodsUrl": "http://imgs.kshop.co.kr/w308/goods/594/339594_i_20170220112148.jpg",
# "goodsCode": "339594",
# "goodsName": "잭필드 봄 숨쉬는 바지 3종_1만원인하",
# "salePrice": 49800,
# "dcAmt": 2000,
# "saleDcAmt": 46800,
# "arsDcAmt": 1000,
# "arsName": "잭필드 봄 숨쉬는 바지 3종",
# "mobileGoodsName": "잭필드 봄 숨쉬는 바지 3종_1만원인하",
# "inviGoodsType": "00",
# "broadDurSaleYn": "N",
# "startTime": "2243",
# "endTime": "2343",
# "onAirYn": "N",
# "seqFrameNo": "1000061934",
# "tapeSeqNo": "01",
# "emYn": "0",
# "subGoodsList": [
#     {
#         "goodsCode": "339594",
#         "goodsUrl": "http://imgs.kshop.co.kr/w240/goods/594/339594_i_20170220112148.jpg",
#         "goodsName": "잭필드 봄 숨쉬는 바지 3종_1만원인하",
#         "salePrice": 49800,
#         "saleDcAmt": 46800,
#         "arsDcAmt": 1000,
#         "arsName": "잭필드 봄 숨쉬는 바지 3종",
#         "mobileGoodsName": "잭필드 봄 숨쉬는 바지 3종_1만원인하",
#         "inviGoodsType": "00"
#     }
#