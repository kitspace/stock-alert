# Kitspace Stock Alert

_work in progess_

This is a webapp to notify via email when a part is back in stock at your PCB assembler. The initial version will support JLC Assembly only.

This project consists of a Scrapy crawler and an Elasticsearch instance to hold/index/search the data and set up "alerts" that send out emails depending on stock levels.

## Development

### Set Up

0. Get all the source code
```
git clone https://github.com/kitspace/stock-alert
cd stock-alert
```

1. Install [Docker](https://www.docker.com/get-started) and [docker-compose](https://pypi.org/project/docker-compose/) (on Ubuntu: `snap install docker` and `apt install docker-compose`)


2. Build and run the docker containers:
```
docker-compose up
```

3. To run the crawler do:

```
docker-compose run crawler
```
