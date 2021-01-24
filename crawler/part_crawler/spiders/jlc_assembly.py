# -*- coding: utf-8 -*-
import scrapy
import xlrd
import logging


class JlcAssemblySpider(scrapy.Spider):
    name = "jlc_assembly"
    allowed_domains = ["jlcpcb.com"]
    start_urls = ["https://jlcpcb.com/componentSearch/uploadComponentInfo"]

    def parse(self, response):
        book = xlrd.open_workbook(file_contents=response.body)
        sheet = book.sheet_by_index(0)
        rows = sheet.get_rows()

        headings = list(next(rows))

        for row in rows:
            data = {}
            for h, x in zip(headings, row):
                data[h.value.lower()] = x.value

            data["sku"] = data["lcsc part"]

            yield data
