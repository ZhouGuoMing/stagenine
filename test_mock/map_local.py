# -*- coding: utf-8 -*-
# @Author  : Ming
# @File    : map_local.py
import json
import sys
from mitmproxy import ctx, http
from mitmproxy.tools.main import mitmdump


class Counter:
    def __init__(self):
        self.num = 0

    def request(self, flow: http.HTTPFlow):
        self.num = self.num + 1
        ctx.log.info("We've seen %d flows" % self.num)

    def response(self, flow: http.HTTPFlow):
        if "https://stock.xueqiu.com/v5/stock/batch/quote.json?_t=" in flow.request.pretty_url:
            with open("xueqiu.json", encoding="utf-8") as f:
                data = json.load(f)
                flow.response.text=json.dumps(data)



addons = [
    Counter()
]
if __name__ == '__main__':

    sys.argv = [__file__, "-s", __file__]
    #
    # 官方要求必须主线程
    mitmdump()