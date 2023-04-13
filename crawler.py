import requests
from urllib.parse import unquote, quote
import json
from concurrent.futures import ThreadPoolExecutor
import time


def get_id(url):
    shopid = int(url.split(".")[-2])
    itemid = int(url.split(".")[-1].split("?")[0])
    return itemid, shopid

def get_product(url):
    # get id
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
    shop_location = unquote(data["shop_location"])

    product = {
        "name": name,
        "price": price,
        "description": description,
        "review": review,
        "rating": rating,
        "type": type,
        "link": url.strip(),
        "sale_quantity": sale_quantity,
        "shop_location": shop_location
    }
    return product

def main():
    # open file json
    with open("full_urls.txt") as f:
        urls = f.readlines()
    f.close()

    idx_continue = 0
    urls = urls[idx_continue:]
    products = []

    # multithreading
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(get_product, url) for url in urls]

        products = []
        # Wait for all tasks to complete
        for i, future in enumerate(futures):
            print(f"Processing {i+idx_continue+1}/{len(futures)+idx_continue}")
            try:
                products.append(future.result())
                time.sleep(0.1)
            except Exception as exc:
                print(f"{i+1} generated an exception: {exc}")

        # write file json
        print("Writing file...")
        with open("datapiece.json", "a", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False) 

        print("Done!")
        f.close()

if __name__ == "__main__":
    main()  