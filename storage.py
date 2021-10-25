import csv

allArticles = []

with open("articles.csv", encoding = "utf-8") as f:
    reader = csv.reader(f)
    data = list(reader)
    allArticles = data[1:]

liked_articles = []
unliked_articles = []