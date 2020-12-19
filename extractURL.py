from urllib.request import urlopen

page = urlopen("https://www.un.org/en/climatechange")
print(page.headers) #extract URL headers
print()
#extract source code of URL
sourceCode = page.read()
print(sourceCode)
