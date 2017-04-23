
import arrow
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By

from product_info import ProductInfo
from utils import wait_for_condition, build_soup_from_page, get_text_from_child


def get_prod_url_by_prod_id(prod_id):
    url = 'http://www.lotteimall.com/goods/viewGoodsDetail.lotte?goods_no={0}'.format(
        prod_id
    )
    return url


def get_image_url_by_prod_id(prod_id):
    url = 'http://image2.lotteimall.com/goods/{0}/{1}/{2}/{3}_H1.jpg'.format(
        prod_id[6:8],
        prod_id[4:6],
        prod_id[2:4],
        prod_id,
    )
    return url


def lotte_home_shopping(window_arrow):
    print ('LOTTE')
    url = "http://www.lotteimall.com/main/viewMain.lotte?dpml_no=6&tab=3&tlog=19000_2"
    driver = webdriver.Firefox()
    driver.get(url)
    # soup = build_soup(driver.page_source)

    date_format = window_arrow.format('MM.DD')
    wait_for_condition(driver, By.XPATH, "//span[@class='rn_day']", 5)
    the_day_element = None
    for element in driver.find_elements_by_xpath("//span[@class='rn_day']"):
        if element.text == date_format:
            the_day_element = element
            break
    if not the_day_element:
        return
    the_day_element.click()

    if wait_for_condition(driver, By.LINK_TEXT, "이전 방송상품 보기", 2):
        prev_see_item = driver.find_element_by_link_text("이전 방송상품 보기")
        try:
            if prev_see_item.is_displayed():
                driver.find_element_by_link_text("이전 방송상품 보기").click()
        except StaleElementReferenceException:
            pass

    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = build_soup_from_page(html)

    item_list = soup.find('div', {'class': 'rn_tsitem_list'}).find_all('div', {'class': 'rn_tsitem_box'})
    for item in item_list:
        prod_id = ''
        the_time = ''
        title = ''
        price = ''
        prod_detail_url = ''
        image_url = ''

        time_item = item.find('div', {'class': 'rn_tsitem_caption'}).find('span')
        the_time = get_text_from_child(time_item)

        view_list = soup.find_all('div', {'class': 'rn_tsitem_view'})
        for view_item in view_list:
            image = view_item.find('img')
            if image:
                prod_id = image['src'].split('/')[-1].split('_')[0]

        info_item = item.find('div', {'class': 'rn_tsitem_info'})
        title_item = info_item.find('a')
        if title_item:
            title = get_text_from_child(title_item)
        price_info_item = info_item.find('div', {'class': 'rn_tsitem_priceinfo'})
        if price_info_item:
            price_item = price_info_item.find('span', {'class': 'rn_tsitem_price'})
            if price_item:
                price = get_text_from_child(price_item)

        prod_detail_url = get_prod_url_by_prod_id(prod_id)
        image_url = get_image_url_by_prod_id(prod_id)

        yield ProductInfo(
            name=title,
            category='',
            start_time=the_time.split(' ~ ')[0],
            end_time=the_time.split(' ~ ')[1],
            detail_product_url=prod_detail_url,
            price=price,
            product_id=prod_id,
            image=image_url,
        )


lotte_home_shopping(arrow.get('2017-04-10'))
