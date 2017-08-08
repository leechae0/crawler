# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime, date, time, timedelta
import urllib
import re
import xlwt
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def webcrawling():
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page)
    return soup

def safeunicode(s):
    try:
        return s.encode('latin-1').decode('cp949')
    except UnicodeEncodeError:
        return s


def filter_time(time):
    if (time.minute % 5 == 1):
        time = time - timedelta(minutes=1)
    elif (time.minute % 5 == 4):
        time = time + timedelta(minutes=1)
    return time


def wait_for_condition(condition_type, condition, timeout):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((condition_type, condition)))
        return True
    except TimeoutException:
        print('Waited for {0} secs. Cannot meet the condition. Ignore It.'.format(timeout))
        return False


print("\n#################################################")
print("####### Homeshopping EPG Crawling Program #######")
print("#################################################")

# exel file(with xlwt lib)
workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('test', cell_overwrite_ok=True)

date_format = xlwt.XFStyle()
date_format.num_format_str = 'hh:mM:sS YYYY/MM/DD'

# excel numbering
p = 0

# 홈쇼핑 채널 선택
channels = [['CJ오쇼핑', 'cjmall', '4'], ['NS홈쇼핑', 'nsmall', '6'], ['GS SHOP', 'gsshop', '8'],
            ['현대홈쇼핑', 'hmall', '10'], ['롯데홈쇼핑', 'lottemall', '12'], ['홈&쇼핑', 'hnsmall', '14']]

driver = webdriver.Firefox()

