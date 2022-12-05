# the list "walks" is already defined
# your code here
total_distance = 0
amount_walks = len(walks)
for walk in walks:
    total_distance += walk.get("distance", 0)

print(total_distance // amount_walks)
