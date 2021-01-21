# -*- coding: utf-8 -*-
import scrapy
import json


class SeeedSpider(scrapy.Spider):
    name = "seeed"
    allowed_domains = ["seeedstudio.com"]

    api_url = "https://sapi.seeedstudio.com/fusion/opl/list?guid=3374C42EFBDB45E6F5F21A94A80D534E&appid=en.pc.bazaar"
    formdata = {
        "page_offset": "1",
        "page_length": "30",
        "type": "HQCHIP",
        "keyword": "",
    }

    def start_requests(self):
        return [
            scrapy.FormRequest(
                self.api_url,
                callback=self.parse,
                formdata={**self.formdata, "category": "Capacitors"},
                meta={"category": "Capacitors"},
            ),
            scrapy.FormRequest(
                self.api_url,
                callback=self.parse,
                formdata={**self.formdata, "category": "Resistors"},
                meta={"category": "Resistors"},
            ),
        ]

    def parse(self, response):
        # re-do the request if we get a "too many requests" response
        # scrapy handles the backing off logic for us?
        if response.status == 429:
            yield response.request
            return

        category = response.meta["category"]
        body = json.loads(response.body_as_unicode())

        # return the parts we got from this request
        parts = body["data"]["list"]
        assert len(parts) > 0
        for part in parts:
            yield part

        # return a request to crawl the next page if not at the end yet
        total_pages = int(body["data"]["page"]["page_count"])
        current_page = int(body["data"]["page"]["page_offset"])
        if current_page < total_pages:
            yield scrapy.FormRequest(
                self.api_url,
                callback=self.parse,
                formdata={
                    **self.formdata,
                    "category": category,
                    "page_offset": str(current_page + 1),
                },
                meta={"category": category},
            )