for channel in channels:
    ch_name = channel[0]
    ch_num = channel[2]
    ch_name_encode = urllib.parse.quote(ch_name.encode("euc-kr"))

    print("\n### " + ch_name + " (ch." + ch_num + ") EPG Crwaling Start. ###")

    # 수집 방영날짜 지정
    # ---------------------------
    year_date = 2017
    month_date = 4
    sday_date = 9
    eday_date = 10
    # ---------------------------
    for day_date in range(sday_date, eday_date + 1):
        date_t = date(year_date, month_date, day_date)
        query_date1 = str(date_t)
        query_date2 = str(year_date) + "%02d" % month_date + "%02d" % day_date
        #롯데홈쇼핑 날짜 형
        query_date3 = "%02d" % month_date +"."+ "%02d" % day_date
        print(query_date3)
        print("\ndate: " + query_date1)

        # HomePage crawling
        print("\n-- HomePage crawling --")
        HPList = []

        ##1)CJ오쇼핑 (time,category,prog_name)
        '''
        if ch_name=='CJ오쇼핑': 
            url="http://www.cjmall.com/etv/broad/schedule_list_week_iframe.jsp?start_date="+query_date2
            page_source=webcrawling()
            find_sc=page_source('tr')

            #해당 날짜 순번 찾기
            find_num=find_sc[0].findAll('strong')
            for i in find_num:
                if str(i).find("%02d"%month_date+'/'+"%02d"%day_date)!=-1: num=find_num.index(i)                

            def cjshop_crawling(HPList):
                cnt=0
                i=index
                x='true'
                while i<len(find_sc[1:]) and x=='true':
                    sc=find_sc[1:][i].findAll('td')[n]
                    i=i+1
                                
                    for j in range(len(sc.findAll('h4'))): #j:시간당 프로그램 개수
                        #시간 추출
                        stime_hhmm=sc.findAll('h4')[j].contents[0].rstrip()
                        stime=datetime(int(year_date),int(month_date),day_date,int(stime_hhmm[0:2]),int(stime_hhmm[3:5]))
                                    
                        if stime_hhmm!='':
                            if cnt==0:
                                hour_tmp=stime_hhmm[0:2]
                                cnt=cnt+1

                            if hour_tmp<=stime_hhmm[0:2]:
                                hour_tmp=stime_hhmm[0:2]
                                            
                                #카테고리 추출
                                category=sc.findAll('strong')[j].string[1:-1]
                                category=safeunicode(category)
                                if category=='':
                                    category='none'

                                #상품명 추출
                                count=int(len(sc.findAll('p')[j].findAll('img'))/2) #count:동시간 방영상품 개수
                                for k in range(0,count):
                                    prog_name=sc.findAll('p')[j].findAll('img')[2*k].next.strip().replace("'","''").replace('"','').replace(';','')
                                    prog_name=safeunicode(prog_name)
                                    HPList.append([stime,category,prog_name])
                            else: x='wrong'                            
                return HPList

            #06~23시 편성표 추출(당일)
            n=num
            index=0
            HPList=cjshop_crawling(HPList)

            #00~05시 편성표 추출(전날)
            def find_morningItem():
                cnt=0
                k=0
                x='continue'
                while k<len(find_sc[1:]) and x=='continue':
                    k=k+1
                    sc=find_sc[1:][k].findAll('td')[n]
                    for j in range(len(sc.findAll('h4'))):
                        stime_hhmm=sc.findAll('h4')[j].contents[0].rstrip()
                        if stime_hhmm!='':
                            if cnt==0:
                                hour_tmp=stime_hhmm[0:2]
                                cnt=cnt+1
                            if hour_tmp<=stime_hhmm[0:2]: hour_tmp=stime_hhmm[0:2]
                            else: x='end'                    
                return k
                
            if num!=0:
                n=num-1
                index=find_morningItem()
                HPList=cjshop_crawling(HPList)
                    
            else: #전날페이지로 넘어가서 추출
                date_t=date_t-timedelta(days=1)
                url="http://www.cjmall.com/etv/broad/schedule_list_week_iframe.jsp?start_date="+str(date_t.year)+"%02d"%date_t.month+"%02d"%date_t.day
                page_source=webcrawling()
                find_sc=page_source('tr')
                n=6
                index=find_morningItem()
                HPList=cjshop_crawling(HPList)

    ##2)NS홈쇼핑 (time,prog_name)                
        if ch_name=='NS홈쇼핑':
            def nsshop_time():
                List=[]
                x=0
                for i in (0,1):
                    f_time=time[i].strip()
                    hour=int(f_time[3:].split(':')[0])
                    minute=int(f_time[3:].split(':')[1])
                        
                    if f_time[0:2]=='오후' and hour<12: hour=hour+12
                    if f_time[0:2]=='오전' and hour==12: hour=0

                    d_time=datetime(int(year_date),int(month_date),day_date,hour,minute)
                    if i==0: stime=d_time
                    elif i==1: etime=d_time

                if etime-stime<timedelta(days=0):
                    etime=etime+timedelta(days=1)
                    x=x+1
                List.append([stime,etime,x])
                return List
                            

            #02~23시 편성표 추출(당일)
            url="http://www.nsmall.com/TVHomeShoppingBrodcastingList?tab_gubun=1&tab_Week=1&tab_bord=0&selectDay="+str(date_t)+"&catalogId=18151&langId=-9&storeId=13001#goToLocation"
            page_source=webcrawling()
            find_sc=page_source.findAll('tr')

            i=0
            while i<len(find_sc):            
                if find_sc[i].find('td',"air")!=None:

                    #시간 추출
                    time=find_sc[i].em.getText().split('~')
                    stime=nsshop_time()[0][0]
                    etime=nsshop_time()[0][1]

                    #상품명 추출
                    j=i+1
                    while (find_sc[j].find('td',"air")==None) and (find_sc[j].find('span',"inform pr10")!=None):
                        y=find_sc[j].find('span',"inform pr10").findAll('a')
                        if len(y)==1: prog_name=y[0].getText().strip()
                        else: prog_name=y[1].getText().strip()
                        HPList.append([stime,etime,prog_name])
                        j=j+1
                        
                    if nsshop_time()[0][2]!=0: break

                    #상품 ID 추출 :prdId


                    #상품Image 추출 :prodImg
                    #상품 가격 추출 :prodPrice




                i=i+1


            #00~02시 편성표 추출(전날)
            date_t=date_t-timedelta(days=1)
            url="http://www.nsmall.com/TVHomeShoppingBrodcastingList?tab_gubun=1&tab_Week=1&tab_bord=0&selectDay="+str(date_t)+"&catalogId=18151&langId=-9&storeId=13001#goToLocation"
            page_source=webcrawling()
            find_sc=page_source.findAll('tr')

            i=len(find_sc)-1
            while i>0:
                if find_sc[i].find('td',"air")!=None:

                    #시간 추출
                    time=find_sc[i].em.getText().split('~')
                    stime=nsshop_time()[0][0]
                    etime=nsshop_time()[0][1]
                    if nsshop_time()[0][2]!=0: break

                    #상품명 추출
                    j=i+1
                    while (find_sc[j].find('td',"air")==None) and (find_sc[j].find('span',"inform pr10")!=None):
                        y=find_sc[j].find('span',"inform pr10").findAll('a')
                        if len(y)==1: prog_name=y[0].getText().strip()
                        else: prog_name=y[1].getText().strip()
                        HPList.append([stime,etime,prog_name])
                        j=j+1
                        
                i=i-1

'''
        ##3)GS SHOP (time,category,prog_name)
        if ch_name == 'GS SHOP':
            url = "http://with.gsshop.com/tv/tvScheduleMain.gs?preValue=Y&selectDate=" + query_date2 + "#end"
            page_source = webcrawling()
            find_sc = page_source('div', id="scheduleTable")[0]
            sc = find_sc.findAll("table")

            for x in sc:
                # li로 find해서 sc 구성
                # if x.find("li",{"class":" ombudsman past-air"}):
                #     continue
                #     print("pass")
                item = x.findAll('tr')

                # 시간 추출
                time = item[0].find('td', 'time').strong.string
                stime = datetime(int(year_date), int(month_date), day_date, int(time[0:2]), int(time[3:5]))
                etime = datetime(int(year_date), int(month_date), day_date, int(time[6:8]), int(time[9:11]))
                prodPrice = 0;
                detail_product_url = 0;

                if stime.hour > 20 and etime.hour < 7: etime = etime + timedelta(days=1)

                for i in range(len(item)):  # 동시간 방영상품 개수

                    # 카테고리 추출
                    category = item[i].find('td', 'desc').find('span', 'category').getText().strip()

                    # 상품명 추출
                    prod = item[i].find('td', 'desc').findAll('a', 'prod_link')
                    if len(prod) == 1:
                        prog_name = prod[0].string
                    elif len(prod) == 2:
                        prog_name = prod[1].string



                    # 상품ID 추출 :prdId
                    prodUrl = item[i].find('div', 'tdWrap').find('a')
                    if prodUrl:
                        prodUrls = str(prodUrl).split("?")
                        if len(prodUrls) >= 2:
                            interUrl = prodUrls[1].split("=")
                            if interUrl:
                                interUrl_2 = interUrl[1].split("&")
                                prodId = interUrl_2[0]


                        # 상품Image 추출 :prodImg(썸네일이미지)
                        #prodImg = item[i].find('div', 'tdWrap').find('img')['src']

                    # 상품 가격 추출 :prodPrice
                    if item[i].find('b'):
                        prodPrice = item[i].find('b').getText()

                        # 상품 상세 페이지 URL : detail_product_URL
                        # 보험상품이 들어갈 경우 ins가 들어가서 현재 정확하게 input으로 들어가지 않음
                        # 1) 보험상품을 제외 data에서 지우기
                        # 2) 보험 상품 url은 다시 가져오기
                    shoppingmall_URL = "http://www.gsshop.com"
                    if item[i].find('div', 'tdWrap').find('a'):
                        product_url = item[i].find('div', 'tdWrap').find('a').attrs["href"]
                        #if product_url이 insu.gsshop(보험)이면 pass 하도록 ..
                        if "insu.gsshop.com" in product_url:
                            continue

                        detail_product_url = str(shoppingmall_URL) + str(product_url)
                        page_source = urllib.request.urlopen(detail_product_url)
                        soup = BeautifulSoup(page_source)

                        if soup.find("div","view_area view_img").find('img')['src']:
                            prodImg = soup.find("div","view_area view_img").find('img')['src']

                    HPList.append([stime, etime, category, prog_name, prodId, prodImg, prodPrice, detail_product_url])

        ##4)현대홈쇼핑 (time,category,prog_name)
        elif ch_name == '현대홈쇼핑':
            def hdshop_crawling(HPList):
                prodImg=0
                page_source = webcrawling()
                find_sc = page_source.tbody.findAll('tr')
                for i in range(len(find_sc)):
                    if find_sc[i].th != None:
                        # 시간 추출
                        time = str(find_sc[i].th).split('>')[1]
                        stime = datetime(int(year_date), int(month_date), day_date, int(time[0:2]),
                                         int(time[3:5]))
                        etime = datetime(int(year_date), int(month_date), day_date, int(time[8:10]),
                                         int(time[11:13]))
                        # if stime.hour > 20 and etime.hour < 7: etime = etime + timedelta(days=1)
                        # if (t == 1 and stime.hour < 5) or (t == 2 and stime.hour >= 5):
                        #     # 카테고리 추출
                        category = find_sc[i].span.string
                        # 상품명 추출
                        prog_name = find_sc[i].dd.a.string
                        # HPList.append([stime,etime,category,prog_name])
                        # 상품ID 추출 :prdId
                        # 상품 상세 페이지 URL : detail_product_URL
                        #prod_Url = find_sc[i].find('div', 'pdtImg2').find('a').attrs["href"]
                    prod_url_r=find_sc[i].find('dd','txt').find('a').attrs["href"]
