import csv
import numpy

games = set()
data = []

with open('steam-200k.csv', 'rb') as data_original:
    reader = csv.reader(data_original, delimiter=',', quotechar='\"')
    for row in reader:
        user_id, name, type, value, _ = row
        if type == 'play':
            games.add(name)
            data.append((user_id, name, value))

name_to_id = {name: i for i, name in enumerate(games)}

with open('game_ratings.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
    for point in data:
        user_id, name, value = point
        game_id = name_to_id[name]
        writer.writerow([user_id, game_id, value])

with open('game_titles.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
    for name, i in name_to_id.iteritems():
        writer.writerow([i, name])

ratings = []
with open('game_ratings.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    for row in reader:
        user_id, game_id, value = row
        ratings.append(float(value))

for rating in ratings[0:1000]:
    print rating

print numpy.mean(ratings)
print numpy.std(ratings)

