import random
import string

class URLShortener:
   def __init__(self):
       self.url_mapping = {}
       self.url_reverseMapping = {}
       self.short_length = 6  # You can adjust the desired length of the short URL

   def generate_random_short_url(self):
       characters = string.ascii_letters + string.digits
       return 'http.bit.ly/'+''.join(random.choice(characters) for _ in range(self.short_length))

   def shorten_url(self, long_url):
       if long_url in self.url_mapping:
           return self.url_mapping[long_url]

       short_url = self.generate_random_short_url()
       self.url_mapping[long_url] = short_url
       self.url_reverseMapping[short_url] = long_url
       return short_url
