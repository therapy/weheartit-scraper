import requests
import os
import re

collection = input("[ / ] collection url [example: https://weheartit.com/unethical/collections/187857915-cats]: ")
folder_name = input("[ / ] folder name [will be created if it doesnt exist (same directory as this script)]: ")

try:
    os.mkdir(folder_name)
except:
    pass

entries = []
before = 0

print("[ / ] collecting images")

while True:
    body = requests.get(f"{collection}?scrolling=true&page=1&before={before}").text

    if not body:
        break

    items = body.split("entry grid-item")
    items.pop(0)

    for item in items:
        entry = re.search('images/(.+?)/superthumb', item).group(1)
        entries.append(entry)

    before = entries[-1]

print("[ / ] downloading images")

for entry in entries:
    body = requests.get(f'https://weheartit.com/entry/{entry}').text
    image_url = re.search('property="og:image" content="(.+?)"', body).group(1)
    image_bytes = requests.get(image_url).content

    try:
        image_bytes = str(image_bytes, 'utf-8')
        print(f'[ / ] failed to download {image_url}')

    except UnicodeDecodeError:
        name = image_url.split("/")[4]
        filetype = image_url.split("/")[5]
        with open(f"{folder_name}/{name}_{filetype}", "wb+") as f:
            f.write(image_bytes)

print("[ / ] done")
