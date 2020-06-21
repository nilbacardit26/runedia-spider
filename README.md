# Getting started

## Install dependencies
### Create virtual environment
`python3 -m venv venv`
Source to it
`source venv/bin/activate`
Install dependencies
`pip install -r requirements.txt`

### Run the spider and save the results
`cd runedia_spider/runedia_spider`
`scrapy crawl races_spider -o results.json`

The first race ever recorded in runedia is from November 1993.
result.json will contain all the mountain races from the November 1993 of until
the actual year, celebrated in Spain.
