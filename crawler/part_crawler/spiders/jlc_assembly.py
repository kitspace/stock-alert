# -*- coding: utf-8 -*-
import scrapy
import xlrd
import logging
from part_crawler.items import Part

expected_headings = [
    "LCSC Part",       #0
    "First Category",  #1
    "Second Category", #2
    "MFR.Part",        #3
    "Package",         #4
    "Solder Joint",    #5
    "Manufacturer",    #6
    "Library Type",    #7
    "Description",     #8
    "Datasheet",       #9
    "Price",           #10
    "Stock",           #11
]


class JlcAssemblySpider(scrapy.Spider):
    name = "jlc_assembly"
    allowed_domains = ["jlcpcb.com"]
    start_urls = ["https://jlcpcb.com/componentSearch/uploadComponentInfo"]

    def parse(self, response):
        book = xlrd.open_workbook(file_contents=response.body)
        sheet = book.sheet_by_index(0)
        rows = sheet.get_rows()

        # make sure the columns haven't changed
        headings = list(next(rows))
        assert [h.value for h in headings] == expected_headings

        row = next(rows)
        r = [x.value for x in row]
        yield Part(vendor="jlc_assembly", sku=r[0], description=r[8], stock=int(r[11]))

