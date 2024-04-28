from scrapy.http import FormRequest
from pathlib import Path
from scrapy import Spider, Request
import scrapy
from scrapy.selector import Selector
from fb_comments_crawler.items import FbCommentsCrawlerItem


class cmtSpider(Spider):
	name = 'comments'
	allowed_domains = ["facebook.com", "www.facebook.com", "m.facebook.com", "mbasic.facebook.com"]
	start_urls = [
		'https://mbasic.facebook.com/login.php',
		# "https://mbasic.facebook.com/photo?fbid=755415003461040&set=a.569288308740378",
	]

	post_urls = [
		"https://mbasic.facebook.com/photo?fbid=755415003461040&set=a.569288308740378",
		# "https://mbasic.facebook.com/story.php?story_fbid=pfbid02eBvF5DVHGAaSfbG79ZpTtqKbA7DWN9jZaj84pyqMBcFfGhXn5qJCaaqeYxmyMzdHl&id=100069776410903&eav=AfaIs9K6QCG6oOZXIDDdxVFIHaL9Q25kMGybYpzylDKETVlfmi3bE4UL_FjpR3xVNCE&p=10&av=61558882323464&paipv=0",
		# "https://mbasic.facebook.com/story.php?story_fbid=pfbid02eBvF5DVHGAaSfbG79ZpTtqKbA7DWN9jZaj84pyqMBcFfGhXn5qJCaaqeYxmyMzdHl&id=100069776410903&eav=AfaIs9K6QCG6oOZXIDDdxVFIHaL9Q25kMGybYpzylDKETVlfmi3bE4UL_FjpR3xVNCE&p=10&av=61558882323464&paipv=0",
		# "https://mbasic.facebook.com/story.php?story_fbid=pfbid0aLUXtYZTQraYSgYdFyPWvMqNG4Sj5FWUNx1XsPgwkaWsjVR1uS5VVx9ypHKxf24ml&id=100069776410903&eav=AfZnXGQQ9tN6udOujTmjC3GVEbh_VgIdyzRxXudfY1PJNZSEBGifdGU2EwNuPhROdas&p=10&av=61558882323464&paipv=0",
		]

	# login
	def parse(self, response):
		print("parse-"*10)
		# Extract CSRF token and other necessary fields from the login form
		csrf_token = response.css('input[name="fb_dtsg"]::attr(value)').get()
		# Assuming 'email' and 'pass' are the input names for the username and password fields
		return FormRequest.from_response(
			response,
			formdata={
				'email': 'idahcmus227nvc@gmail.com',
				'pass': 'VNUhcmus227#',
				'fb_dtsg': csrf_token,
			},
			callback=self.after_login
		)

	def after_login(self, response):
		print("after_login+"*10)
		# Check login success before scraping
		if "login_error" in response.url:
			self.log("Login failed", level=scrapy.logging.ERROR)
		else:
			self.log("Login succeeded")
		# Proceed with scraping after successful login
		# For example, navigate to the target page
		yield Request(url=self.post_urls[0],callback=self.parse_content)
		return

	# for the first page load
	def parse_content(self, response):

		print("parse_content+"*10)
		content = Selector(response).xpath(
			'//*[@id[starts-with(., "ufi")]]/div'
		)

		first_generation_descendants = content.xpath('./*')
		print(len(first_generation_descendants))

		# comment content section doesn't have id attribute
		comment_class = None
		for f in first_generation_descendants:

			_class = f.xpath('@class').get()
			_id = f.xpath('@id').get()

			if _id is None:
				comment_class = _class

		print(comment_class)

		if comment_class is not None:
			comment_selector = content.xpath(f'div[@class="{comment_class}"]')

			# count the numbers of its children (first-class)
			# print(len(comment_selector.xpath('./*')))

			# list of first-class children
			com = comment_selector.xpath('./*')

			# extract links to the previous and the next comments page
			see_prev = comment_selector.xpath('.//div[starts-with(@id,"see_prev")]').get()
			see_next = comment_selector.xpath('.//div[starts-with(@id,"see_next")]')

			# # handle comments sections
			# for c in com:
			# 	print("+"*30)
			# 	_comments = FbCommentsCrawlerItem()
			#
			# 	_comments['Id'] = c.xpath('@id').get()
			# 	if _comments['Id'].startswith('see_prev'):
			# 		continue
			# 	if _comments['Id'].startswith('see_next'):
			# 		print("see_next")
			# 		continue
			#
			# 	# print(c.xpath('div').get())
			# 	_comments['name'] = c.xpath('div/h3/a/text()').get()
			# 	_comments['cmt'] = c.xpath('div/div/text()').get()
			# 	_comments['time'] = c.xpath('div/div[@class="_52jc _52j9 _52jg"]/abbr/text()').get()
			#
			# 	# yield _comments

			'''
			task:
			navigate to the next page and get its content
			'''

			# Extracting the link for the "see next" page
			see_next_link = see_next.xpath('a/@href').get()

			if see_next_link:
				print(see_next_link)
				# If the link exists, yield a request to parse the next page
				next_url = response.urljoin(see_next_link)
				print("="*30)
				print(next_url)

				yield Request(url=next_url, callback=self.parse_content)

		print("-done"*10)

		return

	 # vo_ngoc_tri
	def parse_basic_cmt(self, response):
		comments = Selector(response).xpath(
			'//*[@id="ufi_pfbid0aLUXtYZTQraYSgYdFyPWvMqNG4Sj5FWUNx1XsPgwkaWsjVR1uS5VVx9ypHKxf24ml"]/div/div[4]/div')

		print("=" * 40)
		print(len(comments))
		print("=" * 40)

		for comment in comments:
			item = FbCommentsCrawlerItem()

			item['name'] = comment.xpath('div/h3/a/text()').get()

			item['cmt'] = comment.xpath('div/div/text()').get()

			item['time'] = comment.xpath('div/div[@class="_52jc _52j9 _52jg"]/abbr/text()').get()

			yield item