import dataclasses
import requests
import logging

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class DLSiteDynamicInfoSpider:
    product_id: str
    session: requests.Session = requests.Session()
    # work around dynamic info
    dynamic_info_url: str = "https://www.dlsite.com/maniax-touch/product/info/ajax?product_id={product_id}"
    _json_response: dict = None

    @property
    def url(self):
        return self.dynamic_info_url.format(product_id=self.product_id)

    def _fetch(self):
        response = self.session.get(self.url)
        self._json_response = response.json()[self.product_id]

    @property
    def json(self):
        """
        {"RJ354292":{"site_id":"maniax","site_id_touch":"maniaxtouch","maker_id":"RG43277","affiliate_deny":0,
        "dl_count":"42","wishlist_count":"21","dl_format":0,"rank":[],"rate_average":5,"rate_average_2dp":4.64,
        "rate_average_star":50,"rate_count":14,"rate_count_detail":[{"review_point":1,"count":0,"ratio":0},
        {"review_point":2,"count":0,"ratio":0},{"review_point":3,"count":2,"ratio":14},{"review_point":4,"count":1,
        "ratio":7},{"review_point":5,"count":11,"ratio":78}],"review_count":0,"price":220,"price_without_tax":200,
        "price_str":"220","default_point_rate":10,"default_point":20,"product_point_rate":null,
        "dlsiteplay_work":true,"is_sale":true,"on_sale":1,"is_discount":false,"is_pointup":false,"gift":[],
        "is_rental":false,"work_rentals":[],"upgrade_min_price":110,
        "down_url":"https:\/\/www.dlsite.com\/maniax-touch\/download\/filelist\/=\/product_id\/RJ354292.html",
        "is_tartget":null,"title_id":null,"title_name":null,"is_title_completed":false,"bulkbuy_key":null,"bonuses":[
        ],"is_limit_work":false,"is_sold_out":false,"limit_stock":0,"is_reserve_work":false,"is_reservable":false,
        "is_timesale":false,"timesale_stock":0,"is_free":false,"is_oly":false,"is_led":false,"translation_info":{
        "is_translation_agree":false,"is_volunteer":false,"is_original":true,"is_parent":false,"is_child":false,
        "original_workno":null,"parent_workno":null,"child_worknos":[],"lang":null,"production_trade_price_rate":0},
        "work_name":"\u3010\u7720\u97f3\u308a\u307e\u3011\u3084\u3084\u5c4b\u653e\u9001\u5c40\u7b2c12\u56de\u5f8c
        \u7de8\u3010\u4e59\u5009\u3085\u3044\u3011",
        "work_image":"\/\/img.dlsite.jp\/modpub\/images2\/work\/doujin\/RJ355000\/RJ354292_img_main.jpg",
        "sales_end_info":null,"voice_pack":null,"regist_date":"2021-11-04 16:00:00","locale_price":{"en_US":1.91,
        "":1.44,"zh_TW":53.66,"zh_CN":12.09,"ko_KR":2316},"locale_price_str":{"en_US":"$1.91<i>&nbsp;USD<\/i>",
        "":"1.44","zh_TW":"<i>NT$<\/i>53.66","zh_CN":"12.09<i>&nbsp;RMB<\/i>","ko_KR":"2,316<i>&nbsp;\uc6d0<\/i>"},
        "work_type":"SOU","dl_count_total":0,"dl_count_items":[],"default_point_str":"20"}}
        """
        if not self._json_response:
            self._fetch()

        return self._json_response

    @property
    def dl_count(self) -> int:
        return int(self.json["dl_count"])

    def __getattr__(self, item):
        """
        available attributes:
        site_id, side_id_touch, maker_id, affiliate_deny, dl_count, wishlist_count, dl_format, rank, rate_average,
        rate_average_2dp, rate_average_star, rate_count, rate_count_detail, review_count, price, price_without_tax,
        price_str, default_point_rate, default_point, product_point_rate, dlsiteplay_work, is_sale, on_sale,
        is_discount, is_pointup, gift, is_rental, work_rentals, upgrade_min_price, down_url, is_tartget, title_id,
        title_name, is_title_completed, bulkbuy_key, bonuses, is_limit_work, is_sold_out, limit_stock,
        is_reserve_work, is_reservable, is_timesale, timesale_stock, is_free, is_oly, is_led, translation_info,
        work_name, work_image, sales_end_info, voice_pack, regist_date, locale_price, locale_price_str, work_type,
        dl_count_total, dl_count_items, default_point_str
        :param item:
        :return:
        """
        return self.json[item]