#                   print(prod_url_r)
                    item = re.findall(r'(=?slitmCd=)(\d*)', prod_url_r)
                    test = item[0][1]
                    prodId = str(test).replace('20', '')
                    shoppingmall_URL = "http://www.hyundaihmall.com"
                    detail_product_URL = str(shoppingmall_URL) + str(prod_url_r)
                    print(detail_product_URL)

                    url = detail_product_URL
                    page_source = urllib.request.urlopen(url)
                    soup = BeautifulSoup(page_source)
                    if soup.find("div","product_info"):
                        prodImg = soup.find("div","product_info").find('img')['src']



                            # 상품Image 추출 :prodImg(썸네일이미지)
                           # prodImg = find_sc[i].find('div', 'pdtImg2').find('img')['src']
                            # 상품 가격 추출 :prodPrice
                    prodPrice = 0
                    if find_sc[i].find('span', 'txtStrong'):
                        prodPrice = find_sc[i].find('span', 'txtStrong').getText()
                        # 상품 상세 페이지 URL : detail_product_URL
                    find_sc[i].find('div', 'pdtImg2').find
                    HPList.append([stime, etime, category, prog_name, prodId, prodImg, prodPrice,detail_product_URL])
                    j = i + 1
                    while (j < len(find_sc)) and (find_sc[j].th == None):
                        prog_name = find_sc[j].dd.a.string.lstrip()
                        HPList.append([stime, etime, category, prog_name, prodId, prodImg, prodPrice,detail_product_URL])
                        j = j + 1
                return (HPList)
           # 00~05시 편성표 추출(전날)
           #  date_t = date_t - timedelta(days=1)
           #  url = "http://www.hyundaihmall.com/front/bmc/brodPordPbdv.do?cnt=0&date=" + str(
           #      date_t.year) + "%02d" % date_t.month + "%02d" % date_t.day
           #  t = 1
           #  HPList = hdshop_crawling(HPList)
            # 06~23시 편성표 추출(당일)
            url = "http://www.hyundaihmall.com/front/bmc/brodPordPbdv.do?cnt=0&date=" + query_date2
            t = 2
            HPList = hdshop_crawling(HPList)



            ##5)롯데홈쇼핑 (time,category,prog_name)
        elif ch_name == '롯데홈쇼핑':
            # url="http://www.lotteimall.com/main/searchTvPgmByDay.lotte?bd_date="+query_date2
            url = "http://www.lotteimall.com/main/viewMain.lotte?dpml_no=6&tab=3&tlog=19000_2"

            driver.get(url)
            soup = BeautifulSoup(driver.page_source)

            #날짜 지정: query_date3(년월일ex)20170325)
            print(query_date3)
            start_date_click = soup.find('ul','rn_tsday_list').find_all("span", {"class": "rn_day"})
            for item in start_date_click:

                if item.text == query_date3:
                    #driver.find_element_by_xpath("//span[@class=rn_day]").click()
                #    driver.find_element_by_link_text(item.text).click()
                    driver.find_element_by_xpath("//*[span='{0}']".format(item.text)).click()

                    # soup = BeautifulSoup(driver.page_source)
                    # find_sc = soup.find_all("div","rn_tsitem_box")
                    # for i in range(len(find_sc)):
                    #     prod_id = i.find("div","rn_tsitem_info").find("a",{"onclick":"goods_no"})
                    #     print(prod_id)
                    #     detailed_url = "http: // www.lotteimall.com / goods / viewGoodsDetail.lotte?goods_no = "+prod_id+"& infw_disp_no_sct_cd = 40 & infw_disp_no = 0 & allViewYn = N"



                    if wait_for_condition(By.LINK_TEXT, "이전 방송상품 보기", 8):
                        driver.find_element_by_link_text("이전 방송상품 보기").click()

                        soup = BeautifulSoup(driver.page_source)
                        find_sc2 = soup.findAll('div', 'rn_tsitem_box')

                    # for i in range(len(find_sc2)):
                    for find_sc2_item in find_sc2:
                        if find_sc2_item.find('a', "rn_tsitem_title"):
                            titleText = find_sc2_item.find('a', "rn_tsitem_title").getText()
                            print(titleText)

                            wait_for_condition(By.LINK_TEXT, titleText, 8)
                            driver.find_element_by_link_text(titleText).click()
                            wait_for_condition(By.ID, "Detailtab1", 8)

                            url = driver.current_url
                            page = urllib.request.urlopen(url)
                            page_source = BeautifulSoup(page)
                            #상세 상품 이미지: _big_product_image
                            big_product_image = page_source.find("div", "bimg hand").find('img')['src']

                            wait_for_condition(By.XPATH, "//img[@alt='편성표']", 4)
                            driver.find_element_by_xpath("//img[@alt='편성표']").click()
                            wait_for_condition(By.LINK_TEXT, "이전 방송상품 보기", 4)
                            driver.find_element_by_link_text("이전 방송상품 보기").click()



            ##6)홈&쇼핑 (time,prog_name)
        elif ch_name == '홈&쇼핑':
            url = "http://www.hnsmall.com/display/tvtable.do?from_date=" + str(
                year_date) + "%2F" + "%02d" % month_date + "%2F" + "%02d" % day_date + "&search_key="
            page_source = urllib.request.urlopen(url)
            soup = BeautifulSoup(page_source)
            find_sc = soup.findAll('td', 'dateTime')
            find_good = soup.findAll('td', 'goods')
            find_price = soup.findAll('p', 'price')
            productSet = soup.findAll('tr')

            for i in range(len(find_sc)):
                if productSet[i].find('td', 'dateTime'):
                    time = productSet[i].find('td', 'dateTime').find('span', 'time').string
                    stime = datetime(int(year_date), int(month_date), day_date, int(time[0:2]), int(time[3:5]))
                    etime = datetime(int(year_date), int(month_date), day_date, int(time[8:10]), int(time[11:13]))
                    if stime.hour > 20 and etime.hour < 7: etime = etime + timedelta(days=1)

                # 상품명 추출
                if productSet[i].find('strong', 'tit'):
                    prog_name = productSet[i].find('strong', 'tit').string

                # 상품ID 추출 :prodId
                if productSet[i].find('td', 'goods'):
                    prodID_info = productSet[i].find('td', 'goods').find('div', 'img')
                    item = re.findall(r'goods_code=(\d*)', str(prodID_info))
                    prodId = item[0]

                    # 상품Image 추출 :prodImg

                    prodImg_info = productSet[i].find('td', 'goods').find('div', 'img')
                    prodImg = prodImg_info.find('img')['src']

                # 상품 가격 추출 :prodPrice
                if productSet[i].find('p', 'price'):
                    prodPrice = productSet[i].find('p', 'price').getText().strip()

                # 상품 상세 페이지 URL : detail_product_URL
                if productSet[i].find('td', 'goods'):
                    detail_product_URL = productSet[i].find('td', 'goods').find('div', 'img').find('a').attrs["href"]

                    page_source = urllib.request.urlopen(detail_product_URL)
                    soup = BeautifulSoup(page_source)
                    if soup.find("div","imgBig"):
                        prodImg= soup.find("div","imgBig").find("img")['src']



                    HPList.append([stime, etime, category, prog_name, prodId, prodImg, prodPrice, detail_product_URL])

        p = p + 1

        print("\n-- HP data insert to DB --")
        for HP in HPList:
            start_time = filter_time(HP[0])
            if ch_name == 'CJ오쇼핑':
                end_time = 'unknown'
                category = HP[1]
                prog_name = HP[2]
            else:
                end_time = filter_time(HP[1])
                if ch_name in ['GS SHOP', '현대홈쇼핑']:
                    category = HP[2]
                    prog_name = HP[3]
                    prodId = HP[4]
                    prodImg = HP[5]
                    prodPrice = HP[6]
                    detail_product_URL = HP[7]
                    p = p + 1
                elif ch_name in ['NS홈쇼핑', '홈&쇼핑', '롯데홈쇼핑']:
                    category = 'none'
                    prog_name = HP[3]
                    prodId = HP[4]
                    prodImg = HP[5]
                    prodPrice = HP[6]
                    detail_product_URL = HP[7]
                    p = p + 1
            print(start_time, end_time, ch_name, category, prog_name, prodId, prodImg, prodPrice, detail_product_URL)
            worksheet.write(p, 0, start_time, date_format)
            worksheet.write(p, 1, end_time, date_format)
            worksheet.write(p, 2, ch_name)
            worksheet.write(p, 3, category)
            worksheet.write(p, 4, prog_name)
            worksheet.write(p, 5, prodId)
            worksheet.write(p, 6, prodImg)
            worksheet.write(p, 7, prodPrice)
            worksheet.write(p, 8, detail_product_URL)

    print("\n### " + ch_name + " (ch." + ch_num + ") EPG Crwaling Done. ###")

workbook.save("EPG.xls")
print("\n#################################################")
print("##################   The END   ##################")
print("#################################################")
