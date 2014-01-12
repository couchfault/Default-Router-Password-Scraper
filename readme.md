Let me start off by saying that I take no credit for anything in the bs4 folder, that is all just the BeautifulSoup module. However, since it is not included by default I added it so people could just download and run without errors.

There is no installation necessary, just clone the repository.

Usage:

import scrape_passwords
users = scrape_passwords.get_all_users()
passwords = scrape_passwords.get_all_passwords()