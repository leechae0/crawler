from datetime import timedelta
from urllib.parse import parse_qs
from urllib.parse import urlparse

import requests
import xmltodict
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def extract_value_from_url_key(url, key):
    the_value = ''
    query = urlparse(url)[4]
    parsed_query_dict = parse_qs(query)
    if parsed_query_dict.get(key):
        the_value = parsed_query_dict[key][0]
    return the_value


def xml_to_dict(table):
    return xmltodict.parse(str(table))


def build_soup_from_page(page):
    soup = BeautifulSoup(page, "lxml")
    return soup


def build_soup(url):
    print('BUILD SOUP FROM URL : {0}'.format(url))
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def get_text(tag):
    if not tag.name and tag.strip():
        return tag.strip()
    return ''


def get_text_from_child(tag):
    for child in tag.contents:
        the_text = get_text(child)
        if the_text:
            return the_text
    return ''


def safeunicode(s):
    try:
        return s.encode('latin-1').decode('cp949')
    except UnicodeEncodeError:
        return s


def filter_time(time):
    if time.minute % 5 == 1:
        time = time - timedelta(minutes=1)
    elif time.minute % 5 == 4:
        time = time + timedelta(minutes=1)
    return time


def wait_for_condition(driver, condition_type, condition, timeout=5):
    try:
        element_present = ec.presence_of_element_located((condition_type, condition))
        WebDriverWait(driver, timeout).until(element_present)
        return True
    except TimeoutException:
        print('Waited for {0} secs. Cannot meet the condition. Ignore It.'.format(timeout))
        return False
