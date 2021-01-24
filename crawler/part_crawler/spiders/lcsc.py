import scrapy
import logging

from elasticsearch import Elasticsearch, helpers


class LcscSpider(scrapy.Spider):
    name = "lcsc"
    lcsc_url = "https://lcsc.com/pre_search/link?type=lcsc&&value={sku}"

    def start_requests(self):
        es_settings = dict()
        es_servers = self.settings.get("ELASTICSEARCH_SERVERS", "localhost:9200")
        es_servers = es_servers if isinstance(es_servers, list) else [es_servers]
        es_timeout = self.settings.get("ELASTICSEARCH_TIMEOUT", 60)
        es_settings["hosts"] = es_servers
        es_settings["timeout"] = es_timeout

        if (
            "ELASTICSEARCH_USERNAME" in self.settings
            and "ELASTICSEARCH_PASSWORD" in self.settings
        ):
            es_settings["http_auth"] = (
                self.settings["ELASTICSEARCH_USERNAME"],
                self.settings["ELASTICSEARCH_PASSWORD"],
            )

        es_settings["use_ssl"] = True
        es_settings["verify_certs"] = False

        es = Elasticsearch(**es_settings)
        results = helpers.scan(
            es,
            query={"query": {"match_all": {}}},
            index=f"{self.settings['ELASTICSEARCH_INDEX']}-*",
        )

        for r in results:
            sku = r["_source"]["sku"]
            yield scrapy.Request(
                self.lcsc_url.format(sku=sku),
                callback=self.parse_lcsc_page,
                meta={"data": {"sku": sku}},
            )

    def parse_lcsc_page(self, response):
        sku = response.meta["data"]["sku"]
        image_url = response.css(".main-img.lazy").xpath("@data-original").get()
        if image_url is not None:
            yield {"sku": sku, "image_urls": [image_url]}
