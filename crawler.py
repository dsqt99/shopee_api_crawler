import requests
from urllib.parse import unquote, quote
import json


def get_id(url):
    shopid = int(url.split(".")[-2])
    itemid = int(url.split(".")[-1].split("?")[0])
    return itemid, shopid

# open file json
with open("urls.txt") as f:
    urls = f.readlines()
f.close()

continue_idx = 0
urls = urls[continue_idx:]
products = []

for i, url in enumerate(urls):
    print(f"Processing {i+continue_idx}/{len(urls)+continue_idx}")
    # get id
    try:
        itemid, shopid = get_id(url.strip())
        # get api
        api = f"https://shopee.vn/api/v4/item/get?itemid={itemid}&shopid={shopid}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }
        response = requests.get(api, headers=headers)
        data = response.json().get("data")

        # get data
        name = data["name"]
        price = data["price"]
        description = unquote(data["description"]).replace("\n", "")
        review = data["item_rating"]["rating_count"][0]
        if review == 0:
            rating = 0
        else:
            rating = round(sum([(i+1) * rate for i, rate in enumerate(data["item_rating"]["rating_count"][1:])])/review, 1)
        type = data["fe_categories"][-1]["display_name"]
        sale_quantity = data["historical_sold"]
        shop_name = unquote(data["shop_location"])

        product = {
            "name": name,
            "price": price,
            "description": description,
            "review": review,
            "rating": rating,
            "type": type,
            "link": url.strip(),
            "sale_quantity": sale_quantity,
            "shop_name": shop_name
        }
        products.append(product)
    except:
        continue


# write file json
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=4)
    
f.close()