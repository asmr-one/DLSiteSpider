import datetime
from unittest import TestCase

from datasize import DataSize

from DLSiteSpider import DLSiteStaticInfoSpider


class DLSiteStaticSpiderTestSpecial(TestCase):
    def setUp(self):
        self.spider = DLSiteStaticInfoSpider("RJ376004")

    def testRelease(self):
        self.assertEqual(datetime.date(year=2022, month=2, day=27), self.spider.release)

    def testNoneExistWorkSize(self):
        self.assertEqual(
            DataSize(0),
            DLSiteStaticInfoSpider("RJ211970").size
        )


class DLSiteStaticSpiderTest(TestCase):
    def setUp(self):
        self.spider = DLSiteStaticInfoSpider("RJ354292")

    def testTitle(self):
        self.assertEqual("【眠音りま】やや屋放送局第12回後編【乙倉ゅい】", self.spider.title)

    def testCircle(self):
        self.assertEqual("やや屋", self.spider.circle)

    def testNSFW(self):
        self.assertEqual(True, self.spider.nsfw)

    def testRelease(self):
        self.assertEqual(datetime.date(year=2021, month=11, day=4), self.spider.release)

    def testTags(self):
        self.assertEqual(["萌", "治愈", "癖好/性趣", "淫语"], self.spider.tags)

    def testVAs(self):
        self.assertEqual(["眠音りま", "乙倉ゅい"], self.spider.vas)

    def testSize(self):
        self.assertEqual(DataSize('19.63MB'), self.spider.size)

    def testGirlSite(self):
        """
        测试乙女向版块解析能力
        :return:
        """
        spider = DLSiteStaticInfoSpider("RJ377005")
        self.assertEqual(DataSize('231.03MB'), spider.size)
