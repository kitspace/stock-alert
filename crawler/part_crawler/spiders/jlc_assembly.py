# -*- coding: utf-8 -*-
import scrapy
import xlrd

expected_headings = [
    "LCSC Part",
    "MFR.Part",
    "First Category",
    "Second Category",
    "Package",
    "Solder Joint",
    "Manufacturer",
    "Library Type",
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
        headings = next(rows)
        assert [h.value for h in headings] == expected_headings

        for row in rows:
            r = [x.value for x in row]
            yield {
                "sku": r[0],
                "search": r[1],
                "category": r[2],
                "secondary_category": r[3],
                "package": r[4],
                "number_of_solder_joints": int(r[5]),
                "manufacturer": r[6],
                "jlc_assembly_type": r[7],
            }
