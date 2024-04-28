# Web Crawler - Scrapy: Tutorials and How to use Scrapy to crawl comments from Facebook fanpage


## 1. Introduction and Basic Concepts

- **Scrapy** - a fast high-level web crawling and web scraping framework, used to crawl websites and extract structured data from their pages.

- **Installation**
    > pip install Scrapy
  
- **Things that are good to know**
  - [lxml]()
  - [parsel]()
  - [w3lib]()
  - [twisted]()
  - [crytography]()
  - [pyOpenSSL]()

- **Basic Concepts**
  - **Spider** - user-defined classes and uses to scrape information from a website (or a group of websites) - **custom behaviour**.
  - Items
  - Pipeline
  - Middleware
  - Settings

- **The scraping cycle**
  1. Generate the initial Requests to crawl the first URLs, and specify a callback function.
  2. In the callback function, you parse the response (web page) and return item objects.
  3. In callback functions, you parse the page contents and generate items with the parsed data.
  4. The items returned from the spider will be persisted to a **database** (in some **Item Pipeline**) or written to a **file** using **Feed exports**.

## 2. Simple Example

1. Creating a new Scrapy project

    > scrapy startproject tutorial
   
    - directory:
   
    >
        tutorial/
         
            scrapy.cfg            # deploy configuration file
        
            tutorial/             # project's Python module, you'll import your code from here
         
                __init__.py
        
                items.py          # project items definition file
        
                middlewares.py    # project middlewares file
        
                pipelines.py      # project pipelines file
        
                settings.py       # project settings file
        
                spiders/          # a directory where you'll later put your spiders
                    __init__.py

2. Writing a Spider to crawl a site and extract data
   
   - Must subclass Spider and define the initial requests to make.
   - Attributes and Methods
     - **name** - identifies the Spider, must be unique.
     - **start_requests()** - return an iterable of Requests which the Spider will begin to crawl from.
     - **start_urls** - list of URLs will be used by the **start_requests()** method. (shortcut)
     - **parse()** - be called to handle the response downloaded for each of the requests made.
       - parses the response
       - extract the scraped data as dicts
       - findi new URLs to follow 
       - create new requests (Request).
   - How to run spider
     > scrapy crawl quotes

3. Exporting the scraped data (using the command line)

   - Use dev tool of browser and Scrapy selectors ([CSS](),[XPath](),...) to manipulate **response object**.
   - Store the scraped data is by using [Feed exports](https://docs.scrapy.org/en/latest/topics/feed-exports.html#topics-feed-exports)
     > scrapy crawl quotes -O quotes.json
4. Changing spider to recursively follow links
    - Example
   >
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

## 3. Facebook Crawler

## 4. Insights