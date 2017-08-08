import urllib

from bs4 import BeautifulSoup
from datetime import timedelta

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import arrow
import modular_example


class Response(object):
    def __init__(self, id=None, name=None, category=None):
        self.id = id
        self.name = name
        self.category = category


class BaseCrawler(object):

    HD_CRAWLER_ID = 1
    LT_CRAWLER_ID = 2

    def __init__(self, crawler_id=None):
        self.crawler_id = crawler_id
        self.driver = webdriver.Firefox()

    def _webcrawling(self, url):
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page)
        return soup

    def _safeunicode(self, s):
        s._webcrawling('aaa')
        try:
            return s.encode('latin-1').decode('cp949')
        except UnicodeEncodeError:
            return s

    def _filter_time(self, time):
        if (time.minute % 5 == 1):
            time = time - timedelta(minutes=1)
        elif (time.minute % 5 == 4):
            time = time + timedelta(minutes=1)
        return time

    def _wait_for_condition(self, condition_type, condition, timeout):
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((condition_type, condition)))
        except TimeoutException:
            print('Waited for {0} secs. Cannot meet the condition. Ignore It.')


    def collect_response(self):
        processeed_response = []
        for response in self._yield_response():
            # TODO: do something.
            processeed_response.append(response)
        return processeed_response



    def _yield_response(self):
        raise NotImplementedError()

    @staticmethod
    def new_crawler(crawler_id):
        if crawler_id == BaseCrawler.HD_CRAWLER_ID:
            return HDCrawler(BaseCrawler.HD_CRAWLER_ID)
        elif crawler_id == BaseCrawler.LT_CRAWLER_ID:
            return LTCrawler(BaseCrawler.HD_CRAWLER_ID)

    pass

class HDCrawler(BaseCrawler):
    def __init__(self, crawler_id):
        super().__init__(crawler_id)

    if __name__ == '__main__':
        def _yield_response(self):
            pass
            # Request to the Hyundai Home Shopping
            # Crawl Data
            # Data manipulation
            # Make reponse
            yield Response(id=1, name='Sample', category='Sports')


class LTCrawler(BaseCrawler):
    def __init__(self, crawler_id):
        super().__init__(crawler_id)


def iam_a_caller():

    the_time = '2017-03-31 12:37:00'
    the_time = arrow.get(the_time).replace(hour=0, minute=0, second=0)
    the_time = the_time.replace(days=-1)

    result_list = []
    hd_crawler = BaseCrawler.new_crawler(crawler_id=BaseCrawler.HD_CRAWLER_ID)
    result_list.append(hd_crawler.collect_response())

    lt_crawler = BaseCrawler.new_crawler(crawler_id=BaseCrawler.LT_CRAWLER_ID)
    result_list.append(lt_crawler.collect_response())


if __name__ == "__main__":
    iam_a_caller()