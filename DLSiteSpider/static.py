import dataclasses
import datetime
import requests

from typing import List
from bs4 import BeautifulSoup
from datasize import DataSize
from DLSiteSpider.utils import onException
import logging

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class DLSiteStaticInfoSpider:
    product_id: str
    locale: str = "locale=zh-cn"
    session: requests.Session = requests.Session()
    # work around static info
    _static_info_url: str = "https://www.dlsite.com/maniax/work/=/product_id/{product_id}.html"
    _html: str = ""
    _soup: BeautifulSoup = None

    @property
    def static_info_url(self):
        return self._static_info_url.format(product_id=self.product_id)

    def _fetchPage(self):
        self._html = self.session.get(
            self.static_info_url.format(product_id=self.product_id),
            cookies={"locale": "zh-cn"}
        ).text

    @property
    def html(self):
        if not self._html:
            self._fetchPage()

        return self._html

    @property
    def soup(self):
        if not self._soup:
            self._soup = BeautifulSoup(self.html, "lxml")

        return self._soup

    @property
    def title(self) -> str:
        # work.title = $(`a[href="${url}"] span`).first().text();
        return self.soup.find("a", href=self.static_info_url).find("span").text

    @property
    def release(self) -> datetime.date:
        work_outline = self.soup.select_one("#work_outline")
        # 2021年11月04日 0点
        release = work_outline.find("th", text="贩卖日").parent.find("td").text.strip()
        # 2021年11月04日
        release = release.split(" ")[0]
        # 2021-11-04
        release = release.replace("年", "-").replace("月", "-").replace("日", "")
        return datetime.datetime.strptime(release, "%Y-%m-%d").date()

    @property
    @onException(None)
    def circle(self) -> str:
        circle_element = self.soup.find("span", class_="maker_name").find("a")
        circle_name = circle_element.text

        return circle_name

    @property
    @onException(None)
    def nsfw(self) -> bool:
        work_outline = self.soup.select_one("#work_outline")
        nsfw = work_outline.find("th", text="年龄指定").parent.find("td").text.strip()
        nsfw = True if nsfw == "18禁" else False
        return nsfw

    @property
    @onException([])
    def tags(self) -> List[str]:
        work_outline = self.soup.select_one("#work_outline")
        tags = []
        for tag_element in work_outline.find("th", text="分类").parent.find("td").find("div").find_all("a"):
            tag_name = tag_element.text.strip()
            tags.append(tag_name)

        return tags

    @property
    @onException([])
    def vas(self) -> List[str]:
        vas = []
        work_outline = self.soup.select_one("#work_outline")
        for va_element in work_outline.find("th", text="声优").parent.find("td").find_all("a"):
            va_name = va_element.text.strip()
            vas.append(va_name)

        return vas

    @property
    @onException(DataSize(0))
    def size(self) -> DataSize:
        work_outline = self.soup.select_one("#work_outline")
        size = work_outline.find("th", text="文件容量").parent.find("td").text

        # 边界情况解决
        size = ''.join(filter(str.isascii, size)).strip()

        return DataSize(size)
