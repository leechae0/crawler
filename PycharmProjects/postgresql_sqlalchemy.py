import csv
import random

from numpy import genfromtxt
import sqlalchemy
from sqlalchemy import BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


#db connect

engine = create_engine('postgresql://postgres:postgres@121.138.81.143:5432/')
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session=Session()


class tmp_homeshopping(Base):
    __tablename__='tmp_homeshopping'
    start_date = Column(String)
    end_date = Column(String)
    parthne_name = Column(String)
    shop_code = Column(String)
    prod_name = Column(String)
    # cate1 = Column(String)
    # cate2 = Column(String)
    # cate3 = Column(String)
    # cate4 = Column(String)
    # shop_prod_id = Column(String)
    # prod_id = Column(String)
    # prod_img_url_m = Column(String)
    # prod_price_ = Column(String)
    # prod_url_m = Column(String)
    # participartion_type = Column(String)
    # use_yn = Column(String)
    id = Column(BigInteger, primary_key=True)

try:
    f= open('/home/lcy/2017-07-17_16epg.csv', 'r')
    tbl_reader = csv.reader(f,delimiter='{')

    for i in tbl_reader:
        print(i[8])
        # tmp_homeshopping.insert().values(start_date=i[0],end_date=i[1],prod_name=i[5])
        tmp_homeshopping.start_date = i[0]
        print(tmp_homeshopping.start_date)
        start_date= i[0],
        end_date= i[1],
        parthner_name = i[2],
        shop_code = i[3],
        prod_name = i[5],
        id= i[4]
        query = "INSERT INTO tmp_homeshopping (start_date, end_date, parthner_name, shop_code, prod_name, id) VALUES (%s,%s,%s,%s,%s,%s);"
        data=(start_date,end_date,parthner_name,shop_code,prod_name,id)

        session.execute(query,data)
        session.commit()
finally:
    session.close()  # Close the connection




#instance테이블 생성

#
# for instance in session.query(time_cate).order_by(time_cate.id):
#     if(instance.time=='6'):
#        print(instance.time, instance.ranking,instance.cate1, instance.cate2)

#dic_tc_h = {'prod_id': ['time','cate1','cate2']}
#
# dic_6_1 = {}
# id = 1
#
#
# for tc in session.query(time_cate):
#     for h in session.query(tmp_test_homeshopping):
#         if(tc.time =='6'):
#             if(tc.ranking=='1'):
#                if ((tc.cate2 == h.cate2)):
#                    dic_6_1[id] = {
#                        'prod_id': h.prod_id,
#                        'time': tc.time,
#                        'cate1': tc.cate1,
#                        'cate2': tc.cate2
#                    }
#                    id += 1
# print (dic_6_1)
# #
# #
# # def pop_queue(the_list, size=2):
# #
# #     if len(the_list) >= 2:
# #         return the_list[2:], the_list[0], the_list[1]
# #     elif len(the_list) >= 1:
# #         return the_list[2:], the_list[0], None
# #     return the_list[2:], None, None
# #
# #
# # the_list = [k for k in dic_tc_h.values()]
# #
# # while True:
# #     the_list, first, second = pop_queue(the_list)
# #     print (first, second)
# #     if not the_list:
# #         break
# #
#
# #리스트가 들어오면 0번째를 result table에 넣고 1을 0번째로 바꾸는
# keys = dic_6_1.keys()
# key = keys[0]
# keys = key[1:0]
#
#
#
# recommend_result={}
#
#
#
#
# def pop_queue(the_list):
#     keys = the_list.keys()
#     key = keys[0]
#     keys = keys[1:0]
#
