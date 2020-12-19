import pyshorteners
url = input("Enter URL: ")
shortURL = pyshorteners.Shortener()
link = shortURL.tinyurl.short(url)
print(link)