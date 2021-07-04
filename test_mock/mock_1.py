# -*- coding: utf-8 -*-
# @Author  : Ming
# @File    : mock_1.py
import json
import sys

from mitmproxy import ctx, http
from mitmproxy.tools.main import mitmdump


class Counter:
    def __init__(self):
        self.num = 0

    def request(self, flow:http.HTTPFlow):
        self.num = self.num + 1
        ctx.log.info("We've seen %d flows" % self.num)

    def response(self, flow:http.HTTPFlow):
        if "https://stock.xueqiu.com/v5/stock/batch/quote.json?_t=" in flow.request.pretty_url:
            data = json.loads(flow.response.text)
            datas=data["data"]["items"][1]["quote"]["name"]
            data["data"]["items"][1]["quote"]["name"] +=datas
            data["data"]["items"][2]["quote"]["name"] = ""
            flow.response.text = json.dumps(data)


addons = [
    Counter()
]
if __name__ == '__main__':

    sys.argv = [__file__, "-s", __file__]
    #
    # 官方要求必须主线程
    mitmdump()