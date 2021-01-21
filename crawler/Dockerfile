FROM python:3.9

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["scrapy"]
CMD ["crawl", "jlc_assembly", "-o", "jlc_assembly.jl"]
