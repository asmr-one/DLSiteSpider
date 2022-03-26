from unittest import TestCase

from DLSiteSpider import DLSiteDynamicInfoSpider


class DLSiteDynamicSpiderTest(TestCase):
    def setUp(self):
        self.spider = DLSiteDynamicInfoSpider("RJ354292")

    def testDLCount(self):
        print(self.spider.dl_count)

    def testFetchAttr(self):
        print(self.spider.rate_average_2dp)
        print(self.spider.rate_count)
        print(self.spider.price)
        print(self.spider.review_count)
