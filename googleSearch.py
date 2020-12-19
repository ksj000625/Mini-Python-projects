from googlesearch import search

query = input("Enter search word : ")
for i in search(query, start=0,pause=3):
    print(i)