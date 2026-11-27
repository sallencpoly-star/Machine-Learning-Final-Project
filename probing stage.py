# Data Probing:
# Step 0
import json
path = "yelp_academic_dataset_business.json"
f = open(path, encoding="utf-8")
f.close()
print("found it!")

# Step 1
f = open(path)
line = f.readline()
record = json.loads(line)
print(record["name"], "|", record["city"], record["state"], "|", record["categories"])
f.close()

# Step 2
count = 0
f = open(path, encoding="utf-8")
for line in f:
    count = count + 1
f.close()
print("total businesses in file:", count)

# Step 3
count = 0
f = open(path, encoding="utf-8")
for line in f:
    record = json.loads(line)
    if record["state"] == "CA":
        count = count + 1
f.close()
print("California businesses:", count)

# Step 4
sb_cities = {"santa barbara", "goleta", "santa maria", "solvang", "buellton", "carpinteria", "guadalupe", "lompoc", "isla vista", "orcutt", "montecito", "vandenberg village", "santa ynez", "los alamos", "summerland", "los olivos"}

count = 0
f = open(path, encoding="utf-8")
for line in f:
    record = json.loads(line)
    if record["state"] == "CA" and record["city"].lower() in sb_cities:
        count = count + 1
f.close()
print("businesses in 16 SB County cities/communities:", count)

# Step 5
sb_cities = {"santa barbara", "goleta", "santa maria", "solvang", "buellton", "carpinteria", "guadalupe", "lompoc", "isla vista", "orcutt", "montecito", "vandenberg village", "santa ynez", "los alamos", "summerland", "los olivos"}
ids_boba = set()

count = 0

f = open(path, encoding="utf-8")
for line in f:
    record = json.loads(line)
    cats = record["categories"]
    if cats is None:
        continue
    cats = cats.lower()
    if record["state"] == "CA" and record["city"].lower() in sb_cities and ("bubble tea" in cats or "boba" in cats or "milk tea" in cats):
        count = count + 1
        ids_boba.add(record["business_id"])


print("boba-style shops (16 communities):", count)
print("unique boba shop ids:", len(ids_boba))

# Step 6
review_count = 0

f = open("yelp_academic_dataset_review.json", encoding="utf-8")
for line in f:
    record = json.loads(line)
    if record["business_id"] in ids_boba:
        review_count = review_count + 1
f.close()

print("boba/milk-tea reviews (16 communities):", review_count)

# Pivot/Expand Search
print("Only 19 shops that are explicitly boba and 2,972 reviews across those shops, so we needed to broaden our search.")

# Step 7
from collections import Counter

shops_by_city = Counter()
ids_drink = set()
terms = ("bubble tea", "boba", "milk tea", "coffee & tea", "juice bars")

f = open(path, encoding="utf-8")
for line in f:
    record = json.loads(line)
    if record["state"] != "CA":
        continue
    cats = record["categories"]
    if cats is None:
        continue
    cats = cats.lower()
    if any(t in cats for t in terms):
        shops_by_city[record["city"]] += 1
        ids_drink.add(record["business_id"])
f.close()

print("drink shops total:", len(ids_drink))
for city, n in shops_by_city.most_common():
    print("  ", city, "->", n)

# Step 8
review_count = 0

f = open("yelp_academic_dataset_review.json", encoding="utf-8")
for line in f:
    record = json.loads(line)
    if record["business_id"] in ids_drink:
        review_count = review_count + 1
f.close()

print("drink shop reviews total:", review_count)

# Final probing results
print("33,028 reviews across 226 shops in Santa Barbara County. Probe phase officially complete.")