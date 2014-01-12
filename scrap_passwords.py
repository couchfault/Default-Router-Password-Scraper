#!/usr/bin/env python
import re
import urllib
import urllib2
import threading
from bs4 import BeautifulSoup
class PasswordPage(threading.Thread):
	def __init__(self, url, router_type):
		threading.Thread.__init__(self)
		self.site_url = url
		self.router_type = router_type
		self.pagecontents = None
		self.html_parser = None
		self.users_list = None
		self.passwords_list = None
		self.start()
	def run(self):
		self.pagecontents = self.get_site_contents()
		self.html_parser = BeautifulSoup(self.pagecontents)
		self.users_list = self.grab_site_usernames()
		self.passwords_list = self.grab_site_passwords()
	def get_site_contents(self):
		data = {
			"findpass":"1",
			"router":self.router_type,
			"findpassword":"Find Password"
		}
		resp = post_page(self.site_url, data)
		return resp
	def grab_site_usernames(self):
		table = self.html_parser.find("table")
		cols = [header.string for header in self.html_parser.find('thead').findAll('th')]
		col_idx = cols.index('Username')
		col_values = [td[col_idx].string for td in [tr.findAll('td') for tr in self.html_parser.find('tbody').findAll('tr')]]
		return col_values

	def grab_site_passwords(self):
		table = self.html_parser.find("table")
		cols = [header.string for header in self.html_parser.find('thead').findAll('th')]
		col_idx = cols.index('Password')
		col_values = [td[col_idx].string for td in [tr.findAll('td') for tr in self.html_parser.find('tbody').findAll('tr')]]
		return col_values
def segment(items, chunk_size):
    return [items[i:i+chunk_size] for i in range(0, len(items), chunk_size)]
def post_page(url, data):
	req = urllib2.urlopen(url, urllib.urlencode(data))
	resp = req.read()
	return resp

def get_page(url):
	req = urllib2.urlopen(url)
	resp = req.read()
	return resp

def get_router_types():
	page_html = get_page("http://www.routerpasswords.com")
	parser = BeautifulSoup(page_html)
	menu = parser.findAll("option")
	router_types = [option.get('value') for option in parser.findAll('option')]
	return router_types

def get_all_passwords():
	r_types = get_router_types()
	passwords = []
	segments_r_types = segment(r_types, 100) # I had to handle the pages 100 at a time because too many gives errors. I also don't want to put too much stress on the website
	for types in segments_r_types:
		pass_pages = []
		for t in types:
			pass_pages.append(PasswordPage("http://www.routerpasswords.com", t))
		for pass_page in pass_pages:
			while pass_page.passwords_list==None:
				pass
			print pass_page.passwords_list
			passwords += pass_page.passwords_list
	return passwords
def get_all_users():
	r_types = get_router_types()
	users = []
	segments_r_types = segment(r_types, 100) # I had to handle the pages 100 at a time because too many gives errors. I also don't want to put too much stress on the website
	for types in segments_r_types:
		pass_pages = []
		for t in types:
			pass_pages.append(PasswordPage("http://www.routerpasswords.com", t))
		for pass_page in pass_pages:
			while pass_page.users_list==None:
				pass
			print pass_page.users_list
			users += pass_page.users_list
	return users