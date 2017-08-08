from datetime import datetime
import xlrd
import arrow
import xlwt

# 6 mall EPG info excel
EPG_workbook = xlrd.open_workbook("/home/lcy/Python_workspace/test.xls")
EPG_worksheet_name = EPG_workbook.sheet_by_name('test')
EPG_num_rows = EPG_worksheet_name.nrows  # 줄 수 가져오기

id = 1
detailed_dict = {}
for row_index in range(EPG_num_rows):
    start_cell = EPG_worksheet_name.cell_value(row_index, 0)
    # print(start_cell, type(start_cell))
    end_cell = EPG_worksheet_name.cell_value(row_index, 1)
    if not start_cell or not isinstance(start_cell, float):
        continue
    if not end_cell or not isinstance(end_cell, float):
        continue
    #   From excel date expression to python datetime
    start_date = arrow.get(datetime(*xlrd.xldate_as_tuple(start_cell, EPG_workbook.datemode))).datetime
    end_date = arrow.get(datetime(*xlrd.xldate_as_tuple(end_cell, EPG_workbook.datemode))).datetime
    mall_name = EPG_worksheet_name.cell_value(row_index, 2)
    category = EPG_worksheet_name.cell_value(row_index, 3)
    detailed_product_name = EPG_worksheet_name.cell_value(row_index, 4)


    detailed_dict[id] = {
        'start_date': start_date,
        'end_date': end_date,
        'mall_name': mall_name,
        'category': category,
        'detailed_product_name': detailed_product_name,
    }
    id += 1
'''
for (k, v) in detailed_dict.items():
    print('key: ', k)
    print('start_date: ', v['start_date'])
    print('end_date: ', v['end_date'])
    print('mall_name: ', v['mall_name'])
    print('category: ', v['category'])
    print('detailed_product_name: ', v['detailed_product_name'])
'''

# product_excel file
workbook = xlrd.open_workbook("/home/lcy/Python_workspace/홈쇼핑채널_프로그램별_시청자수(2017.1.26).xlsx")
worksheet_name = workbook.sheet_by_name('현대홈쇼핑')
num_rows = worksheet_name.nrows  # 줄 수 가져오기


product_id =1
product_dict={}

for row_index in range(num_rows):
    date_cell = worksheet_name.cell_value(row_index, 1)
    time_cell = worksheet_name.cell_value(row_index, 2)

    if not date_cell or not isinstance(date_cell, str):
        continue
    if not time_cell or not isinstance(time_cell, str):
        continue

    my_date = arrow.get(date_cell).datetime
    time_splited_list = time_cell.split(' ~ ')

    start_time = time_splited_list[0]
    end_time = time_splited_list[1]

    start_hour = int(start_time.split(':')[0])
    start_min = int(start_time.split(':')[1])
    end_hour = int(end_time.split(':')[0])
    end_min = int(end_time.split(':')[1])

    start_date = my_date.replace(hour=+start_hour, minute=+start_min)
    end_date = my_date.replace(hour=+end_hour, minute=+end_min)
#    mall_name = EPG_worksheet_name.()
    product_name = worksheet_name.cell_value(row_index, 3)
   # OTVOTS_average = EPG_worksheet_name.cell_value(row_index, 11)

    product_dict[product_id] = {
        'start_date': start_date,
        'end_date': end_date,
 #       'mall_name': mall_name,
        'product_name': product_name,
     #   'OTVOTS_average': OTVOTS_average,
    }
    product_id += 1
'''
for (k, v) in product_dict.items():
    print('key: ', k)
    print('start_date: ', v['start_date'])
    print('end_date: ', v['end_date'])
  #print('mall_name: ', v['mall_name'])
    print('product_name: ', v['product_name'])
   # print('OTVOTS_average:',v['OTVOTS_average'])
'''

final_id = 1
final_dict={}
detailed_product_name_list=[]

for(k,v) in product_dict.items():
    for (key, value) in detailed_dict.items():

    # print(v['start_date'])
       # 두 dictionary의 starttime, endtime이 같다면 detailed_product_name에 저장
        if value['start_date']==v['start_date']:
            if not final_dict.get('detailed_product_name_list'):
                final_dict['detailed_product_name_list'] = []
                detailed_product_name_list.append(value['detailed_product_name'])


                detailed_product_name=detailed_product_name_list

                start_date = v['start_date']
                end_date = v['end_date']
                category = value['category']
                product_name = v['product_name']
    #print(detailed_product_name_list)
                final_dict[final_id] = {
                    'start_date': start_date,
                    'end_date': end_date,
                    # 'mall_name': mall_name,
                    'category': category,
                    'product_name': product_name,
                    'detailed_product_name': detailed_product_name,
                    #       'OTVOTS_average': OTVOTS_average,
                }
                final_id += 1

    detailed_product_name_list=[]

    # 두 dict 합쳐서 final_dic 만들기

for (k1, v1) in final_dict.items():
    print('key: ', k1)
    print('start_date: ', v1['start_date'])
    print('end_date: ', v1['end_date'])
        # print('mall_name: ', v['mall_name'])
    print('category: ', v1['category'])
    print('product_name: ', v1['product_name'])
    print('detailed_product_name :', v1['detailed_product_name'])
        # print('OTVOTS_average:',v['OTVOTS_average'])

'''
======================================

                # 두 dictionary의 starttime, endtime이 같다면 detailed_product_name에 저장
    if value['start_date'] == v['start_date']:
        if not final_dict.get('detailed_product_name_list'):
            final_dict['detailed_product_name_list'] = []
        final_dict['detailed_product_name_list'].append(value['detailed_product_name'])
        # detailed_product_name_list.append(value['detailed_product_name'])
        # print(detailed_product_name_list)

id=1
final_dict={}
detailed_product_name_list=[]
for(key,value) in detailed_dict.items():
    for(k,v) in product_dict.items():
   # print(v['start_date'])
       # 두 dictionary의 starttime, endtime이 같다면 detailed_product_name에 저장
        if value['start_date']==v['start_date']:
            detailed_product_name_list.append(value['detailed_product_name'])
            #print(detailed_product_name_list)

        start_date = value['start_date']
        end_date=value['end_date']
      #  mall_name =
        category = value['category']
        detailed_product_name=detailed_product_name_list







    # 두 dictionary의 starttime, endtime이 같다면 detailed_product_name에 저장
if value['start_date'] == v['start_date']:
    if not final_dict.get('detailed_product_name_list'):
        final_dict['detailed_product_name_list'] = []
    final_dict['detailed_product_name_list'].append(value['detailed_product_name'])
    # detailed_product_name_list.append(value['detailed_product_name'])
    # print(detailed_product_name_list)
'''






'''
detailed_product_name_list = []
for (key, value) in detailed_dict.items():
    detailed_product_name_list.append(value['detailed_product_name'])


detailed_product_name_list = [
    v['detailed_product_name'] for (k, v) in detailed_dict.items()
]

print(detailed_product_name_list)
'''
